# Part 4: Foliage, Steppe, Veils, Canyon, and Meadow Copy
part4 = r"""
    // =========================================================
    // 4. FOLIAGE & PROPS (Grassland, Steppe, Canyon, Dream's Edge)
    // =========================================================
    resetPRNG(4242);
    const trunkMat = new THREE.MeshPhongMaterial({ color: 0x75523a, flatShading: true });
    const foliageMat = new THREE.MeshPhongMaterial({ color: 0x488a44, flatShading: true });
    const fruitMat = new THREE.MeshPhongMaterial({ color: 0xf6be28, flatShading: true, emissive: 0x2e2000 });
    const rockMat = new THREE.MeshPhongMaterial({ color: 0x888b83, flatShading: true });
    const flowerMat = new THREE.MeshPhongMaterial({ color: 0xffdf40, flatShading: true });
    const reedMat = new THREE.MeshPhongMaterial({ color: 0x587a38, flatShading: true });

    // Grassland Trees: 44 total, 6 fruit trees
    const TOTAL_TREES = 44;
    const treePositions = [];
    const fruitTreeIndices = new Set([3, 11, 19, 27, 34, 41]);

    let attempts = 0;
    while (treePositions.length < TOTAL_TREES && attempts < 1500) {
      attempts++;
      const tx = 26 + deterministicRandom() * 142;
      const tz = -85 + deterministicRandom() * 170;
      const streamX = getStreamCenter(tz);
      if (Math.abs(tx - streamX) < 5.0) continue;
      if (Math.hypot(tx - 95, tz - 15) < 7.5) continue;
      if (Math.hypot(tx - 130, tz - 44) < 7.5) continue;
      if (Math.hypot(tx - 10, tz - 0) < 6.0) continue;

      let tooClose = false;
      for (let p of treePositions) {
        if (Math.hypot(tx - p.x, tz - p.z) < 9.2) {
          tooClose = true;
          break;
        }
      }
      if (tooClose) continue;
      treePositions.push({ x: tx, z: tz });
    }

    const trunkGeo = new THREE.CylinderGeometry(0.35, 0.55, 3.2, 7);
    trunkGeo.translate(0, 1.6, 0);
    const trunkInstancedMesh = new THREE.InstancedMesh(trunkGeo, trunkMat, TOTAL_TREES);

    const crownData = [];
    const fruitData = [];
    const dummy = new THREE.Object3D();

    treePositions.forEach((pos, idx) => {
      const isFruitTree = fruitTreeIndices.has(idx);
      const ty = getGrasslandElevation(pos.x, pos.z);
      const treeScale = 0.85 + deterministicRandom() * 0.45;

      dummy.position.set(pos.x, ty, pos.z);
      dummy.rotation.set(0, deterministicRandom() * Math.PI * 2, 0);
      dummy.scale.set(treeScale, treeScale, treeScale);
      dummy.updateMatrix();
      trunkInstancedMesh.setMatrixAt(idx, dummy.matrix);

      const sphereCount = 3 + Math.floor(deterministicRandom() * 3);
      const sphereOffsets = [
        { ox: 0, oy: 3.2 * treeScale, oz: 0, r: 1.8 * treeScale },
        { ox: 0.9 * treeScale, oy: 3.6 * treeScale, oz: 0.5 * treeScale, r: 1.4 * treeScale },
        { ox: -0.8 * treeScale, oy: 3.5 * treeScale, oz: -0.4 * treeScale, r: 1.3 * treeScale },
        { ox: 0.2 * treeScale, oy: 4.4 * treeScale, oz: -0.3 * treeScale, r: 1.2 * treeScale },
        { ox: -0.4 * treeScale, oy: 4.1 * treeScale, oz: 0.8 * treeScale, r: 1.1 * treeScale }
      ];

      for (let s = 0; s < sphereCount; s++) {
        const off = sphereOffsets[s];
        crownData.push({
          x: pos.x + off.ox,
          y: ty + off.oy,
          z: pos.z + off.oz,
          scale: off.r
        });
      }

      if (isFruitTree) {
        const fruitCount = 5 + Math.floor(deterministicRandom() * 4);
        for (let f = 0; f < fruitCount; f++) {
          const angle = (f / fruitCount) * Math.PI * 2 + deterministicRandom() * 0.5;
          const dist = 1.35 * treeScale + deterministicRandom() * 0.35;
          const fy = ty + (3.1 + deterministicRandom() * 1.3) * treeScale;
          fruitData.push({
            x: pos.x + Math.cos(angle) * dist,
            y: fy,
            z: pos.z + Math.sin(angle) * dist,
            scale: 0.22 * treeScale
          });
        }
      }
    });

    trunkInstancedMesh.instanceMatrix.needsUpdate = true;
    dreamGroup.add(trunkInstancedMesh);

    const crownSphereGeo = new THREE.SphereGeometry(1, 7, 6);
    const crownInstancedMesh = new THREE.InstancedMesh(crownSphereGeo, foliageMat, crownData.length);
    crownData.forEach((cd, i) => {
      dummy.position.set(cd.x, cd.y, cd.z);
      dummy.rotation.set(0, 0, 0);
      dummy.scale.set(cd.scale, cd.scale * 0.95, cd.scale);
      dummy.updateMatrix();
      crownInstancedMesh.setMatrixAt(i, dummy.matrix);
    });
    crownInstancedMesh.instanceMatrix.needsUpdate = true;
    dreamGroup.add(crownInstancedMesh);

    const fruitGeo = new THREE.SphereGeometry(1, 6, 5);
    const fruitInstancedMesh = new THREE.InstancedMesh(fruitGeo, fruitMat, fruitData.length);
    fruitData.forEach((fd, i) => {
      dummy.position.set(fd.x, fd.y, fd.z);
      dummy.rotation.set(0, 0, 0);
      dummy.scale.set(fd.scale, fd.scale, fd.scale);
      dummy.updateMatrix();
      fruitInstancedMesh.setMatrixAt(i, dummy.matrix);
    });
    fruitInstancedMesh.instanceMatrix.needsUpdate = true;
    dreamGroup.add(fruitInstancedMesh);

    // Scattered boulders, bushes, flowers, reeds in Grassland
    const rockGeo = new THREE.DodecahedronGeometry(1.0, 0);
    for (let i = 0; i < 28; i++) {
      const rx = 20 + deterministicRandom() * 155;
      const rz = -90 + deterministicRandom() * 180;
      const ry = getGrasslandElevation(rx, rz);
      const boulder = new THREE.Mesh(rockGeo, rockMat);
      const s = 0.8 + deterministicRandom() * 1.5;
      boulder.scale.set(s, s * 0.7, s * 1.2);
      boulder.position.set(rx, ry + s * 0.25, rz);
      boulder.rotation.set(deterministicRandom() * 3, deterministicRandom() * 3, deterministicRandom() * 3);
      dreamGroup.add(boulder);
    }

    // Rocky hollow rim rocks at (95, 15)
    for (let i = 0; i < 9; i++) {
      const angle = (i / 9) * Math.PI * 2;
      const dist = 3.6 + deterministicRandom() * 1.2;
      const hx = 95 + Math.cos(angle) * dist;
      const hz = 15 + Math.sin(angle) * dist;
      const hy = getGrasslandElevation(hx, hz);
      const hRock = new THREE.Mesh(rockGeo, rockMat);
      const s = 0.9 + deterministicRandom() * 0.8;
      hRock.scale.set(s * 1.1, s * 0.65, s * 0.9);
      hRock.position.set(hx, hy + s * 0.2, hz);
      hRock.rotation.set(deterministicRandom() * 2, deterministicRandom() * 3, 0);
      dreamGroup.add(hRock);
    }

    const bushGeo = new THREE.SphereGeometry(0.7, 6, 5);
    const bushMat = new THREE.MeshPhongMaterial({ color: 0x5a9c48, flatShading: true });
    for (let i = 0; i < 45; i++) {
      const bx = 20 + deterministicRandom() * 155;
      const bz = -90 + deterministicRandom() * 180;
      const by = getGrasslandElevation(bx, bz);
      const bush = new THREE.Mesh(bushGeo, bushMat);
      const bs = 0.6 + deterministicRandom() * 0.6;
      bush.scale.set(bs * 1.2, bs * 0.7, bs);
      bush.position.set(bx, by + bs * 0.35, bz);
      dreamGroup.add(bush);
    }

    const flowerGeo = new THREE.CylinderGeometry(0.2, 0.05, 0.35, 5);
    for (let i = 0; i < 80; i++) {
      const fx = 20 + deterministicRandom() * 155;
      const fz = -90 + deterministicRandom() * 180;
      const fy = getGrasslandElevation(fx, fz);
      const fl = new THREE.Mesh(flowerGeo, flowerMat);
      fl.position.set(fx, fy + 0.15, fz);
      fl.rotation.y = deterministicRandom() * Math.PI;
      dreamGroup.add(fl);
    }

    const reedStemGeo = new THREE.CylinderGeometry(0.04, 0.06, 1.8, 4);
    reedStemGeo.translate(0, 0.9, 0);
    const reedHeadGeo = new THREE.CylinderGeometry(0.1, 0.1, 0.45, 5);
    reedHeadGeo.translate(0, 1.6, 0);
    const reedGroup = new THREE.Group();
    for (let i = 0; i < 16; i++) {
      const rx = 127 + deterministicRandom() * 4.5;
      const rz = 41 + deterministicRandom() * 5.0;
      const ry = getGrasslandElevation(rx, rz);
      const singleReed = new THREE.Group();
      singleReed.position.set(rx, ry, rz);
      singleReed.add(new THREE.Mesh(reedStemGeo, reedMat));
      singleReed.add(new THREE.Mesh(reedHeadGeo, trunkMat));
      reedGroup.add(singleReed);
    }
    dreamGroup.add(reedGroup);

    // =========================================================
    // WITHERING STEPPE (x from 200 to 330)
    // =========================================================
    // 1. Grass Tufts on regular 4-unit jittered grid
    // Linear density falloff from 1.0 at x=200 to 0.0 at x=330
    // Color lerps from green to dry straw.
    resetPRNG(987654321);
    const steppeTuftGeo = new THREE.ConeGeometry(0.22, 0.45, 4);
    steppeTuftGeo.translate(0, 0.22, 0);

    const steppeTuftsGroup = new THREE.Group();
    for (let gx = 200; gx <= 330; gx += 4) {
      for (let gz = -90; gz <= 90; gz += 4) {
        const jx = gx + (deterministicRandom() - 0.5) * 3.0;
        const jz = gz + (deterministicRandom() - 0.5) * 3.0;
        const u = Math.max(0, Math.min(1, (jx - 200) / 130.0));
        let density = Math.max(0, 1.0 - u);
        if (jx > 300) density *= Math.max(0, (330 - jx) / 30.0);

        if (deterministicRandom() < density) {
          const gy = getGrasslandElevation(jx, jz);
          const tCol = new THREE.Color(0x73b75d).lerp(new THREE.Color(0xc2a649), u);
          const tMat = new THREE.MeshPhongMaterial({ color: tCol, flatShading: true });
          const tuft = new THREE.Mesh(steppeTuftGeo, tMat);
          tuft.position.set(jx, gy, jz);
          tuft.rotation.y = deterministicRandom() * Math.PI;
          steppeTuftsGroup.add(tuft);
        }
      }
    }
    dreamGroup.add(steppeTuftsGroup);

    // 2. Steppe Trees: crown count = clamp(round(4 - 4*(x-200)/130), 0, 4)
    const steppeTreesGroup = new THREE.Group();
    for (let i = 0; i < 30; i++) {
      const tx = 208 + deterministicRandom() * 115;
      const tz = -80 + deterministicRandom() * 160;
      if (Math.abs(tz - (-20)) < 4.0) continue; // avoid gully
      if (Math.hypot(tx - 280, tz - 0) < 14.0) continue; // avoid gathering ground

      const ty = getGrasslandElevation(tx, tz);
      const u = (tx - 200) / 130.0;
      const crownCount = Math.max(0, Math.min(4, Math.round(4.0 - 4.0 * u)));

      const tGroup = new THREE.Group();
      tGroup.position.set(tx, ty, tz);

      // Bare brown trunk
      const tMat = new THREE.MeshPhongMaterial({ color: 0x5a3e26, flatShading: true });
      const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.48, 3.2, 6), tMat);
      tr.position.y = 1.6;
      tGroup.add(tr);

      // Crown spheres
      if (crownCount > 0) {
        const cCol = new THREE.Color(0x488a44).lerp(new THREE.Color(0x6b5329), u);
        const cMat = new THREE.MeshPhongMaterial({ color: cCol, flatShading: true });
        const cOffsets = [
          { ox: 0, oy: 3.2, oz: 0, r: 1.5 },
          { ox: 0.7, oy: 3.5, oz: 0.3, r: 1.2 },
          { ox: -0.6, oy: 3.4, oz: -0.3, r: 1.1 },
          { ox: 0.2, oy: 4.1, oz: -0.2, r: 0.95 }
        ];
        for (let c = 0; c < crownCount; c++) {
          const off = cOffsets[c];
          const sp = new THREE.Mesh(new THREE.SphereGeometry(off.r, 6, 5), cMat);
          sp.position.set(off.ox, off.oy, off.oz);
          tGroup.add(sp);
        }
      }
      steppeTreesGroup.add(tGroup);
    }
    dreamGroup.add(steppeTreesGroup);

    // 3. Six Animal Skeletons (skull-and-ribs clusters)
    const skelPositions = [
      { x: 225, z: -15 }, { x: 245, z: 25 }, { x: 265, z: -30 },
      { x: 285, z: 18 },  { x: 305, z: -10 }, { x: 320, z: 20 }
    ];
    const boneMat = new THREE.MeshPhongMaterial({ color: 0xe6e0d3, flatShading: true });
    skelPositions.forEach(sp => {
      const sy = getGrasslandElevation(sp.x, sp.z);
      const skel = new THREE.Group();
      skel.position.set(sp.x, sy + 0.1, sp.z);

      // Skull
      const skull = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.35, 0.8), boneMat);
      skull.position.set(0, 0.2, 0.8);
      skel.add(skull);

      // Spine
      const spine = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.8, 5), boneMat);
      spine.rotation.x = Math.PI / 2;
      spine.position.set(0, 0.25, 0);
      skel.add(spine);

      // 4 Rib arches
      for (let r = 0; r < 4; r++) {
        const arch = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.05, 4, 8, Math.PI), boneMat);
        arch.position.set(0, 0.1, 0.35 - r * 0.4);
        arch.rotation.z = Math.PI;
        skel.add(arch);
      }
      skel.rotation.y = deterministicRandom() * Math.PI * 2;
      dreamGroup.add(skel);
    });

    // 4. Forty Dust Motes on sinusoidal paths
    const dustMotes = [];
    const dustGeo = new THREE.DodecahedronGeometry(0.14, 0);
    const dustMat = new THREE.MeshBasicMaterial({ color: 0xd9b372, transparent: true, opacity: 0.65 });
    for (let i = 0; i < 40; i++) {
      const dm = new THREE.Mesh(dustGeo, dustMat);
      const baseX = 205 + deterministicRandom() * 120;
      const baseZ = -70 + deterministicRandom() * 140;
      const baseY = getGrasslandElevation(baseX, baseZ) + 0.8 + deterministicRandom() * 2.5;
      dm.position.set(baseX, baseY, baseZ);
      dreamGroup.add(dm);
      dustMotes.push({ mesh: dm, bx: baseX, by: baseY, bz: baseZ, seed: i * 1.7 });
    }

    function updateDustMotes(t) {
      dustMotes.forEach(dm => {
        dm.mesh.position.x = dm.bx + Math.sin(t * 0.6 + dm.seed) * 2.8;
        dm.mesh.position.y = dm.by + Math.sin(t * 1.2 + dm.seed * 2.0) * 0.6;
        dm.mesh.position.z = dm.bz + Math.cos(t * 0.8 + dm.seed * 1.5) * 2.8;
      });
    }

    // 5. Dark Crack Decals
    const crackMat = new THREE.MeshBasicMaterial({ color: 0x3d3020, transparent: true, opacity: 0.45, side: THREE.DoubleSide });
    for (let i = 0; i < 28; i++) {
      const cx = 220 + deterministicRandom() * 105;
      const cz = -80 + deterministicRandom() * 160;
      const cy = getGrasslandElevation(cx, cz);
      const crack = new THREE.Mesh(new THREE.RingGeometry(0.3, 1.4, 5), crackMat);
      crack.rotation.x = -Math.PI / 2;
      crack.position.set(cx, cy + 0.04, cz);
      dreamGroup.add(crack);
    }

    // =========================================================
    // 5. VEILS & FALLEN ROCKS
    // =========================================================
    // Veil 1 at x = 200, 6 units tall, spanning z from -110 to 110
    const veilMat1 = new THREE.MeshPhongMaterial({
      color: 0xffd942,
      transparent: true,
      opacity: 0.68,
      side: THREE.DoubleSide,
      emissive: 0x4a3a10,
      flatShading: true
    });
    const veil1Mesh = new THREE.Mesh(new THREE.PlaneGeometry(220, 6.5, 20, 2), veilMat1);
    veil1Mesh.rotateY(Math.PI / 2);
    veil1Mesh.position.set(200, 3.2, 0);
    dreamGroup.add(veil1Mesh);

    // Veil 2 at x = 330, 6 units tall, spanning corridor
    const veilMat2 = new THREE.MeshPhongMaterial({
      color: 0xffd942,
      transparent: true,
      opacity: 0.68,
      side: THREE.DoubleSide,
      emissive: 0x4a3a10,
      flatShading: true
    });
    const veil2Mesh = new THREE.Mesh(new THREE.PlaneGeometry(28, 6.5, 6, 2), veilMat2);
    veil2Mesh.rotateY(Math.PI / 2);
    veil2Mesh.position.set(330, 3.2, 0);
    dreamGroup.add(veil2Mesh);

    // Fallen Rocks at x = 410 (blocking canyon exit)
    const fallenRocksGroup = new THREE.Group();
    const fRockMat = new THREE.MeshPhongMaterial({ color: 0x5a4f47, flatShading: true });
    for (let i = 0; i < 12; i++) {
      const fr = new THREE.Mesh(new THREE.DodecahedronGeometry(1.4, 0), fRockMat);
      const fz = -9.0 + (i / 11) * 18.0;
      const fy = getGrasslandElevation(410, fz);
      fr.position.set(410 + (deterministicRandom() - 0.5) * 1.5, fy + 0.8 + (i % 2) * 0.9, fz);
      fr.rotation.set(deterministicRandom() * 3, deterministicRandom() * 3, deterministicRandom() * 3);
      fr.scale.set(1.4, 1.2, 1.4);
      fallenRocksGroup.add(fr);
    }
    dreamGroup.add(fallenRocksGroup);

    // Canyon rock walls (faceted blocks on |z| > 12)
    const wallBlockGeo = new THREE.BoxGeometry(7.0, 12.0, 5.0);
    const wallBlockMat = new THREE.MeshPhongMaterial({ color: 0x443d38, flatShading: true });
    for (let wx = 332; wx <= 408; wx += 6.5) {
      // North wall (z > 12)
      const bN = new THREE.Mesh(wallBlockGeo, wallBlockMat);
      bN.position.set(wx, 6.0, 15.0);
      bN.rotation.set(0.1, deterministicRandom() * 0.4, -0.05);
      dreamGroup.add(bN);

      // South wall (z < -12)
      const bS = new THREE.Mesh(wallBlockGeo, wallBlockMat);
      bS.position.set(wx, 6.0, -15.0);
      bS.rotation.set(-0.1, deterministicRandom() * 0.4, 0.05);
      dreamGroup.add(bS);
    }

    // =========================================================
    // 6. THE WAKING-MEADOW COPY AT DREAM'S EDGE (x 410-480, z -40-40)
    // Exact translation of Waking Meadow layout by +410 in x!
    // =========================================================
    const copyGroup = new THREE.Group();

    // Copy Slab Rock at (410 + 35, -20) = (445, -20)
    const copySlab = new THREE.Mesh(slabGeo, slabMat.clone());
    copySlab.position.set(445, getGrasslandElevation(445, -20) + 0.2, -20);
    copySlab.rotation.y = 0.4;
    copyGroup.add(copySlab);

    // Copy Perched Lark on copy slab rock
    const copyLark = createLarkModel(false);
    copyLark.root.position.set(445, getGrasslandElevation(445, -20) + 0.44, -20);
    copyLark.root.rotation.y = -Math.PI * 0.3;
    copyGroup.add(copyLark);

    // Copy Big Boulder at (410 + 50, 5) = (460, 5)
    const copyBoulder = new THREE.Mesh(bigBouldGeo, slabMat.clone());
    copyBoulder.position.set(460, getGrasslandElevation(460, 5) + 1.2, 5);
    copyBoulder.rotation.set(0.4, 0.8, -0.2);
    copyGroup.add(copyBoulder);

    // Copy Trees at (425, -5) and (465, -25)
    copyGroup.add(createSmallMeadowTree(425, -5, true));
    copyGroup.add(createSmallMeadowTree(465, -25, true));

    // Copy Puddles at (440, -10) and (455, 15)
    const copyPuddle1 = new THREE.Mesh(puddleGeo, puddleMat.clone());
    copyPuddle1.position.set(440, getGrasslandElevation(440, -10) + 0.05, -10);
    copyPuddle1.scale.set(1.2, 1, 0.8);
    copyGroup.add(copyPuddle1);

    const copyPuddle2 = new THREE.Mesh(puddleGeo, puddleMat.clone());
    copyPuddle2.position.set(455, getGrasslandElevation(455, 15) + 0.05, 15);
    copyPuddle2.scale.set(0.9, 1, 1.3);
    copyGroup.add(copyPuddle2);

    // Copy Stones and Grass
    resetPRNG(7891);
    for (let i = 0; i < 22; i++) {
      const sx = 410 + 14 + deterministicRandom() * 44;
      const sz = -28 + deterministicRandom() * 56;
      const sy = getGrasslandElevation(sx, sz);
      const st = new THREE.Mesh(stoneGeo, slabMat.clone());
      st.position.set(sx, sy + 0.1, sz);
      st.rotation.set(deterministicRandom() * 3, deterministicRandom() * 3, 0);
      copyGroup.add(st);
    }
    for (let i = 0; i < 35; i++) {
      const gx = 410 + 14 + deterministicRandom() * 44;
      const gz = -28 + deterministicRandom() * 56;
      const gy = getGrasslandElevation(gx, gz);
      const tuft = new THREE.Mesh(tuftGeo, dryGrassMat.clone());
      tuft.position.set(gx, gy + 0.22, gz);
      tuft.rotation.y = deterministicRandom() * Math.PI;
      copyGroup.add(tuft);
    }

    dreamGroup.add(copyGroup);

    // =========================================================
    // 7. STORY CIRCLES
    // =========================================================
    const storyRingMat2 = new THREE.MeshBasicMaterial({ color: 0xffe680, side: THREE.DoubleSide, transparent: true, opacity: 0.75 });
    const storyRingMat3 = new THREE.MeshBasicMaterial({ color: 0x90e0ef, side: THREE.DoubleSide, transparent: true, opacity: 0.35 });
    const storyRingMat4 = new THREE.MeshBasicMaterial({ color: 0xf5b041, side: THREE.DoubleSide, transparent: true, opacity: 0.75 });
    const storyRingMat5 = new THREE.MeshBasicMaterial({ color: 0xff7744, side: THREE.DoubleSide, transparent: true, opacity: 0.75 });
    const storyRingMat6 = new THREE.MeshBasicMaterial({ color: 0xf0b27a, side: THREE.DoubleSide, transparent: true, opacity: 0.35 });
    const storyRingMat7 = new THREE.MeshBasicMaterial({ color: 0xaef5ec, side: THREE.DoubleSide, transparent: true, opacity: 0.85 });

    // Circle 2: Hollow (95, 15), r = 4.0
    const circle2Mesh = new THREE.Mesh(new THREE.RingGeometry(3.6, 4.0, 32), storyRingMat2);
    circle2Mesh.rotateX(-Math.PI / 2);
    circle2Mesh.position.set(95, getGrasslandElevation(95, 15) + 0.12, 15);
    dreamGroup.add(circle2Mesh);

    // Circle 3: Far Bank (130, 44), r = 4.0
    const circle3Mesh = new THREE.Mesh(new THREE.RingGeometry(3.6, 4.0, 32), storyRingMat3);
    circle3Mesh.rotateX(-Math.PI / 2);
    circle3Mesh.position.set(130, getGrasslandElevation(130, 44) + 0.12, 44);
    dreamGroup.add(circle3Mesh);

    // Circle 4: Steppe (210, 0), r = 5.0
    const circle4Mesh = new THREE.Mesh(new THREE.RingGeometry(4.5, 5.0, 32), storyRingMat4);
    circle4Mesh.rotateX(-Math.PI / 2);
    circle4Mesh.position.set(210, getGrasslandElevation(210, 0) + 0.12, 0);
    dreamGroup.add(circle4Mesh);

    // Circle 5: Canyon Entrance (336, 0), r = 5.0
    const circle5Mesh = new THREE.Mesh(new THREE.RingGeometry(4.5, 5.0, 32), storyRingMat5);
    circle5Mesh.rotateX(-Math.PI / 2);
    circle5Mesh.position.set(336, getGrasslandElevation(336, 0) + 0.12, 0);
    dreamGroup.add(circle5Mesh);

    // Circle 6: Mother's Niche (404, -8), r = 4.0
    const circle6Mesh = new THREE.Mesh(new THREE.RingGeometry(3.6, 4.0, 32), storyRingMat6);
    circle6Mesh.rotateX(-Math.PI / 2);
    circle6Mesh.position.set(404, getGrasslandElevation(404, -8) + 0.12, -8);
    dreamGroup.add(circle6Mesh);

    // Circle 7: Dream's Edge Copy Slab Rock (445, -20), r = 2.5 (Interaction Circle)
    const circle7Mesh = new THREE.Mesh(new THREE.RingGeometry(2.1, 2.5, 32), storyRingMat7);
    circle7Mesh.rotateX(-Math.PI / 2);
    circle7Mesh.position.set(445, getGrasslandElevation(445, -20) + 0.12, -20);
    dreamGroup.add(circle7Mesh);
"""
