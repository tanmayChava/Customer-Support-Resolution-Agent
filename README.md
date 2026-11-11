# Customer Support Resolution Agent

An AI-assisted, human-in-the-loop workflow that takes a customer complaint from
"What happened?" to "Here's the verified outcome."

The agent retrieves business data, resolves support policy, proposes a resolution,
waits for human approval, executes the approved action, verifies the result, and
updates the support ticket without claiming more than the APIs confirmed.

## Status

Scaffold only. The repository skeleton and project metadata are in place. The
API, LangGraph workflow, database schema, mock services, UI, and evaluation
suite are the next implementation steps.

## Supported complaint types

- **Order status** — retrieve the order and shipment status, explain the latest
  available information, and update the ticket.
- **Refund request** — check eligibility, prepare a proposal, obtain approval,
  execute the refund, and verify the result.
- **Damaged item** — retrieve the order and policy, collect required evidence,
  prepare a resolution, or escalate.

## Architecture

| Component | Responsibility |
|---|---|
| **FastAPI** | Authentication, ticket API, reviewer decisions, workflow control, request/response validation, demo UI |
| **LangGraph** | Classification, investigation, policy retrieval, proposal creation, approval pauses, execution, verification, escalation |
| **PostgreSQL** | Application data and durable LangGraph checkpoints in a separate schema |
| **Mock services** | Payment/refund, shipping, and ticketing APIs with realistic errors and delayed results |

### Repository layout

```text
app/
  api/          HTTP routes and request/response handling
  auth/         Sessions, roles, and password handling
  schemas/      Pydantic request, response, and workflow models
  agents/       LLM adapters, prompts, and structured outputs
  workflows/    LangGraph graph, nodes, interrupts, and routing
  tools/        Typed clients for orders, shipping, payments, ticketing, and policies
  services/     Ticket, proposal, approval, refund, and policy services
  policies/     Deterministic policy rules, retrieval, and pgvector integration
  db/           SQLAlchemy models, sessions, and repositories
  templates/    Jinja/HTMX demo UI
  static/       UI assets
mock_services/
  payments/     Mock payment and refund API
  shipping/     Mock shipment API
  ticketing/    Mock ticketing API
  common/       Shared mock state and fault-injection helpers
migrations/     Alembic migrations for the application schema only
scripts/        Seed data and policy ingestion
evals/          Evaluation datasets, runner, and reports
tests/          Unit, integration, and failure-scenario tests
docs/           Architecture, API, runbook, and ADRs
```

## Core safety invariants

- Every refund requires a human approval bound to the exact proposal version and amount.
- Refund execution is idempotent.
- The system re-validates eligibility immediately before execution.
- The final customer message distinguishes between **submitted**, **confirmed**,
  **failed**, and **unknown** outcomes.
- Customer identity always comes from the authenticated session, never from
  request input.
- Application tables and LangGraph checkpoints live in separate schemas.

## Planned local workflow

Prerequisites: Python 3.11+, `uv`, and Docker.

```bash
cp .env.example .env
docker compose up -d postgres
uv sync
uv run alembic upgrade head
uv run python scripts/seed_data.py
uv run python scripts/ingest_policies.py
uv run uvicorn app.main:app --reload
```

> These commands become fully functional as the implementation lands.

## Scope for v1

- One store and one currency.
- One customer issue per workflow.
- Human approval for every refund.
- Mock shipping and payment services.
- Customer messaging stays inside the demo interface.
- Chargebacks, fraud adjudication, and complex partial returns are out of scope
  and must be escalated.
