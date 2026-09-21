const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. ADD CSS STYLES FOR TOURNAMENT STANDINGS & INTERMISSION & FINAL SCREEN
const tournamentCSS = `
    /* Round 6: Nebula Tournament Styles */
    .standings-card {
      background: rgba(10, 6, 28, 0.88);
      border: 1px solid rgba(255, 215, 0, 0.4);
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 15px rgba(255, 215, 0, 0.15);
      backdrop-filter: blur(8px);
      overflow: hidden;
      min-width: 260px;
    }
    .standings-table {
      width: 100%; border-collapse: collapse; text-align: left; font-size: 11px;
    }
    .standings-table th, .standings-table td {
      padding: 4px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .standings-table th {
      background: rgba(255, 215, 0, 0.1); color: #ffd700;
      font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
    }
    .standings-row-player {
      background: rgba(0, 246, 255, 0.15); font-weight: 800; color: #00f6ff;
    }
    .standings-row-ai {
      color: #e2e8f0; font-weight: 600;
    }

    /* Intermission Modal Overlay */
    .intermission-card {
      background: rgba(13, 8, 35, 0.96);
      border: 2px solid #ffd700;
      border-radius: 14px; padding: 28px 36px;
      max-width: 700px; width: 90%;
      box-shadow: 0 10px 40px rgba(0,0,0,0.85), 0 0 30px rgba(255, 215, 0, 0.3);
      display: flex; flex-direction: column; gap: 20px; text-align: center;
    }
    .intermission-title {
      font-size: 26px; font-weight: 900; letter-spacing: 2px;
      color: #ffd700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
    }
    .intermission-subtitle {
      font-size: 15px; color: #00f6ff; font-weight: 700; letter-spacing: 1px;
    }
    .tournament-grid-table {
      width: 100%; border-collapse: collapse; font-size: 13px; text-align: center;
      margin-top: 8px;
    }
    .tournament-grid-table th, .tournament-grid-table td {
      border: 1px solid rgba(255, 255, 255, 0.12); padding: 8px 12px;
    }
    .tournament-grid-table th {
      background: rgba(255, 215, 0, 0.15); color: #ffd700; font-weight: 800;
    }
    .champ-highlight {
      background: rgba(255, 215, 0, 0.22) !important;
      border: 2px solid #ffd700 !important;
      font-weight: 900 !important; color: #fff !important;
      text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    }
`;

html = html.replace('</style>', tournamentCSS + '\n  </style>');

// 2. INSERT LIVE STANDINGS TABLE IN HEADER BAR (right beside scoreboard)
const oldScoreboardCard = `<div class="scoreboard-card" id="scoreboard-card">`;
const newScoreboardAndStandings = `<!-- Live Tournament Standings Panel (always visible during play) -->
      <div class="standings-card" id="tournament-standings-card">
        <table class="standings-table">
          <thead>
            <tr>
              <th>POS</th>
              <th>BOWLER</th>
              <th>G1</th>
              <th>G2</th>
              <th>G3</th>
              <th style="color:#ffd700; text-align:right;">TOTAL</th>
            </tr>
          </thead>
          <tbody id="tournament-standings-tbody">
            <!-- Rendered dynamically -->
          </tbody>
        </table>
      </div>

      <div class="scoreboard-card" id="scoreboard-card">`;

html = html.replace(oldScoreboardCard, newScoreboardAndStandings);

// 3. REPLACE READY SCREEN WITH TOURNAMENT READY SCREEN
const oldReadyScreen = `  <!-- Mode Select (Ready) -->
  <div class="overlay-screen" id="screen-ready" style="display:flex;">
    <div class="overlay-content">
      <div class="hero-title">COMET LANES</div>
      <div class="hero-subtitle">Cosmic 3D Bowling Night — Deterministic Physics</div>
      <div class="cards-row" style="max-width:650px;">
        <div class="select-card active" id="card-mode-reg" onclick="setSelectMode('REGULATION')">
          <div class="card-title">REGULATION GAME <span class="card-badge">Full</span></div>
          <div class="card-desc">Standard 10-frame bowling with strikes, spares, frame-10 bonus balls, and live scoreboard.</div>
        </div>
        <div class="select-card" id="card-mode-count" onclick="setSelectMode('COUNT')">
          <div class="card-title">COUNT SESSION <span class="card-badge">10 Throws</span></div>
          <div class="card-desc">10 independent throws at fresh 10-pin racks. Pure running pinfall counter.</div>
        </div>
      </div>
      <div class="prompt-footer">
        Use <span class="key-hint">↑</span> / <span class="key-hint">↓</span> to choose, press <span class="key-hint">Enter</span> to Start
      </div>
    </div>
  </div>`;

