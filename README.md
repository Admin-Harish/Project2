# Project2 – Inventory API

A small containerized REST API for tracking inventory items. It is a sample target for
NEXUS: paste this repository's clone link into the NEXUS UI and NEXUS builds the image,
runs it, executes the approved test cases against it, and emails the report.

## Run

```bash
docker build -t project2 .
docker run --rm -p 8001:8001 project2
```

The service listens on port **8001**. Interactive docs: http://localhost:8001/docs

## API

State is in memory and resets when the container restarts. Item IDs are integers assigned
sequentially starting at **1**. Item names are unique, case-insensitively.

| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | – | 200 `{"status": "ok", "service": "project2"}` | – |
| GET | `/api/items` | – | 200 `{"items": [...], "count": n}`; optional `?q=` filters by name substring | – |
| POST | `/api/items` | `{"name": "Widget", "quantity": 5}` (`quantity` optional, default 0) | 201, returns the item with `id` and `in_stock` (true when quantity > 0) | 409 duplicate name, 422 invalid body (missing/empty name, negative quantity) |
| GET | `/api/items/{id}` | – | 200, returns the item | 404 unknown id |
| PUT | `/api/items/{id}` | `{"quantity": 0}` | 200, returns the updated item (`in_stock` recalculated) | 404 unknown id, 422 negative quantity |
| DELETE | `/api/items/{id}` | – | 204, empty body | 404 unknown id |

## Tests

```bash
pip install -r requirements.txt pytest httpx
pytest
```
