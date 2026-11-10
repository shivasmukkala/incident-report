# System Architecture

## Overview

Incident Report uses a modular frontend and backend architecture.

## Frontend

React provides role-oriented interfaces:

- Reporter portal
- Triage workspace
- Field officer workspace
- Management dashboard

Reusable UI components should be shared wherever practical.

## Backend

FastAPI exposes validated API endpoints.

Responsibilities:

- Case creation and retrieval
- Workflow management
- Routing rules
- AI service integration
- Notification orchestration
- Audit history

## Data Layer

SQLite is the initial database.

Database access must be isolated from API and business logic.

PostgreSQL is the intended production migration option.

## AI Layer

AI functionality is accessed only through backend services.

AI capabilities:

- Classification suggestions
- Duplicate similarity suggestions
- Investigation summaries
- Outcome letter drafting
- Translation

Deterministic rules must handle safety-critical escalation.

## Case Lifecycle

Submitted
-> Under Review
-> Assigned
-> In Progress
-> Resolved
-> Verified
-> Closed

Additional states may include Rejected, Duplicate and Reopened.

## Design Principles

- Separation of concerns
- Reusable components
- Human-in-the-loop decisions
- Explicit workflow transitions
- Auditable operations
- Configurable sector-specific rules
