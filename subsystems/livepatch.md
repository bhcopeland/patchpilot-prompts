# Livepatch — Testability Guide

## Test Selection
- kernel/livepatch/ patches: use kselftest-livepatch
- Livepatch self-tests: use kselftest-livepatch

## Debug Kconfig
- CONFIG_LIVEPATCH=y — livepatch support
- CONFIG_DYNAMIC_FTRACE_WITH_REGS=y — required for livepatch to work
- CONFIG_MODULES=y — livepatch uses kernel modules
- CONFIG_TEST_LIVEPATCH=m — test module for selftests

## Arch Requirements
- Livepatch is only supported on x86_64, arm64, s390, and ppc64le
- Default to x86_64 for livepatch testing

## Timeout Guidance
- kselftest-livepatch: 15 minutes — tests are small and focused

## Known Issues
- Livepatch tests load/unload kernel modules — failures are usually binary (crash or pass)
- Tests require /sys/kernel/livepatch/ interface
- If CONFIG_LIVEPATCH is not set, all tests are skipped (not failed)
- Some tests check transition completion which can be timing-sensitive
