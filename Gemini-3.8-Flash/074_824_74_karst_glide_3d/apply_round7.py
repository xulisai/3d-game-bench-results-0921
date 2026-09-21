# apply_round7.py - Updates index.html with Round 7 Checkpoint Respawns and Reckoning panel

with open("index.html", "r") as f:
    content = f.read()

# 1. Add CSS styles
css_additions = r'''
    /* Round 7: Respawn Warning & Reckoning Styles */
    #respawn-warning {
      position: absolute;
      top: 12%;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(220, 50, 20, 0.92);
      color: #ffffff;
      padding: 10px 26px;
      border-radius: 6px;
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 2px;
      border: 1px solid #ffaaaa;
      box-shadow: 0 0 25px rgba(255, 60, 30, 0.75);
      display: none;
      z-index: 25;
      animation: blink 0.15s infinite alternate;
    }

    #reckoning-screen {
      display: none;
    }

    .rating-badge {
      font-size: 72px;
      font-weight: 900;
      letter-spacing: 4px;
      line-height: 1.0;
      margin: 6px 0;
      display: inline-block;
    }
    .rating-S { color: #ffd700; text-shadow: 0 0 35px rgba(255, 215, 0, 0.9); }
    .rating-A { color: #38ef7d; text-shadow: 0 0 30px rgba(56, 239, 125, 0.9); }
    .rating-B { color: #ffaa33; text-shadow: 0 0 25px rgba(255, 170, 50, 0.8); }
    .rating-C { color: #5bc0be; text-shadow: 0 0 20px rgba(91, 192, 190, 0.7); }
'''

content = content.replace("  </style>", css_additions + "\n  </style>", 1)

# 2. Add #respawn-warning to HUD
respawn_html = '<div id="respawn-warning">RESPAWN &bull; CONTROLS FROZEN (3.0s) &bull; -150 PTS</div>'
content = content.replace('<div id="stall-warning">STALL WARNING</div>', respawn_html + '\n    <div id="stall-warning">STALL WARNING</div>', 1)

# 3. Add Crashes row to #result-banner table
old_table_body = r'''          <tr>
            <td>Proximity (cap 300)</td>
            <td class="score-val score-val-bonus" id="sheet-you-prox">+0.0</td>
            <td class="score-val score-val-bonus" id="sheet-kes-prox">+0.0</td>
          </tr>'''

new_table_body = r'''          <tr>
            <td>Proximity (cap 300)</td>
            <td class="score-val score-val-bonus" id="sheet-you-prox">+0.0</td>
            <td class="score-val score-val-bonus" id="sheet-kes-prox">+0.0</td>
          </tr>
          <tr>
            <td>Crashes (-150/ea)</td>
            <td class="score-val" id="sheet-you-crashes">0 (+0)</td>
            <td class="score-val" id="sheet-kes-crashes">0 (+0)</td>
          </tr>'''

content = content.replace(old_table_body, new_table_body, 1)

# 4. Update Podium button text
content = content.replace(
    '<div class="prompt-action" id="podium-done-btn">PRESS ENTER TO RETURN TO MENU (OR \'R\')</div>',
    '<div class="prompt-action" id="podium-done-btn">PRESS ENTER FOR FINAL RECKONING &amp; RATINGS</div>',
    1
)

