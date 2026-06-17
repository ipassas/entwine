#!/usr/bin/env python3
# Generates all Entwine marketing pages from one shared shell + per-page content.
import re, pathlib

REST = pathlib.Path("restaurants.html").read_text()

def grab(pattern):
    m = re.search(pattern, REST, re.S)
    if not m: raise SystemExit("MISSING: " + pattern[:40])
    return m.group(1)

NAV       = grab(r'(<header class="nav">.*?</header>)')
FOOTER    = grab(r'(<footer class="footer">.*?</footer>)')
FOOTBAR   = grab(r'(<div class="footbar">.*?\n  </div>)')
PRELOADER = grab(r'(<div class="preloader"[^>]*>.*?</div>)')
SCRIPTS   = grab(r'(<!-- store badge icons -->.*?</defs></svg>)')

CRIT = """  <style>
    #preloader{position:fixed;inset:0;z-index:99999;background:#0a0a0a;display:flex;align-items:center;justify-content:center;transition:opacity .6s ease}
    #preloader .pl-mark{width:86px;height:86px;color:#b8a86a;animation:pl-pulse 1.5s ease-in-out infinite}
    @keyframes pl-pulse{0%,100%{opacity:.32;transform:scale(.9)}50%{opacity:1;transform:scale(1)}}
    #preloader.done{opacity:0;pointer-events:none}
  </style>"""

_UNSAFE = ('class="plan', 'class="faq', 'class="job', 'class="newsletter', 'class="blogcard',
           'class="tier', 'class="ptable', 'class="pills', 'class="billing', 'class="statgrid', 'class="timeline')

def vary(main):
    """Alternate section skins (linen/cream/ink/noir) so no two read the same.
    Keeps image (has-bg) and authored-dark sections; only darkens 'safe' simple sections."""
    parts = re.split(r'(<section class="r-sec[^"]*"[^>]*>)', main)
    out = [parts[0]]; prev = 'dark'; lc = 0; dc = [0]
    WM = '\n    <svg class="wmark" viewBox="0 0 42 52" fill="currentColor"><use href="#ew-mark"/></svg>'
    def darksec(tag, body):
        skin = ['ink', 'noir'][dc[0] % 2]; dc[0] += 1
        return re.sub(r'class="[^"]*"', f'class="r-sec {skin} wm js-reveal"', tag), WM + body
    i = 1
    while i < len(parts):
        tag = parts[i]; body = parts[i + 1] if i + 1 < len(parts) else ''
        cls = re.search(r'class="([^"]*)"', tag).group(1)
        if 'has-bg' in cls:
            prev = 'dark'; out += [tag, body]
        elif ' dark' in (' ' + cls):
            t, b = darksec(tag, body); prev = 'dark'; out += [t, b]
        else:
            safe = not any(u in body for u in _UNSAFE)
            if prev == 'light' and safe:
                t, b = darksec(tag, body); prev = 'dark'; out += [t, b]
            else:
                skin = ['tint', 'cream'][lc % 2]; lc += 1; prev = 'light'
                out += [re.sub(r'class="[^"]*"', f'class="r-sec {skin} js-reveal"', tag), body]
        i += 2
    return ''.join(out)

def page(slug, title, desc, main):
    main = vary(main)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="stylesheet" href="styles.css" />
  <script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js"></script>
{CRIT}
</head>
<body>

{PRELOADER}

<div class="stage">

{NAV}

{main}

{FOOTER}

{FOOTBAR}

</div>

{SCRIPTS}

