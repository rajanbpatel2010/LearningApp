# Agent Orchestration Skill

## Objective
Implement the planning and orchestration layer for multi-agent interview coaching.

## Deliverables
- Planning agent
- Specialized agents for learning, quiz, interview, evaluation, and feedback
- Shared workflow state and tool routing
- Fallback logic

## Implementation Checklist
1. Define the orchestration contract for each agent.
2. Implement a planning agent that classifies the request intent.
3. Create a router that chooses RAG, MCP, question bank, or LLM knowledge.
4. Build a session state model so agents can share context.
5. Implement prompt templates for learning, quiz, interview, and feedback responses.
6. Add graceful fallback if RAG or MCP is temporarily unavailable.

## Success Criteria
- A prompt like “prepare me for a Python interview” triggers the correct workflow.
- The system can complete a mock interview session end to end.
- The agent output is grounded and uses retrieval context where appropriate.
