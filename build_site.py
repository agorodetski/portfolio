"""Build Avi's dependency-free, multi-page portfolio into the Site's static dist directory."""
from pathlib import Path
from html import escape
import json
import re
import shutil
import struct
import sys
import zlib

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
SITE = 'Avi Gorodetski'

# The public address (no trailing slash). The site is live on GitHub Pages at this address; change it
# here if a custom domain replaces it. When set, the build emits canonical/og:url/og:image tags and
# sitemap.xml, and the 404 page uses absolute links so it keeps its styling on a subpath host. Left
# empty, those are skipped because they need absolute URLs and the site otherwise uses relative URLs.
SITE_URL = 'https://agorodetski.github.io/portfolio'

# One place to change the public contact address (footer + contact page).
EMAIL = 'agorodetski@tulane.edu'

OG_IMAGE = 'assets/og-image.jpg'


def image_size(path: Path):
    """Return (width, height) of a JPEG or PNG without third-party packages."""
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', data[16:24])
    if data[:2] == b'\xff\xd8':
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                height, width = struct.unpack('>HH', data[i + 5:i + 9])
                return width, height
            i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
    raise ValueError(f'Unsupported image: {path}')


def image_problem(path: Path):
    """Return a message if a JPEG or PNG is truncated or corrupt (it would render as a blank box), else None."""
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        i = 8
        while i + 12 <= len(data):
            length = struct.unpack('>I', data[i:i + 4])[0]
            end = i + 12 + length
            kind = data[i + 4:i + 8]
            if end > len(data):
                return 'PNG data is truncated'
            if zlib.crc32(data[i + 4:i + 8 + length]) != struct.unpack('>I', data[i + 8 + length:end])[0]:
                return f'PNG {kind.decode("latin-1")} chunk is corrupt'
            if kind == b'IEND':
                return None
            i = end
        return 'PNG data is truncated'
    if data[:2] == b'\xff\xd8':
        return None if data.rstrip(b'\x00')[-2:] == b'\xff\xd9' else 'JPEG data is truncated'
    return 'unrecognized image format'


def sync_image_dimensions(markup: str) -> str:
    """Keep every <img> width/height equal to the real file so they can never drift."""
    def fix(match):
        tag = match.group(0)
        src = re.search(r'src="([^"]*assets/[^"]+)"', tag)
        if not src:
            return tag
        file = ROOT / 'assets' / src.group(1).split('assets/', 1)[1]
        if not file.exists():
            return tag
        width, height = image_size(file)
        tag = re.sub(r'\swidth="\d+"', f' width="{width}"', tag)
        tag = re.sub(r'\sheight="\d+"', f' height="{height}"', tag)
        return tag
    return re.sub(r'<img\b[^>]*>', fix, markup)


UPDATE_FIELDS = ('date', 'dateLabel', 'category', 'title', 'summary', 'source', 'url')


def load_updates() -> list:
    """Read updates.json and enforce the rules documented in the README, so a bad edit fails the build."""
    items = json.loads((ROOT / 'updates.json').read_text())
    problems = []
    if not isinstance(items, list) or not 1 <= len(items) <= 6:
        problems.append('updates.json must be a list of 1 to 6 items')
        items = items if isinstance(items, list) else []
    for n, item in enumerate(items, 1):
        for field in UPDATE_FIELDS:
            if not isinstance(item.get(field), str) or not item[field].strip():
                problems.append(f'update {n}: missing or empty "{field}"')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(item.get('date', ''))):
            problems.append(f'update {n}: "date" must be an ISO date (YYYY-MM-DD)')
        if not str(item.get('url', '')).startswith('https://'):
            problems.append(f'update {n}: "url" must be a public https:// address')
    if problems:
        print('updates.json check failed:', *problems, sep='\n  ')
        sys.exit(1)
    return items


UPDATES = load_updates()


def render_updates(limit: int) -> str:
    """Render the first `limit` curated updates as static cards, so they need no JavaScript or extra request."""
    cards = []
    for item in UPDATES[:limit]:
        title, source = escape(item['title']), escape(item['source'])
        cards.append(
            '<article class="update-card">'
            f'<div class="update-meta"><span>{escape(item["category"])}</span>'
            f'<time datetime="{escape(item["date"], quote=True)}">{escape(item["dateLabel"])}</time></div>'
            f'<h3>{title}</h3><p>{escape(item["summary"])}</p>'
            f'<a class="update-link" href="{escape(item["url"], quote=True)}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="{title} — view on {source}">View on {source}</a>'
            '</article>'
        )
    return ''.join(cards)


PAGES = []