</body>
</html>
"""
    pathlib.Path(slug).write_text(html)
    print("wrote", slug, len(html), "bytes")

BADGES = '<a href="download.html" class="badge" data-icon="apple"></a><a href="download.html" class="badge" data-icon="google"></a>'

def hero(eyebrow, h1, sub, cta, img, kw):
    return f"""  <section class="hero hero--page">
    <div class="hero__bg hero__bg--cover"><img class="imgph" alt="" data-img="{img}" data-kw="{kw}" data-w="1920" data-h="1080"></div>
    <div class="hero__inner">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h1}</h1>
      <p class="hero__sub">{sub}</p>
      <div class="hero__badges">{cta}</div>
    </div>
  </section>"""

def head(h2, sub=""):
    s = f'<p class="r-sub">{sub}</p>' if sub else ""
    return f'<div class="r-head"><h2>{h2}</h2></div>{s}'

def cta(h2, sub, primary, links):
    lk = '<span class="dot"></span>'.join(
        f'<a href="{href}">{t} <span>→</span></a>' for t, href in links)
    return f"""  <section class="rcta js-reveal">
    <svg class="wmark" viewBox="0 0 42 52" fill="currentColor" style="color:#0a0a0a"><use href="#ew-mark"/></svg>
    <h2>{h2}</h2>
    <p>{sub}</p>
    <div class="rcta__cta">
      {primary}
      <div class="rcta__links">{lk}</div>
    </div>
  </section>"""

# ============================================================ WINE LOVERS
wl = hero("For Wine Lovers",
  'The perfect wine is <span class="gold">already on the menu.</span> Let Entwine find it for you.',
  "No more pointing at something mid-range and hoping for the best — or sticking to the wines you feel safe choosing. Entwine has your restaurant's full menu built in: choose your dish, set your filters, and get a pairing that actually fits.",
  BADGES, "wine-lovers-hero", "wine,glass,restaurant,dinner,dark")
wl += f"""
  <section class="r-sec tint js-reveal">
    {head('Every level of wine lover deserves a great pairing. <span class="gold">Entwine finds yours.</span>')}
    <div class="cardgrid cardgrid--3">
      <div class="card"><div class="ic"><iconify-icon icon="ph:wine-thin"></iconify-icon></div><h3>The Wine Lover</h3><p>You know your Burgundy from your Barolo. You just want the best match for what you're eating — from this restaurant's actual list. Entwine surfaces the right bottle every time, filtered by style, region, grape, or price.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:smiley-thin"></iconify-icon></div><h3>The Wine-Curious</h3><p>You enjoy wine but the list is overwhelming. You usually point at something mid-range and hope for the best. Entwine takes the guesswork out — just pick your dish and let it do the rest.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:question-thin"></iconify-icon></div><h3>The Curious Diner</h3><p>You're just getting into wine and want to learn as you go. Every Entwine pairing comes with the story behind it — so every meal teaches you a little more.</p></div>
    </div>
  </section>
  <section class="r-sec dark has-bg js-reveal">
    <div class="r-bg"><img class="imgph" alt="" data-img="wine-lovers-pour" data-kw="wine,pouring,glass,dark" data-w="1920" data-h="1200"></div>
    <div class="r-inner">
      {head('Three taps to the <span class="gold">perfect pairing.</span>')}
      <div class="steps">
        <div class="step"><div class="step__node"><iconify-icon icon="ph:fork-knife-thin"></iconify-icon></div><span class="step__num">Tap 01</span><h3>Choose your dish</h3><p>Open the app at an Entwine restaurant and the full menu is already there — the actual dishes you're about to order. Pick what you're eating.</p></div>
        <div class="step"><div class="step__node"><iconify-icon icon="ph:sliders-horizontal-thin"></iconify-icon></div><span class="step__num">Tap 02</span><h3>Set your filters</h3><p>Filter by price, grape, region, or favour local. Entwine matches your dish to the wines on the restaurant's actual list. You lead, Entwine follows.</p></div>
        <div class="step"><div class="step__node"><iconify-icon icon="ph:wine-thin"></iconify-icon></div><span class="step__num">Tap 03</span><h3>Discover the pairing</h3><p>Get your perfect pairing — with the story behind it. Save it to your favourites and build a taste profile that gets smarter every meal.</p></div>
      </div>
    </div>
  </section>
  <section class="r-sec js-reveal">
    {head('Your sommelier. Your rules. <span class="gold">Your perfect bottle.</span>')}
    <div class="cardgrid">
      <div class="card"><div class="ic"><iconify-icon icon="ph:fork-knife-thin"></iconify-icon></div><h3>Restaurant menus in the app</h3><p>Every Entwine restaurant's full menu is built in. Choose your dish, set your filters, and get a pairing matched to what's actually in the cellar.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:book-open-thin"></iconify-icon></div><h3>Learn as you go</h3><p>Every recommendation comes with the story behind the wine — producer, region, tasting notes. Leave every meal knowing more than you arrived.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:sliders-horizontal-thin"></iconify-icon></div><h3>Filter your way</h3><p>Tell Entwine what matters — price, grape, region, style, or local. The recommendations adjust instantly.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:map-pin-thin"></iconify-icon></div><h3>Find Entwine restaurants</h3><p>Discover which restaurants near you are part of the Entwine club — and plan your next dinner with the app ready to help.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:user-circle-thin"></iconify-icon></div><h3>Build your taste profile</h3><p>The more you use Entwine, the better it knows you. Your preferences and history inform smarter recommendations over time.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:heart-thin"></iconify-icon></div><h3>Save your favourites</h3><p>Found a wine you loved? Save it. Every great pairing you discover lives in your profile — ready to revisit or share.</p></div>
    </div>
  </section>
  <section class="r-sec dark js-reveal">
    {head('8,000 wines. <span class="gold">Every one properly understood.</span>')}
    <div class="prose"><p>Entwine's recommendations aren't guesswork. Our database of 8,000+ wines is built from producer technical sheets — real data, from the source. When Entwine suggests a wine, it knows exactly what it's recommending, and why.</p></div>
  </section>
  <section class="r-sec tint js-reveal">
    {head('Already live at some of Malta’s favourite restaurants.', 'Our founding club members — the restaurants that helped build Entwine.')}
    <div class="club">
      <div class="member"><div class="nm">La Vela</div><div class="loc">Entwine Club Member · Malta</div></div>
      <div class="member"><div class="nm">Scala</div><div class="loc">Entwine Club Member · Malta</div></div>
      <div class="member"><div class="nm">Rani</div><div class="loc">Entwine Club Member · Malta</div></div>
    </div>
    <div class="club__cta"><a class="btn btn--outline-dark" href="#">Find an Entwine restaurant near you <span class="arrow">→</span></a></div>
  </section>
