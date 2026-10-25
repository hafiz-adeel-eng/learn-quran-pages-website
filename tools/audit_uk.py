"""Content and route checks independent of the page renderer."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from collections import Counter
import csv, itertools, json, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.hrefs=[];self.graph=[];self.script=False;self.buffer=[];self.faq=0;self.images=[];self.main=False;self.skip=0;self.main_text=[];self.heading=None;self.heading_text=[];self.headings=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ('h1','h2'):self.heading=t;self.heading_text=[]
  if t=='main':self.main=True
  if self.main and t in ('aside','script','style'):self.skip+=1
  if 'id'in a:self.ids.add(a['id'])
  if t=='a':self.hrefs.append(a.get('href',''))
  if t=='details':self.faq+=1
  if t=='img':self.images.append(a)
  if t=='script' and a.get('type')=='application/ld+json':self.script=True;self.buffer=[]
 def handle_data(self,s):
  if self.script:self.buffer.append(s)
  if self.heading:self.heading_text.append(s)
  if self.main and not self.skip:self.main_text.append(s)
 def handle_endtag(self,t):
  if t==self.heading:self.headings.append([t,' '.join(''.join(self.heading_text).split())]);self.heading=None
  if self.main and t in ('aside','script','style'):self.skip-=1
  if t=='main':self.main=False
  if t=='script' and self.script:self.graph.extend(json.loads(''.join(self.buffer)).get('@graph',[]));self.script=False
rows=list(csv.DictReader((ROOT/'content/uk_locations.tsv').open(),delimiter='\t'))
urls=[x.text for x in ET.parse(PUBLIC/'sitemap.xml').getroot().iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
errors=[];pages={};types=Counter()
for url in urls:
 path=urlparse(url).path;p=Page();p.feed((PUBLIC/path.lstrip('/')/'index.html').read_text());pages[path]=p
 if path=='/':continue
 for image in p.images:
  if not all(image.get(k) for k in ['alt','width','height']):errors.append([path,'Image attributes'])
 for g in p.graph:
  types[g.get('@type')]+=1
  if g.get('@type')=='FAQPage' and len(g['mainEntity'])!=p.faq:errors.append([path,'FAQ schema count'])
 for href in p.hrefs:
  parsed=urlparse(href)
  if parsed.netloc in ['quranlyhub.com','www.quranlyhub.com'] and parsed.path!='/my-classes/':errors.append([path,'Reference navigation',href])
for path,p in pages.items():
 for href in p.hrefs:
  u=urlparse(href)
  if u.netloc or not u.fragment:continue
  target=u.path or path
  if target in pages and u.fragment not in pages[target].ids:errors.append([path,'Missing anchor',href])
# Name-normalized five-word overlap: includes independently authored practice paragraphs.
def grams(text):
 text=text.lower()
 for r in rows:text=text.replace(r['name'].lower(),'CITY')
 w=re.findall(r'\w+',text);return set(zip(*(w[i:] for i in range(5))))
sets=[grams(' '.join(r[k] for k in ['brief','question','answer','practice','review'])) for r in rows]
pairs=[]
for i,j in itertools.combinations(range(len(rows)),2):
 a,b=sets[i],sets[j];pairs.append((len(a&b)/len(a|b),rows[i]['name'],rows[j]['name']))
pairs.sort(reverse=True)
if pairs[0][0]>.5:errors.append(['City content','High authored-block overlap',pairs[0]])
redirects=[line.split() for line in (PUBLIC/'_redirects').read_text().splitlines()]
for old,new,status in redirects:
 if old==new or urlparse(new).path not in pages:errors.append(['redirect',old,new])
counts={path:len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",' '.join(p.main_text))) for path,p in pages.items()}
for path,count in counts.items():
 if not 1500<=count<=2000:errors.append([path,'Main content outside 1500–2000 words',count])
(ROOT/'research/current-word-counts.json').write_text(json.dumps([{'path':path,'main_content_words':count} for path,count in counts.items()],indent=2))
baseline=json.loads((ROOT/'content/heading-baseline.json').read_text())
for path,page in pages.items():
 if page.headings!=baseline[path]:errors.append([path,'H1/H2 changed'])
report={'word_minimum':1500,'minimum_main_content_words':min(counts.values()),'unchanged_heading_pages':sum(p.headings==baseline[path] for path,p in pages.items()),'word_limit':2000,'maximum_main_content_words':max(counts.values()),'pages':len(urls),'coverage_by_nation':dict(Counter(r['nation'] for r in rows)),'courses':6,'guides':6,'city_authored_copy':{'unique_introductions':len(set(r['brief'] for r in rows)),'unique_specific_questions':len(set(r['question'] for r in rows)),'unique_practice_paragraphs':len(set(r['practice'] for r in rows)),'maximum_name_normalized_five_word_jaccard':round(pairs[0][0],4),'closest_pairs':pairs[:5],'note':'This tests authored blocks. Shared navigation, factual service details and selected teaching-reference passages intentionally repeat. This statistic is for authored city blocks, not whole-page duplication.'},'schema_counts':dict(types),'errors':errors,'visual_review':'No connected browser available. Responsive CSS breakpoints are implemented; screenshot comparisons were not performed.'}
(ROOT/'research/uk-content-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2));assert not errors,errors[:10]