def page(path: str, title: str, description: str, active: str, body: str, base: str = None, indexable: bool = True,
         document_title: str = None) -> None:
    """Write one page. `title` is the short page name; `document_title` overrides the full <title> (used by the homepage)."""
    full_title = document_title or f'{title} | {SITE}'
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    depth = len(Path(path).parts) - 1
    if base is None:
        base = '../' * depth
    if indexable:
        PAGES.append(path)
    page_url = SITE_URL + '/' + ('' if path == 'index.html' else path.removesuffix('index.html')) if SITE_URL else ''
    canonical = f'\n  <link rel="canonical" href="{page_url}">\n  <meta property="og:url" content="{page_url}">' if page_url and indexable else ''
    og_image = (f'\n  <meta property="og:image" content="{SITE_URL}/{OG_IMAGE}">'
                f'\n  <meta name="twitter:image" content="{SITE_URL}/{OG_IMAGE}">') if SITE_URL else ''
    twitter_card = 'summary_large_image' if SITE_URL else 'summary'
    body = body.replace('@@EMAIL@@', EMAIL).replace('@@BASE@@', base)
    body = re.sub(r'@@UPDATES:(\d+)@@', lambda m: render_updates(int(m.group(1))), body)
    def nav_link(label: str, href: str, class_name: str = '') -> str:
        class_attr = f' class="{class_name}"' if class_name else ''
        # "page" only on the page itself; a section link (Work on a case study) is "true", not "page".
        current = '' if label != active else (' aria-current="page"' if href == path else ' aria-current="true"')
        return f'<a{class_attr} href="{base}{href}"{current}>{label}</a>'

    work_link = nav_link('Work', 'work/index.html', 'nav-work-link')
    work_subnav = ''.join(
        f'<a href="{base}{href}">{label}</a>' for label, href in [
            ('AlphaSights', 'work/alphasights/index.html'),
            ('GiVV', 'work/givv/index.html'),
            ('TUCP', 'work/tucp/index.html'),
            ('BBYO', 'work/bbyo/index.html'),
            ('Strong City', 'work/strong-city/index.html'),
        ]
    )
    nav = ''.join([
        nav_link('Home', 'index.html'),
        nav_link('Now', 'now/index.html', 'nav-now'),
        f'<div class="nav-group">{work_link}<div class="nav-submenu" role="group" aria-label="Work case studies">{work_subnav}</div></div>',
        nav_link('Experience', 'experience/index.html'),
        nav_link('About', 'about/index.html'),
        nav_link('Contact', 'contact/index.html'),
    ])
    markup = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#182b49">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta property="og:title" content="{escape(full_title, quote=True)}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE}">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="{twitter_card}">
  <meta name="author" content="{SITE}">{canonical}{og_image}
  <title>{escape(full_title)}</title>
  <link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
  <link rel="stylesheet" href="{base}styles.css">
  <noscript><style>@media (max-width: 780px) {{ .site-nav {{ display: flex !important; }} .nav-toggle {{ display: none !important; }} }}</style></noscript>
  <script src="{base}script.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{base}index.html" aria-label="Avi Gorodetski, home">avi<span>.</span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="nav-toggle-label">Menu</span> <span class="nav-toggle-icon" aria-hidden="true">+</span></button>
      <nav class="site-nav" id="site-nav" aria-label="Main navigation">{nav}</nav>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer"><div class="container footer-inner"><span>© <span id="year">2026</span> Avi Gorodetski</span><span>New Orleans / New York / DC</span><a href="mailto:{EMAIL}">Email me <span aria-hidden="true">↗</span></a></div></footer>
</body>
</html>
'''
    if not indexable:
        markup = markup.replace('<meta name="author"', '<meta name="robots" content="noindex">\n  <meta name="author"')
    target.write_text(sync_image_dimensions(markup))


home = '''
<section class="hero container">
  <div class="hero-copy"><p class="eyebrow">Avi Gorodetski / Portfolio</p>
    <h1>Strategy, operations, and community.</h1>
    <p class="lede">I’m a Tulane senior with experience across client service, social-impact entrepreneurship, large-scale programming, and global youth leadership.</p>
    <div class="actions"><a class="button button-primary" href="work/index.html">Explore my work <span aria-hidden="true">↗</span></a><a class="text-link" href="assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">View résumé <span aria-hidden="true">↗</span></a></div>
    <p class="hero-aside">Tulane University / Sociology + Social Policy &amp; Practice / Class of 2027</p>
  </div>
  <figure class="hero-photo"><img src="assets/avi-headshot.jpg" alt="Avi Gorodetski smiling outdoors" width="896" height="1343" fetchpriority="high"><figcaption>New Orleans, Louisiana / Currently</figcaption></figure>
