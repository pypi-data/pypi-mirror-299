from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

from luna_sdk.schemas.enums.optimization import InputType
from luna_sdk.schemas.optimization_formats.bqm import BQMSchema
from luna_sdk.schemas.optimization_formats.cqm import CQMSchema
from luna_sdk.schemas.optimization_formats.lp import LPSchema
from luna_sdk.schemas.pretty_base import PrettyBase
from luna_sdk.schemas.wrappers import PydanticDatetimeWrapper


class Optimization(PrettyBase):
    """
    Pydantic model for optimization going OUT.
        Attributes
    ----------
    id: str
        Id of the optimization
    created_date: Optional[DatetimeWrapper]
        Date when optimization was created
    created_by: Optional[str]
        Id of the user who created optimization
    modified_date: Optional[DatetimeWrapper]
        Date when optimization was modified
    modified_by: Optional[str]
        Id of the user who modified optimization
    """

    id: str
    name: Optional[str] = None
    created_date: PydanticDatetimeWrapper
    created_by: str
    modified_date: Optional[PydanticDatetimeWrapper] = None
    modified_by: Optional[str] = None
    input_type: Optional[InputType] = None
    use_case_name: Optional[str] = None
    params: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="ignore", from_attributes=False)


class OptimizationQubo(BaseModel):
    id: str
    name: Optional[str] = None
    created_date: PydanticDatetimeWrapper
    created_by: str
    modified_date: Optional[PydanticDatetimeWrapper] = None
    modified_by: Optional[str] = None

    matrix: List[List[float]]


class OptimizationBQM(Optimization, BQMSchema): ...


class OptimizationCQM(Optimization, CQMSchema): ...


class OptimizationLP(Optimization, LPSchema): ...


class OptimizationUseCase(Optimization, BQMSchema):
    use_case: Dict[str, Any]


T = TypeVar("T")


class OptimizationCreate(BaseModel, Generic[T]):
    """Pydantic model for optimization coming IN."""

    instance: T
