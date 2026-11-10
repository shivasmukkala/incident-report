# Incident Report

### AI-Assisted Incident and Case Management Platform

Incident Report is a modular case management platform designed to take an incident from its initial report through triage, investigation,resolution and communication.

It provides operational visibility to managers while using AI responsibly to reduce repetitive administrative work.

## Problem

Organisations often manage reports, assignments, investigations and outcomes across  disconnected processes.

This creates delays, poor visibility and inconsistent communication.

## Solution

Incident Report provides one connected case lifecycle:

1. Report an issue.
2. Triage, categorise and prioritise.
3. Identify possible duplicate reports.
4. Route the case to the appropriate team.
5. Investigate and record findings.
6. Record resolution evidence.
7. Draft and approve an outcome letter.
8. Review operational performance.

## Initial Setting

**Incident Report — Health and Safety**

Initial report categories:

- Safety hazards
- Near-misses
- Minor incidents
- Unsafe practices

Initial responsible teams:

- Health and Safety Advisor
- Line Manager
- Site Supervisor

Primary performance indicator:

**Time from report received to risk controlled and incident resolved **

## Core Users

- Reporter
- Triage officer
- Field officer
- Team manager

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React and Vite |
| Backend | Python and FastAPI |
| Database | SQLite initially |
| Validation | Pydantic |
| AI integration | Backend-managed AI service |
| Testing | Pytest and frontend testing tools |
| Version control | Git |

## Responsible AI

AI assists with classification, priority recommendations, duplicate suggestions, summaries, drafting and translation.

Humans retain authority over consequential decisions.

AI-generated communications require human approval before sending.

Only fictional, open, anonymised or explicitly approved data will be used during development.

## Repository Structure

- `frontend/` - React application
- `backend/` - FastAPI application
- `docs/` - Product and engineering documentation
- `.claude/skills/` - Reusable Claude Code project skills
- `tests/` - Integration and end-to-end tests

## Development Status

Currently establishing the engineering foundation.

See [Development Plan](docs/DEVELOPMENT_PLAN.md).

## Getting Started

Development and installation instructions will be added as the frontend and backend applications are implemented.

## Security

Never commit passwords, API keys, tokens, personal data or confidential organisational information.

See [Security](docs/SECURITY.md).

## Project Principles

- Reusable components, not one-off screens.
- Human approval for consequential AI-assisted decisions.
- Accessible and understandable interfaces.
- Evidence-based case management.
- Traceable actions and decisions.
- Security from the beginning.

## Project Status

Hackathon development project. Not approved for real-world health and safety operations.