</section>
<div class="fact-band"><div class="container fact-grid"><div><strong>$15K</strong><span>GiVV pitch win</span></div><div><strong>2K</strong><span>Students at a Tulane University Campus Programming concert</span></div><div><strong>25</strong><span>Countries in BBYO’s global Jewish teen network</span></div></div></div>
<section class="section container">
  <div class="section-heading"><div><p class="eyebrow">Selected work / 01</p><h2>Projects and leadership.</h2></div><p>A closer look at what I built, led, and learned.</p></div>
  <div class="feature-grid">
    <a class="feature-card feature-wide" href="work/alphasights/index.html"><div class="feature-media"><img src="assets/alphasights-team.jpeg" alt="Avi with fellow Tulane students at the AlphaSights New York office" loading="lazy" width="1200" height="800"></div><div class="feature-text"><span class="kicker">Client service / 2026</span><h3>AlphaSights</h3><p>Managing fast-moving private equity research projects and connecting clients with the right industry expertise.</p><span class="feature-result">30+ client–expert consultations</span><span class="card-link">View case study <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card feature-large" href="work/givv/index.html"><div class="feature-media"><img src="assets/givv-team.jpg" alt="GiVV team with its first-place $15,000 award" loading="lazy" width="2048" height="1697"></div><div class="feature-text"><span class="kicker">Entrepreneurship / 2026</span><h3>GiVV</h3><p>Building a more social, accessible way for students to support local nonprofits.</p><span class="feature-result">$15K first-place pitch award</span><span class="card-link">View case study <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card" href="work/tucp/index.html"><div class="feature-media"><img src="assets/tucp-team.jpeg" alt="Avi with members of Tulane University Campus Programming on campus" loading="lazy" width="1536" height="2048"></div><div class="feature-text"><span class="kicker">Campus programming / 2024–present</span><h3>TUCP</h3><p>Tulane University Campus Programming: building the teams and systems behind concerts, festivals, speakers, and comedy.</p><span class="card-link">View case study <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card" href="work/bbyo/index.html"><div class="feature-media"><img src="assets/bbyo-speaking.jpg" alt="Avi speaking at BBYO International Convention" loading="lazy" width="2048" height="1367"></div><div class="feature-text"><span class="kicker">Global leadership / 2022–23</span><h3>BBYO</h3><p>Leading a 1,200+ teen network across 25 countries for the global Jewish teen movement.</p><span class="card-link">View case study <span aria-hidden="true">↗</span></span></div></a>
  </div>
  <p class="section-end"><a class="text-link" href="work/index.html">See all selected work <span aria-hidden="true">↗</span></a></p>
</section>
<section class="section updates-section"><div class="container">
  <div class="section-heading"><div><p class="eyebrow">Recently / 02</p><h2>What I’m doing now.</h2></div><p>A short, curated view of current work, community, and the music in rotation.</p></div>
  <div class="updates-grid">@@UPDATES:3@@</div>
  <p class="section-end"><a class="button button-primary" href="now/index.html">See all current updates <span aria-hidden="true">↗</span></a></p>
</div></section>
<section class="section section-ink"><div class="container invitation"><div><p class="eyebrow">Currently</p><h2>Exploring what comes after Tulane.</h2></div><div><p>I’m interested in strategy, philanthropy, program management, and social-impact roles in New York or Washington, DC.</p><a class="button button-light" href="contact/index.html">Contact <span aria-hidden="true">↗</span></a></div></div></section>
'''
page('index.html','Home','Avi Gorodetski builds teams, programs, and experiences across social impact, global leadership, and client service.','Home',home,
     document_title=f'{SITE} | Strategy, operations, and community')

work = '''
<section class="page-intro container"><p class="eyebrow">Selected work / Case studies</p><h1>What I’ve built and led.</h1><p class="lede">Five in-depth case studies showing the challenge, my contribution, and the measurable result—not a complete résumé.</p></section>
<section class="container section section-tight"><div class="work-list">
  <article class="work-row"><a class="work-image" href="alphasights/index.html"><img src="../assets/alphasights-team.jpeg" alt="Avi with fellow Tulane students at the AlphaSights New York office" width="1200" height="800"></a><div class="work-copy"><span class="kicker">01 / Client service · Summer 2026</span><h2>AlphaSights</h2><p>Managed 10+ concurrent research projects for private equity clients, recruited and vetted 100+ industry experts, and facilitated 30+ client–expert consultations.</p><a class="text-link" href="alphasights/index.html">Explore AlphaSights <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image" href="givv/index.html"><img src="../assets/givv-team.jpg" alt="GiVV team holding the first-place award" loading="lazy" width="2048" height="1697"></a><div class="work-copy"><span class="kicker">02 / Entrepreneurship · 2026–present</span><h2>GiVV</h2><p>Co-founded a social marketplace concept to connect Tulane students with New Orleans nonprofits. Fifteen-plus research interviews, a semester of building, and a first-place pitch earned our team $15,000 in startup funding.</p><a class="text-link" href="givv/index.html">Explore GiVV <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image work-image-portrait" href="tucp/index.html"><img src="../assets/tucp-team.jpeg" alt="Avi with members of Tulane University Campus Programming on campus" loading="lazy" width="1536" height="2048"></a><div class="work-copy"><span class="kicker">03 / Campus programming · 2024–present</span><h2>Tulane University Campus Programming</h2><p>Tulane University Campus Programming (TUCP) creates concerts, speakers, comedy, and campus traditions. I helped plan a Natasha Bedingfield concert for roughly 2,000 students, produced a 1,500-person festival, launched TUCP’s first online storefront, and now lead the organization as president.</p><a class="text-link" href="tucp/index.html">Explore TUCP <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image" href="bbyo/index.html"><img src="../assets/bbyo-convention.jpg" alt="BBYO International Convention stage seen from the audience" loading="lazy" width="2048" height="1365"></a><div class="work-copy"><span class="kicker">04 / Global leadership · 2022–23</span><h2>BBYO</h2><p>At BBYO, a global Jewish teen movement, I served as International Teen President, supported a leadership network of 1,200+ teens across 25 countries, and helped bring 4,500 people together for International Convention.</p><a class="text-link" href="bbyo/index.html">Explore BBYO <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image" href="strong-city/index.html"><img src="../assets/strong-city-field-day.jpeg" alt="Avi with the Strong City team at Field Day" loading="lazy" width="2048" height="1365"></a><div class="work-copy"><span class="kicker">05 / Community engagement · 2024–present</span><h2>Strong City</h2><p>Building nonprofit partnerships and helping coordinate Field Day for 100+ New Orleans youth and a Thanksgiving Drive that packs 600+ food boxes for local families.</p><a class="text-link" href="strong-city/index.html">Explore Strong City <span aria-hidden="true">↗</span></a></div></article>
