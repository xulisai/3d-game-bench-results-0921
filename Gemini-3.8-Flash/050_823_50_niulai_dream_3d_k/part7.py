# Part 7: Bola AI, Controls, Waking Sequence, Reset, Render Loop
part7 = r"""
    // =========================================================
    // 13. BOLA COMPANION AI
    // =========================================================
    const hudCompanionPrompt = document.getElementById('hud-companion-prompt');
    const hudRestPrompt = document.getElementById('hud-rest-prompt');

    function toggleBolaWaitFollow() {
      if (STATE.realm !== "dream" || !STATE.memories.hollow) return;
      if (STATE.bola.state === "following" || STATE.bola.state === "bankWaiting") {
        STATE.bola.state = "waiting";
        setBolaPose("sitting");
      } else if (STATE.bola.state === "waiting") {
        STATE.bola.state = "following";
        setBolaPose("standing");
      }
    }

    function updateBolaCompanion(dt) {
      if (STATE.realm !== "dream") return;

      if (!STATE.memories.hollow) {
        STATE.bola.state = "atHollow";
        setBolaPose("sitting");
        bolaData.tailPivot.rotation.y = Math.sin(STATE.elapsedTime * 5.0) * 0.5;
        bolaData.tailPivot.rotation.x = 0.2 + Math.cos(STATE.elapsedTime * 2.5) * 0.2;
        return;
      }

      const pX = STATE.player.pos[0];
      const pZ = STATE.player.pos[2];
      const bX = STATE.bola.pos[0];
      const bZ = STATE.bola.pos[2];

      const distToPlayer = Math.hypot(pX - bX, pZ - bZ);

      if (distToPlayer <= 7.0) {
        hudCompanionPrompt.style.display = 'block';
        if (STATE.bola.state === "following" || STATE.bola.state === "bankWaiting") {
          hudCompanionPrompt.textContent = 'Press T — Bola: Wait';
        } else {
          hudCompanionPrompt.textContent = 'Press T — Bola: Follow';
        }
      } else {
        hudCompanionPrompt.style.display = 'none';
      }

      const playerInWater = STATE.player.wading;

      if (STATE.bola.state === "waiting") {
        setBolaPose("sitting");
        STATE.bola.speed = 0;
      } else {
        if (playerInWater) {
          // Water rule: Bola stops at the water's edge and waits
          STATE.bola.state = "bankWaiting";
          STATE.bola.speed = 0;
          setBolaPose("standing");
          STATE.bola.rotation = Math.atan2(pX - bX, pZ - bZ);
        } else {
          STATE.bola.state = "following";
          const DESIRED_FOLLOW_DIST = 2.2;
          const TOLERANCE = 0.5;

          if (distToPlayer > 25.0) {
            STATE.bola.isCatchingUp = true;
          } else if (distToPlayer <= DESIRED_FOLLOW_DIST + TOLERANCE) {
            STATE.bola.isCatchingUp = false;
          }

          if (distToPlayer > DESIRED_FOLLOW_DIST + TOLERANCE) {
            let targetSpeed = 4.0;
            if (STATE.bola.isCatchingUp) {
              targetSpeed = 6.0;
            } else if (STATE.player.speed > 0.1) {
              targetSpeed = Math.max(STATE.player.speed, 3.0);
            }

            STATE.bola.speed = THREE.MathUtils.lerp(STATE.bola.speed, targetSpeed, dt * 8.0);
            const dirX = (pX - bX) / distToPlayer;
            const dirZ = (pZ - bZ) / distToPlayer;

            let stepDist = Math.min(STATE.bola.speed * dt, distToPlayer - DESIRED_FOLLOW_DIST);
            const nextBX = bX + dirX * stepDist;
            const nextBZ = bZ + dirZ * stepDist;

            const waterAtNext = checkWaterAt(nextBX, nextBZ);
            if (!waterAtNext.inWater) {
              STATE.bola.pos[0] = nextBX;
              STATE.bola.pos[2] = nextBZ;
              STATE.bola.rotation = Math.atan2(dirX, dirZ);
            } else {
              STATE.bola.speed = 0;
            }

            STATE.bola.trotCycle += dt * (STATE.bola.speed * 4.2);
            setBolaPose("trotting", STATE.bola.trotCycle);
          } else {
            STATE.bola.speed = 0;
            setBolaPose("standing");
            const dirX = (pX - bX);
            const dirZ = (pZ - bZ);
            STATE.bola.rotation = THREE.MathUtils.lerp(STATE.bola.rotation, Math.atan2(dirX, dirZ), dt * 4.0);
          }
        }
      }

      STATE.bola.pos[1] = getGrasslandElevation(STATE.bola.pos[0], STATE.bola.pos[2]);
      bolaData.root.position.set(STATE.bola.pos[0], STATE.bola.pos[1], STATE.bola.pos[2]);

      const norm = getGrasslandNormal(STATE.bola.pos[0], STATE.bola.pos[2]);
      const forward = new THREE.Vector3(Math.sin(STATE.bola.rotation), 0, Math.cos(STATE.bola.rotation));
      const right = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), forward).normalize();
      const adjustedForward = new THREE.Vector3().crossVectors(right, norm).normalize();
      const bMat = new THREE.Matrix4().makeBasis(right, norm, adjustedForward);
      bolaData.root.quaternion.setFromRotationMatrix(bMat);

      bolaData.tailPivot.rotation.y = Math.sin(STATE.elapsedTime * 6.0) * 0.45;
      bolaData.tailPivot.rotation.x = 0.25 + Math.cos(STATE.elapsedTime * 3.0) * 0.15;
    }

    // --- Audio Synthesis ---
    let audioCtx = null;
    function initAudio() {
      if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
    }

    function playMemoryFanfare() {
      if (!audioCtx) return;
      try {
        const t = audioCtx.currentTime;
        const freqs = [392, 523.25, 659.25, 783.99];
        freqs.forEach((f, i) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(f, t + i * 0.12);
          gain.gain.setValueAtTime(0, t + i * 0.12);
          gain.gain.linearRampToValueAtTime(0.18, t + i * 0.12 + 0.05);
          gain.gain.exponentialRampToValueAtTime(0.0001, t + i * 0.12 + 1.6);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(t + i * 0.12);
          osc.stop(t + i * 0.12 + 1.8);
        });
      } catch (e) {}
    }

    // --- Controls & UI ---
    const keys = {
      KeyW: false, KeyA: false, KeyS: false, KeyD: false,
      ArrowUp: false, ArrowLeft: false, ArrowDown: false, ArrowRight: false
    };

    window.addEventListener('keydown', (e) => {
      if (e.code in keys) keys[e.code] = true;
      if (e.code === 'Enter') {
        if (!STATE.isReady) startGame();
      }
      if (e.code === 'KeyT') {
        toggleBolaWaitFollow();
      }
      if (e.code === 'KeyE') {
        handleInteract();
      }
      if (e.code === 'KeyR') {
        resetGame();
      }
    });

    window.addEventListener('keyup', (e) => {
      if (e.code in keys) keys[e.code] = false;
    });

    const readyOverlay = document.getElementById('ready-overlay');
    const startBtn = document.getElementById('start-btn');
    const hudZone = document.getElementById('hud-zone');
    const hudMemories = document.getElementById('hud-memories');
    const storyBanner = document.getElementById('story-banner');
    const whiteFade = document.getElementById('white-fade');
    const closingCard = document.getElementById('closing-card');
    const closingLog = document.getElementById('closing-log');

    startBtn.addEventListener('click', () => { if (!STATE.isReady) startGame(); });
    readyOverlay.addEventListener('click', () => { if (!STATE.isReady) startGame(); });

    function startGame() {
      STATE.isReady = true;
      initAudio();
      readyOverlay.style.display = 'none';
    }

    let bannerTimer = null;
    function showStoryBanner(text, callback) {
      storyBanner.textContent = text;
      storyBanner.classList.add('visible');
      playMemoryFanfare();
      if (bannerTimer) clearTimeout(bannerTimer);
      bannerTimer = setTimeout(() => {
        storyBanner.classList.remove('visible');
        bannerTimer = null;
        if (callback) callback();
      }, 4000);
    }

    // Transition from Reality into Dream:
    function transitionToDream() {
      if (STATE.isFading) return;
      STATE.isFading = true;
      whiteFade.style.opacity = '1';

      setTimeout(() => {
        scene.remove(realityGroup);
        scene.add(dreamGroup);

        STATE.realm = "dream";
        STATE.zoneName = "Plentiful Grassland";
        hudZone.textContent = "Plentiful Grassland";
        hudZone.classList.add('dream');
        applyEnvironmentSettings("dream");

        // Spawn player in dream grassland at (10, 0)
        STATE.player.pos[0] = 10;
        STATE.player.pos[2] = 0;
        STATE.player.pos[1] = getGrasslandElevation(10, 0);
        STATE.player.rotation = 0;
        STATE.player.speed = 0;
        STATE.player.targetSpeed = 0;
        STATE.player.wading = false;
        cameraYaw = 0;

        niulai.root.position.set(10, STATE.player.pos[1], 0);

        whiteFade.style.opacity = '0';
        setTimeout(() => {
          STATE.isFading = false;
        }, 1200);

        updateArenaState();
      }, 1200);
    }

    // Waking Up Transition (from Dream's Edge back to Waking Meadow)
    function wakeUpSequence() {
      if (STATE.isFading) return;
      STATE.isFading = true;
      whiteFade.style.opacity = '1';

      setTimeout(() => {
        scene.remove(dreamGroup);
        scene.add(realityGroup);

        STATE.realm = "reality";
        STATE.zoneName = "Waking Meadow";
        STATE.awake = true;
        hudZone.textContent = "Waking Meadow";
        hudZone.classList.remove('dream');
        applyEnvironmentSettings("reality");

        // Niulai back beside the real flat rock at (35, -17)
        STATE.player.pos[0] = 35;
        STATE.player.pos[2] = -17;
        STATE.player.pos[1] = getMeadowElevation(35, -17);
        STATE.player.rotation = Math.PI;
        STATE.player.speed = 0;
        STATE.player.targetSpeed = 0;
        cameraYaw = Math.PI;

        niulai.root.position.set(35, STATE.player.pos[1], -17);

        // Display Closing Card
        displayClosingCard();

        whiteFade.style.opacity = '0';
        setTimeout(() => {
          STATE.isFading = false;
        }, 1500);

        updateArenaState();
      }, 1500);
    }

    function displayClosingCard() {
      closingLog.innerHTML = "";
      const memoryTitles = [
        "1. A lark lands beside Niulai",
        "2. Bola, the leopard cub",
        "3. Crossing the stream",
        "4. The withering steppe",
        "5. Yellow eyes in the pass",
        "6. Mother shields the calf"
      ];
      STATE.log.forEach((entry, i) => {
        const title = memoryTitles[i] || entry.memory;
        const row = document.createElement('div');
        row.className = 'log-entry';
        row.innerHTML = `<span class="log-title">${title}</span><span class="log-time">${entry.time}</span>`;
        closingLog.appendChild(row);
      });
      closingCard.style.display = 'flex';
    }

    function handleInteract() {
      if (STATE.realm !== "dream") return;
      const distToCopyRock = Math.hypot(STATE.player.pos[0] - 445, STATE.player.pos[2] - (-20));
      if (distToCopyRock <= 2.5) {
        if (STATE.memories.count === 6) {
          wakeUpSequence();
        } else {
          const remain = 6 - STATE.memories.count;
          showStoryBanner(`The dream is not finished — ${remain} memories remain.`);
        }
      }
    }

    // --- Reset Function ('R' key) ---
    function resetGame() {
      whiteFade.style.opacity = '0';
      blackFade.style.opacity = '0';
      closingCard.style.display = 'none';
      STATE.isFading = false;
      STATE.isCaughtFading = false;
      STATE.awake = false;

      if (STATE.realm === "dream") {
        scene.remove(dreamGroup);
        scene.add(realityGroup);
      }
      STATE.realm = "reality";
      STATE.zoneName = "Waking Meadow";
      hudZone.textContent = "Waking Meadow";
      hudZone.classList.remove('dream');
      applyEnvironmentSettings("reality");

      // Player back to meadow spawn at (35, 30)
      STATE.player.pos[0] = 35;
      STATE.player.pos[2] = 30;
      STATE.player.pos[1] = getMeadowElevation(35, 30);
      STATE.player.rotation = Math.PI;
      STATE.player.speed = 0;
      STATE.player.targetSpeed = 0;
      STATE.player.wading = false;
      STATE.player.stepCycle = 0;
      cameraYaw = Math.PI;

      // Reset Memories
      STATE.memories.meadow = false;
      STATE.memories.hollow = false;
      STATE.memories.ford = false;
      STATE.memories.steppe = false;
      STATE.memories.canyon = false;
      STATE.memories.niche = false;
      STATE.memories.count = 0;
      STATE.log = [];
      hudMemories.textContent = 'Memories: 0/6';

      // Reset Veils & Rocks
      STATE.veil1 = "standing";
      STATE.veil1FadeTimer = 0;
      veilMat1.opacity = 0.68;
      veil1Mesh.visible = true;

      STATE.veil2 = "standing";
      STATE.veil2FadeTimer = 0;
      veilMat2.opacity = 0.68;
      veil2Mesh.visible = true;

      STATE.rocks = "blocking";
      STATE.rocksLowerTimer = 0;
      fallenRocksGroup.position.y = 0;
      fallenRocksGroup.visible = true;

      // Reset Strikes
      STATE.strikes = 0;
      hudStrikes.textContent = 'Strikes: 0';
      hudStrikes.style.display = 'none';

      // Reset Herd
      STATE.herdPhase = "gathered";
      STATE.migrationStartTime = 0;
      STATE.motherLainDown = false;
      herdEntities.forEach(cow => {
        cow.mesh.position.set(cow.gatherPos.x, cow.gatherPos.y, cow.gatherPos.z);
        cow.mesh.rotation.y = cow.gatherPos.rot;
        cow.parts.setStanding();
      });

      // Reset Wolves
      STATE.wolves.forEach(w => {
        w.dwellTimer = 0;
        w.retreating = false;
        w.retreatTimer = 0;
        w.vanished = false;
      });
      wolfEntities.forEach(wObj => {
        wObj.root.visible = true;
      });

      // Reset Bola
      STATE.bola.state = 'atHollow';
      STATE.bola.pos[0] = 95;
      STATE.bola.pos[1] = getGrasslandElevation(95, 15);
      STATE.bola.pos[2] = 15;
      STATE.bola.rotation = -Math.PI * 0.6;
      STATE.bola.speed = 0;
      STATE.bola.isCatchingUp = false;
      setBolaPose("sitting");

      // Reset Snake
      STATE.snake.fled = false;
      STATE.snake.fleeing = false;
      STATE.snake.fleeTime = 0;
      STATE.snake.pos[0] = 120;
      STATE.snake.pos[1] = getGrasslandElevation(120, -55);
      STATE.snake.pos[2] = -55;
      snakeModel.root.visible = true;
      snakeModel.root.position.set(120, STATE.snake.pos[1], -55);

      // Circles
      meadowRingMat.opacity = 0.75;
      storyRingMat3.opacity = 0.35;
      circle6Mesh.material.opacity = 0.35;

      hudCompanionPrompt.style.display = 'none';
      hudRestPrompt.style.display = 'none';

      if (bannerTimer) {
        clearTimeout(bannerTimer);
        bannerTimer = null;
      }
      storyBanner.classList.remove('visible');

      updateArenaState();
    }

    // Initial player setup
    STATE.player.pos[0] = 35;
    STATE.player.pos[2] = 30;
    STATE.player.pos[1] = getMeadowElevation(35, 30);
    niulai.root.position.set(35, STATE.player.pos[1], 30);

    let cameraYaw = Math.PI;
    camera.position.set(35, STATE.player.pos[1] + 2.2, 35.5);
    camera.lookAt(35, STATE.player.pos[1] + 1.0, 30);

    let rippleTimer = 0;
    let lastTime = performance.now();

    // =========================================================
    // 14. MAIN ANIMATION & RENDER LOOP
    // =========================================================
    function animate(now) {
      requestAnimationFrame(animate);
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      STATE.elapsedTime += dt;

      // 1. Veils & Rocks dissolution
      if (STATE.veil1 === "dissolving") {
        STATE.veil1FadeTimer += dt;
        const progress = Math.min(STATE.veil1FadeTimer / 0.8, 1.0);
        veilMat1.opacity = (1.0 - progress) * 0.68;
        if (progress >= 1.0) {
          STATE.veil1 = "dissolved";
          veil1Mesh.visible = false;
        }
      }
      if (STATE.veil2 === "dissolving") {
        STATE.veil2FadeTimer += dt;
        const progress = Math.min(STATE.veil2FadeTimer / 0.8, 1.0);
        veilMat2.opacity = (1.0 - progress) * 0.68;
        if (progress >= 1.0) {
          STATE.veil2 = "dissolved";
          veil2Mesh.visible = false;
          // Trigger Herd Migration!
          STATE.herdPhase = "walking";
          STATE.migrationStartTime = STATE.elapsedTime;
        }
      }
      if (STATE.rocks === "lowering") {
        STATE.rocksLowerTimer += dt;
        const progress = Math.min(STATE.rocksLowerTimer / 0.8, 1.0);
        fallenRocksGroup.position.y = -progress * 6.0;
        if (progress >= 1.0) {
          STATE.rocks = "cleared";
          fallenRocksGroup.visible = false;
        }
      }

      // 2. Zone Name and Crossfade Handling
      const px = STATE.player.pos[0];
      const pz = STATE.player.pos[2];

      if (STATE.realm === "dream") {
        if (px < 200) {
          STATE.zoneName = "Plentiful Grassland";
        } else if (px < 330) {
          STATE.zoneName = "Withering Steppe";
        } else if (px <= 410) {
          STATE.zoneName = "Wolf Pass";
        } else {
          STATE.zoneName = "Dream's Edge";
        }
        hudZone.textContent = STATE.zoneName;

        // Strikes display only in Wolf Pass
        if (STATE.zoneName === "Wolf Pass") {
          hudStrikes.style.display = 'block';
        } else {
          hudStrikes.style.display = 'none';
        }

        // Sky & Fog Crossfade over x in [435, 445] when z in [-40, 40]
        if (pz >= -40 && pz <= 40) {
          let tCross = 0;
          if (px <= 435) tCross = 0;
          else if (px >= 445) tCross = 1;
          else tCross = (px - 435) / 10.0;

          const colDreamBg = new THREE.Color(0xc48958);
          const colRealityBg = new THREE.Color(0x3b4541);
          scene.background = colDreamBg.clone().lerp(colRealityBg, tCross);

          const colDreamFog = new THREE.Color(0xb88658);
          const colRealityFog = new THREE.Color(0x525c58);
          scene.fog.color = colDreamFog.clone().lerp(colRealityFog, tCross);
          scene.fog.near = THREE.MathUtils.lerp(45, 25, tCross);
          scene.fog.far = THREE.MathUtils.lerp(190, 95, tCross);

          ambientLight.color = new THREE.Color(0xf2c499).lerp(new THREE.Color(0xd5dbd8), tCross);
          dirLight.color = new THREE.Color(0xffd699).lerp(new THREE.Color(0xe4e9e8), tCross);
        } else {
          scene.background.setHex(0xc48958);
          scene.fog.color.setHex(0xb88658);
          scene.fog.near = 45;
          scene.fog.far = 190;
          ambientLight.color.setHex(0xf2c499);
          dirLight.color.setHex(0xffd699);
        }
      }

      // 3. Movement & Physics
      if (STATE.isReady && !STATE.isFading && !STATE.isCaughtFading) {
        let moveX = 0;
        let moveZ = 0;
        if (keys.KeyW || keys.ArrowUp) moveZ += 1;
        if (keys.KeyS || keys.ArrowDown) moveZ -= 1;
        if (keys.KeyA || keys.ArrowLeft) moveX += 1;
        if (keys.KeyD || keys.ArrowRight) moveX -= 1;

        const isMoving = (moveX !== 0 || moveZ !== 0);
        const waterCheck = checkWaterAt(STATE.player.pos[0], STATE.player.pos[2]);
        STATE.player.wading = waterCheck.inWater;

        let maxWalkSpeed = 4.0;
        if (STATE.realm === "reality") {
          maxWalkSpeed = 2.0;
        } else if (STATE.player.wading) {
          maxWalkSpeed = 4.0 * STATE.wadeFactor; // 0.35x = 1.4 units/sec!
        }

        if (isMoving) {
          const moveLen = Math.hypot(moveX, moveZ);
          const dirX = moveX / moveLen;
          const dirZ = moveZ / moveLen;

          const targetRot = Math.atan2(dirX, dirZ);
          let rotDiff = targetRot - STATE.player.rotation;
          while (rotDiff > Math.PI) rotDiff -= Math.PI * 2;
          while (rotDiff < -Math.PI) rotDiff += Math.PI * 2;
          STATE.player.rotation += rotDiff * Math.min(dt * 12.0, 1.0);
          STATE.player.targetSpeed = maxWalkSpeed;
        } else {
          STATE.player.targetSpeed = 0;
        }

        STATE.player.speed = THREE.MathUtils.lerp(STATE.player.speed, STATE.player.targetSpeed, dt * 10.0);

        if (STATE.player.speed > 0.05) {
          const forwardX = Math.sin(STATE.player.rotation);
          const forwardZ = Math.cos(STATE.player.rotation);

          let nextX = STATE.player.pos[0] + forwardX * STATE.player.speed * dt;
          let nextZ = STATE.player.pos[2] + forwardZ * STATE.player.speed * dt;

          let canMove = false;
          if (STATE.realm === "reality") {
            const testY = getMeadowElevation(nextX, nextZ);
            if (testY < 3.8 && nextX >= 8 && nextX <= 62 && nextZ >= -34 && nextZ <= 34) {
              canMove = true;
            }
          } else {
            // Dream boundary checks
            const testY = getGrasslandElevation(nextX, nextZ);
            let blockedByVeil1 = (STATE.veil1 !== "dissolved" && nextX >= 200.0 && STATE.player.pos[0] < 200.0);
            let blockedByVeil2 = (STATE.veil2 !== "dissolved" && nextX >= 330.0 && STATE.player.pos[0] < 330.0);
            let blockedByRocks = (STATE.rocks === "blocking" && nextX >= 409.5 && STATE.player.pos[0] < 409.5);

            let inWalkableCorridor = true;
            if (nextX >= 330 && nextX <= 410) {
              if (Math.abs(nextZ) > 11.5) inWalkableCorridor = false;
            }

            if (!blockedByVeil1 && !blockedByVeil2 && !blockedByRocks && inWalkableCorridor) {
              if (testY < 5.0 && nextX >= 6 && nextX <= 475 && nextZ >= -98 && nextZ <= 98) {
                canMove = true;
              }
            }
          }

          if (canMove) {
            STATE.player.pos[0] = nextX;
            STATE.player.pos[2] = nextZ;
          }

          STATE.player.stepCycle += dt * (STATE.player.speed * 3.5);

          if (STATE.player.wading) {
            rippleTimer += dt;
            if (rippleTimer >= 0.4) {
              rippleTimer = 0;
              spawnRipple(STATE.player.pos[0], STATE.player.pos[1], STATE.player.pos[2]);
            }
          }
        } else {
          if (STATE.player.wading) {
            rippleTimer += dt;
            if (rippleTimer >= 0.4) {
              rippleTimer = 0;
              spawnRipple(STATE.player.pos[0], STATE.player.pos[1], STATE.player.pos[2]);
            }
          } else {
            rippleTimer = 0;
          }
        }
      }

      STATE.player.pos[1] = getCurrentElevation(STATE.player.pos[0], STATE.player.pos[2]);
      niulai.root.position.set(STATE.player.pos[0], STATE.player.pos[1], STATE.player.pos[2]);

      const terrainNorm = getCurrentNormal(STATE.player.pos[0], STATE.player.pos[2]);
      const forwardDir = new THREE.Vector3(Math.sin(STATE.player.rotation), 0, Math.cos(STATE.player.rotation));
      const rightDir = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), forwardDir).normalize();
      const adjustedForward = new THREE.Vector3().crossVectors(rightDir, terrainNorm).normalize();
      const calfMatrix = new THREE.Matrix4().makeBasis(rightDir, terrainNorm, adjustedForward);
      niulai.root.quaternion.setFromRotationMatrix(calfMatrix);

      const walkT = STATE.player.stepCycle;
      const legSwing = Math.sin(walkT) * Math.min(STATE.player.speed / 2.0, 1.0) * 0.75;

      let wobbleRoll = 0;
      let wobbleYaw = 0;
      if (STATE.realm === "reality") {
        if (STATE.player.speed > 0.1) {
          wobbleRoll = Math.sin(walkT * 1.5) * 0.18;
          wobbleYaw = Math.cos(walkT * 1.0) * 0.12;
        } else {
          wobbleRoll = Math.sin(STATE.elapsedTime * 6.0) * 0.04;
        }
      }

      niulai.body.rotation.z = wobbleRoll;
      niulai.body.rotation.y = wobbleYaw;

      niulai.legFL.rotation.x = legSwing + (STATE.realm === "reality" ? wobbleRoll * 0.5 : 0);
      niulai.legBR.rotation.x = legSwing - (STATE.realm === "reality" ? wobbleRoll * 0.5 : 0);
      niulai.legFR.rotation.x = -legSwing - (STATE.realm === "reality" ? wobbleRoll * 0.5 : 0);
      niulai.legBL.rotation.x = -legSwing + (STATE.realm === "reality" ? wobbleRoll * 0.5 : 0);

      const breath = Math.sin(STATE.elapsedTime * 2.5) * 0.04;
      niulai.body.scale.set(1 + breath * 0.5, 1 + breath, 1);
      niulai.headGroup.position.y = 1.25 + breath * 0.4;
      niulai.headGroup.rotation.x = (STATE.player.speed > 0.5) ? -0.1 : (breath * 0.5);
      niulai.tailPivot.rotation.z = Math.sin(STATE.elapsedTime * 4.0) * 0.35 + (STATE.player.speed > 0.5 ? Math.sin(walkT * 2.0) * 0.4 : 0);

      if (STATE.realm === "reality") {
        larkModel.headGroup.rotation.y = Math.sin(STATE.elapsedTime * 1.5) * 0.35;
        larkModel.tail.rotation.x = -0.3 + Math.sin(STATE.elapsedTime * 5.0) * 0.08;
      }

      // 4. Memory Triggers & Interactions
      // Memory 1: Reality Flat Rock at (35, -20)
      if (STATE.realm === "reality" && !STATE.memories.meadow) {
        const distToRock = Math.hypot(STATE.player.pos[0] - 35, STATE.player.pos[2] - (-20));
        if (distToRock <= 4.0) {
          STATE.memories.meadow = true;
          STATE.memories.count = 1;
          STATE.log.push({ memory: "meadow", time: formatTime(STATE.elapsedTime) });
          hudMemories.textContent = `Memories: ${STATE.memories.count}/6`;
          meadowRingMat.opacity = 0.25;
          showStoryBanner("Niulai is too tired to stand. A lark from the desert lands beside him, and together they sink into a long dream.");
          transitionToDream();
        }
      }

      // Dream Memories:
      if (STATE.realm === "dream") {
        // Memory 2: Rocky Hollow at (95, 15)
        const distToHollow = Math.hypot(STATE.player.pos[0] - 95, STATE.player.pos[2] - 15);
        if (distToHollow <= 4.0 && !STATE.memories.hollow) {
          STATE.memories.hollow = true;
          STATE.memories.count = 2;
          STATE.log.push({ memory: "hollow", time: formatTime(STATE.elapsedTime) });
          hudMemories.textContent = `Memories: ${STATE.memories.count}/6`;
          showStoryBanner("In a rocky hollow, Niulai meets Bola, an orphaned leopard cub. Born enemies become friends.");
          STATE.bola.state = "following";
          setBolaPose("standing");
          storyRingMat3.opacity = 0.75;
        }

        // Memory 3: Far Bank of Stream at (130, 44). Inert until hollow fired!
        const distToFord = Math.hypot(STATE.player.pos[0] - 130, STATE.player.pos[2] - 44);
        if (distToFord <= 4.0 && STATE.memories.hollow && !STATE.memories.ford) {
          STATE.memories.ford = true;
          STATE.memories.count = 3;
          STATE.log.push({ memory: "ford", time: formatTime(STATE.elapsedTime) });
          hudMemories.textContent = `Memories: ${STATE.memories.count}/6`;
          showStoryBanner("Niulai fears the water. With Bola watching from the reeds, he crosses the stream for the first time.");
          // Trigger Veil 1 dissolve!
          STATE.veil1 = "dissolving";
        }

        // Memory 4: Withering Steppe at (210, 0), radius 5.0
        const distToSteppe = Math.hypot(STATE.player.pos[0] - 210, STATE.player.pos[2] - 0);
        if (distToSteppe <= 5.0 && STATE.memories.ford && !STATE.memories.steppe) {
          STATE.memories.steppe = true;
          STATE.memories.count = 4;
          STATE.log.push({ memory: "steppe", time: formatTime(STATE.elapsedTime) });
          hudMemories.textContent = `Memories: ${STATE.memories.count}/6`;
          showStoryBanner("The grass withers under a merciless sky. The herd must leave for distant water.");
          // Trigger Veil 2 dissolve!
          STATE.veil2 = "dissolving";
        }

        // Memory 5: Canyon Entrance at (336, 0), radius 5.0
        const distToCanyon = Math.hypot(STATE.player.pos[0] - 336, STATE.player.pos[2] - 0);
        if (distToCanyon <= 5.0 && STATE.memories.steppe && !STATE.memories.canyon) {
          STATE.memories.canyon = true;
          STATE.memories.count = 5;
          STATE.log.push({ memory: "canyon", time: formatTime(STATE.elapsedTime) });
          hudMemories.textContent = `Memories: ${STATE.memories.count}/6`;
          showStoryBanner("Yellow eyes prowl the shadows. Niulai keeps to the light, and keeps walking.");
        }

        // Memory 6: Mother's Niche at (404, -8), radius 4.0. Inert until Mother has lain down!
        const distToNiche = Math.hypot(STATE.player.pos[0] - 404, STATE.player.pos[2] - (-8));
        if (distToNiche <= 4.0 && STATE.memories.canyon && STATE.motherLainDown && !STATE.memories.niche) {
          STATE.memories.niche = true;
          STATE.memories.count = 6;
          STATE.log.push({ memory: "niche", time: formatTime(STATE.elapsedTime) });
          hudMemories.textContent = `Memories: ${STATE.memories.count}/6`;
          showStoryBanner("Mother shields the calf with her body. She does not leave the canyon.");

          // Two nearest wolves (W3 and W4) retreat and vanish
          STATE.wolves[2].retreating = true; // W3
          STATE.wolves[3].retreating = true; // W4

          // Fallen rocks sink into ground over 0.8s
          STATE.rocks = "lowering";
        }

        // Interaction Circle 7: Dream's Edge Copy Slab Rock at (445, -20), radius 2.5
        const distToCopyRock = Math.hypot(STATE.player.pos[0] - 445, STATE.player.pos[2] - (-20));
        if (distToCopyRock <= 2.5) {
          hudRestPrompt.style.display = 'block';
        } else {
          hudRestPrompt.style.display = 'none';
        }

        // Subsystem updates in Dream
        updateBolaCompanion(dt);
        updateGrassSnake(dt);
        updateHerd(STATE.elapsedTime, dt);
        updateWolves(dt);
        updateLarkGuide(STATE.elapsedTime, dt);
        updateDustMotes(STATE.elapsedTime);
        updateRipples(dt);
      }

      // 5. Follow Camera
      const calfPos = niulai.root.position;
      let yawDiff = STATE.player.rotation - cameraYaw;
      while (yawDiff > Math.PI) yawDiff -= Math.PI * 2;
      while (yawDiff < -Math.PI) yawDiff += Math.PI * 2;
      cameraYaw += yawDiff * Math.min(dt * 3.5, 1.0);

      // Camera pulls in to 3.0 units inside Wolf Pass (x in [330, 410])
      let camDistBack = 5.5;
      if (STATE.realm === "dream" && STATE.player.pos[0] >= 330 && STATE.player.pos[0] <= 410) {
        camDistBack = 3.0;
      }
      const camHeightAbove = 2.2;

      let idealCamX = calfPos.x - Math.sin(cameraYaw) * camDistBack;
      let idealCamZ = calfPos.z - Math.cos(cameraYaw) * camDistBack;
      let idealCamY = calfPos.y + camHeightAbove;

      // In Wolf Pass corridor, clamp camera Z to avoid clipping into rock walls
      if (STATE.realm === "dream" && idealCamX >= 330 && idealCamX <= 410) {
        idealCamZ = Math.max(-10.8, Math.min(10.8, idealCamZ));
      }

      const groundAtCam = getCurrentElevation(idealCamX, idealCamZ);
      if (idealCamY < groundAtCam + 0.85) idealCamY = groundAtCam + 0.85;

      camera.position.x = THREE.MathUtils.lerp(camera.position.x, idealCamX, Math.min(dt * 8.0, 1.0));
      camera.position.y = THREE.MathUtils.lerp(camera.position.y, idealCamY, Math.min(dt * 8.0, 1.0));
      camera.position.z = THREE.MathUtils.lerp(camera.position.z, idealCamZ, Math.min(dt * 8.0, 1.0));

      const lookTarget = new THREE.Vector3(
        calfPos.x + Math.sin(STATE.player.rotation) * 1.5,
        calfPos.y + 1.1,
        calfPos.z + Math.cos(STATE.player.rotation) * 1.5
      );
      camera.lookAt(lookTarget);

      // 6. State export
      updateArenaState();

      // Render
      renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    requestAnimationFrame(animate);
    updateArenaState();

  })();
  </script>
</body>
</html>
"""
