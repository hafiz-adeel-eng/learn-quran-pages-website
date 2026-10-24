"""Read-only post-deploy checks against this build's canonical URLs."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
import json, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
ORIGIN='https://learnquran-86k.pages.dev';PUBLIC=Path(__file__).resolve().parents[1]/'public'
NS='{http://www.sitemaps.org/schemas/sitemap/0.9}'
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
  if valid:return url
  if attempt<3:time.sleep(3)
 raise AssertionError('Page response/canonical check failed: '+url)
expected={x.text for x in ET.parse(PUBLIC/'sitemap.xml').getroot().iter(NS+'loc')}
for attempt in range(4):
 status,final,headers,body=fetch(ORIGIN+'/sitemap.xml');actual={x.text for x in ET.fromstring(body).iter(NS+'loc')}
 if actual==expected:break
 time.sleep(3)
assert actual==expected,('Sitemap mismatch',len(actual),len(expected))
with ThreadPoolExecutor(max_workers=6) as pool:checked=list(pool.map(check,sorted(expected)))
assert b'Allow: /' in fetch(ORIGIN+'/robots.txt')[3]
assert fetch(ORIGIN+'/google0857ee4d7c225a56.html')[3].strip()==b'google-site-verification: google0857ee4d7c225a56.html'
for asset in ['/uk.css','/uk.js','/styles.css','/original-interactions.js','/interactions.js']:
 assert fetch(ORIGIN+asset)[0]==200,asset
print(json.dumps({'live_checked_pages':len(checked),'sitemap':'valid','verification_file':'present','assets':'available','note':'Public HTTP checks do not establish Google indexing or screenshot equivalence.'}))
