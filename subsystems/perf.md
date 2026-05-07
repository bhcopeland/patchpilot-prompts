# Perf Tools — Testability Guide

## Test Selection
- tools/perf/ patches: boot test is the practical minimum
- Perf has its own test suite (perf test) but it is not a standard kselftest
- Changes to perf event core (kernel/events/): use kselftest-perf_events

## Debug Kconfig
- CONFIG_PERF_EVENTS=y — perf event support (usually in defconfig)
- CONFIG_DEBUG_PERF_USE_VMALLOC=y — catches perf buffer issues

## Timeout Guidance
- Boot test: standard timeout
- perf test (if available): 30 minutes

## Known Issues
- Perf tool changes are userspace — they build and run against the kernel tree
- perf test requires the perf binary built from the same tree
- Hardware PMU tests are not meaningful in QEMU (no real counters)
- Software event tests (context switches, page faults) work in QEMU
- Boot test alone is INCONCLUSIVE for perf tool changes — mention the gap
