# Ticket: zombie process PID 28952 (defunct, parent 1029/datadog-agent)

## Symptom
`ps -p 28952 -o pid,ppid,stat,command` shows:

```
 PID  PPID STAT COMMAND
28952  1029 Z    <defunct>
```

Parent 1029 is `datadog-agent`.

## Status
Cannot be reaped from inside Hermes without killing the parent. This is low risk because it is defunct.

## Options
- If Datadog is essential, do nothing; zombie disappears when Agent restarts.
- If unnecessary, uninstall or stop Agent in Datadog app.
- If you want immediate reap, `sudo kill -9 1029` (Stops Datadog; test side-effects first.)

## Evidence
- `ps -p 28952`: zombie confirmed
- `ps -ax | grep datadog` should show parent 1029
- `pgrep -fl datadog` optional

## Verify
```bash
ps -p 28952 -o pid,ppid,stat,command
ps -p 1029 -o pid,comm,stat
```

## Workaround
Leave zombie alone; it does not consume memory or CPU.
