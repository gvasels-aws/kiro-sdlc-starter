# Kiro CLI SDLC Replication - Design

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              KIRO CLI                                          │
├───────────────────────────────────────────────────────────────────────────────┤
│                          COMMAND PARSER                                        │
│  kiro sdlc [options]                                                          │
│                                                                                │
│  Subcommands:                                                                  │
│    sdlc              Run SDLC workflow                                        │
│    sdlc status       Check spec status                                        │
│    sdlc resume       Resume from last phase                                   │
│                                                                                │
│  Options:                                                                      │
│    --interactive, -i    Interactive mode (default)                            │
│    --headless           Headless/non-interactive mode                         │
│    --spec <name>        Spec name to use/create                               │
│    --phase <1-6>        Start from specific phase                             │
│    --dry-run            Preview without executing                             │
│    --verbose, -v        Verbose output                                        │
│    --output <format>    Output format (human, json, quiet)                    │
│    --config <path>      Path to config file                                   │
│    --help, -h           Show help                                             │
├───────────────────────────────────────────────────────────────────────────────┤
│                          MODE HANDLER                                          │
│  ┌────────────────────────────┐     ┌────────────────────────────┐           │
│  │     INTERACTIVE MODE       │     │      HEADLESS MODE         │           │
│  │  • User prompts            │     │  • No prompts              │           │
│  │  • Phase confirmations     │     │  • Batch execution         │           │
│  │  • Progress spinners       │     │  • Log output              │           │
│  │  • Error recovery prompts  │     │  • Exit codes              │           │
│  └────────────────────────────┘     └────────────────────────────┘           │
├───────────────────────────────────────────────────────────────────────────────┤
│                       SPEC-WORKFLOW MCP INTEGRATION                            │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐ │
│  │ spec-workflow-  │ │ spec-status     │ │ approvals       │ │ log-        │ │
│  │ guide           │ │                 │ │                 │ │ implementation│
│  │ (Phase 1)       │ │ (Status check)  │ │ (Transitions)   │ │ (Tracking)  │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────┘ │
├───────────────────────────────────────────────────────────────────────────────┤
│                          PHASE EXECUTOR                                        │
│  • Uses same steering documents as IDE                                        │
│  • Executes tools (ruff, bandit, pytest) via subprocess                       │
│  • Reports progress/results                                                    │
│  • Handles phase transitions and prerequisites                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

## Command Flow Diagrams

### Interactive Mode Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  $ kiro sdlc                                                     │
├─────────────────────────────────────────────────────────────────┤
│  > Feature/spec name: user-authentication                       │
│  > Creating spec: .kiro/specs/user-authentication/              │
│                                                                  │
│  Phases:                                                         │
│    1. SPEC   - Define requirements and design                   │
│    2. TEST   - Write failing tests (TDD)                        │
│    3. CODE   - Implement to pass tests                          │
│    4. BUILD  - Lint, type check, coverage                       │
│    5. QUALITY GATE - Security scan, code review                 │
│    6. DOCS   - Generate documentation                           │
│                                                                  │
│  > Start from phase [1-6, default: 1]: 1                        │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│  Phase 1: SPEC                                                   │
│  ═══════════════════════════════════════════════════════════    │
│                                                                  │
│  [Using spec-workflow MCP...]                                   │
│  ✓ Loaded workflow guide                                        │
│  ✓ Created requirements.md                                      │
│  ✓ Created design.md                                            │
│  ✓ Created tasks.md                                             │
│                                                                  │
│  > Proceed to Phase 2: TEST? [Y/n]: Y                          │
│                                                                  │
│  ═══════════════════════════════════════════════════════════    │
│  Phase 2: TEST                                                   │
│  ═══════════════════════════════════════════════════════════    │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Headless Mode Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  $ kiro sdlc --headless --spec user-auth --verbose              │
├─────────────────────────────────────────────────────────────────┤
│  [2025-01-15T10:30:00Z] Starting SDLC workflow                  │
│  [2025-01-15T10:30:00Z] Spec: user-auth                         │
│  [2025-01-15T10:30:00Z] Mode: headless                          │
│  [2025-01-15T10:30:00Z]                                         │
│  [2025-01-15T10:30:01Z] Phase 1: SPEC                           │
│  [2025-01-15T10:30:01Z]   Loading spec-workflow guide...        │
│  [2025-01-15T10:30:02Z]   Creating requirements.md...           │
│  [2025-01-15T10:30:03Z]   Creating design.md...                 │
│  [2025-01-15T10:30:04Z]   Creating tasks.md...                  │
│  [2025-01-15T10:30:04Z]   Phase 1 complete                      │
│  [2025-01-15T10:30:04Z]                                         │
│  [2025-01-15T10:30:05Z] Phase 2: TEST                           │
│  [2025-01-15T10:30:05Z]   Generating test files...              │
│  [2025-01-15T10:30:10Z]   Running tests (expect failure)...     │
│  [2025-01-15T10:30:12Z]   Tests failed as expected (RED)        │
│  [2025-01-15T10:30:12Z]   Phase 2 complete                      │
│  ...                                                             │
│  [2025-01-15T10:35:00Z] SDLC workflow complete                  │
│  [2025-01-15T10:35:00Z] Exit code: 0                            │
└─────────────────────────────────────────────────────────────────┘
```

## Spec-Workflow MCP Integration

### MCP Tools Mapping

| SDLC Phase | MCP Tool | Purpose |
|------------|----------|---------|
| Setup | `steering-guide` | Create project steering documents |
| 1. SPEC | `spec-workflow-guide` | Load spec creation workflow |
| 1. SPEC | `approvals` (request) | Request approval for spec |
| All | `spec-status` | Check overall spec progress |
| All | `approvals` (status) | Check approval status |
| 3-6 | `log-implementation` | Record implementation details |

### Tool Usage Examples

```typescript
// Phase 1: SPEC - Load workflow guide
const guide = await mcp.call('spec-workflow-guide', {});