const newReadyScreen = `  <!-- Tournament Ready Screen (Round 6) -->
  <div class="overlay-screen" id="screen-ready" style="display:flex;">
    <div class="overlay-content">
      <div class="hero-title">NEBULA TOURNAMENT</div>
      <div class="hero-subtitle">3-Game Cosmic Bowling Championship against VEla & Riko</div>
      <div class="cards-row" style="max-width:760px;">
        <div class="select-card active" style="cursor:default;">
          <div class="card-title">TOURNAMENT FORMAT <span class="card-badge">3 Games</span></div>
          <div class="card-desc">Three consecutive full regulation 10-frame games on assigned cosmic lanes:</div>
          <div class="card-traits" style="margin-top:8px;">
            <div><span style="color:#ffd700;">GAME 1:</span> Lane 1 — VELOCITY BELT (Speed crystals z=[8, 10])</div>
            <div><span style="color:#ffd700;">GAME 2:</span> Lane 4 — GATE WORKS (Swinging hazard gate z=10.0)</div>
            <div><span style="color:#ffd700;">GAME 3:</span> Lane 3 — GUARD RAIL (Luminous edge rebound rails)</div>
          </div>
          <div class="card-desc" style="margin-top:6px; color:#cbd5e1;">
            Opponents: <b style="color:#00f6ff;">VEla</b> (Grand Total 692) & <b style="color:#d946ef;">Riko</b> (Grand Total 588).
          </div>
        </div>
      </div>
      <div class="prompt-footer">
        Press <span class="key-hint">Enter</span> to Start Tournament
      </div>
    </div>
  </div>`;

html = html.replace(oldReadyScreen, newReadyScreen);

// 4. REMOVE FREE LANE SELECT SCREEN HTML COMPLETELY
const laneSelectSearch = `  <!-- Lane Select (Lanes 0 - 5) -->
  <div class="overlay-screen" id="screen-lane-select" style="display:none;">
    <div class="overlay-content">
      <div class="hero-title" style="font-size:32px;">SELECT LANE GADGET</div>
      <div class="hero-subtitle" id="lane-select-subtitle">CHOOSE LANE FOR FRAME 1</div>
      <div class="cards-row" style="max-width:920px;">
        <!-- Lane 0 -->
        <div class="select-card active" id="card-lane-0" onclick="setLaneIndex(0)">
          <div class="card-title">CLASSIC COMET <span class="card-badge">LANE 0</span></div>
          <div class="card-desc">Pure regulation cosmic deck without gadgets or hazards.</div>
        </div>
        <!-- Lane 1 -->
        <div class="select-card" id="card-lane-1" onclick="setLaneIndex(1)">
          <div class="card-title">VELOCITY BELT <span class="card-badge">LANE 1</span></div>
          <div class="card-desc">Speed crystal strip at z=[8, 10]: boosts ball speed by ×1.4 (capped at 16.0 m/s).</div>
        </div>
        <!-- Lane 2 -->
        <div class="select-card" id="card-lane-2" onclick="setLaneIndex(2)">
          <div class="card-title">MOSS DRIFT <span class="card-badge">LANE 2</span></div>
          <div class="card-desc">Two slow moss patches at z=[6, 8] and z=[12, 14]: slows speed by ×0.7.</div>
        </div>
        <!-- Lane 3 -->
        <div class="select-card" id="card-lane-3" onclick="setLaneIndex(3)">
          <div class="card-title">GUARD RAIL <span class="card-badge">LANE 3</span></div>
          <div class="card-desc">Luminous rebound rails save gutter balls (rebound lateral vx ×0.8; Bouncer snaps 35°).</div>
        </div>
        <!-- Lane 4 -->
        <div class="select-card" id="card-lane-4" onclick="setLaneIndex(4)">
          <div class="card-title">GATE WORKS <span class="card-badge">LANE 4</span></div>
          <div class="card-desc">Swinging hazard gate at z=10.0 (period 2.4s): blocks lane during [0.9s, 1.7s).</div>
        </div>
        <!-- Lane 5 -->
        <div class="select-card" id="card-lane-5" onclick="setLaneIndex(5)">
          <div class="card-title">HAZARD GAUNTLET <span class="card-badge">LANE 5</span></div>
          <div class="card-desc">Speed strip z=[5, 6.5] → Swinging gate z=10.0 → Slow moss z=[12.5, 14.0].</div>
        </div>
      </div>
      <div class="prompt-footer">
        Use <span class="key-hint">←</span> / <span class="key-hint">→</span> to browse, press <span class="key-hint">Enter</span> to Confirm Lane
      </div>
    </div>
  </div>`;

