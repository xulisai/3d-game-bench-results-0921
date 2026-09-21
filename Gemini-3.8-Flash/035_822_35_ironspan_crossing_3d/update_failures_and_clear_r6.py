with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. Carriage falling physics & failure labeling
# -----------------------------------------------------------------------------
old_truck_fall = """      if (truck.fell) {
        truck.vy += GRAVITY_Y * FIXED_DT;
        truck.x += truck.vx * FIXED_DT;
        truck.y += truck.vy * FIXED_DT;
        truck.pitch += 1.4 * FIXED_DT;
        if (truck.y < -16.0) {
          handleFailure("STAGE 2", "The Heavy Steam Truck plunged into the gorge!");
        }
      }"""

new_carriage_fall = """      if (truck.fell) {
        truck.vy += GRAVITY_Y * FIXED_DT;
        truck.x += truck.vx * FIXED_DT;
        truck.y += truck.vy * FIXED_DT;
        truck.pitch += 1.4 * FIXED_DT;
        if (truck.y < -16.0) {
          const failLabel = (activeLevel === 3 ? "TRUCK" : "STAGE 2");
          handleFailure(failLabel, "The Heavy Steam Truck plunged into the gorge!");
        }
      }
      if (carriage.fell) {
        carriage.vy += GRAVITY_Y * FIXED_DT;
        carriage.x += carriage.vx * FIXED_DT;
        carriage.y += carriage.vy * FIXED_DT;
        carriage.pitch += 1.3 * FIXED_DT;
        if (carriage.y < -16.0) {
          handleFailure("CARRIAGE", "The Royal Steam Carriage plunged into the gorge!");
        }
      }"""

assert old_truck_fall in html, "old_truck_fall not found"
html = html.replace(old_truck_fall, new_carriage_fall)

# Node drop detection failure tag
old_node_drop = """          if (activeStage === 'settle') {
            handleFailure("SETTLE", "Structural collapse! Settle phase failed under self-weight.");
          } else if (activeStage === 'lift') {
            handleFailure("LIFT", "Structural collapse! Flanking structure could not stand without the lift span.");
          } else if (activeStage === 'stage1' && !wagon.fell) {
            wagon.fell = true;
            wagon.vx = wagon.speed * 0.8;
            wagon.vy = -2.0;
          } else if (activeStage === 'stage2' && !truck.fell) {
            truck.fell = true;
            truck.vx = truck.speed * 0.8;
            truck.vy = -2.0;
          }"""

new_node_drop = """          if (activeStage === 'settle') {
            handleFailure("SETTLE", "Structural collapse! Settle phase failed under self-weight.");
          } else if (activeStage === 'lift') {
            handleFailure("LIFT", "Structural collapse! Flanking structure could not stand without the lift span.");
          } else if (isSaluting) {
            handleFailure("SALUTE", "Structural collapse during the Royal Salute!");
          } else if (activeLevel === 3 && activeStage === 'convoy') {
            if (!wagon.won && !wagon.fell) wagon.fell = true;
            if (truck.active && !truck.won && !truck.fell) truck.fell = true;
            if (carriage.active && !carriage.won && !carriage.fell) carriage.fell = true;
            handleFailure(carriage.active ? "CARRIAGE" : (truck.active ? "TRUCK" : "WAGON"), "Structural collapse under convoy load!");
          } else if (activeStage === 'stage1' && !wagon.fell) {
            wagon.fell = true;
            wagon.vx = wagon.speed * 0.8;
            wagon.vy = -2.0;
          } else if (activeStage === 'stage2' && !truck.fell) {
            truck.fell = true;
            truck.vx = truck.speed * 0.8;
            truck.vy = -2.0;
          }"""

assert old_node_drop in html, "old_node_drop not found"
html = html.replace(old_node_drop, new_node_drop)

# Member snap stage tag naming
old_snap_tag = """          const stageLabel = (activeStage === 'settle' ? 'SETTLE' : (activeStage === 'lift' ? 'LIFT' : (activeStage === 'stage2' ? 'STAGE 2' : 'STAGE 1')));
          handleFailure(stageLabel, `Structural failure! Member ${mem.label} snapped under load.`);"""

new_snap_tag = """          let stageLabel = 'STAGE 1';
          if (activeStage === 'settle') stageLabel = 'SETTLE';
          else if (activeStage === 'lift') stageLabel = 'LIFT';
          else if (isSaluting) stageLabel = 'SALUTE';
          else if (activeLevel === 3) {
            if (carriage.active && !carriage.won) stageLabel = 'CARRIAGE';
            else if (truck.active && !truck.won) stageLabel = 'TRUCK';
            else stageLabel = 'WAGON';
          } else if (activeStage === 'stage2') stageLabel = 'STAGE 2';
          handleFailure(stageLabel, `Structural failure! Member ${mem.label} snapped under load.`);"""

assert old_snap_tag in html, "old_snap_tag not found"
html = html.replace(old_snap_tag, new_snap_tag)

