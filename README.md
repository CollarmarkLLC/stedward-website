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
- Homepage (`index.njk`) automatically lists all bulletins in reverse chronological order

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
