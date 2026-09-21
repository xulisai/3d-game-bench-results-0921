with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. switchLevel updates: Level 3 support, Lift tool & UI display
# -----------------------------------------------------------------------------
old_switch_tabs = """      // Update level tabs UI
      document.getElementById('tab-lvl1').classList.toggle('active', activeLevel === 1);
      document.getElementById('tab-lvl2').classList.toggle('active', activeLevel === 2);
      document.getElementById('tool-lift').style.display = (activeLevel === 2 ? 'flex' : 'none');
      document.getElementById('row-stage-lift').style.display = (activeLevel === 2 ? 'flex' : 'none');"""

new_switch_tabs = """      // Update level tabs UI
      document.getElementById('tab-lvl1').classList.toggle('active', activeLevel === 1);
      document.getElementById('tab-lvl2').classList.toggle('active', activeLevel === 2);
      document.getElementById('tab-lvl3').classList.toggle('active', activeLevel === 3);

      const hasLift = (activeLevel === 2 || activeLevel === 3);
      document.getElementById('tool-lift').style.display = hasLift ? 'flex' : 'none';
      document.getElementById('row-stage-lift').style.display = hasLift ? 'flex' : 'none';

      // Level 3 Convoy Acceptance Rows
      document.getElementById('row-stage-carriage').style.display = (activeLevel === 3 ? 'flex' : 'none');
      document.getElementById('row-stage-salute').style.display = (activeLevel === 3 ? 'flex' : 'none');

      const accTitle = document.getElementById('acceptance-title');
      const accSub = document.getElementById('acceptance-sub');
      const lblStage1 = document.getElementById('label-stage1');
      const lblStage2 = document.getElementById('label-stage2');

      if (activeLevel === 3) {
        if (accTitle) accTitle.textContent = "ROYAL CONVOY";
        if (accSub) accSub.textContent = "CONVOY & LIFT";
        if (lblStage1) lblStage1.textContent = "Wagon: Light Steam (60w)";
        if (lblStage2) lblStage2.textContent = "Truck: Heavy Steam (180w)";
      } else {
        if (accTitle) accTitle.textContent = "ROYAL ACCEPTANCE";
        if (accSub) accSub.textContent = (activeLevel === 2 ? "TWO-STAGE + LIFT" : "TWO-STAGE");
        if (lblStage1) lblStage1.textContent = "Stage 1: Light Wagon (60w)";
        if (lblStage2) lblStage2.textContent = "Stage 2: Heavy Truck (180w)";
      }"""

assert old_switch_tabs in html, "old_switch_tabs not found"
html = html.replace(old_switch_tabs, new_switch_tabs)

# Lift tool hotkey enabled on Level 2 and Level 3
old_lift_hotkey = """} else if ((e.key === 'l' || e.key === 'L') && activeLevel === 2) {"""
new_lift_hotkey = """} else if ((e.key === 'l' || e.key === 'L') && (activeLevel === 2 || activeLevel === 3)) {"""

assert old_lift_hotkey in html, "old_lift_hotkey not found"
html = html.replace(old_lift_hotkey, new_lift_hotkey)

old_lift_click = """} else if (selectedTool === 'lift' && activeLevel === 2) {"""
new_lift_click = """} else if (selectedTool === 'lift' && (activeLevel === 2 || activeLevel === 3)) {"""

assert old_lift_click in html, "old_lift_click not found"
html = html.replace(old_lift_click, new_lift_click)

# -----------------------------------------------------------------------------
# 2. updateUI: Crown marks on level tabs, Carriage & Salute Badges
# -----------------------------------------------------------------------------
old_ui_badges = """      updateBadge(badgeStage1, stage1Status);
      updateBadge(badgeStage2, stage2Status);
      if (badgeStageLift) updateBadge(badgeStageLift, stageLiftStatus);

      if (lvl1StatusBadge) {
        lvl1StatusBadge.textContent = level1Status;
        lvl1StatusBadge.className = 'tab-status ' + (level1Status === 'PASSED' ? 'tab-passed' : 'tab-pending');
      }
      if (lvl2StatusBadge) {
        lvl2StatusBadge.textContent = level2Status;
        lvl2StatusBadge.className = 'tab-status ' + (level2Status === 'PASSED' ? 'tab-passed' : 'tab-pending');
      }"""