"""
wl += cta('Your own sommelier is waiting at the table.',
  'Download Entwine free on iOS and Android, and never point at the second-cheapest bottle again.',
  '<a class="btn btn--dark" href="download.html">Download free <span class="arrow">→</span></a>',
  [("Find a restaurant", "#"), ("How it works", "#")])
page("wine-lovers.html", "Entwine for Wine Lovers — Your sommelier at every table",
  "The perfect wine is already on the menu. Choose your dish, set your filters, and let Entwine find your pairing from the restaurant's actual wine list.", wl)

# ============================================================ ABOUT
ab = hero("About",
  'Technology in service of <span class="gold">the table.</span>',
  "Entwine is a wine technology company built by people who sit on both sides of the table — diners frustrated by the gap between wine lists and cellars, and operators who understand the pressure of running a great restaurant. So we built both. The platform we wished existed.",
  '<a class="btn btn--gold" href="#story">Our story <span class="arrow">→</span></a><a class="btn btn--outline-light" href="#team">Meet the team</a>',
  "about-hero", "restaurant,wine,table,people,dark")
ab += f"""
  <section class="r-sec tint js-reveal">
    {head('Three things we believe in. <span class="gold">Everything else follows.</span>')}
    <div class="cardgrid cardgrid--3">
      <div class="card"><div class="ic"><iconify-icon icon="ph:hand-heart-thin"></iconify-icon></div><h3>Technology should serve the experience, not replace it</h3><p>Entwine doesn't put a screen between a guest and a great meal. It makes the meal better — quietly, intelligently, in the background.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:globe-hemisphere-west-thin"></iconify-icon></div><h3>Local expertise, global ambition</h3><p>We started in Malta. We think in Europe. We operate through people who know their markets — because the best wine culture is always local first.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:users-three-thin"></iconify-icon></div><h3>Built by people who sit at both sides of the table</h3><p>As diners, we've been frustrated by the gap between wine lists and cellars. As operators, we know the pressure of running a great restaurant. Entwine was built from both.</p></div>
    </div>
  </section>
  <section class="r-sec dark has-bg js-reveal" id="story">
    <div class="r-bg"><img class="imgph" alt="" data-img="about-story" data-kw="wine,cellar,bottles,dark" data-w="1920" data-h="1200"></div>
    <div class="r-inner">
      {head('The founding story')}
      <div class="prose">
        <p>It started at dinner. Daniel and I were at a newly opened Michelin-starred restaurant. They gave us a digital wine list. We selected a wine — out of stock. We selected another — out of stock again. We settled for our third choice.</p>
        <p>Even at that level, the digital wine list had no connection to the actual cellar. If it was happening there, it was happening everywhere.</p>
        <p>The next morning Daniel arrived with the idea fully formed: wine pairing built specifically for what a restaurant actually has. I stress-tested it from every angle. It held up. That moment became a wine app — and a surreal shower moment a few weeks later gave it its name. <span class="gold">Entwine.</span></p>
      </div>
    </div>
  </section>
  <section class="r-sec dark js-reveal">
    {head('Our journey', 'From a frustrating dinner to a live platform — here’s how Entwine was built.')}
    <div class="timeline">
      <div class="tl"><div class="date">Jan 2023</div><h4>Concept formed</h4></div>
      <div class="tl"><div class="date">Apr 2023</div><h4>Research complete</h4></div>
      <div class="tl"><div class="date">Oct 2023</div><h4>Initial IMS + first app iteration</h4></div>
      <div class="tl"><div class="date">Jan 2024</div><h4>Second software & app iterations</h4></div>
      <div class="tl"><div class="date">Apr 2024</div><h4>Focus group feedback</h4></div>
      <div class="tl"><div class="date">Jul 2024</div><h4>First test restaurant launched</h4></div>
      <div class="tl"><div class="date">Sep 2024</div><h4>2 more restaurants + 3rd app iteration</h4></div>
      <div class="tl"><div class="date">Oct 2024</div><h4>Official public launch — Tech Expo</h4></div>
    </div>
  </section>
  <section class="r-sec js-reveal" id="team">
    {head('The people behind Entwine.')}
    <div class="team">
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Daniel Abela" data-img="team-daniel" data-kw="portrait,man,professional" data-w="600" data-h="600"></div><div class="nm">Daniel Abela</div><div class="ro">Co-founder · Vision &amp; Strategy</div><div class="bio">30+ years in brand strategy. Founder of Redorange, co-founder of Moving Ads, Cowfish, D4n6 and Rani — one of Entwine's founding club restaurants.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Claire Cassar" data-img="team-claire" data-kw="portrait,woman,professional" data-w="600" data-h="600"></div><div class="nm">Claire Cassar-Bonello</div><div class="ro">Co-founder · Revenue &amp; Growth</div><div class="bio">Tech lawyer, former CEO of HAUD, serial entrepreneur. A decade at Vodafone across Malta and Qatar. LL.D and Master's in Competition Law. Board member of MICAS.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Andrew Cachia" data-img="team-andrew" data-kw="portrait,man,developer" data-w="600" data-h="600"></div><div class="nm">Andrew Cachia</div><div class="ro">Co-founder · Technology</div><div class="bio">MSc in AI, Microsoft Accelerator alumni. Previously built an AI trading platform shown at the Davos World Economic Forum. The intelligence behind the pairing engine.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Krisztina Osman" data-img="team-krisztina" data-kw="portrait,woman,sommelier" data-w="600" data-h="600"></div><div class="nm">Krisztina Osman</div><div class="ro">Business Development &amp; Sommelier</div><div class="bio">WSET Level 2, 10+ years in hospitality across Malta and Hungary. Fluent in five languages. Leads onboarding and relationships across the club network.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Will Rizzo" data-img="team-will" data-kw="portrait,sommelier,wine" data-w="600" data-h="600"></div><div class="nm">Will Rizzo</div><div class="ro">Chief Sommelier · DipWSET</div><div class="bio">DipWSET-qualified sommelier who guided the development of Entwine's pairing algorithm. Every recommendation the platform makes carries his expertise.</div></div>
    </div>
  </section>
