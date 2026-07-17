# Tool Schema Audit: External Prompts → MSB v2 / Hermes

## Sources
- `Anthropic/Claude Code/Tools.json`
- `Anthropic/Claude Code/Prompt.txt`
- `Cursor Prompts/Agent Tools v1.0.json`
- `Manus Agent Tools & Prompt/Agent loop.txt`
- `Replit/Tools.json`
- `Windsurf/Prompt Wave 11.txt`

## External tool categories observed
- file inspection: `read_file`, `grep_search`, `glob`
- code editing: patch/edit/write
- shell: bash, package install, service management
- agent delegation: launch subagent / later agent
- retrieval: semantic search, web fetch

## Hermes / MSB v2 equivalents already present
- file inspection → Hermes `read_file`, `search_files`
- code editing → Hermes `patch`, `write_file`, `skill_manage`
- shell → Hermes `terminal`
- retrieval → Hermes `web_search`, `web_fetch`, `session_search`
- memory → Hermes `memory`
- agents → Hermes `delegate_task` / `cronjob`
- multimodal / docs → Hermes `vision_analyze`, `text_to_speech`

## Gaps
- generic MCP tool register/discovery surface
- bounded tool executor with verify-first hooks
- unified tool-schema manifest consumers can introspect

## Opportunity
Use `PromptContract` in `msb_v2/agent/prompt_contract.py` as the canonical
translation layer between external prompt expectations and Hermes tool surfaces.
