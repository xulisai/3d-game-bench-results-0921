import re

with open('index.html', 'r') as f:
    text = f.read()

# 1. Update kd-count-display HTML to include mash meter and prompts
old_kd_display = '''  <!-- Knockdown 8s Count Overlay -->
  <div id="kd-count-display">
    <div id="kd-downed-text" class="kd-text">REFEREE COUNT</div>
    <div id="kd-number-display" class="kd-number">8</div>
  </div>'''

new_kd_display = '''  <!-- Knockdown 10s Mash-to-Rise Count Overlay -->
  <div id="kd-count-display">
    <div id="kd-downed-text" class="kd-text">REFEREE COUNT</div>
    <div id="kd-number-display" class="kd-number">10</div>
    <div id="kd-mash-container" style="margin-top: 10px;">
      <div id="kd-mash-label" style="font-size: 13px; font-weight: 800; color: #ffd700; letter-spacing: 1px;">MASH SPACE TO RISE!</div>
      <div id="kd-mash-count" style="font-size: 20px; font-weight: 900; color: #ffffff; margin: 4px 0;">PRESSES: 0 / 8</div>
      <div style="width: 100%; height: 10px; background: rgba(0,0,0,0.6); border-radius: 5px; overflow: hidden; border: 1px solid rgba(255,255,255,0.3); margin-top: 4px;">
        <div id="kd-mash-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, #ffd700, #ff8800); transition: width 0.05s linear;"></div>
      </div>
    </div>
  </div>'''

assert old_kd_display in text, "old_kd_display not found"
text = text.replace(old_kd_display, new_kd_display, 1)

# 2. Update ready-screen HTML to remove opponent selection UI completely and show fixed challenge
old_ready_screen = '''<!-- Main Menu Overlay (Opponent Select) -->
  <div id="ready-screen" class="screen-overlay">
    <div class="title-box">
      <h1>CANVAS KINGS</h1>
      <div class="subtitle">Championship 3D Boxing — 10-Point-Must System</div>

      <!-- Opponent Selection -->
      <div class="opponent-select-container">
        <div class="opponent-select-title">SELECT OPPONENT (Press 1 / 2 or Arrow Keys)</div>
        <div class="opponents-grid">
          <div id="card-bull" class="opp-card bull selected" onclick="window.__selectOpponent('bull')">
            <div class="opp-card-name">BRONZE BULL</div>
            <div class="opp-card-desc">Pressure fighter. Heavy power hooks and crosses. Relentless forward march.</div>
            <div class="opp-card-tag">Tendency Table A • Key [1]</div>
          </div>
          <div id="card-surgeon" class="opp-card surgeon" onclick="window.__selectOpponent('surgeon')">
            <div class="opp-card-name">THE SURGEON</div>
            <div class="opp-card-desc">Taller, lean counter-puncher. Slips punches and delivers devastating counters.</div>
            <div class="opp-card-tag">Tendency Table B • Key [2]</div>
          </div>
        </div>
      </div>

      <div class="controls-grid">
        <div class="ctrl-item"><span class="key-badge">W</span> Step In (2.0 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">S</span> Step Out (1.8 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">A</span> Orbit Left (1.6 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">D</span> Orbit Right (1.6 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">J</span> Jab (1.7–2.4 m, 4 Dmg, 6 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">K</span> Cross (1.2–2.0 m, 8 Dmg, 10 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">L</span> Hook (0.6–1.4 m, 10 Dmg, 14 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">S+L</span> Body Hook (Hook + Hold S -> Body Hit)</div>
        <div class="ctrl-item"><span class="key-badge">U</span> Uppercut (0.6–1.2 m, 12 Dmg, 12 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">F</span> Guard (Hold: Reduce Dmg, −2 Stm/hit)</div>
        <div class="ctrl-item"><span class="key-badge">Space</span> Slip (0.35s Sway, 0.20s Invuln, 8 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">Enter</span> Start Match with Selected Opponent</div>
        <div class="ctrl-item"><span class="key-badge">R</span> Return to Main Menu</div>
      </div>

      <div style="font-size: 11px; color: #a0aec0; margin-bottom: 12px;">
        Knockdowns: 8s Count (HP Restored to 20) • 3 Knockdowns = TKO • 3-Judge 10-Point-Must Judging
      </div>
      <div class="prompt-banner">Press Enter to Fight</div>
    </div>
  </div>'''