"""
ab += cta('We’re just getting started. <span class="gold">Come be part of it.</span>',
  "Entwine is a product of Cork &amp; Code Limited, a Malta-based technology company building global wine technology from the Mediterranean.",
  '<a class="btn btn--dark" href="invest.html">Invest in Entwine <span class="arrow">→</span></a>',
  [("See the platform", "restaurants.html"), ("Become a partner", "partners.html"), ("Join the team", "careers.html")])
page("about.html", "About Entwine — Technology in service of the table",
  "Entwine is a wine technology company built by people who sit on both sides of the table. Meet the team, the founding story, and what we believe.", ab)

# ============================================================ PRICING
pr = hero("Pricing",
  'The smartest addition to <span class="gold">your team.</span>',
  "A plan sized to fit your food and wine menu. Commit to an annual subscription and save 20%. All plans include a one-time onboarding fee of €150.",
  '<a class="btn btn--gold" href="#plans">See plans <span class="arrow">→</span></a><a class="btn btn--outline-light" href="#demo">Book a demo</a>',
  "pricing-hero", "wine,restaurant,table,dark")
pr += f"""
  <section class="r-sec js-reveal" id="plans">
    {head('Getting started — <span class="gold">€150 one-time.</span>', 'This covers your full onboarding: menu and wine list loaded, database matched, initial pairings configured, and your team trained. Everything you need to go live — handled by us.')}
    <div class="billing"><span class="on">Monthly</span><span>Annually · Save 20%</span></div>
    <div class="ptable">
      <div class="plan"><div class="pn">Starter</div><div class="pr">€120<small>/mo</small></div><div class="pa">€96/mo billed annually</div><div class="pd">For smaller restaurants getting started with intelligent wine management.</div><ul><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 100 wines paired</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 30 dishes</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 2 account users</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Inventory &amp; ordering</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>IMS training included</li></ul><a class="btn btn--outline-dark" href="#demo">Get started</a></div>
      <div class="plan plan--featured"><div class="pn">Plus</div><div class="pr">€150<small>/mo</small></div><div class="pa">€120/mo billed annually</div><div class="pd">For established restaurants ready to get more from their wine programme.</div><ul><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 150 wines paired</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 50 dishes</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 5 account users</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>SLA (office hours)</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Re-pairing fee €500</li></ul><a class="btn btn--gold" href="#demo">Get started</a></div>
      <div class="plan"><div class="pn">Pro</div><div class="pr">€200<small>/mo</small></div><div class="pa">€160/mo billed annually</div><div class="pd">Built for high-volume restaurants and multi-site operations with a serious wine programme.</div><ul><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 200 wines paired</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Up to 10 account users</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Multi-site IMS</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Dedicated account manager</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Re-pairing fee €750</li></ul><a class="btn btn--outline-dark" href="#demo">Get started</a></div>
      <div class="plan"><div class="pn">Enterprise</div><div class="pr">Custom</div><div class="pa">Volume pricing</div><div class="pd">For restaurant groups and hotel chains managing wine programmes across multiple sites.</div><ul><li><iconify-icon icon="ph:check-thin"></iconify-icon>Custom wines &amp; dishes</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Custom account users</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Multi-site IMS</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Custom SLA</li><li><iconify-icon icon="ph:check-thin"></iconify-icon>Dedicated account manager</li></ul><a class="btn btn--outline-dark" href="#demo">Contact us</a></div>
    </div>
  </section>
  <section class="r-sec tint js-reveal">
    {head('Pricing FAQ', 'Answers to common questions about plans and pricing.')}
    <div class="faq">
      <details><summary>Can I change my plan after signing up?<span class="chev"></span></summary><div class="ans">Yes — you can upgrade or downgrade at any time. We'll prorate the difference and re-pair your menu if your tier changes.</div></details>
      <details><summary>What happens if I need more wines or dishes than my plan allows?<span class="chev"></span></summary><div class="ans">Move up a tier whenever you need more capacity. Enterprise offers fully custom limits for large programmes.</div></details>
      <details><summary>What happens when my menu changes?<span class="chev"></span></summary><div class="ans">Re-pairing is handled by us. Plans include a re-pairing fee (€500–€1,000 depending on tier) for significant menu changes.</div></details>
      <details><summary>Is the onboarding fee charged every year?<span class="chev"></span></summary><div class="ans">No. The €150 onboarding fee is a one-time charge that covers your initial setup, database matching, and team training.</div></details>
      <details><summary>What's included in the SLA?<span class="chev"></span></summary><div class="ans">Office-hours support with guaranteed response times. Pro and Enterprise add a dedicated account manager and custom SLA terms.</div></details>
      <details><summary>Do I need to sign a long-term contract?<span class="chev"></span></summary><div class="ans">No long-term contract is required on monthly billing. Annual billing saves 20% in exchange for a yearly commitment.</div></details>
    </div>
  </section>
"""
pr += cta('Your restaurant could be live on Entwine in days.',
  "Let's make it happen. Book a demo and we'll show you exactly what Entwine does for your wine programme.",
  '<a class="btn btn--dark" href="#" id="demo">Book a demo <span class="arrow">→</span></a>',
  [("Explore free tools", "tools.html"), ("Get in touch", "#")])
page("pricing.html", "Entwine Pricing — Plans sized to your wine programme",
  "A plan sized to fit your food and wine menu. Save 20% annually. All plans include a one-time €150 onboarding fee.", pr)

# ============================================================ DOWNLOAD
dl = hero("Download",
  'Your own sommelier. <span class="gold">Free on iOS and Android.</span>',
  "Entwine is the wine pairing app that removes the guesswork from restaurant wine lists. Choose your dish, and we'll find the perfect match from the cellar.",
  BADGES, "download-hero", "wine,phone,app,dinner,dark")
dl += f"""
  <section class="r-sec dark has-bg js-reveal">
    <div class="r-bg"><img class="imgph" alt="" data-img="download-bg" data-kw="wine,glass,restaurant,dark" data-w="1920" data-h="1200"></div>
    <div class="r-inner">
      {head('Everything you need to <span class="gold">order with confidence.</span>')}
      <div class="steps">
        <div class="step"><div class="step__node"><iconify-icon icon="ph:fork-knife-thin"></iconify-icon></div><span class="step__num">Step 01</span><h3>Dish selection</h3><p>You're at an Entwine Club restaurant — open the app and the full menu is already there. Every dish, ready to pair to the ideal wine.</p></div>
        <div class="step"><div class="step__node"><iconify-icon icon="ph:sliders-horizontal-thin"></iconify-icon></div><span class="step__num">Step 02</span><h3>Set your preferences</h3><p>Filter by price, grape, region, or favour local. Entwine matches your dish to the wines on the restaurant's actual list.</p></div>
        <div class="step"><div class="step__node"><iconify-icon icon="ph:wine-thin"></iconify-icon></div><span class="step__num">Step 03</span><h3>Discover the pairing</h3><p>Get your perfect pairing with the story behind it — and build your taste profile over time. Every meal teaches Entwine more about you.</p></div>
      </div>
    </div>
  </section>
  <section class="r-sec tint js-reveal">
    {head('Ready to try it? <span class="gold">Find an Entwine restaurant near you.</span>', "Entwine is live at our founding club member restaurants in Malta, with rapid expansion planned across Europe. Experience seamless wine pairing at the finest dining establishments today.")}
    <div class="club__cta"><a class="btn btn--outline-dark" href="#">Find a restaurant <span class="arrow">→</span></a></div>
  </section>
