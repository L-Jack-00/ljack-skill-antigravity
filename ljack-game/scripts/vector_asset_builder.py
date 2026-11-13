#!/usr/bin/env python3
"""
vector_asset_builder.py - 엘잭 게임 초경량 벡터(SVG) 에셋 빌더 (v1.6.0)

게임 UI 제작 시 무거운 외부 툴 없이 명령줄 하나로 
TCG 카드 프레임, 공격력 칼 뱃지, 체력 플라크, 나선 룬 SVG를 즉시 생성합니다.

사용법:
  python vector_asset_builder.py --type=all --style=comic --out=./ui_assets/
  python vector_asset_builder.py --type=card_frame --style=metallic
  python vector_asset_builder.py --type=sword_badge --style=comic
"""

import sys
import os
import argparse
import math

def get_sword_badge(style="comic"):
    if style == "comic":
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 260" width="260" height="260">
  <defs>
    <filter id="c-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.6"/>
    </filter>
  </defs>
  <g filter="url(#c-shadow)">
    <!-- Diagonal Cartoon Sword -->
    <g transform="translate(130, 130) rotate(-45) translate(-130, -130)">
      <polygon points="130,246 148,195 112,195" fill="#E2E8F0" stroke="#111827" stroke-width="8" stroke-linejoin="round"/>
      <line x1="130" y1="200" x2="130" y2="242" stroke="#94A3B8" stroke-width="4" stroke-linecap="round"/>
      <rect x="90" y="52" width="80" height="18" rx="5" fill="#FBBF24" stroke="#111827" stroke-width="8" stroke-linejoin="round"/>
      <rect x="120" y="24" width="20" height="30" rx="4" fill="#3B82F6" stroke="#111827" stroke-width="8" stroke-linejoin="round"/>
      <rect x="115" y="10" width="30" height="15" rx="5" fill="#FBBF24" stroke="#111827" stroke-width="8" stroke-linejoin="round"/>
    </g>
    <!-- Double Concentric Rings -->
    <circle cx="130" cy="130" r="82" fill="#F59E0B" stroke="#111827" stroke-width="12"/>
    <circle cx="130" cy="130" r="62" fill="#1E293B" stroke="#111827" stroke-width="10"/>
    <circle cx="130" cy="130" r="54" fill="#0F172A" stroke="#334155" stroke-width="3"/>
  </g>
</svg>"""
    else:
        # Metallic Realistic
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280" width="280" height="280">
  <defs>
    <filter id="m-shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity="0.8"/>
    </filter>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/><stop offset="30%" stop-color="#EAB308"/>
      <stop offset="70%" stop-color="#A16207"/><stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
    <radialGradient id="dial" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#2D3748"/><stop offset="70%" stop-color="#1A202C"/><stop offset="100%" stop-color="#0F131A"/>
    </radialGradient>
  </defs>
  <g filter="url(#m-shadow)">
    <g transform="translate(140, 140) rotate(-45) translate(-140, -140)">
      <polygon points="140,260 150,210 130,210" fill="#E2E8F0" stroke="#1E293B" stroke-width="1.5"/>
      <rect x="133" y="70" width="14" height="150" fill="#E2E8F0"/>
      <path d="M 100 62 C 120 60, 132 72, 140 68 C 148 72, 160 60, 180 62 C 185 68, 178 78, 165 74 C 150 72, 145 78, 140 78 C 135 78, 130 72, 115 74 C 102 78, 95 68, 100 62 Z" fill="url(#gold)" stroke="#451A03" stroke-width="2"/>
      <rect x="134" y="26" width="12" height="36" fill="#1E293B"/>
      <circle cx="140" cy="20" r="10" fill="url(#gold)"/>
    </g>
    <circle cx="140" cy="140" r="88" fill="url(#gold)" stroke="#FFDF00" stroke-width="3"/>
    <circle cx="140" cy="140" r="76" fill="none" stroke="#2D1B00" stroke-width="4"/>
    <circle cx="140" cy="140" r="64" fill="url(#dial)" stroke="#B45309" stroke-width="2.5"/>
  </g>
</svg>"""

def get_health_crest(style="comic"):
    if style == "comic":
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 260" width="260" height="260">
  <defs>
    <filter id="c-shadow-plaque" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.6"/>
    </filter>
  </defs>
  <g filter="url(#c-shadow-plaque)">
    <path d="M 82 50 L 178 50 A 26 26 0 0 0 210 82 L 210 178 A 26 26 0 0 0 178 210 L 82 210 A 26 26 0 0 0 50 178 L 50 82 A 26 26 0 0 0 82 50 Z" 
          fill="#EF4444" stroke="#111827" stroke-width="12" stroke-linejoin="round"/>
    <path d="M 90 64 L 170 64 A 18 18 0 0 0 196 90 L 196 170 A 18 18 0 0 0 170 196 L 90 196 A 18 18 0 0 0 64 170 L 64 90 A 18 18 0 0 0 90 64 Z" 
          fill="#991B1B" stroke="#111827" stroke-width="7" stroke-linejoin="round"/>
    <path d="M 76 86 L 76 68 L 102 68" fill="none" stroke="#FCA5A5" stroke-width="5" stroke-linecap="round"/>
  </g>
