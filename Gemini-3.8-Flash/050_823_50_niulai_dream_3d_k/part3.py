# Part 3: Scenes and props
part3 = r"""
    // =========================================================
    // 2. THE WAKING MEADOW (Reality Map)
    // =========================================================
    const meadowGeo = new THREE.PlaneGeometry(80, 90, 75, 75);
    meadowGeo.rotateX(-Math.PI / 2);
    meadowGeo.translate(35, 0, 0);

    const mPos = meadowGeo.attributes.position;
    const mColors = [];
    const colGreyGrass = new THREE.Color(0x667664);
    const colEarth = new THREE.Color(0x56493d);
    const colHillCold = new THREE.Color(0x4a554a);

    for (let i = 0; i < mPos.count; i++) {
      const vx = mPos.getX(i);
      const vz = mPos.getZ(i);
      const vy = getMeadowElevation(vx, vz);
      mPos.setY(i, vy);

      let col = colGreyGrass.clone();
      if (vy > 3.0 || vx < 10 || vx > 60 || vz < -32 || vz > 32) {
        col.lerp(colHillCold, 0.7);
      } else {
        const patch = Math.sin(vx * 0.15) * Math.cos(vz * 0.18);
        if (patch > 0.25) col.lerp(colEarth, 0.45);
      }
      mColors.push(col.r, col.g, col.b);
    }
    meadowGeo.setAttribute('color', new THREE.Float32BufferAttribute(mColors, 3));
    meadowGeo.computeVertexNormals();

    const meadowMat = new THREE.MeshPhongMaterial({
      vertexColors: true,
      flatShading: true,
      shininess: 2,
      specular: 0x111111
    });
    const meadowMesh = new THREE.Mesh(meadowGeo, meadowMat);
    realityGroup.add(meadowMesh);

    // Overcast layered clouds
    const cloudGeo = new THREE.PlaneGeometry(160, 160, 6, 6);
    cloudGeo.rotateX(Math.PI / 2);
    const cloudMat = new THREE.MeshBasicMaterial({
      color: 0x48524e,
      transparent: true,
      opacity: 0.65,
      side: THREE.DoubleSide
    });
    const cloudMesh = new THREE.Mesh(cloudGeo, cloudMat);
    cloudMesh.position.set(35, 24, 0);
    realityGroup.add(cloudMesh);

    // Props in Meadow:
    // Flat slab rock at (35, -20)
    const slabGeo = new THREE.CylinderGeometry(2.2, 2.6, 0.45, 7);
    const slabMat = new THREE.MeshPhongMaterial({ color: 0x636a64, flatShading: true });
    const slabRock = new THREE.Mesh(slabGeo, slabMat);
    slabRock.position.set(35, getMeadowElevation(35, -20) + 0.2, -20);
    slabRock.rotation.y = 0.4;
    realityGroup.add(slabRock);

    // Perched Lark on slab rock
    function createLarkModel(forFlight) {
      const lark = new THREE.Group();
      const feathMat = new THREE.MeshPhongMaterial({ color: 0x826d52, flatShading: true });
      const breastMat = new THREE.MeshPhongMaterial({ color: 0xd9cbb4, flatShading: true });
      const beakMat = new THREE.MeshPhongMaterial({ color: 0xd69a3a, flatShading: true });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x1a1510 });

      const body = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.26, 0.45), feathMat);
      body.position.set(0, 0.2, 0);
      lark.add(body);

      const breast = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.18, 0.26), breastMat);
      breast.position.set(0, 0.15, 0.12);
      lark.add(breast);

      const headGroup = new THREE.Group();
      headGroup.position.set(0, 0.32, 0.22);
      const head = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.2), feathMat);
      headGroup.add(head);

      const beak = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.2, 4), beakMat);
      beak.position.set(0, 0, 0.18);
      beak.rotation.x = Math.PI / 2;
      headGroup.add(beak);

      const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 0.04), eyeMat);
      eyeL.position.set(0.09, 0.04, 0.06);
      const eyeR = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, 0.04), eyeMat);
      eyeR.position.set(-0.09, 0.04, 0.06);
      headGroup.add(eyeL);
      headGroup.add(eyeR);
      lark.add(headGroup);

      const tail = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.04, 0.32), feathMat);
      tail.position.set(0, 0.2, -0.32);
      tail.rotation.x = -0.3;
      lark.add(tail);

      let wingL = null, wingR = null;
      if (forFlight) {
        // Articulated wings for flying
        const wGeo = new THREE.BoxGeometry(0.48, 0.03, 0.26);
        wGeo.translate(0.24, 0, 0);
        wingL = new THREE.Mesh(wGeo, feathMat);
        wingL.position.set(0.12, 0.24, 0.02);
        lark.add(wingL);

        const wGeoR = new THREE.BoxGeometry(0.48, 0.03, 0.26);
        wGeoR.translate(-0.24, 0, 0);
        wingR = new THREE.Mesh(wGeoR, feathMat);
        wingR.position.set(-0.12, 0.24, 0.02);
        lark.add(wingR);
      } else {
        // Folded wings
        const wingL_f = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.18, 0.32), feathMat);
        wingL_f.position.set(0.13, 0.22, -0.05);
        lark.add(wingL_f);
        const wingR_f = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.18, 0.32), feathMat);
        wingR_f.position.set(-0.13, 0.22, -0.05);
        lark.add(wingR_f);
      }

      return { root: lark, headGroup: headGroup, tail: tail, wingL: wingL, wingR: wingR };
    }

    const larkModel = createLarkModel(false);
    larkModel.root.position.set(35, getMeadowElevation(35, -20) + 0.44, -20);
    larkModel.root.rotation.y = -Math.PI * 0.3;
    realityGroup.add(larkModel.root);

    // Big angular boulder at (50, 5)
    const bigBouldGeo = new THREE.DodecahedronGeometry(2.4, 0);
    const boulderMesh = new THREE.Mesh(bigBouldGeo, slabMat);
    boulderMesh.position.set(50, getMeadowElevation(50, 5) + 1.2, 5);
    boulderMesh.rotation.set(0.4, 0.8, -0.2);
    realityGroup.add(boulderMesh);

    // Two small blob-crown trees at (15, -5) and (55, -25)
    function createSmallMeadowTree(x, z, coldPalette) {
      const tree = new THREE.Group();
      const tMat = new THREE.MeshPhongMaterial({ color: coldPalette ? 0x5a4838 : 0x75523a, flatShading: true });
      const fMat = new THREE.MeshPhongMaterial({ color: coldPalette ? 0x485844 : 0x488a44, flatShading: true });

      const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.38, 2.6, 6), tMat);
      tr.position.y = 1.3;
      tree.add(tr);

      const spGeo = new THREE.SphereGeometry(1, 6, 5);
      const crownOffsets = [
        { ox: 0, oy: 2.7, oz: 0, r: 1.25 },
        { ox: 0.6, oy: 3.1, oz: 0.3, r: 0.95 },
        { ox: -0.5, oy: 2.9, oz: -0.4, r: 0.9 },
        { ox: 0.1, oy: 3.6, oz: -0.2, r: 0.8 }
      ];
      crownOffsets.forEach(co => {
        const sp = new THREE.Mesh(spGeo, fMat);
        sp.position.set(co.ox, co.oy, co.oz);
        sp.scale.set(co.r, co.r * 0.9, co.r);
        tree.add(sp);
      });
      tree.position.set(x, getMeadowElevation(x > 100 ? x - 410 : x, z), z);
      return tree;
    }
    realityGroup.add(createSmallMeadowTree(15, -5, true));
    realityGroup.add(createSmallMeadowTree(55, -25, true));

    // Rainwater puddles at (30, -10) and (45, 15)
    const puddleGeo = new THREE.CircleGeometry(2.6, 16);
    puddleGeo.rotateX(-Math.PI / 2);
    const puddleMat = new THREE.MeshPhongMaterial({
      color: 0x485856,
      shininess: 90,
      specular: 0xbbcccc,
      transparent: true,
      opacity: 0.78
    });
    const puddle1 = new THREE.Mesh(puddleGeo, puddleMat);
    puddle1.position.set(30, getMeadowElevation(30, -10) + 0.05, -10);
    puddle1.scale.set(1.2, 1, 0.8);
    realityGroup.add(puddle1);

    const puddle2 = new THREE.Mesh(puddleGeo, puddleMat.clone());
    puddle2.position.set(45, getMeadowElevation(45, 15) + 0.05, 15);
    puddle2.scale.set(0.9, 1, 1.3);
    realityGroup.add(puddle2);

    resetPRNG(7891);
    const stoneGeo = new THREE.DodecahedronGeometry(0.35, 0);
    for (let i = 0; i < 22; i++) {
      const sx = 14 + deterministicRandom() * 44;
      const sz = -28 + deterministicRandom() * 56;
      const sy = getMeadowElevation(sx, sz);
      const st = new THREE.Mesh(stoneGeo, slabMat);
      st.position.set(sx, sy + 0.1, sz);
      st.rotation.set(deterministicRandom() * 3, deterministicRandom() * 3, 0);
      realityGroup.add(st);
    }

    const dryGrassMat = new THREE.MeshPhongMaterial({ color: 0x8a8456, flatShading: true });
    const tuftGeo = new THREE.ConeGeometry(0.2, 0.5, 4);
    for (let i = 0; i < 35; i++) {
      const gx = 14 + deterministicRandom() * 44;
      const gz = -28 + deterministicRandom() * 56;
      const gy = getMeadowElevation(gx, gz);
      const tuft = new THREE.Mesh(tuftGeo, dryGrassMat);
      tuft.position.set(gx, gy + 0.22, gz);
      tuft.rotation.y = deterministicRandom() * Math.PI;
      realityGroup.add(tuft);
    }

    // Story Circle 1: flat rock at (35, -20), radius 4.0
    const ringGeo = new THREE.RingGeometry(3.6, 4.0, 32);
    ringGeo.rotateX(-Math.PI / 2);
    const meadowRingMat = new THREE.MeshBasicMaterial({
      color: 0xffea88,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.75
    });
    const meadowStoryCircle = new THREE.Mesh(ringGeo, meadowRingMat);
    meadowStoryCircle.position.set(35, getMeadowElevation(35, -20) + 0.12, -20);
    realityGroup.add(meadowStoryCircle);

    // =========================================================
    // 3. THE COMPLETE DREAM WORLD (x from 0 to 480)
    // =========================================================
    const TERRAIN_NX = 245;
    const TERRAIN_NZ = 115;
    const terrainGeo = new THREE.PlaneGeometry(490, 230, TERRAIN_NX, TERRAIN_NZ);
    terrainGeo.rotateX(-Math.PI / 2);
    terrainGeo.translate(240, 0, 0);

    const posAttr = terrainGeo.attributes.position;
    const colors = [];
    const colorGrassLush = new THREE.Color(0x73b75d);
    const colorGrassDeep = new THREE.Color(0x569651);
    const colorGrassLight = new THREE.Color(0x94c96b);
    const colorRockHollow = new THREE.Color(0x7e8876);
    const colorSandStream = new THREE.Color(0xa8a474);
    const colorHillsEdge = new THREE.Color(0x437640);
    const colorSteppeDry = new THREE.Color(0xa8935c);
    const colorSteppeBare = new THREE.Color(0x8a774a);
    const colorCanyonFloor = new THREE.Color(0x58524b);
    const colorCanyonWall = new THREE.Color(0x423c36);
    const colorDuskMeadow = new THREE.Color(0x6b7a5a);

    for (let i = 0; i < posAttr.count; i++) {
      const vx = posAttr.getX(i);
      const vz = posAttr.getZ(i);
      const vy = getGrasslandElevation(vx, vz);
      posAttr.setY(i, vy);

      let vertexCol = colorGrassLush.clone();

      if (vx <= 200) {
        // Plentiful Grassland
        const streamX = getStreamCenter(vz);
        const distStream = Math.abs(vx - streamX);
        const distHollow = Math.hypot(vx - 95, vz - 15);

        if (vy > 4.5 || vx < 16 || vz < -96 || vz > 96 || (vx > 175 && Math.abs(vz) > 50)) {
          vertexCol.lerp(colorHillsEdge, 0.75);
        } else if (distStream < 2.4) {
          vertexCol.lerp(colorSandStream, 0.72);
        } else if (distHollow < 10) {
          vertexCol.lerp(colorRockHollow, 0.6);
        } else {
          const tint = Math.sin(vx * 0.1) * Math.cos(vz * 0.1);
          if (tint > 0.2) vertexCol.lerp(colorGrassLight, 0.38);
          else if (tint < -0.2) vertexCol.lerp(colorGrassDeep, 0.32);
        }
      } else if (vx <= 330) {
        // Withering Steppe: gradient from lush green to dry straw / bare
        const u = (vx - 200) / 130.0;
        vertexCol.lerp(colorSteppeDry, Math.min(u * 1.1, 1.0));
        if (u > 0.6) vertexCol.lerp(colorSteppeBare, (u - 0.6) * 2.0);
        const distGully = Math.abs(vz - (-20));
        if (distGully < 2.0) vertexCol.lerp(new THREE.Color(0x5a4832), 0.65);
        if (vz < -96 || vz > 96) vertexCol.lerp(new THREE.Color(0x6b5c46), 0.8);
      } else if (vx <= 410) {
        // Wolf Pass Canyon
        if (Math.abs(vz) > 12) {
          vertexCol.copy(colorCanyonWall);
        } else {
          vertexCol.copy(colorCanyonFloor);
          if (Math.abs(vz - (-6)) < 1.6) vertexCol.lerp(new THREE.Color(0x3a3632), 0.6);
        }
      } else {
        // Dream's Edge (Eastern Meadow Copy)
        if (Math.abs(vz) <= 40) {
          // Cold palette inside copy!
          vertexCol.copy(colGreyGrass);
          const patch = Math.sin((vx - 410) * 0.15) * Math.cos(vz * 0.18);
          if (patch > 0.25) vertexCol.lerp(colEarth, 0.45);
        } else {
          vertexCol.copy(colorDuskMeadow);
          if (Math.abs(vz) > 40 || vx > 470) vertexCol.lerp(new THREE.Color(0x4a444d), 0.7);
        }
      }

      colors.push(vertexCol.r, vertexCol.g, vertexCol.b);
    }
    terrainGeo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    terrainGeo.computeVertexNormals();

    const terrainMat = new THREE.MeshPhongMaterial({
      vertexColors: true,
      flatShading: true,
      shininess: 4,
      specular: 0x223311
    });
    const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
    dreamGroup.add(terrainMesh);

    // Water Ribbons:
    // 1. Grassland Stream (x from 40 to 160)
    const waterSegments = 180;
    const waterRibbonGeo = new THREE.PlaneGeometry(4.4, 230, 4, waterSegments);
    waterRibbonGeo.rotateX(-Math.PI / 2);
    const wPos = waterRibbonGeo.attributes.position;
    for (let i = 0; i < wPos.count; i++) {
      const localZ = wPos.getZ(i);
      const streamX = getStreamCenter(localZ);
      const currentX = wPos.getX(i);
      wPos.setX(i, streamX + currentX);
      const elev = getGrasslandElevation(streamX + currentX, localZ);
      wPos.setY(i, elev + 0.16);
    }
    waterRibbonGeo.computeVertexNormals();
    const waterMat = new THREE.MeshPhongMaterial({
      color: 0x5ea3b5,
      transparent: true,
      opacity: 0.85,
      flatShading: true,
      shininess: 45,
      specular: 0xddeeff
    });
    const waterMesh = new THREE.Mesh(waterRibbonGeo, waterMat);
    dreamGroup.add(waterMesh);

    // 2. Canyon Streamlet (x from 330 to 410, z ≈ -6)
    const streamletGeo = new THREE.PlaneGeometry(80, 2.4, 40, 2);
    streamletGeo.rotateX(-Math.PI / 2);
    streamletGeo.translate(370, 0, -6);
    const slPos = streamletGeo.attributes.position;
    for (let i = 0; i < slPos.count; i++) {
      const vx = slPos.getX(i);
      const vz = slPos.getZ(i);
      const elev = getGrasslandElevation(vx, vz);
      slPos.setY(i, elev + 0.12);
    }
    streamletGeo.computeVertexNormals();
    const streamletMesh = new THREE.Mesh(streamletGeo, waterMat.clone());
    dreamGroup.add(streamletMesh);

    // Water Ripples
    const ripples = [];
    const rippleGeo = new THREE.RingGeometry(0.12, 0.28, 16);
    rippleGeo.rotateX(-Math.PI / 2);
    const rippleMat = new THREE.MeshBasicMaterial({
      color: 0xdaf2f8,
      transparent: true,
      opacity: 0.85,
      side: THREE.DoubleSide
    });

    function spawnRipple(x, y, z) {
      const mesh = new THREE.Mesh(rippleGeo, rippleMat.clone());
      mesh.position.set(x, y + 0.05, z);
      dreamGroup.add(mesh);
      ripples.push({ mesh: mesh, life: 0.0, maxLife: 1.2 });
    }

    function updateRipples(dt) {
      for (let i = ripples.length - 1; i >= 0; i--) {
        const r = ripples[i];
        r.life += dt;
        const progress = r.life / r.maxLife;
        if (progress >= 1.0) {
          dreamGroup.remove(r.mesh);
          r.mesh.geometry.dispose();
          r.mesh.material.dispose();
          ripples.splice(i, 1);
        } else {
          const s = 1.0 + progress * 4.6;
          r.mesh.scale.set(s, 1, s);
          r.mesh.material.opacity = (1.0 - progress) * 0.78;
        }
      }
    }
"""