new_ui_badges = """      updateBadge(badgeStage1, stage1Status);
      updateBadge(badgeStage2, stage2Status);
      if (badgeStageLift) updateBadge(badgeStageLift, stageLiftStatus);

      const badgeCarriage = document.getElementById('badge-stagecarriage');
      if (badgeCarriage) updateBadge(badgeCarriage, stageCarriageStatus);

      const badgeSalute = document.getElementById('badge-stagesalute');
      if (badgeSalute) updateBadge(badgeSalute, stageSaluteStatus);

      // Crown Marks on Level Tabs when passed
      const lvl3StatusBadge = document.getElementById('lvl3-status-badge');
      if (lvl1StatusBadge) {
        lvl1StatusBadge.textContent = (level1Status === 'PASSED' ? "👑 PASSED" : "PENDING");
        lvl1StatusBadge.className = 'tab-status ' + (level1Status === 'PASSED' ? 'tab-passed' : 'tab-pending');
      }
      if (lvl2StatusBadge) {
        lvl2StatusBadge.textContent = (level2Status === 'PASSED' ? "👑 PASSED" : "PENDING");
        lvl2StatusBadge.className = 'tab-status ' + (level2Status === 'PASSED' ? 'tab-passed' : 'tab-pending');
      }
      if (lvl3StatusBadge) {
        lvl3StatusBadge.textContent = (level3Status === 'PASSED' ? "👑 PASSED" : "PENDING");
        lvl3StatusBadge.className = 'tab-status ' + (level3Status === 'PASSED' ? 'tab-passed' : 'tab-pending');
      }"""

assert old_ui_badges in html, "old_ui_badges not found"
html = html.replace(old_ui_badges, new_ui_badges)

# Lift sub-text on toolbox
old_sub_corridor = """liftSubText.textContent = designatedLiftMember ? `Span: [${designatedLiftMember.label}]` : "Corridor [24-32]";"""
new_sub_corridor = """const corrDesc = (activeLevel === 3 ? "Corridor [20-28]" : "Corridor [24-32]");
        liftSubText.textContent = designatedLiftMember ? `Span: [${designatedLiftMember.label}]` : corrDesc;"""

assert old_sub_corridor in html, "old_sub_corridor not found"
html = html.replace(old_sub_corridor, new_sub_corridor)

# Level 3 HUD status text in updateUI
old_hud_test = """        } else if (activeStage === 'stage2') {
          hudStatus.textContent = "STAGE 2: TRUCK (180w)...";
        }"""

new_hud_test = """        } else if (activeStage === 'stage2') {
          hudStatus.textContent = "STAGE 2: TRUCK (180w)...";
        } else if (activeStage === 'convoy') {
          if (isSaluting) {
            hudStatus.textContent = `ROYAL SALUTE (${(4.0 - saluteTimer).toFixed(1)}s)...`;
          } else {
            hudStatus.textContent = `ROYAL CONVOY (${convoyTimeline.toFixed(1)}s)...`;
          }
        }"""

assert old_hud_test in html, "old_hud_test not found"
html = html.replace(old_hud_test, new_hud_test)

# Tab 3 Click Listener
old_tab_listener = """    document.getElementById('tab-lvl1').addEventListener('click', () => switchLevel(1));
    document.getElementById('tab-lvl2').addEventListener('click', () => switchLevel(2));"""

new_tab_listener = """    document.getElementById('tab-lvl1').addEventListener('click', () => switchLevel(1));
    document.getElementById('tab-lvl2').addEventListener('click', () => switchLevel(2));
    const tab3Btn = document.getElementById('tab-lvl3');
    if (tab3Btn) tab3Btn.addEventListener('click', () => switchLevel(3));"""

assert old_tab_listener in html, "old_tab_listener not found"
html = html.replace(old_tab_listener, new_tab_listener)

