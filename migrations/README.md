# Migrations

Alembic manages the application schema only.

LangGraph checkpoint tables are created separately by
`AsyncPostgresSaver.setup()` in the `langgraph` schema. Do not add checkpoint
tables to Alembic migrations.
