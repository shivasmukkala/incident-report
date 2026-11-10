#Incident Report - Claude Code Instructions

## Project Identity

Incident Report is an AI-assisted incident and case management platform.

Initial domain: Health and Safety.

The objective is to manage the complete case lifecycle from reporting to verified resolution and management review.

## Product Vision

Build a modular and reusable platform that can later support:

- Health and safety
- Workplace facilities
- Public realm maintenance
- Housing repairs
- Customer complaints
-generic enough that any organisation could use it.
- A council,
- a housing association, 
- a facilities team,
-  a retailer and
-  a manufacturer should all be able to look at it and say, “we could use that.”  

Do not hard-code the application around one industry.

## Technology

Frontend:
- React
- Vite
- JavaScript initially
- CSS

Backend:
- Python
- FastAPI
- Pydantic
- SQLAlchemy when database integration is introduced

Database:
- SQLite for the initial development environment.
- Keep the design suitable for PostgreSQL migration.

Testing:
- Pytest for backend.
- Appropriate React component and integration tests.

## Engineering Rules

1. Do not invent completed functionality.
2. Do not claim tests passed unless they were executed.
3. Keep frontend and backend responsibilities separate.
4. Use reusable components.
5. Keep business rules out of presentation components.
6. Validate all incoming API data.
7. Use clear names and small, maintainable modules.
8. Document significant architectural decisions.
9. Do not introduce unnecessary dependencies.
10. Explain alternatives when making significant technology choices.

## Responsible AI Rules

1. AI provides suggestions, not autonomous final decisions.
2. Humans approve consequential priority, assignment and closure decisions.
3. AI must never automatically downgrade a serious safety report.
4. Do not treat low model confidence as low incident severity.
5. Record AI suggestions and human overrides.
6. Preserve original reporter information.
7. Disclose AI-assisted drafting and translation.
8. Do not send generated outcome letters without approval.
9. Test performance across different writing styles and languages.
10. Never send confidential data to public AI services.

## Security Rules

- Never commit secrets.
- Never expose backend API keys to React.
- Validate file uploads.
- Restrict upload size and file types.
- Apply role-based authorisation before production use.
- Keep audit records for consequential actions.
- Use fictional or approved anonymised data.
- Do not connect to real organisational systems during the hackathon.

## Development Workflow

For each feature:

1. Understand the requirement.
2. Identify affected components.
3. Propose a small implementation plan.
4. Implement the feature.
5. Add or update tests.
6. Execute relevant tests.
7. Review security and accessibility implications.
8. Update documentation.
9. Summarise changed files and verification results.

Do not silently change existing architectural decisions.

## Git Workflow

- Main branch must remain stable.
- Use descriptive feature branches.
- Make small, meaningful commits.
- Never commit environment files or generated secrets.
- Do not force-push shared branches without approval.

## Communication

Use plain UK English.

Explain:
- What is being built.
- Why it is needed.
- What files change.
- How to run it.
- How to verify it.
- Known limitations.

Always distinguish implemented functionality from planned functionality.