</div></section>
<section class="section soft-section"><div class="container narrow"><p class="eyebrow">Additional work</p><h2>Grantmaking and research.</h2><div class="two-cards"><article><span class="kicker">The Tow Foundation</span><h3>Youth mental health funding</h3><p>Reviewed grant applications for a $10 million innovation fund focused on expanding mental health support for young people.</p></article><article><span class="kicker">Tulane University</span><h3>Qualitative research and editing</h3><p>Analyzed interview narratives in Jewish Studies research and substantively edited a sociology manuscript for structure and clarity.</p></article></div></div></section>
'''
page('work/index.html','Selected Work','Explore Avi Gorodetski’s work with AlphaSights, GiVV, BBYO, TUCP, Strong City Tulane, and The Tow Foundation.','Work',work)

alphasights = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">01 / AlphaSights · Summer Associate</p><h1>Finding the right expertise, fast.</h1><p class="lede">Client service for private equity teams making high-stakes decisions on tight timelines.</p><div class="story-facts"><div><strong>10+</strong><span>Concurrent projects</span></div><div><strong>100+</strong><span>Experts recruited</span></div><div><strong>30+</strong><span>Consultations</span></div></div></section>
<figure class="story-hero"><img src="../../assets/alphasights-team.jpeg" alt="Avi with fellow Tulane students at the AlphaSights New York office" width="1200" height="800"><figcaption>With fellow Tulane students at AlphaSights in New York, summer 2026.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The work</p><h2>Turn a question into the right conversation.</h2></div><div class="story-prose"><p>On AlphaSights’ Private Equity team, I managed more than 10 research projects at once. Each began with a client’s investment question and a tight deadline. My role was to understand the context quickly, identify the specific experience that would be useful, and keep every workstream moving.</p><p>I recruited and vetted more than 100 industry experts, evaluating both the relevance of their backgrounds and their ability to speak directly to a client’s needs.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">Client service</p><h2>Coordinate clearly under pressure.</h2></div><div class="story-prose"><p>I facilitated more than 30 client–expert consultations, managing communication, scheduling, and shifting priorities across clients and experts. The experience sharpened how I ask questions, make tradeoffs, and build trust in fast-moving environments.</p><p>I left the summer with a full-time return offer and a stronger understanding of the relationship work behind good research and decision-making.</p></div></div></section>
<div class="container next-story"><span>Next story</span><a href="../givv/index.html">Building a new way to give <span aria-hidden="true">↗</span></a></div>
'''
page('work/alphasights/index.html','AlphaSights','Avi Gorodetski’s client service experience supporting private equity research at AlphaSights in New York.','Work',alphasights)

now = '''
<section class="page-intro container"><p class="eyebrow">Now / Current updates</p><h1>What I’m doing, building, and listening to.</h1><p class="lede">A living snapshot of recent milestones, current projects, and personal interests—edited for signal, not volume.</p></section>
<section class="section container section-tight">
  <div class="now-intro"><p class="eyebrow">Current notes</p><p>This page brings together selected updates from Tulane University Campus Programming (TUCP), GiVV, and Strong City, plus occasional notes from LinkedIn and my monthly Spotify habit.</p></div>
  <h2 class="visually-hidden">Latest updates</h2>
  <div class="updates-grid updates-grid-full">@@UPDATES:6@@</div>
</section>
<section class="section soft-section"><div class="container source-strip"><div><p class="eyebrow">Follow along</p><h2>Elsewhere.</h2></div><div class="source-links"><a href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://www.geauxtucp.com/" target="_blank" rel="noopener noreferrer">TUCP</a><a href="https://www.instagram.com/thegivvapp/" target="_blank" rel="noopener noreferrer">GiVV on Instagram</a><a href="https://www.mystrongcity.org/" target="_blank" rel="noopener noreferrer">Strong City</a><a href="https://open.spotify.com/search/avigorodetski" target="_blank" rel="noopener noreferrer">Spotify</a><a href="https://github.com/agorodetski/portfolio" target="_blank" rel="noopener noreferrer">GitHub</a></div></div></section>
'''
page('now/index.html','Now','Current work, community projects, ideas, and monthly listening from Avi Gorodetski.','Now',now)

