---
type: security-architecture
title: Security boundaries and application lock lifecycle
description: Explains the JavaScript offline perimeter, privacy overlay, biometric lock lifecycle, screen-capture integration gaps, and conditional clipboard expiry. Distinguishes UI concealment from encrypted-vault access control and native enforcement.
tags: [security, privacy, biometrics, offline, clipboard, lifecycle]
verified:
  - by: openwiki/0.7.2
    at: 2026-10-10T07:14:35.895Z
sources:
  - id: openwiki-source-a09366f2501604d7206766f7
    resource: repo://__tests__/adversarial/tier5_security_ui_hardening.test.tsx
  - id: openwiki-source-6faa6a9b05fca2b0141fda54
    resource: repo://__tests__/unit/biometricLoopFix.test.ts
  - id: openwiki-source-4b7fec5cc05fb98a7f74cece
    resource: repo://__tests__/unit/clipboardClear.test.ts
  - id: openwiki-source-b89b29abf499b15ebe44001a
    resource: repo://__tests__/unit/networkBlocker.test.ts
  - id: openwiki-source-052e5ef8199eb0551b4a9ee1
    resource: repo://src/app/_layout.tsx
  - id: openwiki-source-252524ada82462ca31eddd55
    resource: repo://src/app/index.tsx
  - id: openwiki-source-86562544f87661748ca7a140
    resource: repo://src/components/common/PrivacyShield.tsx
  - id: openwiki-source-415860a5cb2e00f0ef4be92e
    resource: repo://src/components/otp/HotpCard.tsx
  - id: openwiki-source-6d8c2e75c3e10bd2f5e82799
    resource: repo://src/components/otp/TotpCard.tsx
  - id: openwiki-source-d1a72d6b3b675365bc42eb04
    resource: repo://src/components/settings/AccountQrModal.tsx
  - id: openwiki-source-b02ea2fc21fbf14f70fd7b18
    resource: repo://src/components/settings/SettingsModal.tsx
  - id: openwiki-source-31e9a5c41aa2aaff08b86a38
    resource: repo://src/hooks/useVault.ts
  - id: openwiki-source-5e7c70a9ede4df532d719daa
    resource: repo://src/services/auth/biometricAuth.ts
  - id: openwiki-source-63a2bc3d5d23a8c8c55f26cf
    resource: repo://src/services/network/networkBlocker.ts
  - id: openwiki-source-8c21ae3e7d7c73961f08e54b
    resource: repo://src/services/security/biometrics.ts
  - id: openwiki-source-4800078744fac1a02b7139cc
    resource: repo://src/services/security/clipboardClear.ts
  - id: openwiki-source-aa9e9be64e0212a050b457e5
    resource: repo://src/services/security/privacyShield.ts
generated: { by: "openwiki/0.7.2", at: "2026-10-10T07:14:35.895Z" }
---

# Security boundaries and application lock lifecycle

Simple OTP has several separate security mechanisms, not one universal lock. The root layout installs a JavaScript network interceptor; the dashboard mounts an AppState-driven privacy cover; a biometric service owns native authentication and a persisted preference; clipboard copies receive a conditional expiry timer. Screen-capture prevention has an implementation but **no application caller enables it in the inspected `src` tree**.

These controls must not be confused with [encrypted-vault storage](encrypted-vault.md). `PrivacyShieldManager.isVaultLocked()` is a UI state: its unlock path changes flags and notifies listeners, rather than unlocking a cryptographic key or erasing decrypted accounts. `useVault` loads accounts on mount independently of biometric authentication. The overlay is therefore concealment and interaction gating, not a storage authorization boundary.

## Offline perimeter: installed early, limited to intercepted JavaScript APIs

[`src/app/_layout.tsx`](../../src/app/_layout.tsx) calls `installNetworkBlocker()` at module evaluation, before rendering the router stack. Installation is idempotent on the singleton. It replaces APIs present at installation time, saves originals for `uninstall()`, and resets its in-memory violation list on a new installation.

| API | Blocked-call behavior |
| --- | --- |
| `fetch` | Returns a rejected promise with `SECURITY_VIOLATION` |
| `XMLHttpRequest` | Throws in nonlocal `open()` and in `send()` unless a local resource was opened |
| `WebSocket`, `EventSource` | Constructor throws |
| `navigator.sendBeacon` | Returns `false` |

Blocked attempts record API, URL, optional method, and `Date.now()` timestamp; `getNetworkViolationLog()` returns a copied array. This is local diagnostics, not transmitted telemetry.

### Local-resource exception and test mode

Outside `NODE_ENV === 'test'`, **only `fetch` and XHR** allow URLs whose trimmed, lowercased strings start with `file:`, `blob:`, `data:`, `assets-library:`, `ph:`, or `/`. They delegate to the saved implementations. This is a string-prefix allowlist, not URL-origin validation: `/` also accepts strings beginning `//`. Bare relative names and `http://localhost` are not explicitly allowed. In test mode the local-resource predicate always returns `false`, so tests exercise a stricter policy than production. WebSocket, EventSource, and sendBeacon have no local exception.

