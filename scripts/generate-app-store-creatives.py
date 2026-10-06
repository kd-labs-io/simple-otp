#!/usr/bin/env python3
"""
Generate Apple App Store Connect Creative Assets:
- Universal Creative Asset (5244 x 2950 px) - 16:9
- Product Page Header Asset (3840 x 1646 px) - 21:9 Ultra-wide
- Search Results Asset (3840 x 2560 px & 1920 x 1280 px) - 3:2

Complies with Apple 2026 App Store specifications:
- Safe Area margins respected (central focal point)
- 4+ Age Rating compliant
- Localized for Vietnamese ('vi') and English ('en')
- Also generates clean 'artwork_only' variants (editorial featuring standard)
"""

import os
import sys
import base64
import tempfile
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def get_base64_image(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        ext = os.path.splitext(path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('ascii')}"

ICON_B64 = get_base64_image(os.path.join(PROJECT_ROOT, "assets/images/icon.png"))
HEADER_HERO_B64 = get_base64_image(os.path.join(PROJECT_ROOT, "assets/creatives/raw/header_hero.jpg"))

COPY_DATA = {
    "vi": {
        "brand_badge": "KHO KHÓA 100% NGOẠI TUYẾN",
        "title": "Bảo Mật 2FA Offline • An Tâm Tuyệt Đối",
        "subtitle": "Xác thực hai bước an toàn • Không gửi dữ liệu qua Internet • Đồng hành cùng Bé Khóa",
        "header_title": "Bảo Mật 2FA Offline • An Tâm Tuyệt Đối",
        "header_subtitle": "Xác thực hai bước an toàn ngoại tuyến cùng Bé Khóa",
        "chips": ["100% Ngoại Tuyến", "Mã Hóa AES-256", "Mở Khóa Face ID", "Bảo Vệ Tài Khoản"]
    },
    "en": {
        "brand_badge": "100% OFFLINE 2FA VAULT",
        "title": "100% Offline 2FA Vault • Simple, Private & Secure",
        "subtitle": "Hardware-backed two-factor authentication • Zero network tracking • Cute pet companion",
        "header_title": "100% Offline 2FA Vault • Simple & Secure",
        "header_subtitle": "Hardware-backed offline security with companion Bé Khóa",
        "chips": ["100% Offline", "AES-256 Encrypted", "Biometric Face ID", "Zero Tracking"]
    }
}

def render_html_to_image(html_content, width, height, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
        f.write(html_content)
        temp_html = f.name

    try:
        cmd = [
            CHROME_BIN,
            "--headless",
            f"--screenshot={output_path}",
            f"--window-size={width},{height}",
            "--force-device-scale-factor=1",
            "--hide-scrollbars",
            f"file://{temp_html}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Error rendering {output_path}: {res.stderr}")
            return False

        ident_res = subprocess.run(["magick", "identify", output_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✓ Generated: {output_path} ({ident_res.stdout.strip()})")
        return True
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

# ==========================================
# 1. UNIVERSAL CREATIVE ASSET (5244 x 2950 px)
# ==========================================
def build_universal_html(lang=None):
    is_textless = (lang is None)
    c = COPY_DATA.get(lang, COPY_DATA["en"]) if not is_textless else {}

    overlay_html = ""
    if not is_textless:
        chips_html = "".join([f'<div class="chip">{ch}</div>' for ch in c["chips"]])
        overlay_html = f"""
        <div class="header-overlay">
            <div class="brand-pill">
                <img src="{ICON_B64}" class="brand-icon" alt="Simple OTP" />
                <span class="brand-text">Simple OTP</span>
                <span class="pill-divider">•</span>
                <span class="badge-text">{c['brand_badge']}</span>
            </div>
            <h1 class="main-title">{c['title']}</h1>
            <p class="subtitle">{c['subtitle']}</p>
        </div>
        <div class="chips-footer">
            {chips_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        width: 5244px;
        height: 2950px;
        background: #F76B00;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', sans-serif;
        overflow: hidden;
        position: relative;
    }}
    .bg-artwork {{
        position: absolute;
        top: 0;
        left: 0;
        width: 5244px;
        height: 2950px;
        object-fit: cover;
        object-position: center;
        z-index: 1;
    }}
    .lighting-vignette {{
        position: absolute;
        top: 0;
        left: 0;
        width: 5244px;
        height: 2950px;
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.02) 0%, rgba(0,0,0,0.06) 75%, rgba(0,0,0,0.2) 100%);
        pointer-events: none;
        z-index: 2;
    }}
    .header-overlay {{
        position: absolute;
        top: 100px;
        left: 0;
        width: 5244px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        z-index: 10;
        padding: 0 200px;
    }}
    .brand-pill {{
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(50px);
        -webkit-backdrop-filter: blur(50px);
        border: 3px solid rgba(255, 255, 255, 0.55);
        padding: 20px 52px 20px 26px;
        border-radius: 999px;
        box-shadow: 0 24px 50px rgba(0, 0, 0, 0.15), inset 0 2px 4px rgba(255, 255, 255, 0.4);
        margin-bottom: 30px;
    }}
    .brand-icon {{
        width: 72px;
        height: 72px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        margin-right: 24px;
    }}
    .brand-text {{
        font-size: 48px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        text-shadow: 0 3px 12px rgba(0,0,0,0.2);
    }}
    .pill-divider {{
        font-size: 36px;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 20px;
    }}
    .badge-text {{
        font-size: 40px;
        font-weight: 700;
        color: #FFE082;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    .main-title {{
        font-size: 116px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -2px;
        line-height: 1.15;
        margin-bottom: 20px;
        text-shadow: 0 6px 24px rgba(0, 0, 0, 0.35), 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    .subtitle {{
        font-size: 52px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: 0.2px;
        max-width: 3600px;
        line-height: 1.35;
        text-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }}
    .chips-footer {{
        position: absolute;
        bottom: 90px;
        left: 0;
        width: 5244px;
        display: flex;
        justify-content: center;
        gap: 36px;
        z-index: 10;
    }}
    .chip {{
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 2px solid rgba(255, 255, 255, 0.45);
        padding: 20px 50px;
        border-radius: 999px;
        font-size: 40px;
        font-weight: 700;
        color: #FFFFFF;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
        letter-spacing: 0.5px;
    }}
</style>
</head>
<body>
    <img src="{HEADER_HERO_B64}" class="bg-artwork" alt="Hero Art" />
    <div class="lighting-vignette"></div>
    {overlay_html}
</body>
</html>"""

# ==========================================
# 2. PRODUCT PAGE HEADER ASSET (3840 x 1646 px)
# ==========================================
def build_header_html(lang=None):
    is_textless = (lang is None)
    c = COPY_DATA.get(lang, COPY_DATA["en"]) if not is_textless else {}

    overlay_html = ""
    if not is_textless:
        overlay_html = f"""
        <div class="header-overlay">
            <div class="brand-pill">
                <img src="{ICON_B64}" class="brand-icon" alt="Simple OTP" />
                <span class="brand-text">Simple OTP</span>
                <span class="pill-divider">•</span>
                <span class="badge-text">{c['brand_badge']}</span>
            </div>
            <h1 class="main-title">{c['header_title']}</h1>
            <p class="subtitle">{c['header_subtitle']}</p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        width: 3840px;
        height: 1646px;
        background: #F76B00;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', sans-serif;
        overflow: hidden;
        position: relative;
    }}
    .bg-artwork {{
        position: absolute;
        top: 0;
        left: 0;
        width: 3840px;
        height: 1646px;
        object-fit: cover;
        object-position: center 60%;
        z-index: 1;
    }}
    .lighting-vignette {{
        position: absolute;
        top: 0;
        left: 0;
        width: 3840px;
        height: 1646px;
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0.06) 75%, rgba(0,0,0,0.2) 100%);
        pointer-events: none;
        z-index: 2;
    }}
    .header-overlay {{
        position: absolute;
        top: 60px;
        left: 0;
        width: 3840px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        z-index: 10;
        padding: 0 160px;
    }}
    .brand-pill {{
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 2px solid rgba(255, 255, 255, 0.55);
        padding: 14px 38px 14px 20px;
        border-radius: 999px;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.15);
        margin-bottom: 18px;
    }}
    .brand-icon {{
        width: 52px;
        height: 52px;
        border-radius: 14px;
        margin-right: 18px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.2);
    }}
    .brand-text {{
        font-size: 34px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.4px;
    }}
    .pill-divider {{
        font-size: 26px;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 16px;
    }}
    .badge-text {{
        font-size: 28px;
        font-weight: 700;
        color: #FFE082;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }}
    .main-title {{
        font-size: 82px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -1.2px;
        line-height: 1.15;
        margin-bottom: 14px;
        text-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }}
    .subtitle {{
        font-size: 38px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: 0.2px;
        max-width: 2800px;
        line-height: 1.35;
        text-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    }}
</style>
</head>
<body>
    <img src="{HEADER_HERO_B64}" class="bg-artwork" alt="Header Art" />
    <div class="lighting-vignette"></div>
    {overlay_html}
</body>
</html>"""

# ==========================================
# 3. SEARCH RESULTS ASSET (3840 x 2560 px)
# ==========================================
def build_search_html(lang=None):
    is_textless = (lang is None)
    c = COPY_DATA.get(lang, COPY_DATA["en"]) if not is_textless else {}

    overlay_html = ""
    if not is_textless:
        chips_html = "".join([f'<div class="chip">{ch}</div>' for ch in c["chips"]])
        overlay_html = f"""
        <div class="header-overlay">
            <div class="brand-pill">
                <img src="{ICON_B64}" class="brand-icon" alt="Simple OTP" />
                <span class="brand-text">Simple OTP</span>
                <span class="pill-divider">•</span>
                <span class="badge-text">{c['brand_badge']}</span>
            </div>
            <h1 class="main-title">{c['title']}</h1>
            <p class="subtitle">{c['subtitle']}</p>
        </div>
        <div class="chips-footer">
            {chips_html}
        </div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        width: 3840px;
        height: 2560px;
        background: #F76B00;
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', sans-serif;
        overflow: hidden;
        position: relative;
    }}
    .bg-artwork {{
        position: absolute;
        top: 0;
        left: 0;
        width: 3840px;
        height: 2560px;
        object-fit: cover;
        object-position: center;
        z-index: 1;
    }}
    .lighting-vignette {{
        position: absolute;
        top: 0;
        left: 0;
        width: 3840px;
        height: 2560px;
        background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0.06) 75%, rgba(0,0,0,0.2) 100%);
        pointer-events: none;
        z-index: 2;
    }}
    .header-overlay {{
        position: absolute;
        top: 80px;
        left: 0;
        width: 3840px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        z-index: 10;
        padding: 0 160px;
    }}
    .brand-pill {{
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 2px solid rgba(255, 255, 255, 0.55);
        padding: 16px 44px 16px 22px;
        border-radius: 999px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.15);
        margin-bottom: 24px;
    }}
    .brand-icon {{
        width: 62px;
        height: 62px;
        border-radius: 16px;
        margin-right: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    }}
    .brand-text {{
        font-size: 40px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.4px;
    }}
    .pill-divider {{
        font-size: 30px;
        color: rgba(255, 255, 255, 0.6);
        margin: 0 18px;
    }}
    .badge-text {{
        font-size: 34px;
        font-weight: 700;
        color: #FFE082;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    .main-title {{
        font-size: 98px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: -1.6px;
        line-height: 1.15;
        margin-bottom: 16px;
        text-shadow: 0 6px 24px rgba(0, 0, 0, 0.35);
    }}
    .subtitle {{
        font-size: 44px;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: 0.2px;
        max-width: 2900px;
        line-height: 1.35;
        text-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }}
    .chips-footer {{
        position: absolute;
        bottom: 80px;
        left: 0;
        width: 3840px;
        display: flex;
        justify-content: center;
        gap: 32px;
        z-index: 10;
    }}
    .chip {{
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 2px solid rgba(255, 255, 255, 0.45);
        padding: 18px 42px;
        border-radius: 999px;
        font-size: 34px;
        font-weight: 700;
        color: #FFFFFF;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.12);
        letter-spacing: 0.5px;
    }}
</style>
</head>
<body>
    <img src="{HEADER_HERO_B64}" class="bg-artwork" alt="Search Results Art" />
    <div class="lighting-vignette"></div>
    {overlay_html}
</body>
</html>"""

def main():
    print("=" * 60)
    print("🚀 GENERATING APP STORE CREATIVE ASSETS (APPLE STANDARDS)")
    print("=" * 60)

    # 1. Localized sets (vi, en)
    for lang in ["vi", "en"]:
        print(f"\n--- Generating [{lang.upper()}] Creative Assets ---")
        
        # Universal (5244 x 2950)
        uni_path = os.path.join(PROJECT_ROOT, f"assets/creatives/{lang}/universal_5244x2950.png")
        render_html_to_image(build_universal_html(lang), 5244, 2950, uni_path)

        # Header (3840 x 1646)
        hdr_path = os.path.join(PROJECT_ROOT, f"assets/creatives/{lang}/header_3840x1646.png")
        render_html_to_image(build_header_html(lang), 3840, 1646, hdr_path)

        # Search Results (3840 x 2560)
        sch_path = os.path.join(PROJECT_ROOT, f"assets/creatives/{lang}/search_3840x2560.png")
        render_html_to_image(build_search_html(lang), 3840, 2560, sch_path)

        # Search Results 1x (1920 x 1280)
        sch_1x_path = os.path.join(PROJECT_ROOT, f"assets/creatives/{lang}/search_1920x1280.png")
        subprocess.check_call(["magick", sch_path, "-filter", "Lanczos", "-resize", "1920x1280", sch_1x_path])
        print(f"✓ Generated 1x: {sch_1x_path} (1920x1280)")

    # 2. Textless Clean Artwork (Editorial Featuring Standard)
    print("\n--- Generating Clean Textless Artwork Variants ---")
    art_dir = os.path.join(PROJECT_ROOT, "assets/creatives/artwork_only")
    
    uni_art = os.path.join(art_dir, "universal_5244x2950.png")
    render_html_to_image(build_universal_html(None), 5244, 2950, uni_art)

    hdr_art = os.path.join(art_dir, "header_3840x1646.png")
    render_html_to_image(build_header_html(None), 3840, 1646, hdr_art)

    sch_art = os.path.join(art_dir, "search_3840x2560.png")
    render_html_to_image(build_search_html(None), 3840, 2560, sch_art)

    sch_art_1x = os.path.join(art_dir, "search_1920x1280.png")
    subprocess.check_call(["magick", sch_art, "-filter", "Lanczos", "-resize", "1920x1280", sch_art_1x])
    print(f"✓ Generated 1x: {sch_art_1x} (1920x1280)")

    print("\n🎉 ALL APPLE APP STORE CREATIVE ASSETS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
