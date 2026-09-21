# Assemble index.html part 1: HTML Head and CSS
part1 = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Niulai: The Long Dream</title>
  <style>
    * {
      box-sizing: border-box;
      user-select: none;
      margin: 0;
      padding: 0;
    }
    body, html {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #3b4541;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #game-canvas {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: block;
    }
    #ui-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 60;
    }
    .hud-box {
      position: absolute;
      background: rgba(20, 26, 22, 0.82);
      border: 1.5px solid rgba(220, 235, 215, 0.35);
      color: #f7faee;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 0.6px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.35);
      text-shadow: 1px 1px 2px rgba(0,0,0,0.85);
    }
    #hud-zone {
      top: 22px;
      left: 22px;
      font-size: 17px;
      color: #e2ecd8;
      transition: color 0.6s ease;
    }
    #hud-zone.dream {
      color: #fff4ca;
    }
    #hud-memories {
      top: 22px;
      right: 22px;
      font-size: 17px;
      color: #ffd875;
    }
    #hud-strikes {
      top: 66px;
      right: 22px;
      font-size: 16px;
      color: #ff6b6b;
      display: none;
    }
    #hud-controls-hint {
      bottom: 22px;
      left: 22px;
      font-size: 13px;
      color: #d8e5d0;
      opacity: 0.9;
    }
    #hud-companion-prompt {
      bottom: 60px;
      left: 22px;
      font-size: 14px;
      color: #ffeb99;
      background: rgba(36, 46, 28, 0.88);
      border: 1.5px solid rgba(255, 235, 150, 0.45);
      display: none;
    }
    #hud-rest-prompt {
      bottom: 98px;
      left: 22px;
      font-size: 14px;
      color: #bbf2f6;
      background: rgba(22, 38, 44, 0.90);
      border: 1.5px solid rgba(160, 235, 245, 0.55);
      display: none;
    }
    #story-banner {
      position: absolute;
      top: 14%;
      left: 0;
      width: 100%;
      background: linear-gradient(90deg, rgba(16,24,16,0) 0%, rgba(18,26,20,0.94) 15%, rgba(18,26,20,0.94) 85%, rgba(16,24,16,0) 100%);
      border-top: 2px solid #ecd896;
      border-bottom: 2px solid #ecd896;
      padding: 24px 36px;
      color: #fffbe8;
      font-size: 21px;
      text-align: center;
      line-height: 1.55;
      letter-spacing: 0.8px;
      text-shadow: 0 2px 5px rgba(0,0,0,0.95);
      opacity: 0;
      transform: translateY(-24px);
      transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    }
    #story-banner.visible {
      opacity: 1;
      transform: translateY(0);
    }
    #white-fade {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #ffffff;
      opacity: 0;
      pointer-events: none;
      z-index: 50;
      transition: opacity 1.2s ease-in-out;
    }
    #black-fade {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #000000;
      opacity: 0;
      pointer-events: none;
      z-index: 55;
      transition: opacity 0.6s ease-in-out;
    }
    #closing-card {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(18, 24, 20, 0.92);
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #f7faf0;
      z-index: 95;
      pointer-events: auto;
      text-align: center;
      padding: 30px;
    }
    #closing-card h2 {
      font-size: 38px;
      color: #ffe685;
      letter-spacing: 3px;
      font-family: Georgia, 'Times New Roman', serif;
      margin-bottom: 24px;
      text-shadow: 0 3px 10px rgba(0,0,0,0.85);
    }
    #closing-log {
      max-width: 650px;
      width: 90%;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(220, 235, 215, 0.25);
      border-radius: 10px;
      padding: 18px 24px;
      margin-bottom: 26px;
      text-align: left;
      font-size: 15px;
      line-height: 1.85;
      box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    }
    .log-entry {
      display: flex;
      justify-content: space-between;
      border-bottom: 1px dashed rgba(255,255,255,0.15);
      padding: 4px 0;
    }
    .log-entry:last-child {
      border-bottom: none;
    }
    .log-title {
      color: #e8efe2;
    }
    .log-time {
      color: #ffd875;
      font-family: monospace;
      font-size: 16px;
      font-weight: 700;
      margin-left: 16px;
    }
    #closing-card .rain-stopped {
      font-size: 21px;
      color: #dbe8d8;
      font-style: italic;
      margin-bottom: 24px;
    }
    #closing-card .close-hint {
      font-size: 14px;
      color: #9cb09e;
    }
    #ready-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at center, rgba(30, 42, 38, 0.90) 0%, rgba(12, 18, 16, 0.98) 100%);
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: #f7faf0;
      z-index: 100;
      pointer-events: auto;
      text-align: center;
      padding: 20px;
    }
    #ready-overlay h1 {
      font-size: 54px;
      color: #ffe685;
      text-shadow: 0 4px 14px rgba(0,0,0,0.85);
      margin-bottom: 12px;
      letter-spacing: 2px;
      font-family: Georgia, 'Times New Roman', serif;
    }
    #ready-overlay .premise {
      font-size: 21px;
      color: #dbe4d5;
      font-style: italic;
      margin-bottom: 34px;
      text-shadow: 0 2px 6px rgba(0,0,0,0.7);
    }
    #ready-overlay .controls-card {
      background: rgba(255, 255, 255, 0.08);
      padding: 22px 36px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.22);
      font-size: 16px;
      line-height: 1.85;
      margin-bottom: 38px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }
    #ready-overlay .start-btn {
      font-size: 22px;
      font-weight: 700;
      color: #1e331e;
      background: #ffdf70;
      padding: 15px 48px;
      border-radius: 32px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.45);
      animation: pulse 2s infinite;
      cursor: pointer;
      border: none;
      outline: none;
    }
    @keyframes pulse {
      0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 223, 112, 0.7); }
      70% { transform: scale(1.04); box-shadow: 0 0 0 16px rgba(255, 223, 112, 0); }
      100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 223, 112, 0); }
    }
  </style>
  <script src="./assets/_shared/three/build/three.min.js"></script>