# 5. Add Reckoning Screen HTML after Podium Screen
reckoning_html = r'''
  <!-- Championship Reckoning Screen -->
  <div id="reckoning-screen" class="screen-overlay">
    <div class="screen-box" style="max-width: 780px;">
      <h1>CHAMPIONSHIP RECKONING</h1>
      <div class="tagline">Official Season Recap &bull; Course Breakdown &bull; Final Rating</div>

      <div style="margin: 10px 0 16px 0;">
        <div style="font-size: 12px; letter-spacing: 2px; color: #a2bdda; text-transform: uppercase;">PLAYER RATING</div>
        <div id="reckoning-rating-badge" class="rating-badge rating-S">S</div>
        <div id="reckoning-rating-desc" style="font-size: 13.5px; font-weight: bold; color: #ffd875;">LEGENDARY &bull; SCORE &ge; 5600</div>
      </div>

      <table class="score-sheet-table" style="margin-bottom: 14px;">
        <thead>
          <tr>
            <th>COURSE</th>
            <th style="text-align: right;">TIME</th>
            <th style="text-align: right;">GATES</th>
            <th style="text-align: right;">PROX</th>
            <th style="text-align: right;">LANDING</th>
            <th style="text-align: right;">CRASHES</th>
            <th style="text-align: right;">COURSE TOTAL</th>
          </tr>
        </thead>
        <tbody id="reckoning-courses-body">
          <!-- Populated dynamically -->
        </tbody>
      </table>

      <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(20, 36, 64, 0.75); border: 1px solid rgba(255, 200, 100, 0.35); border-radius: 6px; padding: 10px 18px; margin-bottom: 14px;">
        <span style="font-size: 13px; font-weight: 700; color: #ffd875; letter-spacing: 1px;">CHAMPIONSHIP TOTAL</span>
        <span id="reckoning-champ-total" style="font-size: 20px; font-weight: 900; color: #38ef7d; font-family: monospace;">0 PTS</span>
      </div>

      <table class="standings-table" style="margin-bottom: 20px;">
        <thead>
          <tr>
            <th>RANK</th>
            <th>COMPETITOR</th>
            <th style="text-align: right;">TOTAL POINTS</th>
          </tr>
        </thead>
        <tbody id="reckoning-standings-body">
          <!-- Standings -->
        </tbody>
      </table>

      <div class="prompt-action" id="reckoning-done-btn">PRESS ENTER TO RETURN TO MENU (OR 'R')</div>
    </div>
  </div>
'''

content = content.replace('</div>\n  </div>\n\n  <script>', '</div>\n  </div>\n' + reckoning_html + '\n  <script>', 1)

# 6. JavaScript updates: state, crash respawn, reckoning logic
old_state_def = r'''    // --- PLAYER STATE ---
    let currentCourse = COURSES[0];
    const state = {
      phase: 'READY',
      run_clock: 0.0,
      x: 0, y: 620, z: 0,
      v: 18.0,
      gamma: -15.0 * Math.PI / 180,
      psi: 0.0,
      phi: 0.0,
      stall: false,
      landing_grade: null,
      vy: 0.0,
      crashTumble: 0.0,
      gates_passed: 0,
      next_gate_index: 0,
      d_rock: 999.0,
      proximity_pts: 0.0,
      scores: {
        time_pts: 0,
        gate_pts: 0,
        proximity_pts: 0,
        landing_pts: 0,
        precision_pts: 0,
        total: 0
      },
      trim: 'GLIDE',
      targetTrim: 'GLIDE',
      trimBlend: 0.0,
      current_u: 0.0,
      wind: { x: -4.0, y: 0.0, z: -4.0 },
      wind_band_index: 0,
      chosen_fork_variants: [],
      gate_timestamps: []
    };'''

new_state_def = r'''    // --- PLAYER STATE ---
    let currentCourse = COURSES[0];
    const playerCourseStats = [null, null, null];
    const state = {
      phase: 'READY',
      run_clock: 0.0,
      x: 0, y: 620, z: 0,
      v: 18.0,
      gamma: -15.0 * Math.PI / 180,
      psi: 0.0,
      phi: 0.0,
      stall: false,
      landing_grade: null,
      vy: 0.0,
      crashTumble: 0.0,
      gates_passed: 0,
      next_gate_index: 0,
      d_rock: 999.0,
      proximity_pts: 0.0,
      crash_count: 0,
      respawn_freeze: 0.0,
      respawn_point_in_use: null,
      last_passed_variant: null,
      scores: {
        time_pts: 0,
        gate_pts: 0,
        proximity_pts: 0,
        landing_pts: 0,
        precision_pts: 0,
        crash_penalty: 0,
        total: 0
      },
      trim: 'GLIDE',
      targetTrim: 'GLIDE',
      trimBlend: 0.0,
      current_u: 0.0,
      wind: { x: -4.0, y: 0.0, z: -4.0 },
      wind_band_index: 0,
      chosen_fork_variants: [],
      gate_timestamps: []
    };

    function calculatePlayerRating(totalPts) {
      if (totalPts >= 5600) return 'S';
      if (totalPts >= 5200) return 'A';
      if (totalPts >= 4600) return 'B';
      return 'C';
    }'''

