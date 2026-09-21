# Part 6: Herd Migration, Wolves, Lark Flight, Grass Snake
part6 = r"""
    // =========================================================
    // 9. HERD MIGRATION & GRAZING
    // =========================================================
    const MIGRATION_PATH = [
      { x: 280, z: 0 },
      { x: 330, z: 0 },
      { x: 370, z: 0 },
      { x: 404, z: 0 },
      { x: 425, z: 15 },
      { x: 445, z: 65 }
    ];

    const segLengths = [];
    const cumLengths = [0];
    for (let i = 0; i < MIGRATION_PATH.length - 1; i++) {
      const dx = MIGRATION_PATH[i+1].x - MIGRATION_PATH[i].x;
      const dz = MIGRATION_PATH[i+1].z - MIGRATION_PATH[i].z;
      const len = Math.hypot(dx, dz);
      segLengths.push(len);
      cumLengths.push(cumLengths[cumLengths.length - 1] + len);
    }
    const TOTAL_PATH_LEN = cumLengths[cumLengths.length - 1];

    function getPathPoint(dist) {
      if (dist <= 0) {
        const dx = MIGRATION_PATH[1].x - MIGRATION_PATH[0].x;
        const dz = MIGRATION_PATH[1].z - MIGRATION_PATH[0].z;
        const h = Math.hypot(dx, dz) || 1;
        return { x: MIGRATION_PATH[0].x, z: MIGRATION_PATH[0].z, dirX: dx/h, dirZ: dz/h };
      }
      if (dist >= TOTAL_PATH_LEN) {
        const last = MIGRATION_PATH.length - 1;
        const dx = MIGRATION_PATH[last].x - MIGRATION_PATH[last-1].x;
        const dz = MIGRATION_PATH[last].z - MIGRATION_PATH[last-1].z;
        const h = Math.hypot(dx, dz) || 1;
        return { x: MIGRATION_PATH[last].x, z: MIGRATION_PATH[last].z, dirX: dx/h, dirZ: dz/h };
      }
      for (let i = 0; i < segLengths.length; i++) {
        if (dist <= cumLengths[i+1]) {
          const u = (dist - cumLengths[i]) / segLengths[i];
          const p0 = MIGRATION_PATH[i];
          const p1 = MIGRATION_PATH[i+1];
          const dx = p1.x - p0.x;
          const dz = p1.z - p0.z;
          const h = Math.hypot(dx, dz) || 1;
          return {
            x: p0.x + dx * u,
            z: p0.z + dz * u,
            dirX: dx / h,
            dirZ: dz / h
          };
        }
      }
      return { x: 445, z: 65, dirX: 0.37, dirZ: 0.93 };
    }

    function updateHerd(time, dt) {
      if (STATE.realm !== "dream") return;

      if (STATE.herdPhase === "gathered") {
        // Gathering ground loop at (280, 0)
        herdEntities.forEach(cow => {
          const grazeCycle = Math.sin((time + cow.phaseOffset) * 1.4);
          cow.parts.neckGroup.rotation.x = 0.55 + grazeCycle * 0.25;
          cow.parts.neckGroup.rotation.y = Math.cos((time + cow.phaseOffset) * 0.8) * 0.15;
          cow.parts.tailPivot.rotation.z = Math.sin((time + cow.phaseOffset) * 3.5) * 0.4;
          cow.parts.legFL.rotation.x = 0;
          cow.parts.legFR.rotation.x = 0;
          cow.parts.legBL.rotation.x = 0;
          cow.parts.legBR.rotation.x = 0;

          cow.mesh.position.set(cow.gatherPos.x, cow.gatherPos.y, cow.gatherPos.z);
          cow.mesh.rotation.y = cow.gatherPos.rot;

          STATE.herd[cow.id - 1].pos[0] = cow.gatherPos.x;
          STATE.herd[cow.id - 1].pos[1] = cow.gatherPos.y;
          STATE.herd[cow.id - 1].pos[2] = cow.gatherPos.z;
        });
      } else if (STATE.herdPhase === "walking") {
        const elapsedSinceDep = time - STATE.migrationStartTime;
        const leadDist = elapsedSinceDep * STATE.herdSpeed; // 1.6 units / sec

        let allSettled = true;

        herdEntities.forEach(cow => {
          if (cow.isMother) {
            // Mother cow at rear:
            const motherDist = leadDist - cow.longOffset;
            const distToNicheJunction = cumLengths[3]; // at (404, 0), cumLength = 124

            if (motherDist < distToNicheJunction) {
              // Walking along path
              const pt = getPathPoint(Math.max(0, motherDist));
              const nx = -pt.dirZ * cow.latOffset;
              const nz = pt.dirX * cow.latOffset;
              const cx = pt.x + nx;
              const cz = pt.z + nz;
              const cy = getGrasslandElevation(cx, cz);
              cow.mesh.position.set(cx, cy, cz);
              cow.mesh.rotation.y = Math.atan2(pt.dirX, pt.dirZ);

              const legW = Math.sin(motherDist * 3.5) * 0.45;
              cow.parts.legFL.rotation.x = legW;
              cow.parts.legBR.rotation.x = legW;
              cow.parts.legFR.rotation.x = -legW;
              cow.parts.legBL.rotation.x = -legW;

              STATE.herd[cow.id - 1].pos[0] = cx;
              STATE.herd[cow.id - 1].pos[1] = cy;
              STATE.herd[cow.id - 1].pos[2] = cz;
              allSettled = false;
            } else {
              // Branch off to niche at (404, -8)
              const nicheDist = (motherDist - distToNicheJunction);
              const totalNicheLen = 8.0; // from (404, 0) to (404, -8)
              if (nicheDist < totalNicheLen) {
                const u = nicheDist / totalNicheLen;
                const cx = 404;
                const cz = 0 - u * 8.0;
                const cy = getGrasslandElevation(cx, cz);
                cow.mesh.position.set(cx, cy, cz);
                cow.mesh.rotation.y = Math.PI; // facing south into niche

                const legW = Math.sin(motherDist * 3.5) * 0.45;
                cow.parts.legFL.rotation.x = legW;
                cow.parts.legBR.rotation.x = legW;
                cow.parts.legFR.rotation.x = -legW;
                cow.parts.legBL.rotation.x = -legW;

                STATE.herd[cow.id - 1].pos[0] = cx;
                STATE.herd[cow.id - 1].pos[1] = cy;
                STATE.herd[cow.id - 1].pos[2] = cz;
                allSettled = false;
              } else {
                // Arrived in niche and lies down!
                const cx = 404;
                const cz = -8;
                const cy = getGrasslandElevation(cx, cz);
                cow.mesh.position.set(cx, cy, cz);
                cow.mesh.rotation.y = Math.PI * 0.95;
                cow.parts.setLyingDown();
                STATE.motherLainDown = true;
                circle6Mesh.material.opacity = 0.75; // niche circle becomes active!

                STATE.herd[cow.id - 1].pos[0] = cx;
                STATE.herd[cow.id - 1].pos[1] = cy;
                STATE.herd[cow.id - 1].pos[2] = cz;
              }
            }
          } else {
            // Other 7 cattle
            const cowDist = leadDist - cow.longOffset;
            if (cowDist < TOTAL_PATH_LEN) {
              const pt = getPathPoint(Math.max(0, cowDist));
              const nx = -pt.dirZ * cow.latOffset;
              const nz = pt.dirX * cow.latOffset;
              const cx = pt.x + nx;
              const cz = pt.z + nz;
              const cy = getGrasslandElevation(cx, cz);
              cow.mesh.position.set(cx, cy, cz);
              cow.mesh.rotation.y = Math.atan2(pt.dirX, pt.dirZ);

              const legW = Math.sin(cowDist * 3.5) * 0.45;
              cow.parts.legFL.rotation.x = legW;
              cow.parts.legBR.rotation.x = legW;
              cow.parts.legFR.rotation.x = -legW;
              cow.parts.legBL.rotation.x = -legW;

              STATE.herd[cow.id - 1].pos[0] = cx;
              STATE.herd[cow.id - 1].pos[1] = cy;
              STATE.herd[cow.id - 1].pos[2] = cz;
              allSettled = false;
            } else {
              // Settled in eastern meadow
              const sx = cow.settledPos.x;
              const sz = cow.settledPos.z;
              const sy = getGrasslandElevation(sx, sz);
              cow.mesh.position.set(sx, sy, sz);
              cow.mesh.rotation.y = cow.phaseOffset;

              const grazeCycle = Math.sin((time + cow.phaseOffset) * 1.4);
              cow.parts.neckGroup.rotation.x = 0.55 + grazeCycle * 0.25;
              cow.parts.neckGroup.rotation.y = Math.cos((time + cow.phaseOffset) * 0.8) * 0.15;
              cow.parts.tailPivot.rotation.z = Math.sin((time + cow.phaseOffset) * 3.5) * 0.4;
              cow.parts.legFL.rotation.x = 0;
              cow.parts.legFR.rotation.x = 0;
              cow.parts.legBL.rotation.x = 0;
              cow.parts.legBR.rotation.x = 0;

              STATE.herd[cow.id - 1].pos[0] = sx;
              STATE.herd[cow.id - 1].pos[1] = sy;
              STATE.herd[cow.id - 1].pos[2] = sz;
            }
          }
        });

        if (allSettled && STATE.motherLainDown) {
          STATE.herdPhase = "settled";
        }
      } else if (STATE.herdPhase === "settled") {
        herdEntities.forEach(cow => {
          if (cow.isMother) {
            cow.parts.setLyingDown();
            cow.mesh.position.set(404, getGrasslandElevation(404, -8), -8);
          } else {
            const sx = cow.settledPos.x;
            const sz = cow.settledPos.z;
            const sy = getGrasslandElevation(sx, sz);
            cow.mesh.position.set(sx, sy, sz);
            const grazeCycle = Math.sin((time + cow.phaseOffset) * 1.4);
            cow.parts.neckGroup.rotation.x = 0.55 + grazeCycle * 0.25;
            cow.parts.neckGroup.rotation.y = Math.cos((time + cow.phaseOffset) * 0.8) * 0.15;
            cow.parts.tailPivot.rotation.z = Math.sin((time + cow.phaseOffset) * 3.5) * 0.4;
          }
        });
      }
    }

    // =========================================================
    // 10. WOLVES & PATROL LOOPS
    // =========================================================
    function getWolfTrajectory(id, t) {
      if (id === 1) {
        // W1: rectangle (344,-9) -> (356,-9) -> (356,-3) -> (344,-3), speed 1.0
        const perim = 36;
        let d = (t * 1.0) % perim;
        if (d < 12) return { x: 344 + d, z: -9, yaw: Math.PI / 2 };
        d -= 12;
        if (d < 6) return { x: 356, z: -9 + d, yaw: 0 };
        d -= 6;
        if (d < 12) return { x: 356 - d, z: -3, yaw: -Math.PI / 2 };
        d -= 12;
        return { x: 344, z: -3 - d, yaw: Math.PI };
      } else if (id === 2) {
        // W2: ellipse centered (368, 7), radii 6 x 4, speed 0.9
        const theta = (t * 0.9) / 5.0;
        const x = 368 + 6 * Math.cos(theta);
        const z = 7 + 4 * Math.sin(theta);
        const dx = -6 * Math.sin(theta);
        const dz = 4 * Math.cos(theta);
        return { x, z, yaw: Math.atan2(dx, dz) };
      } else if (id === 3) {
        // W3: square (380,-7) +- 4, speed 1.1
        const perim = 32;
        let d = (t * 1.1) % perim;
        if (d < 8) return { x: 376 + d, z: -11, yaw: Math.PI / 2 };
        d -= 8;
        if (d < 8) return { x: 384, z: -11 + d, yaw: 0 };
        d -= 8;
        if (d < 8) return { x: 384 - d, z: -3, yaw: -Math.PI / 2 };
        d -= 8;
        return { x: 376, z: -3 - d, yaw: Math.PI };
      } else {
        // W4: circle around (396, 5), radius 5, speed 0.8
        const theta = (t * 0.8) / 5.0;
        const x = 396 + 5 * Math.cos(theta);
        const z = 5 + 5 * Math.sin(theta);
        const dx = -5 * Math.sin(theta);
        const dz = 5 * Math.cos(theta);
        return { x, z, yaw: Math.atan2(dx, dz) };
      }
    }

    function updateWolves(dt) {
      if (STATE.realm !== "dream") return;

      const pX = STATE.player.pos[0];
      const pZ = STATE.player.pos[2];

      wolfEntities.forEach((wObj, idx) => {
        const wolfState = STATE.wolves[idx];

        if (wolfState.vanished) {
          wObj.root.visible = false;
          return;
        }

        if (wolfState.retreating) {
          wolfState.retreatTimer += dt;
          const retreatProgress = Math.min(wolfState.retreatTimer / 3.0, 1.0);
          // Walk up towards canyon walls and vanish
          const targetZ = (wObj.id === 3) ? -16.0 : 16.0;
          wObj.root.position.z = THREE.MathUtils.lerp(wolfState.pos[2], targetZ, dt * 2.0);
          wObj.root.position.y = getGrasslandElevation(wObj.root.position.x, wObj.root.position.z);
          wolfState.pos[0] = wObj.root.position.x;
          wolfState.pos[1] = wObj.root.position.y;
          wolfState.pos[2] = wObj.root.position.z;

          const legW = Math.sin(STATE.elapsedTime * 8.0) * 0.45;
          wObj.legFL.rotation.x = legW;
          wObj.legBR.rotation.x = legW;
          wObj.legFR.rotation.x = -legW;
          wObj.legBL.rotation.x = -legW;

          if (retreatProgress >= 1.0) {
            wolfState.vanished = true;
            wObj.root.visible = false;
          }
          return;
        }

        const traj = getWolfTrajectory(wObj.id, STATE.elapsedTime);
        const wy = getGrasslandElevation(traj.x, traj.z);
        wObj.root.position.set(traj.x, wy, traj.z);
        wObj.root.rotation.y = traj.yaw;

        wolfState.pos[0] = traj.x;
        wolfState.pos[1] = wy;
        wolfState.pos[2] = traj.z;

        // Animated prowl leg swings
        const legW = Math.sin(STATE.elapsedTime * 6.0) * 0.45;
        wObj.legFL.rotation.x = legW;
        wObj.legBR.rotation.x = legW;
        wObj.legFR.rotation.x = -legW;
        wObj.legBL.rotation.x = -legW;
        wObj.tail.rotation.y = Math.sin(STATE.elapsedTime * 3.5) * 0.2;

        // CATCH RULE:
        // wolfRadius: 7.5 units, wolfDwell: 0.8 seconds
        const distToNiulai = Math.hypot(pX - traj.x, pZ - traj.z);
        if (distToNiulai <= STATE.wolfRadius) {
          wolfState.dwellTimer += dt;
          if (wolfState.dwellTimer >= STATE.wolfDwell && !STATE.isCaughtFading) {
            // Niulai caught!
            triggerWolfCatch();
          }
        } else {
          // Stepping outside ring resets timer
          wolfState.dwellTimer = 0;
        }
      });
    }

    const blackFade = document.getElementById('black-fade');
    const hudStrikes = document.getElementById('hud-strikes');

    function triggerWolfCatch() {
      STATE.isCaughtFading = true;
      blackFade.style.opacity = '1';

      setTimeout(() => {
        // Reappear at canyon mouth (334, 0) with Bola beside him
        STATE.player.pos[0] = 334;
        STATE.player.pos[2] = 0;
        STATE.player.pos[1] = getGrasslandElevation(334, 0);
        STATE.player.speed = 0;
        STATE.player.targetSpeed = 0;
        cameraYaw = 0;

        STATE.bola.pos[0] = 332;
        STATE.bola.pos[2] = 0;
        STATE.bola.pos[1] = getGrasslandElevation(332, 0);
        STATE.bola.state = "following";
        setBolaPose("standing");

        STATE.strikes += 1;
        hudStrikes.textContent = `Strikes: ${STATE.strikes}`;

        // Reset all dwell timers
        STATE.wolves.forEach(w => w.dwellTimer = 0);

        blackFade.style.opacity = '0';
        setTimeout(() => {
          STATE.isCaughtFading = false;
        }, 600);
      }, 600);
    }

    // =========================================================
    // 11. FLYING LARK YUNDING GUIDE
    // =========================================================
    function updateLarkGuide(time, dt) {
      if (STATE.realm !== "dream") {
        flyingLark.root.visible = false;
        return;
      }
      flyingLark.root.visible = true;

      let targetPos = null;
      let radius = 8.0;

      if (!STATE.memories.hollow) {
        targetPos = { x: 95, z: 15 };
      } else if (!STATE.memories.ford) {
        targetPos = { x: 130, z: 44 };
      } else if (!STATE.memories.steppe) {
        targetPos = { x: 210, z: 0 };
      } else if (!STATE.memories.canyon) {
        targetPos = { x: 336, z: 0 };
      } else if (!STATE.memories.niche) {
        targetPos = { x: 404, z: -8 };
      } else {
        // When no unwitnessed memory remains: circles player at 10-unit radius!
        targetPos = { x: STATE.player.pos[0], z: STATE.player.pos[2] };
        radius = 10.0;
      }

      const speed = (radius === 10.0) ? 1.2 : 1.5;
      const angle = time * speed;
      const lx = targetPos.x + radius * Math.cos(angle);
      const lz = targetPos.z + radius * Math.sin(angle);
      const gy = getGrasslandElevation(lx, lz);
      const ly = gy + 4.2 + Math.sin(time * 3.0) * 0.4;

      flyingLark.root.position.set(lx, ly, lz);

      // Tangent direction for flight heading
      const dirX = -Math.sin(angle);
      const dirZ = Math.cos(angle);
      flyingLark.root.rotation.y = Math.atan2(dirX, dirZ);
      flyingLark.root.rotation.z = 0.22; // banking into turn

      // Wing flaps
      const flap = Math.sin(time * 16.0) * 0.65;
      flyingLark.wingL.rotation.z = flap;
      flyingLark.wingR.rotation.z = -flap;
    }

    // =========================================================
    // 12. GRASS SNAKE UPDATE
    // =========================================================
    const SNAKE_ORIGIN = { x: 120, z: -55 };
    const SNAKE_ESCAPE_DIR = { x: 0.6, z: -0.8 };
    const SNAKE_ESCAPE_DIST = 12.0;

    function updateGrassSnake(dt) {
      if (STATE.realm !== "dream") return;

      if (!STATE.snake.fled) {
        const distToPlayer = Math.hypot(STATE.player.pos[0] - STATE.snake.pos[0], STATE.player.pos[2] - STATE.snake.pos[2]);
        if (distToPlayer <= 4.0 && !STATE.snake.fleeing) {
          STATE.snake.fleeing = true;
          STATE.snake.fleeTime = 0;
          showStoryBanner("A grass snake slips away — Niulai shivers, and walks on.");
        }

        if (STATE.snake.fleeing) {
          STATE.snake.fleeTime += dt;
          const progress = Math.min(STATE.snake.fleeTime / 2.4, 1.0);
          const curDist = progress * SNAKE_ESCAPE_DIST;
          const sx = SNAKE_ORIGIN.x + SNAKE_ESCAPE_DIR.x * curDist;
          const sz = SNAKE_ORIGIN.z + SNAKE_ESCAPE_DIR.z * curDist;
          const sy = getGrasslandElevation(sx, sz);

          STATE.snake.pos[0] = sx;
          STATE.snake.pos[1] = sy;
          STATE.snake.pos[2] = sz;

          snakeModel.root.position.set(sx, sy, sz);
          snakeModel.root.rotation.y = Math.atan2(SNAKE_ESCAPE_DIR.x, SNAKE_ESCAPE_DIR.z);

          snakeModel.segments.forEach((seg, i) => {
            seg.position.x = Math.sin(STATE.snake.fleeTime * 14.0 - i * 0.8) * 0.16;
          });

          if (progress >= 1.0) {
            STATE.snake.fleeing = false;
            STATE.snake.fled = true;
            snakeModel.root.visible = false;
          }
        } else {
          snakeModel.segments.forEach((seg, i) => {
            seg.position.x = Math.sin(STATE.elapsedTime * 1.5 + i * 0.5) * 0.05;
          });
        }
      }
    }
"""
