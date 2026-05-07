# RCU — Testability Guide

## Test Selection
- kernel/rcu/ patches: use rcutorture
- Changes to call_rcu, synchronize_rcu, kfree_rcu: use rcutorture
- SRCU changes: rcutorture covers SRCU variants

## Debug Kconfig
- CONFIG_PROVE_RCU=y — detects RCU usage violations (e.g. dereferencing outside read-side critical section)
- CONFIG_RCU_EXPERT=y — unlocks additional RCU debugging tunables
- CONFIG_RCU_CPU_STALL_TIMEOUT=21 — shorter stall timeout for faster detection
- CONFIG_DEBUG_OBJECTS_RCU_HEAD=y — catches double call_rcu on the same object

## Timeout Guidance
- rcutorture: 60 minutes minimum — torture tests run for a configurable duration
- Short runs (5 min) catch most bugs; longer runs catch timing-dependent races

## Known Issues
- rcutorture is a kernel module test, not a userspace selftest — requires CONFIG_RCU_TORTURE_TEST=m
- RCU stall warnings in dmesg are the primary failure signal, not test exit code
- QEMU may not reproduce all SMP race conditions — real hardware catches more
- Boot test alone is INCONCLUSIVE for RCU changes — always run rcutorture
