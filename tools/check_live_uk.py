"""Read-only post-deploy checks against this build's canonical URLs."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import json, re, time, urllib.request, urllib.error, urllib.parse, xml.etree.ElementTree as ET
ORIGIN='https://learnquran-86k.pages.dev';PUBLIC=Path(__file__).resolve().parents[1]/'public'
NS='{http://www.sitemaps.org/schemas/sitemap/0.9}'
BASELINES=json.loads((PUBLIC.parent/'content/heading-baseline.json').read_text())
class Outline(HTMLParser):
 def __init__(self):super().__init__();self.main=False;self.skip=0;self.text=[];self.heading=None;self.parts=[];self.headings=[]
 def handle_starttag(self,t,a):
  if t=='main':self.main=True
  if self.main and t in ('aside','script','style'):self.skip+=1
  if t in ('h1','h2'):self.heading=t;self.parts=[]
 def handle_data(self,s):
  if self.main and not self.skip:self.text.append(s)
  if self.heading:self.parts.append(s)
 def handle_endtag(self,t):
  if t==self.heading:self.headings.append([t,' '.join(''.join(self.parts).split())]);self.heading=None
  if self.main and t in ('aside','script','style'):self.skip-=1
  if t=='main':self.main=False
def fetch(url):
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'QuranHub-Deployment-Check/1.0'}),timeout=35) as response:
    return response.status,response.url,response.headers,response.read()
  except Exception:
   if attempt==3:raise
   time.sleep(2*(attempt+1))
def canonical(source):
 tags=re.findall(r'<link\b[^>]*>',source,re.I)
 for tag in tags:
  if re.search(r'rel=["\x27]canonical["\x27]',tag,re.I):return re.search(r'href=["\x27]([^"\x27]+)',tag,re.I).group(1)
def check(url):
 for attempt in range(4):
  status,final,headers,body=fetch(url);text=body.decode('utf-8-sig')
  valid=status==200 and final.rstrip('/')==url.rstrip('/') and canonical(text)==url and len(re.findall(r'<h1\b',text,re.I))==1 and not re.search(r'<meta[^>]+content=["\x27][^"\x27]*noindex',text,re.I)
  valid=valid and not re.search(r'\b(noindex|none)\b',headers.get('X-Robots-Tag',''),re.I) and '<!-- Quran Hub production release: indexing-repair-2026-10-25 -->' in text
  outline=Outline();outline.feed(text)
  count=len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",' '.join(outline.text)))
  path=urllib.parse.urlparse(url).path
  valid=valid and 1500<=count<=2000 and outline.headings==BASELINES[path]
  if valid:return {'url':url,'words':count}
  if attempt<3:time.sleep(3)
 raise AssertionError('Page response/canonical check failed: '+url)
expected={x.text for x in ET.parse(PUBLIC/'sitemap.xml').getroot().iter(NS+'loc')}
for attempt in range(4):
 status,final,headers,body=fetch(ORIGIN+'/sitemap.xml');actual={x.text for x in ET.fromstring(body).iter(NS+'loc')}
 if actual==expected:break
 time.sleep(3)
assert actual==expected,('Sitemap mismatch',len(actual),len(expected))
with ThreadPoolExecutor(max_workers=6) as pool:checked=list(pool.map(check,sorted(expected)))
robots=fetch(ORIGIN+'/robots.txt')[3]
assert b'Allow: /' in robots and (ORIGIN+'/sitemap-index.xml').encode() in robots
for label,agent in [('browser','Mozilla/5.0'),('googlebot-user-agent','Googlebot/2.1 (+http://www.google.com/bot.html)')]:
 req=urllib.request.Request(ORIGIN+'/sitemap-index.xml',headers={'User-Agent':agent})
 with urllib.request.urlopen(req,timeout=30) as response:
  assert response.status==200 and response.url==ORIGIN+'/sitemap-index.xml'
  assert 'xml' in response.headers.get('Content-Type','')
  index=ET.fromstring(response.read())
  assert index.tag==NS+'sitemapindex'
  assert [x.text for x in index.iter(NS+'loc')]==[ORIGIN+'/sitemap.xml']
print(json.dumps({'sitemap_index':'valid','index_entry':ORIGIN+'/sitemap-index.xml','browser_and_googlebot_user_agent':'HTTP 200','note':'This does not establish a request from actual Google crawler IPs.'}))
assert fetch(ORIGIN+'/google0857ee4d7c225a56.html')[3].strip()==b'google-site-verification: google0857ee4d7c225a56.html'
try:
 with urllib.request.urlopen(urllib.request.Request(ORIGIN+'/quran-hub-route-check-not-found/',headers={'User-Agent':'QuranHub-Deployment-Check/1.0'}),timeout=30) as response:
  raise AssertionError('Missing route returned HTTP '+str(response.status)+' instead of 404')
except urllib.error.HTTPError as error:
 assert error.code==404,error.code
for asset in ['/uk.css','/uk.js','/styles.css','/original-interactions.js','/interactions.js']:
 assert fetch(ORIGIN+asset)[0]==200,asset
print(json.dumps({'live_checked_pages':len(checked),'minimum_words':min(p['words'] for p in checked),'maximum_words':max(p['words'] for p in checked),'unchanged_h1_h2_pages':len(checked),'production_noindex_headers':0,'release_marker':'current','sitemap':'valid','verification_file':'present','assets':'available','note':'Public HTTP checks do not establish Google indexing or screenshot equivalence.'}))
