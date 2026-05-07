# Timers — Testability Guide

## Test Selection
- kernel/time/ patches: use kselftest-timers
- hrtimer changes: use kselftest-timers
- Clock source/event changes: use kselftest-timers
- POSIX timer changes: use kselftest-timers

## Debug Kconfig
- CONFIG_HIGH_RES_TIMERS=y — high-resolution timer support
- CONFIG_DEBUG_TIMERS=y — timer debugging
- CONFIG_TIMER_STATS=y — timer usage statistics (if available)

## Timeout Guidance
- kselftest-timers: 30 minutes — some tests sleep for measured durations
- inconsistency-check and nanosleep tests can run for several minutes each

## Known Issues
- Timer accuracy tests are inherently sensitive to virtualisation jitter
- nanosleep precision tests may report failures in QEMU due to timer coarseness
- adjtimex tests modify the system clock — should not run in parallel with other time-sensitive tests
- set-timer-lat tests measure latency and are unreliable under load
- Mark timer precision failures as flaky in virtualised environments
