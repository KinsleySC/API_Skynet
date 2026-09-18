# SkynetCommand API

Système de commandement Skynet pour la gestion des unités Terminator, de leur
assemblage et des rapports de mission de la Résistance.

## Structure du projet

```
Apiskynet/
├── main.py              # point d'entrée, assemble les routeurs
├── models.py             # modèles Pydantic + enums (PartUnit, ThreatLevel)
├── storage.py             # stockage en mémoire + fonctions get_or_404
├── routers/
│   ├── unit_classes.py
│   ├── commanders.py
│   ├── components.py
│   ├── units.py
│   ├── mission_reports.py
│   └── stats.py
├── requirements.txt
├── README.md
```

## Ressources

- **UnitClass** : classes d'unités (Infiltration, Combat, Aérienne, Aquatique, Commandement)
- **Commander** : commandants Skynet responsables de la production des unités
- **Component** : pièces détachées utilisées pour assembler une unité
- **TerminatorUnit** : unités Terminator, liées à un commandant, une classe d'unité et des components
- **MissionReport** : rapports de mission rédigés sur une unité

## Relations

- `TerminatorUnit.commander_id` -> `Commander`
- `TerminatorUnit.unit_class_id` -> `UnitClass`
- `TerminatorUnit.components[].component_id` -> `Component`
- `MissionReport.unit_id` -> `TerminatorUnit`

## Lancer le projet

http://127.0.0.1:8000/docs

## Routes principales

- CRUD complet sur `/unit-classes`, `/commanders`, `/components`, `/units`, `/mission-reports`
- `GET /units?unit_class_id=&threat_level=&limit=&offset=&sort_by=` : filtrage, pagination, tri
- `GET /stats` : statistiques agrégées