givv = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">02 / GiVV · Co-founder &amp; COO</p><h1>From student research to a $15K pitch win.</h1><p class="lede">Our team developed a social marketplace concept that connects Tulane students with New Orleans nonprofits.</p><div class="story-facts"><div><strong>15+</strong><span>Student interviews</span></div><div><strong>$15K</strong><span>First-place award</span></div><div><strong>2026</strong><span>Founded at Tulane</span></div></div></section>
<figure class="story-hero"><img src="../../assets/givv-pitch.jpg" alt="GiVV team presenting its final startup pitch at Tulane" width="2048" height="1645"><figcaption>GiVV’s final pitch at Tulane’s Startup Strategy Lab, April 2026.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The idea</p><h2>Lower the barriers to local giving.</h2></div><div class="story-prose"><p>GiVV is a social marketplace concept connecting Tulane students with local nonprofits through micro-donations, social sharing, and student-organization competitions.</p><p>In 15+ interviews, students pointed to limited funds, questions of trust, and decision fatigue. Personal connection and seeing friends participate made a difference. Those findings shaped our approach.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">My contribution</p><h2>Building the work behind the pitch.</h2></div><div class="story-prose"><p>As co-founder and COO, I led operations throughout our semester-long startup incubator, contributed to strategy and user research, and developed the social media strategy and content. My teammates and I built and presented the concept together.</p><p>On April 28, 2026, GiVV placed first in Tulane’s Startup Strategy Lab final pitch competition and won $15,000 in startup funding. It was a proof point for the idea—and for what a committed team can do in one semester.</p></div></div></section>
<figure class="story-hero story-photo-end"><img src="../../assets/givv-team.jpg" alt="GiVV founders and supporters celebrating with the $15,000 first-place check" loading="lazy" width="2048" height="1697"><figcaption>The GiVV team after the first-place award.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../tucp/index.html">Programming for an entire campus <span aria-hidden="true">↗</span></a></div>
'''
page('work/givv/index.html','GiVV','How Avi Gorodetski and the GiVV team developed a student-to-nonprofit giving concept and won Tulane’s $15,000 startup pitch award.','Work',givv)

tucp = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">03 / Tulane University Campus Programming · President</p><h1>Programming for an entire campus.</h1><p class="lede">Tulane University Campus Programming (TUCP) produces concerts, festivals, comedy, and speakers—built by students for the Tulane community.</p><div class="story-facts"><div><strong>~2K</strong><span>Concert attendees</span></div><div><strong>200+</strong><span>Organization members</span></div><div><strong>1.5K</strong><span>Festival attendees</span></div></div></section>
<figure class="story-hero story-hero-portrait"><img src="../../assets/tucp-team.jpeg" alt="Avi with members of Tulane University Campus Programming on campus" width="1536" height="2048"><figcaption>With members of the TUCP team on Tulane’s campus.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">Event scale</p><h2>From the run of show to the crowd.</h2></div><div class="story-prose"><p>As part of TUCP’s board, I helped plan a Natasha Bedingfield concert attended by roughly 2,000 students. I also led TGIO 2025, a campus festival for about 1,500 students with vendors, food trucks, merchandise, and live entertainment.</p><p>The visible result is one night on campus. The work behind it is months of coordination, budgeting, communication, and contingency planning.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">Building the organization</p><h2>Make the systems match the ambition.</h2></div><div class="story-prose"><p>As Lagniappe Chair, I helped redesign the role around philanthropy, merchandise, sponsorship, and fundraising. I launched TUCP’s first online storefront, developed merchandise strategy, and supported sponsorship outreach.</p><p>Now, as president, I lead a 15+ member board and a 200+ member organization producing concerts, comedy, speakers, and campus traditions.</p></div></div></section>
<div class="container next-story"><span>Next story</span><a href="../bbyo/index.html">Leading a global teen community <span aria-hidden="true">↗</span></a></div>
'''
page('work/tucp/index.html','TUCP','How Avi Gorodetski helps lead Tulane University Campus Programming and execute large-scale campus events.','Work',tucp)

