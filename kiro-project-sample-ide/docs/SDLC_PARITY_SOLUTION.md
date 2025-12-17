# SDLC Parity Solution for Kiro IDE

**Date**: 2025-12-17
**Goal**: Achieve feature parity between Claude Code's `.claude/` SDLC and Kiro IDE's `.kiro/` SDLC

## Problem Statement

Claude Code has a plugin/agent/skill/command architecture that enables automated SDLC orchestration through the `/sdlc` command. Kiro IDE lacks these concepts, resulting in:

1. No `/sdlc` command
2. No automatic plugin execution
3. No automatic agent delegation
4. Manual phase orchestration required

## Proposed Solution: Custom MCP Server

Create a **`kiro-sdlc-mcp`** server that provides SDLC orchestration tools, achieving parity with Claude Code's capabilities.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Kiro IDE                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Official Kiro Features:                                     │
│  ├── .kiro/steering/     (Context)                          │
│  ├── .kiro/specs/        (Via spec-workflow MCP)            │
│  └── .kiro/settings/     (MCP config)                       │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Custom MCP Server: kiro-sdlc-mcp                           │
│  ├── sdlc_start         → Start SDLC workflow              │
│  ├── sdlc_next_phase    → Progress to next phase           │
│  ├── sdlc_status        → Get current phase status         │
│  ├── run_plugin         → Execute phase plugin             │
│  ├── spawn_agent        → Delegate to specialized agent    │
│  ├── execute_skill      → Run skill with scripts           │
│  └── get_phase_guide    → Get phase instructions           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## MCP Server Implementation

### Server Structure

```
kiro-sdlc-mcp/
├── package.json
├── src/
│   ├── index.ts              # MCP server entry point
│   ├── tools/
│   │   ├── sdlc.ts           # SDLC orchestration tools
│   │   ├── plugins.ts        # Plugin execution tools
│   │   ├── agents.ts         # Agent spawning tools
│   │   └── skills.ts         # Skill execution tools
│   ├── state/
│   │   └── workflow-state.ts # Track SDLC progress
│   └── utils/
│       ├── file-reader.ts    # Read phase/plugin docs
│       └── executor.ts       # Execute commands
└── README.md
```

### MCP Tools Provided

#### 1. SDLC Orchestration Tools

**`sdlc_start`**
```typescript
{
  name: "sdlc_start",
  description: "Start SDLC workflow for a feature",
  inputSchema: {
    feature_name: string,
    start_phase?: number  // Default: 1 (SPEC)
  }
}
```
- Creates workflow state
- Loads phase 1 (SPEC) guidance from `.kiro/steering/phases/01-spec.md`
- Returns instructions for spec phase

**`sdlc_next_phase`**
```typescript
{
  name: "sdlc_next_phase",
  description: "Progress to next SDLC phase",
  inputSchema: {
    feature_name: string
  }
}
```
- Validates current phase completion
- Moves to next phase
- Returns next phase instructions

**`sdlc_status`**
```typescript
{
  name: "sdlc_status",
  description: "Get current SDLC workflow status",
  inputSchema: {
    feature_name: string
  }
}
```
- Returns current phase, completed phases, next steps

#### 2. Plugin Execution Tools

**`run_plugin`**
```typescript
{
  name: "run_plugin",
  description: "Execute an SDLC phase plugin",
  inputSchema: {
    plugin_name: string,  // "spec-writer", "test-writer", etc.
    feature_name: string,
    context?: object
  }
}
```
- Reads plugin instructions from `docs/sdlc-framework/plugins/{plugin}.md`
- Executes plugin logic (calls AI with plugin context)
- Returns plugin results

#### 3. Agent Spawning Tools

**`spawn_agent`**
```typescript
{
  name: "spawn_agent",
  description: "Delegate to specialized agent",
  inputSchema: {
    agent_type: string,  // "test-engineer", "security-auditor", etc.
    task: string,
    context?: object
  }
}
```
- Reads agent instructions from `docs/sdlc-framework/agents/{agent}.md`
- Uses Task tool to spawn agent with specialized context
- Returns agent results

#### 4. Skill Execution Tools

**`execute_skill`**
```typescript
{
  name: "execute_skill",
  description: "Execute a skill with supporting scripts",
  inputSchema: {
    skill_name: string,  // "code-reviewer", "documentation-generator"
    target: string,      // File or directory to process
    options?: object
  }
}
```
- Reads skill instructions from `docs/sdlc-framework/skills/{skill}/`
- Executes supporting Python scripts if available
- Returns skill results

#### 5. Phase Guide Tools

**`get_phase_guide`**
```typescript
{
  name: "get_phase_guide",
  description: "Get guidance for a specific SDLC phase",
  inputSchema: {
    phase: number  // 1-6
  }
}
```
- Returns content from `.kiro/steering/phases/0{phase}-*.md`

## Implementation Steps

### Step 1: Create MCP Server Package

```bash
cd kiro-project-sample-ide
mkdir -p mcp-servers/kiro-sdlc-mcp
cd mcp-servers/kiro-sdlc-mcp

npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node tsx

# Create TypeScript config
npx tsc --init --target ES2022 --module NodeNext --moduleResolution NodeNext
```

### Step 2: Implement Core Server

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new Server(
  {
    name: "kiro-sdlc-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Register tools
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "sdlc_start",
        description: "Start SDLC workflow",
        inputSchema: {
          type: "object",
          properties: {
            feature_name: { type: "string" },
            start_phase: { type: "number", default: 1 }
          },
          required: ["feature_name"]
        }
      },
      // ... other tools
    ]
  };
});

