"""MCP server for VictoriaLogs and VictoriaTraces."""

import asyncio
import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# VictoriaLogs and VictoriaTraces URLs from environment
VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")

server = Server("mcp-obs")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available observability tools."""
    return [
        Tool(
            name="logs_search",
            description="Search logs by keyword and/or time range. Use LogsQL query syntax. Example: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "LogsQL query string (e.g., '_time:1h severity:ERROR')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of log entries to return",
                        "default": 10
                    }
                },
                "required": ["query"]
            },
        ),
        Tool(
            name="logs_error_count",
            description="Count errors per service over a time window. Returns error counts grouped by service name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "time_range": {
                        "type": "string",
                        "description": "Time range for the query (e.g., '1h', '10m', '24h')",
                        "default": "1h"
                    }
                }
            },
        ),
        Tool(
            name="traces_list",
            description="List recent traces for a service from VictoriaTraces. Returns trace IDs and metadata.",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {
                        "type": "string",
                        "description": "Service name to filter traces (e.g., 'Learning Management Service')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of traces to return",
                        "default": 10
                    }
                },
                "required": ["service"]
            },
        ),
        Tool(
            name="traces_get",
            description="Fetch a specific trace by ID from VictoriaTraces. Returns full span hierarchy and error details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {
                        "type": "string",
                        "description": "The trace ID to fetch (e.g., '8c65efae0391e69531561e2e272b2361')"
                    }
                },
                "required": ["trace_id"]
            },
        ),
    ]


async def _query_victorialogs(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Query VictoriaLogs using the logsql API."""
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"query": query, "limit": limit},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json() if response.text else []


async def _query_victoriatraces_traces(service: str, limit: int = 10) -> dict[str, Any]:
    """Query VictoriaTraces for a service using Jaeger-compatible API."""
    url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces"
    params = {"service": service, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json() if response.text else {"data": []}


async def _get_trace_by_id(trace_id: str) -> dict[str, Any]:
    """Fetch a specific trace by ID."""
    url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.json() if response.text else {"data": []}


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name == "logs_search":
        query = arguments.get("query", "_time:1h")
        limit = arguments.get("limit", 10)
        results = await _query_victorialogs(query, limit)
        return [TextContent(type="text", text=f"Logs search results:\n{results}")]

    elif name == "logs_error_count":
        time_range = arguments.get("time_range", "1h")
        query = f"_time:{time_range} severity:ERROR"
        results = await _query_victorialogs(query, 100)
        
        # Count errors by service
        error_counts: dict[str, int] = {}
        if isinstance(results, list):
            for entry in results:
                if isinstance(entry, dict):
                    labels = entry.get("_stream", {})
                    service = labels.get("service.name", "unknown")
                    error_counts[service] = error_counts.get(service, 0) + 1
        
        summary = "\n".join([f"  {svc}: {count} errors" for svc, count in sorted(error_counts.items(), key=lambda x: -x[1])])
        if not summary:
            summary = "  No errors found"
        return [TextContent(type="text", text=f"Error count for last {time_range}:\n{summary}")]

    elif name == "traces_list":
        service = arguments.get("service", "Learning Management Service")
        limit = arguments.get("limit", 10)
        results = await _query_victoriatraces_traces(service, limit)
        
        traces = results.get("data", [])
        if not traces:
            return [TextContent(type="text", text=f"No traces found for service: {service}")]
        
        summary_lines = [f"Found {len(traces)} traces for '{service}':"]
        for trace in traces[:limit]:
            trace_id = trace.get("traceID", "unknown")
            spans = trace.get("spans", [])
            span_count = len(spans)
            # Find root span for operation name
            root_span = next((s for s in spans if not s.get("references")), None)
            operation = root_span.get("operationName", "unknown") if root_span else "unknown"
            summary_lines.append(f"  - {trace_id}: {operation} ({span_count} spans)")
        
        return [TextContent(type="text", text="\n".join(summary_lines))]

    elif name == "traces_get":
        trace_id = arguments.get("trace_id")
        if not trace_id:
            return [TextContent(type="text", text="Error: trace_id is required")]
        
        results = await _get_trace_by_id(trace_id)
        traces = results.get("data", [])
        
        if not traces:
            return [TextContent(type="text", text=f"No trace found with ID: {trace_id}")]
        
        trace = traces[0]
        spans = trace.get("spans", [])
        
        # Build span hierarchy summary
        root_span = next((s for s in spans if not s.get("references")), None)
        if not root_span:
            root_span = spans[0] if spans else None
        
        if not root_span:
            return [TextContent(type="text", text=f"Trace {trace_id} has no spans")]
        
        summary_lines = [
            f"Trace: {trace_id}",
            f"Root operation: {root_span.get('operationName', 'unknown')}",
            f"Total spans: {len(spans)}",
            "",
            "Span hierarchy:"
        ]
        
        # Check for errors
        error_spans = [s for s in spans if any(
            tag.get("key") == "error" and tag.get("value") is True
            for tag in s.get("tags", [])
        )]
        
        if error_spans:
            summary_lines.append("  ⚠️ ERRORS FOUND:")
            for es in error_spans:
                error_msg = "Unknown error"
                for tag in es.get("tags", []):
                    if tag.get("key") == "otel.status_description":
                        error_msg = tag.get("value", "Unknown")
                        break
                summary_lines.append(f"    - {es.get('operationName', 'unknown')}: {error_msg}")
        
        # List all spans with duration
        for span in spans:
            duration_us = span.get("duration", 0)
            duration_ms = duration_us / 1000
            indent = "  "
            if span.get("references"):
                indent = "    "
            status = ""
            for tag in span.get("tags", []):
                if tag.get("key") == "http.status_code":
                    status = f" [HTTP {tag.get('value')}]"
                elif tag.get("key") == "error" and tag.get("value") is True:
                    status = " [ERROR]"
            summary_lines.append(f"{indent}- {span.get('operationName', 'unknown')} ({duration_ms:.1f}ms){status}")
        
        return [TextContent(type="text", text="\n".join(summary_lines))]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


def main() -> None:
    """Run the MCP server."""
    asyncio.run(server.run(stdio_server()))


if __name__ == "__main__":
    main()
