const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf8');

// Section 1: Define AI states and sequences before Scene, Camera, Renderer
const searchBeforeScene = `    // Scene, Camera, Renderer
    const container = document.getElementById('game-container');`;

const aiStateDefinitions = `    // AI Opponent & Match Play State
    const PHASE_AI_PLAYING = 6;

    let matchStatus = 0;
    let holesRemaining = 4;
    let aiStrokes = [null, null, null, null];
    let playerStrokes = [null, null, null, null];

    const AI_SHOT_SEQUENCES = [
      // Hole 1: Par 4 -> 4 strokes (Par)
      [
        { club: 'Driver', power: 96, offset: 0, shape: null, aimOffsetDeg: 0 },
        { club: '7-Iron', power: 74, offset: 0, shape: null, aimOffsetDeg: 0 },
        { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 20 },
        { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: -5 }
      ],
      // Hole 2: Par 3 -> 4 strokes (+1 / Bogey)
      [
        { club: '7-Iron', power: 80, offset: 0, shape: null, aimOffsetDeg: 0 },
        { club: 'Sand Wedge', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
        { club: 'Putter', power: 28, offset: 0, shape: null, aimOffsetDeg: 0 },
        { club: 'Putter', power: 18, offset: 0, shape: null, aimOffsetDeg: 0 }
      ],
      // Hole 3: Par 5 -> 5 strokes (Par)
      [
        { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -23 },
        { club: '7-Iron', power: 95, offset: 0, shape: null, aimOffsetDeg: -23 },
        { club: 'Pitching Wedge', power: 80, offset: 0, shape: null, aimOffsetDeg: -20 },
        { club: 'Putter', power: 29, offset: 0, shape: null, aimOffsetDeg: -3 },
        { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: -9 }
      ],
      // Hole 4: Par 4 -> 3 strokes (-1 / Birdie)
      [
        { club: 'Driver', power: 95, offset: 0, shape: 'draw', aimOffsetDeg: 29.28 },
        { club: 'Pitching Wedge', power: 72, offset: 0, shape: null, aimOffsetDeg: -5 },
        { club: 'Putter', power: 16, offset: 0, shape: null, aimOffsetDeg: 0 }
      ]
    ];

    let aiState = {
      holeIndex: 0,
      shotIndex: 0,
      strokes: 0,
      step: 'idle', // 'address', 'backswing', 'downswing', 'flight', 'wait'
      timer: 0,
      shotOrigin: new THREE.Vector3(),
      aimAngle: 0,
      activeShotVelocity: null,
      holedOut: false
    };

    let aiBall = {
      pos: new THREE.Vector3(0, 0.1, 0),
      vel: new THREE.Vector3(0, 0, 0),
      radius: 0.1,
      isGrounded: true
    };

    // Scene, Camera, Renderer
    const container = document.getElementById('game-container');`;

content = content.replace(searchBeforeScene, aiStateDefinitions);

// Section 2: Add Drop Zone 3D markers in HOLES creation loop
const searchStakeLoop = `stakeGroup.position.set(sideX, getTerrainHeight(sideX, markerZ), markerZ);
          scene.add(stakeGroup);
        });
      });
    });`;