new_ready_screen = '''<!-- Main Menu Overlay (Fixed Challenge Campaign) -->
  <div id="ready-screen" class="screen-overlay">
    <div class="title-box">
      <h1>CANVAS KINGS</h1>
      <div class="subtitle">Championship 3D Boxing — Fixed Challenge Campaign</div>

      <!-- Current Challenge Banner -->
      <div style="background: rgba(20, 26, 40, 0.85); border: 1px solid rgba(255, 215, 0, 0.4); border-radius: 10px; padding: 12px 20px; margin-bottom: 18px; text-align: center;">
        <div style="font-size: 11px; font-weight: 800; color: #ffd700; letter-spacing: 2px; text-transform: uppercase;">CURRENT CHALLENGE</div>
        <div id="menu-current-opp" style="font-size: 22px; font-weight: 900; color: #ffffff; letter-spacing: 1px; margin: 4px 0;">STAGE 1: BRONZE BULL</div>
        <div id="menu-opp-desc" style="font-size: 11px; color: #94a3b8;">Stage 1: Bronze Bull (Pressure Fighter) → Stage 2: The Surgeon (Counter-Puncher)</div>
      </div>

      <div class="controls-grid">
        <div class="ctrl-item"><span class="key-badge">W</span> Step In (2.0 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">S</span> Step Out (1.8 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">A</span> Orbit Left (1.6 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">D</span> Orbit Right (1.6 m/s)</div>
        <div class="ctrl-item"><span class="key-badge">J</span> Jab (1.7–2.4 m, 4 Dmg, 6 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">K</span> Cross (1.2–2.0 m, 8 Dmg, 10 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">L</span> Hook (0.6–1.4 m, 10 Dmg, 14 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">S+L</span> Body Hook (Hook + Hold S -> Body Hit)</div>
        <div class="ctrl-item"><span class="key-badge">U</span> Uppercut (0.6–1.2 m, 12 Dmg, 12 Stm)</div>
        <div class="ctrl-item"><span class="key-badge">F</span> Guard (Hold: Reduce Dmg, −2 Stm/hit)</div>
        <div class="ctrl-item"><span class="key-badge">Space</span> Slip / Mash Space to Rise when Downed</div>
        <div class="ctrl-item"><span class="key-badge">Enter</span> Start Match / Next Challenge / Rematch</div>
        <div class="ctrl-item"><span class="key-badge">R</span> Return to Main Menu</div>
      </div>

      <div style="font-size: 11px; color: #a0aec0; margin-bottom: 12px;">
        10s Mash-to-Rise Count • −10 Max Stamina per Knockdown • 3 Knockdowns = TKO • 3-Judge 10-Point-Must
      </div>
      <div id="menu-prompt-text" class="prompt-banner">Press Enter to Fight</div>
    </div>
  </div>'''

assert old_ready_screen in text, "old_ready_screen not found"
text = text.replace(old_ready_screen, new_ready_screen, 1)

# 3. Update game-over screen banner prompt
old_game_over_prompt = '<div class="prompt-banner">Press Enter to Return to Menu</div>'
new_game_over_prompt = '<div id="game-over-prompt-text" class="prompt-banner">Press Enter to Continue</div>'
assert old_game_over_prompt in text, "old_game_over_prompt not found"
text = text.replace(old_game_over_prompt, new_game_over_prompt, 1)

# 4. Remove opponent-selection CSS if any
# Let's inspect opponent selection css
text = re.sub(r'\.opponent-select-container\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opponent-select-title\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opponents-grid\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opp-card\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opp-card:hover\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opp-card\.selected\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opp-card-name\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opp-card-desc\s*\{[^}]*\}', '', text)
text = re.sub(r'\.opp-card-tag\s*\{[^}]*\}', '', text)

