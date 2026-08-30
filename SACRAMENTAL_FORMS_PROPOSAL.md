# Sacramental Signup Forms — Replacement Proposal

**Status:** Proposal only — no live form, form handler, notification, deployment, or historical-submission access has been changed.

## Scope and source boundary

This proposal covers the requested First Holy Communion and Confirmation signup forms. The supplied legacy screenshots are a design reference only. They were reviewed locally and are not copied into this repository. No past submission was opened, copied, or retained.

The screenshots include First Holy Communion, plus unrelated Wedding, Baptism, and Census forms. They do not include a Confirmation form. Accordingly, the First Holy Communion inventory below is evidence-based; Confirmation must remain a short requirements decision before it is designed or built.

## Observed First Holy Communion intake

The legacy First Holy Communion screen visibly requests:

- Child’s first and last name (required)
- Date of Baptism
- Place of Baptism (city, state, country)
- A photo of the baptismal certificate
- Father’s first and last name (required)
- Mother’s first and last name at birth (required)
- Mailing address: country, address lines, city, state, and ZIP code (the first address line, city, state, and ZIP code are required)

The supplied view does not show a contact person, contact method, privacy notice, confirmation page, submission receipt, or parish notification recipient. Those parts of the workflow are therefore unknown, not implied by the legacy form.

## Minimal replacement

Create two separate public pages under a future `/sacraments/` section: one for First Holy Communion and one for Confirmation. Each page should explain that submitting the form begins a parish follow-up process and does not by itself schedule or guarantee reception of the sacrament.

For First Holy Communion, retain the observed child, baptism, parent-name, and mailing-address fields, but use the least data necessary to complete the parish’s actual preparation and records workflow. In particular, confirm whether a baptismal-certificate upload is genuinely required at initial inquiry. If it is, limit it to common image/PDF formats, publish a clear alternative for families who cannot upload it, and keep the file outside the website repository.

For Confirmation, do not infer fields from the unrelated forms. Before implementation, confirm the required information, whether the registrant is a minor, who may submit on the candidate’s behalf, and whether any certificate or other document is needed.

## Privacy, validation, and retention

- Use server-side form handling only after Ryan approves the provider, notification recipients, access path, and retention/deletion practice.
- Collect only fields needed for sacramental preparation and follow-up; avoid free-text questions unless a specific pastoral purpose requires them.
- Mark only confirmed necessary fields as required. Use appropriate client-side input types for email, telephone, and date, but treat server-side validation as authoritative.
- State in plain language who receives the submission, why the parish needs it, and how a family may contact the parish with questions or corrections.
- Do not put submission data, uploaded documents, recipient addresses, or provider credentials in Git, the public site, build output, or screenshots.
- Add a confirmation page or acknowledgment that says the parish received the request without echoing sensitive details.

## Proposed follow-up workflow

1. A parent, guardian, or adult candidate submits the approved form.
2. The approved private parish recipient receives a notification through the approved provider.
3. Parish staff or clergy review the request in the private system and contact the family using the approved contact method.
4. The parish separately confirms eligibility, preparation, documents, dates, and any needed pastoral conversation.
5. The submission is retained or deleted according to the parish’s approved records practice; it is not used as the canonical sacramental register.

## Decisions needed before implementation

1. Provide the Confirmation legacy form or a concise list of its required fields and intended workflow.
2. Confirm whether First Holy Communion must collect a baptismal-certificate upload at the initial step, and where that upload may be stored.
3. Approve the form provider and the specific private notification recipient(s), including who can access submissions.
4. Approve the data-retention/deletion practice and the public privacy wording.
5. Approve the final field sets and copy before any form is enabled.

After those decisions, the implementation can add the pages and a synthetic end-to-end submission test. Publishing, activating form handling, or sending a real notification remains a separate explicit approval.