</head>
<body>
  <canvas id="game-canvas"></canvas>

  <div id="white-fade"></div>
  <div id="black-fade"></div>

  <div id="ui-container">
    <div id="hud-zone" class="hud-box">Waking Meadow</div>
    <div id="hud-memories" class="hud-box">Memories: 0/6</div>
    <div id="hud-strikes" class="hud-box">Strikes: 0</div>
    <div id="hud-companion-prompt" class="hud-box">Press T — Bola: Wait</div>
    <div id="hud-rest-prompt" class="hud-box">Press E — Rest</div>
    <div id="hud-controls-hint" class="hud-box">WASD: Walk | T: Bola Wait/Follow | E: Interact | R: Reset</div>
    <div id="story-banner"></div>
  </div>

  <div id="closing-card">
    <h2>NIULAI OPENS HIS EYES</h2>
    <div id="closing-log"></div>
    <div class="rain-stopped">The rain has stopped.</div>
    <div class="close-hint">Press R to restart journey</div>
  </div>

  <div id="ready-overlay">
    <h1>Niulai: The Long Dream</h1>
    <div class="premise">A newborn calf dreams of grasslands.</div>
    <div class="controls-card">
      <p><strong>W / A / S / D</strong> &mdash; Walk around</p>
      <p><strong>T</strong> &mdash; Toggle companion Bola: Wait / Follow</p>
      <p><strong>E</strong> &mdash; Rest at story rocks</p>
      <p><strong>R</strong> &mdash; Reset journey to meadow spawn</p>
      <p style="margin-top: 8px; color: #cedac8;">In the cold waking rain, seek the flat stone beside the perched lark.</p>
    </div>
    <button class="start-btn" id="start-btn">Press Enter to Start</button>
  </div>
"""
