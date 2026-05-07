# BPF Subsystem — Testability Guide

## Test Selection
- All BPF patches: use kselftest-bpf
- BPF tool changes (tools/lib/bpf/): use kselftest-bpf
- BPF selftests (tools/testing/selftests/bpf/): use kselftest-bpf

## Toolchain
- clang-19 required for BPF CO-RE (compile-once run-everywhere) programs
- clang-19 required if patch uses __attribute__((preserve_access_index)) or similar
- gcc-14 sufficient for kernel-side BPF changes that don't touch BPF programs

## Kconfig
- CONFIG_BPF=y (usually in defconfig)
- CONFIG_BPF_SYSCALL=y
- CONFIG_BPF_JIT=y
- CONFIG_BPF_JIT_ALWAYS_ON=y
- CONFIG_DEBUG_INFO_BTF=y (needed for CO-RE and BTF-based features)

## Known Issues
- BPF selftests are large — expect 60+ minutes runtime
- Some tests require specific kernel features (XDP, sockmap) that must be enabled via kconfig
- test_progs is the main test binary — failures there are usually real