# 5. Update C7 State variables:
state_vars_old = '''    // C5: Opponent Select ('bull' or 'surgeon')
    let cornerChoiceMade = null; // null, 'water', or 'ice'
    let cornerChoiceThisBreak = null;

    let selectedOpponent = 'bull'; // 'bull' or 'surgeon'
    let opponentName = 'BRONZE BULL';
    let tendencyTable = 'Table A';

    function setOpponentSelection(oppKey) {
      selectedOpponent = oppKey;
      if (selectedOpponent === 'bull') {
        opponentName = 'BRONZE BULL';
        tendencyTable = 'Table A';
        document.getElementById('card-bull').classList.add('selected');
        document.getElementById('card-surgeon').classList.remove('selected');
        document.getElementById('opponent-hud-name').textContent = 'BRONZE BULL';
        document.getElementById('opponent-hud-name').className = 'bull-name';
        if (bullMeshGroup && surgeonMeshGroup) {
          bullMeshGroup.visible = true;
          surgeonMeshGroup.visible = false;
        }
      } else {
        opponentName = 'THE SURGEON';
        tendencyTable = 'Table B';
        document.getElementById('card-surgeon').classList.add('selected');
        document.getElementById('card-bull').classList.remove('selected');
        document.getElementById('opponent-hud-name').textContent = 'THE SURGEON';
        document.getElementById('opponent-hud-name').style.color = '#2ecc71';
        if (bullMeshGroup && surgeonMeshGroup) {
          bullMeshGroup.visible = false;
          surgeonMeshGroup.visible = true;
        }
      }
    }
    window.__selectOpponent = setOpponentSelection;'''

state_vars_new = '''    // C6 Corner Choice Tracking
    let cornerChoiceMade = null; // null, 'water', or 'ice'
    let cornerChoiceThisBreak = null;

    // C7: Fixed Challenge Order: BRONZE BULL -> THE SURGEON
    let campaignIndex = 0; // 0: 'bull', 1: 'surgeon'
    let selectedOpponent = 'bull';
    let opponentName = 'BRONZE BULL';
    let tendencyTable = 'Table A';

    // C7: Mash-to-Rise variables
    let mashRequired = 0;
    let mashProgress = 0;
    let opponentMashAccumulator = 0;
    const OPPONENT_MASH_RATE = 1.35; // presses per second, deterministic fixed rate

    function applyOpponent(oppKey) {
      selectedOpponent = oppKey;
      if (selectedOpponent === 'bull') {
        opponentName = 'BRONZE BULL';
        tendencyTable = 'Table A';
        const oppHud = document.getElementById('opponent-hud-name');
        if (oppHud) {
          oppHud.textContent = 'BRONZE BULL';
          oppHud.className = 'bull-name';
          oppHud.style.color = '#e67e22';
        }
        if (bullMeshGroup && surgeonMeshGroup) {
          bullMeshGroup.visible = true;
          surgeonMeshGroup.visible = false;
        }
      } else {
        opponentName = 'THE SURGEON';
        tendencyTable = 'Table B';
        const oppHud = document.getElementById('opponent-hud-name');
        if (oppHud) {
          oppHud.textContent = 'THE SURGEON';
          oppHud.className = 'bull-name';
          oppHud.style.color = '#2ecc71';
        }
        if (bullMeshGroup && surgeonMeshGroup) {
          bullMeshGroup.visible = false;
          surgeonMeshGroup.visible = true;
        }
      }
      updateMenuDisplay();
    }

    function updateMenuDisplay() {
      const titleEl = document.getElementById('menu-current-opp');
      const descEl = document.getElementById('menu-opp-desc');
      if (titleEl) {
        titleEl.textContent = (campaignIndex === 0) ? 'STAGE 1: BRONZE BULL' : 'STAGE 2: THE SURGEON';
      }
      if (descEl) {
        descEl.textContent = (campaignIndex === 0) ?
          'Stage 1: Bronze Bull (Pressure Fighter • Table A) → Next: The Surgeon' :
          'Stage 2: The Surgeon (Counter-Puncher • Table B) • Final Stage';
      }
    }'''