html = html.replace(laneSelectSearch, '');

// 5. ADD INTERMISSION AND FINAL STANDINGS SCREENS HTML before script
const oldGameOver = `  <!-- Game Over Screen -->
  <div class="overlay-screen" id="screen-game-over" style="display:none;">
    <div class="overlay-content">
      <div class="hero-title" style="color:#ffd700;" id="go-title">GAME COMPLETE</div>
      <div class="hero-subtitle" id="go-subtitle">FINAL SCORE: 0</div>
      <div id="go-details" style="font-size:16px; color:#e2e8f0; max-width:600px; line-height:1.6;"></div>
      <div class="prompt-footer">
        Press <span class="key-hint">R</span> to Return to Menu & Play Again
      </div>
    </div>
  </div>`;

const newOverlays = `  <!-- Intermission Screen between Games (Round 6) -->
  <div class="overlay-screen" id="screen-intermission" style="display:none;">
    <div class="intermission-card">
      <div class="intermission-title" id="intermission-title">GAME 1 COMPLETE</div>
      <div class="intermission-subtitle" id="intermission-subtitle">GAME 1 RESULTS & TOURNAMENT STANDINGS</div>
      <table class="tournament-grid-table">
        <thead>
          <tr>
            <th>POS</th>
            <th>BOWLER</th>
            <th>THIS GAME</th>
            <th>GRAND TOTAL</th>
          </tr>
        </thead>
        <tbody id="intermission-tbody"></tbody>
      </table>
      <div class="prompt-footer" style="margin-top:12px;">
        Press <span class="key-hint">Enter</span> to Proceed to Next Game
      </div>
    </div>
  </div>

  <!-- Final Championship Standings Screen (Round 6) -->
  <div class="overlay-screen" id="screen-final-standings" style="display:none;">
    <div class="intermission-card" style="max-width:800px;">
      <div class="intermission-title" style="font-size:32px;">FINAL TOURNAMENT STANDINGS</div>
      <div class="intermission-subtitle" id="final-champion-banner">CHAMPION: PLAYER</div>
      <table class="tournament-grid-table">
        <thead>
          <tr>
            <th>RANK</th>
            <th>BOWLER</th>
            <th>GAME 1</th>
            <th>GAME 2</th>
            <th>GAME 3</th>
            <th style="color:#ffd700;">GRAND TOTAL</th>
          </tr>
        </thead>
        <tbody id="final-standings-tbody"></tbody>
      </table>
      <div id="final-tiebreak-note" style="font-size:12px; color:#94a3b8; font-style:italic;">
        Ties ranked by Game 3 subtotal, then Game 2 subtotal.
      </div>
      <div class="prompt-footer" style="margin-top:14px;">
        Press <span class="key-hint">R</span> to Reset and Play Tournament Again
      </div>
    </div>
  </div>`;

html = html.replace(oldGameOver, newOverlays);

fs.writeFileSync('index.html', html, 'utf8');
console.log('UI and Screens updated successfully!');
