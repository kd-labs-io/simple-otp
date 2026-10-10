# Files

- [Account ingestion through camera, images, clipboard, and manual entry](account-ingestion.md) - Traces device input and untrusted OTP data through parsing, manual validation, duplicate detection, encrypted vault persistence, and UI feedback. Distinguishes the reusable ingestion router from the dashboard's actual handlers and their concurrency limits.
- [Backup, restore, and QR account transfer](backup-and-transfer.md) - Password-encrypted backup export and restore, including ID-based merge, destructive replacement, and partial-failure semantics. Explains how single-account otpauth QR transfer exposes secrets and where cache and sensitive-state cleanup actually occurs.
