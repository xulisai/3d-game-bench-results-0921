with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Reset Game
old_reset = """      // Reset Hero
      hero.health = hero.maxHealth;"""

new_reset = """      // Reset Blockers
      blockers.forEach(b => scene.remove(b.mesh.root));
      blockers = [];
      recomputeDijkstraField();
      isPlacingBlocker = false;
      if (ghostBlockerGroup) ghostBlockerGroup.visible = false;

      // Reset Hero
      hero.health = hero.maxHealth;"""

assert old_reset in code, "old_reset not found"
code = code.replace(old_reset, new_reset, 1)

# 2. spawnEnemy
old_spawn = """      const enemy = {
        id: ++enemyIdCounter,
        type: type,
        spec: spec,
        model: model,
        lane: assignedLane,
        isFlying: spec.isFlying,
        maxHealth: spec.health,
        health: spec.health,
        distanceTraveled: 0,
        speed: spec.speed,
        baseSpeed: spec.speed,
        goldReward: spec.gold,
        gateDamage: spec.gateDamage,
        chillFactor: spec.chillFactor,
        chillTimer: 0,
        alive: true,
        walkAnimTime: 0
      };"""

new_spawn = """      const enemy = {
        id: ++enemyIdCounter,
        type: type,
        spec: spec,
        model: model,
        lane: assignedLane,
        isFlying: spec.isFlying,
        maxHealth: spec.health,
        health: spec.health,
        distanceTraveled: 0,
        speed: spec.speed,
        baseSpeed: spec.speed,
        goldReward: spec.gold,
        gateDamage: spec.gateDamage,
        chillFactor: spec.chillFactor,
        chillTimer: 0,
        alive: true,
        walkAnimTime: 0,
        onOpenGround: false,
        pos: new THREE.Vector3(),
        pathWaypoints: [],
        pathIndex: 0,
        radius: spec.isFlying ? 0.6 : (type === 'ogre' ? 1.35 : (type === 'elite' ? 0.85 : 0.65))
      };"""

assert old_spawn in code, "old_spawn not found"
code = code.replace(old_spawn, new_spawn, 1)

# 3. getNearestLanePoint
old_nearest_lane = """    // Find nearest point on either left or right lane for initial soldier rally placement
    function getNearestLanePoint(px, pz) {
      let bestPt = new THREE.Vector3(px, 0, pz);
      let minDist = Infinity;"""

new_nearest_lane = """    // Find nearest point on either left or right lane for initial soldier rally placement
    function getNearestLanePoint(px, pz) {
      if (px >= 5.0) {
        return new THREE.Vector3(px - 2.5, 0, pz);
      }
      let bestPt = new THREE.Vector3(px, 0, pz);
      let minDist = Infinity;"""

assert old_nearest_lane in code, "old_nearest_lane not found"
code = code.replace(old_nearest_lane, new_nearest_lane, 1)

# 4. ghostBlockerGroup initialization
old_hero_init = """    const heroModel = createHeroModel();
    heroModel.root.position.copy(HERO_SPAWN_POS);
    scene.add(heroModel.root);"""

new_hero_init = """    ghostBlockerGroup = createGhostBlocker();
    scene.add(ghostBlockerGroup);
    recomputeDijkstraField();

    const heroModel = createHeroModel();
    heroModel.root.position.copy(HERO_SPAWN_POS);
    scene.add(heroModel.root);"""

assert old_hero_init in code, "old_hero_init not found"
code = code.replace(old_hero_init, new_hero_init, 1)

# 5. Skill & Blocker toggle
old_cancel_skill = """    function cancelActiveSkill() {
      activeSkillMode = null;
      btnSkillMeteorEl.classList.remove('active-cast');
      btnSkillReinforceEl.classList.remove('active-cast');
      meteorReticle.visible = false;
      if (!isPlacingRallyPoint) {
        rallyBannerEl.style.display = 'none';
      }
    }"""

