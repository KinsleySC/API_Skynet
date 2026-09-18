from fastapi import APIRouter

import storage

router = APIRouter(tags=["stats"])


@router.get("/stats")
def get_stats():
    total_units = len(storage.units)
    average_assembly_time = (
        round(sum(unit.assembly_time_minutes for unit in storage.units) / total_units, 2)
        if total_units > 0
        else 0
    )

    unit_class_counts = {}
    for unit in storage.units:
        unit_class_counts[unit.unit_class_id] = unit_class_counts.get(unit.unit_class_id, 0) + 1

    most_common_unit_class_id = (
        max(unit_class_counts, key=unit_class_counts.get) if unit_class_counts else None
    )

    most_common_unit_class_name = None
    if most_common_unit_class_id is not None:
        for unit_class in storage.unit_classes:
            if unit_class.id == most_common_unit_class_id:
                most_common_unit_class_name = unit_class.name
                break

    return {
        "total_units": total_units,
        "total_mission_reports": len(storage.mission_reports),
        "average_assembly_time": average_assembly_time,
        "most_common_unit_class": most_common_unit_class_name,
    }
