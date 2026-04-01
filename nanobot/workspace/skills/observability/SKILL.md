# Observability Skill

You have access to observability tools that can query VictoriaLogs and VictoriaTraces. Use these when the user asks about errors, system health, or "what went wrong".

## Tools available

- `logs_search` — Search logs by keyword and/or time range. Use LogsQL query syntax.
- `logs_error_count` — Count errors per service over a time window.
- `traces_list` — List recent traces for a service.
- `traces_get` — Fetch a specific trace by ID.

## When the user asks "What went wrong?" or "Check system health"

Follow this investigation flow:

### Step 1: Check error count first
Call `logs_error_count` with a fresh recent window (e.g., "10m" or "30m"):
```
logs_error_count(time_range="10m")
```

### Step 2: Search error logs
If errors exist, call `logs_search` scoped to the LMS backend:
```
logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR', limit=5)
```

Look for:
- `trace_id` in the log entries
- `event` field (e.g., "db_query", "unhandled_exception")
- `error` or `exception.message` fields

### Step 3: Fetch the matching trace
Extract a `trace_id` from the logs and call:
```
traces_get(trace_id="<extracted_trace_id>")
```

The trace shows:
- Span hierarchy (which operations ran)
- Which span has `error: true`
- The actual error message in `otel.status_description`
- HTTP status codes (404 vs 500)

### Step 4: Summarize findings concisely

Your response must include:

1. **Log evidence**: Quote the error event, timestamp, and error message from logs
2. **Trace evidence**: Name the failing span and the root operation
3. **The discrepancy**: If logs show a database error but HTTP status is 404, point this out
4. **Root cause**: Name the affected service and the failing operation

Example summary format:
```
I found the issue. Here's what went wrong:

**Log evidence:**
- At 14:41:18, the Learning Management Service logged a db_query ERROR
- Error: "connection is closed" (asyncpg InterfaceError)
- Operation: SELECT on the item table

**Trace evidence:**
- Trace ID: c0587e52cda2752a12db669f2577bdf7
- The SELECT span failed with error: "connection is closed"
- HTTP response was 404 (should be 500 for a database error)

**Root cause:**
The PostgreSQL database connection was closed. The backend's /items/ route
caught the database exception but returned 404 "Items not found" instead of
a proper 500 error. This is a misreporting bug — the real issue is database
connectivity, not missing items.
```

## Response format rules

- **NEVER dump raw JSON** — extract and explain the key fields
- Use ✅ for healthy components, ❌ or ⚠️ for failures
- Include timestamps from the logs
- Name the specific span that failed
- Point out any discrepancy between the actual error and the HTTP status
