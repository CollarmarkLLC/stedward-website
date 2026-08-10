# St. Edward the Confessor Catholic Church

Weekly bulletin website for St. Edward the Confessor Parish in Tallulah, Louisiana.

## Repository Authority

This is a collaborative project. Its dedicated GitHub repository is the
writable source of truth for code, issues, pull requests, and deployment.
Agents must work GitHub-first. Forgejo may hold a one-way mirror for local
resilience and discovery, but it must not become a second writable authority.

## Project Structure

- `src/posts/` — Weekly bulletins (one `.md` file per week)
- `src/images/` — Photos and bulletin social images
- Homepage (`index.njk`) presents the six newest bulletins, a disabled
  subscription-form stub, and the parish Mass, Confession, and catechesis times
- `past-bulletins.njk` provides the remaining archive in pages of 24 bulletins

## Adding a New Bulletin (Very Simple)

1. Create a new Markdown file in `src/posts/` with the naming convention:
   `YYYY-MM-DD.md`, where the date is the Sunday covered by the bulletin.

2. Use this frontmatter at the top:

```yaml
---
date: 2026-07-26
title: "Seventeenth Sunday in Ordinary Time"
image: /images/bulletins/green.jpg
---
```

The historical bulletin collection uses exactly these three frontmatter fields.
Titles and liturgical colors come from the generated Sunday projection in
`data/bulletin-sundays-2019-2026.json`; do not infer them from prose in an old
bulletin. The image filename is the lowercase liturgical color.

The current source archive for historical reconciliation is
`/Users/ryan/My Drive (frhumphries@gmail.com)/St Edward/Bulletin`. Copy source
files into this repository; never move or modify the source archive. As of
2026-08-09, the website contains one post for every Sunday from 2019-01-06
through 2026-08-09. Future dated source templates are intentionally excluded
until their bulletin date arrives.

3. Add the rest of the bulletin content below the frontmatter.

4. Ensure the corresponding color image exists in `src/images/bulletins/`.

5. Commit and push — Netlify will automatically rebuild the site.

## Local Development

```bash
pnpm install
pnpm run serve
```

## Deployment

- Push to the connected GitHub repository.
- Netlify will automatically deploy.
- Use the same Hover DNS setup as the Children of Mary site (A record `75.2.60.5`).

## Notes

- The blog is the homepage.
- All posts are sorted newest first.
- Netlify Forms are ready on the Contact page.
