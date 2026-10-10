# Simple OTP 🐾🔐

[![Download on the App Store](https://img.shields.io/badge/App_Store-Download-blue?logo=apple&style=for-the-badge)](https://apps.apple.com/us/app/simple-otp/id6816673973)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Offline](https://img.shields.io/badge/Network-100%25%20Offline-orange?style=for-the-badge)](#zero-network-architecture)
[![Expo](https://img.shields.io/badge/Expo-SDK%2052-000020?logo=expo&style=for-the-badge)](https://expo.dev)

> **High-Security, 100% Offline 2FA Authenticator guarded by interactive companion mascots.**

Simple OTP is an open-source, zero-network two-factor authentication (2FA) mobile application for iOS and Android. It keeps your sensitive verification codes guarded inside hardware-backed storage with zero telemetry, zero analytics, and zero outbound network calls.

---

## 📱 Official Download

Simple OTP is officially published on the Apple App Store:

👉 **[Download Simple OTP on the Apple App Store](https://apps.apple.com/us/app/simple-otp/id6816673973)**

---

## ✨ Features

- **🛡️ 100% Offline & Zero Network Perimeter**: No internet permission requested, no cloud sync, no tracking, and zero telemetry. Outbound network APIs are fail-closed intercepted at runtime.
- **🔐 Hardware-Backed Vault**: Master Vault Keys are derived with PBKDF2 (100,000 iterations) and stored in iOS Keychain / Android Keystore with AES-256-GCM authenticated encryption.
- **🐱 Interactive Mascot Companions**: Choose between **Cipher Cat**, **Byte Dog**, and **Shield Bunny**—smooth Reanimated sprite companions that react to your actions with real-time feedback and speech bubbles.
- **⚡ Standards Compliant**: Full support for RFC 6238 (TOTP - Time-Based) and RFC 4226 (HOTP - Counter-Based), compatible with SHA-1, SHA-256, and SHA-512 algorithms with configurable digits (6 or 8) and periods.
- **📷 Multi-Channel Ingestion**:
  - Live Camera QR scanner with instant validation.
  - Photo library QR image picker (processed entirely on-device).
  - Clipboard auto-detection for `otpauth://` URIs.
  - Manual entry with automated Base32 sanitization.
- **📦 Encrypted Backups**: Export and restore your 2FA accounts in password-protected `.simpleotp` encrypted packages.
- **👁️ Privacy Shield**: Prevents screenshots and masks sensitive screens in the system app switcher (`FLAG_SECURE` on Android and privacy overlay on iOS).
- **🎓 2FA Academy**: Interactive in-app security lessons explaining authentication principles, offline safety, and backup hygiene.

---

## 📖 Documentation

Visit our full documentation website & official showcase:

- 🇺🇸 **[English Documentation](https://kd-labs-io.github.io/simple-otp/en/)** | **[KD Labs Showcase](https://kd.io.vn/en/apps/simple-otp/)**
- 🇻🇳 **[Tài liệu Tiếng Việt](https://kd-labs-io.github.io/simple-otp/vi/)** | **[Trang giới thiệu KD Labs](https://kd.io.vn/apps/simple-otp/)**

---

## 🛠️ Development

### Prerequisites

- [Node.js](https://nodejs.org/) (v20+ recommended)
- [npm](https://www.npmjs.com/) or [bun](https://bun.sh/)
- [Expo CLI](https://docs.expo.dev/)

### Setup

```bash
# 1. Clone repository
git clone https://github.com/kd-labs-io/simple-otp.git
cd simple-otp

# 2. Install dependencies
npm install

# 3. Start development server
npx expo start
```

### Running Tests

The project includes unit, adversarial, stress, and end-to-end test suites:

```bash
npm test
```

### Building Documentation

```bash
cd docs
npm install
npm run dev     # Local preview
npm run build   # Production bundle
```

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