content = content.replace(old_state_def, new_state_def, 1)

# 7. Extend arenaState with crash_count, remaining_respawn_freeze, respawn_point_in_use, final_rating
old_arena_export = r'''      get chosen_fork_variants() { return state.chosen_fork_variants.slice(); },
      get fork_variants() { return state.chosen_fork_variants.slice(); },'''

new_arena_export = r'''      get chosen_fork_variants() { return state.chosen_fork_variants.slice(); },
      get fork_variants() { return state.chosen_fork_variants.slice(); },
      // Round 7: Checkpoint Respawns & Ratings
      get crash_count() { return state.crash_count; },
      get crashCount() { return state.crash_count; },
      get crashes() { return state.crash_count; },
      get remaining_respawn_freeze() { return state.respawn_freeze; },
      get respawn_freeze() { return state.respawn_freeze; },
      get remainingRespawnFreeze() { return state.respawn_freeze; },
      get respawn_point_in_use() {
        if (state.respawn_point_in_use) return Object.assign({}, state.respawn_point_in_use);
        return { x: currentCourse.launch.x, y: currentCourse.launch.y, z: currentCourse.launch.z };
      },
      get respawn_point() {
        if (state.respawn_point_in_use) return Object.assign({}, state.respawn_point_in_use);
        return { x: currentCourse.launch.x, y: currentCourse.launch.y, z: currentCourse.launch.z };
      },
      get final_rating() {
        const sum = championship.course_totals.YOU.reduce((a, b) => a + b, 0);
        return calculatePlayerRating(sum);
      },
      get rating() {
        const sum = championship.course_totals.YOU.reduce((a, b) => a + b, 0);
        return calculatePlayerRating(sum);
      },
      get finalRating() {
        const sum = championship.course_totals.YOU.reduce((a, b) => a + b, 0);
        return calculatePlayerRating(sum);
      },'''

content = content.replace(old_arena_export, new_arena_export, 1)

# 8. Update checkGateCrossing to store last_passed_variant
old_fork_check = r'''        if (passedVariant) {
          state.gates_passed++;
          state.chosen_fork_variants.push(passedVariant.line);
          state.gate_timestamps[state.next_gate_index] = state.run_clock;
          state.next_gate_index++;
          playSound('gate');
          updateGateVisuals();
        }'''

new_fork_check = r'''        if (passedVariant) {
          state.gates_passed++;
          state.chosen_fork_variants.push(passedVariant.line);
          state.last_passed_variant = passedVariant;
          state.gate_timestamps[state.next_gate_index] = state.run_clock;
          state.next_gate_index++;
          playSound('gate');
          updateGateVisuals();
        }'''

content = content.replace(old_fork_check, new_fork_check, 1)

# 9. Implement Checkpoint Respawn function
trigger_respawn_code = r'''
    // --- ROUND 7: CHECKPOINT RESPAWN (replaces crash before final gate) ---
    function triggerRespawn() {
      state.crash_count++;
      state.respawn_freeze = 3.0;

      let respawnX, respawnY, respawnZ, heading;

      if (state.gates_passed === 0) {
        // Respawn back on the launch platform with +Z heading
        respawnX = currentCourse.launch.x;
        respawnY = currentCourse.launch.y;
        respawnZ = currentCourse.launch.z;
        heading = 0.0;
      } else {
        // Respawn at the center of the last passed gate
        const lastGateIdx = state.gates_passed - 1;
        const lastGate = currentCourse.gates[lastGateIdx];

        if (!lastGate.isFork) {
          respawnX = lastGate.x;
          respawnY = lastGate.y;
          respawnZ = lastGate.z;
          heading = Math.atan2(lastGate.normal.x, lastGate.normal.z);
        } else {
          const v = state.last_passed_variant || lastGate.variants[0];
          respawnX = v.x;
          respawnY = v.y;
          respawnZ = v.z;
          heading = Math.atan2(v.normal.x, v.normal.z);
        }
      }

      state.x = respawnX;
      state.y = respawnY;
      state.z = respawnZ;
      prevPos.x = respawnX;
      prevPos.y = respawnY;
      prevPos.z = respawnZ;

      state.v = 20.0;
      state.gamma = -10.0 * Math.PI / 180;
      state.psi = heading;
      state.phi = 0.0;
      state.stall = false;

      state.respawn_point_in_use = { x: respawnX, y: respawnY, z: respawnZ };

      const s_v = 2.0 + 8.0 * Math.pow(state.v / 40.0, 2);
      state.vy = state.v * Math.sin(state.gamma) - s_v + state.current_u;

      playSound('crash');
    }
'''

