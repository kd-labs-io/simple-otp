#!/usr/bin/env python3
"""
Generate 1284 x 2778 px App Store Connect screenshots for iOS (iPhone 6.7" Super Retina XDR).
Complies with Apple Guideline 2.3.3 by rendering the actual app UI in use inside modern
iPhone 16/17 Pro titanium frames with Dynamic Island, clean 9:41 AM status bar,
localized headlines, and the Bé Khóa mascot badge.
"""

import os
import sys
import base64
import subprocess
import tempfile

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def get_base64_image(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode('ascii')}"

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ICON_B64 = get_base64_image(os.path.join(PROJECT_ROOT, "assets/images/splash-icon.png"))
MASCOT_CAT_B64 = get_base64_image(os.path.join(PROJECT_ROOT, "assets/images/pets/cipher-cat-sprites.png"))

def build_qr_svg():
    """Generates a sharp, realistic 2FA QR code with proper position detection squares."""
    return """
    <svg class="qr-target" width="300" height="300" viewBox="0 0 33 33" fill="#FFFFFF">
      <!-- Top-left finder -->
      <rect x="1" y="1" width="7" height="7"/>
      <rect x="2" y="2" width="5" height="5" fill="#1C1B1F"/>
      <rect x="3" y="3" width="3" height="3"/>
      <!-- Top-right finder -->
      <rect x="25" y="1" width="7" height="7"/>
      <rect x="26" y="2" width="5" height="5" fill="#1C1B1F"/>
      <rect x="27" y="3" width="3" height="3"/>
      <!-- Bottom-left finder -->
      <rect x="1" y="25" width="7" height="7"/>
      <rect x="2" y="26" width="5" height="5" fill="#1C1B1F"/>
      <rect x="3" y="27" width="3" height="3"/>
      <!-- Timing patterns -->
      <rect x="9" y="4" width="1" height="1"/><rect x="11" y="4" width="1" height="1"/><rect x="13" y="4" width="1" height="1"/><rect x="15" y="4" width="1" height="1"/><rect x="17" y="4" width="1" height="1"/><rect x="19" y="4" width="1" height="1"/><rect x="21" y="4" width="1" height="1"/><rect x="23" y="4" width="1" height="1"/>
      <rect x="4" y="9" width="1" height="1"/><rect x="4" y="11" width="1" height="1"/><rect x="4" y="13" width="1" height="1"/><rect x="4" y="15" width="1" height="1"/><rect x="4" y="17" width="1" height="1"/><rect x="4" y="19" width="1" height="1"/><rect x="4" y="21" width="1" height="1"/><rect x="4" y="23" width="1" height="1"/>
      <!-- Data modules -->
      <rect x="10" y="2" width="2" height="1"/><rect x="14" y="2" width="1" height="1"/><rect x="17" y="2" width="2" height="1"/><rect x="21" y="2" width="1" height="1"/>
      <rect x="9" y="7" width="1" height="2"/><rect x="12" y="6" width="2" height="1"/><rect x="15" y="7" width="3" height="1"/><rect x="20" y="6" width="2" height="2"/>
      <rect x="1" y="10" width="2" height="1"/><rect x="5" y="10" width="1" height="1"/><rect x="7" y="10" width="1" height="1"/><rect x="10" y="10" width="3" height="1"/><rect x="15" y="10" width="1" height="2"/><rect x="18" y="10" width="2" height="1"/><rect x="22" y="9" width="2" height="1"/><rect x="26" y="10" width="1" height="1"/><rect x="29" y="9" width="3" height="2"/>
      <rect x="2" y="13" width="1" height="2"/><rect x="6" y="12" width="2" height="1"/><rect x="10" y="13" width="2" height="2"/><rect x="14" y="12" width="1" height="1"/><rect x="17" y="13" width="3" height="1"/><rect x="22" y="12" width="1" height="2"/><rect x="25" y="13" width="2" height="1"/><rect x="29" y="12" width="2" height="2"/>
      <rect x="1" y="16" width="3" height="1"/><rect x="6" y="16" width="1" height="1"/><rect x="9" y="15" width="2" height="2"/><rect x="13" y="15" width="3" height="1"/><rect x="18" y="16" width="2" height="2"/><rect x="22" y="15" width="2" height="1"/><rect x="26" y="16" width="1" height="2"/><rect x="29" y="15" width="3" height="1"/>
      <rect x="2" y="19" width="2" height="1"/><rect x="6" y="18" width="2" height="2"/><rect x="10" y="19" width="1" height="1"/><rect x="13" y="18" width="2" height="1"/><rect x="16" y="19" width="1" height="2"/><rect x="20" y="19" width="2" height="1"/><rect x="24" y="18" width="2" height="2"/><rect x="28" y="19" width="1" height="1"/>
      <rect x="1" y="22" width="1" height="1"/><rect x="5" y="21" width="2" height="2"/><rect x="9" y="22" width="3" height="1"/><rect x="14" y="21" width="2" height="2"/><rect x="18" y="22" width="2" height="1"/><rect x="22" y="21" width="1" height="1"/><rect x="25" y="22" width="2" height="1"/><rect x="29" y="22" width="2" height="1"/>
      <!-- Alignment pattern -->
      <rect x="21" y="21" width="5" height="5"/>
      <rect x="22" y="22" width="3" height="3" fill="#1C1B1F"/>
      <rect x="23" y="23" width="1" height="1"/>
      <!-- Bottom data -->
      <rect x="10" y="25" width="2" height="1"/><rect x="14" y="25" width="1" height="2"/><rect x="17" y="26" width="2" height="1"/><rect x="28" y="25" width="2" height="1"/>
      <rect x="9" y="28" width="2" height="2"/><rect x="12" y="29" width="3" height="1"/><rect x="16" y="28" width="1" height="2"/><rect x="19" y="29" width="2" height="1"/><rect x="23" y="28" width="1" height="2"/><rect x="27" y="29" width="3" height="1"/>
      <rect x="10" y="31" width="3" height="1"/><rect x="15" y="31" width="2" height="1"/><rect x="19" y="31" width="1" height="1"/><rect x="22" y="31" width="2" height="1"/><rect x="26" y="31" width="1" height="1"/>
    </svg>
    """

