# Product Requirements Document

## 1. Product Objective

Build a simple, trustworthy, accessible, AI-assisted Request to Resolution service that takes an issue from its first report through triage, investigation, corrective action, response and closure, while giving managers visibility of service performance.

Initial setting: Health and Safety. The platform should use reusable components and configurable categories, teams and routing policies so that it can be adapted to other operational settings.

## 2. Core Workflow

Incident Report follows a six-stage Request-to-Resolution workflow:

1. Report
2. Triage and route
3. Attend and investigate
4. Record outcome
5. Respond
6. Review and improve

## 3. Personas and Roles

### Reporter
A resident, customer, employee, visitor or member of the public. Needs an accessible way to submit an issue, receive confirmation and understand the outcome.

Reporters must be able to:
- Submit a report without creating an account.
- Optionally create an account or sign in before reporting.
- Access the reporting form directly through the website.
- Access the same reporting form by scanning a QR code.
- Submit an identified or anonymous report.
- Receive a unique case reference and securely follow up on their report.

### Case handler / Triage officer
Needs to review reports, clarify information, confirm category and priority, identify possible duplicates and route cases to the appropriate team.

### Field officer
Needs to see assigned cases, attend the location, record findings, evidence and immediate controls, and update corrective actions.

### Team manager
Needs visibility of workload, overdue cases, SLA performance, outstanding actions and trends.

These are the four primary application roles. Administrator access may be added for technical configuration if required, but it is not a primary operational role.

## 4. Functional Requirements — Six Workflow Stages

### Stage 1: Report

- Provide a responsive public reporting interface.
- Allow reporting with or without creating an account.
- Allow access through the public website or by scanning a QR code.
- QR codes may contain a location identifier to pre-populate the reporting location.
- Allow reporters to review and correct pre-populated location information.
- Support identified and anonymous reports.
- Do not require a staff account to submit a report.
- Capture a title, description, category or issue type, perceived urgency, incident date/time and location.
- Support optional evidence uploads.
- Support optional voice-assisted reporting, with a text alternative.
- Generate a unique case reference.
- Provide secure follow-up for guest reporters; a case reference alone must not grant access to private case information.
- Acknowledge receipt and explain how the reporter can follow up.
- Provide a clear emergency instruction: users must not wait for this application in an emergency and must follow the relevant emergency procedures.

### Stage 2: Triage and route

- Present new reports to authorised case handlers.
- Suggest a category and relevant missing information.
- Ask relevant follow-up questions where useful; allow the reporter to skip or answer that they do not know.
- Recommend priority using explicit, explainable rules and available information.
- Identify possible duplicate reports without automatically merging them.
- Recommend a responsible team.
- Require an authorised human to confirm or change consequential triage decisions.
- Record recommendations, decisions and overrides.

### Stage 3: Attend and investigate

- Show field officers the cases assigned to them.
- Provide an appropriate mobile-friendly case view.
- Record attendance, findings, notes and immediate controls.
- Allow supporting evidence to be attached to the case or investigation.
- Restrict access to sensitive location and reporter information by role.

### Stage 4: Record outcome

- Record investigation outcomes and resolution notes.
- Create and track corrective actions, owners and due dates.
- Record completion evidence.
- Track risk control separately from resolution, verification and closure.
- Require authorised verification and closure.
- Support reopening with a recorded reason and audit history.

### Stage 5: Respond

- Record acknowledgement and outcome communications.
- Draft clear, accessible outcome messages.
- Support language selection and translation.
- Disclose when AI has drafted or translated content.
- Require human approval before consequential communication is sent.
- Record approval, language, communication status and sent time.

### Stage 6: Review and improve

- Provide a team manager dashboard.
- Display open, overdue, resolved and closed cases.
- Show team workload and outstanding corrective actions.
- Track acknowledgement, time to risk controlled and time to resolution where the required timestamps exist.
- Show trends by category, location and reporting period.
- Interpret changes carefully: increased reporting may indicate improved reporting rather than worsening underlying conditions.

## 5. AI Requirements and Safety Boundaries

AI may assist with:
- Speech-to-text and suggested form-field extraction.
- Relevant follow-up question suggestions.
- Category and team recommendations.
- Priority recommendations with reasons.
- Possible duplicate identification.
- Investigation summaries.
- Outcome letter drafting and translation.

Controls:
- Reporters review and approve extracted information before submission.
- AI must not invent missing information.
- AI recommendations do not replace professional decisions.
- AI must not automatically downgrade serious reports, close cases, merge cases or dispatch outcome letters.
- Emergency escalation uses deterministic rules and operational procedures, not an AI model.
- Record AI task type, provider/model version where available, suggestion and human decision.
- Consider bias, accessibility, privacy and language differences during testing.

## 6. Non-Functional Requirements

- Responsive and accessible interface.
- Readable language, keyboard access, appropriate contrast and clear validation messages.
- Backend validation and role-based authorisation.
- Secure handling, validation and malware scanning of uploaded files.
- Audit history for important actions and decisions.
- UTC timestamps.
- Data minimisation and approved retention rules.
- Modular, testable and maintainable architecture.
- Use fictional or approved anonymised data in development, testing and demonstration environments. Do not use real personal or confidential information without appropriate authorisation.

## 7. MVP Scope and Delivery Approach

Deliver the complete core case workflow before adding advanced AI capabilities. Implement in verified milestones, with tests and documentation at each stage.

Initial technical slice:
- Submit a fictional report through the API.
- Persist it in the database.
- Generate a unique case reference.
- Retrieve the case using an authorised mechanism.
- Reject invalid submissions with understandable errors.

Subsequent milestones add triage, assignments, investigation, corrective actions, communications, dashboards, AI assistance, security and accessibility evidence.

## 8. Acceptance Criteria

The solution should demonstrate that:
- A reporter can submit an identified or anonymous fictional issue.
- The system returns a unique case reference and acknowledgement.
- A case handler can review, confirm triage information and assign a case.
- A field officer can record attendance, findings, evidence and controls.
- Corrective actions can be tracked and verified.
- An authorised person can close or reopen a case with an audit trail.
- A reporter can receive an approved outcome communication.
- A manager can review workload, delays and trends.
- Invalid input is rejected with understandable validation feedback.
- Use fictional or approved anonymised data in development, testing and demonstration environments.
- Do not use real personal or confidential information without appropriate authorisation.
