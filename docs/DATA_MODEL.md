# Incident Report - Data Model

## 1. Design Principles

- Use SQLite for initial development.
- Use UUIDs or equivalent externally safe identifiers where appropriate.
- Keep database access separate from business logic.
- Preserve historical decisions and assignments.
- Store timestamps in UTC.
- Support migration to PostgreSQL.
- Minimise personal and sensitive information.
- Never store uploaded file contents directly in relational database records.
- Use fictional or approved anonymised data for demonstrations.
- Apply role-based access to personal and exact location data.

Implementation status: the initial `Case` model exists. The entities below describe the target model; do not assume they are already implemented.

## 2. Case

The central request/incident record.

Planned fields:
- id
- reference (unique public-facing case reference)
- title
- description
- reporter_type
- reporter_id (optional, where a Reporter record is used)
- reporter_name (optional)
- reporter_contact (optional)
- contact_updates_requested
- is_anonymous
- anonymous_access_token_hash (optional)
- category_id (optional during migration; required when category selection is enforced)
- perceived_urgency
- confirmed_priority (set by authorised case handler)
- incident_datetime
- location_description (optional)
- location_precision
- location_source
- location_confirmed_by (optional user reference)
- status
- created_at
- updated_at
- acknowledged_at (optional)
- sla_due_at (optional)
- risk_controlled_at (optional)
- resolved_at (optional)
- verified_at (optional)
- closed_at (optional)

Current implementation fields: id, title, description, category as nullable text, incident_datetime, perceived_urgency, location_description, location_precision, status and created_at. The current model does not yet implement the full target Case fields.

## 3. Reporter

Reporter information, separated from staff identity where appropriate.

Planned fields:
- id
- reporter_type
- name (optional)
- contact_email (optional)
- contact_phone (optional)
- preferred_language (optional)
- preferred_contact_method (optional)
- contact_updates_requested
- created_at

Anonymous reporters may have no Reporter record. Do not collect information that is not needed for the service.

## 4. Category

Configurable classification and routing metadata.

Planned fields:
- id
- name
- description
- default_team_id (optional)
- default_priority (optional)
- is_active
- created_at
- updated_at

A Case references Category through `category_id`. During migration from the current free-text `Case.category`, existing values must be mapped deliberately; do not silently discard them.

## 5. Team

Operational teams responsible for handling cases.

Planned fields:
- id
- name
- description
- contact_email (optional)
- working_hours (optional/configurable representation)
- manager_id (optional user reference)
- is_active

## 6. User

Authorised staff accounts.

Planned fields:
- id
- name
- email
- role
- team_id (optional)
- is_active
- created_at

Supported staff roles:
- case_handler
- field_officer
- team_manager

An administrator role may be used for technical configuration if required, but it is not a primary operational role. Reporter access is handled separately and may be anonymous.

## 7. Assignment

Preserves assignment history rather than overwriting the current assignee.

Planned fields:
- id
- case_id
- assigned_user_id (optional)
- assigned_team_id
- assigned_by
- assignment_reason
- assigned_at
- unassigned_at (optional)

## 8. Investigation / Site Visit

Records officer attendance and findings.

Planned fields:
- id
- case_id
- officer_id
- attendance_time (optional)
- findings
- immediate_controls (optional)
- resolution_notes (optional)
- created_at
- updated_at

## 9. Corrective Action

Actions required to control or prevent risks.

Planned fields:
- id
- case_id
- description
- owner_id (optional)
- due_date (optional)
- status
- completed_at (optional)
- completion_notes (optional)
- verified_by (optional)
- verified_at (optional)
- created_at

## 10. Evidence

Metadata for uploaded files and supporting evidence.

Planned fields:
- id
- case_id
- investigation_id (optional)
- corrective_action_id (optional)
- original_filename
- stored_filename
- content_type
- file_size
- storage_path
- scan_status
- uploaded_by (optional)
- uploaded_at

