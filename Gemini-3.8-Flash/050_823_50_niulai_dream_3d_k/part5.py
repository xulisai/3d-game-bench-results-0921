# Part 5: Models & Entities
part5 = r"""
    // =========================================================
    // 8. MODELS & ENTITIES
    // =========================================================
    // 1. Calf (Niulai)
    function createCalfModel() {
      const calf = new THREE.Group();
      const bodyMat = new THREE.MeshPhongMaterial({ color: 0xebbe4d, flatShading: true });
      const underbellyMat = new THREE.MeshPhongMaterial({ color: 0xfff0b8, flatShading: true });
      const darkMat = new THREE.MeshPhongMaterial({ color: 0x4a3219, flatShading: true });
      const muzzleMat = new THREE.MeshPhongMaterial({ color: 0xf2d6a2, flatShading: true });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x221100 });

      const bodyGeo = new THREE.BoxGeometry(0.9, 0.85, 1.45);
      const body = new THREE.Mesh(bodyGeo, bodyMat);
      body.position.set(0, 0.95, 0);
      calf.add(body);

      const bellyGeo = new THREE.BoxGeometry(0.82, 0.25, 1.3);
      const belly = new THREE.Mesh(bellyGeo, underbellyMat);
      belly.position.set(0, 0.65, 0);
      calf.add(belly);

      const headGroup = new THREE.Group();
      headGroup.position.set(0, 1.25, 0.7);

      const neckGeo = new THREE.BoxGeometry(0.5, 0.55, 0.5);
      const neck = new THREE.Mesh(neckGeo, bodyMat);
      neck.position.set(0, 0.1, -0.1);
      neck.rotation.x = -0.3;
      headGroup.add(neck);

      const headGeo = new THREE.BoxGeometry(0.65, 0.6, 0.75);
      const head = new THREE.Mesh(headGeo, bodyMat);
      head.position.set(0, 0.35, 0.25);
      headGroup.add(head);

      const muzzleGeo = new THREE.BoxGeometry(0.48, 0.4, 0.4);
      const muzzle = new THREE.Mesh(muzzleGeo, muzzleMat);
      muzzle.position.set(0, 0.25, 0.65);
      headGroup.add(muzzle);

      const nostrilGeo = new THREE.BoxGeometry(0.08, 0.08, 0.05);
      const n1 = new THREE.Mesh(nostrilGeo, darkMat);
      n1.position.set(0.12, 0.26, 0.86);
      const n2 = new THREE.Mesh(nostrilGeo, darkMat);
      n2.position.set(-0.12, 0.26, 0.86);
      headGroup.add(n1);
      headGroup.add(n2);

      const eyeGeo = new THREE.BoxGeometry(0.08, 0.1, 0.1);
      const eyeL = new THREE.Mesh(eyeGeo, eyeMat);
      eyeL.position.set(0.33, 0.42, 0.35);
      const eyeR = new THREE.Mesh(eyeGeo, eyeMat);
      eyeR.position.set(-0.33, 0.42, 0.35);
      headGroup.add(eyeL);
      headGroup.add(eyeR);

      const earGeo = new THREE.ConeGeometry(0.14, 0.38, 4);
      const earL = new THREE.Mesh(earGeo, bodyMat);
      earL.position.set(0.42, 0.55, 0.05);
      earL.rotation.set(0.2, 0, -1.1);
      const earR = new THREE.Mesh(earGeo, bodyMat);
      earR.position.set(-0.42, 0.55, 0.05);
      earR.rotation.set(0.2, 0, 1.1);
      headGroup.add(earL);
      headGroup.add(earR);

      calf.add(headGroup);

      const legGeo = new THREE.BoxGeometry(0.24, 0.65, 0.26);
      legGeo.translate(0, -0.32, 0);
      const hoofGeo = new THREE.BoxGeometry(0.26, 0.15, 0.28);
      hoofGeo.translate(0, -0.65, 0);

      function createLeg(x, z) {
        const legPivot = new THREE.Group();
        legPivot.position.set(x, 0.72, z);
        legPivot.add(new THREE.Mesh(legGeo, bodyMat));
        legPivot.add(new THREE.Mesh(hoofGeo, darkMat));
        calf.add(legPivot);
        return legPivot;
      }

      const legFL = createLeg(0.32, 0.45);
      const legFR = createLeg(-0.32, 0.45);
      const legBL = createLeg(0.32, -0.48);
      const legBR = createLeg(-0.32, -0.48);

      const tailPivot = new THREE.Group();
      tailPivot.position.set(0, 1.25, -0.72);
      const tailGeo = new THREE.CylinderGeometry(0.06, 0.04, 0.55, 5);
      tailGeo.translate(0, -0.27, 0);
      const tailMesh = new THREE.Mesh(tailGeo, bodyMat);
      tailMesh.rotation.x = -0.25;
      tailPivot.add(tailMesh);
      const tuftGeo = new THREE.ConeGeometry(0.12, 0.22, 5);
      tuftGeo.translate(0, -0.55, 0);
      tailPivot.add(new THREE.Mesh(tuftGeo, darkMat));
      calf.add(tailPivot);

      return {
        root: calf,
        headGroup: headGroup,
        body: body,
        legFL: legFL,
        legFR: legFR,
        legBL: legBL,
        legBR: legBR,
        tailPivot: tailPivot
      };
    }

    const niulai = createCalfModel();
    scene.add(niulai.root);

    // 2. Adult Cow Model
    function createAdultCowModel(colorScheme, isMother, isSleeping = false) {
      const cow = new THREE.Group();
      const baseMat = new THREE.MeshPhongMaterial({ color: colorScheme.base, flatShading: true });
      const patchMat = new THREE.MeshPhongMaterial({ color: colorScheme.patch, flatShading: true });
      const muzzleMat = new THREE.MeshPhongMaterial({ color: 0xe6cfb8, flatShading: true });
      const darkMat = new THREE.MeshPhongMaterial({ color: 0x2b2219, flatShading: true });
      const hornMat = new THREE.MeshPhongMaterial({ color: 0xf5f3e4, flatShading: true });

      const scale = isMother ? 1.28 : 1.0;
      cow.scale.set(scale, scale, scale);

      const body = new THREE.Mesh(new THREE.BoxGeometry(1.35, 1.3, 2.3), baseMat);
      body.position.set(0, 1.45, 0);
      cow.add(body);

      const patch1 = new THREE.Mesh(new THREE.BoxGeometry(1.38, 0.7, 0.9), patchMat);
      patch1.position.set(0, 1.6, 0.3);
      cow.add(patch1);

      if (isMother) {
        // Distinct prominent white markings for Mother
        const headMark = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.2), patchMat);
        headMark.position.set(0, 1.85, 1.35);
        cow.add(headMark);
      }

      const neckGroup = new THREE.Group();
      neckGroup.position.set(0, 1.6, 1.1);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.8, 1.1), baseMat);
      head.position.set(0, -0.1, 0.5);
      neckGroup.add(head);

      const muzzle = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.5, 0.6), muzzleMat);
      muzzle.position.set(0, -0.22, 1.05);
      neckGroup.add(muzzle);

      // Eyes: open or closed if sleeping
      const eyeMat = new THREE.MeshBasicMaterial({ color: isSleeping ? 0x443322 : 0x111111 });
      const eyeGeo = isSleeping ? new THREE.BoxGeometry(0.08, 0.02, 0.12) : new THREE.BoxGeometry(0.08, 0.08, 0.1);
      const eyeL = new THREE.Mesh(eyeGeo, eyeMat);
      eyeL.position.set(0.44, 0.06, 0.6);
      const eyeR = new THREE.Mesh(eyeGeo, eyeMat);
      eyeR.position.set(-0.44, 0.06, 0.6);
      neckGroup.add(eyeL);
      neckGroup.add(eyeR);

      const hornGeo = new THREE.ConeGeometry(0.12, 0.55, 5);
      const hornL = new THREE.Mesh(hornGeo, hornMat);
      hornL.position.set(0.48, 0.45, 0.4);
      hornL.rotation.set(0.2, 0, -0.85);
      const hornR = new THREE.Mesh(hornGeo, hornMat);
      hornR.position.set(-0.48, 0.45, 0.4);
      hornR.rotation.set(0.2, 0, 0.85);
      neckGroup.add(hornL);
      neckGroup.add(hornR);

      const earGeo = new THREE.ConeGeometry(0.16, 0.48, 4);
      const earL = new THREE.Mesh(earGeo, baseMat);
      earL.position.set(0.55, 0.2, 0.2);
      earL.rotation.set(0.1, 0, -1.2);
      const earR = new THREE.Mesh(earGeo, baseMat);
      earR.position.set(-0.55, 0.2, 0.2);
      earR.rotation.set(0.1, 0, 1.2);
      neckGroup.add(earL);
      neckGroup.add(earR);

      cow.add(neckGroup);

      const legGeo = new THREE.BoxGeometry(0.32, 0.95, 0.35);
      legGeo.translate(0, -0.47, 0);
      const hoofGeo = new THREE.BoxGeometry(0.35, 0.2, 0.38);
      hoofGeo.translate(0, -0.95, 0);

      function createCowLeg(x, z) {
        const p = new THREE.Group();
        p.position.set(x, 1.1, z);
        p.add(new THREE.Mesh(legGeo, baseMat));
        p.add(new THREE.Mesh(hoofGeo, darkMat));
        cow.add(p);
        return p;
      }

      const legFL = createCowLeg(0.5, 0.75);
      const legFR = createCowLeg(-0.5, 0.75);
      const legBL = createCowLeg(0.5, -0.8);
      const legBR = createCowLeg(-0.5, -0.8);

      const tailPivot = new THREE.Group();
      tailPivot.position.set(0, 1.9, -1.15);
      const tailGeo = new THREE.CylinderGeometry(0.08, 0.05, 0.85, 5);
      tailGeo.translate(0, -0.42, 0);
      tailPivot.add(new THREE.Mesh(tailGeo, baseMat));
      const tuftGeo = new THREE.ConeGeometry(0.18, 0.3, 5);
      tuftGeo.translate(0, -0.85, 0);
      tailPivot.add(new THREE.Mesh(tuftGeo, darkMat));
      cow.add(tailPivot);

      if (isSleeping) {
        // Folded lying pose
        body.position.y = 0.75;
        neckGroup.position.set(0, 0.85, 1.0);
        neckGroup.rotation.x = 0.35;
        legFL.position.set(0.45, 0.45, 0.65);
        legFL.rotation.z = 1.35;
        legFR.position.set(-0.45, 0.45, 0.65);
        legFR.rotation.z = -1.35;
        legBL.position.set(0.5, 0.45, -0.65);
        legBL.rotation.z = 1.45;
        legBR.position.set(-0.5, 0.45, -0.65);
        legBR.rotation.z = -1.45;
      }

      return {
        root: cow,
        neckGroup: neckGroup,
        body: body,
        legFL: legFL,
        legFR: legFR,
        legBL: legBL,
        legBR: legBR,
        tailPivot: tailPivot,
        isMother: isMother,
        setLyingDown: function() {
          body.position.y = 0.75;
          neckGroup.position.set(0, 0.85, 1.0);
          neckGroup.rotation.x = 0.35;
          legFL.position.set(0.45, 0.45, 0.65);
          legFL.rotation.z = 1.35;
          legFR.position.set(-0.45, 0.45, 0.65);
          legFR.rotation.z = -1.35;
          legBL.position.set(0.5, 0.45, -0.65);
          legBL.rotation.z = 1.45;
          legBR.position.set(-0.5, 0.45, -0.65);
          legBR.rotation.z = -1.45;
        },
        setStanding: function() {
          body.position.y = 1.45;
          neckGroup.position.set(0, 1.6, 1.1);
          neckGroup.rotation.x = 0;
          legFL.position.set(0.5, 1.1, 0.75);
          legFL.rotation.set(0, 0, 0);
          legFR.position.set(-0.5, 1.1, 0.75);
          legFR.rotation.set(0, 0, 0);
          legBL.position.set(0.5, 1.1, -0.8);
          legBL.rotation.set(0, 0, 0);
          legBR.position.set(-0.5, 1.1, -0.8);
          legBR.rotation.set(0, 0, 0);
        }
      };
    }

    // Mother cow in true Waking Meadow (standing at 28, 10)
    const motherColorScheme = { base: 0x3d352e, patch: 0xf5f3ea };
    const meadowMother = createAdultCowModel(motherColorScheme, true, false);
    meadowMother.root.position.set(28, getMeadowElevation(28, 10), 10);
    meadowMother.root.rotation.y = Math.PI * 0.4;
    realityGroup.add(meadowMother.root);

    // Sleeping Mother copy in Dream's Edge (lying down asleep at 410 + 28, 10 = 438, 10)
    const copyMother = createAdultCowModel(motherColorScheme, true, true);
    copyMother.root.position.set(438, getGrasslandElevation(438, 10), 10);
    copyMother.root.rotation.y = Math.PI * 0.4;
    copyGroup.add(copyMother.root);

    // 3. Companion Leopard Cub (Bola)
    function createBolaModel() {
      const bola = new THREE.Group();
      const furMat = new THREE.MeshPhongMaterial({ color: 0xdca355, flatShading: true });
      const spotMat = new THREE.MeshPhongMaterial({ color: 0x482d16, flatShading: true });
      const muzzleMat = new THREE.MeshPhongMaterial({ color: 0xfaeedd, flatShading: true });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x3d783d });

      const torsoGroup = new THREE.Group();
      torsoGroup.position.set(0, 0.5, 0);

      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.45, 0.85), furMat);
      torsoGroup.add(torso);

      const spotGeo = new THREE.BoxGeometry(0.16, 0.12, 0.16);
      const spotsData = [
        [0.25, 0.12, 0.2], [-0.25, 0.15, -0.1], [0.25, 0.05, -0.25],
        [-0.25, 0.08, 0.25], [0, 0.23, 0.1], [0, 0.23, -0.2]
      ];
      spotsData.forEach(pos => {
        const sp = new THREE.Mesh(spotGeo, spotMat);
        sp.position.set(pos[0], pos[1], pos[2]);
        torsoGroup.add(sp);
      });

      const headGroup = new THREE.Group();
      headGroup.position.set(0, 0.35, 0.45);
      headGroup.add(new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.4, 0.45), furMat));

      const hSpot1 = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.08, 0.1), spotMat);
      hSpot1.position.set(0, 0.21, 0);
      headGroup.add(hSpot1);

      const muzzle = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.22, 0.25), muzzleMat);
      muzzle.position.set(0, -0.08, 0.3);
      headGroup.add(muzzle);

      const nose = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.07, 0.05), spotMat);
      nose.position.set(0, -0.02, 0.43);
      headGroup.add(nose);

      const eyeGeo = new THREE.BoxGeometry(0.08, 0.08, 0.06);
      const eyeL = new THREE.Mesh(eyeGeo, eyeMat);
      eyeL.position.set(0.14, 0.06, 0.23);
      const eyeR = new THREE.Mesh(eyeGeo, eyeMat);
      eyeR.position.set(-0.14, 0.06, 0.23);
      headGroup.add(eyeL);
      headGroup.add(eyeR);

      const earGeo = new THREE.CylinderGeometry(0.08, 0.09, 0.12, 5);
      const earL = new THREE.Mesh(earGeo, furMat);
      earL.position.set(0.2, 0.23, -0.05);
      earL.rotation.z = -0.4;
      const earR = new THREE.Mesh(earGeo, furMat);
      earR.position.set(-0.2, 0.23, -0.05);
      earR.rotation.z = 0.4;
      headGroup.add(earL);
      headGroup.add(earR);

      torsoGroup.add(headGroup);
      bola.add(torsoGroup);

      const forelegGeo = new THREE.BoxGeometry(0.15, 0.45, 0.16);
      forelegGeo.translate(0, -0.22, 0);

      const legFL = new THREE.Group();
      legFL.position.set(0.18, 0.4, 0.32);
      legFL.add(new THREE.Mesh(forelegGeo, furMat));
      bola.add(legFL);

      const legFR = new THREE.Group();
      legFR.position.set(-0.18, 0.4, 0.32);
      legFR.add(new THREE.Mesh(forelegGeo, furMat));
      bola.add(legFR);

      const hindThighGeo = new THREE.BoxGeometry(0.22, 0.35, 0.38);
      const hindFootGeo = new THREE.BoxGeometry(0.16, 0.16, 0.32);

      const legBL = new THREE.Group();
      legBL.position.set(0.22, 0.28, -0.26);
      const footL = new THREE.Mesh(hindFootGeo, furMat);
      footL.position.set(0, -0.15, 0.1);
      legBL.add(new THREE.Mesh(hindThighGeo, furMat));
      legBL.add(footL);
      bola.add(legBL);

      const legBR = new THREE.Group();
      legBR.position.set(-0.22, 0.28, -0.26);
      const footR = new THREE.Mesh(hindFootGeo, furMat);
      footR.position.set(0, -0.15, 0.1);
      legBR.add(new THREE.Mesh(hindThighGeo, furMat));
      legBR.add(footR);
      bola.add(legBR);

      const tailPivot = new THREE.Group();
      tailPivot.position.set(0, 0.4, -0.42);
      const tailGeo = new THREE.CylinderGeometry(0.05, 0.035, 0.65, 5);
      tailGeo.translate(0, 0, -0.32);
      tailGeo.rotateX(Math.PI / 2);
      tailPivot.add(new THREE.Mesh(tailGeo, furMat));
      const tipMesh = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.08, 0.12), spotMat);
      tipMesh.position.set(0, 0, -0.65);
      tailPivot.add(tipMesh);
      bola.add(tailPivot);

      return {
        root: bola,
        torsoGroup: torsoGroup,
        headGroup: headGroup,
        legFL: legFL,
        legFR: legFR,
        legBL: legBL,
        legBR: legBR,
        tailPivot: tailPivot
      };
    }

    const bolaData = createBolaModel();
    bolaData.root.position.set(95, getGrasslandElevation(95, 15), 15);
    bolaData.root.rotation.y = -Math.PI * 0.6;
    dreamGroup.add(bolaData.root);

    function setBolaPose(poseName, trotProgress = 0) {
      STATE.bola.pose = poseName;
      if (poseName === "sitting") {
        bolaData.torsoGroup.position.y = 0.38;
        bolaData.torsoGroup.rotation.x = -0.45;
        bolaData.legFL.rotation.x = -0.1;
        bolaData.legFR.rotation.x = -0.1;
        bolaData.legBL.position.y = 0.22;
        bolaData.legBL.rotation.x = -0.7;
        bolaData.legBR.position.y = 0.22;
        bolaData.legBR.rotation.x = -0.7;
      } else if (poseName === "standing") {
        bolaData.torsoGroup.position.y = 0.60;
        bolaData.torsoGroup.rotation.x = 0;
        bolaData.legFL.rotation.x = 0;
        bolaData.legFR.rotation.x = 0;
        bolaData.legBL.position.y = 0.38;
        bolaData.legBL.rotation.x = 0;
        bolaData.legBR.position.y = 0.38;
        bolaData.legBR.rotation.x = 0;
      } else if (poseName === "trotting") {
        bolaData.torsoGroup.position.y = 0.60 + Math.abs(Math.sin(trotProgress * 2.0)) * 0.05;
        bolaData.torsoGroup.rotation.x = 0.05;
        const swing = Math.sin(trotProgress) * 0.65;
        bolaData.legFL.rotation.x = swing;
        bolaData.legBR.rotation.x = swing;
        bolaData.legFR.rotation.x = -swing;
        bolaData.legBL.rotation.x = -swing;
        bolaData.legBL.position.y = 0.38;
        bolaData.legBR.position.y = 0.38;
      }
    }
    setBolaPose("sitting");

    // 4. Lean Wolf Model
    function createWolfModel(id) {
      const wolf = new THREE.Group();
      const furMat = new THREE.MeshPhongMaterial({ color: 0x585c60, flatShading: true });
      const bellyMat = new THREE.MeshPhongMaterial({ color: 0x7a8084, flatShading: true });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0xffea00 }); // yellow eye-glints

      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.6, 1.4), furMat);
      torso.position.set(0, 0.8, 0);
      wolf.add(torso);

      const belly = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.2, 0.9), bellyMat);
      belly.position.set(0, 0.6, -0.1);
      wolf.add(belly);

      // Low head posture
      const neck = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.45, 0.6), furMat);
      neck.position.set(0, 0.72, 0.8);
      neck.rotation.x = 0.35;
      wolf.add(neck);

      const head = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.4, 0.6), furMat);
      head.position.set(0, 0.6, 1.15);
      wolf.add(head);

      const muzzle = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.25, 0.45), furMat);
      muzzle.position.set(0, 0.5, 1.55);
      wolf.add(muzzle);

      // Yellow eye glints
      const eyeL = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.06), eyeMat);
      eyeL.position.set(0.18, 0.68, 1.32);
      const eyeR = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.06), eyeMat);
      eyeR.position.set(-0.18, 0.68, 1.32);
      wolf.add(eyeL);
      wolf.add(eyeR);

      // Erect ears
      const earGeo = new THREE.ConeGeometry(0.1, 0.3, 4);
      const earL = new THREE.Mesh(earGeo, furMat);
      earL.position.set(0.18, 0.88, 1.05);
      earL.rotation.set(-0.2, 0, -0.2);
      const earR = new THREE.Mesh(earGeo, furMat);
      earR.position.set(-0.18, 0.88, 1.05);
      earR.rotation.set(-0.2, 0, 0.2);
      wolf.add(earL);
      wolf.add(earR);

      // Legs
      const legGeo = new THREE.BoxGeometry(0.16, 0.65, 0.18);
      legGeo.translate(0, -0.32, 0);

      function createWolfLeg(x, z) {
        const p = new THREE.Group();
        p.position.set(x, 0.65, z);
        p.add(new THREE.Mesh(legGeo, furMat));
        wolf.add(p);
        return p;
      }

      const legFL = createWolfLeg(0.2, 0.5);
      const legFR = createWolfLeg(-0.2, 0.5);
      const legBL = createWolfLeg(0.2, -0.5);
      const legBR = createWolfLeg(-0.2, -0.5);

      const tail = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 0.7), furMat);
      tail.position.set(0, 0.7, -0.95);
      tail.rotation.x = -0.5;
      wolf.add(tail);

      return {
        id: id,
        root: wolf,
        legFL: legFL,
        legFR: legFR,
        legBL: legBL,
        legBR: legBR,
        tail: tail
      };
    }

    const wolfEntities = [];
    for (let i = 1; i <= 4; i++) {
      const wObj = createWolfModel(i);
      dreamGroup.add(wObj.root);
      wolfEntities.push(wObj);
    }

    // 5. Flying Lark (Yunding Guide in Dream)
    const flyingLark = createLarkModel(true);
    dreamGroup.add(flyingLark.root);

    // 6. Grass Snake at (120, -55)
    function createSnakeModel() {
      const snakeGroup = new THREE.Group();
      const snakeGreen = new THREE.MeshPhongMaterial({ color: 0x416834, flatShading: true });
      const snakeYellow = new THREE.MeshPhongMaterial({ color: 0xbfb64d, flatShading: true });
      const eyeMat = new THREE.MeshBasicMaterial({ color: 0x111111 });

      const segments = [];
      for (let i = 0; i < 8; i++) {
        const r = (i === 0) ? 0.14 : (0.13 - i * 0.013);
        const geo = new THREE.SphereGeometry(r, 6, 5);
        const mat = (i % 2 === 0) ? snakeGreen : snakeYellow;
        const seg = new THREE.Mesh(geo, mat);
        seg.position.set(0, r * 0.8, -i * 0.22);
        snakeGroup.add(seg);
        segments.push(seg);
      }
      return { root: snakeGroup, segments: segments };
    }
    const snakeModel = createSnakeModel();
    snakeModel.root.position.set(120, getGrasslandElevation(120, -55), -55);
    dreamGroup.add(snakeModel.root);

    // 7. Eight Cattle Setup
    const herdConfigs = [
      { id: 1, color: { base: 0xd9c29c, patch: 0x5a3e26 }, isMother: false },
      { id: 2, color: { base: 0x3f3630, patch: 0xecd8c3 }, isMother: false },
      { id: 3, color: { base: 0xc89868, patch: 0xffffff }, isMother: false },
      { id: 4, color: { base: 0xf0efe6, patch: 0x42382f }, isMother: false },
      { id: 5, color: { base: 0x8a6242, patch: 0xf4ead8 }, isMother: false },
      { id: 6, color: { base: 0x3e3834, patch: 0xf2ebe2 }, isMother: false },
      { id: 7, color: { base: 0xd0ab7d, patch: 0x6e4e37 }, isMother: false },
      { id: 8, color: motherColorScheme, isMother: true } // Cow 8 is Mother!
    ];

    const herdEntities = [];
    herdConfigs.forEach((cfg, idx) => {
      const cowObj = createAdultCowModel(cfg.color, cfg.isMother, false);
      dreamGroup.add(cowObj.root);

      // Initial gathered cluster at (280, 0)
      const angle = (idx / 8) * Math.PI * 2;
      const dist = (idx === 7) ? 2.5 : (3.5 + (idx % 3) * 1.5);
      const gx = 280 + Math.cos(angle) * dist;
      const gz = Math.sin(angle) * dist;
      const gy = getGrasslandElevation(gx, gz);
      cowObj.root.position.set(gx, gy, gz);
      cowObj.root.rotation.y = angle + Math.PI;

      herdEntities.push({
        id: cfg.id,
        isMother: cfg.isMother,
        mesh: cowObj.root,
        parts: cowObj,
        gatherPos: { x: gx, y: gy, z: gz, rot: angle + Math.PI },
        settledPos: { x: 442 + (idx % 3) * 4.0, z: 70 + Math.floor(idx / 3) * 4.0 },
        longOffset: idx * 3.4,
        latOffset: (idx % 2 === 0 ? 0.6 : -0.6),
        phaseOffset: idx * 2.8
      });
    });

    STATE.herd = herdEntities.map(h => ({
      id: h.id,
      pos: [h.gatherPos.x, h.gatherPos.y, h.gatherPos.z]
    }));
"""