"""
dl += cta('Ready to find your perfect pairing?',
  "Download Entwine free on iOS and Android. Scan the code or grab it from your app store.",
  '<a class="btn btn--dark" href="#">Download free <span class="arrow">→</span></a>',
  [("Find a restaurant", "#"), ("For restaurants", "restaurants.html")])
page("download.html", "Download Entwine — Free wine pairing on iOS &amp; Android",
  "Entwine removes the guesswork from restaurant wine lists. Choose your dish and get the perfect match from the cellar. Free on iOS and Android.", dl)

# ============================================================ INSIGHTS
ins = hero("Insights",
  'Wine knowledge. Restaurant intelligence. <span class="gold">Entwine thinking.</span>',
  "Guides for wine lovers, resources for restaurants, news from Entwine, and insights from the world of wine technology and hospitality.",
  '<a class="btn btn--gold" href="#articles">Read the latest <span class="arrow">→</span></a>',
  "insights-hero", "wine,books,reading,dark")
ins += f"""
  <section class="r-sec js-reveal" id="articles">
    <div class="pills"><a class="on">All</a><a>Wine education</a><a>Restaurant guides</a><a>Entwine news</a><a>Industry insights</a><a>Partner spotlights</a></div>
    <div class="cardgrid">
      <article class="card blogcard"><div class="ph2"><img class="imgph" alt="" data-img="insight-1" data-kw="wine,cellar,restaurant" data-w="800" data-h="500"></div><div class="meta"><span>Restaurant guides</span><span class="read">6 min read</span></div><h3>Why your digital wine list and your cellar need to be connected</h3><p>The disconnect between digital wine lists and actual cellars is costing restaurants guests — here's why, and how to fix it.</p></article>
      <article class="card blogcard"><div class="ph2"><img class="imgph" alt="" data-img="insight-2" data-kw="wine,food,pairing" data-w="800" data-h="500"></div><div class="meta"><span>Wine lovers</span><span class="read">5 min read</span></div><h3>Wine pairing 101 — a beginner's guide to pairing wine with food</h3><p>Everything you need to stop defaulting to the second-cheapest bottle — how food flavours interact with wine.</p></article>
      <article class="card blogcard"><div class="ph2"><img class="imgph" alt="" data-img="insight-3" data-kw="wine,list,restaurant" data-w="800" data-h="500"></div><div class="meta"><span>Restaurant guides</span><span class="read">7 min read</span></div><h3>How to build a wine list your guests will love</h3><p>It's about the relationship between your food menu, your cellar, and your guests' confidence. Here's how to get it right.</p></article>
      <article class="card blogcard"><div class="ph2"><img class="imgph" alt="" data-img="insight-4" data-kw="wine,dinner,story" data-w="800" data-h="500"></div><div class="meta"><span>Brand story</span><span class="read">4 min read</span></div><h3>The story behind Entwine — from a frustrating dinner to a live platform</h3><p>Three out-of-stock wines at a Michelin-starred restaurant, and the surreal shower moment that gave it its name.</p></article>
    </div>
    <div class="tools__all" style="margin-top:36px"><a class="btn btn--outline-dark" href="#">Load more articles <span class="arrow">→</span></a></div>
  </section>
  <section class="r-sec tint js-reveal">
    <div class="newsletter">
      {head('Stay in the loop.', 'New articles, product updates, and wine intelligence — straight to your inbox.')}
      <form onsubmit="return false"><input type="email" placeholder="Enter your email address" aria-label="Email address"><button class="btn btn--gold" type="submit">Keep me posted</button></form>
      <p class="note">No spam. Unsubscribe any time.</p>
    </div>
  </section>
"""
page("insights.html", "Entwine Insights — Wine knowledge &amp; restaurant intelligence",
  "Guides for wine lovers, resources for restaurants, news from Entwine, and insights from the world of wine technology and hospitality.", ins)

# ============================================================ CAREERS
ca = hero("Careers",
  'Small team. Big ambition. <span class="gold">Help us build the future of wine technology.</span>',
  "Entwine is a wine technology company at an exciting stage of growth. We're looking for people who care about wine, hospitality, and technology — and who are eager to help build something genuinely new.",
  '<a class="btn btn--gold" href="#roles">See open roles <span class="arrow">→</span></a>',
  "careers-hero", "team,restaurant,wine,people,dark")
ca += f"""
  <section class="r-sec tint js-reveal">
    {head("What it's like to be part of the Entwine team.")}
    <div class="cardgrid cardgrid--3">
      <div class="card"><div class="ic"><iconify-icon icon="ph:trend-up-thin"></iconify-icon></div><h3>Growing with the company</h3><p>Early team members grow with the business. The opportunity to shape how we scale — with employee share ownership for the right candidates.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:wine-thin"></iconify-icon></div><h3>Wine + tech + hospitality</h3><p>A rare intersection of three genuinely interesting industries. Work with restaurants, sommeliers, and wine professionals on a product people love.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:users-three-thin"></iconify-icon></div><h3>Small team, big ambition</h3><p>Everyone has real ownership over their work. No layers — direct access to founders. Your contribution is visible from day one.</p></div>
    </div>
  </section>
  <section class="r-sec js-reveal" id="roles">
    {head("We're building our team.", "These are the roles we're looking to fill.")}
    <div>
      <div class="job"><div><div class="dept">Restaurant Operations</div><h3>Customer Success Specialist</h3><div class="loc">Malta · Full-time or part-time</div><p>You'll be the first point of contact for Entwine's restaurant clients — supporting onboarding, managing relationships, and making sure every restaurant gets the most out of the platform. Organised, personable, and comfortable with hospitality professionals.</p></div><span class="av open">Open</span></div>
      <div class="job"><div><div class="dept">Sales &amp; Growth</div><h3>Club Growth Manager</h3><div class="loc">Malta-based · European travel · Full-time</div><p>You'll grow the Entwine club — bringing new restaurants onto the platform across Malta and into European markets. A relationship-led role for someone who knows hospitality and thrives in business development.</p></div><span class="av closed">Filled</span></div>
      <div class="job"><div><div class="dept">Technology</div><h3>Full-Stack Developer</h3><div class="loc">Remote-friendly · Full-time</div><p>You'll work alongside our CTO to build and improve the full Entwine platform — the consumer app, the restaurant IMS, and our suite of professional wine tools. Comfortable across the full stack; AI/ML experience a bonus.</p></div><span class="av open">Open</span></div>
    </div>
  </section>