const newDropZoneMarker = `stakeGroup.position.set(sideX, getTerrainHeight(sideX, markerZ), markerZ);
          scene.add(stakeGroup);
        });
      });

      // 8. Fixed Drop Zone Physical Marker on Fairway
      if (h.dropZone) {
        const dzGroup = new THREE.Group();
        const dzRingGeo = new THREE.RingGeometry(1.2, 1.7, 24);
        dzRingGeo.rotateX(-Math.PI / 2);
        const dzRingMat = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
        const dzRing = new THREE.Mesh(dzRingGeo, dzRingMat);
        dzGroup.add(dzRing);

        const dzDiscGeo = new THREE.CircleGeometry(1.2, 24);
        dzDiscGeo.rotateX(-Math.PI / 2);
        const dzDiscMat = new THREE.MeshLambertMaterial({ color: 0x2d6824, side: THREE.DoubleSide });
        const dzDisc = new THREE.Mesh(dzDiscGeo, dzDiscMat);
        dzDisc.position.y = -0.01;
        dzGroup.add(dzDisc);

        const dzCanvas = document.createElement('canvas');
        dzCanvas.width = 64;
        dzCanvas.height = 64;
        const dzCtx = dzCanvas.getContext('2d');
        dzCtx.fillStyle = '#ffffff';
        dzCtx.font = 'bold 36px Arial';
        dzCtx.textAlign = 'center';
        dzCtx.textBaseline = 'middle';
        dzCtx.fillText('DZ', 32, 32);
        const dzTex = new THREE.CanvasTexture(dzCanvas);
        const dzTextGeo = new THREE.PlaneGeometry(1.5, 1.5);
        dzTextGeo.rotateX(-Math.PI / 2);
        const dzTextMat = new THREE.MeshBasicMaterial({ map: dzTex, transparent: true });
        const dzText = new THREE.Mesh(dzTextGeo, dzTextMat);
        dzText.position.y = 0.02;
        dzGroup.add(dzText);

        dzGroup.position.set(h.dropZone.x, getTerrainHeight(h.dropZone.x, h.dropZone.z) + 0.03, h.dropZone.z);
        scene.add(dzGroup);
      }
    });`;

content = content.replace(searchStakeLoop, newDropZoneMarker);

// Section 3: Add AI Ball and AI Golfer Model
const searchAfterPlayerGolfer = `    swingPivot.add(clubGroup);
    upperBody.add(swingPivot);
    golferGroup.add(upperBody);
    scene.add(golferGroup);`;

