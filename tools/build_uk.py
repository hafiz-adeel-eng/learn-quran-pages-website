"""Build Quran Hub's UK service pages from reviewed editorial data. No network calls."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urlparse, quote, urlencode
from collections import Counter
import csv, hashlib, importlib.util, json, re, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
ORIGIN='https://learnquran-86k.pages.dev'
SOURCE='https://quranlyhub.com'
PHONE='923439486140'
spec=importlib.util.spec_from_file_location('uk_content',ROOT/'content/uk_content.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
extra_spec=importlib.util.spec_from_file_location('uk_expansion',ROOT/'content/uk_expansion.py')
E=importlib.util.module_from_spec(extra_spec);extra_spec.loader.exec_module(E)
for key,data in C.AUDIENCES.items():data['sections']=data['sections']+E.AUDIENCE_EXTRA[key]
C.GUIDES=[(slug,title,description,sections+E.GUIDE_EXTRA[slug]) for slug,title,description,sections in C.GUIDES]
LOCATIONS=list(csv.DictReader((ROOT/'content/uk_locations.tsv').open(),delimiter='\t'))
assert len(LOCATIONS)==83 and len({x['name'] for x in LOCATIONS})==83

def slug(value):
 return re.sub(r'[^a-z0-9]+','-',value.lower()).strip('-')
def loc_path(row):return '/locations/uk/'+slug(row['name'])+'/'
def nation_path(nation):return '/locations/uk/'+slug(nation)+'/'
def link(path,label):return '<a href="'+escape(path,quote=True)+'">'+escape(label)+'</a>'
def para(text):return '<p>'+escape(text)+'</p>'
def bullets(items):return '<ul>'+''.join('<li>'+escape(x)+'</li>' for x in items)+'</ul>'
def section(title,content,sid=''):
 return '<section'+(' id="'+sid+'"' if sid else '')+'><h2>'+escape(title)+'</h2>'+content+'</section>'
def wa(location='UK',course='a suitable Quran course'):
 return 'https://wa.me/'+PHONE+'?'+urlencode({'text':f'Assalamualaikum! Quran Hub, I would like a free trial for {course}. Location: {location}. Please confirm a suitable teacher, UK-time slot and the fee.'})
def button(url,label):return '<a class="elementor-button elementor-button-link qhuk-button" href="'+escape(url,quote=True)+'">'+escape(label)+' <span aria-hidden="true">→</span></a>'
def actions(location='UK'):
 return '<div class="qhuk-actions">'+button(wa(location),'Book a free trial')+link('/pricing/','See fees and lesson details')+'</div>'
def image(course=None):
 path=course['image'] if course else '2026/08/home-hero-quranlyhub-online-quran-academy-1024x1024.webp'
 alt='Course learning illustration: '+course['name'] if course else 'Student attending a live online Quran lesson using a laptop and headphones'
 width,height=(1586,992) if course and course['slug']=='quran-reading-tajweed' else (1535,1024) if course and course['slug'] in ('quran-memorization-hifz','advanced-tajweed') else (1536,1024) if course else (1024,1024)
 return '<img src="'+SOURCE+'/wp-content/uploads/'+path+'" alt="'+escape(alt,quote=True)+'" width="'+str(width)+'" height="'+str(height)+'" loading="lazy" decoding="async">'

COURSES={x['slug']:x for x in C.COURSES}
NATIONS=['England','Scotland','Wales','Northern Ireland']
NATION_COPY={
 'England':('Online Quran Classes in England for Kids and Adults','Families can compare the teaching plan with the school or working week they actually follow. Term dates can differ between councils, schools and academies, so confirm your own calendar when arranging a recurring lesson. A UK-time appointment does not automatically define holiday or missed-class arrangements.'),
 'Scotland':('Online Quran Classes in Scotland: UK-Time Private Lessons','Scottish school and university calendars can differ from those used elsewhere in the UK. Share the dates relevant to your household instead of planning from an English term-time example. Scotland follows UK GMT/BST clock changes; the lesson should be confirmed in local UK time, with changes discussed directly.'),
 'Wales':('Online Quran Classes in Wales for Children and Adults','Welsh-medium schooling does not imply that an online academy teaches in Welsh. Quran Hub lists teaching in English, Arabic and Urdu; explain any language needs before booking and use the trial to check comfortable communication. Confirm your own school calendar and the recurring UK-time appointment separately.'),
 'Northern Ireland':('Online Quran Classes in Northern Ireland','Families in Northern Ireland can enquire for private online lessons without travelling to a teaching centre. Confirm appointments in UK local time, while using the relevant school or working calendar for breaks. Bangor in Northern Ireland has a separate location page from Bangor in Wales, and Derry/Londonderry uses one combined enquiry page to avoid duplicate destinations.'),
}
COURSE_LINKS=[('/courses/'+c['slug']+'/',c['name']) for c in C.COURSES]
CORE_LINKS=[('/locations/uk/','UK overview'),('/online-quran-classes-for-kids-uk/','Classes for kids'),('/online-quran-classes-for-adults-uk/','Classes for adults'),('/online-quran-classes-for-beginners-uk/','Classes for beginners'),('/female-quran-teachers-uk/','Female teacher requests'),('/pricing/','Fees and monthly plans')]
GUIDE_LINKS=[('/blog/'+g[0]+'/',g[1]) for g in C.GUIDES]

def nav_links(items,cls=''):
 return ''.join('<a'+(' class="'+cls+'"' if cls else '')+' href="'+p+'">'+escape(t)+'</a>' for p,t in items)
def chrome():
 courses='<ul class="qh-nav-drop">'+''.join('<li>'+link(p,t)+'</li>' for p,t in COURSE_LINKS)+'</ul>'
 places='<ul class="qh-nav-drop"><li>'+link('/locations/uk/','All UK cities and towns')+'</li>'+''.join('<li>'+link(nation_path(n),n)+'</li>' for n in NATIONS)+'</ul>'
 chev='<svg class="qh-nav-chev" viewBox="0 0 12 8" fill="none" aria-hidden="true"><path d="m1 1 5 5 5-5" stroke="currentColor" stroke-width="1.6"/></svg>'
 header='<header class="qh-head"><div class="qh-head__in"><button class="qh-burger" aria-label="Open navigation" aria-controls="qh-drawer" aria-expanded="false" data-qh-open><span></span><span></span><span></span></button><a class="qh-brand" href="/"><b>Quran <i>Hub</i></b><span>Online Quran &amp; Arabic Academy</span></a><nav class="qh-nav" aria-label="Main navigation">'+link('/','Home')+'<div class="qh-nav-item"><button class="qh-nav-toggle" type="button" aria-haspopup="true" aria-expanded="false">Courses '+chev+'</button>'+courses+'</div><div class="qh-nav-item"><button class="qh-nav-toggle" type="button" aria-haspopup="true" aria-expanded="false">UK locations '+chev+'</button>'+places+'</div>'+nav_links([('/blog/','Learning guides'),('/about/','About'),('/contact/','Contact')])+'</nav><a class="qh-cta" href="/contact/">Book Free Trial</a></div></header>'
 mobile='<div class="qh-drawer" id="qh-drawer" data-open="false"><div class="qh-drawer__veil" data-qh-close></div><div class="qh-drawer__panel" role="dialog" aria-modal="true" aria-label="Site menu"><div class="qh-drawer__top"><span class="qh-brand"><b>Quran <i>Hub</i></b></span><button class="qh-close" aria-label="Close menu" data-qh-close>×</button></div>'+nav_links([('/','Home')]+CORE_LINKS,'qh-dlink')+'<div class="qh-dgroup"><button class="qh-dlink qh-dtoggle" type="button" aria-expanded="false" aria-controls="qh-uk-courses" data-qh-toggle>Courses '+chev+'</button><div class="qh-dsub" id="qh-uk-courses" data-open="false">'+nav_links(COURSE_LINKS,'qh-dlink')+'</div></div><div class="qh-dgroup"><button class="qh-dlink qh-dtoggle" type="button" aria-expanded="false" aria-controls="qh-uk-nations" data-qh-toggle>UK locations '+chev+'</button><div class="qh-dsub" id="qh-uk-nations" data-open="false">'+nav_links([(nation_path(n),n) for n in NATIONS],'qh-dlink')+'</div></div>'+nav_links([('/blog/','Learning guides'),('/about/','About Quran Hub'),('/contact/','Contact'),(SOURCE+'/my-classes/','Existing student portal')],'qh-dlink')+'<a class="qh-drawer__cta" href="/contact/">Book Free Trial</a></div></div><nav class="qh-bar" aria-label="Quick actions"><a class="qh-bar-gold" href="/contact/">Book Free Trial Class</a><a class="qh-bar-teal" href="/courses/">Our Courses</a></nav>'
 floating='<div class="qh-wa-float"><a class="qh-wa-fab" href="'+escape(wa(),quote=True)+'" aria-label="Chat with Quran Hub on WhatsApp" target="_blank" rel="noopener"><svg viewBox="0 0 32 32" aria-hidden="true" fill="currentColor"><path d="M16 2a14 14 0 0 0-12 21L2 30l7-2A14 14 0 1 0 16 2Zm0 2.5a11.5 11.5 0 1 1-6 21.3l-.5-.3-4 1.1 1.1-4-.3-.5A11.5 11.5 0 0 1 16 4.5Zm-4 4c-.5 0-1 .2-1.4.7-1 1.3-1 2.8-.2 4.5 1.7 3.7 4.8 6.3 8.3 7.3 1.7.5 3.5-.3 4-1.6.2-.5.3-1.2-.2-1.5l-2.6-1.3c-.4-.2-.7-.1-.9.3l-1 1.2c-2.3-1-4-2.4-5.1-4.3l1-1.3c.2-.3.3-.6.1-1l-1.2-2.6c-.2-.4-.5-.5-.8-.4Z"/></svg></a></div>'
 footer='<footer class="qh-foot"><div class="qh-foot__in"><div class="qh-foot__grid"><div class="qh-foot-brand"><b>Quran <i>Hub</i></b><p>Live one-to-one online Quran learning for children and adults. UK lesson times are confirmed in GMT or BST.</p>'+link('/contact/','Book a free trial')+'</div><div><h3 class="qh-foot-heading">Courses</h3><ul>'+''.join('<li>'+link(p,t)+'</li>' for p,t in COURSE_LINKS)+'</ul></div><div><h3 class="qh-foot-heading">UK learning</h3><ul>'+''.join('<li>'+link(p,t)+'</li>' for p,t in CORE_LINKS[:5])+'</ul></div><div><h3 class="qh-foot-heading">Quran Hub</h3><ul>'+''.join('<li>'+link(p,t)+'</li>' for p,t in [('/blog/','Learning guides'),('/pricing/','Fees'),('/about/','About'),('/contact/','Contact'),('/privacy-policy/','Privacy'),('/terms-of-service/','Lesson terms')])+'</ul></div></div><div class="qh-foot__bottom"><span>© 2026 Quran Hub. All rights reserved.</span><span>Online lessons • No UK classroom is claimed.</span></div></div></footer>'
 return header,mobile+floating,footer

PAGE_REGISTRY=[]
def write_page(path,title,description,lead,body,crumbs,faq=None,kind='service',city=None,hero_image=None):
 if not path.startswith('/') or not path.endswith('/'):raise ValueError(path)
 faq=faq or []
 canonical=ORIGIN+path
 graph=[{'@type':'EducationalOrganization','@id':ORIGIN+'/#academy','name':'Quran Hub','url':ORIGIN+'/','email':'info@quranlyhub.com','telephone':'+923439486140','areaServed':{'@type':'Country','name':'United Kingdom'},'contactPoint':{'@type':'ContactPoint','contactType':'course enquiries','telephone':'+923439486140','availableLanguage':['English','Arabic','Urdu']}},{'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'inLanguage':'en-GB','isPartOf':{'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'Quran Hub'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':ORIGIN+p} for i,(p,name) in enumerate(crumbs)]}]
 if kind=='service':graph.append({'@type':'Service','@id':canonical+'#service','name':title,'description':description,'serviceType':'Live online Quran tuition','provider':{'@id':ORIGIN+'/#academy'},'areaServed':{'@type':'Place','name':city,'containedInPlace':{'@type':'Country','name':'United Kingdom'}} if city else {'@type':'Country','name':'United Kingdom'},'availableChannel':{'@type':'ServiceChannel','serviceUrl':canonical}})
 if kind=='article':graph.append({'@type':'Article','headline':title,'description':description,'mainEntityOfPage':{'@id':canonical+'#webpage'},'author':{'@type':'Organization','name':'Quran Hub'},'publisher':{'@id':ORIGIN+'/#academy'}})
 if kind=='course':graph.append({'@type':'Course','name':title,'description':description,'provider':{'@id':ORIGIN+'/#academy'},'inLanguage':['en','ar','ur'],'url':canonical})
 if faq:graph.append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faq]})
 faq_html=section('Questions before you book','<div class="qhuk-faq">'+''.join('<details name="uk-faq"><summary>'+escape(q)+'</summary>'+para(a)+'</details>' for q,a in faq)+'</div>','questions') if faq else ''
 header,mobile,footer=chrome()
 trail='<nav class="qhuk-breadcrumb" aria-label="Breadcrumb">'+'<span aria-hidden="true"> / </span>'.join(link(p,n) for p,n in crumbs)+'</nav>'
 hero='<section class="qhuk-hero"><div class="qhuk-wrap qhuk-hero-grid"><div>'+trail+'<p class="qhuk-eyebrow">Quran Hub • Live online learning</p><h1>'+escape(title)+'</h1>'+para(lead)+'<div class="qhuk-pills"><span>One-to-one tuition</span><span>UK time: GMT / BST</span><span>Free trial</span></div>'+actions(city or 'UK')+'</div><figure class="qhuk-hero-image'+(' qhuk-course-hero-image' if kind=='course' else '')+'">'+(hero_image or image())+'<figcaption>'+('Course illustration from the Quran Hub course collection.' if kind=='course' else 'Live learning from home; illustrative student image.')+'</figcaption></figure></div></section>'
 aside='<aside class="qhuk-aside"><div class="qhuk-panel"><h2>Find your starting point</h2>'+nav_links(CORE_LINKS,'qhuk-side-link')+'</div><div class="qhuk-panel"><h2>Practical learning guides</h2>'+nav_links(GUIDE_LINKS,'qhuk-side-link')+'</div></aside>'
 html='<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+' | Quran Hub</title><meta name="description" content="'+escape(description,quote=True)+'"><meta name="robots" content="index, follow"><meta name="theme-color" content="#16847A"><link rel="canonical" href="'+canonical+'"><meta property="og:type" content="'+('article' if kind=='article' else 'website')+'"><meta property="og:title" content="'+escape(title,quote=True)+'"><meta property="og:description" content="'+escape(description,quote=True)+'"><meta property="og:url" content="'+canonical+'"><meta property="og:site_name" content="Quran Hub"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/uk.css"><script src="/original-interactions.js" defer></script><script src="/interactions.js" defer></script><script src="/uk.js" defer></script><script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')+'</script></head><body class="page page-id-280 qhuk-page"><a class="qhuk-skip" href="#main">Skip to content</a>'+header+'<main id="main"><div class="elementor-280">'+hero+'<div class="qhuk-wrap qhuk-body"><article class="qhuk-article">'+body+faq_html+'<section class="qhuk-trial"><h2>Discuss a suitable free trial</h2><p>Tell us the learner’s level, preferred UK-time windows and any teacher preference. We will confirm availability and the appropriate course before you choose a plan.</p>'+actions(city or 'UK')+'</section></article>'+aside+'</div></div></main>'+mobile+footer+'</body></html>'
 target=PUBLIC/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)
 PAGE_REGISTRY.append({'path':path,'title':title,'description':description,'kind':kind,'city':city,'text':unescape(re.sub('<[^>]+>',' ',body))})

def course_list():
 return '<div class="qhuk-cards">'+''.join('<article><a class="qhuk-course-image" href="/courses/'+c['slug']+'/" aria-label="'+escape(c['name'],quote=True)+'">'+image(c)+'</a><p class="qhuk-eyebrow">'+escape(c['level'])+'</p><h3>'+link('/courses/'+c['slug']+'/',c['name'])+'</h3>'+para(c['intro'])+link('/courses/'+c['slug']+'/','Explore the course →')+'</article>' for c in C.COURSES)+'</div>'
def city_grid(rows):
 return '<div class="qhuk-city-grid">'+''.join('<a data-city="'+escape((r['name']+' '+r['nation']+' '+r['region']).lower(),quote=True)+'" href="'+loc_path(r)+'"><strong>'+escape(r['name'])+'</strong><span>'+escape(r['nation'])+'</span></a>' for r in rows)+'</div>'
def fees():
 return '<div class="qhuk-table-scroll"><table><caption>Published Quran Hub monthly fees, per learner, in USD</caption><thead><tr><th>Course group</th><th>8 lessons / month</th><th>16 lessons / month</th><th>Lesson length</th></tr></thead><tbody><tr><th>Qaida, Quran reading, advanced Tajweed, Hifz and Quranic Arabic</th><td>USD 30</td><td>USD 40</td><td>30 minutes</td></tr><tr><th>Tafseer</th><td>USD 60</td><td>USD 100</td><td>30 minutes</td></tr></tbody></table></div><p class="qhuk-note">These are the published USD plans, not GBP quotations. Confirm the current fee, payment currency and any conversion charges directly before enrolling. Tutor availability and lesson arrangements are confirmed separately.</p>'

def build_city(row):
 name=row['name'];nation=row['nation'];focus=C.FOCUS[row['focus']]
 path=loc_path(row)
 title='Online Quran Classes in '+name+' for Kids & Adults'
 description=f'Live one-to-one Quran lessons for {name} learners. Explore a suitable course, UK-time scheduling, published fees and a free trial with Quran Hub.'
 lead=f'Learn from home in {name} through live, one-to-one Quran lessons. Discuss your starting level, teaching language and UK-time availability before choosing a course.'
 body=section('Online Quran classes in '+name+': a suitable learning plan',para(row['brief'])+para('These are online lessons for learners in '+name+'. No physical teaching centre or home-visit service in this location is claimed. The first decision is whether the teaching format and explanation suit the individual learner.'))
 body+=section(focus[0],para(focus[4])+bullets(focus[3])+para('Use these as trial discussion points, not as a promised curriculum or an assessment result. A teacher needs to listen before recommending the next stage.'))
 body+=section('Quran classes for kids and adults: choose a suitable course',para('For the learning question discussed on this page, consider '+focus[1]+' as a conversation starter, then let the reading assessment guide the choice. Children and adults can have different needs even when studying the same text.')+'<p>'+link('/courses/'+focus[2]+'/',focus[1])+' · '+link('/online-quran-classes-for-kids-uk/','Children’s learning')+' · '+link('/online-quran-classes-for-adults-uk/','Adult learning')+' · '+link('/online-quran-classes-for-beginners-uk/','Complete beginners')+'</p>')
 body+=section('A practical next step for your lesson',para(row['practice'])+para(row['review']))
 body+=section('An example note to take into the trial','<blockquote><p>Location: '+escape(name)+'. My main question is: '+escape(row['question'])+' I would like the teacher to hear a short sample and explain a suitable first practice task.</p></blockquote>'+para('This is a preparation example, not a student testimonial. Add your own reading experience and two practical UK-time windows. Explain the difficulty honestly rather than choosing a course only because it sounds more advanced.'))
 body+=section('Online Quran lesson times: GMT, BST and local planning',para(NATION_COPY[nation][1])+'<p>'+link(nation_path(nation),'Explore lessons across '+nation)+' · '+link('/blog/uk-quran-class-times-gmt-bst/','Read the GMT/BST planning guide')+'</p>')
 body+=section('Online Quran class fees and teacher availability',para('The standard published plans begin at USD 30 for eight 30-minute lessons per month; sixteen standard lessons are USD 40. Tafseer has separate pricing. These amounts are not GBP prices, and a suitable teacher, preference and recurring slot need confirmation.')+'<p>'+link('/pricing/','See the full fee table and questions to ask before payment')+' · '+link('/female-quran-teachers-uk/','Request a female teacher')+'</p>')
 peers=[r for r in LOCATIONS if r['region']==row['region'] and r['name']!=name]
 if not peers:peers=[r for r in LOCATIONS if r['nation']==nation and r['name']!=name]
 peers=peers[:4]
 body+=section('Other enquiry pages in '+row['region'],city_grid(peers)+'<p>'+link('/locations/uk/','Browse all 83 UK cities and towns')+'</p>')
 faq=[(row['question'],row['answer']),('What should I include in my '+name+' trial enquiry?','Share the learner’s reading experience, their main difficulty and realistic UK-time windows. For this enquiry, start with the question on this page: '+row['question']),('Do I need to travel to join these classes?','No. This is an online service-area page. Use the trial to test clear audio, a readable shared page and the learner’s comfort with remote teaching before deciding whether to continue.')]
 write_page(path,title,description,lead,body,[('/','Home'),('/locations/uk/','UK'),(nation_path(nation),nation),(path,name)],faq,city=name)

def build_main_hubs():
 path='/locations/uk/'
 body=section('Online Quran classes UK: choose a useful starting point',para('A UK location enquiry should lead to a suitable learning plan, not simply a list of cities. Start with the learner’s level: first Arabic letters, connected reading, recurring Tajweed mistakes, memorisation or guided understanding. A trial gives you a chance to hear the teacher’s explanation and discuss the practical arrangement before choosing a monthly plan.')+'<div class="qhuk-cards">'+''.join('<article><h3>'+link(p,t)+'</h3>'+para(desc)+'</article>' for (p,t),desc in zip(CORE_LINKS[1:5],['Readiness, parent involvement and a workable home routine.','Private lessons for an adult starting point or a return to study.','Find out whether letters, joining or supported reading comes first.','Discuss tutor preference, teaching language and availability.']))+'</div>')
 body+=section('From Noorani Qaida to Tajweed, Hifz and understanding',course_list())
 body+=section('One-to-one online Quran classes: teachers and free trials',para('Quran Hub’s listed teaching model is live and one-to-one. Ask the academy to explain the tutor’s relevant experience and credentials, listen to a correction and let the learner try again. Parents can discuss how they will remain involved; adults can ask for a private starting assessment. Do not assume a recording, background-check or cancellation policy from another academy’s advertising.')+'<p>'+link('/blog/first-online-quran-trial/','Prepare for the first trial')+' · '+link('/blog/safe-online-quran-tutor-questions/','Questions to ask about teaching arrangements')+'</p>')
 body+=section('Lesson times in England, Scotland, Wales and Northern Ireland',para('Appointments should be confirmed in UK local time: GMT in winter and BST during the summer clock period. School calendars can differ by nation, council and school. Tell us your actual availability and confirm the next lesson when the clocks change; a suggested timetable is not a live appointment listing.')+'<p>'+link('/blog/uk-quran-class-times-gmt-bst/','Plan a clear UK-time routine')+'</p>')
 body+=section('Online Quran class fees for UK families',fees())
 body+=''.join(section(h,para(t)) for h,t in E.UK_EXTRA)
 directory='<label class="qhuk-search-label" for="city-search">Find your UK city or town</label><input class="qhuk-city-search" id="city-search" type="search" placeholder="Search city, nation or region" aria-describedby="city-count"><p id="city-count" role="status">83 locations: 76 official UK cities and 7 additional towns.</p>'
 for nation in NATIONS:
  rows=[r for r in LOCATIONS if r['nation']==nation]
  directory+='<section class="qhuk-directory-nation"><h3>'+link(nation_path(nation),nation)+'</h3>'+city_grid(rows)+'</section>'
 body+=section('Browse every UK city and the additional reference towns',directory,'city-directory')
 body+=section('How this coverage is defined',para('The city directory follows the Cabinet Office list for England, Scotland, Wales and Northern Ireland. It adds Luton, Blackburn, Huddersfield, Dewsbury, Slough, Oldham and Bolton from the academy’s reference coverage. Crown Dependencies and Overseas Territories are not included as UK cities. The directory describes online service areas, not a network of physical classrooms.')+'<p>'+link('https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html','Official UK city list')+'</p>')
 faq=[('Are these online Quran classes available throughout the UK?','You can enquire from anywhere in the UK with a suitable connection. A teacher, preferred language and recurring UK-time appointment must be confirmed.'),('Do you have a teaching centre in every listed city?','No. The directory describes learners’ online service areas. It does not claim local premises, a mosque partnership or a home-visit service.'),('Are your fees quoted in pounds?','The published plans shown here are in USD. Ask the academy to confirm the payment amount and any conversion before comparing them with a GBP quotation.'),('How do I choose the best online Quran class for my family?','Use a real trial, compare individual reading time and explanation, and check fees, teacher continuity, communication and attendance arrangements. The best fit depends on the learner rather than an unsupported ranking.')]
 write_page(path,'Online Quran Classes UK for Kids and Adults','Explore one-to-one Quran classes across all 76 UK cities and 7 additional towns, with beginner pathways, published fees and free trial enquiries.','Find live Quran lessons matched to your reading level and a practical UK-time routine. Compare the course paths, prepare for a free trial and browse the city directory.',body,[('/','Home'),(path,'UK classes')],faq)
 for nation in NATIONS:
  path=nation_path(nation);title,intro=NATION_COPY[nation]
  rows=[r for r in LOCATIONS if r['nation']==nation]
  body=section('Online Quran classes in '+nation+': planning your lessons',para(intro)+para('Explain whether lessons are for a child, adult or family, then describe current reading and a realistic regular slot. A free trial should help establish the starting level and whether the teaching explanation is suitable.'))
  body+=section('Choose a learning path','<p>'+nav_links(CORE_LINKS[1:5],'qhuk-chip-link')+'</p>'+para('A location does not determine a course level. A learner who knows some surahs from memory may still need a reading check, while someone returning after a break may retain skills that can be built on.'))
  body+=section('Cities and towns in '+nation,city_grid(rows))
  body+=section('Fees and clear lesson arrangements',fees()+'<p>'+link('/pricing/','Understand fees and attendance questions')+' · '+link('/blog/first-online-quran-trial/','Plan a useful trial')+'</p>')
  body+=''.join(section(h,para(t)) for h,t in E.NATION_EXTRA[nation])
  write_page(path,title,'Explore Quran Hub online lessons, suitable starting courses and city enquiries across '+nation+'. UK-time appointments and tutor preferences are confirmed.',intro,body,[('/','Home'),('/locations/uk/','UK'),(path,nation)],[(f'Is there a physical Quran Hub centre in {nation}?','No physical teaching centre is claimed. The pages describe live online lessons for learners in the listed service areas.'),(f'Which time zone is used for {nation} lessons?','Use UK local time and confirm the appointment when GMT/BST changes. Your school or working calendar should be discussed separately.')])

def build_audiences_and_courses():
 paths={'kids':'/online-quran-classes-for-kids-uk/','adults':'/online-quran-classes-for-adults-uk/','beginners':'/online-quran-classes-for-beginners-uk/','female-teachers':'/female-quran-teachers-uk/'}
 for key,data in C.AUDIENCES.items():
  path=paths[key];body=''.join(section(h,para(t)) for h,t in data['sections'])
  body+=section('Explore a suitable course',course_list())
  body+=section('Published fees and a clear next step',para('A free trial does not require payment or a credit card. Standard published plans are USD 30 for eight or USD 40 for sixteen 30-minute lessons per month, with separate Tafseer fees. Confirm the actual course, teacher and recurring UK-time slot before choosing a plan.')+'<p>'+link('/pricing/','View fees and payment questions')+' · '+link('/locations/uk/','Find your UK city')+' · '+link('/blog/first-online-quran-trial/','What to ask in the trial')+'</p>')
  write_page(path,data['title'],data['description'],data['lead'],body,[('/','Home'),('/locations/uk/','UK'),(path,data['title'])],data['faq'])
 body=section('Match the course to the reading sample',para('These six courses address different learning needs. Use the descriptions to prepare a useful enquiry, then ask the tutor for a recommendation based on actual reading. No course is automatically the right choice for every child, adult or learner in a particular city.')+course_list())
 body+=section('Before choosing a monthly plan',para('Confirm lesson length, session frequency, teaching language, tutor preference and the payment currency. Ask how attendance changes are handled and what practice will be expected between sessions. A detailed course title should not substitute for that practical conversation.')+'<p>'+link('/pricing/','Compare the published plans')+' · '+link('/locations/uk/','UK city coverage')+'</p>')
 write_page('/courses/','Online Quran Courses: Qaida, Tajweed, Hifz, Tafseer and Arabic','Compare six Quran learning paths and discuss an appropriate starting level with Quran Hub in a free one-to-one trial.','Choose a course from your current learning need, then confirm a suitable starting point with a teacher.',body,[('/','Home'),('/courses/','Courses')],kind='collection')
 for c in C.COURSES:
  path='/courses/'+c['slug']+'/'
  body=section({'noorani-qaida':'Learn Noorani Qaida online: letters, vowels and joined reading','quran-reading-tajweed':'Online Quran classes with Tajweed: reading and pronunciation','quran-memorization-hifz':'Online Hifz classes: Quran memorisation and revision','tafseer':'Online Tafseer classes: guided Quran understanding','advanced-tajweed':'Advanced Tajweed classes: articulation and recitation rules','quranic-arabic':'Quranic Arabic classes: vocabulary and understanding'}[c['slug']],bullets(c['topics'])+para('These are areas to discuss in the trial. The order and pace should be appropriate to the learner rather than a fixed completion promise.'))
  body+=section('A structured starting sequence','<ol>'+''.join('<li>'+escape(x)+'</li>' for x in c['path'])+'</ol>')
  body+=section('A common mistake to avoid',para(c['mistake']))
  body+=''.join(section(h,para(t)) for h,t in E.COURSE_EXTRA[c['slug']])
  body+=section('Practising between live lessons',para('Ask the tutor for a small exercise that was demonstrated in the lesson, a clear model and an explanation of what to bring back next time. Record uncertainty instead of guessing at a correction. The teacher should check whether the skill transfers to another suitable example before increasing the workload.')+'<p>'+link('/blog/quran-practice-for-children/','Supporting a child’s practice')+' · '+link('/blog/first-online-quran-trial/','Preparing a useful trial')+'</p>')
  body+=section('Private lessons for UK learners',para('Children and adults can enquire from the UK directory. Agree the teaching language, preferred teacher and a realistic GMT/BST appointment. If the learner has previous experience, bring the last book or passage studied so the assessment can build on it appropriately.')+'<p>'+link('/online-quran-classes-for-beginners-uk/','Starting as a beginner')+' · '+link('/online-quran-classes-for-adults-uk/','Adult learning')+'</p>')
  body+=section('Fees and the next learning stage',para('Tafseer uses separately published fees; the other listed courses use the standard monthly plans. The tutor should explain whether the next course is appropriate before you change focus.')+'<p>'+link('/pricing/','View the actual fee table')+' · '+link('/courses/'+c['next']+'/',COURSES[c['next']]['name'])+'</p>')
  faq=[('Can I try '+c['name']+' before choosing a plan?','A free trial is available to discuss level and suitability. Tell the academy your starting experience and preferred UK-time windows; the teacher and arrangement need confirmation.'),('Is a completion date guaranteed?','No. Progress depends on the starting point, accurate practice and an appropriate teaching pace. Review the next step with the tutor rather than relying on a fixed completion promise.'),('Can I request a female teacher for this course?','You can request a female teacher when enquiring. Availability depends on a suitable teacher and a mutually workable lesson time.')]
  write_page(path,c['title'],c['intro'],c['intro'],body,[('/','Home'),('/courses/','Courses'),(path,c['name'])],faq,kind='course',hero_image=image(c))

def build_guides():
 for name,title,description,sections in C.GUIDES:
  path='/blog/'+name+'/'
  body='<p class="qhuk-note">Quran Hub learning guide. Practical education information; individual plans are agreed with the tutor.</p>'+''.join(section(h,para(p)) for h,p in sections)
  body+=section('Useful next reading','<ul>'+''.join('<li>'+link(p,t)+'</li>' for p,t in CORE_LINKS[1:5])+'</ul>')
  if name=='uk-quran-class-times-gmt-bst':body+=section('Official clock-change information','<p>'+link('https://www.gov.uk/when-do-the-clocks-change','GOV.UK: when the UK clocks change')+'</p>')
  write_page(path,title,description,description,body,[('/','Home'),('/blog/','Learning guides'),(path,title)],kind='article')
 body=section('Practical answers before you enrol','<div class="qhuk-cards">'+''.join('<article><h2>'+link('/blog/'+name+'/',title)+'</h2>'+para(description)+link('/blog/'+name+'/','Read the guide →')+'</article>' for name,title,description,_ in C.GUIDES)+'</div>')
 body+=section('Connect the guide to a real learning path',para('Use the guides to prepare questions, compare the format and understand the routine. A reading assessment should still guide the course recommendation. City pages describe online service areas rather than local teaching centres.')+'<p>'+link('/courses/','Compare courses')+' · '+link('/locations/uk/','UK locations')+'</p>')
 write_page('/blog/','Quran Learning Guides for UK Families and Adult Learners','Read practical Quran Hub guides on teacher selection, trial lessons, practice, Hifz revision, UK lesson times and parent questions.','Use these guides to make a more informed course and tutor enquiry, rather than relying on a promise or a course name alone.',body,[('/','Home'),('/blog/','Learning guides')],kind='collection')

def build_support():
 body=section('Online Quran class pricing for UK families',fees())
 body+=section('Compare the fee on a like-for-like basis',para('Check the currency, session length, lessons per month, individual or group format and the course included. The published USD amounts should not be presented as pounds. Your bank or payment provider may apply a conversion or charge; ask for the actual payment arrangement before deciding whether the plan fits your budget.'))
 body+=section('What to confirm before payment',bullets(['Which course and teacher have been agreed','The number and duration of lessons included','The UK-time recurring appointment and any clock-change arrangement','How missed lessons, cancellations and tutor changes are handled','The final payment amount and currency']))
 body+=section('Free trial and teacher requests',para('The free trial is usually 20 to 30 minutes and does not require payment or a credit card. Use it to meet the teacher, discuss the starting point and ask how regular teaching will work. A requested female teacher or preferred slot depends on availability; confirm the match before treating it as booked.'))
 body+=section('Choosing a manageable frequency',para('A learner’s realistic practice time and attention should inform the schedule. More sessions do not automatically produce better retention if the work cannot be reviewed accurately. Ask the tutor to explain the recommended frequency and what should happen between lessons.')+'<p>'+link('/blog/hifz-revision-around-school/','Planning Hifz revision')+' · '+link('/blog/best-online-quran-classes-uk/','Comparing academies fairly')+'</p>')
 faq=[('Do you publish GBP fees?','The plans currently published on this site are in USD. Request a confirmed payment amount and any applicable conversion before enrolling.'),('Does Tafseer cost the same as the standard courses?','No. Tafseer is listed at USD 60 for eight or USD 100 for sixteen monthly 30-minute lessons; the standard plans are USD 30 and USD 40 respectively.'),('Is there an automatic sibling discount?','No sibling discount is promised here. Describe your family’s enquiry and ask the academy to confirm any current arrangement.'),('Can I reschedule or cancel a lesson?','Contact the tutor or academy as early as possible. The applicable arrangement must be confirmed for your plan; this page does not promise unlimited make-up sessions or an automatic refund.')]
 write_page('/pricing/','Online Quran Class Fees for UK Learners: Plans and Trial','See Quran Hub’s published USD monthly plans, separate Tafseer fees and the payment, scheduling and trial questions UK families should confirm.','Compare the actual number of lessons, duration and course before choosing a monthly plan. Prices below retain their published USD currency.',body,[('/','Home'),('/pricing/','Fees')],faq,kind='information')
 form='<form class="qhuk-enquiry" data-uk-enquiry><label>Your name<input name="name" autocomplete="name" required maxlength="100"></label><label>City or town<input name="location" autocomplete="address-level2" required maxlength="120" placeholder="For example: Glasgow, Scotland"></label><label>Learner<select name="learner"><option>Child</option><option>Adult</option><option>Family enquiry</option></select></label><label>Starting point<select name="level"><option>Not sure — please assess</option><option>First Arabic letters</option><option>Reading with corrections</option><option>Hifz and revision</option><option>Tafseer or Arabic</option></select></label><label>Preferred UK-time windows<input name="times" maxlength="200" placeholder="Include days and local UK times"></label><label>Teacher or language preference<textarea name="message" rows="3" maxlength="600"></textarea></label><p class="qhuk-note">This opens WhatsApp with your enquiry prepared. You review and send it there; this website does not store the form details.</p><button class="qhuk-submit" type="submit">Prepare my free-trial enquiry →</button></form>'
 body=section('Prepare a useful free-trial enquiry',form)
 body+=section('What happens next',para('The academy can discuss the learner’s level, a suitable teacher and the preferred UK-time windows. A proposed course or timetable should be confirmed before payment. If you prefer email, contact info@quranlyhub.com; WhatsApp uses the existing academy contact number shown in the link.')+'<p>'+link('mailto:info@quranlyhub.com','Email the academy')+' · '+link(wa(),'Open WhatsApp directly')+'</p>')
 body+=section('Before choosing a plan','<p>'+link('/blog/first-online-quran-trial/','Read the trial checklist')+' · '+link('/pricing/','Check published fees')+' · '+link('/privacy-policy/','How enquiry details are handled')+'</p>')
 write_page('/contact/','Book a Free Online Quran Trial with Quran Hub','Send Quran Hub a free-trial enquiry with the learner’s starting point, location, UK-time availability and tutor preference.','Tell us who the lessons are for and what you want to work on. A free trial is a chance to discuss fit before choosing a monthly plan.',body,[('/','Home'),('/contact/','Free trial')],kind='information')
 body=section('An individual starting point',para('Quran Hub presents live, one-to-one online Quran courses for children and adults. A starting assessment helps distinguish first-letter reading, recitation correction, memorisation and guided understanding, so a course name does not replace listening to the learner.'))
 body+=section('What we encourage you to check',para('Ask about the proposed teacher’s relevant credentials and experience, teaching language, availability and correction style. The reference academy describes Ijazah-certified Quran tutors, but a family should still understand the particular teaching arrangement before enrolling. This site does not claim a local UK office, fabricated tutor profile, DBS check or independent review score.'))
 body+=section('A routine that fits real life',para('Appointments should be discussed in UK local time, including GMT/BST changes. A short practice task can support the live lesson, while attendance, cancellation and rescheduling terms need direct confirmation. The aim is a clear, realistic first step rather than a guaranteed completion promise.'))
 body+=section('Explore the learning paths',course_list())
 write_page('/about/','About Quran Hub: One-to-One Online Quran Learning','Understand Quran Hub’s online learning approach, starting assessments, UK-time enquiries and the questions to ask before enrolling.','A clear starting point, guided practice and an informed decision about the teacher and course.',body,[('/','Home'),('/about/','About')],kind='information')
 privacy=section('Enquiries and contact details',para('The trial form prepares a WhatsApp message on your device. It does not send or store that form information on this static website. When you choose to send the message or email the academy, the contact service and the academy receive the details you provide for responding to the enquiry. Avoid sharing information that is not needed to arrange a lesson.'))+section('Hosting, images and external services',para('The site is hosted through Cloudflare Pages. Original course images and font files may load from the reference academy’s public asset URLs, and WhatsApp or email opens an external service. Those providers may process technical data under their own policies. This static site does not add an advertising analytics script.'))+section('Questions about your information','<p>Contact '+link('mailto:info@quranlyhub.com','info@quranlyhub.com')+' to ask about enquiry information shared with the academy. For information already sent through an external service, also consult that service’s privacy controls.</p>')
 write_page('/privacy-policy/','Privacy and Enquiry Information','How the Quran Hub static website handles the trial form, external WhatsApp and email enquiries, hosting and public media assets.','Read how a website enquiry is prepared and what happens when you choose an external contact service.',privacy,[('/','Home'),('/privacy-policy/','Privacy')],kind='information')
 terms=section('Online tuition and availability',para('This website describes online courses and allows a learner to enquire about a free trial. A course, teacher, regular lesson time and paid plan are not reserved until the academy confirms them. City pages are online service-area information; they do not promise a physical local classroom.'))+section('Fees and attendance arrangements',para('The published plans are shown in USD. Confirm the final fee, payment currency, lesson duration and course before paying. Ask directly about cancellation, refunds, missed sessions, make-up lessons and teacher changes; this website does not create additional guarantees beyond the arrangement confirmed with the academy.'))+section('Learning outcomes and information',para('Progress varies with the starting point, practice and teaching fit. No completion deadline, search ranking or educational outcome is guaranteed by these pages. Learning guides are general preparation information and should not be treated as an individual assessment or a religious ruling.'))+section('Contact','<p>'+link('/contact/','Discuss a course or an existing arrangement')+' before relying on a general description where your circumstances need clarification.</p>')
 write_page('/terms-of-service/','Course Enquiries and Lesson Terms','Understand what is confirmed at enquiry, the published fee currency and why attendance and payment arrangements need direct agreement.','Use the course descriptions to prepare an enquiry, then confirm the arrangement that applies to your lessons.',terms,[('/','Home'),('/terms-of-service/','Lesson terms')],kind='information')

def rewrite_home():
 p=PUBLIC/'index.html';home=p.read_text()
 mapping={'/locations/':'/locations/uk/','/locations/uk/':'/locations/uk/','/services/':'/courses/','/blog/':'/blog/','/contact/':'/contact/','/about-our-academy/':'/about/','/pricing/':'/pricing/','/privacy-policy/':'/privacy-policy/','/terms-of-service/':'/terms-of-service/'}
 for c in C.COURSES:mapping['/services/'+c['slug']+'/']='/courses/'+c['slug']+'/'
 for r in LOCATIONS:
  name=slug(r['name']);dest=loc_path(r)
  mapping['/locations/uk/'+name+'/']=dest
  mapping['/online-quran-classes-'+name+'/']=dest
 mapping['/online-quran-classes-huddersfield-dewsbury/']='/locations/uk/huddersfield/'
 def href(m):
  old=unescape(m[1]);u=urlparse(old)
  if u.netloc in ('quranlyhub.com','www.quranlyhub.com') and u.path in mapping:return 'href="'+mapping[u.path]+('?' + u.query if u.query else '')+('#'+u.fragment if u.fragment else '')+'"'
  return m[0]
 home=re.sub(r'href="([^"]*)"',href,home)
 head,mobile,foot=chrome()
 discovery='<section class="qhuk-discovery"><div class="qhuk-wrap"><p class="qhuk-eyebrow">Quran Hub in the UK</p><h2>Find online Quran classes for your starting point and location</h2><p>Explore all 76 UK cities and seven additional towns, then compare a suitable learning path and prepare for a free trial.</p><div class="qhuk-discovery-links">'+nav_links(CORE_LINKS+GUIDE_LINKS[:2],'qhuk-chip-link')+'</div>'+button('/locations/uk/','Explore UK classes and cities')+'</div></section>'
 home,n=re.subn(r'<header\b[^>]*class="qh-head".*?</footer>',lambda _:head+mobile+discovery+foot,home,flags=re.S)
 if n!=1:raise ValueError('Expected one homepage header-to-footer navigation region')
 if '<link rel="stylesheet" href="/uk.css">' not in home:home=home.replace('</head>','<link rel="stylesheet" href="/uk.css"><script src="/uk.js" defer></script></head>')
 p.write_text(home)

def write_sitemap():
 paths=['/']+[p['path'] for p in PAGE_REGISTRY]
 if len(paths)!=len(set(paths)):raise ValueError('Duplicate canonical route')
 root=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
 for path in sorted(paths):ET.SubElement(ET.SubElement(root,'url'),'loc').text=ORIGIN+path
 ET.indent(root,space='  ')
 (PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n')
 (PUBLIC/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
 redirects=[]
 for c in C.COURSES:redirects.append('/services/'+c['slug']+'/ /courses/'+c['slug']+'/ 301')
 for row in LOCATIONS:redirects.append('/online-quran-classes-'+slug(row['name'])+'/ '+loc_path(row)+' 301')
 redirects+=['/locations/ /locations/uk/ 301','/services/ /courses/ 301','/online-quran-classes-huddersfield-dewsbury/ /locations/uk/huddersfield/ 301','/about-our-academy/ /about/ 301']
 (PUBLIC/'_redirects').write_text('\n'.join(redirects)+'\n')

def validate():
 class Page(HTMLParser):
  def __init__(self):super().__init__();self.h1=0;self.links=[];self.ids=[];self.title=False;self.titles=[];self.canonical=[];self.json=False;self.json_text=[];self.schemas=[]
  def handle_starttag(self,tag,attrs):
   a=dict(attrs)
   if tag=='h1':self.h1+=1
   if tag=='title':self.title=True
   if tag=='a' and 'href' in a:self.links.append(a['href'])
   if 'id' in a:self.ids.append(a['id'])
   if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
   if tag=='script' and a.get('type')=='application/ld+json':self.json=True;self.json_text=[]
  def handle_endtag(self,tag):
   if tag=='title':self.title=False
   if tag=='script' and self.json:self.schemas.append(json.loads(''.join(self.json_text)));self.json=False
  def handle_data(self,data):
   if self.title:self.titles.append(data)
   if self.json:self.json_text.append(data)
 failures=[];titles=[];pages=['/']+[p['path'] for p in PAGE_REGISTRY]
 for path in pages:
  file=PUBLIC/'index.html' if path=='/' else PUBLIC/path.strip('/')/'index.html'
  source=file.read_text();page=Page();page.feed(source)
  if page.h1!=1:failures.append((path,'H1 count',page.h1))
  if len(page.ids)!=len(set(page.ids)):failures.append((path,'duplicate IDs'))
  if page.canonical!=[ORIGIN+path]:failures.append((path,'canonical',page.canonical))
  if 'noindex' in source.lower():failures.append((path,'noindex'))
  titles.append(''.join(page.titles))
  for target in page.links:
   u=urlparse(target)
   if not u.netloc and u.path.startswith('/'):
    dest=PUBLIC/u.path.lstrip('/')
    if not (dest.is_file() or (dest/'index.html').is_file()):failures.append((path,'missing local page',u.path))
  if path!='/' and 'QuranlyHub' in source:failures.append((path,'old brand'))
 if len(titles)!=len(set(titles)):failures.append(('all','duplicate titles'))
 # Check the actual editorial blocks rather than shared navigation, fees and chrome.
 paragraphs=[r['brief']+' '+r['question']+' '+r['answer']+' '+r['practice'] for r in LOCATIONS]
 if len(set(paragraphs))!=83:failures.append(('cities','duplicate editorial copy'))
 report={'total_indexable_pages':len(pages),'city_and_town_pages':83,'official_cities':76,'additional_towns':7,'supporting_pages':len(PAGE_REGISTRY)-83,'unique_titles':len(set(titles)),'errors':failures,'scope':'UK service pages plus courses, audience pathways and practical learning guides','limits':'Static checks do not establish search rankings, rich-result eligibility or visual screenshot equivalence.'}
 (ROOT/'research').mkdir(exist_ok=True)
 (ROOT/'research/uk-build-validation.json').write_text(json.dumps(report,indent=2))
 if failures:raise ValueError(json.dumps(failures[:20]))
 print(json.dumps(report))

if __name__=='__main__':
 for row in LOCATIONS:build_city(row)
 build_main_hubs();build_audiences_and_courses();build_guides();build_support();rewrite_home();write_sitemap();validate()
