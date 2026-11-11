# Architecture Decision Records

## ADR-001: React and Vite

Status: Accepted

Context:
The product requires multiple responsive interfaces and reusable UI.

Decision:
Use React with Vite.

## ADR-002: FastAPI

Status: Accepted

Context:
The team is using Python and requires validated REST APIs.

Decision:
Use FastAPI and Pydantic.

## ADR-003: SQLite for Initial Development

Status: Accepted

Context:
The hackathon MVP needs simple persistent storage.

Decision:
Start with SQLite while keeping database access modular.

## ADR-004: Human-in-the-Loop AI

Status: Accepted

Context:
Safety-related decisions and communications require accountability.

Decision:
AI suggestions require human review and approval where consequential.

## ADR-005: Configurable Sector Settings

Status: Accepted

Context:
The platform should be reusable across different operational sectors.

Decision:
Keep categories, teams and routing policies configurable.

Future decisions should be added with context, alternatives,
consequences and implementation evidence.

## ADR-006: Azure AI Speech for Voice Transcription

Status: Accepted for MVP evaluation

Context:
Safe Spot requires optional voice-assisted incident reporting.
The solution should be reliable, economical and privacy-conscious.

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
