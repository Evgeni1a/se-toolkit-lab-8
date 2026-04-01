# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Q: What is the agentic loop?**

The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It typically consists of these core stages:

1. **Perceive** — Gather information from the environment (user input, files, APIs, sensors, etc.)
2. **Reason/Plan** — Analyze the information, determine goals, and decide on a course of action
3. **Act** — Execute actions using available tools (file operations, API calls, code execution, etc.)
4. **Observe** — Receive feedback from the actions taken (outputs, errors, state changes)
5. **Reflect/Iterate** — Evaluate results, adjust the plan if needed, and continue the loop until the goal is achieved

This loop enables agents to handle complex, multi-step tasks, adapt to unexpected outcomes, learn from feedback, and work autonomously toward goals.

**Q: What labs are available in our LMS?**

Based on the agent's exploration of the workspace:

- **Current Lab: Lab 8** (repository: se-toolkit-lab-8)
- **Lab Structure:**
  - Required Tasks: Task 1, Task 2, Task 3, Task 4, Task 5
  - Optional Tasks: Task 1
- **Wiki Documentation:** Lab 1 documentation exists at `/root/se-toolkit-lab-8/wiki/lab-1/`, suggesting the LMS contains multiple labs (Lab 1 through Lab 8)
- **Topics covered:** Git workflow, Docker & Docker Compose, PostgreSQL database, Python/Node.js development, REST APIs, Web development (React frontend), Linux administration, and more

Note: The agent inspected local repo files to answer — it does NOT have live LMS backend access yet (that comes in Part B with the MCP server).

## Task 1B — Agent with LMS tools

**Q: What labs are available?**

The agent now uses the MCP server to fetch real data from the LMS backend:

```
Here are the available labs:
1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08
```

The MCP server registered 9 tools: `lms_health`, `lms_labs`, `lms_learners`, `lms_pass_rates`, `lms_timeline`, `lms_groups`, `lms_top_learners`, `lms_completion_rate`, `lms_sync_pipeline`.

**Q: Is the LMS backend healthy?**

```
Yes, the LMS backend is healthy! It's currently tracking 56 items.
```

**Q: Which lab has the lowest pass rate?**

The agent chained multiple tool calls to answer:

```
Based on the completion rates:

 Lab     Completion Rate  Passed  Total
 ──────────────────────────────────────
 Lab 01  100.0%           258     258
 Lab 02  89.1%            131     147
 Lab 03  89.1%            156     175
 Lab 04  97.2%            239     246
 Lab 05  98.8%            247     250
 Lab 06  98.4%            242     246
 Lab 07  99.6%            238     239
 Lab 08  0.0%             0       0

Lab 08 has the lowest pass rate at 0.0%, but this appears to be because no students have attempted it yet (0 total submissions).

Among labs with actual submissions, Lab 02 and Lab 03 are tied for the lowest pass rate at 89.1%.
```

**Q: Describe the architecture of the LMS system**

The agent used multiple MCP tools to explore and describe the system:

**Core Components:**
- **Labs** - 8 course modules (Lab 01-08), each with multiple tasks
- **Learners** - 258 registered students organized into groups (e.g., B25-CSE-01, B25-DSAI-05)
- **Tasks** - Individual assignments within labs, tracking scores and attempt counts

**MCP Tools (9 total):**
| Tool | Purpose |
|------|---------|
| `lms_health` | System health check + item count |
| `lms_labs` | List all available labs |
| `lms_learners` | List all registered students |
| `lms_pass_rates` | Get avg score & attempts per task for a lab |
| `lms_completion_rate` | Get pass/fail statistics for a lab |
| `lms_groups` | Get performance breakdown by student group |
| `lms_timeline` | Get submission history by date |
| `lms_top_learners` | Get highest-performing students |
| `lms_sync_pipeline` | Trigger data synchronization |

**Analytics Capabilities:**
- Performance Tracking: Average scores, attempt counts per task
- Completion Metrics: Pass rates (passed/total students)
- Group Analysis: Performance comparison across student groups
- Timeline Analysis: Submission patterns over time
- Leaderboards: Top performers by average score

**Architecture Pattern:** Service-oriented architecture where the LMS backend manages all educational data, and MCP tools provide a standardized interface for AI agents to query and interact with the system.

## Task 1C — Skill prompt

**Q: Show me the scores** (without specifying a lab)

The agent now follows the LMS skill strategy — it fetches available labs first and asks the user to choose:

```
I'll help you view the scores. First, let me check what labs are available in the LMS.

I can see there are 8 labs available. To show you the scores, I need to know which lab you're interested in. Here are the options:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

Which lab would you like to see the scores for? Or would you like me to show scores for all labs?
```

**Skill file created:** `nanobot/workspace/skills/lms/SKILL.md`

The skill teaches the agent to:
- Call `lms_labs` first when the user requests lab-specific data without naming a lab
- Present lab choices to the user before calling tools that require a `lab` parameter
- Use each lab's title as the user-facing label
- Format numeric results as percentages and keep responses concise

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
