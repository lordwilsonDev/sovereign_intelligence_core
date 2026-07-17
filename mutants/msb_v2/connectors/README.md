# Connectors

This package hosts external adapters for the Sovereign Stack.

## Modules

- `slack.py` — Slack RTM/Events API client for inbound/outbound messaging.
- `discord.py` — Discord gateway and slash-command connector.
- `telegram.py` — Telegram Bot API connector.

## Contract

Each connector exposes an async `connect()` / `disconnect()` lifecycle and
emits normalized envelopes that the runtime router can consume defensively.
No connector may block the main runtime thread.