new_cancel_skill = """    const btnSkillBlockerEl = document.getElementById('btn-skill-blocker');
    const hudBlockerStateEl = document.getElementById('hud-blocker-state');

    function toggleBlockerPlacement() {
      if (isPlacingBlocker) {
        cancelBlockerPlacement();
      } else {
        if (gameState.phase !== 'defending') return;
        if (gameState.gold < BLOCKER_COST) {
          showRallyFeedback('Not enough gold (costs ' + BLOCKER_COST + ' G)!', true, window.innerWidth / 2, 120);
          return;
        }
        if (blockers.length >= MAX_BLOCKERS) {
          showRallyFeedback('Maximum blockers (' + MAX_BLOCKERS + ') reached!', true, window.innerWidth / 2, 120);
          return;
        }
        cancelActiveSkill();
        isPlacingRallyPoint = false;
        rallyTowerTarget = null;
        isPlacingBlocker = true;
        btnSkillBlockerEl.classList.add('active-cast');
        rallyBannerEl.textContent = 'Click on open ground to place a Blocker (Esc to cancel)';
        rallyBannerEl.style.display = 'block';
      }
    }

    function cancelBlockerPlacement() {
      isPlacingBlocker = false;
      if (btnSkillBlockerEl) btnSkillBlockerEl.classList.remove('active-cast');
      if (ghostBlockerGroup) ghostBlockerGroup.visible = false;
      if (!isPlacingRallyPoint && !activeSkillMode) {
        rallyBannerEl.style.display = 'none';
      }
    }

    function cancelActiveSkill() {
      activeSkillMode = null;
      btnSkillMeteorEl.classList.remove('active-cast');
      btnSkillReinforceEl.classList.remove('active-cast');
      meteorReticle.visible = false;
      cancelBlockerPlacement();
      if (!isPlacingRallyPoint) {
        rallyBannerEl.style.display = 'none';
      }
    }"""

assert old_cancel_skill in code, "old_cancel_skill not found"
code = code.replace(old_cancel_skill, new_cancel_skill, 1)

# 6. Button listener for Blocker
old_skill_reinforce_click = """    btnSkillReinforceEl.addEventListener('click', (e) => {
      e.stopPropagation();
      activateSkill('reinforce');
    });"""

new_skill_reinforce_click = """    btnSkillReinforceEl.addEventListener('click', (e) => {
      e.stopPropagation();
      activateSkill('reinforce');
    });

    btnSkillBlockerEl.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleBlockerPlacement();
    });"""

assert old_skill_reinforce_click in code, "old_skill_reinforce_click not found"
code = code.replace(old_skill_reinforce_click, new_skill_reinforce_click, 1)

# 7. mousedown additions
old_mousedown_tower = """        // Check for click on existing tower
        const towerClickables = [];"""

new_mousedown_tower = """        // Check for click on existing blocker (to remove it)
        if (!isPlacingBlocker && !activeSkillMode && !isPlacingRallyPoint) {
          const blockerHitMeshes = [];
          blockers.forEach(b => {
            if (b.mesh && b.mesh.hitBox) blockerHitMeshes.push(b.mesh.hitBox);
          });
          const blockerHits = raycaster.intersectObjects(blockerHitMeshes, false);
          if (blockerHits.length > 0) {
            const hit = blockerHits[0];
            const blockerObj = hit.object.userData.blockerObj;
            if (blockerObj) {
              const bIdx = blockers.indexOf(blockerObj);
              if (bIdx !== -1) {
                scene.remove(blockerObj.mesh.root);
                blockers.splice(bIdx, 1);
                gameState.gold += BLOCKER_COST;
                recomputeDijkstraField();
                replanAllOpenGroundEnemies();
                showRallyFeedback('🛡️ Blocker Removed (+' + BLOCKER_COST + ' G)', false, e.clientX, e.clientY);
                updateHUD();
                updateArenaState();
                return;
              }
            }
          }
        }

        // Handle Blocker Placement
        if (isPlacingBlocker) {
          const groundHits = raycaster.intersectObject(groundMesh, false);
          let clickWorldPos = null;
          if (groundHits.length > 0) {
            clickWorldPos = groundHits[0].point.clone();
          } else {
            const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
            const pt = new THREE.Vector3();
            if (raycaster.ray.intersectPlane(plane, pt)) {
              clickWorldPos = pt;
            }
          }

          if (clickWorldPos) {
            const val = validateBlockerPlacement(clickWorldPos.x, clickWorldPos.z);
            if (!val.valid) {
              showRallyFeedback(val.reason, true, e.clientX, e.clientY);
              return;
            }

            gameState.gold -= BLOCKER_COST;
            const model = createBlockerModel();
            const targetY = getRealSurfaceHeight(clickWorldPos.x, clickWorldPos.z);
            model.root.position.set(clickWorldPos.x, targetY, clickWorldPos.z);
            scene.add(model.root);

            const blockerObj = {
              id: ++blockerIdCounter,
              x: clickWorldPos.x,
              z: clickWorldPos.z,
              mesh: model
            };
            model.hitBox.userData.blockerObj = blockerObj;
            blockers.push(blockerObj);

            recomputeDijkstraField();
            replanAllOpenGroundEnemies();
            showRallyFeedback('🛡️ Blocker Placed (-' + BLOCKER_COST + ' G)', false, e.clientX, e.clientY);
            cancelBlockerPlacement();
            updateHUD();
            updateArenaState();
            return;
          }
          return;
        }

        // Check for click on existing tower
        const towerClickables = [];"""