# -----------------------------------------------------------------------------
# 2. triggerCrossingClear: Level 3 Royal Seal Display & Crown Marks
# -----------------------------------------------------------------------------
old_crossing_clear = """    function triggerCrossingClear() {
      if (gameState === 'won') return;
      gameState = 'won';
      isReplaying = false;
      lastTestResult = "CROSSING CLEAR";

      stage1Status = 'PASSED';
      stage2Status = 'PASSED';
      if (activeLevel === 2) stageLiftStatus = 'PASSED';

      if (activeLevel === 1) level1Status = 'PASSED';
      else level2Status = 'PASSED';

      bannerTitle.textContent = "CROSSING CLEAR";
      bannerTitle.className = "banner-headline banner-win";
      bannerDesc.textContent = `Full Royal Acceptance Granted! Remaining Budget: ${remainingBudget} sovereigns`;

      bannerStages.style.display = 'flex';
      bannerStage1Tag.textContent = "Stage 1: PASSED (Light Wagon)";
      bannerStage1Tag.style.background = "rgba(34,197,94,0.25)";
      bannerStage1Tag.style.borderColor = "#22c55e";
      bannerStage1Tag.style.color = "#86efac";

      bannerStage2Tag.textContent = "Stage 2: PASSED (Heavy Truck)";
      bannerStage2Tag.style.background = "rgba(34,197,94,0.25)";
      bannerStage2Tag.style.borderColor = "#22c55e";
      bannerStage2Tag.style.color = "#86efac";

      bannerScreen.style.display = 'flex';
      updateUI();
    }"""

new_crossing_clear = """    function triggerCrossingClear() {
      if (gameState === 'won') return;
      gameState = 'won';
      isReplaying = false;
      lastTestResult = "CROSSING CLEAR";

      stage1Status = 'PASSED';
      stage2Status = 'PASSED';
      if (activeLevel === 2 || activeLevel === 3) stageLiftStatus = 'PASSED';
      if (activeLevel === 3) {
        stageCarriageStatus = 'PASSED';
        stageSaluteStatus = 'PASSED';
      }

      if (activeLevel === 1) level1Status = 'PASSED';
      else if (activeLevel === 2) level2Status = 'PASSED';
      else if (activeLevel === 3) level3Status = 'PASSED';

      if (activeLevel === 3) {
        // Round 6: Royal Seal Victory Display for Level 3
        bannerTitle.textContent = "ROYAL SEAL OF THE REALM";
        bannerTitle.className = "banner-headline banner-win";
        bannerDesc.textContent = `The Royal Convoy has conquered Thunderfall Chasm! Remaining: ${remainingBudget} sovereigns`;

        const sealSummary = document.getElementById('royal-seal-summary');
        if (sealSummary) {
          sealSummary.style.display = 'block';
          const sealStatusDiv = document.getElementById('seal-level-status');
          if (sealStatusDiv) {
            sealStatusDiv.innerHTML = `
              <div><strong>LEVEL 1:</strong> ${level1Status} (${levelData[1].remainingBudget} sov)</div>
              <div><strong>LEVEL 2:</strong> ${level2Status} (${levelData[2].remainingBudget} sov)</div>
              <div><strong>LEVEL 3:</strong> ${level3Status} (${remainingBudget} sov)</div>
            `;
          }
        }
      } else {
        bannerTitle.textContent = "CROSSING CLEAR";
        bannerTitle.className = "banner-headline banner-win";
        bannerDesc.textContent = `Full Royal Acceptance Granted! Remaining Budget: ${remainingBudget} sovereigns`;
        const sealSummary = document.getElementById('royal-seal-summary');
        if (sealSummary) sealSummary.style.display = 'none';
      }

      bannerStages.style.display = 'flex';
      bannerStage1Tag.textContent = (activeLevel === 3 ? "Wagon: PASSED" : "Stage 1: PASSED (Light Wagon)");
      bannerStage1Tag.style.background = "rgba(34,197,94,0.25)";
      bannerStage1Tag.style.borderColor = "#22c55e";
      bannerStage1Tag.style.color = "#86efac";

      bannerStage2Tag.textContent = (activeLevel === 3 ? "Truck: PASSED" : "Stage 2: PASSED (Heavy Truck)");
      bannerStage2Tag.style.background = "rgba(34,197,94,0.25)";
      bannerStage2Tag.style.borderColor = "#22c55e";
      bannerStage2Tag.style.color = "#86efac";

      const bLift = document.getElementById('banner-stagelift-tag');
      if (bLift) bLift.style.display = (activeLevel === 2 || activeLevel === 3 ? 'inline-block' : 'none');
      const bCarriage = document.getElementById('banner-stagecarriage-tag');
      if (bCarriage) bCarriage.style.display = (activeLevel === 3 ? 'inline-block' : 'none');
      const bSalute = document.getElementById('banner-stagesalute-tag');
      if (bSalute) bSalute.style.display = (activeLevel === 3 ? 'inline-block' : 'none');

      bannerScreen.style.display = 'flex';
      updateUI();
    }"""

assert old_crossing_clear in html, "old_crossing_clear not found"
html = html.replace(old_crossing_clear, new_crossing_clear)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated failures and victory clear with Royal Seal!")
