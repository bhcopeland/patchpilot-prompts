# DMA-BUF — Testability Guide

## Test Selection
- drivers/dma-buf/ patches: use kselftest-dmabuf-heaps
- DMA-BUF heap and exporter changes: use kselftest-dmabuf-heaps

## Debug Kconfig
- CONFIG_DMABUF_HEAPS=y — DMA-BUF heap support
- CONFIG_DMABUF_HEAPS_SYSTEM=y — system heap for testing
- CONFIG_DMABUF_HEAPS_CMA=y — CMA heap
- CONFIG_DMA_API_DEBUG=y — catches DMA mapping errors

## Timeout Guidance
- kselftest-dmabuf-heaps: 10 minutes — tests are fast

## Known Issues
- DMA-BUF tests need at least one heap available (system heap is the default)
- CMA tests may fail if CMA region is too small in QEMU
- Tests exercise allocation, mapping, CPU access, and sync operations
- GPU/display interop testing requires real hardware — QEMU tests cover the API only
