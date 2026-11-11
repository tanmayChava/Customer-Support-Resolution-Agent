# Architecture

## Components

### FastAPI application

The only public entry point. It owns:

- Customer requests.
- Authentication and authorization.
- Ticket creation.
- Workflow creation and status queries.
- Reviewer decisions.
- Input and response validation.
- The Jinja/HTMX demo interface.

### LangGraph workflow

Coordinates the resolution lifecycle:

```text
classify
  -> investigate
  -> retrieve policy
  -> evaluate eligibility
  -> propose resolution
  -> pause for human approval
  -> validate
  -> execute refund (if approved)
  -> verify result
  -> update ticket
  -> close or escalate
```

The graph uses a durable Postgres checkpointer. `thread_id` is the workflow run
ID. Approval and missing-evidence pauses use LangGraph interrupts.

### PostgreSQL

The application schema stores customers, orders, returns, tickets, policies,
proposals, approvals, refund operations, and audit events.

LangGraph checkpoint tables live in a separate `langgraph` schema. Alembic
manages only the application schema.

### Mock external services

Separate FastAPI applications simulate:

- Payment and refund API.
- Shipping API.
- Ticketing API.

Each service supports deterministic seeded state, reset, error injection, and
delayed or pending responses so failure paths can be tested.

## Safety invariants

1. Customer identity comes from the authenticated session, never request input.
2. Every refund requires an approval record bound to the proposal version and amount.
3. Refund execution is idempotent.
4. Eligibility is re-validated immediately before execution.
5. Verification is a separate step from execution.
6. Customer messages distinguish submitted, confirmed, failed, and unknown outcomes.
7. Out-of-scope issues are escalated, not resolved by the agent.

## Policy handling

Structured policy rules drive eligibility. The LLM may classify the complaint
and draft explanations, but it does not decide eligibility. Policy chunks and
optional pgvector embeddings provide citations and supporting text.