"""
ca += cta("Don't see your role here? <span class=\"gold\">We'd still love to hear from you.</span>",
  "Wine. Technology. Hospitality. If that intersection excites you and you think you have something to contribute — get in touch and tell us about yourself.",
  '<a class="btn btn--dark" href="mailto:taste@entwine.club">Send us a note <span class="arrow">→</span></a>',
  [("Learn about Entwine", "about.html")])
page("careers.html", "Careers at Entwine — Wine. Technology. Hospitality.",
  "Entwine is a wine technology company at an exciting stage of growth. Explore open roles and help us build the future of wine technology.", ca)

# ============================================================ PARTNERS
pa = hero("Partners",
  'Your market is waiting. <span class="gold">Let’s build something together.</span>',
  "Entwine is building a network of channel partners across Europe and beyond. If you know restaurants, wine, or hospitality in your market — and you want to build a meaningful revenue stream alongside us — let's talk.",
  '<a class="btn btn--gold" href="#how">How it works <span class="arrow">→</span></a><a class="btn btn--outline-light" href="mailto:partner@entwine.club">Express interest</a>',
  "partners-hero", "wine,handshake,restaurant,business,dark")
pa += f"""
  <section class="r-sec tint js-reveal">
    {head('If restaurants trust your advice — <span class="gold">Entwine is the next conversation.</span>', 'Who is a channel partner? Five types.')}
    <div class="cardgrid cardgrid--3">
      <div class="card"><div class="ic"><iconify-icon icon="ph:wine-thin"></iconify-icon></div><h3>Wine consultant</h3><p>You advise restaurants on their wine programme. Entwine gives your clients the technology to execute it — and you a recurring revenue share on every account.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:chart-line-up-thin"></iconify-icon></div><h3>Restaurant consultant</h3><p>You help restaurants improve operations. Entwine's IMS is a natural fit for any client serious about their wine programme.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:graduation-cap-thin"></iconify-icon></div><h3>Sommelier / wine educator</h3><p>You train teams and shape their relationship with wine. Entwine puts intelligent pairing behind the knowledge you've instilled — and keeps clients coming back.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:fork-knife-thin"></iconify-icon></div><h3>F&amp;B consultant</h3><p>You advise on the full food and beverage offering. Entwine's IMS and pairing engine is the wine intelligence layer your clients are missing.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:buildings-thin"></iconify-icon></div><h3>Hospitality management consultant</h3><p>You help restaurants and hotel groups run better. Entwine's platform — from IMS to guest pairing — is a high-impact addition to any brief that touches dining.</p></div>
    </div>
  </section>
  <section class="r-sec dark has-bg js-reveal">
    <div class="r-bg"><img class="imgph" alt="" data-img="partners-bg" data-kw="wine,vineyard,europe,dark" data-w="1920" data-h="1200"></div>
    <div class="r-inner">
      {head('We reward both <span class="gold">the hunt and the farm.</span>')}
      <div class="cardgrid cardgrid--2">
        <div class="card"><div class="k">The hunt — onboarding</div><h3>Earn on every restaurant you bring in</h3><p>A revenue share every time you onboard a new restaurant. No cap within your territory. Each partner owns one territory — the market where their relationships run deepest.</p></div>
        <div class="card"><div class="k">The farm — retention</div><h3>Earn every month they stay active</h3><p>A revenue share every month your restaurant stays on Entwine. A partner with 10 active restaurants has a meaningful, growing recurring income. The more you retain, the more it compounds.</p></div>
      </div>
    </div>
  </section>
  <section class="r-sec js-reveal">
    {head('A partnership built to grow. <span class="gold">Here’s what we bring to it.</span>')}
    <div class="cardgrid cardgrid--3">
      <div class="card"><div class="ic"><iconify-icon icon="ph:student-thin"></iconify-icon></div><h3>Product &amp; pairing training</h3><p>Deep training so you can answer any question a restaurant throws at you.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:monitor-thin"></iconify-icon></div><h3>Platform access + demo</h3><p>Full access to Entwine so you can demo the product confidently to prospects.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:megaphone-simple-thin"></iconify-icon></div><h3>Marketing &amp; sales collateral</h3><p>Decks, one-pagers, and digital assets to present Entwine professionally in your market.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:gift-thin"></iconify-icon></div><h3>No cost to join</h3><p>No fee to become a partner. The investment is your time, relationships, and market knowledge.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:handshake-thin"></iconify-icon></div><h3>Co-branded materials</h3><p>Collateral carrying both brands — so you go to market as a credible, established partnership.</p></div>
      <div class="card"><div class="ic"><iconify-icon icon="ph:lifebuoy-thin"></iconify-icon></div><h3>Dedicated partner support</h3><p>A direct line to the Entwine team. Questions answered quickly, issues resolved fast.</p></div>
    </div>
  </section>
  <section class="r-sec tint js-reveal" id="how">
    {head('From first conversation to live in your market.', "Here's how it works.")}
    <div class="steps">
      <div class="step"><div class="step__node"><iconify-icon icon="ph:paper-plane-tilt-thin"></iconify-icon></div><span class="step__num">Step 01</span><h3>Express interest</h3><p>Fill in a short form or drop us a message at partner@entwine.club.</p></div>
      <div class="step"><div class="step__node"><iconify-icon icon="ph:phone-thin"></iconify-icon></div><span class="step__num">Step 02</span><h3>Intro call</h3><p>We learn about your market, your network, and what a great partnership looks like for you.</p></div>
      <div class="step"><div class="step__node"><iconify-icon icon="ph:handshake-thin"></iconify-icon></div><span class="step__num">Step 03</span><h3>Go live</h3><p>Formalise the partnership, complete onboarding and training, then start bringing restaurants into the club — earning on every one you onboard and retain.</p></div>
    </div>
  </section>
  <section class="r-sec js-reveal">
    {head('Partner FAQ', 'Answers to common questions about becoming a partner.')}
    <div class="faq">
      <details><summary>Is there a cost to becoming a channel partner?<span class="chev"></span></summary><div class="ans">No. There's no fee to join. Your investment is your time, your relationships, and your market knowledge.</div></details>
      <details><summary>How is the revenue share calculated?<span class="chev"></span></summary><div class="ans">You earn on both onboarding and monthly retention for every restaurant you bring into the club within your territory.</div></details>
      <details><summary>Do I need wine industry experience?<span class="chev"></span></summary><div class="ans">Not strictly — but relationships with restaurants and an understanding of hospitality go a long way. We provide full product and pairing training.</div></details>
      <details><summary>Can I partner with Entwine in more than one market?<span class="chev"></span></summary><div class="ans">Each partner owns one territory — the market where their relationships run deepest. We can discuss additional territories as you grow.</div></details>
      <details><summary>What kind of support do I get once I'm live?<span class="chev"></span></summary><div class="ans">A dedicated partner contact, co-branded materials, demo access, early feature access, and on-the-ground support for key events and meetings.</div></details>
    </div>
  </section>
