# -*- coding: utf-8 -*-
import sys

out = []

out.append('''    // --- Domino Walls & Night-light Towers Structures ---
    const dominoWalls = []; // { id, tiles, tangent }
    const nightLightTowers = []; // { id, root, pos, hp, maxHp, bulbLight, auraMesh, alive }

    const dominoTileGeo = new THREE.BoxGeometry(0.38, 0.72, 0.16);
    const dominoTileMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.35, metalness: 0.1 });
    const dominoDotMat = new THREE.MeshBasicMaterial({ color: 0x0f172a });

    function createDominoTileMesh() {
      const g = new THREE.Group();
      const body = new THREE.Mesh(dominoTileGeo, dominoTileMat);
      body.castShadow = true; body.receiveShadow = true;
      g.add(body);
      const dot = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.02, 8), dominoDotMat);
      dot.rotation.x = Math.PI / 2; dot.position.set(0, 0.18, 0.09);
      g.add(dot);
      return g;
    }

    function createDominoWall(startPt, endPt) {
      const dir = new THREE.Vector3().subVectors(endPt, startPt);
      dir.y = 0;
      const totalLen = dir.length();
      if (totalLen < 0.5) return;
      dir.normalize();

      const spacing = 0.55;
      const numTiles = Math.max(1, Math.floor(totalLen / spacing) + 1);
      const totalCost = numTiles * 5;

      if (bottlecaps < totalCost) return;
      bottlecaps -= totalCost;
      playSfx('build');

      const wall = {
        id: nextTileId++,
        tangent: dir.clone(),
        tiles: []
      };

      const wallYaw = Math.atan2(dir.x, dir.z);

      for (let i = 0; i < numTiles; i++) {
        const tPos = startPt.clone().addScaledVector(dir, i * spacing);
        tPos.y = 0.36; // half height

        const mesh = createDominoTileMesh();
        mesh.position.copy(tPos);
        mesh.rotation.y = wallYaw;
        scene.add(mesh);
        mesh.updateMatrixWorld(true);

        const box = new THREE.Box3().setFromObject(mesh);
        const tile = {
          wall: wall,
          index: i,
          mesh: mesh,
          pos: new THREE.Vector3(tPos.x, 0, tPos.z),
          box: box,
          hp: 20,
          maxHp: 20,
          state: 'standing', // 'standing', 'falling', 'fallen'
          fallTimer: 0,
          toppleDir: null,
          alive: true
        };
        wall.tiles.push(tile);
        // Standing tiles block movement and corks
        obstacles.push({ box: box, isBlock: false, isDomino: true, tile: tile });
      }

      dominoWalls.push(wall);
    }

    // Physical force domino topple chain
    function toppleDominoTile(tile, pushDir) {
      if (!tile.alive || tile.state !== 'standing') return;
      tile.state = 'falling';
      tile.fallTimer = 0.25;

      // Determine forward or backward along wall tangent
      const dot = pushDir.dot(tile.wall.tangent);
      const chainStep = (dot >= 0) ? 1 : -1;
      const effDir = tile.wall.tangent.clone().multiplyScalar(chainStep);
      tile.toppleDir = effDir;

      // Animate tipping over in direction of push
      playSfx('domino');
      tile.mesh.position.y = 0.1;
      const pitchAxis = new THREE.Vector3(-effDir.z, 0, effDir.x);
      tile.mesh.rotateOnWorldAxis(pitchAxis, Math.PI * 0.44);
      tile.mesh.updateMatrixWorld(true);

      // Deals 15 damage to any unit standing where tile falls
      const fallImpactPos = tile.pos.clone().addScaledVector(effDir, 0.45);
      dealDominoCrushDamage(fallImpactPos);

      // Remove from obstacles: low ramp units can walk over, corks pass through
      removeDominoFromObstacles(tile);

      // Schedule chain reaction after 0.25s
      setTimeout(() => {
        if (!tile.alive) return;
        tile.state = 'fallen';
        const nextIdx = tile.index + chainStep;
        if (nextIdx >= 0 && nextIdx < tile.wall.tiles.length) {
          const nextTile = tile.wall.tiles[nextIdx];
          if (nextTile && nextTile.alive && nextTile.state === 'standing') {
            toppleDominoTile(nextTile, effDir);
          }
        }
      }, 250);
    }

    function removeDominoFromObstacles(tile) {
      const idx = obstacles.findIndex(obs => obs.tile === tile);
      if (idx !== -1) {
        obstacles.splice(idx, 1);
      }
    }

    function dealDominoCrushDamage(pos) {
      // 15 damage to any unit within 0.45 units
      playerSoldiers.forEach(s => {
        if (s.alive && s.pos.distanceTo(pos) <= 0.6) {
          s.hp = Math.max(0, s.hp - 15);
          playSfx('hit');
          if (s.hp <= 0) destroyPlayerSoldier(s);
        }
      });
      outposts.forEach(op => {
        if (op.alive && op.pos.distanceTo(pos) <= 1.2) {
          op.hp = Math.max(0, op.hp - 15);
          if (op.hp <= 0) destroyOutpost(op);
        }
      });
      enemyPatrols.forEach(sq => {
        if (!sq.alive) return;
        sq.soldiers.forEach(sol => {
          if (sol.alive && sol.pos.distanceTo(pos) <= 0.6) {
            sol.hp = Math.max(0, sol.hp - 15);
            playSfx('hit');
            if (sol.hp <= 0) destroyPatrolSoldier(sol, sq);
          }
        });
      });
      assaultWaveSoldiers.forEach(sol => {
        if (sol.alive && sol.pos.distanceTo(pos) <= 0.6) {
          sol.hp = Math.max(0, sol.hp - 15);
          playSfx('hit');
          if (sol.hp <= 0) destroyWaveSoldier(sol);
        }
      });
    }

    function destroyDominoTileByGunfire(tile) {
      tile.alive = false;
      scene.remove(tile.mesh);
      removeDominoFromObstacles(tile);
    }

    // --- Night-light Towers ---
    // 40 caps, max 3 towers. Toy lamp with glowing bulb head casting radius 7 light circle.
    // 100 HP. Effects inside circle: enemies move at x0.7 speed, friendly riflemen fire at 1.2s instead of 1.5s. Overlaps do not stack.
    function buildNightLightTower(groundPt) {
      if (nightLightTowers.length >= 3 || bottlecaps < 40) return;
      bottlecaps -= 40;
      playSfx('build');

      const root = new THREE.Group();
      root.position.copy(groundPt);

      // Lamp base
      const tBase = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.8, 0.2, 16), new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.5, roughness: 0.4 }));
      tBase.position.y = 0.1; tBase.castShadow = true; root.add(tBase);

      // Lamp shaft
      const tShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 2.2, 8), new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.7, roughness: 0.2 }));
      tShaft.position.y = 1.2; tShaft.castShadow = true; root.add(tShaft);

      // Lamp shade & bulb head
      const tShade = new THREE.Mesh(new THREE.ConeGeometry(0.75, 0.6, 12, 1, true), new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.5, side: THREE.DoubleSide }));
      tShade.position.y = 2.4; root.add(tShade);

      const bulbGeo = new THREE.SphereGeometry(0.3, 12, 12);
      const bulbMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
      const bulb = new THREE.Mesh(bulbGeo, bulbMat);
      bulb.position.y = 2.25; root.add(bulb);

      // PointLight on bulb
      const bulbLight = new THREE.PointLight(0xfef08a, 1.4, 10, 1.5);
      bulbLight.position.y = 2.3; root.add(bulbLight);

      // Visible warm light circle of radius 7 on floor
      const auraGeo = new THREE.RingGeometry(0.2, TOWER_RADIUS, 36);
      const auraMat = new THREE.MeshBasicMaterial({ color: 0xfef08a, side: THREE.DoubleSide, transparent: true, opacity: 0.12, depthWrite: false });
      const auraMesh = new THREE.Mesh(auraGeo, auraMat);
      auraMesh.rotation.x = -Math.PI / 2;
      auraMesh.position.y = 0.02;
      root.add(auraMesh);

      // HP Bar
      const hpBarBg = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.14), new THREE.MeshBasicMaterial({ color: 0x0f172a, side: THREE.DoubleSide }));
      hpBarBg.position.set(0, 3.0, 0); root.add(hpBarBg);
      const hpFill = new THREE.Mesh(new THREE.PlaneGeometry(1.14, 0.1), new THREE.MeshBasicMaterial({ color: 0x22c55e, side: THREE.DoubleSide }));
      hpFill.position.set(0, 3.0, 0.01); root.add(hpFill);

      scene.add(root);
      root.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(tBase);
      box.max.y = 2.8;

      const tower = {
        id: nextTowerId++,
        root: root,
        pos: new THREE.Vector3(groundPt.x, 0, groundPt.z),
        box: box,
        hp: 100,
        maxHp: 100,
        hpFill: hpFill,
        alive: true
      };

      nightLightTowers.push(tower);
      obstacles.push({ box: box, isBlock: false, isTower: true, tower: tower });
    }

    function destroyTower(tower) {
      tower.alive = false;
      scene.remove(tower.root);
      const idx = nightLightTowers.indexOf(tower);
      if (idx !== -1) nightLightTowers.splice(idx, 1);
      const obsIdx = obstacles.findIndex(obs => obs.tower === tower);
      if (obsIdx !== -1) obstacles.splice(obsIdx, 1);
    }

    function isInsideAnyTowerRadius(pos) {
      for (let i = 0; i < nightLightTowers.length; i++) {
        const t = nightLightTowers[i];
        if (t.alive && t.pos.distanceTo(pos) <= TOWER_RADIUS) {
          return true;
        }
      }
      return false;
    }
''')

with open('c5_part4.js', 'w') as f:
    f.write(''.join(out))
print("Part 4 written")
