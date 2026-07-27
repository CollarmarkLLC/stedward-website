# St. Edward the Confessor Catholic Church

Weekly bulletin website for St. Edward the Confessor Parish in Tallulah, Louisiana.

## Project Structure

- `src/posts/` — Weekly bulletins (one `.md` file per week)
- `src/images/` — Photos and bulletin social images
- Homepage (`index.njk`) automatically lists all bulletins in reverse chronological order

## Adding a New Bulletin (Very Simple)

1. Create a new Markdown file in `src/posts/` with the naming convention:
   `YYYY-MM-DD-bulletin.md`

2. Use this frontmatter at the top:

```yaml
---
title: "August 3, 2026 – Eighteenth Sunday in Ordinary Time"
date: 2026-08-03
image: /images/bulletins/2026-08-03.jpg
summary: "Brief one-sentence description for the homepage."
---
```

3. Add the rest of the bulletin content below the frontmatter.

4. Place the social-share image in `src/images/bulletins/`.

5. Commit and push — Netlify will automatically rebuild the site.

## Local Development

```bash
npm install
npm run serve
```

## Deployment

- Push to the connected GitHub repository.
- Netlify will automatically deploy.
- Use the same Hover DNS setup as the Children of Mary site (A record `75.2.60.5`).

## Notes

- The blog is the homepage.
- All posts are sorted newest first.
- Netlify Forms are ready on the Contact page.