content = content.replace("    // --- COLLISION & TOUCHDOWN JUDGMENT ---", trigger_respawn_code + "\n    // --- COLLISION & TOUCHDOWN JUDGMENT ---", 1)

# 10. Update checkCollisions to use triggerRespawn before final gate
old_check_collisions = r'''    // --- COLLISION & TOUCHDOWN JUDGMENT ---
    function checkCollisions() {
      const pad = currentCourse.pad;
      const d_pad = Math.hypot(state.x - pad.x, state.z - pad.z);

      for (let i = 0; i < currentCourse.pillars.length; i++) {
        const p = currentCourse.pillars[i];
        if (state.y >= currentCourse.valleyFloorY && state.y <= p.topY) {
          const distToAxis = Math.hypot(state.x - p.x, state.z - p.z);
          if (distToAxis <= p.radius) {
            judgeFinalOutcome('CRASH', 'Contact with stone pillar P' + (i + 1) + '!', d_pad);
            return;
          }
        }
      }

      if (d_pad <= pad.radius) {
        if (state.y <= pad.y) {
          state.y = pad.y;
          judgeTouchdown(d_pad, true);
          return;
        }
      }

      if (state.y <= currentCourse.valleyFloorY) {
        // Outside pad contact with valley floor
        if (d_pad <= pad.radius && currentCourse.pad.y < currentCourse.valleyFloorY) {
          // Inside recessed pad cylinder on Course 2
        } else {
          state.y = currentCourse.valleyFloorY;
          judgeTouchdown(d_pad, false);
          return;
        }
      }
    }'''

new_check_collisions = r'''    // --- COLLISION & TOUCHDOWN JUDGMENT ---
    function checkCollisions() {
      const pad = currentCourse.pad;
      const d_pad = Math.hypot(state.x - pad.x, state.z - pad.z);
      const isBeforeFinalGate = (state.next_gate_index < currentCourse.gates.length);

      // 1. Pillar collision check
      for (let i = 0; i < currentCourse.pillars.length; i++) {
        const p = currentCourse.pillars[i];
        if (state.y >= currentCourse.valleyFloorY && state.y <= p.topY) {
          const distToAxis = Math.hypot(state.x - p.x, state.z - p.z);
          if (distToAxis <= p.radius) {
            if (isBeforeFinalGate) {
              triggerRespawn();
              return;
            } else {
              judgeFinalOutcome('CRASH', 'Contact with stone pillar P' + (i + 1) + '!', d_pad);
              return;
            }
          }
        }
      }

      // 2. Pad surface contact (only when final gate passed)
      if (!isBeforeFinalGate && d_pad <= pad.radius) {
        if (state.y <= pad.y) {
          state.y = pad.y;
          judgeTouchdown(d_pad, true);
          return;
        }
      }

      // 3. Valley floor contact
      if (state.y <= currentCourse.valleyFloorY) {
        if (isBeforeFinalGate) {
          triggerRespawn();
          return;
        } else {
          if (d_pad <= pad.radius && currentCourse.pad.y < currentCourse.valleyFloorY) {
            // Inside recessed pad cylinder on Course 2, continue descending to pad
          } else {
            state.y = currentCourse.valleyFloorY;
            judgeTouchdown(d_pad, false);
            return;
          }
        }
      }
    }'''

