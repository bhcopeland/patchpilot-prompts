# KVM — Testability Guide

## Test Selection
- virt/kvm/ patches: use kselftest-kvm
- arch/x86/kvm/ patches: use kselftest-kvm with x86_64 arch
- arch/arm64/kvm/ patches: use kselftest-kvm with arm64 arch
- KVM selftests (tools/testing/selftests/kvm/): use kselftest-kvm

## Arch Matching
- KVM selftests are arch-specific — match the device/arch to the code being changed
- x86 KVM patches must test on qemu-x86_64
- arm64 KVM patches must test on qemu-arm64
- Cross-arch virt/kvm/ core changes: test on the default arch

## Debug Kconfig
- CONFIG_KVM=y (usually in defconfig)
- CONFIG_KVM_INTEL=y or CONFIG_KVM_AMD=y for x86
- CONFIG_HAVE_KVM=y

## Timeout Guidance
- kselftest-kvm: 45 minutes — some tests create nested VMs which are slow in QEMU
- Dirty log tests and migration tests are the slowest

## Known Issues
- Nested virtualisation tests (KVM-on-KVM) may not work in all QEMU configurations
- Some x86 KVM tests require specific CPU features (VMX/SVM) that QEMU may not expose
- kselftest-kvm test count varies significantly between architectures
