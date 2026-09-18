from typing import List

from fastapi import APIRouter, HTTPException

import storage
from models import Commander, CommanderCreate, CommanderPublic, CommanderUpdate

router = APIRouter(prefix="/commanders", tags=["commanders"])


@router.post("", response_model=CommanderPublic, status_code=201)
def create_commander(payload: CommanderCreate):
    commander = Commander(id=storage.next_commander_id(), **payload.model_dump())
    storage.commanders.append(commander)
    return commander


@router.get("", response_model=List[CommanderPublic])
def list_commanders():
    return storage.commanders


@router.get("/{commander_id}", response_model=CommanderPublic)
def get_commander(commander_id: int):
    return storage.get_commander_or_404(commander_id)


@router.patch("/{commander_id}", response_model=CommanderPublic)
def update_commander(commander_id: int, payload: CommanderUpdate):
    commander = storage.get_commander_or_404(commander_id)
    update_data = payload.model_dump(exclude_unset=True)
    updated = commander.model_copy(update=update_data)
    storage.commanders[storage.commanders.index(commander)] = updated
    return updated


@router.delete("/{commander_id}", status_code=204)
def delete_commander(commander_id: int):
    commander = storage.get_commander_or_404(commander_id)
    if any(unit.commander_id == commander_id for unit in storage.units):
        raise HTTPException(status_code=400, detail="commander has published units")
    storage.commanders.remove(commander)
    return None