content = content.replace(old_check_collisions, new_check_collisions, 1)

# 11. Update pitch/bank controls during respawn_freeze in stepPhysics
old_step_physics_controls = r'''      // 3. Pitch control (W / S) - strictly air-relative
      if (state.stall) {
        state.gamma -= STALL_FORCE_DOWN_RATE * DT;
      } else {
        if (keys.w) state.gamma += PITCH_RATE * DT;
        if (keys.s) state.gamma -= PITCH_RATE * DT;
      }
      state.gamma = Math.max(GAMMA_MIN, Math.min(GAMMA_MAX, state.gamma));'''

new_step_physics_controls = r'''      // Freeze timer countdown
      if (state.respawn_freeze > 0) {
        state.respawn_freeze = Math.max(0.0, state.respawn_freeze - DT);
      }

      // 3. Pitch control (W / S) - frozen during respawn_freeze
      if (state.stall) {
        state.gamma -= STALL_FORCE_DOWN_RATE * DT;
      } else if (state.respawn_freeze <= 0) {
        if (keys.w) state.gamma += PITCH_RATE * DT;
        if (keys.s) state.gamma -= PITCH_RATE * DT;
      }
      state.gamma = Math.max(GAMMA_MIN, Math.min(GAMMA_MAX, state.gamma));'''

content = content.replace(old_step_physics_controls, new_step_physics_controls, 1)

old_step_physics_bank = r'''      // 7. Bank and turn - strictly air-relative
      if (keys.d) {
        state.phi += BANK_DRIVE_RATE * DT;
      } else if (keys.a) {
        state.phi -= BANK_DRIVE_RATE * DT;
      } else {
        if (state.phi > 0) {
          state.phi = Math.max(0, state.phi - BANK_SPRING_RATE * DT);
        } else if (state.phi < 0) {
          state.phi = Math.min(0, state.phi + BANK_SPRING_RATE * DT);
        }
      }
      state.phi = Math.max(-BANK_MAX, Math.min(BANK_MAX, state.phi));'''

new_step_physics_bank = r'''      // 7. Bank and turn - frozen during respawn_freeze
      if (state.respawn_freeze <= 0) {
        if (keys.d) {
          state.phi += BANK_DRIVE_RATE * DT;
        } else if (keys.a) {
          state.phi -= BANK_DRIVE_RATE * DT;
        } else {
          if (state.phi > 0) {
            state.phi = Math.max(0, state.phi - BANK_SPRING_RATE * DT);
          } else if (state.phi < 0) {
            state.phi = Math.min(0, state.phi + BANK_SPRING_RATE * DT);
          }
        }
      } else {
        if (state.phi > 0) {
          state.phi = Math.max(0, state.phi - BANK_SPRING_RATE * DT);
        } else if (state.phi < 0) {
          state.phi = Math.min(0, state.phi + BANK_SPRING_RATE * DT);
        }
      }
      state.phi = Math.max(-BANK_MAX, Math.min(BANK_MAX, state.phi));'''

content = content.replace(old_step_physics_bank, new_step_physics_bank, 1)

# 12. Update judgeFinalOutcome with crash penalty and record course stats
old_outcome_total = r'''      const total = timePts + gatePts + proxPts + landingPts + precisionPts;

      state.scores.time_pts = timePts;
      state.scores.gate_pts = gatePts;
      state.scores.proximity_pts = proxPts;
      state.scores.landing_pts = landingPts;
      state.scores.precision_pts = precisionPts;
      state.scores.total = total;'''

new_outcome_total = r'''      const crashPenalty = -150 * state.crash_count;
      const total = timePts + gatePts + proxPts + landingPts + precisionPts + crashPenalty;

      state.scores.time_pts = timePts;
      state.scores.gate_pts = gatePts;
      state.scores.proximity_pts = proxPts;
      state.scores.landing_pts = landingPts;
      state.scores.precision_pts = precisionPts;
      state.scores.crash_penalty = crashPenalty;
      state.scores.total = total;

      playerCourseStats[championship.currentCourseIdx] = {
        name: currentCourse.name,
        time: state.run_clock,
        gates: state.gates_passed + '/' + totalGates,
        proximity: state.proximity_pts,
        landingGrade: grade,
        crashes: state.crash_count,
        total: Math.round(total)
      };'''