assert old_mousedown_tower in code, "old_mousedown_tower not found"
code = code.replace(old_mousedown_tower, new_mousedown_tower, 1)

# 8. mousemove ghost preview
old_mousemove_drag = """    window.addEventListener('mousemove', (e) => {
      if (isRightDragging) {"""

new_mousemove_drag = """    window.addEventListener('mousemove', (e) => {
      if (isPlacingBlocker && ghostBlockerGroup) {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);

        const groundHits = raycaster.intersectObject(groundMesh, false);
        let pt = null;
        if (groundHits.length > 0) {
          pt = groundHits[0].point;
        } else {
          const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
          const tempPt = new THREE.Vector3();
          if (raycaster.ray.intersectPlane(plane, tempPt)) {
            pt = tempPt;
          }
        }
        if (pt) {
          ghostBlockerGroup.visible = true;
          const y = getRealSurfaceHeight(pt.x, pt.z);
          ghostBlockerGroup.position.set(pt.x, y, pt.z);

          const val = validateBlockerPlacement(pt.x, pt.z);
          if (val.valid) {
            ghostBlockerMat.color.setHex(0x22dd33);
          } else {
            ghostBlockerMat.color.setHex(0xdd2222);
          }
        }
      }

      if (isRightDragging) {"""

assert old_mousemove_drag in code, "old_mousemove_drag not found"
code = code.replace(old_mousemove_drag, new_mousemove_drag, 1)

# 9. keydown for 3 / B
old_keydown = """      } else if (e.key === '2') {
        activateSkill('reinforce');
      } else if (e.key === 'Escape') {"""

new_keydown = """      } else if (e.key === '2') {
        activateSkill('reinforce');
      } else if (e.key === '3' || e.key === 'b' || e.key === 'B') {
        toggleBlockerPlacement();
      } else if (e.key === 'Escape') {
        cancelBlockerPlacement();"""

assert old_keydown in code, "old_keydown not found"
code = code.replace(old_keydown, new_keydown, 1)

# 10. updateHUD
old_hud_end = """      } else {
        hudWaveEl.textContent = 'Wave 4 / 4';
        hudCountdownEl.textContent = 'Final Wave';
        gameState.waveIndex = 4;
      }
    }"""

new_hud_end = """      } else {
        hudWaveEl.textContent = 'Wave 4 / 4';
        hudCountdownEl.textContent = 'Final Wave';
        gameState.waveIndex = 4;
      }

      if (hudBlockerStateEl) {
        hudBlockerStateEl.textContent = blockers.length + ' / ' + MAX_BLOCKERS + ' (' + BLOCKER_COST + 'G)';
        if (blockers.length >= MAX_BLOCKERS || gameState.gold < BLOCKER_COST) {
          btnSkillBlockerEl.classList.add('cooling-down');
        } else {
          btnSkillBlockerEl.classList.remove('cooling-down');
        }
      }
    }"""

assert old_hud_end in code, "old_hud_end not found"
code = code.replace(old_hud_end, new_hud_end, 1)

# 11. getEnemyCenterPosition
old_enemy_center = """    function getEnemyCenterPosition(enemy, out) {
      out.copy(enemy.model.root.position);
      out.y += 1.35 * enemy.model.scale;
      return out;
    }"""

