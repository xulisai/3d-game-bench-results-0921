# -*- coding: utf-8 -*-
import sys

# Generate parts for C5 index.html
print("Starting C5 generator...")

part1 = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tin Soldier Command</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
    body, html { width: 100%; height: 100%; overflow: hidden; background: #070913; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #canvas-container { width: 100%; height: 100%; position: absolute; left: 0; top: 0; }
    
    /* Top Status HUD */
    #hud-top {
      position: absolute; top: 10px; left: 50%; transform: translateX(-50%);
      display: flex; gap: 14px; align-items: center;
      background: rgba(12, 16, 28, 0.92); border: 1px solid #3c4b6e;
      border-radius: 8px; padding: 7px 18px; color: #e2e8f0;
      box-shadow: 0 8px 24px rgba(0,0,0,0.6); pointer-events: none; z-index: 10;
    }
    .hud-stat { display: flex; flex-direction: column; align-items: center; min-width: 58px; }
    .hud-label { font-size: 9px; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; font-weight: 600; }
    .hud-val { font-size: 17px; font-weight: 700; color: #f8fafc; font-variant-numeric: tabular-nums; }
    .hud-val.alert { color: #f87171; }
    .hud-val.gold { color: #fbbf24; }
    .hud-val.caps { color: #38bdf8; }
    .hud-val.wave { color: #f43f5e; }

    /* Control Groups bar */
    #hud-groups {
      position: absolute; top: 68px; left: 50%; transform: translateX(-50%);
      display: flex; gap: 10px; align-items: center; pointer-events: none; z-index: 10;
    }
    .group-badge {
      background: rgba(15, 23, 42, 0.85); border: 1px solid #475569; border-radius: 4px;
      padding: 3px 10px; font-size: 12px; font-weight: 600; color: #94a3b8;
      display: none;
    }
    .group-badge.active { display: inline-block; color: #38bdf8; border-color: #38bdf8; }

    /* Build Mode Indicator */
    #build-mode-indicator {
      position: absolute; top: 16px; left: 16px; background: rgba(59, 130, 246, 0.9);
      color: #fff; font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 6px;
      letter-spacing: 1px; display: none; z-index: 10; box-shadow: 0 4px 12px rgba(59,130,246,0.4);
    }

    /* Barracks UI Panel */
    #barracks-card {
      position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
      background: rgba(12, 16, 28, 0.94); border: 1px solid #3b82f6;
      border-radius: 8px; padding: 12px 22px; color: #e2e8f0;
      display: flex; flex-direction: column; gap: 10px; min-width: 500px; max-width: 90vw;
      box-shadow: 0 10px 30px rgba(0,0,0,0.8); z-index: 15;
      transition: opacity 0.2s;
    }
    #barracks-card.hidden { display: none; }
    .barracks-header { display: flex; justify-content: space-between; align-items: center; }
    .barracks-title { font-size: 16px; font-weight: 700; color: #60a5fa; }
    .barracks-queue-info { font-size: 12px; color: #94a3b8; }
    .barracks-buttons { display: flex; gap: 8px; }
    .btn-prod {
      background: #1e293b; border: 1px solid #475569; border-radius: 6px;
      color: #f1f5f9; padding: 7px 10px; font-size: 11px; font-weight: 600;
      cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 2px;
      transition: background 0.15s, border-color 0.15s; flex: 1;
    }
    .btn-prod:hover:not(:disabled) { background: #334155; border-color: #38bdf8; color: #38bdf8; }
    .btn-prod:disabled { opacity: 0.45; cursor: not-allowed; }
    .btn-prod .cost { color: #fbbf24; font-size: 10px; }
    .btn-prod .time { color: #94a3b8; font-size: 9px; }
    .prod-progress-wrap { width: 100%; height: 6px; background: #0f172a; border-radius: 3px; overflow: hidden; border: 1px solid #334155; }
    .prod-progress-fill { height: 100%; background: #38bdf8; width: 0%; transition: width 0.1s linear; }

    /* Selection Details Panel */
    #selection-card {
      position: absolute; bottom: 16px; left: 50%; transform: translateX(-50%);
      background: rgba(12, 16, 28, 0.92); border: 1px solid #3c4b6e;
      border-radius: 8px; padding: 10px 22px; color: #e2e8f0;
      display: flex; gap: 24px; align-items: center; min-width: 400px; max-width: 85vw;
      box-shadow: 0 10px 30px rgba(0,0,0,0.7); pointer-events: none; z-index: 10;
      transition: opacity 0.2s;
    }
    #selection-card.hidden { display: none; }
    .sel-info { display: flex; flex-direction: column; gap: 2px; }
    .sel-title { font-size: 15px; font-weight: 700; color: #38bdf8; letter-spacing: 0.5px; }
    .sel-desc { font-size: 11px; color: #94a3b8; }
    .sel-bars { display: flex; flex-direction: column; gap: 6px; flex-grow: 1; }
    .bar-row { display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 600; }
    .bar-wrap { flex-grow: 1; height: 7px; background: #1e293b; border-radius: 4px; overflow: hidden; border: 1px solid #334155; position: relative; }
    .bar-fill-hp { height: 100%; background: #22c55e; transition: width 0.1s linear; }
    .bar-fill-spring { height: 100%; background: #f59e0b; transition: width 0.1s linear; }

    /* Drag Box Overlay */
    #select-rect {
      position: absolute; border: 1px solid #38bdf8; background: rgba(56, 189, 248, 0.15);
      display: none; pointer-events: none; z-index: 20;
    }

    /* Attack Cursor Indicator */
    #attack-mode-indicator {
      position: absolute; top: 48px; left: 16px; background: rgba(239, 68, 68, 0.9);
      color: #fff; font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 6px;
      letter-spacing: 1px; display: none; z-index: 10; box-shadow: 0 4px 12px rgba(239,68,68,0.4);
    }

    /* Modals & Banners */
    .modal-overlay {
      position: absolute; inset: 0; background: rgba(5, 7, 15, 0.85);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      z-index: 100; backdrop-filter: blur(4px);
    }
    .modal-overlay.hidden { display: none; }
    .modal-box {
      background: #0f172a; border: 2px solid #38bdf8; border-radius: 12px;
      padding: 24px 34px; max-width: 680px; text-align: center; color: #f1f5f9;
      box-shadow: 0 16px 48px rgba(0,0,0,0.8); max-height: 90vh; overflow-y: auto;
    }
    .modal-title { font-size: 28px; font-weight: 800; letter-spacing: 2px; color: #fbbf24; text-shadow: 0 2px 10px rgba(251,191,36,0.3); margin-bottom: 8px; }
    .modal-subtitle { font-size: 13px; color: #cbd5e1; margin-bottom: 12px; line-height: 1.5; }
    .key-grid {
      display: grid; grid-template-columns: 140px 1fr; gap: 6px 14px;
      text-align: left; font-size: 12px; margin: 12px 0 16px 0;
      background: #1e293b; padding: 12px 16px; border-radius: 8px; border: 1px solid #334155;
    }
    .key-tag { font-weight: 700; color: #38bdf8; }
    .start-prompt { font-size: 15px; font-weight: 700; color: #22c55e; animation: pulse 1.5s infinite ease-in-out; }
    @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.65; transform: scale(0.98); } }

    #banner-win, #banner-lose {
      position: absolute; inset: 0; background: rgba(4, 7, 18, 0.88);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      z-index: 110; pointer-events: none;
    }
    #banner-win.hidden, #banner-lose.hidden { display: none; }
    .banner-text-win { font-size: 58px; font-weight: 900; color: #4ade80; letter-spacing: 4px; text-shadow: 0 0 32px rgba(74,222,128,0.5); }
    .banner-text-lose { font-size: 58px; font-weight: 900; color: #f87171; letter-spacing: 4px; text-shadow: 0 0 32px rgba(248,113,113,0.5); }
    .banner-sub { font-size: 18px; color: #e2e8f0; margin-top: 14px; font-weight: 600; letter-spacing: 1px; }
  </style>
  <script src="./assets/_shared/three/build/three.min.js"></script>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="select-rect"></div>
  <div id="build-mode-indicator">BUILD DOMINO WALL (DRAG GROUND)</div>
  <div id="attack-mode-indicator">ATTACK-MOVE (A + LEFT CLICK)</div>

  <div id="hud-top">
    <div class="hud-stat">
      <span class="hud-label">Bottlecaps</span>
      <span id="stat-caps" class="hud-val caps">50</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Next Wave</span>
      <span id="stat-wave" class="hud-val wave">02:00</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Barracks HP</span>
      <span id="stat-barracks-hp" class="hud-val">300</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Bowl Marbles</span>
      <span id="stat-marbles" class="hud-val gold">0 / 5</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Tin Army</span>
      <span id="stat-soldiers" class="hud-val">12</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Outposts</span>
      <span id="stat-outposts" class="hud-val alert">3</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Patrols</span>
      <span id="stat-patrols" class="hud-val alert">2</span>
    </div>
    <div class="hud-stat">
      <span class="hud-label">Clock</span>
      <span id="stat-clock" class="hud-val gold">00:00</span>
    </div>
  </div>

  <div id="hud-groups">
    <div id="grp-badge-1" class="group-badge">[1: 0]</div>
    <div id="grp-badge-2" class="group-badge">[2: 0]</div>
    <div id="grp-badge-3" class="group-badge">[3: 0]</div>
    <div id="grp-badge-4" class="group-badge">[4: 0]</div>
  </div>

  <!-- Barracks Panel -->
  <div id="barracks-card" class="hidden">
    <div class="barracks-header">
      <div class="barracks-title">Toybox Barracks</div>
      <div id="barracks-queue-label" class="barracks-queue-info">Queue: 0/5</div>
    </div>
    <div class="prod-progress-wrap">
      <div id="barracks-progress" class="prod-progress-fill"></div>
    </div>
    <div class="barracks-buttons">
      <button id="btn-prod-rifleman" class="btn-prod">
        <span>Rifleman</span>
        <span class="cost">30 Caps</span>
        <span class="time">8s</span>
      </button>
      <button id="btn-prod-drummer" class="btn-prod">
        <span>Drummer</span>
        <span class="cost">50 Caps</span>
        <span class="time">12s</span>
      </button>
      <button id="btn-prod-orderly" class="btn-prod">
        <span>Orderly</span>
        <span class="cost">40 Caps</span>
        <span class="time">10s</span>
      </button>
      <button id="btn-prod-cavalry" class="btn-prod">
        <span>Cavalry</span>
        <span class="cost">70 Caps</span>
        <span class="time">15s</span>
      </button>
      <button id="btn-prod-catapult" class="btn-prod">
        <span>Catapult</span>
        <span class="cost">100 Caps</span>
        <span class="time">20s</span>
      </button>
    </div>
  </div>

  <!-- Selection Card -->
  <div id="selection-card" class="hidden">
    <div class="sel-info">
      <div id="sel-name" class="sel-title">Tin Squad</div>
      <div id="sel-details" class="sel-desc">10 Riflemen, 2 Drummers</div>
    </div>
    <div class="sel-bars">
      <div class="bar-row">
        <span style="color:#22c55e; width:45px;">HP</span>
        <div class="bar-wrap"><div id="sel-hp-fill" class="bar-fill-hp" style="width: 100%;"></div></div>
        <span id="sel-hp-text" style="width:55px; text-align:right;">100%</span>
      </div>
      <div class="bar-row">
        <span style="color:#f59e0b; width:45px;">SPRING</span>
        <div class="bar-wrap"><div id="sel-spring-fill" class="bar-fill-spring" style="width: 100%;"></div></div>
        <span id="sel-spring-text" style="width:55px; text-align:right;">100%</span>
      </div>
    </div>
  </div>

  <!-- Ready Modal -->
  <div id="ready-modal" class="modal-overlay">
    <div class="modal-box">
      <div class="modal-title">TIN SOLDIER COMMAND</div>
      <div class="modal-subtitle">Bedroom Floor Battlefield — Operation Toybox<br>Defend the Barracks against Green Army assault waves & destroy all outposts!</div>
      <div class="key-grid">
        <div class="key-tag">Left Click</div><div>Select soldier or Toybox Barracks</div>
        <div class="key-tag">Box Drag</div><div>Box-select friendly soldiers</div>
        <div class="key-tag">Right Click Ground</div><div>Move in 1.2-grid / Set Barracks rally flag / Catapult fire</div>
        <div class="key-tag">Right Click Target</div><div>Attack enemy / Cavalry charge / Orderly rewind / Collect marble</div>
        <div class="key-tag">A + Left Click</div><div>Attack-Move (advance & auto-engage enemies)</div>
        <div class="key-tag">B Key</div><div>Build Mode: drag ground to lay Domino Walls (5 caps/tile)</div>
        <div class="key-tag">T Key</div><div>Build Mode: click ground to build Night-light Tower (40 caps)</div>
        <div class="key-tag">Assault Waves</div><div>Waves at 120s, 300s, 480s with Green Sergeants! Defend Barracks</div>
        <div class="key-tag">Winder Orderly</div><div>ONLY source of spring! Winding: target +18/s, self -6/s</div>
        <div class="key-tag">R Key</div><div>Reset game to initial state at any time</div>
      </div>
      <div class="start-prompt">PRESS [ ENTER ] TO COMMENCE BATTLE</div>
    </div>
  </div>

  <div id="banner-win" class="hidden">
    <div class="banner-text-win">FLOOR SECURED</div>
    <div class="banner-sub">All plastic army outposts neutralized! Press [ R ] to play again.</div>
  </div>

  <div id="banner-lose" class="hidden">
    <div class="banner-text-lose">DEFEAT</div>
    <div class="banner-sub">Your base was overrun or tin soldiers lost. Press [ R ] to retry.</div>
  </div>
'''

with open('c5_part1.html', 'w') as f:
    f.write(part1)
print("Part 1 written")