content = content.replace(old_outcome_total, new_outcome_total, 1)

# 13. Update showScoreSheet with crashes row
old_sheet_prox = r'''      document.getElementById('sheet-you-prox').textContent = '+' + state.proximity_pts.toFixed(1);
      document.getElementById('sheet-you-landing').textContent = grade + ' (+' + state.scores.landing_pts + ')';'''

new_sheet_prox = r'''      document.getElementById('sheet-you-prox').textContent = '+' + state.proximity_pts.toFixed(1);
      document.getElementById('sheet-you-crashes').textContent = state.crash_count + ' (' + (state.scores.crash_penalty === 0 ? '+0' : state.scores.crash_penalty) + ')';
      document.getElementById('sheet-kes-crashes').textContent = '0 (+0)';
      document.getElementById('sheet-you-landing').textContent = grade + ' (+' + state.scores.landing_pts + ')';'''

content = content.replace(old_sheet_prox, new_sheet_prox, 1)

# 14. Add showReckoningPanel function and button handlers
reckoning_js = r'''
    // --- ROUND 7: RECKONING PANEL & RATINGS ---
    function showReckoningPanel() {
      state.phase = 'RECKONING';
      document.getElementById('podium-screen').style.display = 'none';
      const reckoningScreen = document.getElementById('reckoning-screen');

      const standings = championship.getStandings();
      const youStanding = standings.find(s => s.name === 'YOU');
      const champTotal = youStanding ? youStanding.total : 0;
      const rating = calculatePlayerRating(champTotal);

      const ratingBadge = document.getElementById('reckoning-rating-badge');
      ratingBadge.className = 'rating-badge rating-' + rating;
      ratingBadge.textContent = rating;

      const descMap = {
        'S': 'LEGENDARY &bull; SCORE &ge; 5600',
        'A': 'EXPERT &bull; SCORE &ge; 5200',
        'B': 'PROFICIENT &bull; SCORE &ge; 4600',
        'C': 'NOVICE &bull; SCORE < 4600'
      };
      document.getElementById('reckoning-rating-desc').innerHTML = descMap[rating];
      document.getElementById('reckoning-champ-total').textContent = champTotal + ' PTS';

      // Courses Breakdown Table
      const cBody = document.getElementById('reckoning-courses-body');
      cBody.innerHTML = '';
      for (let i = 0; i < 3; i++) {
        const stats = playerCourseStats[i] || {
          name: COURSES[i].name,
          time: 0,
          gates: '0/' + COURSES[i].gates.length,
          proximity: 0,
          landingGrade: '--',
          crashes: 0,
          total: championship.course_totals.YOU[i] || 0
        };
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><b>${i + 1}. ${stats.name}</b></td>
          <td style="text-align: right;">${stats.time ? stats.time.toFixed(1) + 's' : '--'}</td>
          <td style="text-align: right;">${stats.gates}</td>
          <td style="text-align: right;">+${stats.proximity ? stats.proximity.toFixed(1) : '0.0'}</td>
          <td style="text-align: right;">${stats.landingGrade}</td>
          <td style="text-align: right; color: ${stats.crashes > 0 ? '#ff5566' : '#d8e5f5'};">${stats.crashes}</td>
          <td style="text-align: right; font-weight: bold; color: #ffd875;">${stats.total}</td>
        `;
        cBody.appendChild(tr);
      }

      // Final Standings Table
      const sBody = document.getElementById('reckoning-standings-body');
      sBody.innerHTML = '';
      standings.forEach(s => {
        const tr = document.createElement('tr');
        if (s.name === 'YOU') tr.className = 'highlight-you';
        tr.innerHTML = `
          <td class="standings-rank-${s.rank}">#${s.rank}</td>
          <td><b>${s.name}</b></td>
          <td style="text-align: right; font-weight: bold; color: #ffd875;">${s.total} PTS</td>
        `;
        sBody.appendChild(tr);
      });

      reckoningScreen.style.display = 'flex';
    }
'''

