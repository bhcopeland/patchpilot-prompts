# Cgroup — Testability Guide

## Test Selection
- kernel/cgroup/ patches: use kselftest-cgroup
- Memory controller (mm/memcontrol.c): use kselftest-cgroup
- CPU controller changes: use kselftest-cgroup
- Cgroup v2 interface changes: use kselftest-cgroup

## Debug Kconfig
- CONFIG_CGROUPS=y (usually in defconfig)
- CONFIG_CGROUP_SCHED=y — CPU controller
- CONFIG_MEMCG=y — memory controller
- CONFIG_CGROUP_PIDS=y — PID controller
- CONFIG_CGROUP_FREEZER=y — freezer controller

## Timeout Guidance
- kselftest-cgroup: 30 minutes
- Memory controller tests may allocate large amounts of memory

## Known Issues
- Some cgroup tests require cgroup v2 unified hierarchy (CONFIG_CGROUP_V2=y)
- Memory pressure tests can be flaky in memory-constrained QEMU
- Tests assume cgroup2 is mounted at /sys/fs/cgroup
- Freezer tests can be timing-sensitive
