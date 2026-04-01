# mcp-obs

MCP server for observability tools (VictoriaLogs and VictoriaTraces).

## Tools

- `logs_search` — Search logs by keyword and/or time range
- `logs_error_count` — Count errors per service over a time window
- `traces_list` — List recent traces for a service
- `traces_get` — Fetch a specific trace by ID

## Environment Variables

- `NANOBOT_VICTORIALOGS_URL` — VictoriaLogs base URL (default: `http://victorialogs:9428`)
- `NANOBOT_VICTORIATRACES_URL` — VictoriaTraces base URL (default: `http://victoriatraces:10428`)

## Usage

```bash
python -m mcp_obs
```
