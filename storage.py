from typing import List

from fastapi import HTTPException

from models import (
    Commander,
    Component,
    MissionReport,
    TerminatorUnit,
    TerminatorUnitCreate,
    UnitClass,
)

unit_classes: List[UnitClass] = []
commanders: List[Commander] = []
components: List[Component] = []
units: List[TerminatorUnit] = []
mission_reports: List[MissionReport] = []

unit_class_id_counter = 1
commander_id_counter = 1
component_id_counter = 1
unit_id_counter = 1
mission_report_id_counter = 1


def next_unit_class_id() -> int:
    global unit_class_id_counter
    value = unit_class_id_counter
    unit_class_id_counter += 1
    return value


def next_commander_id() -> int:
    global commander_id_counter
    value = commander_id_counter
    commander_id_counter += 1
    return value


def next_component_id() -> int:
    global component_id_counter
    value = component_id_counter
    component_id_counter += 1
    return value


def next_unit_id() -> int:
    global unit_id_counter
    value = unit_id_counter
    unit_id_counter += 1
    return value


def next_mission_report_id() -> int:
    global mission_report_id_counter
    value = mission_report_id_counter
    mission_report_id_counter += 1
    return value


def get_unit_class_or_404(unit_class_id: int) -> UnitClass:
    for item in unit_classes:
        if item.id == unit_class_id:
            return item
    raise HTTPException(status_code=404, detail=f"unit_class {unit_class_id} not found")


def get_commander_or_404(commander_id: int) -> Commander:
    for item in commanders:
        if item.id == commander_id:
            return item
    raise HTTPException(status_code=404, detail=f"commander {commander_id} not found")


def get_component_or_404(component_id: int) -> Component:
    for item in components:
        if item.id == component_id:
            return item
    raise HTTPException(status_code=404, detail=f"component {component_id} not found")


def get_unit_or_404(unit_id: int) -> TerminatorUnit:
    for item in units:
        if item.id == unit_id:
            return item
    raise HTTPException(status_code=404, detail=f"unit {unit_id} not found")


def get_mission_report_or_404(mission_report_id: int) -> MissionReport:
    for item in mission_reports:
        if item.id == mission_report_id:
            return item
    raise HTTPException(status_code=404, detail=f"mission_report {mission_report_id} not found")


def check_unit_foreign_keys(payload: TerminatorUnitCreate) -> None:
    get_commander_or_404(payload.commander_id)
    get_unit_class_or_404(payload.unit_class_id)
    for item in payload.components:
        get_component_or_404(item.component_id)