// Tool handlers
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "sdlc_start":
      return handleSdlcStart(args);
    case "sdlc_next_phase":
      return handleSdlcNextPhase(args);
    // ... other handlers
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Step 3: Implement Workflow State

```typescript
// src/state/workflow-state.ts
interface WorkflowState {
  feature_name: string;
  current_phase: number;
  completed_phases: number[];
  started_at: string;
  phase_artifacts: Record<number, string[]>;
}

export class WorkflowStateManager {
  private state_dir = ".kiro/state";

  async createWorkflow(feature_name: string): Promise<WorkflowState> {
    // Create state file
    const state: WorkflowState = {
      feature_name,
      current_phase: 1,
      completed_phases: [],
      started_at: new Date().toISOString(),
      phase_artifacts: {}
    };

    await fs.writeFile(
      `${this.state_dir}/${feature_name}.json`,
      JSON.stringify(state, null, 2)
    );

    return state;
  }

  async getWorkflow(feature_name: string): Promise<WorkflowState | null> {
    // Load state file
  }

  async updatePhase(feature_name: string, phase: number): Promise<void> {
    // Update phase in state
  }
}
```

### Step 4: Register in Kiro

```json
// .kiro/settings/mcp.json
{
  "mcpServers": {
    "kiro-sdlc": {
      "command": "node",
      "args": ["./mcp-servers/kiro-sdlc-mcp/dist/index.js"],
      "env": {
        "PROJECT_PATH": "${workspaceFolder}"
      },
      "disabled": false,
      "autoApprove": [
        "sdlc_start",
        "sdlc_status",
        "get_phase_guide"
      ],
      "disabledTools": []
    },
    "spec-workflow": { /* existing */ },
    "docs-mcp-server": { /* existing */ },
    "context7": { /* existing */ }
  }
}
```

## Usage in Kiro IDE

### Start SDLC Workflow

```
User: "Start SDLC workflow for user authentication feature"

Claude (via MCP):
> Using tool: sdlc_start
> Arguments: { feature_name: "user-authentication" }

Response:
✅ SDLC workflow started for "user-authentication"
📍 Current Phase: 1 - SPEC (Requirements & Design)

Next Steps:
1. Create requirements.md with EARS notation
2. Design data models and API contracts
3. Create tasks.md with implementation plan

Would you like me to help with the requirements?
```

### Automatic Phase Progression

```
User: "Requirements and design are complete, move to next phase"

Claude (via MCP):
> Using tool: sdlc_next_phase
> Arguments: { feature_name: "user-authentication" }

Response:
✅ Phase 1 (SPEC) marked complete
🚀 Moving to Phase 2 - TEST (TDD)

Next Steps:
1. Create test files following design
2. Write tests for success scenarios
3. Write tests for error scenarios
4. Run tests to verify they fail (Red phase)

Loading test-engineer agent to help with test creation...
```

### Agent Delegation

```
User: "Write comprehensive tests"

Claude (via MCP):
> Using tool: spawn_agent
> Arguments: {
>   agent_type: "test-engineer",
>   task: "Write unit tests for user authentication",
>   context: { spec: "user-authentication" }
> }

[Test engineer agent creates tests following TDD patterns]
```

## Hooks Integration

Configure in Agent Hooks Panel:

### Hook 1: Auto-Progress on Phase Completion
```yaml
Name: SDLC Phase Auto-Progress
Trigger: Manual (after marking phase complete)
Action:
  Use sdlc_next_phase tool to progress to next phase
  Load next phase guidance
  Show next steps
```

### Hook 2: Build Quality Gate
```yaml
Name: Build Quality Gate
Trigger: File Save (src/**/*.py)
Action:
  Run make build
  If failures: show errors
  If success: check if phase 4 complete
```

### Hook 3: Security Scan
```yaml
Name: Security Scan
Trigger: File Save (src/**/*.py)
Action:
  Run make quality-gate
  Report vulnerabilities
```

## Benefits

1. **Parity with Claude Code**: `/sdlc` equivalent via MCP tools
2. **Automated Orchestration**: Phase-to-phase progression
3. **Agent Delegation**: Specialized agents via `spawn_agent`
4. **Skill Execution**: Skills with scripts via `execute_skill`
5. **State Tracking**: Workflow progress persisted
6. **Native Integration**: Uses official Kiro MCP protocol

## Alternative Solutions

### Option 2: Enhanced Steering Documents

- Add better orchestration logic in steering docs
- Use conditional inclusion for phase-specific guidance
- **Pros**: No custom code needed
- **Cons**: Still requires manual phase transitions

### Option 3: Hooks-Only Approach

- Configure all automation via Kiro IDE hooks
- Use hooks to trigger phase progressions
- **Pros**: No MCP server needed
- **Cons**: Limited to UI-triggered actions

### Option 4: Hybrid Approach

- MCP for orchestration + complex tasks
- Hooks for automatic quality gates
- Steering for guidance
- **Pros**: Best of all worlds
- **Cons**: More complex setup

## Recommendation

**Implement Option 1 (Custom MCP Server) + Option 4 (Hooks for quality gates)**

This provides the closest parity to Claude Code's architecture while leveraging Kiro's strengths.

## Next Steps

1. Build `kiro-sdlc-mcp` server
2. Test SDLC orchestration tools
3. Configure hooks for quality gates
4. Document usage and setup
5. Create example workflow walkthrough
