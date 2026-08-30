# Parish Intake Forms — Replacement Proposal

**Status:** Proposal only — no live form, form handler, notification, deployment, or historical-submission access has been changed.

## Scope and source boundary

St. Edward needs a public inquiry form for every parish register: Baptism, Confirmation, First Holy Communion, Marriage, and Funerals/Death. It also needs a parish Census form and a Mausoleum Application stub. The private Registers manifest is the authority for each register’s required record fields. The supplied legacy screenshots are a local design reference only; they are not copied into this repository, and no historical submission was opened, copied, or retained.

Each public form gathers the parishioner- or family-provided facts needed to begin the process and prepare the private record. The parish office completes the register number, officiant, final sacramental or funeral date and place, official remarks, and other facts that arise during pastoral preparation. A public submission is never itself the canonical register entry.

## Shared design and workflow

Create one `/forms/` index and six accessible form pages: `/forms/baptism/`, `/forms/confirmation/`, `/forms/first-holy-communion/`, `/forms/marriage/`, `/forms/funeral/`, and `/forms/parish-census/`. Add `/forms/mausoleum-application/` as a non-collecting stub. Each active form page should say that submitting begins parish follow-up and does not schedule, approve, or complete the associated rite or register entry.

All forms use a named primary contact, email, phone, and clear consent for parish follow-up. For a minor, collect the parent or guardian’s contact details and only collect the minor’s own contact information where the parish confirms it is necessary. Validate required inputs on the server, use suitable email/phone/date controls in the browser, and provide a private alternative for families who cannot use an online form.

The approved private recipient receives the submission. Parish staff or clergy then review it, contact the family, complete preparation, and enter verified facts in the private register. The public acknowledgment should confirm receipt without repeating any sensitive content.

## Register-specific intake fields

### Baptism

- Child’s baptismal and family name; place and date of birth; proposed baptism date if known
- Father’s name and mother’s maiden name
- Sponsor or sponsors
- Primary contact name, phone, and email; certificate recipient name and mailing address
- Optional, purpose-limited notes for circumstances the office needs before follow-up

The parish completes the register number, final baptism date, minister, later Confirmation/marriage annotations, and official remarks.

### Confirmation

- Candidate’s baptismal and family name; confirmation name; date and place of baptism; residence; date of birth or age
- Parents’ names and sponsor
- Candidate contact details only when approved as necessary; parent or guardian contact details for a minor
- Certificate recipient name and mailing address

The parish completes the register number, final Confirmation date, minister, and official remarks.

### First Holy Communion

- Candidate’s baptismal and family name; place and date of birth; age calculated from date of birth where needed; date and place of baptism; residence
- Parents’ names
- Primary contact name, phone, and email; certificate recipient name and mailing address
- Optional, purpose-limited remarks

The parish completes the official register entry and any later pastoral notes. The visible legacy request for a baptismal-certificate photo should be included only if Ryan approves both its necessity at initial inquiry and its private storage location.

### Marriage

- Each contracting party’s name, residence, place and date of baptism, and parent information
- Proposed marriage date and place, witnesses if known, and marriage-license number when available
- Both parties’ contact name, phone, and email
- Purpose-limited fields for banns, dispensations, or special circumstances only when the parish confirms they belong in online intake

The parish completes the register number, verified marriage date/place, minister, final witnesses, dispensations, and official remarks. The form must clearly state that a requested date is not reserved until the parish confirms it.

### Funerals / Death

- Deceased’s name, residence, age or date of birth, date of death, known sacraments, next of kin/spouse/parent information, and desired contact person
- Proposed funeral and burial details if known, including date/place and clergy preference where appropriate
- Contact name, phone, and email; optional, purpose-limited pastoral remarks

The parish completes the register number, verified sacramental and death details, officiant, final burial details, and official remarks. The page should include a prominent route for urgent pastoral contact that does not depend on an online form.

## Parish Census

The legacy Census screen is the visible-field reference for this separate household-information form. It requests family surname; home-parish choice and, when applicable, the other parish; residential and different mailing addresses; one or two heads of household; preferred names, birthdays, mobile phone numbers, emails, and contact preferences; children or dependents living at home or away; and optional comments about pastoral needs or interest in parish service.

The replacement should use structured fields for household members and addresses rather than unbounded lists where practical, make the second household head optional, and allow a household to choose no contact preferences. It should state the pastoral purpose and contact/retention policy plainly. Do not treat the Census as a sacramental register or use it to overwrite a private parish record without office review.

## Mausoleum Application stub

Add a clearly labeled `/forms/mausoleum-application/` page and link it from the forms index. Until Ryan approves a specific application, pricing, payment, contract, recipient, and retention workflow, the page collects no data. It explains that applications are not yet available online and directs interested people to the approved parish office contact path. It must not imply availability, reservation, pricing, or a binding application.

## Privacy, documents, and retention

- Use server-side handling only after Ryan approves the provider, specific notification recipient(s), access path, and retention/deletion practice.
- Keep submission data, documents, recipient addresses, and provider credentials out of Git, public pages, build output, and screenshots.
- Do not request uploads unless a specific register workflow needs one. When approved, restrict type/size, state why it is needed, provide an offline alternative, and store it only in the approved private system.
- State in plain language who receives a submission, why it is needed, how long it is retained, and how a family can correct it.

## Decisions needed before implementation

1. Approve the six-form scope plus the non-collecting Mausoleum Application stub, and the public-intake/private-register split for each register.
2. Confirm which optional or sensitive fields are necessary at initial inquiry, including whether either sacramental form needs document upload.
3. Confirm minor-submitter and candidate-contact rules, plus the intended Census contact/retention practice.
4. Approve the form provider, exact private notification recipient(s), access model, and retention/deletion practice.
5. Approve the Mausoleum office-contact path and final page copy, then approve the synthetic test plan before any active form handling is enabled.

After those decisions, implementation can add the pages and use synthetic data for end-to-end testing. Publishing, activating form handling, or sending any notification remains a separate explicit approval.
