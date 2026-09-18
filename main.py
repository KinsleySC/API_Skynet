from fastapi import FastAPI

from routers import commanders, components, mission_reports, stats, unit_classes, units

app = FastAPI(title="SkynetCommand API")

app.include_router(unit_classes.router)
app.include_router(commanders.router)
app.include_router(components.router)
app.include_router(units.router)
app.include_router(mission_reports.router)
app.include_router(stats.router)