new_enemy_center = """    function getEnemyCenterPosition(enemy, out) {
      if (enemy.onOpenGround) {
        out.copy(enemy.pos);
      } else {
        out.copy(enemy.model.root.position);
      }
      out.y += 1.35 * enemy.model.scale;
      return out;
    }"""

assert old_enemy_center in code, "old_enemy_center not found"
code = code.replace(old_enemy_center, new_enemy_center, 1)

# 12. Enemy movement & open ground transition, separation solver, and tower targeting
old_movement_and_targeting = """          } else if (enemy.heldUpByQueue) {
            enemy.heldUpByQueue = false;
            const currentLoc = getPathPointAndDir(enemy.distanceTraveled, enemy.lane);
            enemy.model.root.position.copy(currentLoc.point);
            enemy.model.leftLeg.rotation.x = 0;
            enemy.model.rightLeg.rotation.x = 0;
            enemy.model.leftArm.rotation.x = 0;
            enemy.model.rightArm.rotation.x = 0;

          } else {
            enemy.distanceTraveled += enemy.speed * delta;
            const pathDist = PATH_DATA[enemy.lane].totalDist;
            const currentLoc = getPathPointAndDir(enemy.distanceTraveled, enemy.lane);
            enemy.model.root.position.copy(currentLoc.point);

            const targetQuat = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), currentLoc.dir);
            enemy.model.root.quaternion.slerp(targetQuat, 0.4);

            enemy.walkAnimTime += delta * enemy.speed * 4.0;
            const legSwing = Math.sin(enemy.walkAnimTime) * 0.6;
            enemy.model.leftLeg.rotation.x = legSwing;
            enemy.model.rightLeg.rotation.x = -legSwing;
            enemy.model.leftArm.rotation.x = -legSwing;
            enemy.model.rightArm.rotation.x = legSwing;

            if (enemy.distanceTraveled >= pathDist) {
              enemy.alive = false;
              scene.remove(enemy.model.root);
              enemies.splice(i, 1);
              gameState.gateHealth -= enemy.gateDamage;
              if (gameState.gateHealth <= 0) {
                gameState.gateHealth = 0;
                triggerDefeat();
                return;
              }
              continue;
            }
          }
        }

        // Health bar update
        enemy.model.barGroup.lookAt(camera.position);
        const hpPercent = Math.max(0, enemy.health / enemy.maxHealth);
        enemy.model.fgBar.scale.x = hpPercent;
        if (enemy.type === 'ogre') {
          enemy.model.fgBarMat.color.setHex(0xdd2222);
        } else if (enemy.type === 'elite') {
          enemy.model.fgBarMat.color.setHex(0x3a86ff);
        } else if (hpPercent > 0.5) {
          enemy.model.fgBarMat.color.setHex(0x22dd33);
        } else if (hpPercent > 0.25) {
          enemy.model.fgBarMat.color.setHex(0xffaa00);
        } else {
          enemy.model.fgBarMat.color.setHex(0xff2222);
        }

        if (enemy.health <= 0) {
          enemy.alive = false;
          if (enemy.blockedByHero) {
            enemy.blockedByHero.engagedEnemy = null;
            enemy.blockedByHero = null;
          }
          if (enemy.blockedBySoldier) {
            enemy.blockedBySoldier.engagedEnemy = null;
            enemy.blockedBySoldier = null;
          }
          scene.remove(enemy.model.root);
          enemies.splice(i, 1);
          gameState.gold += enemy.goldReward;
          continue;
        }
      }

      gameState.enemiesAlive = enemies.length;

      // 3. Towers Target & Fire (Arrow and Frost; ALL towers respect line of sight)
      for (const tower of towers) {
        if (tower.type === 'barracks') continue;

        tower.fireCooldown = Math.max(0, tower.fireCooldown - delta);
        getTowerHeadPosition(tower, _towerHeadPos);

        let bestTarget = null;
        let maxTraveled = -1;

        for (const enemy of enemies) {
          if (!enemy.alive) continue;
          if (enemy.isFlying && tower.type !== 'arrow') {
            continue;
          }

          getEnemyCenterPosition(enemy, _enemyCenterPos);
          const dist3D = _towerHeadPos.distanceTo(_enemyCenterPos);
          if (dist3D <= tower.effectiveRange) {
            if (enemy.distanceTraveled > maxTraveled) {
              maxTraveled = enemy.distanceTraveled;
              bestTarget = enemy;
            }
          }
        }"""