assert state_vars_old in text, "state_vars_old not found"
text = text.replace(state_vars_old, state_vars_new, 1)

# 6. Update createFighter to add maxStamina: 100
create_fighter_old = '''    function createFighter(initialPos) {
      return {
        pos: initialPos.clone(),
        hp: 100,
        stamina: 100,'''

create_fighter_new = '''    function createFighter(initialPos) {
      return {
        pos: initialPos.clone(),
        hp: 100,
        stamina: 100,
        maxStamina: 100,'''

assert create_fighter_old in text, "create_fighter_old not found"
text = text.replace(create_fighter_old, create_fighter_new, 1)

# 7. Update resetFighter to reset maxStamina: 100
reset_fighter_old = '''    function resetFighter(f, initialPos) {
      f.pos.copy(initialPos);
      f.hp = 100;
      f.stamina = 100;'''

reset_fighter_new = '''    function resetFighter(f, initialPos) {
      f.pos.copy(initialPos);
      f.hp = 100;
      f.maxStamina = 100;
      f.stamina = 100;'''

assert reset_fighter_old in text, "reset_fighter_old not found"
text = text.replace(reset_fighter_old, reset_fighter_new, 1)

# 8. Update resetMatch to reset mash state
reset_match_old = '''      simTime = 0;
      cornerChoiceMade = null;
      cornerChoiceThisBreak = null;

      resetFighter(player, new THREE.Vector2(0, 1.8));'''

reset_match_new = '''      simTime = 0;
      cornerChoiceMade = null;
      cornerChoiceThisBreak = null;
      mashRequired = 0;
      mashProgress = 0;
      opponentMashAccumulator = 0;

      applyOpponent(campaignIndex === 0 ? 'bull' : 'surgeon');

      resetFighter(player, new THREE.Vector2(0, 1.8));'''

assert reset_match_old in text, "reset_match_old not found"
text = text.replace(reset_match_old, reset_match_new, 1)

# 9. Update triggerKnockdown for C7 Mash-to-rise and -10 max stamina
knockdown_old = '''    // --- KNOCKDOWN TRIGGER (REPLACES INSTANT KO) ---
    function triggerKnockdown(downed, attacker, isPlayerDowned) {
      downed.hp = 0;
      downed.knockdownCount++;
      downed.roundKnockdowns[currentRound - 1]++;
      downed.action = 'ko';
      downed.isGuarding = false;
      downed.isSlipping = false;
      downed.isInvulnerable = false;
      downed.isStaggered = false;
      downed.staggerTimer = 0;
      downed.punchType = null;
      downed.punchTimer = 0;

      downedFighter = isPlayerDowned ? 'player' : 'opponent';
      playSound('ko_thud');

      if (downed.knockdownCount >= 3) {
        matchEndReason = 'TKO';
        matchWinner = isPlayerDowned ? 'opponent' : 'player';
        setPhase('game_over');
        return;
      }

      knockdownTimer = 8.0;
      setPhase('knockdown');
    }'''

knockdown_new = '''    // --- KNOCKDOWN TRIGGER (C7 MASH-TO-RISE & MAX STAMINA PENALTY) ---
    function triggerKnockdown(downed, attacker, isPlayerDowned) {
      downed.hp = 0;
      const priorKnockdowns = downed.knockdownCount; // knockdowns already suffered this match before this one
      downed.knockdownCount++;
      downed.roundKnockdowns[currentRound - 1]++;

      // C7: Every knockdown permanently lowers max stamina by -10 for rest of match
      downed.maxStamina = Math.max(0, downed.maxStamina - 10);
      downed.stamina = Math.min(downed.stamina, downed.maxStamina);

      downed.action = 'ko';
      downed.isGuarding = false;
      downed.isSlipping = false;
      downed.isInvulnerable = false;
      downed.isStaggered = false;
      downed.staggerTimer = 0;
      downed.punchType = null;
      downed.punchTimer = 0;

      downedFighter = isPlayerDowned ? 'player' : 'opponent';
      playSound('ko_thud');

      // 3-knockdown TKO rule is unchanged
      if (downed.knockdownCount >= 3) {
        matchEndReason = 'TKO';
        matchWinner = isPlayerDowned ? 'opponent' : 'player';
        setPhase('game_over');
        return;
      }

      // C7 Mash-to-Rise: 10s count, 8 + 2 * priorKnockdowns
      knockdownTimer = 10.0;
      mashRequired = 8 + 2 * priorKnockdowns;
      mashProgress = 0;
      opponentMashAccumulator = 0;

      setPhase('knockdown');
    }'''

