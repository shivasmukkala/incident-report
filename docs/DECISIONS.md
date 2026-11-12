# Architecture Decision Records

Future decisions should include context, alternatives, consequences and implementation evidence.

## ADR-001: React and Vite

Status: Accepted

Context:
The product requires one responsive application with role-oriented experiences and reusable UI components.

Decision:
Use React with Vite for the frontend.

Consequences:
- Share UI components across role-based views.
- Treat frontend role-based navigation as presentation only; backend authorisation remains mandatory.

## ADR-002: FastAPI

Status: Accepted

Context:
The project uses Python and requires validated REST APIs, modular services and integration with Python-based AI capabilities.

Decision:
Use FastAPI and Pydantic for the backend API.

Consequences:
- Keep route handlers thin.
- Put business rules and workflow operations in service modules.
- Enforce permissions on the backend.

## ADR-003: SQLite for Initial Development

Status: Accepted

Context:
The initial MVP needs simple persistent storage and a low-friction local development setup.

Decision:
Start with SQLite while keeping database access modular. Use SQLAlchemy and Alembic. PostgreSQL is the intended production migration option.

Consequences:
- Avoid SQLite-specific assumptions in business logic.
- Test migrations and database behaviour.
- Reassess database choice before production deployment.

## ADR-004: Human-in-the-Loop AI

Status: Accepted

Context:
Incident and safety-related decisions and communications require accountability.

Decision:
AI suggestions require human review and approval where consequential. AI must not automatically close cases, merge duplicates, downgrade serious reports or dispatch outcome communications.

Consequences:
- Record AI suggestions and model information where available.
- Record human decisions and overrides.
- Keep emergency escalation and safety-critical workflow rules deterministic.

## ADR-005: Configurable Sector Settings

Status: Accepted

Context:
The product should support reusable components that can be adapted across operational settings.

Decision:
Keep categories, teams, SLA rules and routing policies configurable rather than hard-coding a single organisation's structure.

Consequences:
- Model Category and Team as data entities.
- Keep initial Health and Safety configuration separate from reusable application logic.

## ADR-006: Azure AI Speech for Voice Transcription

Status: Accepted for MVP evaluation

Context:
Incident Report may provide optional voice-assisted reporting. The solution should be reliable, economical and privacy-conscious.

Decision:
Evaluate Azure AI Speech standard speech-to-text for voice transcription.

Development:
Use the F0 free tier where available and suitable.

Production:
Evaluate the S0 pay-as-you-go tier using measured usage, accuracy and regional pricing.

Constraints:
- Voice input remains optional.
- Reporters review and approve extracted information.
- Audio retention must follow an approved policy.
- Do not store recordings unnecessarily.
- Provide a text-based alternative.

Evidence required:
- Transcription accuracy tests using varied accents and background noise.
- Cost per hour of audio.
- Privacy and data-processing review.
- Error handling and service availability tests.

## ADR-007: Python Full-Stack Architecture

Status: Accepted

Context:
Incident Report requires a responsive, role-based application with modular APIs, maintainable business logic, structured data persistence and AI integration capabilities.

Decision:
Use React and Vite for the frontend, Python and FastAPI for the backend, and SQLAlchemy for database access. Use SQLite for initial development and PostgreSQL as the intended production database.

Reasons:
- Maintainability: Separate presentation, API, business logic, AI services and data persistence.
- Python development: Build practical Python and backend engineering capability.
- API control: Maintain control over API contracts, validation, business rules and access control.
- Modularity: Keep components independently testable and replaceable.
- AI integration: Integrate AI capabilities through modular services without coupling core workflows to a specific AI provider.

Consequences:
- The project is responsible for developing and maintaining its frontend, backend, authentication, authorisation and integrations.
- Backend permissions must protect all restricted operations.
- Architecture changes must preserve testability, accessibility, auditability and responsible AI controls.

## ADR-008: Product Name

Status: Accepted

Context:
The project requires consistent product, repository and API naming.

Decision:
Use Incident Report as the product name, `incident-report` as the repository/project directory name and `Incident Report API` as the API title.

Consequences:
- Use Incident Report consistently in documentation, UI, API metadata and presentations.
- Do not use the earlier working name Safe Spot as the product/API name.
