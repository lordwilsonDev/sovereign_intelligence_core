# First Contact — Public Demonstration Notes

**Status:** Ready for public demonstration on local runtime.

## Public Surface

- `POST /first-contact/start`
- `POST /first-contact/advance`
- `GET /first-contact/status/{session_id}`
- `GET /first-contact/demo`

All three primary endpoints are anonymous-friendly in the live app router and covered by tests in `tests/first_contact/`.

## Verified Live Behavior

```bash
curl -s -X POST http://127.0.0.1:8766/first-contact/start
# Returns: session_id, current_step="welcome", completed=false

curl -s -X POST http://127.0.0.1:8766/first-contact/advance \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<id>","step":"assumption","text":"AI cannot reason"}'
# Returns: participant_assumption captured

curl -s -X POST http://127.0.0.1:8766/first-contact/advance \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<id>","step":"invert","text":"AI might reason"}'
# Returns: proposals list with inverted assumption

curl -s -X POST http://127.0.0.1:8766/first-contact/advance \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<id>","step":"reveal","text":"I assumed AI cannot change my mind"}'
# Returns: completed=true, revealed_assumption recorded
```

## Public Ingress Guidance

When exposing `/first-contact/*` externally:

1. **Route:** proxy `/first-contact/*` to `http://127.0.0.1:8766/first-contact/*`
2. **Auth:** anonymous access is allowed for these routes in local bypass mode; confirm production auth policy before public exposure.
3. **Session persistence:** sessions are stored in `MSB_FIRST_CONTACT_PATH` or `./runtime/first_contact_sessions.jsonl` by default. For multi-worker/restart-resilient deployments, set `MSB_FIRST_CONTACT_PATH=/var/lib/msb-v2/first_contact_sessions.jsonl` to an absolute, writable path.
4. **Rate limiting:** recommend lightweight rate limiting on `/first-contact/start` to prevent session exhaustion.
5. **CORS:** if calling from a browser, ensure CORS headers allow the origin.

## Production Note

For external public access, ensure ingress rules allow anonymous access only to `/first-contact/*` and that session state is persisted across restarts if long-running contact protocols are expected.
