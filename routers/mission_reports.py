from typing import List, Optional

from fastapi import APIRouter

import storage
from models import MissionReport, MissionReportCreate, MissionReportPublic, MissionReportUpdate

router = APIRouter(prefix="/mission-reports", tags=["mission-reports"])


@router.post("", response_model=MissionReportPublic, status_code=201)
def create_mission_report(payload: MissionReportCreate):
    storage.get_unit_or_404(payload.unit_id)
    mission_report = MissionReport(id=storage.next_mission_report_id(), **payload.model_dump())
    storage.mission_reports.append(mission_report)
    return mission_report


@router.get("", response_model=List[MissionReportPublic])
def list_mission_reports(unit_id: Optional[int] = None):
    if unit_id is not None:
        return [report for report in storage.mission_reports if report.unit_id == unit_id]
    return storage.mission_reports


@router.get("/{mission_report_id}", response_model=MissionReportPublic)
def get_mission_report(mission_report_id: int):
    return storage.get_mission_report_or_404(mission_report_id)


@router.patch("/{mission_report_id}", response_model=MissionReportPublic)
def update_mission_report(mission_report_id: int, payload: MissionReportUpdate):
    mission_report = storage.get_mission_report_or_404(mission_report_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = mission_report.model_copy(update=update_data)
    storage.mission_reports[storage.mission_reports.index(mission_report)] = updated
    return updated


@router.delete("/{mission_report_id}", status_code=204)
def delete_mission_report(mission_report_id: int):
    mission_report = storage.get_mission_report_or_404(mission_report_id)
    storage.mission_reports.remove(mission_report)
    return None
