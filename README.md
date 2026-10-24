# QuranlyHub

QuranlyHub website with a medium teal palette (#16847A), six courses, separate cacheable CSS, responsive navigation, pricing, FAQ accordion and the original imagery. The Alim & Aalimah course has been removed.

## Automatic deployment with Cloudflare Pages

1. In Cloudflare, open Workers & Pages and create a Pages project connected to GitHub.
2. Select `hafiz-adeel-eng/learn-quran-pages-website`.
3. Project name: `learnquran` (subject to availability).
4. Production branch: `main`.
5. Framework preset: `None`.
6. Build command: `exit 0`.
7. Build output directory: `public`.
8. Save and Deploy.

The expected address is `https://learnquran.pages.dev` if Cloudflare accepts that project name. Deployment and name availability must be confirmed in Cloudflare. After the Git integration is connected, changes pushed to `main` deploy automatically. No GitHub Actions secrets are required.

## Editing

- `public/index.html`: page content.
- `public/styles.css`: visual styles.
- `public/original-interactions.js`: original menu and reveal behavior.
- `public/interactions.js`: standalone FAQ, keyboard and anchor support.

Open `public/index.html` in a browser to preview. Original public images and fonts require internet access. Other page, login, contact and WhatsApp links retain their original QuranlyHub destinations. No changes were made to quranlyhub.com.

JavaScript syntax and content checks passed. Screenshot comparison at desktop, tablet and mobile sizes remains unverified because browser tooling was unavailable.
