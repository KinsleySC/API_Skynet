from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

app = FastAPI(title="SkynetCommand API")


class UnitClassBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class UnitClassCreate(UnitClassBase):
    pass


class UnitClassUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)


class UnitClass(UnitClassBase):
    id: int


unit_classes: List[UnitClass] = []
unit_class_id_counter = 1


def get_unit_class_or_404(unit_class_id: int) -> UnitClass:
    for c in unit_classes:
        if c.id == unit_class_id:
            return c
    raise HTTPException(status_code=404, detail=f"unit_class {unit_class_id} not found")


@app.post("/unit-classes", response_model=UnitClass, status_code=201)
def create_unit_class(payload: UnitClassCreate):
    global unit_class_id_counter
    unit_class = UnitClass(id=unit_class_id_counter, **payload.model_dump())
    unit_class_id_counter += 1
    unit_classes.append(unit_class)
    return unit_class


@app.get("/unit-classes", response_model=List[UnitClass])
def list_unit_classes():
    return unit_classes


@app.get("/unit-classes/{unit_class_id}", response_model=UnitClass)
def get_unit_class(unit_class_id: int):
    return get_unit_class_or_404(unit_class_id)


@app.patch("/unit-classes/{unit_class_id}", response_model=UnitClass)
def update_unit_class(unit_class_id: int, payload: UnitClassUpdate):
    unit_class = get_unit_class_or_404(unit_class_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = unit_class.model_copy(update=update_data)
    unit_classes[unit_classes.index(unit_class)] = updated
    return updated


@app.delete("/unit-classes/{unit_class_id}", status_code=204)
def delete_unit_class(unit_class_id: int):
    unit_class = get_unit_class_or_404(unit_class_id)
    unit_classes.remove(unit_class)
    return None



class CommanderBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: str
    bio: Optional[str] = Field(default=None, max_length=300)


class CommanderCreate(CommanderBase):
    pass


class CommanderUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    email: Optional[str] = None
    bio: Optional[str] = Field(default=None, max_length=300)


class Commander(CommanderBase):
    id: int


commanders: List[Commander] = []
commander_id_counter = 1


def get_commander_or_404(commander_id: int) -> Commander:
    for a in commanders:
        if a.id == commander_id:
            return a
    raise HTTPException(status_code=404, detail=f"commander {commander_id} not found")


@app.post("/commanders", response_model=Commander, status_code=201)
def create_commander(payload: CommanderCreate):
    global commander_id_counter
    commander = Commander(id=commander_id_counter, **payload.model_dump())
    commander_id_counter += 1
    commanders.append(commander)
    return commander


@app.get("/commanders", response_model=List[Commander])
def list_commanders():
    return commanders


@app.get("/commanders/{commander_id}", response_model=Commander)
def get_commander(commander_id: int):
    return get_commander_or_404(commander_id)


@app.patch("/commanders/{commander_id}", response_model=Commander)
def update_commander(commander_id: int, payload: CommanderUpdate):
    commander = get_commander_or_404(commander_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = commander.model_copy(update=update_data)
    commanders[commanders.index(commander)] = updated
    return updated


@app.delete("/commanders/{commander_id}", status_code=204)
def delete_commander(commander_id: int):
    commander = get_commander_or_404(commander_id)
    commanders.remove(commander)
    return None



class PartUnit(str, Enum):
    GRAM = "GRAM"
    KILOGRAM = "KILOGRAM"
    LITER = "LITER"
    MILLILITER = "MILLILITER"
    PIECE = "PIECE"
    TABLESPOON = "TABLESPOON"
    TEASPOON = "TEASPOON"


class ComponentBase(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    unit: PartUnit


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=60)
    unit: Optional[PartUnit] = None


class Component(ComponentBase):
    id: int


components: List[Component] = []
component_id_counter = 1


def get_component_or_404(component_id: int) -> Component:
    for i in components:
        if i.id == component_id:
            return i
    raise HTTPException(status_code=404, detail=f"component {component_id} not found")


@app.post("/components", response_model=Component, status_code=201)
def create_component(payload: ComponentCreate):
    global component_id_counter
    component = Component(id=component_id_counter, **payload.model_dump())
    component_id_counter += 1
    components.append(component)
    return component


@app.get("/components", response_model=List[Component])
def list_components():
    return components


@app.get("/components/{component_id}", response_model=Component)
def get_component(component_id: int):
    return get_component_or_404(component_id)


@app.patch("/components/{component_id}", response_model=Component)
def update_component(component_id: int, payload: ComponentUpdate):
    component = get_component_or_404(component_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = component.model_copy(update=update_data)
    components[components.index(component)] = updated
    return updated


@app.delete("/components/{component_id}", status_code=204)
def delete_component(component_id: int):
    component = get_component_or_404(component_id)
    components.remove(component)
    return None



class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    EXTREME = "EXTREME"


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
        if self.threat_level == ThreatLevel.EXTREME and self.assembly_time_minutes > 30:
            raise ValueError("a EXTREME unit cannot take more than 30 minutes")
        return self


class TerminatorUnitCreate(TerminatorUnitBase):
    pass


class TerminatorUnitUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    commander_id: Optional[int] = None
    unit_class_id: Optional[int] = None
    assembly_time_minutes: Optional[int] = Field(default=None, ge=1, le=600)
    description: Optional[str] = Field(default=None, max_length=500)


class TerminatorUnit(TerminatorUnitBase):
    id: int


units: List[TerminatorUnit] = []
unit_id_counter = 1


def get_unit_or_404(unit_id: int) -> TerminatorUnit:
    for r in units:
        if r.id == unit_id:
            return r
    raise HTTPException(status_code=404, detail=f"unit {unit_id} not found")


@app.post("/units", response_model=TerminatorUnit, status_code=201)
def create_unit(payload: TerminatorUnitCreate):
    global unit_id_counter
    unit = TerminatorUnit(id=unit_id_counter, **payload.model_dump())
    unit_id_counter += 1
    units.append(unit)
    return unit


@app.get("/units", response_model=List[TerminatorUnit])
def list_units():
    return units


@app.get("/units/{unit_id}", response_model=TerminatorUnit)
def get_unit(unit_id: int):
    return get_unit_or_404(unit_id)


@app.patch("/units/{unit_id}", response_model=TerminatorUnit)
def update_unit(unit_id: int, payload: TerminatorUnitUpdate):
    unit = get_unit_or_404(unit_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = unit.model_copy(update=update_data)
    units[units.index(unit)] = updated
    return updated


@app.delete("/units/{unit_id}", status_code=204)
def delete_unit(unit_id: int):
    unit = get_unit_or_404(unit_id)
    if any(rv.unit_id == unit_id for rv in mission_reports):
        raise HTTPException(status_code=400, detail="unit has mission_reports and cannot be deleted")
    units.remove(unit)
    return None



class MissionReportBase(BaseModel):
    unit_id: int
    reporter_name: str = Field(min_length=2, max_length=80)
    success_rating: int
    comment: Optional[str] = Field(default=None, max_length=400)
    classified_note: Optional[str] = Field(default=None, max_length=200)


class MissionReportCreate(MissionReportBase):
    pass


class MissionReportUpdate(BaseModel):
    reporter_name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    success_rating: Optional[int] = None
    comment: Optional[str] = Field(default=None, max_length=400)
    classified_note: Optional[str] = Field(default=None, max_length=200)


class MissionReport(MissionReportBase):
    id: int


mission_reports: List[MissionReport] = []
mission_report_id_counter = 1


def get_mission_report_or_404(mission_report_id: int) -> MissionReport:
    for rv in mission_reports:
        if rv.id == mission_report_id:
            return rv
    raise HTTPException(status_code=404, detail=f"mission_report {mission_report_id} not found")


@app.post("/mission-reports", response_model=MissionReport, status_code=201)
def create_mission_report(payload: MissionReportCreate):
    global mission_report_id_counter
    get_unit_or_404(payload.unit_id)
    mission_report = MissionReport(id=mission_report_id_counter, **payload.model_dump())
    mission_report_id_counter += 1
    mission_reports.append(mission_report)
    return mission_report


@app.get("/mission-reports", response_model=List[MissionReport])
def list_mission_reports(unit_id: Optional[int] = None):
    if unit_id is not None:
        return [rv for rv in mission_reports if rv.unit_id == unit_id]
    return mission_reports


@app.get("/mission-reports/{mission_report_id}", response_model=MissionReport)
def get_mission_report(mission_report_id: int):
    return get_mission_report_or_404(mission_report_id)


@app.patch("/mission-reports/{mission_report_id}", response_model=MissionReport)
def update_mission_report(mission_report_id: int, payload: MissionReportUpdate):
    mission_report = get_mission_report_or_404(mission_report_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = mission_report.model_copy(update=update_data)
    mission_reports[mission_reports.index(mission_report)] = updated
    return updated


@app.delete("/mission-reports/{mission_report_id}", status_code=204)
def delete_mission_report(mission_report_id: int):
    mission_report = get_mission_report_or_404(mission_report_id)
    mission_reports.remove(mission_report)
    return None

