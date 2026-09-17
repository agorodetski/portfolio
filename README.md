# Avi Gorodetski — Portfolio

A responsive, multi-page personal and professional portfolio for Avi Gorodetski. The site features work with GiVV, BBYO, TUCP, and other organizations, plus an experience page, a personal introduction, and direct contact links.

## Pages

- `index.html` — introduction and featured work
- `work/index.html` — selected work
- `work/givv/index.html` and `work/bbyo/index.html` — project stories
- `about/index.html` — background and interests
- `experience/index.html` — roles, education, and résumé
- `contact/index.html` — email, LinkedIn, and résumé

The supplied headshot, event photography, and résumé are in `assets/`. The copy and page markup live in `build_site.py`, while `styles.css` and `script.js` provide the shared presentation and mobile navigation. The script writes HTML to the repository root and mirrors the complete static site into `dist/` for Sites hosting. All links and assets use relative URLs, so the site works on a subpath as well as a domain root.

## Editing and preview

Run `python3 build_site.py` after changing page content, CSS, or JavaScript. Preview locally with `python3 -m http.server 8000` and open `http://localhost:8000/`. No package installation is required.

The site uses semantic landmarks, visible keyboard focus, a skip link, reduced-motion support, and a navigation menu that works as ordinary links when JavaScript is unavailable.

## Publishing

The current hosted Site uses `.openai/hosting.json` and the static `dist/` directory. The repository-root pages can also be served with GitHub Pages.

The Site's audience remains owner-only until its access settings are changed. The contact email is Avi's Tulane address from her résumé. The Spotify handle appears as text because a direct profile URL has not yet been verified.