// Phase 1: SPEC - Create approval request
const approval = await mcp.call('approvals', {
  action: 'request',
  category: 'spec',
  categoryName: 'user-auth',
  type: 'document',
  title: 'Requirements approval',
  filePath: '.kiro/specs/user-auth/requirements.md'
});

// Check status
const status = await mcp.call('spec-status', {
  specName: 'user-auth',
  projectPath: process.cwd()
});

// Log implementation after task completion
await mcp.call('log-implementation', {
  specName: 'user-auth',
  taskId: '2.1',
  summary: 'Implemented User model with email validation',
  filesModified: ['src/models/user.py'],
  filesCreated: ['tests/unit/test_user.py'],
  statistics: { linesAdded: 150, linesRemoved: 0 },
  artifacts: {
    classes: [{
      name: 'User',
      purpose: 'User data model',
      location: 'src/models/user.py',
      methods: ['__init__', '__repr__'],
      isExported: true
    }]
  }
});
```

## Phase Execution Logic

```python
class SDLCPhaseExecutor:
    """Executes SDLC phases in CLI context."""

    PHASES = {
        1: ("spec", "Define requirements and design"),
        2: ("test", "Write failing tests (TDD)"),
        3: ("code", "Implement to pass tests"),
        4: ("build", "Lint, type check, coverage"),
        5: ("quality_gate", "Security scan, code review"),
        6: ("docs", "Generate documentation"),
    }

    PREREQUISITES = {
        1: [],  # SPEC has no prerequisites
        2: ["spec_complete"],  # TEST requires spec
        3: ["tests_exist", "tests_fail"],  # CODE requires failing tests
        4: ["tests_pass"],  # BUILD requires passing tests
        5: ["build_pass"],  # QUALITY GATE requires build
        6: ["quality_gate_pass"],  # DOCS requires quality gate
    }

    def __init__(self, mcp_client, config):
        self.mcp = mcp_client
        self.config = config

    async def execute_phase(
        self,
        phase_num: int,
        spec_name: str,
        interactive: bool = True
    ) -> PhaseResult:
        """Execute a specific phase."""
        phase_name, description = self.PHASES[phase_num]

        # Check prerequisites
        if not await self.check_prerequisites(phase_num, spec_name):
            return PhaseResult(
                success=False,
                error="Prerequisites not met",
                exit_code=3
            )

        # Execute based on phase
        handler = getattr(self, f"_execute_{phase_name}")
        result = await handler(spec_name, interactive)

        # Log implementation if successful
        if result.success and phase_num >= 3:
            await self._log_implementation(spec_name, phase_num, result)

        return result

    async def _execute_spec(self, spec_name: str, interactive: bool) -> PhaseResult:
        """Execute SPEC phase using spec-workflow MCP."""
        # Load workflow guide
        guide = await self.mcp.call('spec-workflow-guide', {})

        # Create spec directory
        spec_path = f".kiro/specs/{spec_name}"

        # Create requirements.md
        await self._create_requirements(spec_name, interactive)

        # Create design.md
        await self._create_design(spec_name, interactive)

        # Create tasks.md
        await self._create_tasks(spec_name, interactive)

        # Request approval
        if interactive:
            await self.mcp.call('approvals', {
                'action': 'request',
                'category': 'spec',
                'categoryName': spec_name,
                'type': 'document',
                'title': f'Spec approval for {spec_name}',
                'filePath': f'{spec_path}/requirements.md'
            })

        return PhaseResult(success=True, exit_code=0)

    async def _execute_build(self, spec_name: str, interactive: bool) -> PhaseResult:
        """Execute BUILD phase with quality checks."""
        checks = [
            ("Lint check", ["ruff", "check", "src/", "tests/"]),
            ("Type check", ["mypy", "src/"]),
            ("Test suite", ["pytest", "--cov=src", "--cov-fail-under=80"]),
        ]

        for name, cmd in checks:
            result = await self._run_command(cmd)
            if result.returncode != 0:
                return PhaseResult(
                    success=False,
                    error=f"{name} failed",
                    exit_code=4,
                    output=result.output
                )

        return PhaseResult(success=True, exit_code=0)

    async def _execute_quality_gate(self, spec_name: str, interactive: bool) -> PhaseResult:
        """Execute QUALITY GATE phase with security and review."""
        # Security scan
        bandit_result = await self._run_command(["bandit", "-r", "src/", "-f", "json"])
        if self._has_critical_findings(bandit_result.output):
            return PhaseResult(
                success=False,
                error="Critical security vulnerabilities found",
                exit_code=5
            )

        # Dependency check
        safety_result = await self._run_command(["safety", "check", "-r", "requirements.txt"])
        if safety_result.returncode != 0:
            return PhaseResult(
                success=False,
                error="Vulnerable dependencies found",
                exit_code=5
            )

        # Code review (interactive mode triggers review prompt)
        if interactive:
            # Trigger code review conversation
            pass

        return PhaseResult(success=True, exit_code=0)
