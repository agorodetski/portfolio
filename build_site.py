"""Build Avi's dependency-free, multi-page portfolio into the Site's static dist directory."""
from pathlib import Path
from html import escape
import shutil

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
SITE = 'Avi Gorodetski'


def page(path: str, title: str, description: str, active: str, body: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    depth = len(Path(path).parts) - 1
    base = '../' * depth
    links = [('Home', 'index.html'), ('Work', 'work/index.html'), ('Now', 'now/index.html'),
             ('About', 'about/index.html'), ('Experience', 'experience/index.html'),
             ('Contact', 'contact/index.html')]
    nav = ''.join(
        f'<a href="{base}{href}"' + (' aria-current="page"' if label == active else '') +
        f'>{label}</a>' for label, href in links
    )
    markup = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#182b49">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta property="og:title" content="{escape(title, quote=True)} | {SITE}">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:type" content="website">
  <title>{escape(title)} | {SITE}</title>
  <link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{base}styles.css">
  <script src="{base}script.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{base}index.html" aria-label="Avi Gorodetski, home">avi<span>.</span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" hidden>Menu <span aria-hidden="true">+</span></button>
      <nav class="site-nav" id="site-nav" aria-label="Main navigation">{nav}</nav>
    </div>
  </header>
  <main id="main">{body}</main>
  <footer class="site-footer"><div class="container footer-inner"><span>© <span id="year">2026</span> Avi Gorodetski</span><span>New Orleans / New York / DC</span><a href="mailto:agorodetski@tulane.edu">Email me <span aria-hidden="true">↗</span></a></div></footer>
</body>
</html>
'''
    target.write_text(markup)


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
<div class="fact-band"><div class="container fact-grid"><div><strong>$15K</strong><span>GiVV pitch win</span></div><div><strong>2K</strong><span>Students at a TUCP concert</span></div><div><strong>25</strong><span>Countries in BBYO’s teen leadership network</span></div></div></div>
<section class="section container">
  <div class="section-heading"><div><p class="eyebrow">Selected work / 01</p><h2>Projects and leadership.</h2></div><p>A closer look at what I built, led, and learned.</p></div>
  <div class="feature-grid">
    <a class="feature-card feature-large" href="work/givv/index.html"><div class="feature-media"><img src="assets/givv-team.jpg" alt="GiVV team with its first-place $15,000 award" loading="lazy" width="2048" height="1697"></div><div class="feature-text"><span class="kicker">Entrepreneurship / 2026</span><h3>GiVV</h3><p>Building a more social, accessible way for students to support local nonprofits.</p><span class="card-link">Read the story <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card" href="work/tucp/index.html"><div class="feature-media"><img src="assets/tucp-team.jpeg" alt="Avi with members of the TUCP team on Tulane's campus" loading="lazy" width="1536" height="2048"></div><div class="feature-text"><span class="kicker">Campus programming / 2024–present</span><h3>TUCP</h3><p>Building the teams and systems behind concerts, festivals, speakers, and comedy.</p><span class="card-link">Read the story <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card" href="work/bbyo/index.html"><div class="feature-media"><img src="assets/bbyo-speaking.jpg" alt="Avi speaking at BBYO International Convention" loading="lazy" width="2048" height="1367"></div><div class="feature-text"><span class="kicker">Global leadership / 2022–23</span><h3>BBYO</h3><p>Leading a 1,200+ teen network across 25 countries.</p><span class="card-link">Read the story <span aria-hidden="true">↗</span></span></div></a>
  </div>
  <p class="section-end"><a class="text-link" href="work/index.html">See all selected work <span aria-hidden="true">↗</span></a></p>
</section>
<section class="section updates-section"><div class="container">
  <div class="section-heading"><div><p class="eyebrow">Recently / 02</p><h2>What I’m doing now.</h2></div><p>A short, curated view of current work, community, and the music in rotation.</p></div>
  <div class="updates-grid" data-updates-source="updates.json" data-updates-limit="3"><p class="updates-status">Loading recent updates…</p></div>
  <p class="section-end"><a class="text-link" href="now/index.html">Visit the Now page</a></p>
</div></section>
<section class="section section-ink"><div class="container invitation"><div><p class="eyebrow">Currently</p><h2>Exploring what comes after Tulane.</h2></div><div><p>I’m interested in strategy, philanthropy, program management, and social-impact roles in New York or Washington, DC.</p><a class="button button-light" href="contact/index.html">Contact <span aria-hidden="true">↗</span></a></div></div></section>
'''
page('index.html','Home','Avi Gorodetski builds teams, programs, and experiences across social impact, global leadership, and client service.','Home',home)

work = '''
<section class="page-intro container"><p class="eyebrow">Selected work / 01</p><h1>What I’ve built and led.</h1><p class="lede">Four projects that show how I approach research, operations, leadership, and execution.</p></section>
<section class="container section section-tight"><div class="work-list">
  <article class="work-row"><a class="work-image" href="givv/index.html"><img src="../assets/givv-team.jpg" alt="GiVV team holding the first-place award" width="2048" height="1697"></a><div class="work-copy"><span class="kicker">01 / Entrepreneurship · 2026–present</span><h2>GiVV</h2><p>Co-founded a social marketplace concept to connect Tulane students with New Orleans nonprofits. Fifteen-plus research interviews, a semester of building, and a first-place pitch earned our team $15,000.</p><a class="text-link" href="givv/index.html">Explore GiVV <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image work-image-portrait" href="tucp/index.html"><img src="../assets/tucp-team.jpeg" alt="Avi with members of the TUCP team on Tulane's campus" loading="lazy" width="1536" height="2048"></a><div class="work-copy"><span class="kicker">02 / Campus programming · 2024–present</span><h2>Tulane University Campus Programming</h2><p>Helped plan a Natasha Bedingfield concert for roughly 2,000 students, produced a 1,500-person campus festival, launched TUCP’s first online storefront, and now lead the organization as president.</p><a class="text-link" href="tucp/index.html">Explore TUCP <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image" href="bbyo/index.html"><img src="../assets/bbyo-convention.jpg" alt="BBYO International Convention stage seen from the audience" loading="lazy" width="2048" height="1365"></a><div class="work-copy"><span class="kicker">03 / Global leadership · 2022–23</span><h2>BBYO</h2><p>As International Teen President, I supported a leadership network of 1,200+ teens across 25 countries and helped bring 4,500 people together for International Convention.</p><a class="text-link" href="bbyo/index.html">Explore BBYO <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image" href="strong-city/index.html"><img src="../assets/strong-city-field-day.jpeg" alt="Avi with the Strong City team at Field Day" loading="lazy" width="2048" height="1365"></a><div class="work-copy"><span class="kicker">04 / Community engagement · 2024–present</span><h2>Strong City</h2><p>Building nonprofit partnerships and helping coordinate Field Day for 100+ New Orleans youth and a Thanksgiving Drive that packs 600+ food boxes for local families.</p><a class="text-link" href="strong-city/index.html">Explore Strong City <span aria-hidden="true">↗</span></a></div></article>
</div></section>
<section class="section soft-section"><div class="container narrow"><p class="eyebrow">Additional work</p><h2>Grantmaking and research.</h2><div class="two-cards"><article><span class="kicker">The Tow Foundation</span><h3>Youth mental health funding</h3><p>Reviewed grant applications for a $10 million innovation fund focused on expanding mental health support for young people.</p></article><article><span class="kicker">Tulane University</span><h3>Qualitative research and editing</h3><p>Analyzed interview narratives in Jewish Studies research and substantively edited a sociology manuscript for structure and clarity.</p></article></div></div></section>
'''
page('work/index.html','Selected Work','Explore Avi Gorodetski’s work with GiVV, BBYO, TUCP, Strong City Tulane, and The Tow Foundation.','Work',work)

now = '''
<section class="page-intro container"><p class="eyebrow">Now / 02</p><h1>What I’m doing, building, and listening to.</h1><p class="lede">A living page for the work and ideas that are most current—edited for signal, not volume.</p></section>
<section class="section container section-tight">
  <div class="now-intro"><p class="eyebrow">Current notes</p><p>This page brings together selected updates from my work with TUCP, GiVV, and Strong City, plus occasional notes from LinkedIn and my monthly Spotify habit.</p></div>
  <div class="updates-grid updates-grid-full" data-updates-source="../updates.json" data-updates-limit="6"><p class="updates-status">Loading current updates…</p></div>
</section>
<section class="section soft-section"><div class="container source-strip"><div><p class="eyebrow">Follow along</p><h2>Elsewhere.</h2></div><div class="source-links"><a href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="https://www.geauxtucp.com/" target="_blank" rel="noopener noreferrer">TUCP</a><a href="https://www.instagram.com/thegivvapp/" target="_blank" rel="noopener noreferrer">GiVV</a><a href="https://www.mystrongcity.org/" target="_blank" rel="noopener noreferrer">Strong City</a><a href="https://open.spotify.com/search/avigorodetski" target="_blank" rel="noopener noreferrer">Spotify</a><a href="https://github.com/agorodetski/portfolio" target="_blank" rel="noopener noreferrer">GitHub</a></div></div></section>
'''
page('now/index.html','Now','Current work, community projects, ideas, and monthly listening from Avi Gorodetski.','Now',now)

givv = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">01 / GiVV · Co-founder &amp; COO</p><h1>From student research to a $15K pitch win.</h1><p class="lede">Our team developed a social marketplace concept that connects Tulane students with New Orleans nonprofits.</p><div class="story-facts"><div><strong>15+</strong><span>Student interviews</span></div><div><strong>$15K</strong><span>First-place award</span></div><div><strong>2026</strong><span>Founded at Tulane</span></div></div></section>
<figure class="story-hero"><img src="../../assets/givv-pitch.jpg" alt="GiVV team presenting its final startup pitch at Tulane" width="2048" height="1645"><figcaption>GiVV’s final pitch at Tulane’s Strategy Start-Up Lab, April 2026.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The idea</p><h2>Lower the barriers to local giving.</h2></div><div class="story-prose"><p>GiVV is a social marketplace concept connecting Tulane students with local nonprofits through micro-donations, social sharing, and student-organization competitions.</p><p>In 15+ interviews, students pointed to limited funds, questions of trust, and decision fatigue. Personal connection and seeing friends participate made a difference. Those findings shaped our approach.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">My contribution</p><h2>Building the work behind the pitch.</h2></div><div class="story-prose"><p>As co-founder and COO, I led operations throughout our semester-long startup incubator, contributed to strategy and user research, and developed the social media strategy and content. My teammates and I built and presented the concept together.</p><p>On April 28, 2026, GiVV placed first in Tulane’s Strategy Start-Up Lab final pitch competition and earned a $15,000 award. It was a proof point for the idea—and for what a committed team can do in one semester.</p></div></div></section>
<figure class="story-hero story-photo-end"><img src="../../assets/givv-team.jpg" alt="GiVV founders and supporters celebrating with the $15,000 first-place check" loading="lazy" width="2048" height="1697"><figcaption>The GiVV team after the first-place award.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../tucp/index.html">Programming for an entire campus <span aria-hidden="true">↗</span></a></div>
'''
page('work/givv/index.html','GiVV','How Avi Gorodetski and the GiVV team developed a student-to-nonprofit giving concept and won Tulane’s $15,000 startup pitch award.','Work',givv)

tucp = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">02 / TUCP · President</p><h1>Programming for an entire campus.</h1><p class="lede">Concerts, festivals, comedy, and speakers—built by students and designed for the Tulane community.</p><div class="story-facts"><div><strong>~2K</strong><span>Concert attendees</span></div><div><strong>200+</strong><span>Organization members</span></div><div><strong>$450K</strong><span>Programming budget</span></div></div></section>
<figure class="story-hero story-hero-portrait"><img src="../../assets/tucp-team.jpeg" alt="Avi with members of the TUCP team on Tulane's campus" width="1536" height="2048"><figcaption>With members of the TUCP team on Tulane’s campus.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">Event scale</p><h2>From the run of show to the crowd.</h2></div><div class="story-prose"><p>As part of TUCP’s board, I helped plan a Natasha Bedingfield concert attended by roughly 2,000 students. I also led TGIO 2025, a campus festival for about 1,500 students with vendors, food trucks, merchandise, and live entertainment.</p><p>The visible result is one night on campus. The work behind it is months of coordination, budgeting, communication, and contingency planning.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">Building the organization</p><h2>Make the systems match the ambition.</h2></div><div class="story-prose"><p>As Lagniappe Chair, I helped redesign the role around philanthropy, merchandise, sponsorship, and fundraising. I launched TUCP’s first online storefront, developed merchandise strategy, and supported sponsorship outreach.</p><p>Now, as president, I lead a 15+ member board and a 200+ member organization responsible for a $450,000 programming budget.</p></div></div></section>
<div class="container next-story"><span>Next story</span><a href="../bbyo/index.html">Leading a global teen community <span aria-hidden="true">↗</span></a></div>
'''
page('work/tucp/index.html','TUCP','How Avi Gorodetski helps lead Tulane University Campus Programming and execute large-scale campus events.','Work',tucp)

bbyo = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">02 / BBYO · International Teen President</p><h1>Leading a network across 25 countries.</h1><p class="lede">One year working with teen leaders around the world, supporting local chapters, and helping plan a 4,500-person convention.</p><div class="story-facts"><div><strong>1,200+</strong><span>Teen leaders</span></div><div><strong>25</strong><span>Countries</span></div><div><strong>750+</strong><span>Chapters</span></div></div></section>
<figure class="story-hero"><img src="../../assets/bbyo-speaking.jpg" alt="Avi speaking at a BBYO International Convention podium alongside a fellow teen leader" width="2048" height="1367"><figcaption>Speaking at BBYO International Convention in 2023.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The role</p><h2>Coordinate globally. Support locally.</h2></div><div class="story-prose"><p>I deferred a year of college to serve as BBYO’s International Teen President. I led a board of 10 peers and worked with a network of more than 1,200 teen leaders in 25 countries, supporting leadership development and engagement across more than 750 chapters.</p><p>Traveling to 13 countries and 20 states taught me that a global organization depends on strong local leaders. My job was to listen, share context, and help those leaders act.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">The scale</p><h2>Convention planning at scale.</h2></div><div class="story-prose"><p>Alongside governance and co-managing a $60,000 budget, I helped lead a 250+ person team executing a five-day International Convention for 4,500 attendees. I also spoke on BBYO stages before audiences of 5,000+.</p><p>The work taught me to set a clear direction, distribute ownership, and keep a large team moving.</p></div></div></section>
<figure class="story-hero story-photo-end"><img src="../../assets/bbyo-convention.jpg" alt="Wide view of BBYO International Convention stage with audience in the foreground" loading="lazy" width="2048" height="1365"><figcaption>A view from the audience at International Convention.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../strong-city/index.html">Community work built on relationships <span aria-hidden="true">↗</span></a></div>
'''
page('work/bbyo/index.html','BBYO Leadership','Avi Gorodetski’s year as BBYO International Teen President, leading a global network of 1,200+ teen leaders.','Work',bbyo)

strong_city = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">04 / Strong City · Engagement Director</p><h1>Community work built on relationships.</h1><p class="lede">Connecting Tulane students with New Orleans organizations through sustained partnerships and large-scale service.</p><div class="story-facts"><div><strong>100+</strong><span>Youth at Field Day</span></div><div><strong>600+</strong><span>Food boxes packed</span></div><div><strong>2024–</strong><span>Strong City leadership</span></div></div></section>
<figure class="story-hero"><img src="../../assets/strong-city-field-day.jpeg" alt="Avi with the Strong City team at Field Day" width="2048" height="1365"><figcaption>The Strong City team at Field Day, the organization’s largest annual event.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">Field Day</p><h2>Bring campus and community together.</h2></div><div class="story-prose"><p>Strong City’s annual Field Day brings more than 100 young people from across New Orleans to Tulane for a day of activities and connection.</p><p>My work focuses on the relationships and coordination that make programs like this possible: partnering with local nonprofits, organizing students, and keeping community priorities at the center.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">Thanksgiving Drive</p><h2>Turn a big goal into a clear operation.</h2></div><div class="story-prose"><p>Each year, the Thanksgiving Drive coordinates volunteers to pack more than 600 boxes of nonperishable food and produce for families across New Orleans.</p><p>It is community engagement at its most practical: many people, many moving pieces, and a tangible result.</p></div></div></section>
<figure class="story-hero story-photo-end story-hero-crop"><img src="../../assets/strong-city-thanksgiving.png" alt="Strong City volunteers assembling boxes during the Thanksgiving Drive" loading="lazy" width="944" height="2048"><figcaption>Volunteers assembling food boxes for Strong City’s Thanksgiving Drive.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../givv/index.html">Building a new way to give <span aria-hidden="true">↗</span></a></div>
'''
page('work/strong-city/index.html','Strong City','Avi Gorodetski’s community engagement work with Strong City in New Orleans.','Work',strong_city)

about = '''
<section class="page-intro container"><p class="eyebrow">About / 02</p><h1>About Avi.</h1><p class="lede">A sociology student, operator, community builder, and very committed monthly playlist maker.</p></section>
<section class="section container about-grid"><div class="about-photo"><img src="../assets/avi-headshot.jpg" alt="Portrait of Avi Gorodetski outdoors" width="896" height="1343"></div><div class="about-text"><p class="eyebrow">Background</p><h2>Virginia to New Orleans.</h2><p>I’m a first-generation American from Northern Virginia and a senior at Tulane University, where I study Sociology and Social Policy &amp; Practice with minors in Jewish Studies and Strategy, Leadership &amp; Analytics.</p><p>My studies make me curious about how institutions and communities shape people’s lives. Outside the classroom, I’ve focused on the practical side of that question: building programs, supporting nonprofits, and creating the conditions for people to connect.</p><p>My experience spans a global youth organization, a private equity client-service team, New Orleans nonprofit partnerships, and a startup I founded with friends. I like complex work that calls for both empathy and a good plan.</p><a class="text-link" href="../experience/index.html">Explore my experience <span aria-hidden="true">↗</span></a></div></section>
<section class="section soft-section"><div class="container"><p class="eyebrow">Outside the résumé</p><h2>Current interests.</h2><div class="personal-grid"><article><span class="personal-number">01 / MUSIC</span><h3>12 playlists a year.</h3><p>I make a new Spotify playlist every month. It’s how I keep track of a place, a season, and the people who were there.</p><span class="personal-aside">Spotify / @avigorodetski</span></article><article><span class="personal-number">02 / TRAVEL</span><h3>32 countries so far.</h3><p>My goal is 50 countries by 50. I’m at 32 and always planning the next one.</p><div class="travel-meter" role="meter" aria-label="Countries visited toward a goal of 50" aria-valuemin="0" aria-valuemax="50" aria-valuenow="32"><span></span></div><span class="personal-aside">32 / 50 countries</span></article><article><span class="personal-number">03 / FOOD</span><h3>Always choosing the restaurant.</h3><p>Exploring a place usually starts with figuring out what to eat. New Orleans has been especially good for this habit.</p></article></div></div></section>
<section class="section container closing"><p class="eyebrow">How I work</p><h2>Clear context, shared ownership, strong execution.</h2><p>Whether I’m organizing a campus event or working through an uncertain idea with a team, I care about clear communication and the details that keep work moving.</p><a class="button button-primary" href="../contact/index.html">Contact <span aria-hidden="true">↗</span></a></section>
'''
page('about/index.html','About Avi','Meet Avi Gorodetski: sociology student, community builder, monthly playlist maker, and traveler with a goal of 50 countries by 50.','About',about)

experience = '''
<section class="page-intro container"><p class="eyebrow">Experience / 03</p><h1>Experience.</h1><p class="lede">Client service, startup operations, grant review, campus programming, nonprofit partnerships, and research.</p><div class="actions"><a class="button button-primary" href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">View résumé <span aria-hidden="true">↗</span></a><a class="text-link" href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a></div></section>
<section class="section container experience-layout"><div class="experience-heading"><p class="eyebrow">Professional experience</p><h2>What I’ve done.</h2></div><div class="experience-list">
<article><div class="role-top"><span>2026</span><span>New York, NY</span></div><h3>AlphaSights</h3><p class="role-name">Summer Associate, Client Services · Private Equity</p><p>Managed 10+ concurrent projects for private equity clients, recruited and vetted 100+ industry experts, and facilitated 30+ client–expert consultations to support investment research.</p></article>
<article><div class="role-top"><span>2026–present</span><span>New Orleans, LA</span></div><h3>GiVV Inc.</h3><p class="role-name">Co-founder</p><p>Led operations throughout a startup incubator and developed social content and strategy for a giving platform concept. Our team won first place and $15,000 in the final pitch competition.</p></article>
<article><div class="role-top"><span>2025</span><span>New York, NY</span></div><h3>The Tow Foundation</h3><p class="role-name">Innovation Fund Community Advisor</p><p>Reviewed and scored grant applications for an innovation fund investing in expanded youth mental health support.</p></article>
<article><div class="role-top"><span>2024–present</span><span>New Orleans, LA</span></div><h3>Tulane Technology Services</h3><p class="role-name">Classroom Experience Assistant</p><p>Support classroom technology and troubleshoot issues to keep learning environments running smoothly.</p></article>
<article><div class="role-top"><span>2024–2025</span><span>New Orleans, LA</span></div><h3>Tulane University</h3><p class="role-name">Substantive Editor · Research Assistant</p><p>Edited a sociology manuscript for structure and clarity, and analyzed qualitative interview narratives in Jewish Studies research.</p></article>
</div></section>
<section class="section soft-section"><div class="container experience-layout"><div class="experience-heading"><p class="eyebrow">Leadership</p><h2>What I’ve led.</h2></div><div class="experience-list">
<article id="tucp"><div class="role-top"><span>2026–present</span><span>Tulane University</span></div><h3>Tulane University Campus Programming</h3><p class="role-name">President · Former Lagniappe Chair</p><p>Lead a 15+ member board and a 200+ member organization in concerts, comedy, and speaker programming. Manage a $450,000 budget; previously helped plan a roughly 2,000-person Natasha Bedingfield concert, produced a 1,500-person festival, and launched TUCP’s first online storefront.</p></article>
<article><div class="role-top"><span>2024–present</span><span>New Orleans, LA</span></div><h3>Strong City Tulane</h3><p class="role-name">Engagement Director · Former Program Coordinator</p><p>Build relationships with New Orleans nonprofit partners and develop student engagement initiatives, including Field Day for 100+ local youth and a Thanksgiving Drive packing 600+ food boxes for families.</p></article>
<article><div class="role-top"><span>2022–2023</span><span>Global</span></div><h3>BBYO</h3><p class="role-name">International Teen President</p><p>Led a 10-member board and worked with 1,200+ teen leaders across 25 countries. Co-managed a $60,000 budget and helped execute International Convention for 4,500 attendees.</p></article>
</div></div></section>
<section class="section container credentials"><div><p class="eyebrow">Education</p><h2>Tulane University</h2><p>BA, Sociology and Social Policy &amp; Practice · Minors in Jewish Studies and Strategy, Leadership &amp; Analytics · Expected May 2027</p><p>GPA 3.98/4.0 · Dean’s List</p></div><div><p class="eyebrow">Languages &amp; skills</p><h3>Connecting across contexts.</h3><p>Native English and Hebrew; intermediate Spanish. Experience with Salesforce, Canva, Microsoft Office, and Google Workspace.</p><a class="text-link" href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">Full résumé <span aria-hidden="true">↗</span></a></div></section>
'''
page('experience/index.html','Experience','Avi Gorodetski’s experience in client service, social-impact entrepreneurship, campus leadership, grant review, and research.','Experience',experience)

contact = '''
<section class="contact-page container"><p class="eyebrow">Contact / 04</p><h1>Get in touch.</h1><p class="lede">For recruiting, partnerships, startup conversations, or anything else: email is best.</p><div class="contact-options"><a href="mailto:agorodetski@tulane.edu"><span>Email</span><strong>agorodetski@tulane.edu</strong><span aria-hidden="true">↗</span></a><a href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span><strong>avigorodetski</strong><span aria-hidden="true">↗</span></a><a href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener"><span>Résumé</span><strong>Download PDF</strong><span aria-hidden="true">↗</span></a></div><p class="contact-footnote">New Orleans, Louisiana · Graduating from Tulane in May 2027</p></section>
'''
page('contact/index.html','Contact','Get in touch with Avi Gorodetski by email or LinkedIn, and view her résumé.','Contact',contact)

# Mirror the authored static site into the directory used by Sites hosting.
DIST.mkdir(exist_ok=True)
for path in ['index.html','styles.css','script.js','favicon.svg','updates.json']:
    shutil.copy2(ROOT / path, DIST / path)
for directory in ['work','now','about','experience','contact','assets']:
    src = ROOT / directory
    dst = DIST / directory
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
print('Built ten static pages with supplied photography, résumé, and curated updates.')