# -----------------------------------------------------------------------------
# 3. window.__arena_state EXPORT SCHEMA
# -----------------------------------------------------------------------------
old_arena_state_block = """      const isWagonMoving = ((gameState === 'test' || isReplaying) && wagon.active && !wagon.fell && !wagon.won);
      const isTruckMoving = ((gameState === 'test' || isReplaying) && truck.active && !truck.fell && !truck.won);

      let stageName = null;
      if (gameState === 'test' || gameState === 'won' || gameState === 'lost' || isReplaying) {
        if (activeStage === 'settle') stageName = 'SETTLE';
        else if (activeStage === 'stage1' || activeStage === 'stage1_toast') stageName = 'STAGE 1';
        else if (activeStage === 'lift') stageName = 'LIFT';
        else if (activeStage === 'stage2') stageName = 'STAGE 2';
        else stageName = activeStage;
      }

      window.__arena_state = {
        mode: isReplaying ? 'replay' : gameState,
        active_level: activeLevel,
        activeLevel: activeLevel,
        levels: {
          level1: level1Status,
          level2: level2Status
        },
        level1_status: level1Status,
        level2_status: level2Status,
        remaining_budget: remainingBudget,
        remainingBudget: remainingBudget,
        settle_phase: (gameState === 'test' && activeStage === 'settle'),
        settlePhase: (gameState === 'test' && activeStage === 'settle'),
        test_result: lastTestResult,
        last_test_result: lastTestResult,
        active_stage: stageName,
        activeStage: stageName,
        stages: {
          stage1: stage1Status,
          lift: activeLevel === 2 ? stageLiftStatus : undefined,
          stage2: stage2Status
        },
        stage1_status: stage1Status,
        stage_lift_status: activeLevel === 2 ? stageLiftStatus : undefined,
        stage2_status: stage2Status,
        lift_span: (activeLevel === 2 && designatedLiftMember) ? {
          id: designatedLiftMember.label,
          label: designatedLiftMember.label,
          phase: liftCyclePhase,
          raised_y: +(liftSpanCurrentRaiseY.toFixed(2))
        } : null,
        liftSpan: (activeLevel === 2 && designatedLiftMember) ? {
          id: designatedLiftMember.label,
          label: designatedLiftMember.label,
          phase: liftCyclePhase,
          raised_y: +(liftSpanCurrentRaiseY.toFixed(2))
        } : null,
        airship: {
          active: !!airshipState.active,
          position: [+(airshipState.x.toFixed(2)), +(airshipState.y.toFixed(2)), +(airshipState.z.toFixed(2))],
          progress: +(airshipState.progress.toFixed(2))
        },
        wagon: {
          position: [+(wagon.x.toFixed(2)), +(wagon.y.toFixed(2)), +(wagon.z.toFixed(2))],
          speed: isWagonMoving ? wagon.speed : 0
        },
        truck: {
          position: [+(truck.x.toFixed(2)), +(truck.y.toFixed(2)), +(truck.z.toFixed(2))],
          speed: isTruckMoving ? truck.speed : 0
        },
        first_snapped_member: firstSnappedMember ? {
          id: firstSnappedMember.label,
          type: firstSnappedMember.type,
          load_percentage: firstSnappedMember.snapLoad,
          snap_load: firstSnappedMember.snapLoad
        } : null,
        budget_ceiling: (activeLevel === 2 ? LEVEL_2_CONFIG.budget : LEVEL_1_CONFIG.budget),
        budgetCeiling: (activeLevel === 2 ? LEVEL_2_CONFIG.budget : LEVEL_1_CONFIG.budget),
        level_budgets: {
          level1: LEVEL_1_CONFIG.budget,
          level2: LEVEL_2_CONFIG.budget
        },"""

