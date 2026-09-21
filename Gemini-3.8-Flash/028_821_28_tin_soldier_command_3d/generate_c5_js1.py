# -*- coding: utf-8 -*-
import sys

out = []

out.append('''  <script>
  (function() {
    'use strict';

    // --- Deterministic Pseudo-Random Generator (LCG) ---
    // Zero Math.random() usage anywhere in the entire game!
    let _seed = 123456789;
    function deterministicRandom() {
      _seed = (1103515245 * _seed + 12345) & 0x7fffffff;
      return _seed / 0x7fffffff;
    }
    function resetDeterministicSeed() {
      _seed = 123456789;
    }

    // --- Synthesized Audio (Web Audio API) ---
    let audioCtx = null;
    function initAudio() {
      if (!audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
    }
    function playSfx(type) {
      if (!audioCtx) return;
      try {
        const now = audioCtx.currentTime;
        if (type === 'shot') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(420, now);
          osc.frequency.exponentialRampToValueAtTime(80, now + 0.08);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.08);
        } else if (type === 'hit') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'square';
          osc.frequency.setValueAtTime(130, now);
          osc.frequency.exponentialRampToValueAtTime(35, now + 0.06);
          gain.gain.setValueAtTime(0.08, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.06);
        } else if (type === 'drum') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(150, now);
          osc.frequency.exponentialRampToValueAtTime(45, now + 0.09);
          gain.gain.setValueAtTime(0.07, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.09);
        } else if (type === 'wind') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(850, now);
          osc.frequency.linearRampToValueAtTime(1250, now + 0.05);
          gain.gain.setValueAtTime(0.04, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.05);
        } else if (type === 'coin') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(987, now);
          osc.frequency.setValueAtTime(1318, now + 0.08);
          gain.gain.setValueAtTime(0.1, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.22);
        } else if (type === 'catapult') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(110, now);
          osc.frequency.exponentialRampToValueAtTime(40, now + 0.35);
          gain.gain.setValueAtTime(0.15, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.35);
        } else if (type === 'domino') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(320, now);
          osc.frequency.exponentialRampToValueAtTime(120, now + 0.07);
          gain.gain.setValueAtTime(0.09, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.07);
        } else if (type === 'build') {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(550, now);
          osc.frequency.exponentialRampToValueAtTime(880, now + 0.12);
          gain.gain.setValueAtTime(0.1, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
          osc.connect(gain); gain.connect(audioCtx.destination);
          osc.start(now); osc.stop(now + 0.12);
        }
      } catch (e) {}
    }

    // --- Map Bounds & Physics Constants ---
    const MAP_MIN_X = -26, MAP_MAX_X = 26;
    const MAP_MIN_Z = -22, MAP_MAX_Z = 22;
    const GRAVITY = 18.0;
    const CORK_SPEED = 14.0;
    const DRUMMER_AURA_RADIUS = 6.0;
    const COVER_RADIUS = 1.0;
    const TOWER_RADIUS = 7.0;

    // --- State Variables ---
    let gameState = 'ready'; // 'ready', 'playing', 'win', 'lose'
    let gameTime = 0;
    let selectedUnits = [];
    let selectedBuilding = null; // 'barracks'
    let bottlecaps = 50;
    let nextUnitId = 100;
    let nextTileId = 1;
    let nextTowerId = 1;
    const controlGroups = { 1: [], 2: [], 3: [], 4: [] };
    const lastDigitPress = { 1: 0, 2: 0, 3: 0, 4: 0 };
    let attackMoveArmed = false;

    // Build Modes: null, 'domino', 'tower'
    let buildMode = null;
    let dominoDragStartPt = null;
    const dominoPreviewMeshes = [];

    // --- Three.js Setup ---
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0f1d);
    scene.fog = new THREE.FogExp2(0x0a0f1d, 0.016);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.5, 200);
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Camera Rig & Edges
    const cameraTarget = new THREE.Vector3(0, 0, 8);
    let cameraDistance = 26;
    const CAM_MIN_DIST = 12;
    const CAM_MAX_DIST = 42;
    const CAM_PITCH = Math.PI * 0.32;
    const CAM_PAN_SPEED = 18;

    function updateCameraPosition() {
      cameraTarget.x = Math.max(MAP_MIN_X + 6, Math.min(MAP_MAX_X - 6, cameraTarget.x));
      cameraTarget.z = Math.max(MAP_MIN_Z + 4, Math.min(MAP_MAX_Z - 4, cameraTarget.z));
      const cy = Math.sin(CAM_PITCH) * cameraDistance;
      const cz = Math.cos(CAM_PITCH) * cameraDistance;
      camera.position.set(cameraTarget.x, cy, cameraTarget.z + cz);
      camera.lookAt(cameraTarget.x, 0, cameraTarget.z);
    }
    updateCameraPosition();

    // --- Lighting (Nostalgic Moonlit Toybox) ---
    const ambientLight = new THREE.AmbientLight(0x2d3a5a, 0.85);
    scene.add(ambientLight);

    const moonDir = new THREE.DirectionalLight(0xa5c9f5, 1.4);
    moonDir.position.set(-20, 35, 15);
    moonDir.castShadow = true;
    moonDir.shadow.mapSize.width = 2048;
    moonDir.shadow.mapSize.height = 2048;
    moonDir.shadow.camera.near = 5;
    moonDir.shadow.camera.far = 70;
    moonDir.shadow.camera.left = -28;
    moonDir.shadow.camera.right = 28;
    moonDir.shadow.camera.top = 28;
    moonDir.shadow.camera.bottom = -28;
    moonDir.shadow.bias = -0.0005;
    scene.add(moonDir);

    const beamGeo = new THREE.CylinderGeometry(8, 14, 45, 16, 1, true);
    const beamMat = new THREE.MeshBasicMaterial({
      color: 0xa8cbf8,
      transparent: true,
      opacity: 0.045,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    const moonbeamMesh = new THREE.Mesh(beamGeo, beamMat);
    moonbeamMesh.position.set(-8, 18, 5);
    moonbeamMesh.rotation.z = 0.35;
    moonbeamMesh.rotation.x = -0.2;
    scene.add(moonbeamMesh);

    const bedLight = new THREE.PointLight(0x22c55e, 1.6, 22, 1.2);
    bedLight.position.set(0, 3, -19);
    scene.add(bedLight);

    const bedRed = new THREE.PointLight(0xef4444, 0.8, 16, 1.5);
    bedRed.position.set(6, 2, -18);
    scene.add(bedRed);

    const baseLight = new THREE.PointLight(0xf59e0b, 1.2, 14, 1.4);
    baseLight.position.set(0, 2.5, 14);
    scene.add(baseLight);

    // --- Environment Obstacles & Displaceable Blocks ---
    const obstacles = [];
    const woodenBlocks = [];

    // Floor
    const floorGeo = new THREE.PlaneGeometry(60, 50);
    const floorCanvas = document.createElement('canvas');
    floorCanvas.width = 1024;
    floorCanvas.height = 1024;
    const fctx = floorCanvas.getContext('2d');
    fctx.fillStyle = '#1e140d';
    fctx.fillRect(0, 0, 1024, 1024);
    fctx.strokeStyle = '#120b06';
    fctx.lineWidth = 3;
    for (let y = 0; y < 1024; y += 32) {
      fctx.beginPath(); fctx.moveTo(0, y); fctx.lineTo(1024, y); fctx.stroke();
    }
    const rugX = 160, rugY = 160, rugW = 704, rugH = 704;
    fctx.fillStyle = '#1e293b';
    fctx.fillRect(rugX - 12, rugY - 12, rugW + 24, rugH + 24);
    const sqSize = 44;
    for (let r = 0; r < rugH / sqSize; r++) {
      for (let c = 0; c < rugW / sqSize; c++) {
        fctx.fillStyle = (r + c) % 2 === 0 ? '#334155' : '#475569';
        fctx.fillRect(rugX + c * sqSize, rugY + r * sqSize, sqSize, sqSize);
      }
    }
    const floorTex = new THREE.CanvasTexture(floorCanvas);
    floorTex.wrapS = floorTex.wrapT = THREE.ClampToEdgeWrapping;
    const floorMat = new THREE.MeshStandardMaterial({ map: floorTex, roughness: 0.75, metalness: 0.15 });
    const floorMesh = new THREE.Mesh(floorGeo, floorMat);
    floorMesh.rotation.x = -Math.PI / 2;
    floorMesh.receiveShadow = true;
    scene.add(floorMesh);

    // Bed Frame
    const bedGroup = new THREE.Group();
    bedGroup.position.set(0, 0, -21);
    const bedBoardGeo = new THREE.BoxGeometry(46, 7, 1.8);
    const bedWoodMat = new THREE.MeshStandardMaterial({ color: 0x271911, roughness: 0.8 });
    const bedBoard = new THREE.Mesh(bedBoardGeo, bedWoodMat);
    bedBoard.position.set(0, 3.5, -1);
    bedBoard.castShadow = true;
    bedBoard.receiveShadow = true;
    bedGroup.add(bedBoard);

    const mattressGeo = new THREE.BoxGeometry(46, 2.5, 12);
    const mattressMat = new THREE.MeshStandardMaterial({ color: 0x111625, roughness: 0.9 });
    const mattress = new THREE.Mesh(mattressGeo, mattressMat);
    mattress.position.set(0, 6, -6);
    mattress.castShadow = true;
    bedGroup.add(mattress);

    [-22, 22].forEach(px => {
      const post = new THREE.Mesh(new THREE.BoxGeometry(1.4, 7, 1.4), bedWoodMat);
      post.position.set(px, 3.5, 0);
      post.castShadow = true;
      bedGroup.add(post);
    });
    scene.add(bedGroup);

    const bedBox = new THREE.Box3().setFromObject(bedBoard);
    bedBox.min.z -= 4;
    obstacles.push({ box: bedBox, isBlock: false, name: 'bedFrame' });

    // Wooden Building Blocks
    const woodBlockMat1 = new THREE.MeshStandardMaterial({ color: 0xc28847, roughness: 0.6, metalness: 0.05 });
    const woodBlockMat2 = new THREE.MeshStandardMaterial({ color: 0xa86732, roughness: 0.6, metalness: 0.05 });
    const woodBlockMat3 = new THREE.MeshStandardMaterial({ color: 0xd99b58, roughness: 0.6, metalness: 0.05 });

    function createWoodenBlock(x, z, sx, sy, sz, rotY, mat) {
      const geo = new THREE.BoxGeometry(sx, sy, sz);
      const mesh = new THREE.Mesh(geo, mat || woodBlockMat1);
      mesh.position.set(x, sy / 2, z);
      mesh.rotation.y = rotY || 0;
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      scene.add(mesh);
      mesh.updateMatrixWorld(true);

      const box = new THREE.Box3().setFromObject(mesh);
      const blockRecord = {
        mesh: mesh,
        sx: sx, sy: sy, sz: sz,
        initialPos: new THREE.Vector3(x, sy / 2, z),
        initialRot: new THREE.Euler(0, rotY || 0, 0),
        box: box,
        isBlock: true,
        toppled: false
      };
      woodenBlocks.push(blockRecord);
      obstacles.push(blockRecord);
      return mesh;
    }

    createWoodenBlock(-7.5, 6.0, 3.2, 1.4, 1.4, 0.2, woodBlockMat1);
    createWoodenBlock(-9.0, 5.0, 1.6, 2.2, 1.6, 0.0, woodBlockMat2);
    createWoodenBlock(-6.2, 6.8, 1.8, 1.2, 1.8, -0.4, woodBlockMat3);

    createWoodenBlock(7.5, 6.5, 3.4, 1.4, 1.4, -0.25, woodBlockMat3);
    createWoodenBlock(9.2, 5.5, 1.6, 2.2, 1.6, 0.1, woodBlockMat1);
    createWoodenBlock(6.0, 7.2, 1.6, 1.3, 1.6, 0.35, woodBlockMat2);

    createWoodenBlock(-1.5, 1.0, 2.8, 1.5, 1.5, 0.1, woodBlockMat2);
    createWoodenBlock(1.8, 0.5, 3.0, 1.5, 1.5, -0.15, woodBlockMat1);
    createWoodenBlock(0.2, 0.8, 2.0, 1.4, 1.6, 0.05, woodBlockMat3);

    createWoodenBlock(-11.0, -6.5, 3.6, 1.5, 1.5, 0.3, woodBlockMat1);
    createWoodenBlock(11.0, -6.0, 3.6, 1.5, 1.5, -0.3, woodBlockMat2);
    createWoodenBlock(0.0, -8.0, 4.0, 1.6, 1.6, 0.0, woodBlockMat3);

    // Hardcover Book Lying Flat
    const bookGroup = new THREE.Group();
    bookGroup.position.set(-6, 0.45, -1.5);
    bookGroup.rotation.y = 0.32;
    const bookCover = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.9, 6.4), new THREE.MeshStandardMaterial({ color: 0x831843, roughness: 0.5 }));
    bookCover.castShadow = true; bookCover.receiveShadow = true;
    bookGroup.add(bookCover);
    const pages = new THREE.Mesh(new THREE.BoxGeometry(4.3, 0.76, 6.1), new THREE.MeshStandardMaterial({ color: 0xfef08a, roughness: 0.9 }));
    pages.position.set(0.12, 0, 0);
    bookGroup.add(pages);
    scene.add(bookGroup);
    bookGroup.updateMatrixWorld(true);
    obstacles.push({ box: new THREE.Box3().setFromObject(bookGroup), isBlock: false, mesh: bookGroup });

    // Fence Line of Fallen Pencils
    const pencilColors = [0xef4444, 0x3b82f6, 0x10b981, 0xf59e0b, 0x8b5cf6];
    function createFallenPencil(x, z, rotY, colorIdx) {
      const penGroup = new THREE.Group();
      penGroup.position.set(x, 0.22, z);
      penGroup.rotation.y = rotY;

      const body = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 5.0, 6), new THREE.MeshStandardMaterial({ color: pencilColors[colorIdx % pencilColors.length], roughness: 0.5 }));
      body.rotation.z = Math.PI / 2;
      body.castShadow = true; body.receiveShadow = true;
      penGroup.add(body);

      const tip = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.7, 6), new THREE.MeshStandardMaterial({ color: 0xfde68a, roughness: 0.8 }));
      tip.rotation.z = -Math.PI / 2; tip.position.set(2.85, 0, 0);
      penGroup.add(tip);

      const lead = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.25, 6), new THREE.MeshBasicMaterial({ color: 0x111827 }));
      lead.rotation.z = -Math.PI / 2; lead.position.set(3.25, 0, 0);
      penGroup.add(lead);

      const fer = new THREE.Mesh(new THREE.CylinderGeometry(0.23, 0.23, 0.5, 8), new THREE.MeshStandardMaterial({ color: 0xd1d5db, metalness: 0.8, roughness: 0.3 }));
      fer.rotation.z = Math.PI / 2; fer.position.set(-2.6, 0, 0);
      penGroup.add(fer);

      const ers = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.21, 0.5, 8), new THREE.MeshStandardMaterial({ color: 0xf472b6, roughness: 0.7 }));
      ers.rotation.z = Math.PI / 2; ers.position.set(-3.0, 0, 0);
      penGroup.add(ers);

      scene.add(penGroup);
      penGroup.updateMatrixWorld(true);
      obstacles.push({ box: new THREE.Box3().setFromObject(penGroup), isBlock: false, mesh: penGroup });
    }

    createFallenPencil(5.5, -2.5, 0.15, 0);
    createFallenPencil(10.2, -2.0, -0.1, 1);
    createFallenPencil(14.8, -2.2, 0.2, 2);
    createFallenPencil(-14.0, -11.0, 0.7, 3);
    createFallenPencil(13.0, -12.0, -0.6, 4);

    function displaceBlock(block, impactPos) {
      const curX = block.mesh.position.x;
      const curZ = block.mesh.position.z;
      const dirX = curX - impactPos.x;
      const dirZ = curZ - impactPos.z;
      let len = Math.hypot(dirX, dirZ);
      let nx = 0, nz = 1;
      if (len > 0.001) {
        nx = dirX / len;
        nz = dirZ / len;
      }
      const targetX = Math.max(MAP_MIN_X + 2, Math.min(MAP_MAX_X - 2, curX + nx * 1.5));
      const targetZ = Math.max(MAP_MIN_Z + 2, Math.min(MAP_MAX_Z - 2, curZ + nz * 1.5));

      block.mesh.position.x = targetX;
      block.mesh.position.z = targetZ;
      block.mesh.position.y = Math.min(block.sx, block.sz) / 2;
      block.mesh.rotation.z = Math.PI / 2;
      block.mesh.rotation.x = 0.2;
      block.mesh.updateMatrixWorld(true);

      block.box.setFromObject(block.mesh);
      block.toppled = true;
    }
''')

with open('c5_part2.js', 'w') as f:
    f.write(''.join(out))
print("Part 2 written")