Files must be validated and scanned before authorised access. The file itself is stored outside the relational database.

## 11. Intake Session

Temporary reporting session before a case is submitted.

Planned fields:
- id
- session_token_hash
- reporter_type (optional)
- status: in_progress, ready_for_review, submitted, expired
- extracted_fields (structured data)
- created_at
- updated_at
- expires_at (optional)
- submitted_case_id (optional)

Purpose:
- Manage voice/text reporting before case creation.
- Store suggested fields for reporter review.
- Link voice records and follow-up questions to the session.
- Create a Case only after reporter approval.
- Expire abandoned sessions under an approved retention policy.

## 12. Voice Record

Planned fields:
- id
- case_id (optional before submission)
- intake_session_id
- transcript
- language
- speech_service
- model_version
- processing_status
- audio_storage_path (optional)
- retention_expiry (optional)
- created_at

Voice is optional. Preserve the transcript as appropriate, avoid unnecessary audio retention and provide a text alternative.

## 13. Follow-up Question

Planned fields:
- id
- case_id (optional before submission)
- intake_session_id (optional)
- question_text
- answer_text (optional)
- question_reason
- ai_assessment_id (optional)
- status
- created_at
- answered_at (optional)

## 14. AI Assessment

Records AI-generated suggestions and review.

Planned fields:
- id
- case_id (optional before submission)
- intake_session_id (optional)
- task_type
- input_reference
- suggestion
- model_provider
- model_version
- confidence (optional)
- human_decision (optional)
- override_reason (optional)
- reviewed_by (optional)
- reviewed_at (optional)
- created_at

Task types may include speech_extraction, follow_up_questions, classification, priority_recommendation, duplicate_detection, investigation_summary, translation and outcome_drafting.

## 15. Communication / Outcome Letter

Planned fields:
- id
- case_id
- communication_type (acknowledgement or outcome)
- language
- draft_content
- approval_status
- approved_by (optional)
- approved_at (optional)
- sent_at (optional)
- created_at

## 16. SLA Rule

Planned fields:
- id
- priority
- acknowledgement_target
- resolution_target
- working_calendar (optional/configurable)
- is_active

SLA targets should be configurable for each priority level. Example targets are for demonstration purposes only; operational targets and working-time rules must be approved by the organisation.

## 17. Audit Event

Records important case and operational changes.

Planned fields:
- id
- case_id (optional for non-case events)
- actor_id (optional for system actions)
- action
- entity_type
- entity_id
- previous_value (optional)
- new_value (optional)
- timestamp

## 18. Relationships

- One Category can be associated with many Cases; each Case has zero or one Category during the migration period, then normally one.
- A Category may have one default Team.
- One Team can have many Users.
- One Team can be responsible for many Assignments.
- One Case can have many Assignments over time.
- One Case can have many Investigations.
- One Case can have many Corrective Actions.
- One Case can have many Evidence records.
- One Case can have many AI Assessments.
- One Case can have many Follow-up Questions.
- One Case can have many Communications.
- One Case can have many Audit Events.
- A User may be assigned to many Cases through Assignment records.
- A Corrective Action may have one owner.
- One Intake Session can have multiple Voice Records, Follow-up Questions and AI Assessments.
- One Intake Session can create at most one submitted Case.
- Reporter records may be associated with multiple Cases; anonymous reports need not have a Reporter record.

## 19. Important Data Rules

- A case reference alone is not sufficient to access an anonymous report.
- Store only a hash of an anonymous access token.
- Reporter urgency and professional priority must remain separate.
- Incident time and report submission time must remain separate.
- Attendance does not mean risk controlled.
- Risk controlled, resolved, verified and closed are separate milestones.
- Assignment history must be preserved.
- AI suggestions must not overwrite human decisions.
- Evidence must be validated and malware-scanned before authorised access.
- Exact location data must only be visible to authorised roles.
- Apply approved retention and deletion policies to personal data.
- Preserve audit history according to the organisation's retention policy.
