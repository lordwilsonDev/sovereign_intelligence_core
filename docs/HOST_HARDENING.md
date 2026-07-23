# Host Hardening — macOS Operational Guidance

## Current SSHH RED Warnings

- `Disk 95.8% full`
- `1 zombie process`

These are host-state issues, not application bugs. The application correctly reports them through `/systems-health/status`.

## Disk Cleanup

```bash
# Check usage
df -h /

# Find top-level offenders
sudo du -sh /* 2>/dev/null | sort -rh | head -20

# Common caches to clear (restart apps afterward if needed)
rm -rf ~/Library/Caches/*

# Remove old Xcode simulators if present
sudo rm -rf ~/Library/Developer/Xcode/DerivedData/*

# Purge old logs
sudo rm -rf /private/var/log/*.gz
sudo rm -rf /private/var/log/asl/*.asl
```

## Zombie Processes

```bash
# List defunct processes
ps aux | grep defunct

# Zombies are already-terminated children waiting for the parent to read exit status.
# Remediate by restarting the parent process or, if necessary, restarting the host.
pkill -HUP <parent_process_name>
```

## Periodic Monitoring

Consider a lightweight `launchd` plist or `cron` entry to alert when disk exceeds 90% or zombie count rises.

## Application Behavior

`/systems-health/status` correctly reports `RED` while host issues persist. `/schh/status` remains `GREEN`; treat `/schh/status` as the application health signal and `/systems-health/status` as the host condition signal.