new_movement_and_targeting = """          } else if (enemy.heldUpByQueue) {
            enemy.heldUpByQueue = false;
            if (!enemy.onOpenGround) {
              const currentLoc = getPathPointAndDir(enemy.distanceTraveled, enemy.lane);
              enemy.model.root.position.copy(currentLoc.point);
            } else {
              enemy.pos.y = getRealSurfaceHeight(enemy.pos.x, enemy.pos.z);
              enemy.model.root.position.copy(enemy.pos);
            }
            enemy.model.leftLeg.rotation.x = 0;
            enemy.model.rightLeg.rotation.x = 0;
            enemy.model.leftArm.rotation.x = 0;
            enemy.model.rightArm.rotation.x = 0;

          } else {
            if (!enemy.onOpenGround) {
              // Lane Marching (before bridge exit at x = 5.0)
              enemy.distanceTraveled += enemy.speed * delta;
              const pathDist = PATH_DATA[enemy.lane].totalDist;
              const currentLoc = getPathPointAndDir(enemy.distanceTraveled, enemy.lane);
              enemy.model.root.position.copy(currentLoc.point);

              const targetQuat = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), currentLoc.dir);
              enemy.model.root.quaternion.slerp(targetQuat, 0.4);

              enemy.walkAnimTime += delta * enemy.speed * 4.0;
              const legSwing = Math.sin(enemy.walkAnimTime) * 0.6;
              enemy.model.leftLeg.rotation.x = legSwing;
              enemy.model.rightLeg.rotation.x = -legSwing;
              enemy.model.leftArm.rotation.x = -legSwing;
              enemy.model.rightArm.rotation.x = legSwing;

              if (enemy.distanceTraveled >= pathDist || currentLoc.point.x >= 5.0) {
                // Crossing bridge complete: Enter Open Ground!
                enemy.onOpenGround = true;
                enemy.pos.copy(currentLoc.point);
                planRouteForEnemy(enemy);
              }
            } else {
              // Open Ground Navigation: each enemy follows its own planned route to gate
              if (!enemy.pathWaypoints || enemy.pathWaypoints.length === 0 || enemy.pathIndex >= enemy.pathWaypoints.length) {
                planRouteForEnemy(enemy);
              }

              const targetWp = enemy.pathWaypoints[enemy.pathIndex] || CASTLE_GATE_POS;
              const tdx = targetWp.x - enemy.pos.x;
              const tdz = targetWp.z - enemy.pos.z;
              const distToWp = Math.hypot(tdx, tdz);

              if (distToWp < 0.65) {
                enemy.pathIndex++;
              }

              const moveStep = enemy.speed * delta;
              if (distToWp > 0.001) {
                const nx = tdx / distToWp;
                const nz = tdz / distToWp;
                enemy.pos.x += nx * moveStep;
                enemy.pos.z += nz * moveStep;
                const moveDir = new THREE.Vector3(nx, 0, nz);
                const targetQuat = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), moveDir);
                enemy.model.root.quaternion.slerp(targetQuat, 0.35);
              }

              enemy.pos.y = getRealSurfaceHeight(enemy.pos.x, enemy.pos.z);
              enemy.model.root.position.copy(enemy.pos);

              enemy.walkAnimTime += delta * enemy.speed * 4.0;
              const legSwing = Math.sin(enemy.walkAnimTime) * 0.6;
              enemy.model.leftLeg.rotation.x = legSwing;
              enemy.model.rightLeg.rotation.x = -legSwing;
              enemy.model.leftArm.rotation.x = -legSwing;
              enemy.model.rightArm.rotation.x = legSwing;

              if (enemy.pos.x >= 23.5 && Math.abs(enemy.pos.z - 8.0) <= 2.2) {
                enemy.alive = false;
                scene.remove(enemy.model.root);
                enemies.splice(i, 1);
                gameState.gateHealth -= enemy.gateDamage;
                if (gameState.gateHealth <= 0) {
                  gameState.gateHealth = 0;
                  triggerDefeat();
                  return;
                }
                continue;
              }
            }
          }
        }

        // Health bar update
        enemy.model.barGroup.lookAt(camera.position);
        const hpPercent = Math.max(0, enemy.health / enemy.maxHealth);
        enemy.model.fgBar.scale.x = hpPercent;
        if (enemy.type === 'ogre') {
          enemy.model.fgBarMat.color.setHex(0xdd2222);
        } else if (enemy.type === 'elite') {
          enemy.model.fgBarMat.color.setHex(0x3a86ff);
        } else if (hpPercent > 0.5) {
          enemy.model.fgBarMat.color.setHex(0x22dd33);
        } else if (hpPercent > 0.25) {
          enemy.model.fgBarMat.color.setHex(0xffaa00);
        } else {
          enemy.model.fgBarMat.color.setHex(0xff2222);
        }

        if (enemy.health <= 0) {
          enemy.alive = false;
          if (enemy.blockedByHero) {
            enemy.blockedByHero.engagedEnemy = null;
            enemy.blockedByHero = null;
          }
          if (enemy.blockedBySoldier) {
            enemy.blockedBySoldier.engagedEnemy = null;
            enemy.blockedBySoldier = null;
          }
          scene.remove(enemy.model.root);
          enemies.splice(i, 1);
          gameState.gold += enemy.goldReward;
          continue;
        }
      }

      // Separation solver: Ground enemies on open ground keep apart and never overlap
      const groundEnemies = enemies.filter(e => e.alive && !e.isFlying);
      for (let a = 0; a < groundEnemies.length; a++) {
        for (let b = a + 1; b < groundEnemies.length; b++) {
          const ea = groundEnemies[a];
          const eb = groundEnemies[b];
          const posA = ea.onOpenGround ? ea.pos : ea.model.root.position;
          const posB = eb.onOpenGround ? eb.pos : eb.model.root.position;
          const ddx = posA.x - posB.x;
          const ddz = posA.z - posB.z;
          const dsq = ddx * ddx + ddz * ddz;
          const minD = (ea.radius || 0.7) + (eb.radius || 0.7);
          if (dsq < minD * minD && dsq > 0.0001) {
            const dist = Math.sqrt(dsq);
            const push = (minD - dist) * 0.5 * 0.6;
            const nx = ddx / dist;
            const nz = ddz / dist;
            if (ea.onOpenGround && !ea.blockedByHero && !ea.blockedBySoldier) {
              ea.pos.x += nx * push;
              ea.pos.z += nz * push;
              ea.pos.y = getRealSurfaceHeight(ea.pos.x, ea.pos.z);
              ea.model.root.position.copy(ea.pos);
            }
            if (eb.onOpenGround && !eb.blockedByHero && !eb.blockedBySoldier) {
              eb.pos.x -= nx * push;
              eb.pos.z -= nz * push;
              eb.pos.y = getRealSurfaceHeight(eb.pos.x, eb.pos.z);
              eb.model.root.position.copy(eb.pos);
            }
          }
        }
      }

      gameState.enemiesAlive = enemies.length;

      // 3. Towers Target & Fire (Unified rule across entire match: closest to gate along walkable route)
      for (const tower of towers) {
        if (tower.type === 'barracks') continue;

        tower.fireCooldown = Math.max(0, tower.fireCooldown - delta);
        getTowerHeadPosition(tower, _towerHeadPos);

        let bestTarget = null;
        let minRemainingDist = Infinity;

        for (const enemy of enemies) {
          if (!enemy.alive) continue;
          if (enemy.isFlying && tower.type !== 'arrow') {
            continue;
          }

          getEnemyCenterPosition(enemy, _enemyCenterPos);
          const dist3D = _towerHeadPos.distanceTo(_enemyCenterPos);
          if (dist3D <= tower.effectiveRange) {
            const remDist = getEnemyRemainingDistToGate(enemy);
            if (remDist < minRemainingDist) {
              minRemainingDist = remDist;
              bestTarget = enemy;
            }
          }
        }"""

assert old_movement_and_targeting in code, "old_movement_and_targeting not found"
code = code.replace(old_movement_and_targeting, new_movement_and_targeting, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Part 3 applied cleanly and completely!")
