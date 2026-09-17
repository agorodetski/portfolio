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
    links = [('Home', 'index.html'), ('Work', 'work/index.html'), ('About', 'about/index.html'),
             ('Experience', 'experience/index.html'), ('Contact', 'contact/index.html')]
    nav = ''.join(
        f'<a href="{base}{href}"' + (' aria-current="page"' if label == active else '') +
        f'>{label}</a>' for label, href in links
    )
    markup = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f8f7f2">
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
  <footer class="site-footer"><div class="container footer-inner"><span>© <span id="year">2026</span> Avi Gorodetski</span><span>People, purpose &amp; follow-through.</span><a href="mailto:agorodetski@tulane.edu">Say hello <span aria-hidden="true">↗</span></a></div></footer>
</body>
</html>
'''
    target.write_text(markup)


home = '''
<section class="hero container">
  <div class="hero-copy"><p class="eyebrow">Hi, I’m Avi Gorodetski</p>
    <h1>I bring people together <em>and ideas to life.</em></h1>
    <p class="lede">I build teams, programs, and experiences that make people feel part of something. My work spans a social-impact startup, global youth leadership, campus programming, and client service.</p>
    <div class="actions"><a class="button button-primary" href="work/index.html">Explore my work <span aria-hidden="true">↗</span></a><a class="text-link" href="assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">View résumé <span aria-hidden="true">↗</span></a></div>
    <p class="hero-aside">Tulane University · Sociology &amp; Social Policy &amp; Practice · Class of 2027</p>
  </div>
  <figure class="hero-photo"><img src="assets/avi-headshot.jpg" alt="Avi Gorodetski smiling outdoors" width="896" height="1343" fetchpriority="high"><figcaption>New Orleans, Louisiana / Currently</figcaption></figure>
</section>
<div class="fact-band"><div class="container fact-grid"><div><strong>$15K</strong><span>GiVV pitch win</span></div><div><strong>200+</strong><span>TUCP members</span></div><div><strong>25</strong><span>Countries in BBYO’s teen leadership network</span></div></div></div>
<section class="section container">
  <div class="section-heading"><div><p class="eyebrow">Selected work / 01</p><h2>The work, <em>up close.</em></h2></div><p>Different roles, one throughline: connect people, find a way forward, and make it happen.</p></div>
  <div class="feature-grid">
    <a class="feature-card feature-large" href="work/givv/index.html"><div class="feature-media"><img src="assets/givv-team.jpg" alt="GiVV team with its first-place $15,000 award" loading="lazy" width="2048" height="1697"></div><div class="feature-text"><span class="kicker">Entrepreneurship / 2026</span><h3>GiVV</h3><p>Building a more social, accessible way for students to support local nonprofits.</p><span class="card-link">Read the story <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card" href="work/bbyo/index.html"><div class="feature-media"><img src="assets/bbyo-speaking.jpg" alt="Avi speaking at BBYO International Convention" loading="lazy" width="2048" height="1367"></div><div class="feature-text"><span class="kicker">Global leadership / 2022–23</span><h3>BBYO</h3><p>Leading a 1,200+ teen network across 25 countries.</p><span class="card-link">Read the story <span aria-hidden="true">↗</span></span></div></a>
    <a class="feature-card card-graphic" href="experience/index.html#tucp"><div class="graphic-top"><span>TULANE UNIVERSITY<br>CAMPUS PROGRAMMING</span><span>EST. 1957</span></div><div class="graphic-word">TUCP<span aria-hidden="true">✳</span></div><div class="feature-text"><span class="kicker">Campus experiences / 2026–27</span><h3>For the whole campus.</h3><p>Leading a 200+ member organization and a $450K programming budget.</p><span class="card-link">See the experience <span aria-hidden="true">↗</span></span></div></a>
  </div>
  <p class="section-end"><a class="text-link" href="work/index.html">See all selected work <span aria-hidden="true">↗</span></a></p>