"""
pa += cta('Your market. Our platform. <span class="gold">Let’s grow it together.</span>',
  "Wherever wine is taken seriously, Entwine belongs there. If you know the territory — let's talk.",
  '<a class="btn btn--dark" href="mailto:partner@entwine.club">Express interest <span class="arrow">→</span></a>',
  [("Get in touch", "mailto:partner@entwine.club")])
page("partners.html", "Entwine Partners — Bring Entwine to your market",
  "Become an Entwine channel partner. Earn a revenue share on every restaurant you onboard and retain. Your market, our platform — let's grow it together.", pa)

# ============================================================ INVEST
iv = hero("Invest",
  'We’ve built it, launched it, <span class="gold">and the market has validated it.</span>',
  "A clear gap. A validated market. A platform that connects both sides of the table. We're raising to move faster — and every investment moves Entwine forward.",
  '<a class="btn btn--gold" href="#raise">Why invest now <span class="arrow">→</span></a><a class="btn btn--outline-light" href="#options">Invest on Zaar</a>',
  "invest-hero", "wine,investment,growth,dark")
iv += f"""
  <section class="r-sec dark js-reveal">
    {head('Built, launched, validated.')}
    <div class="statgrid">
      <div class="stat"><div class="big">8,000+</div><div class="lbl">Wines in the database</div><div class="d">Built from producer technical sheets — not scraped data. The foundation of the pairing engine.</div></div>
      <div class="stat"><div class="big">iOS + Android</div><div class="lbl">Consumer app live</div><div class="d">Restaurant-specific pairing available at the table, on both platforms.</div></div>
      <div class="stat"><div class="big">7 tools</div><div class="lbl">Live &amp; generating revenue</div><div class="d">Four free, two freemium, one one-time. Driving B2B interest and direct revenue.</div></div>
      <div class="stat"><div class="big">IMS</div><div class="lbl">Deployed &amp; operating</div><div class="d">Live across founding club restaurants. Inventory tracked, orders placed, lists optimised.</div></div>
    </div>
  </section>
  <section class="r-sec js-reveal" id="raise">
    {head('Why invest now', 'The market gap is real. The product is proven. The opportunity is now.')}
    <div class="cardgrid cardgrid--2">
      <div class="card"><div class="k">The timing argument</div><h3>Acceleration, not development</h3><p>The product is built and proven — this is acceleration funding. The market space is unoccupied: no direct competitor connects restaurant menus to consumer pairing at scale. The channel-partner model creates asset-light expansion — growth without proportional overhead.</p></div>
      <div class="card"><div class="k">What the raise funds</div><h3>Move faster, reach further</h3><p>More restaurants onboarded. A more powerful pairing engine. New app features — including the one-off pairing tool and wine list stress test. A channel-partner network that takes Entwine global, and a growing user base that unlocks the advertising revenue layer.</p></div>
    </div>
  </section>
  <section class="r-sec dark has-bg js-reveal">
    <div class="r-bg"><img class="imgph" alt="" data-img="invest-bg" data-kw="vineyard,wine,europe,dark" data-w="1920" data-h="1200"></div>
    <div class="r-inner">
      {head('A global market. <span class="gold">An unoccupied space.</span>')}
      <div class="cardgrid cardgrid--2">
        <div class="card"><div class="k">Global wine-tech angle</div><h3>$500B market, 44% in Europe</h3><p>The global wine market is valued at over $500 billion, growing ~5% annually. Europe leads with 44% of global revenue — Entwine's home territory. No platform connects the consumer pairing experience directly to a restaurant's actual menu. That space is unoccupied.</p></div>
        <div class="card"><div class="k">Dual B2B + consumer SaaS</div><h3>Two revenue streams that reinforce each other</h3><p>A consumer app with recurring engagement and in-app advertising at scale; a B2B IMS with recurring subscription revenue; revenue-generating tools; and an asset-light channel-partner model. Two primary streams that reinforce each other — and a third emerging through the tools.</p></div>
      </div>
    </div>
  </section>
  <section class="r-sec js-reveal" id="options">
    {head('Join our early supporters. <span class="gold">Every investment moves Entwine forward.</span>')}
    <div class="cardgrid cardgrid--2">
      <div class="card"><div class="k">Zaar · Malta</div><h3>Invest on Zaar</h3><p>Our primary crowdfunding campaign — open to investors in Malta and internationally. Target €50,000. Campaign window: May–Jun 2026.</p><a class="more" href="#">Campaign link once live <span>→</span></a></div>
      <div class="card"><div class="k">Crowdcube · Europe</div><h3>Invest on Crowdcube</h3><p>Equity crowdfunding for European investors. Investing through Crowdcube means you become a shareholder in Entwine.</p><a class="more" href="#">Find out more <span>→</span></a></div>
    </div>
  </section>
  <section class="r-sec dark js-reveal">
    {head('Our founding team')}
    <div class="team">
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Daniel Abela" data-img="team-daniel" data-kw="portrait,man,professional" data-w="600" data-h="600"></div><div class="nm">Daniel Abela</div><div class="ro">Co-founder · Vision &amp; Strategy</div><div class="bio">30+ years building brands. Founder of Redorange, co-founder of Moving Ads, Cowfish, D4n6, and Rani — a founding club restaurant. An operator's perspective on the problem Entwine solves.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Claire Cassar" data-img="team-claire" data-kw="portrait,woman,professional" data-w="600" data-h="600"></div><div class="nm">Claire Cassar-Bonello</div><div class="ro">Co-founder · Revenue &amp; Growth</div><div class="bio">Serial entrepreneur and tech CEO. Former CEO of HAUD, board member of MICAS. LL.D and Master's in Competition Law. Former senior roles at Vodafone Malta.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Andrew Cachia" data-img="team-andrew" data-kw="portrait,man,developer" data-w="600" data-h="600"></div><div class="nm">Andrew Cachia</div><div class="ro">Co-founder · Technology</div><div class="bio">MSc in AI, Microsoft Accelerator alumni. Built an AI trading platform shown at Davos. The ML engine behind Entwine's pairing algorithm is built on his expertise.</div></div>
      <div class="teammate"><div class="ph2"><img class="imgph" alt="Will Rizzo" data-img="team-will" data-kw="portrait,sommelier,wine" data-w="600" data-h="600"></div><div class="nm">Will Rizzo</div><div class="ro">Chief Sommelier · DipWSET</div><div class="bio">DipWSET-qualified sommelier — the wine intelligence behind Entwine. He guided the pairing algorithm so every recommendation is grounded in genuine expertise.</div></div>
    </div>
  </section>
  <section class="r-sec tint js-reveal">
    {head('Investor FAQ', 'Answers to common questions about our business model and financials.')}
    <div class="faq">
      <details><summary>What stage is Entwine at?<span class="chev"></span></summary><div class="ans">Built, launched, and validated. The app and IMS are live across founding club restaurants in Malta, with seven tools generating B2B interest and revenue. This is acceleration funding.</div></details>
      <details><summary>What will the funds be used for?<span class="chev"></span></summary><div class="ans">Onboarding more restaurants, a more powerful pairing engine, new app features, and a channel-partner network that takes Entwine global.</div></details>
      <details><summary>What is the difference between Zaar and Crowdcube?<span class="chev"></span></summary><div class="ans">Zaar is our Malta-based primary campaign (open internationally). Crowdcube is equity crowdfunding for European investors — you become a shareholder.</div></details>
      <details><summary>Who are the founding club member restaurants?<span class="chev"></span></summary><div class="ans">A group of Malta's respected restaurants — including Rani — that helped shape the platform and run it live today.</div></details>
      <details><summary>I'm interested in a larger or institutional investment — who do I contact?<span class="chev"></span></summary><div class="ans">Reach our team directly at invest@entwine.club.</div></details>
    </div>
  </section>
