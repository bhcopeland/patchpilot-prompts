# Filesystems/VFS — Testability Guide

## Test Selection
- fs/ core VFS patches: use kselftest-filesystems
- fs/ext4/ patches: boot test (xfstests not available in standard kselftest)
- fs/btrfs/ patches: boot test (xfstests not available)
- fs/xfs/ patches: boot test
- fs/fuse/ patches: boot test
- fs/proc/ patches: kselftest-proc
- fs/tmpfs/ patches: kselftest-tmpfs
- fs/overlayfs/ patches: kselftest-filesystems (includes overlay tests)

## Tree Selection
- Most filesystem patches go to mainline
- ext4/xfs/btrfs have their own trees but mainline is usually safe for testing

## Debug Kconfig
- CONFIG_DEBUG_LOCK_ALLOC=y — catches VFS locking order violations
- CONFIG_PROVE_LOCKING=y — lockdep for inode/dentry lock ordering
- CONFIG_DEBUG_ATOMIC_SLEEP=y — catches sleeping in atomic VFS paths

## Timeout Guidance
- kselftest-filesystems: 20 minutes
- kselftest-proc: 10 minutes
- kselftest-tmpfs: 10 minutes

## Known Issues
- Most filesystem-specific testing requires xfstests, which is not a kselftest
- Boot test is often the only practical test for specific filesystem drivers
- Boot test alone is INCONCLUSIVE for VFS core changes — mention the coverage gap
- kselftest-filesystems covers VFS core and mount API, not specific filesystems