assert knockdown_old in text, "knockdown_old not found"
text = text.replace(knockdown_old, knockdown_new, 1)

# 10. Update setPhase for C7 knockdown HUD
set_phase_kd_old = '''      } else if (phase === 'knockdown') {
        kdEl.style.display = 'block';
        document.getElementById('kd-downed-text').textContent = (downedFighter === 'player' ? 'PLAYER' : opponentName) + ' IS DOWN!';
        document.getElementById('kd-number-display').textContent = '8';
      }'''

set_phase_kd_new = '''      } else if (phase === 'knockdown') {
        kdEl.style.display = 'block';
        document.getElementById('kd-downed-text').textContent = (downedFighter === 'player' ? 'PLAYER' : opponentName) + ' IS DOWN!';
        document.getElementById('kd-number-display').textContent = '10';
        updateMashUI();
      }'''

assert set_phase_kd_old in text, "set_phase_kd_old not found"
text = text.replace(set_phase_kd_old, set_phase_kd_new, 1)

# 11. Add updateMashUI and handleMashPress helper functions
mash_helpers = '''
    // --- C7 MASH-TO-RISE HELPERS ---
    function updateMashUI() {
      const kdEl = document.getElementById('kd-count-display');
      if (!kdEl || phase !== 'knockdown') return;

      const numEl = document.getElementById('kd-number-display');
      const countSeconds = Math.max(1, Math.ceil(knockdownTimer));
      if (numEl) numEl.textContent = countSeconds;

      const mashLabel = document.getElementById('kd-mash-label');
      const mashCount = document.getElementById('kd-mash-count');
      const mashBar = document.getElementById('kd-mash-bar');

      if (downedFighter === 'player') {
        if (mashLabel) mashLabel.textContent = 'MASH SPACE TO RISE!';
      } else {
        if (mashLabel) mashLabel.textContent = opponentName + ' IS STRUGGLING TO RISE...';
      }

      if (mashCount) {
        mashCount.textContent = 'PROGRESS: ' + mashProgress + ' / ' + mashRequired;
      }
      if (mashBar) {
        const pct = Math.min(100, Math.round((mashProgress / Math.max(1, mashRequired)) * 100));
        mashBar.style.width = pct + '%';
      }
    }

    function handlePlayerMash() {
      if (phase !== 'knockdown' || downedFighter !== 'player') return;
      mashProgress++;
      playSound('block');
      updateMashUI();

      if (mashProgress >= mashRequired) {
        // Player successfully rises
        player.hp = 20;
        player.action = 'idle';
        downedFighter = null;
        knockdownTimer = 0;
        mashProgress = 0;
        mashRequired = 0;
        setPhase('round');
        showBanner('FIGHT!', 1500);
      }
    }
'''

# Put mash_helpers before setPhase
text = text.replace('    function setPhase(newPhase) {', mash_helpers + '\n    function setPhase(newPhase) {', 1)

# 12. Update updateStamina to respect fighter.maxStamina
stamina_cap_old = 'fighter.stamina = Math.min(100.0, fighter.stamina + rate * dt);'
stamina_cap_new = 'fighter.stamina = Math.min(fighter.maxStamina, fighter.stamina + rate * dt);'
assert stamina_cap_old in text, "stamina_cap_old not found"
text = text.replace(stamina_cap_old, stamina_cap_new, 1)

# Also check corner break water stamina addition:
water_cap_old = 'player.stamina = Math.min(100.0, player.stamina + 40.0);'
water_cap_new = 'player.stamina = Math.min(player.maxStamina, player.stamina + 40.0);'
assert water_cap_old in text, "water_cap_old not found"
text = text.replace(water_cap_old, water_cap_new, 1)

