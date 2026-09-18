from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class PartUnit(str, Enum):
    GRAM = "GRAM"
    KILOGRAM = "KILOGRAM"
    LITER = "LITER"
    MILLILITER = "MILLILITER"
    PIECE = "PIECE"
    TABLESPOON = "TABLESPOON"
    TEASPOON = "TEASPOON"


class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    EXTREME = "EXTREME"


class UnitClassBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class UnitClassCreate(UnitClassBase):
    pass


class UnitClassUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)


class UnitClass(UnitClassBase):
    id: int


class CommanderBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str
    bio: Optional[str] = Field(default=None, max_length=300)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be blank")
        if any(char.isdigit() for char in v):
            raise ValueError("name must not contain digits")
        return v.strip()


class CommanderCreate(CommanderBase):
    pass


class CommanderUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    email: Optional[str] = None
    bio: Optional[str] = Field(default=None, max_length=300)


class Commander(CommanderBase):
    id: int


class CommanderPublic(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None


class ComponentBase(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    unit: PartUnit

    @field_validator("name")
    @classmethod
    def component_name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("component name must not be blank")
        return v.strip().lower()


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=60)
    unit: Optional[PartUnit] = None


class Component(ComponentBase):
    id: int


class TerminatorUnitComponent(BaseModel):
    component_id: int
    quantity: float = Field(gt=0, le=10000)


class TerminatorUnitBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    commander_id: int
    unit_class_id: int
    assembly_time_minutes: int = Field(ge=1, le=600)
    threat_level: ThreatLevel
    description: Optional[str] = Field(default=None, max_length=500)
    components: List[TerminatorUnitComponent] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_threat_level_matches_time(self):
        if self.threat_level == ThreatLevel.LOW and self.assembly_time_minutes > 30:
            raise ValueError("a LOW threat unit cannot take more than 30 minutes to assemble")
        if self.threat_level == ThreatLevel.EXTREME and self.assembly_time_minutes < 20:
            raise ValueError("an EXTREME threat unit cannot take less than 20 minutes to assemble")
        return self


class TerminatorUnitCreate(TerminatorUnitBase):
    pass


class TerminatorUnitUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    commander_id: Optional[int] = None
    unit_class_id: Optional[int] = None
    assembly_time_minutes: Optional[int] = Field(default=None, ge=1, le=600)
    description: Optional[str] = Field(default=None, max_length=500)
    components: Optional[List[TerminatorUnitComponent]] = None


class TerminatorUnit(TerminatorUnitBase):
    id: int


class MissionReportBase(BaseModel):
    unit_id: int
    reporter_name: str = Field(min_length=2, max_length=80)
    success_rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=400)
    classified_note: Optional[str] = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def check_low_success_rating_has_comment(self):
        if self.success_rating <= 2 and not (self.comment and self.comment.strip()):
            raise ValueError("a success_rating of 2 or less requires a comment")
        return self


class MissionReportCreate(MissionReportBase):
    pass


class MissionReportUpdate(BaseModel):
    reporter_name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    success_rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=400)
    classified_note: Optional[str] = Field(default=None, max_length=200)


class MissionReport(MissionReportBase):
    id: int


class MissionReportPublic(BaseModel):
    id: int
    unit_id: int
    reporter_name: str
    success_rating: int
    comment: Optional[str] = None
