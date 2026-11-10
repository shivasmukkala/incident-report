# Initial Data Model

## Case

- id
- reference
- reporter_name
- reporter_contact
- is_anonymous
- category
- severity
- description
- location
- incident_datetime
- status
- assigned_team_id
- created_at
- updated_at
- risk_controlled_at
- resolved_at
- closed_at

## Team

- id
- name
- description

## User

- id
- name
- role
- team_id

## Assignment

- id
- case_id
- assigned_user_id
- assigned_team_id
- assigned_at

## Investigation

- id
- case_id
- officer_id
- attendance_time
- findings
- immediate_controls
- resolution_notes

## Evidence

- id
- case_id
- filename
- content_type
- storage_path
- uploaded_at

## AI Assessment

- id
- case_id
- task_type
- suggestion
- model_version
- confidence
- human_decision
- override_reason
- created_at

## Outcome Letter

- id
- case_id
- language
- draft_content
- approval_status
- approved_by
- approved_at
- sent_at

## Audit Event

- id
- case_id
- actor_id
- action
- previous_value
- new_value
- timestamp

This is a logical starting model. Physical database constraints
and relationships must be defined during implementation.