bbyo = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">04 / BBYO · International Teen President</p><h1>Leading a network across 25 countries.</h1><p class="lede">One year leading within BBYO, a global Jewish teen movement: supporting local chapters and helping plan a 4,500-person convention.</p><div class="story-facts"><div><strong>1,200+</strong><span>Teen leaders</span></div><div><strong>25</strong><span>Countries</span></div><div><strong>750+</strong><span>Chapters</span></div></div></section>
<figure class="story-hero"><img src="../../assets/bbyo-speaking.jpg" alt="Avi speaking at a BBYO International Convention podium alongside a fellow teen leader" width="2048" height="1367"><figcaption>Speaking at BBYO International Convention in 2023.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The role</p><h2>Coordinate globally. Support locally.</h2></div><div class="story-prose"><p>I deferred a year of college to serve as BBYO’s International Teen President. I led a board of 10 peers and worked with a network of more than 1,200 teen leaders in 25 countries, supporting leadership development and engagement across more than 750 chapters.</p><p>Traveling to 13 countries and 20 states taught me that a global organization depends on strong local leaders. My job was to listen, share context, and help those leaders act.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">The scale</p><h2>Convention planning at scale.</h2></div><div class="story-prose"><p>Alongside governance and co-managing a $60,000 budget, I helped lead a 250+ person team executing a five-day International Convention for 4,500 attendees. I also spoke on BBYO stages before audiences of 5,000+.</p><p>The work taught me to set a clear direction, distribute ownership, and keep a large team moving.</p></div></div></section>
<figure class="story-hero story-photo-end"><img src="../../assets/bbyo-convention.jpg" alt="Wide view of BBYO International Convention stage with audience in the foreground" loading="lazy" width="2048" height="1365"><figcaption>A view from the audience at International Convention.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../strong-city/index.html">Community work built on relationships <span aria-hidden="true">↗</span></a></div>
'''
page('work/bbyo/index.html','BBYO Leadership','Avi Gorodetski’s year as BBYO International Teen President, leading a global network of 1,200+ teen leaders.','Work',bbyo)

# The Thanksgiving Drive photo (assets/strong-city-thanksgiving.png) was removed because the committed
# file was corrupt (truncated PNG data) and rendered as a blank box. To restore it, re-export the original
# photo as a ~1600px JPEG, add it to assets/, and re-add a <figure> after the Thanksgiving Drive section.
strong_city = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">05 / Strong City · Engagement Director</p><h1>Community work built on relationships.</h1><p class="lede">Connecting Tulane students with New Orleans organizations through sustained partnerships and large-scale service.</p><div class="story-facts"><div><strong>100+</strong><span>Youth at Field Day</span></div><div><strong>600+</strong><span>Food boxes packed</span></div><div><strong>2024–</strong><span>Strong City leadership</span></div></div></section>
<figure class="story-hero"><img src="../../assets/strong-city-field-day.jpeg" alt="Avi with the Strong City team at Field Day" width="2048" height="1365"><figcaption>The Strong City team at Field Day, the organization’s largest annual event.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">Field Day</p><h2>Bring campus and community together.</h2></div><div class="story-prose"><p>Strong City’s annual Field Day brings more than 100 young people from across New Orleans to Tulane for a day of activities and connection.</p><p>My work focuses on the relationships and coordination that make programs like this possible: partnering with local nonprofits, organizing students, and keeping community priorities at the center.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">Thanksgiving Drive</p><h2>Turn a big goal into a clear operation.</h2></div><div class="story-prose"><p>Each year, the Thanksgiving Drive coordinates volunteers to pack more than 600 boxes of nonperishable food and produce for families across New Orleans.</p><p>It is community engagement at its most practical: many people, many moving pieces, and a tangible result.</p></div></div></section>
<div class="container next-story"><span>Next story</span><a href="../alphasights/index.html">Finding the right expertise, fast <span aria-hidden="true">↗</span></a></div>
'''
page('work/strong-city/index.html','Strong City','Avi Gorodetski’s community engagement work with Strong City in New Orleans.','Work',strong_city)

about = '''
<section class="page-intro container"><p class="eyebrow">About / Background</p><h1>About Avi.</h1><p class="lede">A sociology student, operator, community builder, and very committed monthly playlist maker.</p></section>
<section class="section container about-grid"><div class="about-photo"><img src="../assets/avi-headshot.jpg" alt="Portrait of Avi Gorodetski outdoors" width="896" height="1343"></div><div class="about-text"><p class="eyebrow">Background</p><h2>Virginia to New Orleans.</h2><p>I’m a first-generation American from Northern Virginia and a senior at Tulane University, where I study Sociology and Social Policy &amp; Practice with minors in Jewish Studies and Strategy, Leadership &amp; Analytics.</p><p>My studies make me curious about how institutions and communities shape people’s lives. Outside the classroom, I’ve focused on the practical side of that question: building programs, supporting nonprofits, and creating the conditions for people to connect.</p><p>My experience spans a global youth organization, a private equity client-service team, New Orleans nonprofit partnerships, and a startup I founded with friends. I like complex work that calls for both empathy and a good plan.</p><a class="text-link" href="../experience/index.html">Explore my experience <span aria-hidden="true">↗</span></a></div></section>
<section class="section soft-section"><div class="container"><p class="eyebrow">Outside the résumé</p><h2>Current interests.</h2><div class="personal-grid"><article><span class="personal-number">01 / MUSIC</span><h3>12 playlists a year.</h3><p>I make a new Spotify playlist every month. It’s how I keep track of a place, a season, and the people who were there.</p><span class="personal-aside">Spotify / @avigorodetski</span></article><article><span class="personal-number">02 / TRAVEL</span><h3>32 countries so far.</h3><p>My goal is 50 countries by 50. I’m at 32 and always planning the next one.</p><div class="travel-meter" role="meter" aria-label="Countries visited toward a goal of 50" aria-valuemin="0" aria-valuemax="50" aria-valuenow="32"><span></span></div><span class="personal-aside">32 / 50 countries</span></article><article><span class="personal-number">03 / FOOD</span><h3>Always choosing the restaurant.</h3><p>Exploring a place usually starts with figuring out what to eat. New Orleans has been especially good for this habit.</p></article></div></div></section>
<section class="section container closing"><p class="eyebrow">How I work</p><h2>Clear context, shared ownership, strong execution.</h2><p>Whether I’m organizing a campus event or working through an uncertain idea with a team, I care about clear communication and the details that keep work moving.</p><a class="button button-primary" href="../contact/index.html">Contact <span aria-hidden="true">↗</span></a></section>
'''
page('about/index.html','About Avi','Meet Avi Gorodetski: sociology student, community builder, monthly playlist maker, and traveler with a goal of 50 countries by 50.','About',about)

