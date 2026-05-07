# Tracing/Ftrace — Testability Guide

## Test Selection
- kernel/trace/ patches: use kselftest-ftrace
- Tracepoint changes (include/trace/events/): use kselftest-ftrace
- perf tracing changes (tools/perf/ tracing paths): use kselftest-ftrace
- Function graph tracer changes: use kselftest-ftrace

## Debug Kconfig
- CONFIG_FTRACE=y — base ftrace support
- CONFIG_FUNCTION_TRACER=y — function-level tracing
- CONFIG_DYNAMIC_FTRACE=y — dynamic function tracing (most tests require this)
- CONFIG_FUNCTION_GRAPH_TRACER=y — function graph tracer tests
- CONFIG_STACK_TRACER=y — stack depth tracing
- CONFIG_KPROBE_EVENTS=y — kprobe-based tracing tests
- CONFIG_UPROBE_EVENTS=y — uprobe-based tracing tests

## Timeout Guidance
- kselftest-ftrace: 45 minutes — shell-based tests can be slow
- Individual ftrace tests are small but the full suite has 100+ tests

## Known Issues
- ftrace selftests are shell scripts run from tools/testing/selftests/ftrace/
- Some tests require /sys/kernel/debug/tracing (debugfs mounted)
- Trigger and filter tests can be timing-sensitive in QEMU
- Event tracing tests depend on specific tracepoints being compiled in