const newAIGolferModel = `    swingPivot.add(clubGroup);
    upperBody.add(swingPivot);
    golferGroup.add(upperBody);
    scene.add(golferGroup);

    // ==========================================
    // AI BALL & AI GOLFER CHARACTER (Visually distinct: Crimson/Charcoal)
    // ==========================================
    const aiBallMat = new THREE.MeshStandardMaterial({
      color: 0xffd700, // Golden yellow ball
      roughness: 0.3,
      metalness: 0.1
    });
    const aiBallMesh = new THREE.Mesh(ballGeo, aiBallMat);
    aiBallMesh.castShadow = true;
    scene.add(aiBallMesh);

    const aiGolferGroup = new THREE.Group();
    const aiShirtMat = new THREE.MeshLambertMaterial({ color: 0xc92a2a }); // Crimson polo
    const aiPantsMat = new THREE.MeshLambertMaterial({ color: 0x2c3437 }); // Dark charcoal slacks
    const aiShoesMat = new THREE.MeshLambertMaterial({ color: 0xefefef }); // White shoes
    const aiCapMat = new THREE.MeshLambertMaterial({ color: 0xc92a2a });   // Crimson cap

    const aiLeftLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 1.2, 8), aiPantsMat);
    aiLeftLeg.position.set(-0.25, 0.6, 0);
    aiLeftLeg.castShadow = true;
    aiGolferGroup.add(aiLeftLeg);

    const aiRightLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 1.2, 8), aiPantsMat);
    aiRightLeg.position.set(0.25, 0.6, 0);
    aiRightLeg.castShadow = true;
    aiGolferGroup.add(aiRightLeg);

    const aiLeftShoe = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.14, 0.42), aiShoesMat);
    aiLeftShoe.position.set(-0.25, 0.07, 0.06);
    aiGolferGroup.add(aiLeftShoe);

    const aiRightShoe = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.14, 0.42), aiShoesMat);
    aiRightShoe.position.set(0.25, 0.07, 0.06);
    aiGolferGroup.add(aiRightShoe);

    const aiUpperBody = new THREE.Group();
    aiUpperBody.position.set(0, 1.2, 0);

    const aiTorso = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.9, 0.38), aiShirtMat);
    aiTorso.position.y = 0.45;
    aiTorso.castShadow = true;
    aiUpperBody.add(aiTorso);

    const aiHead = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), skinMat);
    aiHead.position.y = 1.15;
    aiHead.castShadow = true;
    aiUpperBody.add(aiHead);

    const aiCap = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.12, 12), aiCapMat);
    aiCap.position.set(0, 1.3, 0);
    aiUpperBody.add(aiCap);

    const aiVisor = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.04, 0.22), aiCapMat);
    aiVisor.position.set(0, 1.28, 0.22);
    aiUpperBody.add(aiVisor);

    const aiSwingPivot = new THREE.Group();
    aiSwingPivot.position.set(0, 0.8, 0.15);

    const aiLeftArm = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.08, 0.8, 8), aiShirtMat);
    aiLeftArm.position.set(-0.28, -0.35, 0.18);
    aiLeftArm.rotation.x = -0.4;
    aiLeftArm.castShadow = true;
    aiSwingPivot.add(aiLeftArm);

    const aiRightArm = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.08, 0.8, 8), aiShirtMat);
    aiRightArm.position.set(0.28, -0.35, 0.18);
    aiRightArm.rotation.x = -0.4;
    aiRightArm.castShadow = true;
    aiSwingPivot.add(aiRightArm);

    const aiHands = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 8), skinMat);
    aiHands.position.set(0, -0.7, 0.35);
    aiSwingPivot.add(aiHands);

    const aiClubGroup = new THREE.Group();
    aiClubGroup.position.set(0, -0.7, 0.35);

    const aiClubShaft = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.25, 8), clubShaftMat);
    aiClubShaft.position.set(0, -0.55, 0.15);
    aiClubShaft.rotation.x = 0.28;
    aiClubShaft.castShadow = true;
    aiClubGroup.add(aiClubShaft);

    const aiClubHead = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.08, 0.18), clubHeadMat);
    aiClubHead.position.set(0.05, -1.15, 0.32);
    aiClubHead.castShadow = true;
    aiClubGroup.add(aiClubHead);

    aiSwingPivot.add(aiClubGroup);
    aiUpperBody.add(aiSwingPivot);
    aiGolferGroup.add(aiUpperBody);
    scene.add(aiGolferGroup);

    function updateAIGolferStance(pos, aimAngle) {
      const standOffsetDist = 0.75;
      const perpAngle = aimAngle - Math.PI / 2;
      const gx = pos.x + Math.sin(perpAngle) * standOffsetDist;
      const gz = pos.z + Math.cos(perpAngle) * standOffsetDist;
      const gy = getTerrainHeight(gx, gz);
      aiGolferGroup.position.set(gx, gy, gz);
      aiGolferGroup.rotation.y = aimAngle + Math.PI / 2;
    }

    function updateAIGolferPose(progress, step) {
      if (step === 'backswing') {
        aiSwingPivot.rotation.z = -progress * 1.5;
        aiSwingPivot.rotation.x = -progress * 0.8;
        aiUpperBody.rotation.y = -progress * 0.5;
      } else if (step === 'downswing') {
        const t = progress;
        aiSwingPivot.rotation.z = -1.5 + t * 2.85;
        aiSwingPivot.rotation.x = -0.8 + t * 1.35;
        aiUpperBody.rotation.y = -0.5 + t * 1.35;
      } else if (step === 'flight' || step === 'followthrough') {
        aiSwingPivot.rotation.z = 1.35;
        aiSwingPivot.rotation.x = 0.55;
        aiUpperBody.rotation.y = 0.85;
      } else {
        aiSwingPivot.rotation.z = 0;
        aiSwingPivot.rotation.x = 0;
        aiUpperBody.rotation.y = 0;
      }
    }`;

content = content.replace(searchAfterPlayerGolfer, newAIGolferModel);

fs.writeFileSync('index.html', content);
console.log('DropZones 3D and AI Golfer model added');
