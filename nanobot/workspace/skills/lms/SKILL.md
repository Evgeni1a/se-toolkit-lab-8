---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to fetch live course data from the backend.

## Available Tools

- `lms_health` — Check if the LMS backend is healthy (returns item count)
- `lms_labs` — List all available labs (no parameters needed)
- `lms_learners` — List all registered learners (no parameters needed)
- `lms_pass_rates` — Get avg score & attempts per task for a specific lab (requires `lab`)
- `lms_completion_rate` — Get pass/fail stats for a specific lab (requires `lab`)
- `lms_groups` — Get performance breakdown by student group for a specific lab (requires `lab`)
- `lms_timeline` — Get submission history by date for a specific lab (requires `lab`)
- `lms_top_learners` — Get top performers by avg score for a specific lab (requires `lab`, optional `limit`)
- `lms_sync_pipeline` — Trigger data synchronization (no parameters needed)

## Strategy

### When user asks for lab-specific data without naming a lab

If the user asks for scores, pass rates, completion, groups, timeline, or top learners **without specifying a lab**:

1. Call `lms_labs` first to get the list of available labs
2. Use `mcp_webchat_ui_message` with `type: "choice"` to present lab options to the user
3. Wait for the user to select a lab before calling the requested tool

### Lab choice presentation

- Call `lms_labs` to fetch available labs
- Build a choice UI where each option uses:
  - `label`: the lab's `title` field (short, user-friendly name)
  - `value`: the lab's `id` field (stable identifier for follow-up tool calls)
- Use `mcp_webchat_ui_message` with `type: "choice"` to send the choice UI
- Read the `chat_id` from runtime context and pass it so the payload routes to the active WebSocket client
- Wait for user selection; the selected `value` becomes the `lab` parameter for subsequent tool calls

### When user asks "what can you do?"

Explain that you can:
- Check LMS backend health
- List available labs and learners
- Show pass rates, completion rates, and group performance for any lab
- Display submission timelines and top performers
- Trigger data synchronization

Be clear about what information you need (e.g., "Which lab would you like to see?")