new_arena_state_block = """      const isWagonMoving = ((gameState === 'test' || isReplaying) && wagon.active && !wagon.fell && !wagon.won && !isSaluting);
      const isTruckMoving = ((gameState === 'test' || isReplaying) && truck.active && !truck.fell && !truck.won && !isSaluting);
      const isCarriageMoving = ((gameState === 'test' || isReplaying) && carriage.active && !carriage.fell && !carriage.won && !isSaluting);

      let stageName = null;
      if (gameState === 'test' || gameState === 'won' || gameState === 'lost' || isReplaying) {
        if (activeStage === 'settle') stageName = 'SETTLE';
        else if (isSaluting) stageName = 'SALUTE';
        else if (activeStage === 'stage1' || activeStage === 'stage1_toast') stageName = 'STAGE 1';
        else if (activeStage === 'lift') stageName = 'LIFT';
        else if (activeStage === 'stage2') stageName = 'STAGE 2';
        else if (activeStage === 'convoy') stageName = 'CONVOY';
        else stageName = activeStage;
      }

      const activeCfg = (activeLevel === 3 ? LEVEL_3_CONFIG : (activeLevel === 2 ? LEVEL_2_CONFIG : LEVEL_1_CONFIG));
      const hasLiftActive = (activeLevel === 2 || activeLevel === 3);

      window.__arena_state = {
        mode: isReplaying ? 'replay' : gameState,
        active_level: activeLevel,
        activeLevel: activeLevel,
        levels: {
          level1: level1Status,
          level2: level2Status,
          level3: level3Status
        },
        level1_status: level1Status,
        level2_status: level2Status,
        level3_status: level3Status,
        remaining_budget: remainingBudget,
        remainingBudget: remainingBudget,
        settle_phase: (gameState === 'test' && activeStage === 'settle'),
        settlePhase: (gameState === 'test' && activeStage === 'settle'),
        test_result: lastTestResult,
        last_test_result: lastTestResult,
        active_stage: stageName,
        activeStage: stageName,
        stages: {
          stage1: stage1Status,
          wagon: stage1Status,
          truck: stage2Status,
          stage2: stage2Status,
          carriage: activeLevel === 3 ? stageCarriageStatus : undefined,
          salute: activeLevel === 3 ? stageSaluteStatus : undefined,
          lift: hasLiftActive ? stageLiftStatus : undefined
        },
        stage1_status: stage1Status,
        stage_lift_status: hasLiftActive ? stageLiftStatus : undefined,
        stage2_status: stage2Status,
        stage_carriage_status: activeLevel === 3 ? stageCarriageStatus : undefined,
        stage_salute_status: activeLevel === 3 ? stageSaluteStatus : undefined,
        salute_countdown: +(Math.max(0, 4.0 - saluteTimer).toFixed(2)),
        convoy_order: ['wagon', 'truck', 'carriage'],
        lift_span: (hasLiftActive && designatedLiftMember) ? {
          id: designatedLiftMember.label,
          label: designatedLiftMember.label,
          phase: liftCyclePhase,
          raised_y: +(liftSpanCurrentRaiseY.toFixed(2))
        } : null,
        liftSpan: (hasLiftActive && designatedLiftMember) ? {
          id: designatedLiftMember.label,
          label: designatedLiftMember.label,
          phase: liftCyclePhase,
          raised_y: +(liftSpanCurrentRaiseY.toFixed(2))
        } : null,
        airship: {
          active: !!airshipState.active,
          position: [+(airshipState.x.toFixed(2)), +(airshipState.y.toFixed(2)), +(airshipState.z.toFixed(2))],
          progress: +(airshipState.progress.toFixed(2))
        },
        wagon: {
          position: [+(wagon.x.toFixed(2)), +(wagon.y.toFixed(2)), +(wagon.z.toFixed(2))],
          speed: isWagonMoving ? wagon.speed : 0
        },
        truck: {
          position: [+(truck.x.toFixed(2)), +(truck.y.toFixed(2)), +(truck.z.toFixed(2))],
          speed: isTruckMoving ? truck.speed : 0
        },
        carriage: {
          position: [+(carriage.x.toFixed(2)), +(carriage.y.toFixed(2)), +(carriage.z.toFixed(2))],
          speed: isCarriageMoving ? carriage.speed : 0
        },
        first_snapped_member: firstSnappedMember ? {
          id: firstSnappedMember.label,
          type: firstSnappedMember.type,
          load_percentage: firstSnappedMember.snapLoad,
          snap_load: firstSnappedMember.snapLoad
        } : null,
        budget_ceiling: activeCfg.budget,
        budgetCeiling: activeCfg.budget,
        level_budgets: {
          level1: LEVEL_1_CONFIG.budget,
          level2: LEVEL_2_CONFIG.budget,
          level3: LEVEL_3_CONFIG.budget
        },"""

assert old_arena_state_block in html, "old_arena_state_block not found"
html = html.replace(old_arena_state_block, new_arena_state_block)

# -----------------------------------------------------------------------------
# 4. Animate Loop: Onlooker Banners Rise during Royal Salute
# -----------------------------------------------------------------------------
old_flag_anim = """      // Flag stir in wind
      flagPoles.forEach((fp, idx) => {
        const t = (currentTime * 0.003) + idx;
        fp.flagMesh.rotation.y = Math.sin(t) * 0.25;
      });"""

new_flag_anim = """      // Flag stir in wind
      flagPoles.forEach((fp, idx) => {
        const t = (currentTime * 0.003) + idx;
        fp.flagMesh.rotation.y = Math.sin(t) * 0.25;
      });

      // Onlooker banners rising during Royal Salute
      if (typeof onlookerBanners !== 'undefined' && onlookerBanners.length > 0) {
        const liftOffset = (isSaluting ? 0.7 : 0.0);
        onlookerBanners.forEach((ob, idx) => {
          ob.mesh.position.y = ob.basePos.y + liftOffset + Math.sin(currentTime * 0.006 + idx) * 0.08;
          ob.mesh.rotation.y = Math.sin(currentTime * 0.004 + idx) * 0.3;
        });
      }"""

assert old_flag_anim in html, "old_flag_anim not found"
html = html.replace(old_flag_anim, new_flag_anim)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated UI, level tabs, and window.__arena_state export!")
