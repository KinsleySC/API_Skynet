from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

import storage
from models import ThreatLevel, TerminatorUnit, TerminatorUnitCreate, TerminatorUnitUpdate

router = APIRouter(prefix="/units", tags=["units"])


@router.post("", response_model=TerminatorUnit, status_code=201)
def create_unit(payload: TerminatorUnitCreate):
    storage.check_unit_foreign_keys(payload)
    unit = TerminatorUnit(id=storage.next_unit_id(), **payload.model_dump())
    storage.units.append(unit)
    return unit


@router.get("", response_model=List[TerminatorUnit])
def list_units(
    unit_class_id: Optional[int] = None,
    threat_level: Optional[ThreatLevel] = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort_by: Optional[str] = Query(default=None, pattern="^(assembly_time_minutes|title)$"),
):
    result = storage.units
    if unit_class_id is not None:
        result = [unit for unit in result if unit.unit_class_id == unit_class_id]
    if threat_level is not None:
        result = [unit for unit in result if unit.threat_level == threat_level]
    if sort_by is not None:
        result = sorted(result, key=lambda unit: getattr(unit, sort_by))
    return result[offset: offset + limit]


@router.get("/{unit_id}", response_model=TerminatorUnit)
def get_unit(unit_id: int):
    return storage.get_unit_or_404(unit_id)


@router.patch("/{unit_id}", response_model=TerminatorUnit)
def update_unit(unit_id: int, payload: TerminatorUnitUpdate):
    unit = storage.get_unit_or_404(unit_id)
    update_data = payload.model_dump(exclude_unset=True)
    if "commander_id" in update_data:
        storage.get_commander_or_404(update_data["commander_id"])
    if "unit_class_id" in update_data:
        storage.get_unit_class_or_404(update_data["unit_class_id"])
    if "components" in update_data and update_data["components"] is not None:
        for item in update_data["components"]:
            storage.get_component_or_404(item["component_id"])
    updated = unit.model_copy(update=update_data)
    storage.units[storage.units.index(unit)] = updated
    return updated


@router.delete("/{unit_id}", status_code=204)
def delete_unit(unit_id: int):
    unit = storage.get_unit_or_404(unit_id)
    if any(report.unit_id == unit_id for report in storage.mission_reports):
        raise HTTPException(status_code=400, detail="unit has mission_reports and cannot be deleted")
    storage.units.remove(unit)
    return None