</section>
<section class="section section-ink"><div class="container invitation"><div><p class="eyebrow">What’s next</p><h2>Let’s make something <em>meaningful.</em></h2></div><div><p>I’m interested in strategy, social impact, philanthropy, and the kind of work where big ideas need people who can make them real.</p><a class="button button-light" href="contact/index.html">Get in touch <span aria-hidden="true">↗</span></a></div></div></section>
'''
page('index.html','Home','Avi Gorodetski builds teams, programs, and experiences across social impact, global leadership, and client service.','Home',home)

work = '''
<section class="page-intro container"><p class="eyebrow">Selected work / 01</p><h1>Ideas take shape <em>with people.</em></h1><p class="lede">From a startup pitch to a global stage, these are projects where I’ve helped bring a group toward a shared goal.</p></section>
<section class="container section section-tight"><div class="work-list">
  <article class="work-row"><a class="work-image" href="givv/index.html"><img src="../assets/givv-team.jpg" alt="GiVV team holding the first-place award" width="2048" height="1697"></a><div class="work-copy"><span class="kicker">01 / Entrepreneurship · 2026–present</span><h2>GiVV</h2><p>Co-founded a social marketplace concept to connect Tulane students with New Orleans nonprofits. Fifteen-plus research interviews, a semester of building, and a first-place pitch earned our team $15,000.</p><a class="text-link" href="givv/index.html">Explore GiVV <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><a class="work-image" href="bbyo/index.html"><img src="../assets/bbyo-convention.jpg" alt="BBYO International Convention stage seen from the audience" loading="lazy" width="2048" height="1365"></a><div class="work-copy"><span class="kicker">02 / Global leadership · 2022–23</span><h2>BBYO</h2><p>As International Teen President, I supported a leadership network of 1,200+ teens across 25 countries and helped bring 4,500 people together for International Convention.</p><a class="text-link" href="bbyo/index.html">Explore BBYO <span aria-hidden="true">↗</span></a></div></article>
  <article class="work-row"><div class="work-image work-tucp" aria-hidden="true"><span>TUCP<span>✳</span></span></div><div class="work-copy"><span class="kicker">03 / Campus programming · 2024–present</span><h2>Tulane University Campus Programming</h2><p>From producing a festival for roughly 1,500 students to leading TUCP’s 15+ person board, I’ve learned how to make ambitious experiences happen through good systems and strong teams.</p><a class="text-link" href="../experience/index.html#tucp">See my role <span aria-hidden="true">↗</span></a></div></article>
</div></section>
<section class="section soft-section"><div class="container narrow"><p class="eyebrow">More of the story</p><h2>Impact happens <em>in many forms.</em></h2><div class="two-cards"><article><span class="kicker">Strong City Tulane</span><h3>New Orleans, with New Orleans.</h3><p>Building relationships with local nonprofit partners and bringing more students into community-centered work.</p></article><article><span class="kicker">The Tow Foundation</span><h3>Listening before deciding.</h3><p>Reviewing grant applications for a youth mental health innovation fund taught me to evaluate bold ideas with care and context.</p></article></div></div></section>
'''
page('work/index.html','Selected Work','Explore Avi Gorodetski’s work with GiVV, BBYO, TUCP, Strong City Tulane, and The Tow Foundation.','Work',work)

givv = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">01 / GiVV · Co-founder &amp; COO</p><h1>Giving feels different when it’s <em>personal.</em></h1><p class="lede">How our team made local philanthropy feel more accessible to college students—and took the idea from research to a first-place pitch.</p><div class="story-facts"><div><strong>15+</strong><span>Student interviews</span></div><div><strong>$15K</strong><span>First-place award</span></div><div><strong>2026</strong><span>Founded at Tulane</span></div></div></section>
<figure class="story-hero"><img src="../../assets/givv-pitch.jpg" alt="GiVV team presenting its final startup pitch at Tulane" width="2048" height="1645"><figcaption>GiVV’s final pitch at Tulane’s Strategy Start-Up Lab, April 2026.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The idea</p><h2>Show up for the places that shape us.</h2></div><div class="story-prose"><p>GiVV is a social marketplace concept connecting Tulane students with local nonprofits through micro-donations, social sharing, and student-organization competitions. We wanted to make giving easy to start and meaningful enough to keep doing.</p><p>In 15+ interviews, students told us about limited funds, questions of trust, and the fatigue of deciding where to give. Personal connection and seeing friends participate made a difference. Those insights shaped our approach.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">My contribution</p><h2>Building the work behind the pitch.</h2></div><div class="story-prose"><p>As co-founder and COO, I led operations throughout our semester-long startup incubator, contributed to strategy and user research, and developed the social media strategy and content. My teammates and I built and presented the concept together.</p><p>On April 28, 2026, GiVV placed first in Tulane’s Strategy Start-Up Lab final pitch competition and earned a $15,000 award. It was a proof point for the idea—and for what a committed team can do in one semester.</p></div></div></section>
<figure class="story-hero story-photo-end"><img src="../../assets/givv-team.jpg" alt="GiVV founders and supporters celebrating with the $15,000 first-place check" loading="lazy" width="2048" height="1697"><figcaption>The GiVV team after the first-place award.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../bbyo/index.html">Leading a global teen community <span aria-hidden="true">↗</span></a></div>
'''
page('work/givv/index.html','GiVV','How Avi Gorodetski and the GiVV team developed a student-to-nonprofit giving concept and won Tulane’s $15,000 startup pitch award.','Work',givv)

