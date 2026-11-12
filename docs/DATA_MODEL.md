
# Incident Report - Data Model

## 1. Design Principles

- Use SQLite for initial development.
- Use UUIDs or equivalent unique identifiers.
- Keep database access separate from business logic.
- Preserve historical decisions and assignments.
- Store timestamps in UTC.
- Support migration to PostgreSQL.
- Minimise personal and sensitive information.
- Never store uploaded files directly in database records.

## 2. Cases

Implementation status: The initial Case model is implemented.
Additional fields and related entities in this document represent the planned target data model unless explicitly marked as implemented.

- id
- reference
- reporter_type: employee, resident, visitor, public, other
- reporter_name (optional)
- reporter_contact (optional)
- contact_updates_requested
- is_anonymous
- anonymous_access_token_hash (optional)
- category
- description
- perceived_urgency
- confirmed_priority (set by case handler)
- incident_datetime
- location_description (optional)
- location_precision
- location_source
- location_confirmed_by (optional)
- status
- created_at
- updated_at
- risk_controlled_at (optional)
- resolved_at (optional)
- verified_at (optional)
- closed_at (optional)


## 3. Intake Sessions

Temporary reporting sessions created before an incident is submitted.

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
- Manage voice and text reporting before case creation.
- Store suggested form fields for reporter review.
- Link follow-up questions and voice records to the reporting session.
- Create a case only after the reporter approves submission.
- Expire abandoned sessions according to an approved retention policy.


## 4. Users

Authorised staff accounts.

- id
- name
- email
- role
- team_id
- is_active
- created_at

Roles:
- triage_officer
- field_officer
- manager
- administrator

## 5. Teams

Operational teams.

- id
- name
- description
- is_active

## 6. Assignments

Assignment history.

- id
- case_id
- assigned_user_id
- assigned_team_id
- assigned_by
- assignment_reason
- assigned_at
- unassigned_at (optional)

## 7. Investigations

Officer investigation records.

- id
- case_id
- officer_id
- attendance_time
- findings
- immediate_controls
- resolution_notes
- created_at
- updated_at

## 8. Corrective Actions

Actions required to control or prevent risks.

- id
- case_id
- description
- owner_id
- due_date
- status
- completed_at (optional)
- completion_notes
- verified_by (optional)
- verified_at (optional)
- created_at

## 9. Evidence

Uploaded files and supporting evidence.

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

## 10. Voice Records

Voice transcription records.

- id
- case_id (optional, before submission)
- transcript
- language
- speech_service
- model_version
- processing_status
- audio_storage_path (optional)
- retention_expiry (optional)
- created_at
- intake_session_id

## 11. Follow-up Questions

Questions and answers used to clarify reports.

- id
- case_id
- question_text
- answer_text (optional)
- question_reason
- ai_assessment_id (optional)
- status
- created_at
- answered_at (optional)
- intake_session_id (optional)

## 12. AI Assessments

Record AI-generated suggestions.

- id
- case_id
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
- intake_session_id (optional)

Task types may include:
- speech_extraction
- follow_up_questions
- classification
- duplicate_detection
- investigation_summary
- translation
- outcome_drafting

## 13. Outcome Letters

- id
- case_id
- language
- draft_content
- approval_status
- approved_by (optional)
- approved_at (optional)
- sent_at (optional)
- created_at

## 14. Audit Events

Record important case and operational changes.

- id
- case_id
- actor_id (optional for system actions)
- action
- entity_type
- entity_id
- previous_value (optional)
- new_value (optional)
- timestamp

## 15. Important Data Rules

- A case reference is not sufficient to access an anonymous report.
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

## 16. Database Relationships

- One case can have multiple assignments.
- One case can have multiple investigations.
- One case can have multiple corrective actions.
- One case can have multiple evidence records.
- One case can have multiple AI assessments.
- One case can have multiple follow-up questions.
- One case can have multiple audit events.
- Users belong to teams where applicable.
- Assignments link cases, users and teams.
- Corrective actions may have an assigned owner.
- One intake session can have multiple voice records.
- One intake session can have multiple follow-up questions.
- One intake session can have multiple AI assessments.
- One intake session can create one submitted case.
- After submission, related intake records retain their original history.
