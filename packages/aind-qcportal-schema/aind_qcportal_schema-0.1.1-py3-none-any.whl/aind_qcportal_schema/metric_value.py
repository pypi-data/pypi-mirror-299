from pydantic import BaseModel, Field
from typing import Any, Optional
from aind_data_schema.core.quality_control import Status


class DropdownMetric(BaseModel):
    """Dropdown metric schema"""

    value: Any = Field(..., title="Value")
    options: list[Any] = Field(..., title="Options")
    status: Optional[list[Status]] = Field(default=None, title="Option to status mapping")
    type: str = "dropdown"


class CheckboxMetric(BaseModel):
    """Checkbox metric schema"""

    value: Any = Field(..., title="Value")
    options: list[Any] = Field(..., title="Options")
    status: Optional[list[Status]] = Field(default=None, title="Option to status mapping")
    type: str = "dropdown"


class RulebasedMetric(BaseModel):
    """Rulebased metric schema"""

    value: Any = Field(..., title="Value")
    rule: str = Field(..., title="Runs eval(rule), Status.PASS when true, Status.FAIL when false")