# 13. Update gameUpdate's knockdown block to handle 10s count, opponent mash rate, and KO on failure
kd_update_old = '''      if (phase === 'knockdown') {
        knockdownTimer -= dt;
        const countSeconds = Math.max(1, Math.ceil(knockdownTimer));
        document.getElementById('kd-number-display').textContent = countSeconds;

        if (knockdownTimer <= 0) {
          if (downedFighter === 'player') {
            player.hp = 20;
            player.action = 'idle';
          } else {
            opponent.hp = 20;
            opponent.action = 'idle';
          }
          downedFighter = null;
          knockdownTimer = 0;
          setPhase('round');
          showBanner('FIGHT!', 1500);
        }
        return;
      }'''

kd_update_new = '''      if (phase === 'knockdown') {
        knockdownTimer -= dt;

        // If opponent is downed, simulate deterministic fixed press rate
        if (downedFighter === 'opponent') {
          opponentMashAccumulator += OPPONENT_MASH_RATE * dt;
          while (opponentMashAccumulator >= 1.0) {
            opponentMashAccumulator -= 1.0;
            mashProgress++;
            if (mashProgress >= mashRequired) {
              break;
            }
          }
          if (mashProgress >= mashRequired) {
            // Opponent rises
            opponent.hp = 20;
            opponent.action = 'idle';
            downedFighter = null;
            knockdownTimer = 0;
            mashProgress = 0;
            mashRequired = 0;
            setPhase('round');
            showBanner('FIGHT!', 1500);
            return;
          }
        }

        updateMashUI();

        // Failing the count ends the match immediately as a KO loss for the downed fighter
        if (knockdownTimer <= 0) {
          knockdownTimer = 0;
          matchEndReason = 'KO';
          matchWinner = (downedFighter === 'player') ? 'opponent' : 'player';
          downedFighter = null;
          setPhase('game_over');
          return;
        }
        return;
      }'''

assert kd_update_old in text, "kd_update_old not found"
text = text.replace(kd_update_old, kd_update_new, 1)

# 14. Update keyboard listeners:
# - remove Digit1/2 opponent selection
# - Space in knockdown mashes
# - Enter in game_over advances campaign or rematches
key_listeners_old = '''      if (phase === 'ready') {
        if (e.code === 'Digit1' || e.code === 'Numpad1' || e.code === 'ArrowLeft') {
          setOpponentSelection('bull');
        } else if (e.code === 'Digit2' || e.code === 'Numpad2' || e.code === 'ArrowRight') {
          setOpponentSelection('surgeon');
        }
      } else if (phase === 'corner_break') {
        if (e.code === 'Digit1' || e.code === 'Numpad1') {
          takeCornerAction('water');
        } else if (e.code === 'Digit2' || e.code === 'Numpad2') {
          takeCornerAction('ice');
        }
      }

      if (e.code === 'Enter') {
        if (phase === 'ready') {
          resetMatch();
          setPhase('round');
        } else if (phase === 'game_over') {
          resetMatch();
          setPhase('ready');
        }
      }

      if (e.code === 'KeyR') {
        resetMatch();
        setPhase('ready');
      }

      if (phase === 'round') {
        if (e.code === 'KeyJ') {
          triggerPlayerPunch('jab');
        } else if (e.code === 'KeyK') {
          triggerPlayerPunch('cross');
        } else if (e.code === 'KeyL') {
          triggerPlayerPunch('hook');
        } else if (e.code === 'KeyU') {
          triggerPlayerPunch('uppercut');
        } else if (e.code === 'Space') {
          triggerSlip(player);
        }
      }'''

