# Networking Subsystem — Testability Guide

## Test Selection
- net/bridge/ patches: use kselftest-net-forwarding, NOT kselftest-net
- net/mptcp/ patches: use kselftest-net-mptcp
- net/netfilter/ patches: use kselftest-netfilter
- net/hsr/ patches: use kselftest-net-hsr
- net/unix/ patches: use kselftest-net-af_unix
- net/rds/ patches: use kselftest-net-rds
- drivers/net/<vendor>/ patches: use kselftest-drivers-net, NOT kselftest-net
- Core net/ changes (ipv4, ipv6, routing, sockets): use kselftest-net
- Avoid kselftest-net for non-core changes — it has 190+ tests and often times out in QEMU

## Timeout Guidance
- kselftest-net: 90 minutes minimum, may still time out
- kselftest-net-forwarding: 90 minutes minimum — bridge/vlan/tc tests are slow in QEMU
- Traffic-scheduling tests (ETS, TBF, HTB): expect QEMU timing failures — these are flaky in virtualised environments

## Kconfig
- Enable CONFIG_DEBUG_NET=y for all net patches
- Bridge patches: CONFIG_BRIDGE=y, CONFIG_BRIDGE_VLAN_FILTERING=y
- Netfilter: CONFIG_NETFILTER=y, CONFIG_NF_TABLES=y
- MPTCP: CONFIG_MPTCP=y, CONFIG_MPTCP_IPV6=y

## Known Issues
- ETS qdisc band tests frequently fail in QEMU due to virtualised network timing — mark as flaky, not regression
- Bridge forwarding tests require CONFIG_VLAN_8021Q=y
- Some net selftests require netcat/socat/iperf3 in the rootfs