experience = '''
<section class="page-intro container"><p class="eyebrow">Experience / Résumé view</p><h1>Experience.</h1><p class="lede">A chronological overview of my professional roles, leadership, education, and skills. Visit Work for the deeper case studies behind selected experiences.</p><div class="actions"><a class="button button-primary" href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">View résumé <span aria-hidden="true">↗</span></a><a class="text-link" href="../work/index.html">Explore case studies <span aria-hidden="true">↗</span></a><a class="text-link" href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a></div></section>
<section class="section container experience-layout"><div class="experience-heading"><p class="eyebrow">Professional experience</p><h2>What I’ve done.</h2></div><div class="experience-list">
<article><div class="role-top"><span>2026</span><span>New York, NY</span></div><h3>AlphaSights</h3><p class="role-name">Summer Associate, Client Services · Private Equity</p><p>Managed 10+ concurrent projects for private equity clients, recruited and vetted 100+ industry experts, and facilitated 30+ client–expert consultations to support investment research.</p><a class="text-link role-link" href="../work/alphasights/index.html">AlphaSights case study <span aria-hidden="true">↗</span></a></article>
<article><div class="role-top"><span>2026–present</span><span>New Orleans, LA</span></div><h3>GiVV Inc.</h3><p class="role-name">Co-founder</p><p>Led operations throughout a startup incubator and developed social content and strategy for a giving platform concept. Our team won first place and $15,000 in startup funding in the final pitch competition.</p><a class="text-link role-link" href="../work/givv/index.html">GiVV case study <span aria-hidden="true">↗</span></a></article>
<article><div class="role-top"><span>2025</span><span>New York, NY</span></div><h3>The Tow Foundation</h3><p class="role-name">Innovation Fund Community Advisor</p><p>Reviewed and scored grant applications for an innovation fund investing in expanded youth mental health support.</p></article>
<article><div class="role-top"><span>2024–present</span><span>New Orleans, LA</span></div><h3>Tulane Technology Services</h3><p class="role-name">Classroom Experience Assistant</p><p>Support classroom technology and troubleshoot issues to keep learning environments running smoothly.</p></article>
<article><div class="role-top"><span>2024–2025</span><span>New Orleans, LA</span></div><h3>Tulane University</h3><p class="role-name">Substantive Editor · Research Assistant</p><p>Edited a sociology manuscript for structure and clarity, and analyzed qualitative interview narratives in Jewish Studies research.</p></article>
</div></section>
<section class="section soft-section"><div class="container experience-layout"><div class="experience-heading"><p class="eyebrow">Leadership</p><h2>What I’ve led.</h2></div><div class="experience-list">
<article id="tucp"><div class="role-top"><span>2026–present</span><span>Tulane University</span></div><h3>Tulane University Campus Programming</h3><p class="role-name">President · Former Lagniappe Chair</p><p>Lead a 15+ member board and a 200+ member organization in concerts, comedy, and speaker programming. Previously helped plan a roughly 2,000-person Natasha Bedingfield concert, produced a 1,500-person festival, and launched TUCP’s first online storefront.</p><a class="text-link role-link" href="../work/tucp/index.html">TUCP case study <span aria-hidden="true">↗</span></a></article>
<article><div class="role-top"><span>2024–present</span><span>New Orleans, LA</span></div><h3>Strong City Tulane</h3><p class="role-name">Engagement Director · Former Program Coordinator</p><p>Build relationships with New Orleans nonprofit partners and develop student engagement initiatives, including Field Day for 100+ local youth and a Thanksgiving Drive packing 600+ food boxes for families.</p><a class="text-link role-link" href="../work/strong-city/index.html">Strong City case study <span aria-hidden="true">↗</span></a></article>
<article><div class="role-top"><span>2022–2023</span><span>Global</span></div><h3>BBYO</h3><p class="role-name">International Teen President</p><p>Led a 10-member board and worked with 1,200+ teen leaders across 25 countries in BBYO, a global Jewish teen movement. Co-managed a $60,000 budget and helped execute International Convention for 4,500 attendees.</p><a class="text-link role-link" href="../work/bbyo/index.html">BBYO case study <span aria-hidden="true">↗</span></a></article>
</div></div></section>
<section class="section container credentials"><div><p class="eyebrow">Education</p><h2>Tulane University</h2><p>BA, Sociology and Social Policy &amp; Practice · Minors in Jewish Studies and Strategy, Leadership &amp; Analytics · Expected May 2027</p><p>GPA 3.98/4.0 · Dean’s List</p></div><div><p class="eyebrow">Languages &amp; skills</p><h3>Connecting across contexts.</h3><p>Native English and Hebrew; intermediate Spanish. Experience with Salesforce, Canva, Microsoft Office, and Google Workspace.</p><a class="text-link" href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">Full résumé <span aria-hidden="true">↗</span></a></div></section>
'''
page('experience/index.html','Experience','Avi Gorodetski’s experience in client service, social-impact entrepreneurship, campus leadership, grant review, and research.','Experience',experience)

