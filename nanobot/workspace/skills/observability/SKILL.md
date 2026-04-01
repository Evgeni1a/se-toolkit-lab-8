# Observability Skill

You have access to observability tools that can query VictoriaLogs and VictoriaTraces. Use these when the user asks about errors, system health, or what went wrong.

## Tools available

- `logs_search` — Search logs by keyword and/or time range. Use LogsQL query syntax.
- `logs_error_count` — Count errors per service over a time window.
- `traces_list` — List recent traces for a service.
- `traces_get` — Fetch a specific trace by ID.

## How to answer observability questions

### When asked about errors

1. First call `logs_error_count` with an appropriate time range (e.g., "10m" for last 10 minutes) to see if there are recent errors.

2. If errors exist, call `logs_search` with a query like:
   ```
   _time:10m service.name:"Learning Management Service" severity:ERROR
   ```

3. If you find a `trace_id` in the log results, call `traces_get` with that ID to see the full request flow and error details.

4. Summarize findings concisely:
   - How many errors found
   - Which service failed
   - What the error was
   - When it happened
   - Root cause if you found a trace

### When asked about system health

1. Call `logs_error_count` with time_range="10m" to check for recent errors.

2. If no errors: "No errors found in the last 10 minutes. The system is healthy."

3. If errors exist: Report the count and affected services, then offer to investigate further.

## Example queries

**Check for LMS backend errors in last 10 minutes:**
```
logs_error_count(time_range="10m")
```

**Search LMS error logs:**
```
logs_search(query='_time:10m service.name:"Learning Management Service" severity:ERROR', limit=10)
```

**Get full trace details:**
```
traces_get(trace_id="8c65efae0391e69531561e2e272b2361")
```

## Response format

- Keep responses concise — don't dump raw JSON
- Highlight errors with ⚠️ or ❌
- Show healthy status with ✅
- Include timestamps when available
- Explain what the error means in plain language