The XHR replacement also makes header, abort, and event-listener methods no-ops, even for the local branch. Do not assume delegation preserves full XHR behavior when adding local-resource consumers.

**Scope:** this interceptor is not an OS firewall or proof that all native traffic is blocked. It covers calls through the replaced globals, not native SDK networking or previously retained references. New native dependencies and resource loaders require their own offline review. Keep the startup integration in the [runtime](runtime.md), but validate the actual device perimeter separately from JavaScript unit tests.

## Privacy cover ownership and placement

[`PrivacyShield`](../../src/components/common/PrivacyShield.tsx) starts the singleton manager's AppState listener, subscribes to `(isShielded, isLocked)`, and removes the subscription and listener on unmount. It returns `null` only when both flags are false. Otherwise it renders an opaque absolute-fill `View` with `pointerEvents="auto"`, `zIndex: 99999`, and `elevation: 99999`. Locked mode adds an unlock button with a loading/disabled state for manual retry.

The actual mount is the **last child of the dashboard's `SafeAreaView`**, after its modal components, not a router-wide overlay in `_layout.tsx`. High z-index orders views within that hierarchy; it does not establish coverage of separate native Modal presentations. For example, `AccountQrModal` presents secret-bearing QR content in React Native `Modal`, and contains no privacy-cover integration. Do not infer native-modal protection from the style comment claiming the cover is above all modals. Sensitive modal previews and touch blocking need device-level verification or a modal-aware integration.

The manager starts with both flags false. Initial biometric preference lookup is asynchronous; only after it resolves enabled does startup mark the UI shielded and locked. Consequently this is not a synchronous pre-render authentication gate.

## Application lifecycle and avoiding the Face ID loop

The manager distinguishes a temporary loss of focus from actual backgrounding. `inactive` synchronously updates the shield flag and notifies listeners, without independently locking. `background` additionally sets `wasInBackground`. On `active`, it ignores transitions during an ongoing biometric prompt or manager unlock, consumes the background marker, reads the preference, and checks that the app is still active after that asynchronous read.

```mermaid
sequenceDiagram
    participant OS as AppState
    participant PM as PrivacyShieldManager
    participant BS as Biometric service
    participant UI as PrivacyShield
    OS->>PM: inactive
    PM->>UI: Shield on, lock unchanged
    alt Only transient inactive
        OS->>PM: active
        PM->>BS: Read lock preference
        PM->>UI: Unshield if not already locked
        Note over PM,BS: No new Face ID prompt for transient inactive
    else Actual background
        OS->>PM: background
        Note over PM: Set wasInBackground and keep cover
        OS->>PM: active
        PM->>BS: Read lock preference
        Note over PM: Abort if no longer active
        alt Lock enabled
            PM->>UI: Shield on and locked
            PM->>BS: Authenticate with manager unlock guard
            Note over BS: Global biometric mutex rejects concurrent calls
            OS->>PM: inactive then active during prompt
            Note over PM: Keep cover on inactive, ignore active while authenticating
            alt Success and current state is not background
                BS-->>PM: success
                PM->>UI: Unlock and remove cover
            else Cancel, failure, or success while background
                BS-->>PM: unsuccessful unlock
                Note over PM,UI: Keep locked cover
                UI->>PM: User retries unlock
            end
            Note over PM,BS: Release both guards in finally
        else Lock disabled and not already locked
            PM->>UI: Remove cover
        end
    end
```
*AppState concealment and biometric retry flow, with separate manager and global authentication guards.*

The two defenses against the Face ID feedback loop are complementary:

- The biometric service sets a global `isAuthenticating` mutex **before availability checks**, rejects concurrent authentication with `already_authenticating`, and resets it in `finally`. The manager's `isUnlocking` prevents duplicate unlock attempts.
- Returning from `inactive` without recorded backgrounding does not request a fresh lock. This prevents the verification prompt used to enable biometrics from immediately causing another prompt on return to `active`.

Startup with the preference enabled sets the locked cover and automatically prompts only when the manager and native AppState indicate active (including the explicit unknown-state fallback). Cancel or failure leaves an already locked cover intact; the button can retry. Success removes the cover unless the **current** state is `background`. That guard intentionally allows success during `inactive`; it is not a requirement that success occur strictly in `active`.

## Biometric policy and failure semantics

[`biometrics.ts`](../../src/services/security/biometrics.ts) wraps `expo-local-authentication`. Availability checks hardware, enrollment, supported types, and enrolled security level. Missing hardware yields `not_available`; no enrollment yields `not_enrolled`. Availability exceptions become an unavailable result. Native prompts request `biometricsSecurityLevel: 'strong'` and `requireConfirmation: true`, with device PIN/passcode fallback enabled by default (`disableDeviceFallback: false`). Native failures retain error/warning information; thrown errors become unsuccessful results rather than escaping.