"""
iv += cta('Be part of what comes next. <span class="gold">The opportunity is open now.</span>',
  "The right wine, at the right table, in every restaurant that takes wine seriously. Institutional enquiries: invest@entwine.club.",
  '<a class="btn btn--dark" href="#">Invest on Zaar <span class="arrow">→</span></a>',
  [("Invest on Crowdcube", "#"), ("Get in touch", "mailto:invest@entwine.club")])
page("invest.html", "Invest in Entwine — Built, launched, validated",
  "A clear gap, a validated market, and a platform that connects both sides of the table. Join Entwine's early supporters on Zaar and Crowdcube.", iv)

# ============================================================ TOOLS HUB
EXT = ' target="_blank" rel="noopener"'
to = hero("Free Tools",
  'Seven degrees of separation — <span class="gold">between a good wine programme and a great one.</span>',
  "From auditing your wine list to training your team — seven tools built for wine professionals. Most are free. All are worth your time. No account needed to get started.",
  '<a class="btn btn--gold" href="#tools">Explore the tools <span class="arrow">→</span></a>',
  "tools-hero", "wine,list,laptop,restaurant,dark")
to += f"""
  <section class="r-sec tint js-reveal">
    {head('Understanding our pricing tiers', 'Tools designed to fit your budget and growth trajectory.')}
    <div class="tiers">
      <div class="tier"><div class="nm">Free</div><div class="ct">4 tools</div><p>Essential tools available to all restaurants at absolutely no cost. Perfect for getting started.</p></div>
      <div class="tier"><div class="nm">Freemium</div><div class="ct">2 tools</div><p>Powerful core features for free, with optional premium upgrades for advanced capabilities.</p></div>
      <div class="tier"><div class="nm">One-time fee</div><div class="ct">1 tool</div><p>Premium, specialised tools available for a single, flat-rate purchase. No recurring subscriptions.</p></div>
    </div>
  </section>
  <section class="r-sec js-reveal" id="tools">
    {head('Seven professional tools. <span class="gold">Yours to try first.</span>')}
    <div class="cardgrid cardgrid--3">
      <div class="card"><span class="tag">Free</span><h3>Wine List Audit</h3><p>Upload your wine list and get a scored audit in minutes — gaps, imbalances, margin opportunities, and pairing blind spots. No filters pulled.</p><a class="more" href="#"{EXT}>Start free <span>→</span></a></div>
      <div class="card"><span class="tag">Free</span><h3>BTG Optimiser</h3><p>Analyse your by-the-glass selection for margin, variety, and pairing value. See which pours are working and which are holding you back.</p><a class="more" href="#"{EXT}>Start free <span>→</span></a></div>
      <div class="card"><span class="tag">Free · Upgrades</span><h3>Wine List Gap Finder</h3><p>Identify the style, region, and price-point gaps in your current wine list. Know exactly what's missing before your next buying decision.</p><a class="more" href="#"{EXT}>Start free <span>→</span></a></div>
      <div class="card"><span class="tag">Free</span><h3>Digital Menu Builder</h3><p>Build a clean digital menu your guests can browse and order from — reducing wait times and staff load.</p><a class="more" href="#"{EXT}>Start free <span>→</span></a></div>
      <div class="card"><span class="tag">One-time fee</span><h3>Sommelier Pairing Service</h3><p>Expert, on-demand pairing for a special menu or event — a single flat-rate purchase, no subscription.</p><a class="more" href="#"{EXT}>View pricing <span>→</span></a></div>
      <div class="card"><span class="tag">Freemium</span><h3>Wine List Creator</h3><p>Create a balanced wine list from scratch. Core features free, with advanced segmentation on premium.</p><a class="more" href="#"{EXT}>Learn more <span>→</span></a></div>
      <div class="card"><span class="tag">Freemium</span><h3>Team Wine Trainer</h3><p>Train your front-of-house team with quizzes and tasting notes. Free tier included; premium automates and tracks progress.</p><a class="more" href="#"{EXT}>Learn more <span>→</span></a></div>
    </div>
  </section>
"""
to += cta('The tools showed you what’s possible. <span class="gold">The platform delivers it — every day.</span>',
  "The free tools give you a snapshot of your wine programme's potential. The Entwine IMS gives you the full picture — inventory, ordering, analytics, and guest pairing. All connected.",
  '<a class="btn btn--dark" href="restaurants.html">See the full platform <span class="arrow">→</span></a>',
  [("Contact us for a demo", "#"), ("Pricing", "pricing.html")])
page("tools.html", "Entwine Free Tools — Seven professional wine tools",
  "Seven tools built for wine professionals — from auditing your wine list to training your team. Most are free. No account needed to get started.", to)

print("DONE")