key_listeners_new = '''      if (phase === 'corner_break') {
        if (e.code === 'Digit1' || e.code === 'Numpad1') {
          takeCornerAction('water');
        } else if (e.code === 'Digit2' || e.code === 'Numpad2') {
          takeCornerAction('ice');
        }
      } else if (phase === 'knockdown') {
        if (e.code === 'Space') {
          handlePlayerMash();
        }
      }

      if (e.code === 'Enter') {
        if (phase === 'ready') {
          resetMatch();
          setPhase('round');
        } else if (phase === 'game_over') {
          // C7 Progression: Beating current opponent advances to next; losing offers rematch
          if (matchWinner === 'player') {
            if (campaignIndex === 0) {
              campaignIndex = 1; // Advance to The Surgeon
            } else {
              campaignIndex = 0; // Completed campaign, loop to stage 1
            }
          }
          // If losing, campaignIndex stays the same (rematch against same opponent)
          resetMatch();
          setPhase('round');
        }
      }

      if (e.code === 'KeyR') {
        resetMatch();
        setPhase('ready');
      }

      if (phase === 'round') {
        if (e.code === 'KeyJ') {
          triggerPlayerPunch('jab');
        } else if (e.code === 'KeyK') {
          triggerPlayerPunch('cross');
        } else if (e.code === 'KeyL') {
          triggerPlayerPunch('hook');
        } else if (e.code === 'KeyU') {
          triggerPlayerPunch('uppercut');
        } else if (e.code === 'Space') {
          triggerSlip(player);
        }
      }'''

assert key_listeners_old in text, "key_listeners_old not found"
text = text.replace(key_listeners_old, key_listeners_new, 1)

# 15. Update populateScorecards to handle matchEndReason === 'KO' and update prompt banner
populate_scorecards_old = '''    if (matchEndReason === 'TKO') {
      resTitle.textContent = matchWinner.toUpperCase() + ' WINS';
      resReason.textContent = 'TECHNICAL KNOCKOUT (3 KNOCKDOWNS)';
    } else {'''

populate_scorecards_new = '''    if (matchEndReason === 'KO') {
      resTitle.textContent = (matchWinner === 'player' ? 'PLAYER WINS' : opponentName + ' WINS');
      resReason.textContent = 'KNOCKOUT (COUNT OUT)';
    } else if (matchEndReason === 'TKO') {
      resTitle.textContent = (matchWinner === 'player' ? 'PLAYER WINS' : opponentName + ' WINS');
      resReason.textContent = 'TECHNICAL KNOCKOUT (3 KNOCKDOWNS)';
    } else {'''

assert populate_scorecards_old in text, "populate_scorecards_old not found"
text = text.replace(populate_scorecards_old, populate_scorecards_new, 1)

prompt_update_old = '''      totalTr.innerHTML = `
        <td>TOTAL</td>
        <td>${judges[0].totals.player} – ${judges[0].totals.bull}</td>
        <td>${judges[1].totals.player} – ${judges[1].totals.bull}</td>
        <td>${judges[2].totals.player} – ${judges[2].totals.bull}</td>
      `;
      tbody.appendChild(totalTr);
    }'''

prompt_update_new = '''      totalTr.innerHTML = `
        <td>TOTAL</td>
        <td>${judges[0].totals.player} – ${judges[0].totals.bull}</td>
        <td>${judges[1].totals.player} – ${judges[1].totals.bull}</td>
        <td>${judges[2].totals.player} – ${judges[2].totals.bull}</td>
      `;
      tbody.appendChild(totalTr);

      const goPrompt = document.getElementById('game-over-prompt-text');
      if (goPrompt) {
        if (matchWinner === 'player') {
          goPrompt.textContent = (campaignIndex === 0) ? 'Press Enter for Next Challenge (The Surgeon)' : 'Press Enter to Restart Campaign';
        } else {
          goPrompt.textContent = 'Press Enter for Rematch against ' + opponentName;
        }
      }
    }'''

assert prompt_update_old in text, "prompt_update_old not found"
text = text.replace(prompt_update_old, prompt_update_new, 1)

# 16. Update updateHUD to show max stamina and KD clock
hud_stm_old = '''      document.getElementById('player-stm-bar').style.width = pStm + '%';
      document.getElementById('player-stm-text').textContent = Math.round(pStm) + ' / 100';'''

hud_stm_new = '''      const pMaxStm = player.maxStamina || 100;
      document.getElementById('player-stm-bar').style.width = (pStm / pMaxStm * 100) + '%';
      document.getElementById('player-stm-text').textContent = Math.round(pStm) + ' / ' + pMaxStm;'''

