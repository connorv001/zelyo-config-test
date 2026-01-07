# Plan: Kubescape MCP Integration

## Phase 1: SSE Client Implementation
- [x] Task: Create `src/mcp_client.py` and implement basic SSE connection logic using `httpx`. [e682c7e]
- [x] Task: Implement MCP initialization handshake (initialize, initialized notifications). [d2f5f2c]
- [x] Task: Implement message exchange logic for MCP tools/resources. [f5131e7]
- [ ] Task: Conductor - User Manual Verification 'Phase 1: SSE Client Implementation' (Protocol in workflow.md)

## Phase 2: Finding Mapping & Data Flow
- [ ] Task: Implement logic to request "config hygiene" resources from the Kubescape MCP server.
- [ ] Task: Update `src/parser.py` to map MCP finding payloads to internal `Finding` models.
- [ ] Task: Implement error handling for disconnected streams or malformed MCP messages.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Finding Mapping & Data Flow' (Protocol in workflow.md)

## Phase 3: Refactoring & Integration
- [ ] Task: Refactor `src/scanner.py` to use `mcp_client` instead of `subprocess.run()`.
- [ ] Task: Update `POST /scan` endpoint to utilize the asynchronous MCP stream.
- [ ] Task: Verify end-to-face integration with existing `GET /findings` endpoint.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Refactoring & Integration' (Protocol in workflow.md)
