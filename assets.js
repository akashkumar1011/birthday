// Vector Graphic Assets & Generators for Birthday Card
// Includes Milk & Mocha cute bears, foil balloon numbers, tied yarn bows, and stickers

const ASSETS = {
  // 3D Glossy Pink Foil "HAPPY BIRTHDAY" Balloon Sticker
  happyBirthdayBalloonSvg: `
    <svg viewBox="0 0 500 110" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="foilGradHbd" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="15%" stop-color="#ffb8d9"/>
          <stop offset="45%" stop-color="#ff4382"/>
          <stop offset="70%" stop-color="#e01862"/>
          <stop offset="90%" stop-color="#ff85b3"/>
          <stop offset="100%" stop-color="#c21350"/>
        </linearGradient>
        <filter id="hbdPop" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="5" stdDeviation="5" flood-color="rgba(0,0,0,0.6)"/>
          <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="rgba(255,101,155,0.4)"/>
        </filter>
      </defs>
      <g filter="url(#hbdPop)">
        <!-- Outer white sticker border -->
        <text x="50%" y="42" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="44" fill="none" stroke="#ffffff" stroke-width="11" stroke-linejoin="round" letter-spacing="4">HAPPY</text>
        <text x="50%" y="94" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="52" fill="none" stroke="#ffffff" stroke-width="12" stroke-linejoin="round" letter-spacing="5">BIRTHDAY</text>
        
        <!-- Deep pink shadow line -->
        <text x="50%" y="42" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="44" fill="none" stroke="#8c0d3a" stroke-width="5" stroke-linejoin="round" letter-spacing="4">HAPPY</text>
        <text x="50%" y="94" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="52" fill="none" stroke="#8c0d3a" stroke-width="5" stroke-linejoin="round" letter-spacing="5">BIRTHDAY</text>
        
        <!-- Main Foil Gradient Fill -->
        <text x="50%" y="42" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="44" fill="url(#foilGradHbd)" letter-spacing="4">HAPPY</text>
        <text x="50%" y="94" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="52" fill="url(#foilGradHbd)" letter-spacing="5">BIRTHDAY</text>

        <!-- Glossy highlight glints -->
        <text x="49.5%" y="40.5" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="42" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.8" letter-spacing="4">HAPPY</text>
        <text x="49.5%" y="92.5" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="50" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.8" letter-spacing="5">BIRTHDAY</text>
      </g>
    </svg>
  `,

  // Cute Birthday Cake with Glowing Candles Sticker
  birthdayCakeSvg: `
    <svg viewBox="0 0 100 100" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="cakeGlow">
          <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="rgba(0,0,0,0.2)"/>
        </filter>
      </defs>
      <g filter="url(#cakeGlow)">
        <!-- Cake Stand -->
        <ellipse cx="50" cy="88" rx="36" ry="6" fill="#f8c9d8" stroke="#333" stroke-width="2"/>
        <path d="M 44 88 L 42 96 L 58 96 L 56 88 Z" fill="#f8c9d8" stroke="#333" stroke-width="2"/>
        <!-- Bottom Tier -->
        <rect x="22" y="62" width="56" height="24" rx="4" fill="#ffffff" stroke="#333" stroke-width="2"/>
        <path d="M 22 66 Q 30 74 36 66 Q 44 74 50 66 Q 58 74 64 66 Q 72 74 78 66 L 78 62 L 22 62 Z" fill="#ff7fa8"/>
        <!-- Top Tier -->
        <rect x="30" y="44" width="40" height="20" rx="3" fill="#ffffff" stroke="#333" stroke-width="2"/>
        <path d="M 30 48 Q 36 54 42 48 Q 50 54 58 48 Q 64 54 70 48 L 70 44 L 30 44 Z" fill="#ff7fa8"/>
        <!-- Strawberries / Cherries on Top -->
        <circle cx="36" cy="42" r="3.5" fill="#e01862"/>
        <circle cx="50" cy="42" r="3.5" fill="#e01862"/>
        <circle cx="64" cy="42" r="3.5" fill="#e01862"/>
        <!-- Candle -->
        <rect x="48" y="26" width="4" height="15" fill="#ffda79" stroke="#333" stroke-width="1.2"/>
        <!-- Candle Flame with Glow -->
        <path d="M 50 16 C 47 21, 48 24, 50 26 C 52 24, 53 21, 50 16 Z" fill="#ff5252"/>
        <circle cx="50" cy="22" r="2" fill="#fff176"/>
        <!-- Mini sparkles -->
        <path d="M 20 30 L 22 34 L 26 36 L 22 38 L 20 42 L 18 38 L 14 36 L 18 34 Z" fill="#ffd1dc"/>
        <path d="M 80 32 L 82 35 L 85 36 L 82 37 L 80 40 L 78 37 L 75 36 L 78 35 Z" fill="#ffd1dc"/>
      </g>
    </svg>
  `,

  // Cute White Bear holding Pink Heart (Milk bear)
  bearHeartSvg: `
    <svg viewBox="0 0 100 100" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="rgba(0,0,0,0.15)"/>
        </filter>
        <linearGradient id="pinkHeartGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#ff9ecb"/>
          <stop offset="50%" stop-color="#ff6b9d"/>
          <stop offset="100%" stop-color="#e0487c"/>
        </linearGradient>
      </defs>
      <!-- Ears -->
      <circle cx="28" cy="28" r="14" fill="#ffffff" stroke="#333333" stroke-width="2.5"/>
      <circle cx="28" cy="28" r="7" fill="#ffd1dc"/>
      <circle cx="72" cy="28" r="14" fill="#ffffff" stroke="#333333" stroke-width="2.5"/>
      <circle cx="72" cy="28" r="7" fill="#ffd1dc"/>
      <!-- Body & Head -->
      <path d="M 22 75 C 22 55, 30 45, 50 45 C 70 45, 78 55, 78 75 C 78 88, 70 94, 50 94 C 30 94, 22 88, 22 75 Z" fill="#ffffff" stroke="#333333" stroke-width="2.5"/>
      <ellipse cx="50" cy="46" rx="34" ry="30" fill="#ffffff" stroke="#333333" stroke-width="2.5"/>
      <!-- Eyes & Blush -->
      <circle cx="38" cy="46" r="3.2" fill="#222222"/>
      <circle cx="62" cy="46" r="3.2" fill="#222222"/>
      <circle cx="39" cy="45" r="1" fill="#ffffff"/>
      <circle cx="63" cy="45" r="1" fill="#ffffff"/>
      <ellipse cx="32" cy="52" rx="4.5" ry="2.5" fill="#ffb4c8" opacity="0.8"/>
      <ellipse cx="68" cy="52" rx="4.5" ry="2.5" fill="#ffb4c8" opacity="0.8"/>
      <!-- Snout & Mouth -->
      <ellipse cx="50" cy="51" rx="6" ry="4" fill="#fff5f7"/>
      <ellipse cx="50" cy="49" rx="2" ry="1.4" fill="#333333"/>
      <path d="M 47 52 Q 50 55 53 52" stroke="#333333" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      <!-- Paws holding Heart -->
      <g filter="url(#softGlow)">
        <path d="M 50 63 C 44 54, 32 54, 32 66 C 32 75, 45 83, 50 88 C 55 83, 68 75, 68 66 C 68 54, 56 54, 50 63 Z" fill="url(#pinkHeartGrad)" stroke="#ffffff" stroke-width="1.5"/>
        <path d="M 40 60 C 44 56, 48 60, 47 64" stroke="#ffffff" stroke-width="1.2" fill="none" stroke-linecap="round" opacity="0.8"/>
      </g>
      <!-- Arms hugging heart -->
      <ellipse cx="32" cy="68" rx="5.5" ry="7" fill="#ffffff" stroke="#333333" stroke-width="2" transform="rotate(-20 32 68)"/>
      <ellipse cx="68" cy="68" rx="5.5" ry="7" fill="#ffffff" stroke="#333333" stroke-width="2" transform="rotate(20 68 68)"/>
    </svg>
  `,

  // Two Bears Hugging (Mocha brown bear + Milk white bear)
  bearsHuggingSvg: `
    <svg viewBox="0 0 120 100" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="brownFur" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#b58263"/>
          <stop offset="100%" stop-color="#916142"/>
        </linearGradient>
      </defs>
      <!-- Brown Bear (Mocha) on left -->
      <circle cx="26" cy="38" r="11" fill="#b58263" stroke="#2c1a11" stroke-width="2.2"/>
      <circle cx="26" cy="38" r="5" fill="#885235"/>
      <ellipse cx="40" cy="54" rx="24" ry="22" fill="url(#brownFur)" stroke="#2c1a11" stroke-width="2.2"/>
      <circle cx="34" cy="52" r="2.8" fill="#1f130c"/>
      <ellipse cx="28" cy="57" rx="3.5" ry="2" fill="#d49a7a"/>
      <path d="M 37 56 Q 40 58 43 56" stroke="#1f130c" stroke-width="1.6" fill="none"/>
      
      <!-- White Bear (Milk) on right hugging Mocha -->
      <circle cx="94" cy="38" r="11" fill="#ffffff" stroke="#333333" stroke-width="2.2"/>
      <circle cx="94" cy="38" r="5" fill="#ffd1dc"/>
      <circle cx="70" cy="36" r="10" fill="#ffffff" stroke="#333333" stroke-width="2.2"/>
      <circle cx="70" cy="36" r="5" fill="#ffd1dc"/>
      <ellipse cx="78" cy="54" rx="24" ry="22" fill="#ffffff" stroke="#333333" stroke-width="2.2"/>
      <!-- Closed happy eyes on Milk bear -->
      <path d="M 68 53 Q 73 49 77 53" stroke="#222222" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M 83 53 Q 88 49 92 53" stroke="#222222" stroke-width="2" fill="none" stroke-linecap="round"/>
      <ellipse cx="68" cy="59" rx="4" ry="2" fill="#ffb4c8"/>
      <ellipse cx="90" cy="59" rx="4" ry="2" fill="#ffb4c8"/>
      <!-- Intertwined arms hugging -->
      <path d="M 50 64 C 58 60, 68 62, 74 66" stroke="#2c1a11" stroke-width="4.5" fill="none" stroke-linecap="round"/>
      <path d="M 66 66 C 58 68, 48 66, 42 62" stroke="#ffffff" stroke-width="4.5" fill="none" stroke-linecap="round"/>
      <!-- Floating mini hearts -->
      <path d="M 58 26 C 55 20, 48 20, 48 27 C 48 32, 58 38, 58 38 C 58 38, 68 32, 68 27 C 68 20, 61 20, 58 26 Z" fill="#ff5c8a"/>
    </svg>
  `,

  // Tied Pink Yarn Bow
  yarnBowSvg: `
    <svg viewBox="0 0 100 80" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="yarnShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="rgba(0,0,0,0.3)"/>
        </filter>
      </defs>
      <g filter="url(#yarnShadow)">
        <!-- Left Loop -->
        <path d="M 48 36 C 30 15, 8 20, 14 38 C 20 54, 42 46, 48 38" fill="none" stroke="#e6397d" stroke-width="5.5" stroke-linecap="round"/>
        <path d="M 48 36 C 30 15, 8 20, 14 38 C 20 54, 42 46, 48 38" fill="none" stroke="#ff75a6" stroke-width="2" stroke-linecap="round"/>
        <!-- Right Loop -->
        <path d="M 52 36 C 70 15, 92 20, 86 38 C 80 54, 58 46, 52 38" fill="none" stroke="#e6397d" stroke-width="5.5" stroke-linecap="round"/>
        <path d="M 52 36 C 70 15, 92 20, 86 38 C 80 54, 58 46, 52 38" fill="none" stroke="#ff75a6" stroke-width="2" stroke-linecap="round"/>
        <!-- Center Knot -->
        <ellipse cx="50" cy="37" rx="6.5" ry="5.5" fill="#d81b60" stroke="#ff85af" stroke-width="1.8"/>
        <!-- Hanging tails -->
        <path d="M 47 40 C 42 54, 30 64, 20 72" fill="none" stroke="#e6397d" stroke-width="4.8" stroke-linecap="round"/>
        <path d="M 47 40 C 42 54, 30 64, 20 72" fill="none" stroke="#ff75a6" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M 53 40 C 58 54, 72 64, 82 72" fill="none" stroke="#e6397d" stroke-width="4.8" stroke-linecap="round"/>
        <path d="M 53 40 C 58 54, 72 64, 82 72" fill="none" stroke="#ff75a6" stroke-width="1.8" stroke-linecap="round"/>
      </g>
    </svg>
  `,

  // Glossy 3D Pink Heart Sticker
  glossyHeartSvg: `
    <svg viewBox="0 0 80 80" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="heartSphere" cx="35%" cy="35%" r="65%">
          <stop offset="0%" stop-color="#ffb6d5"/>
          <stop offset="40%" stop-color="#ff4d8d"/>
          <stop offset="85%" stop-color="#c2185b"/>
          <stop offset="100%" stop-color="#880e4f"/>
        </radialGradient>
        <filter id="stickerShadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="2" dy="3" stdDeviation="3" flood-color="rgba(0,0,0,0.4)"/>
        </filter>
      </defs>
      <g filter="url(#stickerShadow)">
        <path d="M 40 22 C 34 8, 14 8, 14 26 C 14 42, 34 58, 40 66 C 46 58, 66 42, 66 26 C 66 8, 46 8, 40 22 Z" fill="url(#heartSphere)" stroke="#ffffff" stroke-width="2"/>
        <ellipse cx="28" cy="22" rx="7" ry="4" fill="#ffffff" opacity="0.65" transform="rotate(-30 28 22)"/>
        <circle cx="34" cy="27" r="2" fill="#ffffff" opacity="0.75"/>
      </g>
    </svg>
  `,

  // Hand-Drawn Pink Botanical Flower Stems Doodle
  botanicalStemSvg: `
    <svg viewBox="0 0 60 90" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <path d="M 30 85 C 30 55, 34 35, 32 15" stroke="#ffa4c5" stroke-width="2" fill="none" stroke-linecap="round"/>
      <!-- Leaves -->
      <path d="M 31 65 C 22 62, 16 54, 18 46 C 26 48, 30 58, 31 65 Z" fill="#ff7da7" opacity="0.8"/>
      <path d="M 31 48 C 40 45, 46 38, 44 30 C 36 32, 32 42, 31 48 Z" fill="#ff7da7" opacity="0.8"/>
      <path d="M 32 30 C 24 26, 20 18, 22 12 C 28 14, 31 22, 32 30 Z" fill="#ffa4c5" opacity="0.9"/>
      <!-- Little Blossom Buds -->
      <circle cx="32" cy="13" r="4.5" fill="#ffffff" stroke="#ff4d8d" stroke-width="1.5"/>
      <circle cx="18" cy="46" r="3" fill="#ff4d8d"/>
      <circle cx="44" cy="30" r="3" fill="#ff4d8d"/>
    </svg>
  `,

  // Hand-Drawn Ribbon Bow Doodle (like in user reference image)
  drawnBowSvg: `
    <svg viewBox="0 0 80 50" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
      <!-- Left loop -->
      <path d="M 38 22 C 25 8, 10 12, 15 26 C 20 38, 35 32, 38 24" fill="none" stroke="#ffa4c5" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Right loop -->
      <path d="M 42 22 C 55 8, 70 12, 65 26 C 60 38, 45 32, 42 24" fill="none" stroke="#ffa4c5" stroke-width="2.5" stroke-linecap="round"/>
      <!-- Center Knot -->
      <ellipse cx="40" cy="23" rx="4" ry="3.5" fill="#ff659b"/>
      <!-- Tails -->
      <path d="M 38 25 C 34 35, 26 42, 18 46" fill="none" stroke="#ffa4c5" stroke-width="2.2" stroke-linecap="round"/>
      <path d="M 42 25 C 46 35, 54 42, 62 46" fill="none" stroke="#ffa4c5" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
  `,

  // 3D Foil Balloon Number Generator (SVG)
  getNumberSvg: function(numStr) {
    return `
      <svg viewBox="0 0 160 120" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="foilGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffd2e5"/>
            <stop offset="25%" stop-color="#ff7da7"/>
            <stop offset="50%" stop-color="#ff4382"/>
            <stop offset="75%" stop-color="#ffaec9"/>
            <stop offset="100%" stop-color="#e02466"/>
          </linearGradient>
          <filter id="balloonPop" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="3" dy="6" stdDeviation="4" flood-color="rgba(0,0,0,0.5)"/>
          </filter>
        </defs>
        <g filter="url(#balloonPop)">
          <text x="50%" y="82" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="88" fill="none" stroke="#ffffff" stroke-width="12" stroke-linejoin="round" letter-spacing="4">${numStr}</text>
          <text x="50%" y="82" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="88" fill="none" stroke="#901344" stroke-width="6" stroke-linejoin="round" letter-spacing="4">${numStr}</text>
          <text x="50%" y="82" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="88" fill="url(#foilGrad)" letter-spacing="4">${numStr}</text>
          <text x="49%" y="80" text-anchor="middle" font-family="'Outfit', sans-serif" font-weight="900" font-size="85" fill="none" stroke="#ffffff" stroke-width="2.5" opacity="0.75" letter-spacing="4">${numStr}</text>
        </g>
      </svg>
    `;
  }
};
