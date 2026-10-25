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

## Follow-up after Access read permission was granted

On 25 October 2026 at approximately 13:38–13:41 Pakistan time, the authenticated Access API succeeded: one application, scoped to `*.learnquran-86k.pages.dev`, with a members-only email allow policy. No Access application matched the bare production hostname.

Fresh diagnostics found a real production indexing blocker on the London and Noorani Qaida URLs: HTTP X-Robots-Tag noindex, CF-Cache-Status HIT, and Cache-Control public, s-maxage=604800. Their HTML still said index/follow. A cache-busting query returned the homepage HTML at those same routes instead of their own pages. This is distinct from the earlier successful public checks and does not prove the precise cause of Google's historical sitemap fetch error.

Cloudflare's authenticated project settings showed a GitHub source with native production deployments enabled, an empty build command and an empty output directory. Recent deployments showed native github:push jobs for the diagnostic commits replacing the earlier ad_hoc deployments made by GitHub Actions. The generator is necessary to create nested routes; publishing source files without running it produces an incomplete deployment with homepage fallback.

Repair: production publishing is consolidated in GitHub Actions. The workflow sets the native production deployment switch to false and configures the correct generator/audit command and public output for any native preview builds. Already-started native production builds must finish before publishing. Static HTML is regenerated with a release marker, production-host headers remove X-Robots-Tag and prevent stale HTML edge caching, and a real 404 document prevents missing routes from silently becoming the homepage. Existing H1/H2 and visible word counts are preserved. The post-deploy check requires all 112 routes to have the current marker, their own canonical and headings, 1500–2000 words and no noindex HTTP header.

Search Console acceptance remains a separate verification requiring Google's actual fetch result. Do not claim the historical GSC report has cleared solely because hosting checks pass.
