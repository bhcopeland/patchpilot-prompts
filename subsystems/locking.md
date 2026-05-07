# Locking — Testability Guide

## Test Selection
- kernel/locking/ patches: use kselftest-locking
- Changes to mutex, rwsem, spinlock implementations: use kselftest-locking
- Lock contention or wait/wound mutex changes: use kselftest-locking

## Debug Kconfig
- CONFIG_PROVE_LOCKING=y — enables lockdep, the most important locking debugger
- CONFIG_DEBUG_LOCK_ALLOC=y — tracks lock allocation and detects use-after-free of locks
- CONFIG_DEBUG_MUTEXES=y — validates mutex operations
- CONFIG_DEBUG_SPINLOCK=y — catches uninitialised spinlock usage
- CONFIG_DEBUG_RWSEMS=y — validates rwsem operations
- CONFIG_LOCK_STAT=y — lock contention statistics

## Timeout Guidance
- kselftest-locking: 15 minutes — tests are fast
- locktorture is available for deeper testing but not a standard kselftest

## Known Issues
- lockdep (PROVE_LOCKING) significantly increases memory usage and slows execution
- lockdep has a finite number of lock classes — very large configs may exhaust them
- Some locking tests require multiple CPUs to trigger contention paths
- Boot test alone is INCONCLUSIVE for locking changes — lockdep splats in dmesg are the primary signal
