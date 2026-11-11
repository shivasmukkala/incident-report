# Product Requirements Document

## 1. Objective

Create a simple, trustworthy, AI-assisted service that takes an issue
from first report to resolved case and provides management visibility.

## 2. Initial Setting

Health and Safety.

## 3. Personas

### Reporter
Needs accessible reporting, confirmation and a clear outcome.

### Triage Officer
Needs accurate reports, useful routing suggestions and less manual work.

### Field Officer
Needs an assigned case list, investigation tools and evidence capture.

### Team Manager
Needs workload visibility, delays, trends and performance measures.

## 4. Functional Requirements

### FR-01: Reporting
- Submit reports without requiring an account.
- Support anonymous reporting.
- Capture category, severity, description and location.
- Support optional attachments.
- Generate a unique case reference.

### FR-02: Triage
- Suggest incident categories.
- Recommend priority using explicit safety rules.
- Identify possible duplicate reports.
- Recommend a responsible team.
- Require human confirmation.

### FR-03: Investigation
- Display assigned cases.
- Record attendance and findings.
- Record immediate risk controls.
- Upload supporting evidence.

### FR-04: Resolution
- Record actions and resolution notes.
- Capture completion evidence.
- Require authorised closure.

### FR-05: Communication
- Draft outcome letters.
- Support language selection and translation.
- Require human approval.
- Record communication status.

### FR-06: Management
- Display active and closed cases.
- Track time to risk controlled.
- Monitor overdue cases.
- Show team workload and trends.

## 5. Non-Functional Requirements

- Responsive design.
- Accessible forms.
- Clear error messages.
- API validation.
- Secure file handling.
- Traceable case updates.
- Maintainable modular architecture.

## 6. MVP Scope

First deliver:
- Employee reporting interface.
- FastAPI submission endpoint.
- Persistent case storage.
- Case reference generation.

Subsequent functionality must be added through verified milestones.

## 7. Acceptance Criteria

A reporter can submit a valid fictional incident,
receive a unique reference and retrieve the stored case.

The system must reject invalid submissions and provide
understandable validation errors.

## AI-First MVP Scope

### 1. Incident reporting
- Support employees, residents, visitors and members of the public.
- Allow anonymous and identified reports.
- Capture incident category, description, perceived urgency, incident date/time and location.
- Support optional evidence uploads.
- Generate a unique case reference.

### 2. Voice-assisted reporting
- Allow reporters to provide a spoken description.
- Convert speech into a transcript and suggested form fields.
- Preserve the original transcript.
- Never invent missing information.
- Allow the reporter to review, correct and approve all extracted information before submission.
- Explain how voice data is processed and retained.

### 3. AI-assisted follow-up questions
- Identify important missing or unclear information.
- Ask relevant questions, normally one at a time.
- Allow the reporter to skip questions or answer "I don't know".
- Never delay urgent reporting because of follow-up questions.

### 4. AI-assisted triage
- Suggest incident category and relevant information.
- Identify possible duplicate reports.
- Recommend priority and responsible team.
- Require a case handler to confirm or change recommendations.
- Record human decisions and overrides.

### 5. Operational case management
- Assign cases to field officers.
- Record investigation findings, evidence and corrective actions.
- Track risk control separately from investigation and case closure.
- Require authorised verification and closure.

### 6. Manager dashboard
- Display open, overdue and closed cases.
- Show outstanding corrective actions.
- Provide basic category, location and monthly reporting.

### 7. AI safety boundaries
- AI recommendations must never replace professional safety decisions.
- Emergency escalation must use deterministic rules and operational procedures.
- AI must not automatically downgrade serious reports, close cases or dispatch outcome letters.
- Human approval is required for consequential decisions.
- Record AI suggestions, model version and human decisions.

### MVP acceptance criteria
- A reporter can submit an identified or anonymous incident.
- Voice input can populate suggested fields for human review.
- Follow-up questions can clarify missing information.
- A case handler can confirm priority and assign an officer.
- An officer can record findings and risk controls.
- A manager can verify actions and close a case.
- Important decisions and status changes are auditable.
