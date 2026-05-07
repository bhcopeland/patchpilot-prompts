# pidfd — Testability Guide

## Test Selection
- pidfd-related patches: use kselftest-pidfd
- Changes to kernel/pid.c, kernel/fork.c (pidfd paths): use kselftest-pidfd
- clone3 + pidfd interaction: use kselftest-pidfd and kselftest-clone3

## Debug Kconfig
- No special kconfig needed beyond defconfig

## Timeout Guidance
- kselftest-pidfd: 10 minutes — tests are fast

## Known Issues
- pidfd tests require CONFIG_PID_NS=y for namespace tests
- pidfd_open, pidfd_send_signal, pidfd_getfd are all exercised
- Some tests use clone3 with CLONE_PIDFD — requires CONFIG_CLONE3=y (default)
