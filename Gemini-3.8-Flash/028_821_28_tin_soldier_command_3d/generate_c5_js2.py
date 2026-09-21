# -*- coding: utf-8 -*-
import sys

out = []

out.append('''    // --- Toybox Barracks & Rally Point ---
    const barracksGroup = new THREE.Group();
    barracksGroup.position.set(-8.5, 0, 14.0);

    const tbBodyGeo = new THREE.BoxGeometry(3.6, 1.8, 2.6);
    const tbBodyMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.5, metalness: 0.1 });
    const tbBody = new THREE.Mesh(tbBodyGeo, tbBodyMat);
    tbBody.position.y = 0.9;
    tbBody.castShadow = true; tbBody.receiveShadow = true;
    barracksGroup.add(tbBody);

    const tbTrimGeo = new THREE.BoxGeometry(3.8, 0.2, 2.8);
    const tbTrimMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4, metalness: 0.3 });
    const tbTrim = new THREE.Mesh(tbTrimGeo, tbTrimMat);
    tbTrim.position.y = 1.8;
    barracksGroup.add(tbTrim);

    const tbLidGeo = new THREE.BoxGeometry(3.8, 0.2, 2.8);
    const tbLidMat = new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.5 });
    const tbLid = new THREE.Mesh(tbLidGeo, tbLidMat);
    tbLid.position.set(0, 2.5, -1.2);
    tbLid.rotation.x = -Math.PI * 0.35;
    tbLid.castShadow = true;
    barracksGroup.add(tbLid);

    const toySpill1 = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.6, 8), new THREE.MeshStandardMaterial({ color: 0xef4444 }));
    toySpill1.position.set(-0.8, 1.9, 0.9); toySpill1.rotation.z = 0.5; barracksGroup.add(toySpill1);
    const toySpill2 = new THREE.Mesh(new THREE.SphereGeometry(0.28, 8, 8), new THREE.MeshStandardMaterial({ color: 0x10b981 }));
    toySpill2.position.set(0.6, 1.9, 0.8); barracksGroup.add(toySpill2);

    const bSelRingGeo = new THREE.RingGeometry(2.3, 2.5, 32);
    const bSelRingMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide });
    const barracksSelRing = new THREE.Mesh(bSelRingGeo, bSelRingMat);
    barracksSelRing.rotation.x = -Math.PI / 2; barracksSelRing.position.y = 0.04;
    barracksSelRing.visible = false;
    barracksGroup.add(barracksSelRing);

    // Barracks HP Bar
    const bHpBarBg = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 0.24), new THREE.MeshBasicMaterial({ color: 0x0f172a, side: THREE.DoubleSide }));
    bHpBarBg.position.set(0, 3.2, 0); barracksGroup.add(bHpBarBg);
    const bHpFill = new THREE.Mesh(new THREE.PlaneGeometry(2.7, 0.18), new THREE.MeshBasicMaterial({ color: 0x22c55e, side: THREE.DoubleSide }));
    bHpFill.position.set(0, 3.2, 0.01); barracksGroup.add(bHpFill);

    scene.add(barracksGroup);
    barracksGroup.updateMatrixWorld(true);
    const barracksBox = new THREE.Box3().setFromObject(tbBody);
    obstacles.push({ box: barracksBox, isBlock: false, name: 'barracks' });

    const barracks = {
      pos: new THREE.Vector3(-8.5, 0, 14.0),
      spawnPoint: new THREE.Vector3(-8.5, 0, 11.2),
      rallyPoint: new THREE.Vector3(-5.0, 0, 12.0),
      queue: [],
      selected: false,
      box: barracksBox,
      selRing: barracksSelRing,
      hpFill: bHpFill,
      maxHp: 300,
      hp: 300,
      alive: true
    };

    // Visible Rally Flag
    const rallyFlagGroup = new THREE.Group();
    rallyFlagGroup.position.copy(barracks.rallyPoint);
    const flagPole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.6, 8), new THREE.MeshStandardMaterial({ color: 0xd1d5db, metalness: 0.8 }));
    flagPole.position.y = 0.8; flagPole.castShadow = true;
    rallyFlagGroup.add(flagPole);
    const flagCloth = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.6, 3), new THREE.MeshStandardMaterial({ color: 0x3b82f6 }));
    flagCloth.rotation.z = -Math.PI / 2; flagCloth.position.set(0.3, 1.3, 0);
    rallyFlagGroup.add(flagCloth);
    const flagBase = new THREE.Mesh(new THREE.RingGeometry(0.2, 0.4, 16), new THREE.MeshBasicMaterial({ color: 0x60a5fa, side: THREE.DoubleSide }));
    flagBase.rotation.x = -Math.PI / 2; flagBase.position.y = 0.03;
    rallyFlagGroup.add(flagBase);
    scene.add(rallyFlagGroup);

    function setBarracksRally(pos) {
      barracks.rallyPoint.copy(pos);
      rallyFlagGroup.position.copy(pos);
      rallyFlagGroup.visible = true;
    }

    // --- Marble-Run Economy & Depot Pad ---
    const marbleRunGroup = new THREE.Group();
    marbleRunGroup.position.set(12.0, 0, 12.0);

    const mPillar1 = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 4.0, 8), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.4 }));
    mPillar1.position.set(-2.0, 2.0, 0); mPillar1.castShadow = true; marbleRunGroup.add(mPillar1);

    const mPillar2 = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 2.5, 8), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.4 }));
    mPillar2.position.set(0.5, 1.25, 0); mPillar2.castShadow = true; marbleRunGroup.add(mPillar2);

    const railGeo = new THREE.BoxGeometry(4.2, 0.12, 0.6);
    const railMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.7, roughness: 0.2 });
    const railMesh = new THREE.Mesh(railGeo, railMat);
    railMesh.position.set(-0.8, 2.6, 0);
    railMesh.rotation.z = -0.32;
    railMesh.castShadow = true;
    marbleRunGroup.add(railMesh);

    const bowlGeo = new THREE.CylinderGeometry(1.2, 0.8, 0.6, 16);
    const bowlMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.3, metalness: 0.6 });
    const bowlMesh = new THREE.Mesh(bowlGeo, bowlMat);
    bowlMesh.position.set(1.6, 0.3, 0);
    bowlMesh.castShadow = true; bowlMesh.receiveShadow = true;
    marbleRunGroup.add(bowlMesh);

    scene.add(marbleRunGroup);
    marbleRunGroup.updateMatrixWorld(true);
    const marbleRunBox = new THREE.Box3().setFromObject(marbleRunGroup);
    obstacles.push({ box: marbleRunBox, isBlock: false, name: 'marbleRun' });

    const bowlWorldPos = new THREE.Vector3(13.6, 0, 12.0);

    const depotPadGroup = new THREE.Group();
    depotPadGroup.position.set(-2.0, 0.04, 14.0);
    const depotPad = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.3, 0.08, 24), new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.4, metalness: 0.7 }));
    depotPad.receiveShadow = true;
    depotPadGroup.add(depotPad);
    const depotRing = new THREE.Mesh(new THREE.RingGeometry(1.3, 1.9, 24), new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide }));
    depotRing.rotation.x = -Math.PI / 2; depotRing.position.y = 0.05;
    depotPadGroup.add(depotRing);
    scene.add(depotPadGroup);
    const depotWorldPos = new THREE.Vector3(-2.0, 0, 14.0);

    const marbleMat = new THREE.MeshPhysicalMaterial({
      color: 0x06b6d4,
      transmission: 0.85,
      opacity: 1.0,
      transparent: true,
      roughness: 0.1,
      metalness: 0.1,
      ior: 1.5
    });
    function createMarbleMesh() {
      const m = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), marbleMat);
      m.castShadow = true;
      return m;
    }

    const marbleRunState = {
      spawnTimer: 0,
      spawnInterval: 10.0,
      bowlCount: 0,
      maxBowlCount: 5,
      bowlMarbles: [],
      rollingMarbles: [],
      droppedMarbles: []
    };

    // --- Cork Projectiles System ---
    const corkProjectiles = [];
    const corkGeo = new THREE.CylinderGeometry(0.13, 0.13, 0.32, 8);
    const corkMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.85, metalness: 0.05 });

    function spawnBallisticCork(startPos, targetPos, damage, isPlayerShot, shooter) {
      const mesh = new THREE.Mesh(corkGeo, corkMat);
      mesh.castShadow = true;
      mesh.position.copy(startPos);
      scene.add(mesh);

      const dx = targetPos.x - startPos.x;
      const dz = targetPos.z - startPos.z;
      const d = Math.max(0.1, Math.hypot(dx, dz));
      const dy = targetPos.y - startPos.y;

      let V0 = CORK_SPEED;
      const g = GRAVITY;
      let term = V0 * V0 * V0 * V0 - g * (2.0 * dy * V0 * V0 + g * d * d);
      if (term < 0) {
        V0 = Math.sqrt(g * (d + Math.max(0, dy))) + 1.0;
        term = Math.max(0, V0 * V0 * V0 * V0 - g * (2.0 * dy * V0 * V0 + g * d * d));
      }

      const tanTheta = (V0 * V0 - Math.sqrt(term)) / (g * d);
      const theta = Math.atan(tanTheta);
      const vh = V0 * Math.cos(theta);
      const vy = V0 * Math.sin(theta);
      const vx = vh * (dx / d);
      const vz = vh * (dz / d);

      const flightEst = d / Math.max(0.1, vh);

      corkProjectiles.push({
        mesh: mesh,
        pos: startPos.clone(),
        vel: new THREE.Vector3(vx, vy, vz),
        damage: damage,
        isPlayerShot: isPlayerShot,
        shooter: shooter,
        alive: true,
        age: 0,
        maxLife: flightEst + 0.8
      });
      playSfx('shot');
    }

    // --- Lobbed Catapult Marbles ---
    const lobbedMarbles = [];
    function spawnLobbedMarble(startPos, targetGroundPos) {
      const mesh = createMarbleMesh();
      mesh.position.copy(startPos);
      scene.add(mesh);

      const dx = targetGroundPos.x - startPos.x;
      const dz = targetGroundPos.z - startPos.z;
      const d = Math.max(0.1, Math.hypot(dx, dz));
      const dy = targetGroundPos.y - startPos.y;

      const T = 1.35;
      const vx = dx / T;
      const vz = dz / T;
      const vy = (dy + 0.5 * GRAVITY * T * T) / T;

      lobbedMarbles.push({
        mesh: mesh,
        pos: startPos.clone(),
        vel: new THREE.Vector3(vx, vy, vz),
        targetPos: targetGroundPos.clone(),
        alive: true,
        age: 0,
        maxLife: T + 0.15
      });
      playSfx('catapult');
    }

    function triggerCatapultExplosion(impactPos) {
      playSfx('hit');
      const blastRing = new THREE.Mesh(
        new THREE.RingGeometry(0.2, 2.5, 24),
        new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.8 })
      );
      blastRing.rotation.x = -Math.PI / 2;
      blastRing.position.set(impactPos.x, 0.05, impactPos.z);
      scene.add(blastRing);
      setTimeout(() => scene.remove(blastRing), 400);

      // Damage outposts
      outposts.forEach(op => {
        if (op.alive && op.pos.distanceTo(impactPos) <= 2.5 + 1.2) {
          op.hp = Math.max(0, op.hp - 30);
          if (op.hp <= 0) destroyOutpost(op);
        }
      });

      // Damage patrols
      enemyPatrols.forEach(sq => {
        if (!sq.alive) return;
        sq.soldiers.forEach(sol => {
          if (sol.alive && sol.pos.distanceTo(impactPos) <= 2.5 + 0.5) {
            sol.hp = Math.max(0, sol.hp - 30);
            if (sol.hp <= 0) destroyPatrolSoldier(sol, sq);
          }
        });
      });

      // Damage assault wave soldiers
      assaultWaveSoldiers.forEach(sol => {
        if (sol.alive && sol.pos.distanceTo(impactPos) <= 2.5 + 0.5) {
          sol.hp = Math.max(0, sol.hp - 30);
          if (sol.hp <= 0) destroyWaveSoldier(sol);
        }
      });

      // Damage player soldiers
      playerSoldiers.forEach(s => {
        if (s.alive && s.pos.distanceTo(impactPos) <= 2.5 + 0.5) {
          s.hp = Math.max(0, s.hp - 30);
          if (s.hp <= 0) destroyPlayerSoldier(s);
        }
      });

      // Damage & topple wooden blocks
      woodenBlocks.forEach(b => {
        const center2D = new THREE.Vector2(b.mesh.position.x, b.mesh.position.z);
        const impact2D = new THREE.Vector2(impactPos.x, impactPos.z);
        if (center2D.distanceTo(impact2D) <= 2.5) {
          displaceBlock(b, impactPos);
        }
      });

      // Physical force topples standing domino tiles within radius 2.5!
      dominoWalls.forEach(wall => {
        wall.tiles.forEach(tile => {
          if (tile.alive && tile.state === 'standing') {
            const d = tile.pos.distanceTo(impactPos);
            if (d <= 2.5) {
              const pushDir = new THREE.Vector3().subVectors(tile.pos, impactPos);
              pushDir.y = 0;
              if (pushDir.lengthSq() < 0.001) pushDir.set(wall.tangent.x, 0, wall.tangent.z);
              pushDir.normalize();
              toppleDominoTile(tile, pushDir);
            }
          }
        });
      });
    }
''')

with open('c5_part3.js', 'w') as f:
    f.write(''.join(out))
print("Part 3 written")