assert hud_stm_old in text, "hud_stm_old not found"
text = text.replace(hud_stm_old, hud_stm_new, 1)

hud_bull_stm_old = '''      document.getElementById('bull-stm-bar').style.width = bStm + '%';
      document.getElementById('bull-stm-text').textContent = Math.round(bStm) + ' / 100';'''

hud_bull_stm_new = '''      const bMaxStm = opponent.maxStamina || 100;
      document.getElementById('bull-stm-bar').style.width = (bStm / bMaxStm * 100) + '%';
      document.getElementById('bull-stm-text').textContent = Math.round(bStm) + ' / ' + bMaxStm;'''

assert hud_bull_stm_old in text, "hud_bull_stm_old not found"
text = text.replace(hud_bull_stm_old, hud_bull_stm_new, 1)

# KD clock update in updateHUD
hud_kd_clock_old = '''      } else if (phase === 'knockdown') {
        document.getElementById('round-indicator').textContent = 'KNOCKDOWN COUNT';
        document.getElementById('clock-indicator').textContent = '00:' + (Math.ceil(knockdownTimer) < 10 ? '0' : '') + Math.ceil(knockdownTimer);
      }'''

hud_kd_clock_new = '''      } else if (phase === 'knockdown') {
        document.getElementById('round-indicator').textContent = 'COUNT (' + (mashProgress) + '/' + (mashRequired) + ')';
        document.getElementById('clock-indicator').textContent = '00:' + (Math.ceil(knockdownTimer) < 10 ? '0' : '') + Math.ceil(knockdownTimer);
      }'''

assert hud_kd_clock_old in text, "hud_kd_clock_old not found"
text = text.replace(hud_kd_clock_old, hud_kd_clock_new, 1)

# 17. Update updateArenaDebugState with C7 fields
arena_player_old = '''        stamina: player.stamina,
        action: player.action,'''

arena_player_new = '''        stamina: player.stamina,
        maxStamina: player.maxStamina,
        action: player.action,'''

assert arena_player_old in text, "arena_player_old not found"
text = text.replace(arena_player_old, arena_player_new, 1)

arena_opp_old = '''        stamina: opponent.stamina,
        action: opponent.action,'''

arena_opp_new = '''        stamina: opponent.stamina,
        maxStamina: opponent.maxStamina,
        action: opponent.action,'''

assert arena_opp_old in text, "arena_opp_old not found"
text = text.replace(arena_opp_old, arena_opp_new, 1)

# Add mashRequired, mashProgress, maxStaminas, etc. to stateObj
state_obj_old = '''        // Knockdowns & Judging
        knockdownTimer: knockdownTimer,
        downedFighter: downedFighter,
        playerKnockdowns: player.knockdownCount,
        bullKnockdowns: opponent.knockdownCount,'''

state_obj_new = '''        // C7 Mash-to-Rise & Max Stamina
        mashRequired: mashRequired,
        mashProgress: mashProgress,
        pressesNeeded: mashRequired,
        pressesRegistered: mashProgress,
        countClock: knockdownTimer,
        playerMaxStamina: player.maxStamina,
        bullMaxStamina: opponent.maxStamina,
        opponentMaxStamina: opponent.maxStamina,
        // Knockdowns & Judging
        knockdownTimer: knockdownTimer,
        downedFighter: downedFighter,
        playerKnockdowns: player.knockdownCount,
        bullKnockdowns: opponent.knockdownCount,'''

assert state_obj_old in text, "state_obj_old not found"
text = text.replace(state_obj_old, state_obj_new, 1)

# 18. Update initialization at the bottom of the script
init_old = '''    resetMatch();
    setOpponentSelection('bull');
    updateArenaDebugState();
    requestAnimationFrame(animate);'''

init_new = '''    applyOpponent('bull');
    resetMatch();
    updateArenaDebugState();
    requestAnimationFrame(animate);'''

assert init_old in text, "init_old not found"
text = text.replace(init_old, init_new, 1)

with open('index.html', 'w') as f:
    f.write(text)

print("Patch R7 applied successfully!")
