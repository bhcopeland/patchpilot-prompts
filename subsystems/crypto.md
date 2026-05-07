# Crypto Subsystem — Testability Guide

## Test Selection
- crypto/ patches: use ltp-crypto, NOT kselftest
- include/crypto/ patches: use ltp-crypto
- AF_ALG / algif patches: use ltp-crypto (covers algif_hash, algif_skcipher, algif_aead)
- There is no kselftest-crypto — do not fabricate one

## Kconfig
- Most crypto algorithms are modules — ensure the specific algorithm is built
- CONFIG_CRYPTO_USER_API=y — needed for AF_ALG tests
- CONFIG_CRYPTO_USER_API_HASH=y — needed for algif_hash tests
- CONFIG_CRYPTO_USER_API_SKCIPHER=y — needed for algif_skcipher tests
- CONFIG_CRYPTO_USER_API_AEAD=y — needed for algif_aead tests

## Known Issues
- ltp-crypto tests are quick (under 5 minutes)
- Many crypto tests skip if the specific algorithm module is not loaded
- High skip count is normal — only the tested algorithm's tests run