contact = '''
<section class="contact-page container"><p class="eyebrow">Contact / Reach out</p><h1>Get in touch.</h1><p class="lede">For recruiting, partnerships, startup conversations, or anything else: email is best.</p><div class="contact-options"><a href="mailto:@@EMAIL@@"><span>Email</span><strong>@@EMAIL@@</strong><span aria-hidden="true">↗</span></a><a href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span><strong>avigorodetski</strong><span aria-hidden="true">↗</span></a><a href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener"><span>Résumé</span><strong>Download PDF</strong><span aria-hidden="true">↗</span></a></div><p class="contact-footnote">New Orleans, Louisiana · Graduating from Tulane in May 2027</p></section>
'''
page('contact/index.html','Contact','Get in touch with Avi Gorodetski by email or LinkedIn, and view the résumé.','Contact',contact)

not_found = '''
<section class="contact-page container"><p class="eyebrow">404 / Not found</p><h1>That page isn’t here.</h1><p class="lede">The link may be out of date. Head back to the homepage or browse selected work.</p><div class="actions"><a class="button button-primary" href="@@BASE@@index.html">Home <span aria-hidden="true">↗</span></a><a class="text-link" href="@@BASE@@work/index.html">Selected work</a></div></section>
'''
# A 404 page is served from whatever URL was mistyped, so relative links would break. It uses the
# public address when SITE_URL is set, otherwise root-relative paths (fine on a domain root).
page('404.html', 'Page not found', 'This page could not be found.', '', not_found,
     base=(SITE_URL + '/') if SITE_URL else '/', indexable=False)

# robots.txt always; sitemap.xml only when absolute URLs are possible.
robots = 'User-agent: *\nAllow: /\n'
sitemap_path = ROOT / 'sitemap.xml'
if SITE_URL:
    robots += f'\nSitemap: {SITE_URL}/sitemap.xml\n'
    urls = ''.join(
        f'  <url><loc>{SITE_URL}/{"" if p == "index.html" else p.removesuffix("index.html")}</loc></url>\n'
        for p in PAGES
    )
    sitemap_path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n'
    )
elif sitemap_path.exists():
    sitemap_path.unlink()
(ROOT / 'robots.txt').write_text(robots)

# Mirror the authored static site into the directory used by Sites hosting.
DIST.mkdir(exist_ok=True)
FILES = ['index.html', '404.html', 'styles.css', 'script.js', 'favicon.svg', 'apple-touch-icon.png', 'updates.json', 'robots.txt', 'sitemap.xml']
for name in FILES:
    src = ROOT / name
    if src.exists():
        shutil.copy2(src, DIST / name)
    elif (DIST / name).exists():
        (DIST / name).unlink()
for directory in ['work', 'now', 'about', 'experience', 'contact', 'assets']:
    src = ROOT / directory
    dst = DIST / directory
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def check_site(site_root: Path) -> list:
    """Return problems: any local link, image, script, or data file a page references that is missing."""
    problems = []
    for html_file in sorted(site_root.rglob('*.html')):
        if site_root == ROOT and DIST in html_file.parents:
            continue
        for ref in re.findall(r'(?:href|src)="([^"]+)"', html_file.read_text()):
            if re.match(r'(?:[a-z][a-z0-9+.-]*:|#|/)', ref, re.I):
                continue  # external URL, anchor, or root-relative path
            if not (html_file.parent / ref.split('#')[0].split('?')[0]).resolve().exists():
                problems.append(f'{html_file.relative_to(ROOT)}: missing {ref}')
    return problems


# Fail loudly if either copy of the site references a file that is not there, or if an image is damaged.
problems = check_site(ROOT) + check_site(DIST)
for image in sorted((ROOT / 'assets').iterdir()):
    if image.suffix.lower() in ('.jpg', '.jpeg', '.png'):
        message = image_problem(image)
        if message:
            problems.append(f'assets/{image.name}: {message}')
if problems:
    print('Build check failed:', *problems, sep='\n  ')
    sys.exit(1)
print(f'Built {len(PAGES)} static pages plus a 404 page; all local links and assets resolve in the root and dist copies.')
