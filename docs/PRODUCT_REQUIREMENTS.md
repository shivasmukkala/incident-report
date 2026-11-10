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
