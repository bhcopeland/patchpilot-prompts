# io_uring — Testability Guide

## Test Selection
- io_uring/ patches: use kselftest-io_uring
- io_uring selftest changes: use kselftest-io_uring

## Debug Kconfig
- CONFIG_IO_URING=y — io_uring support (usually in defconfig)
- CONFIG_IO_URING_STATS=y — usage statistics
- CONFIG_DEBUG_LOCK_ALLOC=y — catches locking issues in io_uring

## Timeout Guidance
- kselftest-io_uring: 30 minutes
- Some tests exercise concurrent submission paths which can be slow in QEMU

## Known Issues
- io_uring tests require a relatively recent liburing or build their own
- Some tests need specific features (fixed files, registered buffers) that depend on kconfig
- io_uring changed directory layout from tools/testing/selftests/io_uring/ to io_uring/ in recent kernels
- Timeout and cancellation tests can be timing-sensitive in virtualised environments