</svg>"""
    else:
        # Metallic Realistic
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280" width="280" height="280">
  <defs>
    <filter id="m-shadow-p" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity="0.8"/>
    </filter>
    <linearGradient id="p-gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/><stop offset="30%" stop-color="#EAB308"/>
      <stop offset="70%" stop-color="#A16207"/><stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
    <radialGradient id="p-ruby" cx="45%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#881337"/><stop offset="60%" stop-color="#4C0519"/><stop offset="100%" stop-color="#1A0208"/>
    </radialGradient>
  </defs>
  <g filter="url(#m-shadow-p)">
    <path d="M 85 55 L 195 55 C 195 72, 208 85, 225 85 L 225 195 C 208 195, 195 208, 195 225 L 85 225 C 85 208, 72 195, 55 195 L 55 85 C 72 85, 85 72, 85 55 Z" 
          fill="url(#p-gold)" stroke="#FFDF00" stroke-width="4"/>
    <circle cx="65" cy="65" r="9" fill="url(#p-gold)"/>
    <circle cx="215" cy="65" r="9" fill="url(#p-gold)"/>
    <circle cx="65" cy="215" r="9" fill="url(#p-gold)"/>
    <circle cx="215" cy="215" r="9" fill="url(#p-gold)"/>
    <path d="M 96 73 L 184 73 C 184 84, 194 94, 207 94 L 207 186 C 194 186, 184 196, 184 207 L 96 207 C 96 196, 86 186, 73 186 L 73 94 C 86 94, 96 84, 96 73 Z" 
          fill="url(#p-ruby)" stroke="#E11D48" stroke-width="2"/>
  </g>
</svg>"""

def get_card_frame(style="comic"):
    if style == "comic":
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 580" width="500" height="580">
  <defs>
    <filter id="c-card-s" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000" flood-opacity="0.6"/>
    </filter>
  </defs>
  <g filter="url(#c-card-s)">
    <path d="M 32 50 Q 32 20, 62 20 L 438 20 Q 468 20, 468 50 L 468 540 Q 468 554, 454 554 L 46 554 Q 32 554, 32 540 Z" fill="#334155" stroke="#111827" stroke-width="14" stroke-linejoin="round"/>
    <path d="M 44 54 Q 44 32, 66 32 L 434 32 Q 456 32, 456 54 L 456 534 L 44 534 Z" fill="#1E293B" stroke="#F59E0B" stroke-width="5" stroke-linejoin="round"/>
    <rect x="52" y="44" width="396" height="66" rx="8" fill="#F8FAFC" stroke="#111827" stroke-width="11" stroke-linejoin="round"/>
    <rect x="60" y="52" width="380" height="50" rx="5" fill="#FEF3C7" stroke="#D97706" stroke-width="3"/>
    <rect x="52" y="124" width="396" height="300" rx="10" fill="#0F172A" stroke="#111827" stroke-width="11" stroke-linejoin="round"/>
    <rect x="42" y="434" width="416" height="110" rx="8" fill="#1E293B" stroke="#111827" stroke-width="11" stroke-linejoin="round"/>
    <rect x="160" y="446" width="180" height="86" rx="12" fill="#F8FAFC" stroke="#111827" stroke-width="9" stroke-linejoin="round"/>
  </g>
</svg>"""
    else:
        # Metallic
        return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 700" width="600" height="700">
  <defs>
    <filter id="m-frame-s" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#000" flood-opacity="0.8"/>
    </filter>
    <linearGradient id="m-gold-c" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/><stop offset="30%" stop-color="#EAB308"/>
      <stop offset="70%" stop-color="#A16207"/><stop offset="100%" stop-color="#451A03"/>
    </linearGradient>
  </defs>
  <g filter="url(#m-frame-s)">
    <path d="M 40 40 Q 40 20, 60 20 L 540 20 Q 560 20, 560 40 L 560 670 Q 560 680, 550 680 L 50 680 Q 40 680, 40 670 Z" fill="#1E232E" stroke="url(#m-gold-c)" stroke-width="8"/>
    <rect x="65" y="45" width="470" height="75" rx="10" fill="url(#m-gold-c)" stroke="#FFDF00" stroke-width="2.5"/>
    <rect x="72" y="52" width="456" height="61" rx="7" fill="#181D24"/>
    <rect x="65" y="132" width="470" height="390" rx="12" fill="none" stroke="url(#m-gold-c)" stroke-width="6"/>
    <rect x="71" y="138" width="458" height="378" rx="8" fill="#161B26"/>
    <rect x="52" y="530" width="496" height="136" rx="8" fill="#13171F" stroke="url(#m-gold-c)" stroke-width="4"/>
    <rect x="175" y="542" width="250" height="112" rx="10" fill="#FDFBF7" stroke="url(#m-gold-c)" stroke-width="3.5"/>
  </g>
</svg>"""

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="엘잭 게임 초경량 벡터 에셋 빌더")
    parser.add_argument("--type", choices=["sword_badge", "health_crest", "card_frame", "all"], default="all", help="생성할 에셋 유형")
    parser.add_argument("--style", choices=["comic", "metallic"], default="comic", help="비주얼 스타일: comic (볼드 카툰풍) 또는 metallic (골드 메탈릭)")
    parser.add_argument("--out", default="./ui_assets", help="출력 디렉토리 경로")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    targets = []
    if args.type in ["sword_badge", "all"]:
        targets.append((f"{args.style}_badge_attack_sword.svg", get_sword_badge(args.style)))
    if args.type in ["health_crest", "all"]:
        targets.append((f"{args.style}_badge_health_crest.svg", get_health_crest(args.style)))
    if args.type in ["card_frame", "all"]:
        targets.append((f"{args.style}_card_frame_base.svg", get_card_frame(args.style)))

    print(f"=== [LJack Vector Asset Builder (Style: {args.style})] ===")
    for fname, svg_code in targets:
        p = os.path.join(args.out, fname)
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg_code)
        size_kb = len(svg_code) / 1024.0
        print(f"[OK] Generated: {p} ({size_kb:.1f} KB)")
    print(f"\nAll assets generated in {args.out}. Ready to import directly into Godot 4!\n")

if __name__ == "__main__":
    main()