bbyo = '''
<section class="story-intro container"><a class="back-link" href="../index.html">← All work</a><p class="eyebrow">02 / BBYO · International Teen President</p><h1>Leadership starts with <em>showing up.</em></h1><p class="lede">A year of listening to young leaders around the world, supporting local chapters, and helping a global community feel connected.</p><div class="story-facts"><div><strong>1,200+</strong><span>Teen leaders</span></div><div><strong>25</strong><span>Countries</span></div><div><strong>750+</strong><span>Chapters</span></div></div></section>
<figure class="story-hero"><img src="../../assets/bbyo-speaking.jpg" alt="Avi speaking at a BBYO International Convention podium alongside a fellow teen leader" width="2048" height="1367"><figcaption>Speaking at BBYO International Convention in 2023.</figcaption></figure>
<section class="section container story-layout"><div><p class="eyebrow">The role</p><h2>Global reach. Local relationships.</h2></div><div class="story-prose"><p>I deferred a year of college to serve as BBYO’s International Teen President. I led a board of 10 peers and worked with a network of more than 1,200 teen leaders in 25 countries, supporting leadership development and engagement across more than 750 chapters.</p><p>Traveling to 13 countries and 20 states taught me that a global organization stays strong through relationships with the people doing the work locally. I learned to listen across cultures, communicate a shared purpose, and make room for others to lead.</p></div></section>
<section class="section soft-section"><div class="container story-layout"><div><p class="eyebrow">The scale</p><h2>Moments that make a movement tangible.</h2></div><div class="story-prose"><p>Alongside governance and co-managing a $60,000 budget, I helped lead a 250+ person team executing a five-day International Convention for 4,500 attendees. I also spoke on BBYO stages before audiences of 5,000+.</p><p>The most lasting lesson was that leadership is less about being the person at the microphone and more about helping thousands of others feel equipped to use theirs.</p></div></div></section>
<figure class="story-hero story-photo-end"><img src="../../assets/bbyo-convention.jpg" alt="Wide view of BBYO International Convention stage with audience in the foreground" loading="lazy" width="2048" height="1365"><figcaption>A view from the audience at International Convention.</figcaption></figure>
<div class="container next-story"><span>Next story</span><a href="../givv/index.html">Building a new way to give <span aria-hidden="true">↗</span></a></div>
'''
page('work/bbyo/index.html','BBYO Leadership','Avi Gorodetski’s year as BBYO International Teen President, leading a global network of 1,200+ teen leaders.','Work',bbyo)

