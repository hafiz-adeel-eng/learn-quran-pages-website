# UK expansion

`content/uk_locations.tsv` contains 83 original location briefs, individual questions, answers and practical next steps. `content/uk_content.py` supplies the six course descriptions, four audience pathways, 15 learning-focus groups and six guides.

Run `python tools/build_uk.py` then `python tools/audit_uk.py`. The build writes the actual static HTML into `public/`, updates the homepage navigation and sitemap, and validates all internal routes. GitHub Actions performs the same build before Cloudflare Pages publishing; generated nested HTML is a deployment artifact, while its editable source is versioned here.

The complete site has 112 canonical pages: homepage, 83 city/town pages, UK hub, four nation hubs, four audience pages, course index, six course pages, blog index, six guides, and five support pages. These are 112 real routes, not a claim that 250 pages have been authored.

See `uk-keywords-and-sources.md` for intent clusters, sampled competitors, questions and research limitations. `uk-build-validation.json` and `uk-content-audit.json` record local checks. Post-deploy `tools/check_live_uk.py` checks every published route against the generated sitemap.
