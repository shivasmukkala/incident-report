from enum import Enum


class CaseStatus(str, Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INVESTIGATING = "investigating"
    ACTION_IN_PROGRESS = "action_in_progress"
    RESOLVED = "resolved"
    VERIFIED = "verified"
    CLOSED = "closed"