content = content.replace("    function startChampionship() {", reckoning_js + "\n    function startChampionship() {", 1)

# 15. Update button on Podium to call showReckoningPanel, and add Reckoning button listener
old_listeners = r'''    document.getElementById('podium-done-btn').addEventListener('click', () => {
      if (state.phase === 'PODIUM') resetToChampionshipMenu();
    });'''

new_listeners = r'''    document.getElementById('podium-done-btn').addEventListener('click', () => {
      if (state.phase === 'PODIUM') showReckoningPanel();
    });
    document.getElementById('reckoning-done-btn').addEventListener('click', () => {
      if (state.phase === 'RECKONING') resetToChampionshipMenu();
    });'''

content = content.replace(old_listeners, new_listeners, 1)

# 16. Update Enter key listener for Podium and Reckoning
old_enter_listener = r'''      // Enter: Advances between courses or returns from podium
      if (e.key === 'Enter') {
        if (state.phase === 'LANDED') {
          advanceToNextCourse();
        } else if (state.phase === 'PODIUM') {
          resetToChampionshipMenu();
        }
      }'''

new_enter_listener = r'''      // Enter: Advances between courses, advances to Reckoning, or returns from Reckoning
      if (e.key === 'Enter') {
        if (state.phase === 'LANDED') {
          advanceToNextCourse();
        } else if (state.phase === 'PODIUM') {
          showReckoningPanel();
        } else if (state.phase === 'RECKONING') {
          resetToChampionshipMenu();
        }
      }'''

content = content.replace(old_enter_listener, new_enter_listener, 1)

# 17. Reset crash_count and freeze in launchCourse and resetToChampionshipMenu
old_launch_resets = r'''      state.chosen_fork_variants = [];
      state.gate_timestamps = [];'''

new_launch_resets = r'''      state.chosen_fork_variants = [];
      state.gate_timestamps = [];
      state.crash_count = 0;
      state.respawn_freeze = 0.0;
      state.respawn_point_in_use = null;
      state.last_passed_variant = null;'''

content = content.replace(old_launch_resets, new_launch_resets)

# 18. Also hide reckoning-screen in launchCourse and resetToChampionshipMenu
content = content.replace(
    "document.getElementById('podium-screen').style.display = 'none';",
    "document.getElementById('podium-screen').style.display = 'none';\n      document.getElementById('reckoning-screen').style.display = 'none';"
)

# 19. Update HUD for respawn freeze banner
hud_respawn_update = r'''
      const hudRespawn = document.getElementById('respawn-warning');
      if (state.respawn_freeze > 0 && state.phase === 'FLIGHT') {
        hudRespawn.textContent = 'CHECKPOINT RESPAWN \u2022 CONTROLS FROZEN (' + state.respawn_freeze.toFixed(1) + 's) \u2022 -150 PTS';
        hudRespawn.style.display = 'block';
      } else {
        hudRespawn.style.display = 'none';
      }
'''

content = content.replace("      if (state.stall && state.phase === 'FLIGHT') {", hud_respawn_update + "\n      if (state.stall && state.phase === 'FLIGHT') {", 1)

# 20. Update camera update for RECKONING phase
content = content.replace(
    "if (state.phase === 'READY' || state.phase === 'PODIUM')",
    "if (state.phase === 'READY' || state.phase === 'PODIUM' || state.phase === 'RECKONING')"
)

# 21. Expose triggerRespawn and showReckoningPanel in test API
old_test_api = r'''      resetToChampionshipMenu,
      showPodiumCeremony
    };'''

new_test_api = r'''      resetToChampionshipMenu,
      showPodiumCeremony,
      showReckoningPanel,
      triggerRespawn,
      playerCourseStats
    };'''

content = content.replace(old_test_api, new_test_api, 1)

with open("index.html", "w") as f:
    f.write(content)

print("Round 7 successfully applied to index.html! New length:", len(content))
