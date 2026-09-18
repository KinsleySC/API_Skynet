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

