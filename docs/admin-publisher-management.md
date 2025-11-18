# Publisher Administration Guide

This guide outlines how administrators can manage Real Money Gaming publishers and their category assignments within the LiveFBAds platform.

## Goals
- Allow authorized administrators to add, update, or remove publisher records without deploying new code.
- Maintain an auditable history of changes to publisher/category mappings.
- Enforce business rules (e.g., Real Money Gaming publishers must operate in the United States).

## User Roles
- **Administrator** – Full read/write access to publisher records, categories, and assignments.
- **Viewer** – Read-only access to the catalog of publishers and categories.

## Data Model Implications
- Extend the data model described in `meta-ad-library-overview.md` with tables/entities:
  - `administrators`: stores user accounts permitted to manage publisher data.
  - `publisher`: includes `id`, `name`, `status`, `country`, `notes`, `created_at`, `updated_at`.
  - `publisher_category`: join table linking publishers to one or more categories.
  - `audit_log`: captures changes to publisher records (actor, action, payload diff, timestamp).

## API Requirements
- Secure endpoints (`/api/admin/publishers`) protected by authentication middleware.
- CRUD operations are implemented in the FastAPI service:
  - `POST /api/admin/publishers` – create a publisher with assigned categories.
  - `PUT /api/admin/publishers/{id}` – update publisher fields or category assignments.
  - `DELETE /api/admin/publishers/{id}` – soft delete a publisher, preserving historical creatives.
  - `GET /api/categories/{id}/publishers` – surface publisher lists for public consumption.
- Extend payloads to capture a change reason for audit logging in future iterations.
- Return validation errors if publishers are assigned to unsupported categories or non-US regions.

## Admin UI Considerations
- Add an "Admin" section to the web application accessible only to administrators.
- Provide forms for adding/editing publishers, including:
  - Publisher name
  - Country (default to United States)
  - Status (Active/Inactive)
  - Category multi-select
  - Notes field for compliance context
- Display a table of existing publishers with quick actions (Edit, Archive, Reactivate).
- Include an audit log view showing recent changes with user, date, and summary.

## Workflow for Adding Publishers
1. Administrator opens the Admin panel and selects "Add Publisher".
2. Fill out required fields and choose one or more categories.
3. Submit the form; backend validates and creates the record, storing an audit entry.
4. Newly added publisher becomes eligible for ingestion in the next Meta API sync.

## Workflow for Removing Publishers
1. Administrator selects a publisher and chooses "Archive" or "Remove".
2. Backend performs a soft delete (status set to Inactive) to retain historical data.
3. Audit log stores the action with metadata and optional notes.
4. Ingestion jobs skip inactive publishers automatically.

## Permissions & Security
- Protect admin endpoints with OAuth or SSO integration; sessions must expire and require MFA per company policy.
- Rate-limit admin operations and log all failed authentication attempts.
- Ensure CSRF protection on admin forms.

## Testing & Monitoring
- Implement integration tests covering CRUD flows and audit logging behavior.
- Add metrics for admin actions (count of additions, removals, edits) to monitor operational activity.

