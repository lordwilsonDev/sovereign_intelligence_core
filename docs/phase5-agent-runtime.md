# Phase 5 — Agent OS Runtime Prompt Contract

## Source grounding
Distilled from:
- `system-prompts-and-models-of-ai-tools/Anthropic/Claude Code/Prompt.txt`
- `system-prompts-and-models-of-ai-tools/Anthropic/Claude Code 2.0.txt`
- `system-prompts-and-models-of-ai-tools/Cursor Prompts/Agent Prompt v1.2.txt`
- `system-prompts-and-models-of-ai-tools/Manus Agent Tools & Prompt/Agent loop.txt`
- `system-prompts-and-models-of-ai-tools/Replit/Prompt.txt`

## Hermes Phase 5 Prompt Template

```
{contract.render()}

<User request>
{task}
</User request>
```

## Registered tools available to Phase 5 agents
- `agent_run`: execute `AgentRuntime.run(run_id, tasks)` against dotted-path callables
- `run_status`: read stored run state by run_id
- `runtime_status`: inspect RuntimeContext / WorkerPool health

## Behavioral contract
- operate under MSB v2 rules
- prefer tool use; do not guess
- no preamble / postamble
- cite memory when relevant
- verify with pytest before claiming success

## TODO
- expand tool list from Cursor/Replit/Manus as needed
- add bounded-concurrency policy to `agent_run`
- add pid/trace forensics into run responses