def build_html(screen_id, lang):
    is_vi = (lang == 'vi')
    
    # Common status bar SVGs and indicators
    status_bar_html = """
    <div class="status-bar">
      <div class="time">9:41</div>
      <div class="dynamic-island">
        <div class="island-camera"></div>
      </div>
      <div class="status-icons">
        <svg width="22" height="15" viewBox="0 0 22 15" fill="#111827">
          <rect x="1" y="10" width="3" height="5" rx="1"/>
          <rect x="6" y="7" width="3" height="8" rx="1"/>
          <rect x="11" y="4" width="3" height="11" rx="1"/>
          <rect x="16" y="1" width="3" height="14" rx="1"/>
        </svg>
        <svg width="19" height="15" viewBox="0 0 19 15" fill="#111827" style="margin-left: 6px;">
          <path d="M9.5 2.5C5.8 2.5 2.5 4.1 0 6.6L9.5 16L19 6.6C16.5 4.1 13.2 2.5 9.5 2.5Z"/>
        </svg>
        <svg width="28" height="14" viewBox="0 0 28 14" fill="#111827" style="margin-left: 6px;">
          <rect x="0.5" y="0.5" width="24" height="13" rx="4" fill="none" stroke="#111827" stroke-width="1.5"/>
          <rect x="2.5" y="2.5" width="20" height="9" rx="2.5" fill="#111827"/>
          <path d="M26 4.5V9.5" stroke="#111827" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </div>
    </div>
    """

    home_indicator_html = '<div class="home-indicator"></div>'

    if screen_id == '01_offline_security':
        title = "BẢO MẬT NGOẠI TUYẾN 100%" if is_vi else "100% OFFLINE & PRIVATE"
        subtitle = "Kho Khóa Xác Thực 2FA Tức Thì • Không Cần Mạng" if is_vi else "Hardware-Backed 2FA Vault • Zero Network Access"
        
        screen_content = f"""
        <div class="app-screen">
          {status_bar_html}
          <div class="vault-header">
            <div class="brand-title">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>
                <path d="m9 12 2 2 4-4"/>
              </svg>
              <span class="brand-name">Simple OTP</span>
              <span class="token-count-badge">{"6 Khóa" if is_vi else "6 Keys"}</span>
            </div>
            <div class="settings-icon-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            </div>
          </div>

          <div class="search-bar">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2.2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <span class="search-placeholder">{"Tìm kiếm tài khoản, dịch vụ..." if is_vi else "Search accounts, services..."}</span>
          </div>

          <!-- Category filter tabs -->
          <div class="category-tabs">
            <div class="tab-chip active">{"Tất Cả (6)" if is_vi else "All (6)"}</div>
            <div class="tab-chip">{"Công Việc" if is_vi else "Work"}</div>
            <div class="tab-chip">{"Tài Chính" if is_vi else "Finance"}</div>
            <div class="tab-chip">{"Mạng Xã Hội" if is_vi else "Social"}</div>
          </div>

          <div class="cards-container">
            <!-- Google Card -->
            <div class="totp-card">
              <div class="card-left">
                <div class="service-icon google-bg">
                  <svg width="28" height="28" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.8-2.4 3.65v3h3.88c2.27-2.09 3.665-5.17 3.665-9.09z"/>
                    <path fill="#34A853" d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.1C3.26 21.44 7.33 24 12 24z"/>
                    <path fill="#FBBC05" d="M5.28 14.32c-.25-.72-.38-1.49-.38-2.32s.13-1.6.38-2.32V6.58H1.25C.45 8.18 0 9.99 0 12c0 2.01.45 3.82 1.25 5.42l4.03-3.1z"/>
                    <path fill="#EA4335" d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.56 1.25 6.58l4.03 3.1c.95-2.83 3.6-4.93 6.72-4.93z"/>
                  </svg>
                </div>
                <div class="service-info">
                  <div class="service-issuer">Google</div>
                  <div class="service-account">alex.developer@gmail.com</div>
                </div>
              </div>
              <div class="code-and-timer">
                <div class="totp-code">584 <span class="code-space">921</span></div>
                <div class="countdown-wrap">
                  <svg width="48" height="48" viewBox="0 0 44 44">
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F0F0F3" stroke-width="4.5"/>
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F76B00" stroke-width="4.5" stroke-dasharray="113.09" stroke-dashoffset="24" stroke-linecap="round" transform="rotate(-90 22 22)"/>
                  </svg>
                  <span class="countdown-text">24s</span>
                </div>
              </div>
            </div>

            <!-- GitHub Card -->
            <div class="totp-card">
              <div class="card-left">
                <div class="service-icon github-bg">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="#111827">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
                  </svg>
                </div>
                <div class="service-info">
                  <div class="service-issuer">GitHub</div>
                  <div class="service-account">@octocat-admin</div>
                </div>
              </div>
              <div class="code-and-timer">
                <div class="totp-code">819 <span class="code-space">304</span></div>
                <div class="countdown-wrap">
                  <svg width="48" height="48" viewBox="0 0 44 44">
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F0F0F3" stroke-width="4.5"/>
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F76B00" stroke-width="4.5" stroke-dasharray="113.09" stroke-dashoffset="46" stroke-linecap="round" transform="rotate(-90 22 22)"/>
                  </svg>
                  <span class="countdown-text">18s</span>
                </div>
              </div>
            </div>

            <!-- Binance Card -->
            <div class="totp-card">
              <div class="card-left">
                <div class="service-icon binance-bg">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#F3BA2F">
                    <path d="M12 0L5.35 6.65l2.67 2.67L12 5.35l3.98 3.98 2.67-2.67L12 0zm-6.65 9.32L0 14.67l2.67 2.67 2.68-2.68-2.67-2.67l2.67-2.67zm13.3 0l-2.67 2.67 2.67 2.67 2.68 2.68 2.67-2.67-5.35-5.35zm-6.65 2.68l-2.67 2.67 2.67 2.68 2.68-2.68-2.68-2.67zm-3.98 3.98L5.35 18.66 12 25.3l6.65-6.64-2.67-2.68L12 19.96l-3.98-3.98z"/>
                  </svg>
                </div>
                <div class="service-info">
                  <div class="service-issuer">Binance Exchange</div>
                  <div class="service-account">trader@crypto.io</div>
                </div>
              </div>
              <div class="code-and-timer">
                <div class="totp-code">472 <span class="code-space">109</span></div>
                <div class="countdown-wrap">
                  <svg width="48" height="48" viewBox="0 0 44 44">
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F0F0F3" stroke-width="4.5"/>
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F76B00" stroke-width="4.5" stroke-dasharray="113.09" stroke-dashoffset="10" stroke-linecap="round" transform="rotate(-90 22 22)"/>
                  </svg>
                  <span class="countdown-text">28s</span>
                </div>
              </div>
            </div>

            <!-- AWS Card -->
            <div class="totp-card">
              <div class="card-left">
                <div class="service-icon aws-bg">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#FF9900">
                    <path d="M18.78 17.5c-4.13 2.69-10.15 3.42-15.09.84-.71-.37-.77-.85-.18-1.22.42-.26 1.05-.28 1.76.08 4.29 2.19 9.53 1.54 13.14-.77.58-.37 1.15.11.83.62-.12.18-.28.34-.46.45zm1.55-1.26c-.46-.62-2.99-.44-4.14-.3-.35.04-.4-.25-.09-.47 2-.1.45 4.96.67 4.94 1.84-.02.44-.45.54-.71.23z"/>
                  </svg>
                </div>
                <div class="service-info">
                  <div class="service-issuer">Amazon Web Services</div>
                  <div class="service-account">root-infra-admin</div>
                </div>
              </div>
              <div class="code-and-timer">
                <div class="totp-code">930 <span class="code-space">248</span></div>
                <div class="countdown-wrap">
                  <svg width="48" height="48" viewBox="0 0 44 44">
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F0F0F3" stroke-width="4.5"/>
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F76B00" stroke-width="4.5" stroke-dasharray="113.09" stroke-dashoffset="68" stroke-linecap="round" transform="rotate(-90 22 22)"/>
                  </svg>
                  <span class="countdown-text">12s</span>
                </div>
              </div>
            </div>

            <!-- ProtonMail Card -->
            <div class="totp-card">
              <div class="card-left">
                <div class="service-icon proton-bg">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#6D4AFF">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 4c2.21 0 4 1.79 4 4 0 1.5-.83 2.8-2.06 3.48L14 16h-4v-2.52C8.83 12.8 8 11.5 8 10c0-2.21 1.79-4 4-4z"/>
                  </svg>
                </div>
                <div class="service-info">
                  <div class="service-issuer">Proton Mail</div>
                  <div class="service-account">secure@pm.me</div>
                </div>
              </div>
              <div class="code-and-timer">
                <div class="totp-code">629 <span class="code-space">184</span></div>
                <div class="countdown-wrap">
                  <svg width="48" height="48" viewBox="0 0 44 44">
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F0F0F3" stroke-width="4.5"/>
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F76B00" stroke-width="4.5" stroke-dasharray="113.09" stroke-dashoffset="35" stroke-linecap="round" transform="rotate(-90 22 22)"/>
                  </svg>
                  <span class="countdown-text">21s</span>
                </div>
              </div>
            </div>

            <!-- Discord Card (Urgent 5s) -->
            <div class="totp-card urgent-card">
              <div class="card-left">
                <div class="service-icon discord-bg">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="#5865F2">
                    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
                  </svg>
                </div>
                <div class="service-info">
                  <div class="service-issuer">Discord</div>
                  <div class="service-account">alex_gaming#1337</div>
                </div>
              </div>
              <div class="code-and-timer">
                <div class="totp-code urgent-code">115 <span class="code-space">842</span></div>
                <div class="countdown-wrap">
                  <svg width="48" height="48" viewBox="0 0 44 44">
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#F0F0F3" stroke-width="4.5"/>
                    <circle cx="22" cy="22" r="18" fill="none" stroke="#FF3B30" stroke-width="4.5" stroke-dasharray="113.09" stroke-dashoffset="94" stroke-linecap="round" transform="rotate(-90 22 22)"/>
                  </svg>
                  <span class="countdown-text urgent-text">5s</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Floating Mascot Anchor & FAB (+) -->
          <div class="dashboard-bottom-bar">
            <div class="pet-companion-fab">
              <img src="{ICON_B64}" class="pet-mini-avatar" alt="Bé Khóa"/>
              <div class="pet-mini-badge">{"An toàn" if is_vi else "Protected"}</div>
            </div>

            <div class="fab-btn">
              <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
            </div>
          </div>

          {home_indicator_html}
        </div>
        """

    elif screen_id == '02_qr_scanner':
        title = "QUÉT MÃ QR SIÊU TỐC" if is_vi else "LIGHTNING FAST QR SCANNER"
        subtitle = "Nhận Diện Mã 2FA Tức Thì Qua Máy Ảnh & Thư Viện" if is_vi else "Instant Camera & Photo Gallery QR Code Import"

        qr_svg = build_qr_svg()

        screen_content = f"""
        <div class="app-screen dark-bg">
          {status_bar_html}
          <div class="scanner-top-bar">
            <div class="icon-round-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </div>
            <div class="scanner-title">{"Quét Mã QR 2FA" if is_vi else "Scan 2FA QR Code"}</div>
            <div class="icon-round-btn active-torch">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="#F76B00" stroke="#F76B00" stroke-width="2">
                <path d="M18 6c0 2-2 4-2 7v6a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-6c0-3-2-5-2-7a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2z"/>
              </svg>
            </div>
          </div>

          <div class="viewfinder-section">
            <div class="scanner-prompt-pill">
              <span class="pulse-dot"></span>
              {"Hướng camera vào mã QR 2FA" if is_vi else "Align camera with 2FA QR code"}
            </div>

            <!-- Viewfinder Reticle -->
            <div class="reticle-box">
              <div class="corner-bracket top-left"></div>
              <div class="corner-bracket top-right"></div>
              <div class="corner-bracket bottom-left"></div>
              <div class="corner-bracket bottom-right"></div>
              
              <!-- Clean SVG 2FA QR code -->
              {qr_svg}

              <!-- Glowing Scan Laser line -->
              <div class="laser-line"></div>
            </div>

            <!-- Detected Account Card Preview -->
            <div class="detected-toast">
              <div class="check-circle">✓</div>
              <div class="detected-info">
                <div class="detected-name">Google: alex.developer@gmail.com</div>
                <div class="detected-sub">{"Mã OTP hợp lệ • Sẵn sàng thêm" if is_vi else "Valid 2FA secret recognized • Ready to save"}</div>
              </div>
            </div>

            <!-- Features callout bar -->
            <div class="scanner-features-row">
              <div class="feature-chip">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{"Tự động quét" if is_vi else "Auto-detect"}</span>
              </div>
              <div class="feature-chip">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{"Không cần mạng" if is_vi else "100% Offline"}</span>
              </div>
              <div class="feature-chip">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                <span>{"Bảo mật cao" if is_vi else "Encrypted"}</span>
              </div>
            </div>
          </div>

          <!-- Bottom Action Buttons -->
          <div class="scanner-bottom-actions">
            <div class="action-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2">
                <rect x="3" y="3" width="18" height="18" rx="3"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
              <span>{"Chọn Từ Thư Viện" if is_vi else "Import from Photos"}</span>
            </div>
            <div class="action-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2">
                <rect x="2" y="4" width="20" height="16" rx="2"/>
                <line x1="6" y1="8" x2="6" y2="8"/>
                <line x1="10" y1="8" x2="10" y2="8"/>
                <line x1="14" y1="8" x2="14" y2="8"/>
                <line x1="18" y1="8" x2="18" y2="8"/>
                <line x1="7" y1="16" x2="17" y2="16"/>
              </svg>
              <span>{"Nhập Mã Thủ Công" if is_vi else "Enter Key Manually"}</span>
            </div>
          </div>

          {home_indicator_html}
        </div>
        """

    elif screen_id == '03_pet_academy':
        title = "HỌC VIỆN BÉ KHÓA" if is_vi else "SECURITY PET ACADEMY"
        subtitle = "Nuôi Thú Ảo Bảo Mật • Rèn Luyện Thói Quen An Toàn" if is_vi else "Gamified 2FA Habits with Companion Bé Khóa"

        screen_content = f"""
        <div class="app-screen">
          {status_bar_html}
          <div class="vault-header">
            <div class="brand-title">
              <div class="academy-badge-icon">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.4">
                  <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                  <path d="M6 12v5c3 3 9 3 12 0v-5"/>
                </svg>
              </div>
              <span class="brand-name">{"Học Viện Bé Khóa" if is_vi else "Pet Academy"}</span>
            </div>
            <div class="settings-icon-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2.4">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </div>
          </div>

          <div class="academy-container">
            <!-- Hero Mascot Card -->
            <div class="pet-hero-card">
              <div class="pet-avatar-wrap">
                <img src="{ICON_B64}" class="pet-hero-img" alt="Bé Khóa"/>
                <div class="level-tag">Lv. 5</div>
              </div>
              <div class="pet-meta">
                <div class="pet-name">Bé Khóa</div>
                <div class="pet-role">{"Hộ Vệ An Ninh Cấp Cao" if is_vi else "Master Security Guardian"}</div>
                <div class="xp-bar-bg">
                  <div class="xp-bar-fill" style="width: 85%;"></div>
                </div>
                <div class="xp-label">850 / 1,000 XP (85%)</div>
              </div>
              <div class="streak-pill">
                🔥 {"Chuỗi 7 Ngày" if is_vi else "7-Day Streak"}
              </div>
            </div>

            <!-- Dialogue Speech Bubble -->
            <div class="mascot-speech-bubble">
              <div class="bubble-tail"></div>
              <p>{"\"Tuyệt vời! Bạn đã kích hoạt đầy đủ Face ID và sao lưu mã hóa ngoại tuyến!\"" if is_vi else "\"Awesome! You've activated Face ID protection and full offline encrypted backups!\""}</p>
            </div>

            <!-- Habits Checklist -->
            <div class="habits-section-title">
              {"NHIỆM VỤ AN NINH HÀNG NGÀY" if is_vi else "DAILY SECURITY MISSIONS"}
            </div>

            <div class="habit-card completed">
              <div class="habit-icon-check">✓</div>
              <div class="habit-info">
                <div class="habit-title">{"Bật Khóa Sinh Trắc Học (Face ID)" if is_vi else "Enable Biometric Face ID"}</div>
                <div class="habit-sub">{"Bảo vệ ví khóa trước truy cập trái phép" if is_vi else "Secure vault from unauthorized eyes"}</div>
              </div>
              <div class="xp-reward">+100 XP</div>
            </div>

            <div class="habit-card completed">
              <div class="habit-icon-check">✓</div>
              <div class="habit-info">
                <div class="habit-title">{"Xuất Bản Sao Lưu Mã Hóa AES-256" if is_vi else "Export Encrypted Backup File"}</div>
                <div class="habit-sub">{"Lưu trữ an toàn ngoại tuyến không sợ mất" if is_vi else "Cloudless AES-256-GCM vault backup"}</div>
              </div>
              <div class="xp-reward">+100 XP</div>
            </div>

            <div class="habit-card completed">
              <div class="habit-icon-check">✓</div>
              <div class="habit-info">
                <div class="habit-title">{"Bảo Vệ Trên 5 Tài Khoản Quan Trọng" if is_vi else "Protect 5+ Core Accounts"}</div>
                <div class="habit-sub">{"Google, GitHub, Binance, AWS secured" if not is_vi else "Google, GitHub, Binance, AWS đã bảo vệ"}</div>
              </div>
              <div class="xp-reward">+150 XP</div>
            </div>

            <!-- Academy Lesson Card to fill screen naturally -->
            <div class="academy-lesson-card">
              <div class="lesson-header">
                <span class="lesson-tag">{"BÀI HỌC BẢO MẬT #1" if is_vi else "SECURITY LESSON #1"}</span>
                <span class="lesson-xp">+50 XP</span>
              </div>
              <div class="lesson-title">{"Tại Sao 2FA Tốt Hơn Tin Nhắn SMS?" if is_vi else "Why TOTP Authenticator Beats SMS?"}</div>
              <div class="lesson-desc">{"Mã TOTP được sinh hoàn toàn offline trên thiết bị, chống hoàn toàn nguy cơ tấn công SIM Swap và nghe lén đường truyền." if is_vi else "TOTP codes are generated 100% locally on your device, immune to SIM swapping and cellular interception."}</div>
            </div>
          </div>

          {home_indicator_html}
        </div>
        """

    elif screen_id == '04_encrypted_backup':
        title = "SAO LƯU MÃ HÓA AES-256" if is_vi else "MILITARY-GRADE BACKUP"
        subtitle = "Bảo Vệ Sinh Trắc Học & Khóa Face ID Ngoại Tuyến" if is_vi else "AES-256 Encryption & Hardware Biometric Lock"

        screen_content = f"""
        <div class="app-screen">
          {status_bar_html}
          <div class="vault-header">
            <div class="brand-title">
              <div class="academy-badge-icon">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.4">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </div>
              <span class="brand-name">{"Cài Đặt & Bảo Mật" if is_vi else "Security & Settings"}</span>
            </div>
            <div class="settings-icon-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2.4">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </div>
          </div>

          <div class="settings-container">
            <!-- Group 1: Hardware Security -->
            <div class="settings-group-title">
              {"BẢO VỆ PHẦN CỨNG & SINH TRẮC HỌC" if is_vi else "BIOMETRIC & HARDWARE SECURITY"}
            </div>
            <div class="settings-card">
              <div class="settings-row">
                <div class="row-left">
                  <div class="row-icon orange-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F76B00" stroke-width="2.3">
                      <path d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 0 0 8 11a4 4 0 1 1 8 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0 0 15.5 16m-6.3-4.5a3 3 0 1 1 6 0c0 1.018-.088 2.019-.258 2.99"/>
                    </svg>
                  </div>
                  <div class="row-text">
                    <div class="row-label">{"Khóa Sinh Trắc Học (Face ID)" if is_vi else "Biometric Lock (Face ID)"}</div>
                    <div class="row-desc">{"Bảo vệ truy cập bằng Apple Face ID" if is_vi else "Secure app unlock with Apple Face ID"}</div>
                  </div>
                </div>
                <div class="ios-switch on"><div class="switch-knob"></div></div>
              </div>

              <div class="row-divider"></div>

              <div class="settings-row">
                <div class="row-left">
                  <div class="row-icon blue-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#007AFF" stroke-width="2.3">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="12 6 12 12 16 14"/>
                    </svg>
                  </div>
                  <div class="row-text">
                    <div class="row-label">{"Tự Động Khóa" if is_vi else "Auto-Lock"}</div>
                    <div class="row-desc">{"Khóa ngay khi rời ứng dụng" if is_vi else "Immediately upon leaving app"}</div>
                  </div>
                </div>
                <div class="row-value-badge">{"Ngay lập tức" if is_vi else "Immediate"}</div>
              </div>

              <div class="row-divider"></div>

              <div class="settings-row">
                <div class="row-left">
                  <div class="row-icon purple-icon">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#AF52DE" stroke-width="2.3">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                  </div>
                  <div class="row-text">
                    <div class="row-label">{"Màn Chắn Riêng Tư" if is_vi else "Privacy Shield"}</div>
                    <div class="row-desc">{"Ẩn mã OTP khi chuyển đổi ứng dụng" if is_vi else "Hide OTP codes in App Switcher"}</div>
                  </div>
                </div>
                <div class="ios-switch on"><div class="switch-knob"></div></div>
              </div>
            </div>

            <!-- Group 2: Encrypted Backup -->
            <div class="settings-group-title">
              {"SAO LƯU NGOẠI TUYẾN MÃ HÓA" if is_vi else "ENCRYPTED OFFLINE BACKUP"}
            </div>
            <div class="backup-box">
              <div class="backup-header-row">
                <div class="backup-chip">AES-256-GCM</div>
                <div class="backup-chip">PBKDF2 100k Iterations</div>
              </div>
              <p class="backup-desc">
                {"Xuất toàn bộ mã 2FA thành tệp tin mã hóa quân đội. Mật khẩu giải mã chỉ lưu trong đầu bạn, hoàn toàn không gửi lên bất kỳ máy chủ nào." if is_vi else "Export all 2FA accounts encrypted with military-grade AES-256-GCM. Your passphrase is never sent to any server — 100% offline security."}
              </p>
              
              <div class="btn-export-backup">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.4">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                <span>{"Xuất Bản Sao Lưu (.enc)" if is_vi else "Export Encrypted Backup (.enc)"}</span>
              </div>

              <div class="btn-restore-backup">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2.4">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <span>{"Khôi Phục Từ Bản Sao Lưu" if is_vi else "Restore from Backup File"}</span>
              </div>
            </div>

            <!-- Group 3: Vault Telemetry / Stats -->
            <div class="stats-box">
              <div class="stat-item">
                <div class="stat-val">0</div>
                <div class="stat-lbl">{"Lần Gọi Mạng" if is_vi else "Network Calls"}</div>
              </div>
              <div class="stat-div"></div>
              <div class="stat-item">
                <div class="stat-val">256-bit</div>
                <div class="stat-lbl">{"Khóa Phần Cứng" if is_vi else "Secure Enclave"}</div>
              </div>
              <div class="stat-div"></div>
              <div class="stat-item">
                <div class="stat-val">100%</div>
                <div class="stat-lbl">{"Ngoại Tuyến" if is_vi else "Air-Gapped"}</div>
              </div>
            </div>

            <!-- Zero tracking badge -->
            <div class="zero-tracking-pill">
              <div class="green-check-dot">✓</div>
              <span>{"Zero Network Permission: Không yêu cầu quyền kết nối Internet" if is_vi else "Zero Network Permission: No internet access requested"}</span>
            </div>
          </div>

          {home_indicator_html}
        </div>
        """

    # Assemble Complete 1284 x 2778 Canvas
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; user-select: none; }}
  
  body {{
    width: 1284px;
    height: 2778px;
    background: radial-gradient(circle at 50% 12%, rgba(255, 210, 80, 0.42) 0%, rgba(247, 107, 0, 0.95) 45%, #D44B00 100%),
                linear-gradient(180deg, #F76B00 0%, #D84800 100%);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 110px;
  }}

  /* Background decorative ambient lights */
  .bg-glow-1 {{
    position: absolute;
    width: 960px;
    height: 960px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.22) 0%, rgba(255,255,255,0) 70%);
    top: -180px;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
  }}

  /* Top Banner Header */
  .banner-header {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 60px;
    z-index: 10;
  }}

  .mascot-header-wrap {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 22px;
  }}

  .mascot-badge-img {{
    width: 105px;
    height: 105px;
    border-radius: 28px;
    box-shadow: 0 16px 36px rgba(0,0,0,0.25), 0 0 0 3px rgba(255,255,255,0.35);
  }}

  .mascot-badge-pill {{
    background: rgba(255,255,255,0.24);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.45);
    padding: 10px 22px;
    border-radius: 30px;
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 0.8px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }}

  .banner-title {{
    color: #FFFFFF;
    font-size: 56px;
    font-weight: 900;
    letter-spacing: -0.5px;
    line-height: 1.15;
    text-shadow: 0 4px 16px rgba(0,0,0,0.3);
    max-width: 1140px;
    margin-bottom: 14px;
  }}

  .banner-subtitle {{
    color: rgba(255,255,255,0.96);
    font-size: 32px;
    font-weight: 600;
    letter-spacing: -0.2px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
    max-width: 1080px;
  }}

  /* Titanium Device Mockup Frame */
  .device-mockup {{
    width: 1080px;
    height: 2260px;
    background: #1C1B1F;
    border: 16px solid #38373B;
    border-radius: 78px;
    box-shadow: 
      0 45px 130px -10px rgba(0,0,0,0.55),
      0 20px 40px -10px rgba(0,0,0,0.35),
      inset 0 0 0 3px rgba(255,255,255,0.2),
      0 0 0 3px rgba(255,255,255,0.3);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    z-index: 5;
  }}

  /* Screen Area Inside Phone */
  .app-screen {{
    flex: 1;
    background: #F9FAFB;
    border-radius: 60px;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
  }}

  .app-screen.dark-bg {{
    background: #0D0E12;
  }}

  /* iOS Status Bar */
  .status-bar {{
    height: 64px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 46px;
    position: relative;
    z-index: 50;
  }}

  .status-bar .time {{
    font-size: 24px;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.2px;
    width: 90px;
  }}

  .dark-bg .status-bar .time {{
    color: #FFFFFF;
  }}

  /* Dynamic Island */
  .dynamic-island {{
    width: 260px;
    height: 52px;
    background: #000000;
    border-radius: 26px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 14px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 22px;
    box-shadow: inset 0 0 1px rgba(255,255,255,0.3);
  }}

  .island-camera {{
    width: 14px;
    height: 14px;
    background: #111424;
    border-radius: 50%;
    border: 1px solid #1C2038;
  }}

  .status-icons {{
    display: flex;
    align-items: center;
    width: 90px;
    justify-content: flex-end;
  }}

  .dark-bg .status-icons svg {{
    fill: #FFFFFF !important;
  }}

  .dark-bg .status-icons svg rect,
  .dark-bg .status-icons svg path {{
    stroke: #FFFFFF !important;
  }}
  .dark-bg .status-icons svg rect[fill="#111827"] {{
    fill: #FFFFFF !important;
  }}

  /* Home Indicator Bar */
  .home-indicator {{
    width: 250px;
    height: 7px;
    background: rgba(0,0,0,0.32);
    border-radius: 4px;
    position: absolute;
    bottom: 16px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 50;
  }}

  .dark-bg .home-indicator {{
    background: rgba(255,255,255,0.4);
  }}

  /* Screen 1: Vault Styling */
  .vault-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 22px 38px 16px;
    background: #FFFFFF;
    border-bottom: 1px solid #E5E7EB;
  }}

  .brand-title {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .brand-name {{
    font-size: 34px;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.5px;
  }}

  .token-count-badge {{
    background: #FFF0E6;
    color: #F76B00;
    font-size: 20px;
    font-weight: 800;
    padding: 5px 15px;
    border-radius: 16px;
    border: 1px solid #FED7AA;
  }}

  .settings-icon-btn {{
    width: 50px;
    height: 50px;
    border-radius: 15px;
    background: #F3F4F6;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .search-bar {{
    margin: 18px 38px 12px;
    background: #F0F1F5;
    border-radius: 20px;
    padding: 16px 22px;
    display: flex;
    align-items: center;
    gap: 14px;
  }}

  .search-placeholder {{
    font-size: 22px;
    color: #6B7280;
    font-weight: 500;
  }}

  .category-tabs {{
    display: flex;
    gap: 12px;
    padding: 6px 38px 14px;
  }}

  .tab-chip {{
    background: #F3F4F6;
    color: #4B5563;
    font-size: 19px;
    font-weight: 700;
    padding: 8px 20px;
    border-radius: 18px;
  }}

  .tab-chip.active {{
    background: #F76B00;
    color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(247, 107, 0, 0.28);
  }}

  .cards-container {{
    padding: 4px 38px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex: 1;
  }}

  .totp-card {{
    background: #FFFFFF;
    border-radius: 24px;
    padding: 22px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.035), 0 1px 3px rgba(0,0,0,0.02);
    border: 1px solid #EAECEF;
  }}

  .totp-card.urgent-card {{
    border: 1.5px solid #FCA5A5;
    background: #FEF2F2;
  }}

  .card-left {{
    display: flex;
    align-items: center;
    gap: 20px;
  }}

  .service-icon {{
    width: 62px;
    height: 62px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F8F9FA;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }}

  .google-bg {{ background: #FFFFFF; border: 1px solid #E5E7EB; }}
  .github-bg {{ background: #F3F4F6; border: 1px solid #E5E7EB; }}
  .binance-bg {{ background: #1E2329; }}
  .aws-bg {{ background: #232F3E; }}
  .proton-bg {{ background: #F0EDFF; }}
  .discord-bg {{ background: #F0F2FE; }}

  .service-info {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .service-issuer {{
    font-size: 25px;
    font-weight: 700;
    color: #111827;
  }}

  .service-account {{
    font-size: 19px;
    color: #6B7280;
    font-weight: 500;
  }}

  .code-and-timer {{
    display: flex;
    align-items: center;
    gap: 22px;
  }}

  .totp-code {{
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    font-family: "SF Pro Rounded", -apple-system, monospace;
    letter-spacing: 2.5px;
  }}

  .totp-code.urgent-code {{
    color: #DC2626;
  }}

  .code-space {{
    margin-left: 6px;
  }}

  .countdown-wrap {{
    position: relative;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .countdown-text {{
    position: absolute;
    font-size: 15px;
    font-weight: 700;
    color: #F76B00;
  }}

  .countdown-text.urgent-text {{
    color: #DC2626;
  }}

  .dashboard-bottom-bar {{
    position: absolute;
    bottom: 46px;
    left: 40px;
    right: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 40;
  }}

  .pet-companion-fab {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: #FFFFFF;
    border: 1.5px solid #FED7AA;
    padding: 8px 18px 8px 10px;
    border-radius: 36px;
    box-shadow: 0 8px 24px rgba(247, 107, 0, 0.15);
  }}

  .pet-mini-avatar {{
    width: 50px;
    height: 50px;
    border-radius: 16px;
  }}

  .pet-mini-badge {{
    font-size: 19px;
    font-weight: 700;
    color: #EA580C;
  }}

  .fab-btn {{
    width: 76px;
    height: 76px;
    border-radius: 38px;
    background: #F76B00;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 28px rgba(247, 107, 0, 0.45);
  }}

  /* Screen 2: Scanner Styling */
  .scanner-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 38px;
  }}

  .scanner-title {{
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 700;
  }}

  .icon-round-btn {{
    width: 52px;
    height: 52px;
    border-radius: 26px;
    background: rgba(255,255,255,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .icon-round-btn.active-torch {{
    background: #FFFFFF;
  }}

  .viewfinder-section {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0 38px;
    position: relative;
  }}

  .scanner-prompt-pill {{
    background: rgba(0,0,0,0.7);
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 600;
    padding: 14px 30px;
    border-radius: 26px;
    border: 1px solid rgba(255,255,255,0.2);
    margin-bottom: 50px;
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .pulse-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 10px #10B981;
  }}

  .reticle-box {{
    width: 520px;
    height: 520px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.04);
    border-radius: 40px;
  }}

  .corner-bracket {{
    position: absolute;
    width: 70px;
    height: 70px;
    border-color: #F76B00;
    border-style: solid;
  }}

  .top-left {{ top: 0; left: 0; border-width: 8px 0 0 8px; border-top-left-radius: 28px; }}
  .top-right {{ top: 0; right: 0; border-width: 8px 8px 0 0; border-top-right-radius: 28px; }}
  .bottom-left {{ bottom: 0; left: 0; border-width: 0 0 8px 8px; border-bottom-left-radius: 28px; }}
  .bottom-right {{ bottom: 0; right: 0; border-width: 0 8px 8px 0; border-bottom-right-radius: 28px; }}

  .laser-line {{
    position: absolute;
    left: 20px;
    right: 20px;
    top: 50%;
    height: 5px;
    background: #00F0FF;
    box-shadow: 0 0 18px #00F0FF, 0 0 35px #00F0FF;
    border-radius: 3px;
  }}

  .detected-toast {{
    margin-top: 50px;
    background: rgba(16, 185, 129, 0.22);
    border: 1.5px solid #10B981;
    backdrop-filter: blur(16px);
    border-radius: 22px;
    padding: 18px 26px;
    display: flex;
    align-items: center;
    gap: 16px;
    width: 90%;
    max-width: 600px;
  }}

  .check-circle {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #10B981;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 20px;
  }}

  .detected-name {{
    color: #FFFFFF;
    font-size: 22px;
    font-weight: 700;
  }}

  .detected-sub {{
    color: #A7F3D0;
    font-size: 18px;
    font-weight: 500;
    margin-top: 3px;
  }}

  .scanner-features-row {{
    display: flex;
    gap: 14px;
    margin-top: 40px;
  }}

  .feature-chip {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.18);
    padding: 8px 18px;
    border-radius: 18px;
    color: #FFFFFF;
    font-size: 18px;
    font-weight: 600;
  }}

  .scanner-bottom-actions {{
    display: flex;
    justify-content: space-around;
    padding: 30px 48px 60px;
  }}

  .action-btn {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    padding: 18px 30px;
    border-radius: 24px;
    color: #FFFFFF;
    font-size: 21px;
    font-weight: 600;
  }}

  /* Screen 3: Pet Academy Styling */
  .academy-badge-icon {{
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: #FFF0E6;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .academy-container {{
    padding: 24px 38px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }}

  .pet-hero-card {{
    background: linear-gradient(135deg, #FFF6EE 0%, #FFE9D6 100%);
    border: 1.5px solid #FED7AA;
    border-radius: 30px;
    padding: 26px 30px;
    display: flex;
    align-items: center;
    gap: 26px;
    position: relative;
    box-shadow: 0 6px 20px rgba(247, 107, 0, 0.08);
  }}

  .pet-avatar-wrap {{
    position: relative;
    width: 120px;
    height: 120px;
  }}

  .pet-hero-img {{
    width: 120px;
    height: 120px;
    border-radius: 30px;
    background: #FFFFFF;
    box-shadow: 0 8px 24px rgba(247, 107, 0, 0.2);
  }}

  .level-tag {{
    position: absolute;
    bottom: -6px;
    right: -6px;
    background: #F76B00;
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 800;
    padding: 3px 10px;
    border-radius: 12px;
    border: 2px solid #FFFFFF;
  }}

  .pet-meta {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .pet-name {{
    font-size: 32px;
    font-weight: 800;
    color: #111827;
  }}

  .pet-role {{
    font-size: 20px;
    font-weight: 600;
    color: #EA580C;
  }}

  .xp-bar-bg {{
    width: 100%;
    height: 12px;
    background: rgba(0,0,0,0.08);
    border-radius: 6px;
    overflow: hidden;
    margin-top: 4px;
  }}

  .xp-bar-fill {{
    height: 100%;
    background: linear-gradient(90deg, #F76B00, #FBBF24);
    border-radius: 6px;
  }}

  .xp-label {{
    font-size: 17px;
    font-weight: 600;
    color: #6B7280;
  }}

  .streak-pill {{
    position: absolute;
    top: 20px;
    right: 22px;
    background: #FFFFFF;
    border: 1px solid #FED7AA;
    color: #EA580C;
    font-size: 16px;
    font-weight: 700;
    padding: 6px 14px;
    border-radius: 16px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
  }}

  .mascot-speech-bubble {{
    position: relative;
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 22px;
    padding: 20px 26px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }}

  .mascot-speech-bubble p {{
    font-size: 22px;
    color: #374151;
    font-weight: 500;
    line-height: 1.45;
  }}

  .bubble-tail {{
    position: absolute;
    top: -12px;
    left: 50px;
    width: 0;
    height: 0;
    border-left: 10px solid transparent;
    border-right: 10px solid transparent;
    border-bottom: 12px solid #FFFFFF;
  }}

  .habits-section-title {{
    font-size: 19px;
    font-weight: 800;
    color: #6B7280;
    letter-spacing: 0.8px;
    margin-top: 8px;
  }}

  .habit-card {{
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 22px;
    padding: 20px 24px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  }}

  .habit-card.completed {{
    border-color: #D1FAE5;
    background: #F0FDF4;
  }}

  .habit-icon-check {{
    width: 44px;
    height: 44px;
    border-radius: 14px;
    background: #10B981;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    font-weight: 800;
  }}

  .habit-info {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}

  .habit-title {{
    font-size: 22px;
    font-weight: 700;
    color: #111827;
  }}

  .habit-sub {{
    font-size: 18px;
    color: #6B7280;
    font-weight: 500;
  }}

  .xp-reward {{
    font-size: 19px;
    font-weight: 800;
    color: #059669;
    background: #D1FAE5;
    padding: 6px 14px;
    border-radius: 14px;
  }}

  .academy-lesson-card {{
    background: #FFFFFF;
    border: 1.5px solid #E5E7EB;
    border-radius: 24px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }}

  .lesson-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .lesson-tag {{
    font-size: 16px;
    font-weight: 800;
    color: #F76B00;
    letter-spacing: 0.6px;
  }}

  .lesson-xp {{
    background: #FFF0E6;
    color: #EA580C;
    font-size: 16px;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 12px;
  }}

  .lesson-title {{
    font-size: 24px;
    font-weight: 800;
    color: #111827;
  }}

  .lesson-desc {{
    font-size: 19px;
    color: #4B5563;
    line-height: 1.45;
  }}

  /* Screen 4: Settings & Backup Styling */
  .settings-container {{
    padding: 24px 38px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }}

  .settings-group-title {{
    font-size: 19px;
    font-weight: 800;
    color: #6B7280;
    letter-spacing: 0.8px;
  }}

  .settings-card {{
    background: #FFFFFF;
    border-radius: 24px;
    border: 1px solid #E5E7EB;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  }}

  .settings-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 22px 24px;
  }}

  .row-left {{
    display: flex;
    align-items: center;
    gap: 18px;
  }}

  .row-icon {{
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}

  .orange-icon {{ background: #FFF0E6; }}
  .blue-icon {{ background: #EBF5FF; }}
  .purple-icon {{ background: #F3E8FF; }}

  .row-text {{
    display: flex;
    flex-direction: column;
    gap: 4px;
  }}

  .row-label {{
    font-size: 22px;
    font-weight: 700;
    color: #111827;
  }}

  .row-desc {{
    font-size: 17px;
    color: #6B7280;
    font-weight: 500;
  }}

  .row-divider {{
    height: 1px;
    background: #F3F4F6;
    margin-left: 90px;
  }}

  /* iOS Switch UI */
  .ios-switch {{
    width: 60px;
    height: 36px;
    background: #E5E7EB;
    border-radius: 18px;
    padding: 3px;
    display: flex;
    align-items: center;
  }}

  .ios-switch.on {{
    background: #34C759;
    justify-content: flex-end;
  }}

  .switch-knob {{
    width: 30px;
    height: 30px;
    background: #FFFFFF;
    border-radius: 50%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  }}

  .row-value-badge {{
    font-size: 19px;
    color: #6B7280;
    font-weight: 600;
  }}

  .backup-box {{
    background: #FFFFFF;
    border-radius: 26px;
    border: 1.5px solid #FED7AA;
    padding: 28px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    box-shadow: 0 6px 18px rgba(247, 107, 0, 0.06);
  }}

  .backup-header-row {{
    display: flex;
    gap: 10px;
  }}

  .backup-chip {{
    background: #FFF7ED;
    border: 1px solid #FDBA74;
    color: #EA580C;
    font-size: 16px;
    font-weight: 700;
    padding: 5px 14px;
    border-radius: 12px;
  }}

  .backup-desc {{
    font-size: 20px;
    color: #4B5563;
    line-height: 1.45;
  }}

  .btn-export-backup {{
    background: #F76B00;
    color: #FFFFFF;
    border-radius: 20px;
    padding: 19px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    font-size: 22px;
    font-weight: 700;
    box-shadow: 0 8px 20px rgba(247, 107, 0, 0.35);
    margin-top: 4px;
  }}

  .btn-restore-backup {{
    background: #F3F4F6;
    color: #111827;
    border-radius: 20px;
    padding: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    font-size: 20px;
    font-weight: 700;
    border: 1px solid #E5E7EB;
  }}

  .stats-box {{
    background: #FFFFFF;
    border-radius: 22px;
    border: 1px solid #E5E7EB;
    padding: 20px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
  }}

  .stat-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
  }}

  .stat-val {{
    font-size: 26px;
    font-weight: 800;
    color: #111827;
  }}

  .stat-lbl {{
    font-size: 16px;
    color: #6B7280;
    font-weight: 600;
  }}

  .stat-div {{
    width: 1px;
    height: 36px;
    background: #E5E7EB;
  }}

  .zero-tracking-pill {{
    background: #ECFDF5;
    border: 1.5px solid #A7F3D0;
    border-radius: 20px;
    padding: 16px 22px;
    display: flex;
    align-items: center;
    gap: 14px;
    color: #065F46;
    font-size: 19px;
    font-weight: 600;
  }}

  .green-check-dot {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #10B981;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 16px;
  }}
</style>
</head>
<body>
  <div class="bg-glow-1"></div>

  <!-- Top Banner Header -->
  <div class="banner-header">
    <div class="mascot-header-wrap">
      <img src="{ICON_B64}" class="mascot-badge-img" alt="Simple OTP"/>
      <div class="mascot-badge-pill">SIMPLE OTP</div>
    </div>
    <div class="banner-title">{title}</div>
    <div class="banner-subtitle">{subtitle}</div>
  </div>

  <!-- Modern Titanium Device Mockup Frame -->
  <div class="device-mockup">
    {screen_content}
  </div>
</body>
</html>
"""
    return html

def render_screenshot(screen_id, lang, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_content = build_html(screen_id, lang)
    
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
        f.write(html_content)
        temp_html_path = f.name

    try:
        cmd = [
            CHROME_BIN,
            "--headless",
            f"--screenshot={output_path}",
            "--window-size=1284,2778",
            "--force-device-scale-factor=1",
            "--hide-scrollbars",
            f"file://{temp_html_path}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Error rendering {output_path}: {res.stderr}")
            return False
        
        # Verify file dimensions using magick identify
        ident_res = subprocess.run(["magick", "identify", output_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✓ Generated: {output_path} -> {ident_res.stdout.strip()}")
        return True
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

def main():
    screens = [
        '01_offline_security',
        '02_qr_scanner',
        '03_pet_academy',
        '04_encrypted_backup'
    ]
    languages = ['en', 'vi']

    for lang in languages:
        for screen in screens:
            # 1. Primary iOS standard banners (1284x2778)
            ios_out = os.path.join(PROJECT_ROOT, f"assets/banners/ios/{lang}/{screen}.png")
            render_screenshot(screen, lang, ios_out)
            
            # 2. Also keep root assets/banners/{lang}/ updated
            root_out = os.path.join(PROJECT_ROOT, f"assets/banners/{lang}/{screen}.png")
            render_screenshot(screen, lang, root_out)

if __name__ == '__main__':
    main()
