# LiveFBAds

Using the Meta Ad Library to maintain up-to-date competitor ad reports.

## Getting Started

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   Or use the included `Makefile` helpers:

   ```bash
   make install
   ```

2. Run the FastAPI service locally:

   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`. Interactive docs are exposed at `/docs`.

   With `make`:

   ```bash
   make run
   ```

3. (Optional) Provide a Meta Graph API access token via the `META_ACCESS_TOKEN` environment variable to enable live refreshes of creatives.

## Available Endpoints

- `GET /api/categories` – List categories with publisher counts.
- `GET /api/categories/{category_id}/publishers` – Publishers assigned to a category.
- `GET /api/categories/{category_id}/ads` – Cached creatives for publishers in a category.
- `POST /api/admin/publishers` – Create a new publisher.
- `PUT /api/admin/publishers/{publisher_id}` – Update publisher metadata or assignments.
- `DELETE /api/admin/publishers/{publisher_id}` – Archive a publisher while retaining history.

## Tests

Run the API test suite with:

```bash
pytest
```

Or simply:

```bash
make test
```

For a one-command local verification that ensures dependencies are installed and then executes the pytest suite, run:

```bash
./scripts/verify.sh
```

Or invoke the `Makefile` proxy:

```bash
make verify
```

## Additional Documentation

- [Meta Ad Library Context](docs/meta-ad-library-overview.md)
- [Publisher Administration Guide](docs/admin-publisher-management.md)