The lock preference is the SecureStore string `simpleotp_biometric_lock_enabled`; only the exact string `'true'` enables it. **A read error returns false**, so preference lookup is not fail-closed. Enabling checks availability and normally verifies authentication; disabling normally verifies too. Successful writes use `SecureStore.WHEN_UNLOCKED`. The public `verifyWithAuth` argument can bypass verification, but the Settings UI passes `true` for both directions. It reloads the current preference on failure and suppresses an error alert for `user_cancel`. Write failures return an error result.

[`BiometricAuth`](../../src/services/auth/biometricAuth.ts) is a facade over the same checks and authentication function, not a second lock implementation. New authentication consumers should share this mutex-bearing service rather than opening parallel native prompts.

## Screen capture: implemented service, missing activation

`enablePrivacyShield()` requests `preventScreenCaptureAsync('simpleotp_privacy_shield')`, then on iOS conditionally invokes `enableAppSwitcherProtectionAsync(0.8)`. Disable uses the matching key and optional iOS disable function. Both catch and silently ignore errors. `isScreenProtectionActive` changes only after the whole sequence succeeds, so partial native success followed by failure can leave the boolean out of sync with native protection.

The service describes Android `FLAG_SECURE` and iOS app-switcher blur as its intended platform mechanisms. However, neither `PrivacyShield` mounting nor `startListening()` calls enable or disable. Searching application source finds only the methods and their exported wrappers, while adversarial tests call those wrappers directly. **API presence and passing mocked tests do not mean screen-capture protection is enabled in the shipped application.**

Treat this as an integration gap, not as a guaranteed screenshot/recording barrier. A future owner must deliberately pair enable/disable with the intended lifetime, check native platform support, handle partial failures, and verify dashboard and native Modal behavior on real devices. Unsupported environments are currently tolerated silently, without a user-visible protection failure.

## Clipboard: conditional expiry, not guaranteed erasure

TOTP and HOTP cards call `copyWithAutoClear(code)`; the QR export modal calls it with the whitespace-stripped account secret. The singleton owns one tracked token and deadline. A new copy cancels the old timer and starts a fresh **30,000 ms** interval by default; callers can supply another delay. Empty copies return `false` without scheduling.

Expiry clears to `''` only if the clipboard still contains the tracked token, preserving a user's replacement text. If `hasStringAsync` reports no string it skips the wipe. On `active` resume it compares wall-clock elapsed time with the deadline: overdue content is checked immediately, otherwise the timer is rearmed for the remaining duration. There is no immediate wipe simply on backgrounding, and suspended JavaScript is not a guaranteed 30-second execution deadline.

`cancelClipboardClear()` cancels tracking **without wiping**. `clearClipboardImmediately()` cancels tracking and attempts an unconditional wipe. Tracking is reset before conditional clipboard reads/writes, so a failed clear is not automatically retried. Clipboard operation failures are caught and logged with `console.warn`; AppState listener setup failures are silently ignored.

Missing platform API functions are skipped: a missing setter can still let `copyWithAutoClear` report success and schedule, while a missing getter skips the equality check before any available setter. This defensive behavior accommodates incomplete environments but weakens the preservation guarantee. The normal UI callers await the helper without checking its boolean result; QR copy feedback can therefore appear even after a handled write failure.

Clipboard expiry cannot retract text already pasted, read by another application, or retained externally. Its tracking state is in memory, not a persistent OS deletion job. Review new secret-copy entrypoints to ensure they use this helper, and do not present it as durable erasure.

## Validation and safe changes

The relevant tests are executable specifications of service behavior, not proof of native enforcement:

- [`biometricLoopFix.test.ts`](../../__tests__/unit/biometricLoopFix.test.ts) exercises mutex rejection, enabling-lock Face ID without looping, real background resume, and transient inactive events.
- [`clipboardClear.test.ts`](../../__tests__/unit/clipboardClear.test.ts) checks the exact 30-second threshold, replacement preservation, second-copy rescheduling, overdue resume, cancellation without wiping, and handled clipboard failures.
- [`networkBlocker.test.ts`](../../__tests__/unit/networkBlocker.test.ts) checks the five interception surfaces, violation logging, idempotent installation, and restoration on uninstall. Remember that `NODE_ENV === 'test'` disables the production local allowlist.
- [`tier5_security_ui_hardening.test.tsx`](../../__tests__/adversarial/tier5_security_ui_hardening.test.tsx) adds startup active/background branches, AppState listener cleanup, asynchronous background races, SecureStore failures, direct screen-capture wrapper calls, and clipboard resume branches. Its native modules are mocked.

When extending security behavior, preserve the distinction between focus loss and backgrounding, keep both authentication guards, and test cancellation/retry and state changes across asynchronous reads. Add native-modal and screen-capture device checks rather than relying on React view order or mocks. See [validation](../testing/validation.md), [build and release](../operations/build-and-release.md), and [backup and transfer](../workflows/backup-and-transfer.md) for the adjacent testing, deployment, and intentional secret-export boundaries.
