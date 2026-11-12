# System Architecture

## 1. Architecture Decision
Incident Report uses a full-stack Python architecture.

- Frontend: React and Vite
- Backend: Python and FastAPI
- ORM: SQLAlchemy
- Development database: SQLite
- Target production database: PostgreSQL

The application follows a modular architecture that separates presentation, API endpoints, business logic, AI integrations and data persistence.

The design prioritises maintainability, security, testability and the ability to evolve individual components without rewriting the entire application.

Technical decisions and their rationale are documented in DECISIONS.md.

## 2. High-Level Components

### Frontend — React and Vite
A single responsive application with role-oriented views:
- Reporter experience
- Case handler / triage workspace
- Field officer workspace
- Team manager dashboard

The frontend controls navigation and presentation by role. Frontend visibility is not a security boundary.

### Backend — Python and FastAPI
FastAPI exposes validated REST endpoints and owns:
- Authentication integration and backend authorisation
- Case creation and retrieval
- Workflow rules and permitted state transitions
- Triage, routing and assignment operations
- Investigation and corrective-action operations
- Communication approval and orchestration
- AI service integration
- Notifications and audit history

All protected operations must enforce permissions in the backend.

### Business Services
Keep business rules separate from route handlers and database models. Services should own workflow transitions, routing, SLA calculations, assignment rules and audit recording.

### AI Services
AI capabilities are accessed through backend service interfaces. Provider-specific code must not be embedded in API route handlers or core case workflow logic.

Potential capabilities:
- Speech-to-text and field extraction
- Contextual follow-up question suggestions
- Category and team recommendations
- Priority recommendations
- Duplicate similarity suggestions
- Investigation summaries
- Outcome letter drafting and translation

AI is advisory. Deterministic application rules handle safety-critical escalation and workflow enforcement. Human review is required for consequential decisions.

### Data Layer
- SQLAlchemy provides database access.
- SQLite is used for initial development and testing.
- PostgreSQL is the intended production migration option.
- Database access is isolated from API and business logic.
- Schema changes are managed through Alembic migrations.
- Store timestamps in UTC.
- Uploaded files are stored outside relational database records; database rows retain metadata and storage references.

## 3. Role-Based Access

The application has one entry point and shared case records, with role-specific pages and permitted actions.

Application roles:
- Reporter
- Case handler / triage officer
- Field officer
- Team manager

A reporter may submit without a staff account. Anonymous tracking must use a secure access token; a case reference alone must not grant access. Staff-only actions require authenticated users and backend permission checks. Exact location and personal information must only be returned to authorised roles.

## 4. Core Request-to-Resolution Workflow

The workflow follows six stages:

1. Report — create a case and acknowledge receipt.
2. Triage and route — review, categorise, confirm priority and assign a team/officer.
3. Attend and investigate — record attendance, findings and evidence.
4. Record outcome — track controls, corrective actions, resolution and verification.
5. Respond — prepare, approve and record reporter communications.
6. Review and improve — provide operational dashboards and trends.

Case lifecycle states and permitted transitions are defined centrally in backend workflow logic. Status changes, assignments, approvals and other important actions create audit events. Status changes and their audit records should be committed atomically.

Attendance, risk controlled, resolved, verified and closed are distinct milestones. Reopening requires an authorised action and a recorded reason.

## 5. Data Domains

The target data model includes:
- Cases, categories and teams
- Staff users and assignments
- Reporter details and anonymous access credentials
- Intake sessions, voice records and follow-up questions
- Investigations, corrective actions and evidence
- AI assessments and human review decisions
- Outcome communications
- SLA rules and audit events

See `DATA_MODEL.md` for fields and relationships.

## 6. Security, Privacy and Accessibility

- Enforce role-based permissions in FastAPI, not only in React.
- Validate all request data at the API boundary.
- Store only a hash of anonymous access tokens.
- Validate file type and size; quarantine and scan uploads before access.
- Restrict sensitive reporter and location data.
- Keep secrets out of source control and shared screenshots.
- Use fictional or approved anonymised demonstration data.
- Apply approved retention and deletion policies.
- Provide accessible forms, keyboard navigation, readable language and clear errors.
- Obtain appropriate organisational privacy/security review before any real-world deployment.

## 7. Observability and Quality

- Automated tests for API, services, permissions and workflow transitions.
- Audit events for important case operations and human decisions.
- Structured application logging without unnecessary personal data.
- Health endpoint and deployment checks.
- Documented test evidence and known limitations.

## 8. Deployment Evolution

Hosting, identity provider, AI provider and production integrations remain decisions to validate against deployment and operational requirements.
