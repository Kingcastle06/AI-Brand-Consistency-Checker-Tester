from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class JobStatus(str, Enum):
    ACCEPTED = "accepted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"


class Artifact(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    path: str
    type: str
    description: Optional[str] = None


class BrandIssue(BaseModel):
    """Strict structural definition for an individual corporate guideline violation."""
    model_config = ConfigDict(strict=True, extra="forbid")

    issue_name: str = Field(..., description="Short classification of the infraction (e.g., Tone Violation).")
    offending_text: str = Field(..., description="The exact problematic string detected in copy.")
    corrected_text: str = Field(..., description="The highly accurate engineering/brand alternative.")
    brand_rule_violated: str = Field(..., description="The explicit guideline reference number or string.")


class BrandCheckerResult(BaseModel):
    """The concrete domain model wrapped inside the generic result dictionary."""
    model_config = ConfigDict(strict=True, extra="forbid")

    summary: str = Field(..., description="Executive summary overview of copy compliance.")
    issues: List[BrandIssue] = Field(..., description="Array of zero or more structured rule infractions.")


class CheckerInput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    request_id: str = Field(..., min_length=1, description="Caller-supplied idempotency and trace identifier.")
    tool_id: Literal["ai_brand_consistency_checker"] = "ai_brand_consistency_checker"
    input: Dict[str, Any] = Field(..., description="Domain input for AI Brand Consistency Checker.")
    options: Dict[str, Any] = Field(..., description="Execution options such as output format or limits.")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Non-sensitive caller metadata for tracing and audit.")


class CheckerOutput(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    job_id: str = Field(..., min_length=1, description="Server-generated job identifier.")
    tool_id: Literal["ai_brand_consistency_checker"] = "ai_brand_consistency_checker"
    status: JobStatus = Field(..., description="Job lifecycle state.")
    result: Optional[BrandCheckerResult] = Field(..., description="Validated domain result. Structured strictly when status is succeeded.")
    metadata: Dict[str, Any]
    citations: Optional[List[Dict[str, Any]]] = None
    warnings: Optional[List[str]] = None
    artifacts: Optional[List[Artifact]] = None