about = '''
<section class="page-intro container"><p class="eyebrow">About / 02</p><h1>Curious about systems. <em>Committed to people.</em></h1><p class="lede">The throughline in my work is simple: I love understanding people, bringing them together, and making something useful happen.</p></section>
<section class="section container about-grid"><div class="about-photo"><img src="../assets/avi-headshot.jpg" alt="Portrait of Avi Gorodetski outdoors" width="896" height="1343"></div><div class="about-text"><p class="eyebrow">A little background</p><h2>Hi, I’m Avi.</h2><p>I’m a first-generation American from Northern Virginia and a senior at Tulane University, where I study Sociology and Social Policy &amp; Practice with minors in Jewish Studies and Strategy, Leadership &amp; Analytics.</p><p>My studies make me curious about how institutions and communities shape people’s lives. Outside the classroom, I’ve found myself drawn to the practical side of that question: building programs, supporting nonprofits, and creating the conditions for people to connect.</p><p>My experience has taken me from a global youth organization to a private equity client-service team, from New Orleans nonprofit partnerships to founding a startup with friends. I like complex work that calls for both empathy and a good plan.</p><a class="text-link" href="../experience/index.html">Explore my experience <span aria-hidden="true">↗</span></a></div></section>
<section class="section soft-section"><div class="container"><p class="eyebrow">Outside the résumé</p><h2>There’s always <em>more to explore.</em></h2><div class="personal-grid"><article><span class="personal-number">01 / MUSIC</span><h3>A playlist for every month.</h3><p>I make a new Spotify playlist every month. Music is how I remember a place, a season, and the people who were there.</p><span class="personal-aside">Spotify / @avigorodetski</span></article><article><span class="personal-number">02 / TRAVEL</span><h3>32 countries down. 18 to go.</h3><p>My goal is to visit 50 countries by 50. I’m currently at 32, and I love the sense of perspective that comes with being somewhere new.</p><div class="travel-meter" role="meter" aria-label="Countries visited toward a goal of 50" aria-valuemin="0" aria-valuemax="50" aria-valuenow="32"><span></span></div><span class="personal-aside">32 / 50 countries</span></article><article><span class="personal-number">03 / FOOD</span><h3>Find me at the table.</h3><p>Exploring a place usually starts with figuring out what to eat. In New Orleans and everywhere I travel, food is one of my favorite ways to connect.</p></article></div></div></section>
<section class="section container closing"><p class="eyebrow">The way I work</p><h2>Lead with context. Make room for people. <em>Follow through.</em></h2><p>Whether I’m organizing a campus event or working through an uncertain idea with a team, I care about clear communication, shared ownership, and the details that help people do their best work.</p><a class="button button-primary" href="../contact/index.html">Let’s connect <span aria-hidden="true">↗</span></a></section>
'''
page('about/index.html','About Avi','Meet Avi Gorodetski: sociology student, community builder, monthly playlist maker, and traveler with a goal of 50 countries by 50.','About',about)

