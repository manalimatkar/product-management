---
platformSlug: pdf-workflow
appSlug: workflow-manager
version: 4
priorVersion: null
sourceTool: Claude Design
uploadedBy:
  name: Manali
  role: Producing Designer
uploadedAt: 2026-09-08
status: Received
readiness: Ready with Limitations
knownLimitations:
- '**No persistent context while editing.** Once a field row is expanded for edit,
  especially on a long page, there''s no breadcrumb reminding the user which field/section
  they''re editing if they scroll.'
- '**Compound type tags (`Field-List-3x`, `Custom-App-signature-pad`) need onboarding.**
  They''re compact but non-obvious on first encounter — consider a tooltip or one-time
  legend, especially for FieldGroup/Custom.'
- '**Low-confidence rows don''t visually escalate.** A <50%-confidence row (the ones
  most needing human review) has the same visual weight as a 96% row apart from a
  muted color — consider a stronger cue or default-sorting low-confidence to the top.'
- '**Table/Card view markup duplication.** In the HTML reference the two views'' edit
  panels are hand-duplicated (same fields, two places) — in the real implementation,
  extract this once (e.g. a shared row/card-edit component) so future edits to the
  edit panel don''t need to land twice.'
screens:
- Forgot Password (Light).dc.html
- Forgot Password.dc.html
- Login (Light).dc.html
- Login.dc.html
- Mapping Report (Light).dc.html
- Mapping Report.dc.html
- Signup (Light).dc.html
- Signup.dc.html
- Verify Email (Light).dc.html
- Verify Email.dc.html
- Workflow Dashboard (Light).dc.html
- Workflow Dashboard.dc.html
- Workflow Page Editor (Light).dc.html
- Workflow Page Editor.dc.html
- Workflow Settings Dialog (Light).dc.html
- Workflow Settings Dialog.dc.html
---
