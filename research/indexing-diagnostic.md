# Quran Hub indexing access — 25 October 2026

Independent GitHub runner diagnostic: https://github.com/hafiz-adeel-eng/learn-quran-pages-website/actions/runs/40153312487

At 02:08 UTC, production robots.txt, sitemap.xml, homepage, London page and Noorani Qaida page returned HTTP 200 with no redirect or CF-Mitigated header for browser, Googlebot and Google-InspectionTool user-agent strings. XML was served as application/xml and parsed successfully: 112 unique URLs, all on the production host. Robots allowed each checked path. HTML pages used index/follow and their own production canonical, with no X-Robots-Tag noindex. DNS A/AAAA records existed and standard certificate validation succeeded.

Cloudflare Pages API confirmed project learnquran, production branch main, environment production, subdomain learnquran-86k.pages.dev and successful production deployment. The versioned deployment host 796f2403.learnquran-86k.pages.dev carried X-Robots-Tag: noindex; the production host did not. This distinction does not prove the user submitted a preview URL.

The current token returned HTTP 403 for account Access application inspection. Private Access rules, WAF/bot events and actual Google crawler requests were not fully inspected. Spoofed user-agent tests run from GitHub, not from verified Google crawler IP addresses. The private Search Console error and its last-fetch record were not accessible. No robots/HTTP/XML indexing blocker was found in the completed checks; the precise cause of the reported GSC failure remains unconfirmed.

A separate sitemap-index.xml entry point now refers to the existing valid sitemap.xml. Robots discovery points to that index. Explicit XML/plain-text MIME and revalidation headers are configured. This provides a new valid submission URL; it is not evidence that a Google-side error has been cured or that the old sitemap was malformed. Original sitemap.xml remains available. No page headings or Cloudflare security rules were changed.

Search Console property: https://learnquran-86k.pages.dev/
New entry: https://learnquran-86k.pages.dev/sitemap-index.xml
Child URL set: https://learnquran-86k.pages.dev/sitemap.xml

Do not claim Google verification, sitemap acceptance or indexing success until Search Console reports it. Inspect an actual dated Google fetch and any corresponding Cloudflare security event if the new entry also fails. Avoid disabling protections or moving domains without evidence of a relevant block.
