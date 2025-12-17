---
name: deploy-verifier
description: Post-deployment API verification with automatic rollback
phase: post-deploy
skills: []
agents: []
mcp_servers: []
---

# Deploy Verifier Plugin

Verifies API Gateway + Lambda deployments are functioning correctly and triggers rollback on failure.

## Phase Position

```
1. SPEC → 2. TEST → 3. CODE → 4. BUILD → 5. DOCS → PR → Deploy → [VERIFY]
                                                                      ▲
                                                              YOU ARE HERE
                                                          (Post-deployment)
```

## Verification Pipeline

```
HEALTH CHECK (Verify endpoints are reachable)
         │
         ▼
CONTRACT VALIDATION (Request/response schema validation)
         │
         ▼
SMOKE TESTS (Critical path API calls)
         │
         ▼
    ALL PASSED?
    │         │
   YES        NO
    │         │
    ▼         ▼
SUCCESS   ROLLBACK + NOTIFY
```

## Verification Test File

Create `verify.config.json` in the service root:

```json
{
  "apiBaseUrl": "${API_BASE_URL}",
  "healthEndpoint": "/health",
  "healthTimeout": 60,
  "tests": [
    {
      "name": "Create Resource",
      "endpoint": "POST /api/v1/resources",
      "request": {
        "body": {
          "name": "smoke-test-${TIMESTAMP}",
          "type": "standard"
        }
      },
      "expected": {
        "status": 201,
        "bodyContains": ["id", "name", "createdAt"]
      },
      "cleanup": true
    }
  ],
  "rollback": {
    "enabled": true,
    "strategy": "lambda-alias",
    "notifyOnRollback": ["platform-admin@example.com"]
  }
}
```

## Rollback Strategies

| Strategy | Use Case | Speed |
|----------|----------|-------|
| **Lambda Alias** | Single function updates | Fast (~seconds) |
| **API Gateway Stage** | API configuration changes | Fast (~seconds) |
| **OpenTofu State** | Infrastructure changes | Medium (~minutes) |
| **Blue-Green** | Full stack deployment | Fast (DNS switch) |

## Failure Handling

```
VERIFICATION FAILED
         │
    ┌────┴────┐
    ▼         ▼
ROLLBACK   NOTIFY
Previous   Team
Version
    │         │
    └────┬────┘
         ▼
  CREATE INCIDENT
  (GitHub Issue)
```

## Full SDLC Complete

```
✅ 1. SPEC      - Requirements and design documented
✅ 2. TEST      - Tests written (TDD)
✅ 3. CODE      - Implementation complete
✅ 4. BUILD     - Quality gates passed
✅ 5. DOCS      - Documentation generated
✅ PR Created   - Security audit and code review passed
✅ Deployed     - Infrastructure provisioned
✅ 7. VERIFY    - Post-deployment validation passed

🚀 Deployment verified and stable!
```
