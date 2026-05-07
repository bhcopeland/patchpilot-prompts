# Seccomp — Testability Guide

## Test Selection
- kernel/seccomp.c patches: use kselftest-seccomp
- Seccomp BPF filter changes: use kselftest-seccomp
- tools/testing/selftests/seccomp/: use kselftest-seccomp

## Debug Kconfig
- CONFIG_SECCOMP=y
- CONFIG_SECCOMP_FILTER=y — BPF-based filtering
- CONFIG_SECCOMP_CACHE_DEBUG=y — debugging for seccomp cache

## Timeout Guidance
- kselftest-seccomp: 15 minutes — tests are fast

## Known Issues
- seccomp_bpf test binary is arch-specific — ensure arch matches device
- Some tests exercise SECCOMP_RET_USER_NOTIF which requires newer kernels
- Seccomp tests use ptrace heavily — ptrace restrictions (Yama LSM) can cause false failures
