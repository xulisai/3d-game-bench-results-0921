with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the vehicle update block in fixedPhysicsStep
start_marker = "      if (activeStage === 'settle') {"
end_marker = "      if (wagon.fell) {"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)
assert start_idx != -1 and end_idx != -1, "Vehicle update block markers not found"

new_stages_code = """      if (activeStage === 'settle') {
        wagon.testTimer += FIXED_DT;
        settlePhaseActive = (wagon.testTimer < SETTLE_DURATION);

        if (wagon.testTimer >= SETTLE_DURATION) {
          settlePhaseActive = false;
          if (activeLevel === 3) {
            // Level 3: Start Royal Convoy!
            activeStage = 'convoy';
            stage1Status = 'RUNNING';
            wagon.active = true;
            wagon.mesh.visible = true;
            convoyTimeline = 0.0;
            document.getElementById('stage-toast').textContent = "ROYAL CONVOY DEPARTING";
            document.getElementById('stage-toast').style.display = 'block';
          } else {
            activeStage = 'stage1';
            stage1Status = 'RUNNING';
            wagon.active = true;
            wagon.mesh.visible = true;
          }
        }
      } else if (activeLevel === 3 && activeStage === 'convoy') {
        // Round 6: Royal Convoy continuous sequence on Level 3 (48u span)
        // Fixed departure schedule: Wagon at 0s, Truck at 6s, Carriage at 12s
        convoyTimeline += FIXED_DT;
        if (convoyTimeline > 1.5) {
          document.getElementById('stage-toast').style.display = 'none';
        }

        // 1. Truck departure at 6.0s
        if (convoyTimeline >= 6.0 && !truck.active && !truck.won && !truck.fell) {
          truck.active = true;
          truck.mesh.visible = true;
          stage2Status = 'RUNNING';
        }

        // 2. Royal Carriage departure at 12.0s
        if (convoyTimeline >= 12.0 && !carriage.active && !carriage.won && !carriage.fell) {
          carriage.active = true;
          carriage.mesh.visible = true;
          stageCarriageStatus = 'RUNNING';
        }

        // 3. Check Royal Salute trigger when carriage reaches mid-span (x = 24.0)
        if (carriage.active && !carriage.won && !carriage.fell && carriage.x >= 24.0 && stageSaluteStatus === 'PENDING') {
          isSaluting = true;
          saluteTimer = 0.0;
          stageSaluteStatus = 'RUNNING';
          document.getElementById('stage-toast').textContent = "ROYAL SALUTE (4s)";
          document.getElementById('stage-toast').style.display = 'block';
        }

        // 4. Handle 4s Royal Salute holding pause
        if (isSaluting) {
          saluteTimer += FIXED_DT;
          if (saluteTimer >= 4.0) {
            isSaluting = false;
            stageSaluteStatus = 'PASSED';
            document.getElementById('stage-toast').style.display = 'none';
          }
        }

        // Move active vehicles if NOT saluting (or apply static load if saluting)
        const canMove = !isSaluting;

        // Wagon Update
        if (wagon.active && !wagon.won && !wagon.fell) {
          if (canMove) wagon.x += wagon.speed * FIXED_DT;
          if (wagon.x >= 48.0) {
            wagon.won = true;
            wagon.y = DECK_Y + 0.45;
            wagon.pitch = 0;
            stage1Status = 'PASSED';
          } else {
            const frontX = wagon.x + 1.1;
            const rearX = wagon.x - 1.1;
            const totalW = WAGON_WEIGHT * Math.abs(GRAVITY_Y);
            const hFront = applyAxleLoadAndGetHeight(frontX, totalW * 0.5);
            const hRear = applyAxleLoadAndGetHeight(rearX, totalW * 0.5);

            if (hFront === null || hRear === null) {
              wagon.fell = true;
              wagon.vx = wagon.speed;
              wagon.vy = -1.0;
            } else {
              const targetY = (hFront + hRear) * 0.5 + 0.45;
              wagon.y += (targetY - wagon.y) * 0.5;
              wagon.pitch = Math.atan2(hFront - hRear, 2.2);
            }
          }
        }

        // Truck Update
        if (truck.active && !truck.won && !truck.fell) {
          if (canMove) truck.x += truck.speed * FIXED_DT;
          if (truck.x >= 48.0) {
            truck.won = true;
            truck.y = DECK_Y + 0.48;
            truck.pitch = 0;
            stage2Status = 'PASSED';
          } else {
            const axleFrontX = truck.x + 1.9;
            const axleMidX = truck.x - 0.7;
            const axleRearX = truck.x - 2.6;
            const totalW = TRUCK_WEIGHT * Math.abs(GRAVITY_Y);
            const axleWeight = totalW / 3.0;

            const hFront = applyAxleLoadAndGetHeight(axleFrontX, axleWeight);
            const hMid = applyAxleLoadAndGetHeight(axleMidX, axleWeight);
            const hRear = applyAxleLoadAndGetHeight(axleRearX, axleWeight);

            if (hFront === null || hMid === null || hRear === null) {
              truck.fell = true;
              truck.vx = truck.speed;
              truck.vy = -1.0;
            } else {
              const targetY = (hFront + hRear) * 0.5 + 0.48;
              truck.y += (targetY - truck.y) * 0.5;
              truck.pitch = Math.atan2(hFront - hRear, 4.5);
            }
          }
        }

        // Royal Steam Carriage Update
        if (carriage.active && !carriage.won && !carriage.fell) {
          if (canMove) carriage.x += carriage.speed * FIXED_DT;
          if (carriage.x >= 48.0) {
            carriage.won = true;
            carriage.y = DECK_Y + 0.52;
            carriage.pitch = 0;
            stageCarriageStatus = 'PASSED';
          } else {
            const axleFrontX = carriage.x + 1.8;
            const axleMidX = carriage.x;
            const axleRearX = carriage.x - 1.8;
            const totalW = CARRIAGE_WEIGHT * Math.abs(GRAVITY_Y);
            const axleWeight = totalW / 3.0;

            const hFront = applyAxleLoadAndGetHeight(axleFrontX, axleWeight);
            const hMid = applyAxleLoadAndGetHeight(axleMidX, axleWeight);
            const hRear = applyAxleLoadAndGetHeight(axleRearX, axleWeight);

            if (hFront === null || hMid === null || hRear === null) {
              carriage.fell = true;
              carriage.vx = carriage.speed;
              carriage.vy = -1.0;
            } else {
              const targetY = (hFront + hRear) * 0.5 + 0.52;
              carriage.y += (targetY - carriage.y) * 0.5;
              carriage.pitch = Math.atan2(hFront - hRear, 3.6);
            }
          }
        }

        // When all 3 vehicles have safely arrived across 48u, begin the LIFT phase!
        if (wagon.won && truck.won && carriage.won && stageSaluteStatus === 'PASSED') {
          activeStage = 'lift';
          liftCyclePhase = 'raising';
          liftCycleTimer = 0.0;
          stageLiftStatus = 'RUNNING';
          document.getElementById('stage-toast').textContent = "ALL CONVOY ARRIVED — OPENING LIFT SPAN";
          document.getElementById('stage-toast').style.display = 'block';
        }
      } else if (activeStage === 'stage1') {
        if (!wagon.fell && !wagon.won) {
          wagon.x += wagon.speed * FIXED_DT;

          const currentSpanEnd = (activeLevel === 2 ? 36.0 : 24.0);
          if (wagon.x >= currentSpanEnd) {
            wagon.won = true;
            wagon.y = DECK_Y + 0.45;
            wagon.pitch = 0;
            stage1Status = 'PASSED';
            stageToastTimer = 0.0;

            if (activeLevel === 2) {
              activeStage = 'lift';
              liftCyclePhase = 'raising';
              liftCycleTimer = 0.0;
              stageLiftStatus = 'RUNNING';
              document.getElementById('stage-toast').textContent = "STAGE 1 PASSED — OPENING LIFT SPAN";
              document.getElementById('stage-toast').style.display = 'block';
            } else {
              activeStage = 'stage1_toast';
              document.getElementById('stage-toast').textContent = "STAGE 1 PASSED";
              document.getElementById('stage-toast').style.display = 'block';
            }
          } else {
            const frontX = wagon.x + 1.1;
            const rearX = wagon.x - 1.1;
            const totalW = WAGON_WEIGHT * Math.abs(GRAVITY_Y);
            const hFront = applyAxleLoadAndGetHeight(frontX, totalW * 0.5);
            const hRear = applyAxleLoadAndGetHeight(rearX, totalW * 0.5);

            if (hFront === null || hRear === null) {
              wagon.fell = true;
              wagon.vx = wagon.speed;
              wagon.vy = -1.0;
            } else {
              const targetY = (hFront + hRear) * 0.5 + 0.45;
              wagon.y += (targetY - wagon.y) * 0.5;
              wagon.pitch = Math.atan2(hFront - hRear, 2.2);
            }
          }
        }
      } else if (activeStage === 'stage1_toast') {
        const currentSpanEnd = (activeLevel === 2 ? 36.0 : 24.0);
        wagon.x = currentSpanEnd + 2.0;
        wagon.y = DECK_Y + 0.45;
        wagon.pitch = 0;
        stageToastTimer += FIXED_DT;

        if (stageToastTimer >= STAGE_TOAST_DURATION) {
          document.getElementById('stage-toast').style.display = 'none';
          activeStage = 'stage2';
          stage2Status = 'RUNNING';
          truck.active = true;
          truck.fell = false;
          truck.vx = 0;
          truck.vy = 0;
          truck.pitch = 0;
          truck.mesh.visible = true;
          truck.x = -6.0;
          truck.y = DECK_Y + 0.48;
        }
      } else if (activeStage === 'lift') {
        const activeCfg = (activeLevel === 3 ? LEVEL_3_CONFIG : LEVEL_2_CONFIG);
        const midCorridorX = (activeLevel === 3 ? 24.0 : 28.0);

        liftCycleTimer += FIXED_DT;
        if (liftCycleTimer > 1.5) {
          document.getElementById('stage-toast').style.display = 'none';
        }

        if (liftCyclePhase === 'raising') {
          const t = Math.min(1.0, liftCycleTimer / activeCfg.liftRaiseDuration);
          liftSpanCurrentRaiseY = t * activeCfg.liftHeight;

          if (liftCycleTimer >= activeCfg.liftRaiseDuration) {
            liftCyclePhase = 'holding';
            liftCycleTimer = 0.0;
            liftSpanCurrentRaiseY = activeCfg.liftHeight;
            airshipState.active = true;
            airshipMesh.visible = true;
          }
        } else if (liftCyclePhase === 'holding') {
          liftSpanCurrentRaiseY = activeCfg.liftHeight;
          const t = Math.min(1.0, liftCycleTimer / activeCfg.liftHoldDuration);
          airshipState.progress = t;
          airshipState.x = midCorridorX;
          airshipState.y = DECK_Y + 1.2;
          airshipState.z = -35.0 + t * 70.0;
          airshipMesh.position.set(airshipState.x, airshipState.y, airshipState.z);

          if (liftCycleTimer >= activeCfg.liftHoldDuration) {
            liftCyclePhase = 'lowering';
            liftCycleTimer = 0.0;
            airshipState.active = false;
            airshipMesh.visible = false;
          }
        } else if (liftCyclePhase === 'lowering') {
          const t = Math.min(1.0, liftCycleTimer / activeCfg.liftLowerDuration);
          liftSpanCurrentRaiseY = (1.0 - t) * activeCfg.liftHeight;

          if (liftCycleTimer >= activeCfg.liftLowerDuration) {
            liftCyclePhase = 'completed';
            liftSpanCurrentRaiseY = 0.0;

            // Re-seat lift span rest length to current resting joint distance
            if (designatedLiftMember) {
              const idxA = nodeIndexMap.get(designatedLiftMember.nodeA.id);
              const idxB = nodeIndexMap.get(designatedLiftMember.nodeB.id);
              if (idxA !== undefined && idxB !== undefined) {
                const nA = simNodes[idxA];
                const nB = simNodes[idxB];
                const d = Math.sqrt((nB.x - nA.x) ** 2 + (nB.y - nA.y) ** 2 + (nB.z - nA.z) ** 2);
                designatedLiftMember.restLength = d;
              }
            }

            stageLiftStatus = 'PASSED';
            if (activeLevel === 3) {
              // Level 3 finishes on lift span lowering!
              triggerCrossingClear();
            } else {
              activeStage = 'stage2';
              stage2Status = 'RUNNING';
              truck.active = true;
              truck.fell = false;
              truck.vx = 0;
              truck.vy = 0;
              truck.pitch = 0;
              truck.mesh.visible = true;
              truck.x = -6.0;
              truck.y = DECK_Y + 0.48;
            }
          }
        }

        updateLiftPistonVisuals();
      } else if (activeStage === 'stage2') {
        if (!truck.fell && !truck.won) {
          truck.x += truck.speed * FIXED_DT;

          const currentSpanEnd = (activeLevel === 2 ? 36.0 : 24.0);
          if (truck.x >= currentSpanEnd) {
            truck.won = true;
            truck.y = DECK_Y + 0.48;
            truck.pitch = 0;
            stage2Status = 'PASSED';
            triggerCrossingClear();
          } else {
            const axleFrontX = truck.x + 1.9;
            const axleMidX = truck.x - 0.7;
            const axleRearX = truck.x - 2.6;
            const totalW = TRUCK_WEIGHT * Math.abs(GRAVITY_Y);
            const axleWeight = totalW / 3.0;

            const hFront = applyAxleLoadAndGetHeight(axleFrontX, axleWeight);
            const hMid = applyAxleLoadAndGetHeight(axleMidX, axleWeight);
            const hRear = applyAxleLoadAndGetHeight(axleRearX, axleWeight);

            if (hFront === null || hMid === null || hRear === null) {
              truck.fell = true;
              truck.vx = truck.speed;
              truck.vy = -1.0;
            } else {
              const targetY = (hFront + hRear) * 0.5 + 0.48;
              truck.y += (targetY - truck.y) * 0.5;
              truck.pitch = Math.atan2(hFront - hRear, 4.5);
            }
          }
        }
      }

"""

html = html[:start_idx] + new_stages_code + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated vehicle simulation loop with Level 3 convoy and salute!")
