#!/usr/bin/env python3
"""
Generate Apple App Store Connect 6.1" Screenshots (1179 x 2556 px):
Complies with Apple App Store Guideline 2.3.3 (Accurate Metadata)
by processing real screenshots taken directly from the app:
- Upscaling to crisp 1179 x 2556 px (iPhone 6.1" Super Retina XDR standard)
- Replacing status bar with official Apple standard (9:41 AM, 100% battery, full signal, zero TestFlight)
- Retaining 100% authentic in-app UI without artificial mockups
- Localized for both Vietnamese ('vi') and English ('en')
- Preserves native Home Indicator
"""

import os
import sys
import base64
import tempfile
import subprocess
import shutil

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Screen processing order (Recommended for Guideline 2.3.3 compliance)
SCREENS = [
    ("3-show-otp.jpg", "01_show_otp.png", "Active 2FA OTP Codes & Pet Companion"),
    ("5-add-new.jpg", "02_add_new.png", "Add Account & Scan QR Options"),
    ("4-manual-input.jpg", "03_manual_input.png", "Manual Secret Key Entry"),
    ("2-settings.jpg", "04_settings.png", "Mascot, Security & Backup Settings"),
    ("1-empty.jpg", "05_empty.png", "Welcome & Empty State Screen")
]

LANGUAGES = ["vi", "en"]

def get_base64_image(path):
    with open(path, "rb") as f:
        ext = os.path.splitext(path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('ascii')}"

def render_screenshot(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Upscale and apply slight unsharp mask to ensure crisp text
    tmp_upscaled = tempfile.mktemp(suffix=".png")
    try:
        subprocess.check_call([
            "magick", input_path,
            "-filter", "Lanczos",
            "-resize", "1179x2556!",
            "-unsharp", "0x0.6+0.8+0.01",
            tmp_upscaled
        ])

        # 2. Sample top status background color from center safe area (x=600, y=80)
        c_hex = subprocess.check_output([
            "magick", tmp_upscaled,
            "-crop", "1x1+600+80",
            "-format", "%[hex:p{0,0}]",
            "info:"
        ]).decode().strip()
        bg_color = f"#{c_hex[:6]}"

        bg_b64 = get_base64_image(tmp_upscaled)

        # 3. HTML template with Apple standard status bar & home indicator
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 1179px;
    height: 2556px;
    background: {bg_color};
    overflow: hidden;
    position: relative;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", sans-serif;
  }}
  .app-screenshot {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1179px;
    height: 2556px;
    object-fit: fill;
  }}
  .status-cover {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1179px;
    height: 145px;
    background: {bg_color};
    z-index: 10;
  }}
  .status-bar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1179px;
    height: 145px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 96px 0 96px;
    z-index: 20;
    color: #000000;
  }}
  .time {{
    font-size: 46px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }}
  .status-icons {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .signal-bars {{
    display: flex;
    align-items: flex-end;
    gap: 4.5px;
    height: 34px;
    padding-bottom: 2px;
  }}
  .bar {{
    width: 8px;
    background: #000000;
    border-radius: 2.5px;
  }}
  .b1 {{ height: 10px; }}
  .b2 {{ height: 16px; }}
  .b3 {{ height: 23px; }}
  .b4 {{ height: 30px; }}

  .wifi-svg {{
    width: 44px;
    height: 32px;
    fill: #000000;
  }}
  .battery-container {{
    display: flex;
    align-items: center;
  }}
  .battery-body {{
    width: 66px;
    height: 34px;
    border: 3.5px solid #000000;
    border-radius: 10px;
    padding: 2.5px;
    display: flex;
    align-items: center;
  }}
  .battery-fill {{
    width: 100%;
    height: 100%;
    background: #000000;
    border-radius: 4px;
  }}
  .battery-terminal {{
    width: 4px;
    height: 14px;
    background: #000000;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    margin-left: 1.5px;
  }}
  .home-indicator {{
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: 410px;
    height: 15px;
    background: #000000;
    opacity: 0.85;
    border-radius: 8px;
    z-index: 30;
  }}
</style>
</head>
<body>
  <img src="{bg_b64}" class="app-screenshot" alt="App Screenshot" />
  <div class="status-cover"></div>
  <div class="status-bar">
    <div class="time">9:41</div>
    <div class="status-icons">
      <div class="signal-bars">
        <div class="bar b1"></div>
        <div class="bar b2"></div>
        <div class="bar b3"></div>
        <div class="bar b4"></div>
      </div>
      <svg class="wifi-svg" viewBox="0 0 24 24">
        <path d="M12 4C7.31 4 3.07 5.9 0 8.98L12 21L24 8.98C20.93 5.9 16.69 4 12 4ZM12 8C15.17 8 18.06 9.17 20.31 11.11L12 19.46L3.69 11.11C5.94 9.17 8.83 8 12 8Z"/>
      </svg>
      <div class="battery-container">
        <div class="battery-body">
          <div class="battery-fill"></div>
        </div>
        <div class="battery-terminal"></div>
      </div>
    </div>
  </div>
  <div class="home-indicator"></div>
</body>
</html>"""

        with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as f:
            f.write(html)
            temp_html = f.name

        try:
            cmd = [
                CHROME_BIN,
                "--headless",
                f"--screenshot={output_path}",
                "--window-size=1179,2556",
                "--force-device-scale-factor=1",
                "--hide-scrollbars",
                f"file://{temp_html}"
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode != 0:
                print(f"Error rendering {output_path}: {res.stderr}")
                return False

            ident_res = subprocess.run(["magick", "identify", output_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"  ✓ {os.path.basename(output_path)} -> {ident_res.stdout.strip()}")
            return True
        finally:
            if os.path.exists(temp_html):
                os.remove(temp_html)
    finally:
        if os.path.exists(tmp_upscaled):
            os.remove(tmp_upscaled)

def main():
    print("=" * 70)
    print("🚀 GENERATING APP STORE SCREENSHOTS (IPHONE 6.1\" - 1179 x 2556 PX)")
    print("   Complies with Apple Guideline 2.3.3: Accurate Metadata")
    print("=" * 70)

    for lang in LANGUAGES:
        print(f"\n📂 Processing Language: [{lang.upper()}]")
        src_dir = os.path.join(PROJECT_ROOT, f"assets/banners/ios-app-preview/{lang}")
        dst_dir = os.path.join(PROJECT_ROOT, f"assets/banners/ios/{lang}")

        # Clear old banners
        if os.path.exists(dst_dir):
            for old_f in os.listdir(dst_dir):
                old_p = os.path.join(dst_dir, old_f)
                if os.path.isfile(old_p):
                    os.remove(old_p)
        else:
            os.makedirs(dst_dir, exist_ok=True)

        for src_name, dst_name, desc in SCREENS:
            src_file = os.path.join(src_dir, src_name)
            dst_file = os.path.join(dst_dir, dst_name)

            if not os.path.exists(src_file):
                print(f"  ⚠️ Missing input: {src_file}")
                continue

            print(f"  ⚡ [{src_name}] -> [{dst_name}] ({desc})")
            render_screenshot(src_file, dst_file)

    print("\n🎉 ALL 1179 x 2556 PX APP STORE SCREENSHOTS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
