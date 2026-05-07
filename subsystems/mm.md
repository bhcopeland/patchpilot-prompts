# Memory Management — Testability Guide

## Test Selection
- mm/ patches: use kselftest-mm
- mm/damon/ patches: use kselftest-damon
- include/linux/mm* patches: use kselftest-mm
- userfaultfd patches: use kselftest-mm (includes userfaultfd tests)

## Kconfig
- CONFIG_KASAN=y — catches use-after-free, out-of-bounds access
- CONFIG_KASAN_INLINE=y — inline instrumentation for better coverage
- CONFIG_DEBUG_VM=y — enables VM debugging assertions
- CONFIG_USERFAULTFD=y — needed for userfaultfd selftests
- CONFIG_TRANSPARENT_HUGEPAGE=y — needed for THP tests
- CONFIG_DEBUG_PAGEALLOC=y — catches page allocation bugs

## Known Issues
- KASAN increases memory usage significantly — may need more QEMU RAM (4G+)
- Some mm tests are timing-sensitive (compaction, migration)
- kselftest-mm includes both unit tests and stress tests — total runtime 15-30 min
