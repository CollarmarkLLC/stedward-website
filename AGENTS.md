# Collarmark Repository Agent Instructions

## Purpose and precedence

Work toward the repository's documented purpose while protecting its users,
content, deployment, and history. Read this file, the README, and any nearer
agent instructions before acting.

Current human instructions take precedence over this file. Repository-specific
documentation, checked-in configuration, and verified live state govern the
project. If those authorities disagree, identify the conflict instead of
silently choosing one.

## Authority and ownership

- The repository under the `CollarmarkLLC` GitHub organization is the canonical
  writable Git authority unless the README explicitly says otherwise.
- Do not create a second writable authority. A Forgejo copy, if one exists, is
  a backup or one-way mirror only.
- Ryan and Fr Chris use separate accounts, credentials, SSH keys, development
  environments, and agents. Never request, copy, or share a private key or
  personal login.
- Default new repositories to private. Publication is a deliberate human
  decision.
- Do not infer a license. Add or change licensing only with explicit human
  direction.

## Working model

- A person actively directing an agent may use the repository's ordinary Git
  workflow, including a direct push when the repository permits it.
- Use a branch and pull request when an agent independently proposes work, when
  either collaborator requests review or discussion, or when the change is
  broad, risky, difficult to reverse, or affects publication, security,
  production data, or deployment ownership.
- Do not require pull requests, project boards, teams, issue templates, labels,
  or mandatory reviews by default. Add process only when it solves an observed
  coordination problem.
- Keep changes narrowly scoped. Preserve unrelated working-tree changes and do
  not reformat or reorganize unrelated material.
- Make small, coherent commits with clear imperative messages. Update relevant
  documentation when behavior, operation, ownership, or a project milestone
  changes.

## Before changing anything

- Inspect the current branch, remotes, worktree status, repository instructions,
  and relevant implementation before editing.
- Confirm that the requested work belongs in this repository and that GitHub is
  still its canonical authority.
- Treat existing uncommitted and untracked material as someone else's work
  unless the current task clearly establishes otherwise.
- Ask before destructive, irreversible, externally visible, or materially
  scope-expanding actions. Never delete or overwrite work merely to obtain a
  clean checkout.

## Privacy and secrets

- Never commit passwords, tokens, private keys, recovery codes, authenticated
  URLs, `.env` files containing secrets, or production credentials.
- Keep parish records, pastoral communications, donor information, family
  documents, private sermons or notes, production form submissions, and other
  personal or ministry data outside the repository unless the repository has an
  explicit, reviewed design for that data.
- Code, schemas, fixtures, and documentation should use synthetic or properly
  anonymized examples by default.
- Store deployment secrets in the approved deployment provider or secret
  manager. Document the secret's name and purpose, never its value.
- Before an initial public push or a private-to-public change, inspect the full
  tracked history and current tree for secrets, private data, large source
  assets, and unclear licensing.

## Deployment and integrations

- Use least-privilege access for GitHub Apps, OAuth apps, CI, Netlify, and other
  integrations. Grant repository-specific access unless broader access is
  demonstrably necessary.
- Reconnect an existing production site rather than creating a replacement.
  Preserve its site identity, domains, TLS, deploy history, forms, and
  notifications.
- Ryan is the default deployment owner unless the repository documents another
  owner. This assigns operational responsibility; it does not grant exclusive
  project ownership.
- Do not change production domains, DNS, site identifiers, form handling,
  notification recipients, environment variables, or access controls without
  explicit authorization.
- Prefer checked-in build and deployment configuration over undocumented UI-only
  settings when the platform supports it.

## Implementation and verification

- Prefer the simplest implementation consistent with the repository's current
  architecture. Do not introduce shared infrastructure, a new framework, or a
  new service merely for uniformity across Collarmark projects.
- Reuse existing commands and conventions. Add dependencies only when their
  benefit exceeds their maintenance and security cost.
- Run the smallest relevant checks during development and the repository's
  documented build or test suite before handoff.
- For a deployed website, verify the actual public result as well as the local
  build. Check HTTPS, the canonical domain and redirects, important pages, and
  any forms or other critical user paths affected by the change.
- Never describe a Git push, successful CI run, or provider dashboard state as
  proof that the user-facing result works.

## Handoff and completion

A useful handoff states:

- the user-visible outcome;
- the files, commits, or pull request involved;
- the checks performed and their results;
- any deployment or live-site verification performed;
- remaining risks, decisions, or human-only steps.

A setup task is complete when the canonical repository and individual access
work, required builds and deployments have been verified, sensitive data and
secrets remain outside Git, and another collaborator or agent can understand
the next step from the repository itself.

## Evolving these defaults

These are defaults, not an attempt to predict every future collaboration need.
When a recurring point of friction appears, record the narrowest useful rule in
the affected repository. Promote it to the shared baseline only if it applies
across several projects. Remove rules that no longer protect a real boundary or
support a real workflow.