experience = '''
<section class="page-intro container"><p class="eyebrow">Experience / 03</p><h1>Big ideas need <em>good operators.</em></h1><p class="lede">I’ve learned to work across different contexts—from time-sensitive client service to campus leadership, nonprofit partnerships, and research.</p><div class="actions"><a class="button button-primary" href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">View résumé <span aria-hidden="true">↗</span></a><a class="text-link" href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer">LinkedIn <span aria-hidden="true">↗</span></a></div></section>
<section class="section container experience-layout"><div class="experience-heading"><p class="eyebrow">Professional experience</p><h2>What I’ve done.</h2></div><div class="experience-list">
<article><div class="role-top"><span>2026</span><span>New York, NY</span></div><h3>AlphaSights</h3><p class="role-name">Summer Associate, Client Services · Private Equity</p><p>Managed 10+ concurrent projects for private equity clients, recruited and vetted 100+ industry experts, and facilitated 30+ client–expert consultations to support investment research.</p></article>
<article><div class="role-top"><span>2026–present</span><span>New Orleans, LA</span></div><h3>GiVV Inc.</h3><p class="role-name">Co-founder</p><p>Led operations throughout a startup incubator and developed social content and strategy for a giving platform concept. Our team won first place and $15,000 in the final pitch competition.</p></article>
<article><div class="role-top"><span>2025</span><span>New York, NY</span></div><h3>The Tow Foundation</h3><p class="role-name">Innovation Fund Community Advisor</p><p>Reviewed and scored grant applications for an innovation fund investing in expanded youth mental health support.</p></article>
<article><div class="role-top"><span>2024–present</span><span>New Orleans, LA</span></div><h3>Tulane Technology Services</h3><p class="role-name">Classroom Experience Assistant</p><p>Support classroom technology and troubleshoot issues to keep learning environments running smoothly.</p></article>
<article><div class="role-top"><span>2024–2025</span><span>New Orleans, LA</span></div><h3>Tulane University</h3><p class="role-name">Substantive Editor · Research Assistant</p><p>Edited a sociology manuscript for structure and clarity, and analyzed qualitative interview narratives in Jewish Studies research.</p></article>
</div></section>
<section class="section soft-section"><div class="container experience-layout"><div class="experience-heading"><p class="eyebrow">Leadership</p><h2>What I’ve led.</h2></div><div class="experience-list">
<article id="tucp"><div class="role-top"><span>2026–present</span><span>Tulane University</span></div><h3>Tulane University Campus Programming</h3><p class="role-name">President · Former Lagniappe Chair</p><p>Lead a 15+ member board and a 200+ member organization in concerts, comedy, and speaker programming. Manage a $450,000 budget and strengthen team operations. Previously organized TGIO 2025, a campus festival with roughly 1,500 attendees.</p></article>
<article><div class="role-top"><span>2024–present</span><span>New Orleans, LA</span></div><h3>Strong City Tulane</h3><p class="role-name">Program Coordinator · Engagement Director</p><p>Build relationships with nonprofit partners across New Orleans and develop student engagement initiatives.</p></article>
<article><div class="role-top"><span>2022–2023</span><span>Global</span></div><h3>BBYO</h3><p class="role-name">International Teen President</p><p>Led a 10-member board and worked with 1,200+ teen leaders across 25 countries. Co-managed a $60,000 budget and helped execute International Convention for 4,500 attendees.</p></article>
</div></div></section>
<section class="section container credentials"><div><p class="eyebrow">Education</p><h2>Tulane University</h2><p>BA, Sociology and Social Policy &amp; Practice · Minors in Jewish Studies and Strategy, Leadership &amp; Analytics · Expected May 2027</p><p>GPA 3.98/4.0 · Dean’s List</p></div><div><p class="eyebrow">Languages &amp; skills</p><h3>Connecting across contexts.</h3><p>Native English and Hebrew; intermediate Spanish. Experience with Salesforce, Canva, Microsoft Office, and Google Workspace.</p><a class="text-link" href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener">Full résumé <span aria-hidden="true">↗</span></a></div></section>
'''
page('experience/index.html','Experience','Avi Gorodetski’s experience in client service, social-impact entrepreneurship, campus leadership, grant review, and research.','Experience',experience)

contact = '''
<section class="contact-page container"><p class="eyebrow">Contact / 04</p><h1>Let’s start a <em>conversation.</em></h1><p class="lede">I’d love to connect with recruiters, collaborators, investors, and people working at the intersection of strategy, community, and social impact.</p><div class="contact-options"><a href="mailto:agorodetski@tulane.edu"><span>Email</span><strong>agorodetski@tulane.edu</strong><span aria-hidden="true">↗</span></a><a href="https://www.linkedin.com/in/avigorodetski" target="_blank" rel="noopener noreferrer"><span>LinkedIn</span><strong>Connect with me</strong><span aria-hidden="true">↗</span></a><a href="../assets/avi-gorodetski-resume.pdf" target="_blank" rel="noopener"><span>Résumé</span><strong>View my experience</strong><span aria-hidden="true">↗</span></a></div><p class="contact-footnote">Based in New Orleans while finishing my degree at Tulane University.</p></section>
'''
page('contact/index.html','Contact','Get in touch with Avi Gorodetski by email or LinkedIn, and view her résumé.','Contact',contact)

# Mirror the authored static site into the directory used by Sites hosting.
DIST.mkdir(exist_ok=True)
for path in ['index.html','styles.css','script.js','favicon.svg']:
    shutil.copy2(ROOT / path, DIST / path)
for directory in ['work','about','experience','contact','assets']:
    src = ROOT / directory
    dst = DIST / directory
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
print('Built seven static pages with supplied photography and résumé.')