```

## Exit Codes

| Code | Constant | Meaning |
|------|----------|---------|
| 0 | `EXIT_SUCCESS` | All phases completed successfully |
| 1 | `EXIT_ERROR` | General/unexpected error |
| 2 | `EXIT_INVALID_ARGS` | Invalid command-line arguments |
| 3 | `EXIT_PREREQ_FAIL` | Phase prerequisites not met |
| 4 | `EXIT_PHASE_FAIL` | Phase execution failed (lint, test, etc.) |
| 5 | `EXIT_QUALITY_FAIL` | Quality gate failed (security, coverage) |
| 6 | `EXIT_MCP_ERROR` | MCP server communication error |

## Configuration File

### `.kiro/cli-config.json`

```json
{
  "sdlc": {
    "defaultPhase": 1,
    "specPrefix": "",
    "timeout": {
      "phase": 300000,
      "command": 60000
    },
    "quality": {
      "coverageThreshold": 80,
      "lintErrors": 0,
      "securityLevel": "high"
    },
    "output": {
      "format": "human",
      "verbose": false,
      "timestamps": true
    },
    "mcp": {
      "specWorkflow": {
        "autoApprove": false,
        "approvalTimeout": 86400000
      }
    }
  }
}
```

## Output Formats

### Human (Default)

```
═══════════════════════════════════════════════════════════
Phase 1: SPEC - Define requirements and design
═══════════════════════════════════════════════════════════

✓ Loaded workflow guide
✓ Created requirements.md
✓ Created design.md
✓ Created tasks.md

Phase 1 complete. Proceed to Phase 2? [Y/n]:
```

### JSON

```json
{
  "phase": 1,
  "name": "spec",
  "status": "complete",
  "duration_ms": 3500,
  "artifacts": [
    ".kiro/specs/user-auth/requirements.md",
    ".kiro/specs/user-auth/design.md",
    ".kiro/specs/user-auth/tasks.md"
  ],
  "next_phase": 2
}
```

### Quiet

```
[PASS] Phase 1: SPEC
[PASS] Phase 2: TEST
[PASS] Phase 3: CODE
[PASS] Phase 4: BUILD
[PASS] Phase 5: QUALITY GATE
[PASS] Phase 6: DOCS
```
