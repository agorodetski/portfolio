# Avi Gorodetski — Portfolio

A personal and professional portfolio featuring Avi’s work in social-impact entrepreneurship, community leadership, campus programming, and client service.

## Structure

- `index.html`: biography, selected project stories, experience, and contact link
- `styles.css`: responsive editorial design, print styles, focus states, and reduced-motion support
- `script.js`: progressively enhanced mobile navigation and current copyright year
- `favicon.svg`: custom site icon

## Design and accessibility

The site uses semantic HTML, native expandable project details, a skip link, visible keyboard focus, and a mobile menu with accurate expanded state and Escape handling. Navigation and project content remain available without JavaScript. There are no runtime dependencies, external font requests, trackers, or third-party embeds.

All local assets use relative paths, so the site works from a domain root or a GitHub Pages repository subdirectory.

## Preview

Run `python3 -m http.server 8000` in this directory, then open `http://localhost:8000`. There is no build step or package installation.

## Editing content

Update the sections directly in `index.html`. Each project uses a native `details` element for its longer story. Keep the short project introduction readable without expanding the details. Define site-wide colors and spacing in the CSS `:root` variables.

The contact destination currently points to Avi’s verified GitHub profile. Replace it with a preferred professional email or LinkedIn URL once provided. No email, profile URL, résumé download, headshot, or testimonial has been invented.

## Publishing

This repository is ready for static hosting. For GitHub Pages, enable Pages in repository settings and select **Deploy from a branch → main → / (root)** after merging the website changes. Repository code being updated does not itself confirm Pages is enabled.

Before publishing, review biography, role dates, and project metrics for accuracy. Refresh time-sensitive information when roles change or after graduation.
