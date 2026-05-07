# DRM/Graphics Subsystem — Testability Guide

## Test Selection
- drivers/gpu/drm/ patches: boot test is often the best available option
- DRM core changes: boot test + check for GPU driver probe success
- No comprehensive kselftest suite for DRM exists in-tree
- IGT GPU Tools exist but require real GPU hardware, not suitable for QEMU

## Kconfig
- CONFIG_DRM=y
- Driver-specific configs (CONFIG_DRM_I915, CONFIG_DRM_AMDGPU, etc.)
- CONFIG_DRM_FBDEV_EMULATION=y if framebuffer patches

## Known Issues
- Most DRM testing requires real hardware — QEMU cannot exercise GPU codepaths
- Boot test verifies the driver loads without oops/panic
- Verdict should typically be INCONCLUSIVE for DRM patches with only boot tests
- Flag as coverage gap: DRM selftests require IGT on real hardware
