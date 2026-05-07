# Scheduler — Testability Guide

## Test Selection
- kernel/sched/ patches: use kselftest-sched
- SCHED_EXT patches (kernel/sched/ext.c, sched_ext): use kselftest-sched_ext
- CFS/EEVDF changes: use kselftest-sched
- CPU isolation/affinity changes: use kselftest-sched

## Debug Kconfig
- CONFIG_SCHED_DEBUG=y — exposes /proc/sched_debug and per-task stats
- CONFIG_SCHEDSTATS=y — enables scheduler statistics
- CONFIG_DEBUG_PREEMPT=y — catches preemption count mismatches
- CONFIG_PROVE_LOCKING=y — if patch touches runqueue locking

## Timeout Guidance
- kselftest-sched: 30 minutes, tests are generally fast
- CPU-intensive stress tests may need more QEMU vCPUs for meaningful results

## Known Issues
- Some sched tests require multiple CPUs — ensure QEMU has at least 2 vCPUs
- Priority inversion tests can be timing-sensitive in virtualised environments
- sched_ext tests require CONFIG_SCHED_CLASS_EXT=y
