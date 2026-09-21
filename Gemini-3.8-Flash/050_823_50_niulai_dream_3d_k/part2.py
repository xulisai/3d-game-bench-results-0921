# Part 2: Constants, State, Math, Terrain Elevation
part2 = r"""
  <script>
  (function() {
    'use strict';

    // --- Deterministic PRNG (Linear Congruential Generator) ---
    // Strictly NO standard random functions in the game!
    let _seed = 123456789;
    function deterministicRandom() {
      _seed = (_seed * 1664525 + 1013904223) >>> 0;
      return _seed / 4294967296;
    }
    function resetPRNG(seed) {
      _seed = seed || 123456789;
    }

    // --- Global Game State ---
    const STATE = {
      isReady: false,
      realm: "reality", // "reality" or "dream"
      elapsedTime: 0,
      zoneName: "Waking Meadow",
      strikes: 0,
      wadeFactor: 0.35,
      wolfRadius: 7.5,
      wolfDwell: 0.8,
      herdSpeed: 1.6,
      motesPresent: false,
      larkGuide: "meadow",
      copyZone: false,
      awake: false,
      log: [],
      memories: {
        meadow: false,
        hollow: false,
        ford: false,
        steppe: false,
        canyon: false,
        niche: false,
        count: 0
      },
      veil1: "standing", // "standing", "dissolving", "dissolved"
      veil1FadeTimer: 0,
      veil2: "standing", // "standing", "dissolving", "dissolved"
      veil2FadeTimer: 0,
      rocks: "blocking", // "blocking", "lowering", "cleared"
      rocksLowerTimer: 0,
      herdPhase: "gathered", // "gathered", "walking", "settled"
      migrationStartTime: 0,
      motherLainDown: false,
      player: {
        pos: [35, 0, 30], // meadow spawn at (35, 30)
        rotation: Math.PI,
        speed: 0,
        targetSpeed: 0,
        wading: false,
        stepCycle: 0
      },
      bola: {
        state: "atHollow", // 'atHollow' / 'following' / 'waiting' / 'bankWaiting'
        pos: [95, 0, 15],
        rotation: -Math.PI * 0.6,
        pose: "sitting",
        trotCycle: 0,
        speed: 0,
        isCatchingUp: false
      },
      snake: {
        fled: false,
        fleeing: false,
        fleeTime: 0,
        pos: [120, 0, -55]
      },
      wolves: [
        { id: 1, pos: [344, 0, -9], dwellTimer: 0, retreating: false, retreatTimer: 0, vanished: false },
        { id: 2, pos: [368, 0, 7],  dwellTimer: 0, retreating: false, retreatTimer: 0, vanished: false },
        { id: 3, pos: [380, 0, -7], dwellTimer: 0, retreating: false, retreatTimer: 0, vanished: false },
        { id: 4, pos: [396, 0, 5],  dwellTimer: 0, retreating: false, retreatTimer: 0, vanished: false }
      ],
      herd: [],
      isFading: false,
      isCaughtFading: false
    };
    window.__game = STATE;

    // Helper: format mm:ss
    function formatTime(sec) {
      const m = Math.floor(sec / 60);
      const s = Math.floor(sec % 60);
      return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }

    // Export to window.__arena_state
    function updateArenaState() {
      // Determine lark target
      let currentGuide = "player";
      if (STATE.realm === "reality") {
        currentGuide = "meadow";
      } else {
        if (!STATE.memories.hollow) currentGuide = "hollow";
        else if (!STATE.memories.ford) currentGuide = "ford";
        else if (!STATE.memories.steppe) currentGuide = "steppe";
        else if (!STATE.memories.canyon) currentGuide = "canyon";
        else if (!STATE.memories.niche) currentGuide = "niche";
        else currentGuide = "player";
      }
      STATE.larkGuide = currentGuide;

      // Copy zone check
      const px = STATE.player.pos[0];
      const pz = STATE.player.pos[2];
      STATE.copyZone = (STATE.realm === "dream" && px >= 410 && px <= 480 && pz >= -40 && pz <= 40);

      const herdArr = STATE.herd.map(c => ({
        id: c.id,
        pos: [
          parseFloat(c.pos[0].toFixed(3)),
          parseFloat(c.pos[1].toFixed(3)),
          parseFloat(c.pos[2].toFixed(3))
        ]
      }));
      herdArr.phase = STATE.herdPhase;
      herdArr.positions = herdArr.map(c => c.pos);

      window.__arena_state = {
        realm: STATE.realm,
        zone: STATE.zoneName,
        player: {
          pos: [
            parseFloat(STATE.player.pos[0].toFixed(3)),
            parseFloat(STATE.player.pos[1].toFixed(3)),
            parseFloat(STATE.player.pos[2].toFixed(3))
          ],
          speed: parseFloat(STATE.player.speed.toFixed(3)),
          wading: STATE.player.wading
        },
        memories: {
          meadow: STATE.memories.meadow,
          hollow: STATE.memories.hollow,
          ford: STATE.memories.ford,
          steppe: STATE.memories.steppe,
          canyon: STATE.memories.canyon,
          niche: STATE.memories.niche,
          count: STATE.memories.count
        },
        veil1: STATE.veil1 === "dissolving" ? "dissolving" : (STATE.veil1 === "dissolved" ? "dissolved" : "standing"),
        veil2: STATE.veil2 === "dissolving" ? "dissolving" : (STATE.veil2 === "dissolved" ? "dissolved" : "standing"),
        rocks: STATE.rocks === "cleared" ? "cleared" : "blocking",
        strikes: STATE.strikes,
        wadeFactor: STATE.wadeFactor,
        wolfRadius: STATE.wolfRadius,
        wolfDwell: STATE.wolfDwell,
        herdSpeed: STATE.herdSpeed,
        motesPresent: STATE.motesPresent,
        larkGuide: STATE.larkGuide,
        copyZone: STATE.copyZone,
        awake: STATE.awake,
        log: STATE.log,
        herd: herdArr,
        wolves: STATE.wolves.map(w => ({
          id: w.id,
          pos: [
            parseFloat(w.pos[0].toFixed(3)),
            parseFloat(w.pos[1].toFixed(3)),
            parseFloat(w.pos[2].toFixed(3))
          ]
        })),
        bola: {
          state: STATE.bola.state,
          pos: [
            parseFloat(STATE.bola.pos[0].toFixed(3)),
            parseFloat(STATE.bola.pos[1].toFixed(3)),
            parseFloat(STATE.bola.pos[2].toFixed(3))
          ]
        },
        snake: {
          fled: STATE.snake.fled,
          pos: [
            parseFloat(STATE.snake.pos[0].toFixed(3)),
            parseFloat(STATE.snake.pos[1].toFixed(3)),
            parseFloat(STATE.snake.pos[2].toFixed(3))
          ]
        }
      };
    }

    // --- Three.js Setup ---
    const canvas = document.getElementById('game-canvas');
    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      powerPreference: "high-performance"
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const camera = new THREE.PerspectiveCamera(54, window.innerWidth / window.innerHeight, 0.4, 600);
    const scene = new THREE.Scene();

    const realityGroup = new THREE.Group();
    const dreamGroup = new THREE.Group();
    scene.add(realityGroup);

    // Environments:
    const ambientLight = new THREE.AmbientLight(0xd5dbd8, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xe4e9e8, 0.45);
    dirLight.position.set(50, 80, 40);
    scene.add(dirLight);

    // Warm evening light shaft in Wolf Pass canyon opening (x > 395)
    const canyonShaftLight = new THREE.PointLight(0xffaa44, 1.8, 45, 1.2);
    canyonShaftLight.position.set(402, 6.0, 0);
    dreamGroup.add(canyonShaftLight);

    const shaftBeamGeo = new THREE.CylinderGeometry(0.8, 5.0, 14.0, 8, 1, true);
    shaftBeamGeo.rotateZ(0.25);
    const shaftBeamMat = new THREE.MeshBasicMaterial({
      color: 0xffb855,
      transparent: true,
      opacity: 0.22,
      side: THREE.DoubleSide
    });
    const shaftMesh = new THREE.Mesh(shaftBeamGeo, shaftBeamMat);
    shaftMesh.position.set(400, 7.0, 0);
    dreamGroup.add(shaftMesh);

    function applyEnvironmentSettings(realm) {
      if (realm === "reality") {
        scene.background = new THREE.Color(0x3b4541);
        scene.fog = new THREE.Fog(0x525c58, 25, 95);
        ambientLight.color.setHex(0xd5dbd8);
        ambientLight.intensity = 0.7;
        dirLight.color.setHex(0xe4e9e8);
        dirLight.intensity = 0.45;
        renderer.setClearColor(0x3b4541, 1);
      } else {
        scene.background = new THREE.Color(0xc48958);
        scene.fog = new THREE.Fog(0xb88658, 45, 190);
        ambientLight.color.setHex(0xf2c499);
        ambientLight.intensity = 0.72;
        dirLight.color.setHex(0xffd699);
        dirLight.intensity = 0.55;
        renderer.setClearColor(0xc48958, 1);
      }
    }
    applyEnvironmentSettings("reality");

    // =========================================================
    // 1. ELEVATION FUNCTIONS
    // =========================================================
    function getMeadowElevation(x, z) {
      let edgeElev = 0;
      if (x < 10) edgeElev += Math.pow((10 - x) / 10, 2) * 14;
      if (x > 60) edgeElev += Math.pow((x - 60) / 10, 2) * 14;
      if (z < -32) edgeElev += Math.pow((-32 - z) / 8, 2) * 14;
      if (z > 32) edgeElev += Math.pow((z - 32) / 8, 2) * 14;

      const m1 = Math.sin(x * 0.08 + 0.4) * Math.cos(z * 0.09) * 0.75;
      const m2 = Math.cos(x * 0.05 - 0.7) * Math.sin(z * 0.06 + 0.5) * 0.5;
      return m1 + m2 + edgeElev;
    }

    function getMeadowNormal(x, z) {
      const d = 0.3;
      const yL = getMeadowElevation(x - d, z);
      const yR = getMeadowElevation(x + d, z);
      const yD = getMeadowElevation(x, z - d);
      const yU = getMeadowElevation(x, z + d);
      return new THREE.Vector3((yL - yR) / (2 * d), 1.0, (yD - yU) / (2 * d)).normalize();
    }

    function getStreamCenter(z) {
      if (z <= -30) {
        const u = (z - (-110)) / 80;
        return 40 + u * 30 + Math.sin(u * Math.PI) * 4.2;
      } else if (z <= 40) {
        const u = (z - (-30)) / 70;
        return 70 + u * 60 + Math.sin(u * Math.PI) * -5.0;
      } else {
        const u = (z - 40) / 70;
        return 130 + u * 30 + Math.sin(u * Math.PI) * 3.8;
      }
    }

    const FORD_1 = { x: 70, z: -30, r: 7.0 };
    const FORD_2 = { x: 130, z: 40, r: 7.0 };

    function smoothstep(edge0, edge1, x) {
      const t = Math.max(0, Math.min(1, (x - edge0) / (edge1 - edge0)));
      return t * t * (3 - 2 * t);
    }

    function rawGrassland(x, z) {
      const h1 = Math.sin(x * 0.045 + 0.8) * Math.cos(z * 0.04 - 0.4) * 1.5;
      const h2 = Math.cos(x * 0.026 - 1.2) * Math.sin(z * 0.032 + 0.9) * 1.2;
      const h3 = Math.sin((x + z) * 0.02) * 0.5;
      let y = (h1 + h2 + h3) * 0.85;

      const distHollow = Math.hypot(x - 95, z - 15);
      if (distHollow < 14) y -= Math.pow(1 - distHollow / 14, 2) * 1.5;

      const streamX = getStreamCenter(z);
      const distToStream = Math.abs(x - streamX);
      if (distToStream < 2.0) {
        const dFord1 = Math.hypot(x - FORD_1.x, z - FORD_1.z);
        const dFord2 = Math.hypot(x - FORD_2.x, z - FORD_2.z);
        let streamDepth = 0.35;
        if (dFord1 < FORD_1.r) streamDepth = THREE.MathUtils.lerp(0.15, 0.35, dFord1 / FORD_1.r);
        else if (dFord2 < FORD_2.r) streamDepth = THREE.MathUtils.lerp(0.15, 0.35, dFord2 / FORD_2.r);
        y -= Math.cos((distToStream / 2.0) * (Math.PI / 2)) * streamDepth;
      }
      return y;
    }

    function rawSteppe(x, z) {
      const s1 = Math.sin(x * 0.035 + 0.5) * Math.cos(z * 0.035) * 0.9;
      const s2 = Math.cos(x * 0.02 - 0.4) * Math.sin(z * 0.025 + 0.3) * 0.7;
      let y = s1 + s2;
      const distGully = Math.abs(z - (-20));
      if (distGully < 1.5) y -= Math.cos((distGully / 1.5) * (Math.PI / 2)) * 1.2;
      return y;
    }

    function rawCanyon(x, z) {
      let y = Math.sin(x * 0.05) * 0.3;
      const distStreamlet = Math.abs(z - (-6));
      if (distStreamlet < 1.2) {
        y -= Math.cos((distStreamlet / 1.2) * (Math.PI / 2)) * 0.25;
      }
      return y;
    }

    function rawEasternMeadow(x, z) {
      if (Math.abs(z) <= 40) {
        return getMeadowElevation(x - 410, z);
      }
      return Math.sin(x * 0.04) * Math.cos(z * 0.035) * 1.0;
    }

    function getGrasslandElevation(x, z) {
      let base = 0;
      if (x < 190) base = rawGrassland(x, z);
      else if (x < 210) {
        const t = smoothstep(190, 210, x);
        base = (1 - t) * rawGrassland(x, z) + t * rawSteppe(x, z);
      } else if (x < 320) base = rawSteppe(x, z);
      else if (x < 335) {
        const t = smoothstep(320, 335, x);
        base = (1 - t) * rawSteppe(x, z) + t * rawCanyon(x, z);
      } else if (x < 405) base = rawCanyon(x, z);
      else if (x < 420) {
        const t = smoothstep(405, 420, x);
        base = (1 - t) * rawCanyon(x, z) + t * rawEasternMeadow(x, z);
      } else base = rawEasternMeadow(x, z);

      // Boundaries & Walls:
      let wallElev = 0;
      // West edge (x < 16)
      if (x < 16) wallElev += Math.pow((16 - x) / 16, 2) * 18;

      // North / South edges
      if (x <= 330) {
        if (z < -96) wallElev += Math.pow((-96 - z) / 14, 2) * 20;
        if (z > 96) wallElev += Math.pow((z - 96) / 14, 2) * 20;
        if (x > 175 && x <= 200 && Math.abs(z) > 50) {
          wallElev += Math.pow((x - 175) / 25, 2) * 20;
        }
        if (x > 320 && Math.abs(z) > 12) {
          const u = (x - 320) / 10;
          wallElev += u * Math.min(12.0, (Math.abs(z) - 12) * 1.2);
        }
      } else if (x <= 410) {
        // Canyon corridor: z in [-12, 12]
        // Niche at (404, -8)
        const distNiche = Math.hypot(x - 404, z - (-8));
        if (distNiche < 3.2) {
          wallElev = 0;
        } else if (Math.abs(z) > 12) {
          const dz = Math.abs(z) - 12;
          wallElev += Math.min(13.5, 3.5 + Math.floor(dz / 2.0) * 2.5 + dz * 0.8);
        }
      } else {
        // Dream's Edge
        if (Math.abs(z) > 40) {
          const dz = Math.abs(z) - 40;
          wallElev += Math.min(22.0, Math.pow(dz / 15, 2) * 16);
        }
        if (x > 470) {
          wallElev += Math.pow((x - 470) / 10, 2) * 22;
        }
      }

      return base + wallElev;
    }

    function checkWaterAt(x, z) {
      if (STATE.realm !== "dream") return { inWater: false, depth: 0 };
      if (x <= 200) {
        const streamX = getStreamCenter(z);
        const dist = Math.abs(x - streamX);
        if (dist <= 2.0) {
          const dFord1 = Math.hypot(x - FORD_1.x, z - FORD_1.z);
          const dFord2 = Math.hypot(x - FORD_2.x, z - FORD_2.z);
          let depth = 0.35;
          if (dFord1 < FORD_1.r || dFord2 < FORD_2.r) depth = 0.15;
          return { inWater: true, depth: depth };
        }
      } else if (x >= 330 && x <= 410) {
        const dist = Math.abs(z - (-6));
        if (dist <= 1.2) return { inWater: true, depth: 0.25 };
      }
      return { inWater: false, depth: 0 };
    }

    function getGrasslandNormal(x, z) {
      const delta = 0.3;
      const yL = getGrasslandElevation(x - delta, z);
      const yR = getGrasslandElevation(x + delta, z);
      const yD = getGrasslandElevation(x, z - delta);
      const yU = getGrasslandElevation(x, z + delta);
      return new THREE.Vector3((yL - yR) / (2 * delta), 1.0, (yD - yU) / (2 * delta)).normalize();
    }

    function getCurrentElevation(x, z) {
      return STATE.realm === "dream" ? getGrasslandElevation(x, z) : getMeadowElevation(x, z);
    }
    function getCurrentNormal(x, z) {
      return STATE.realm === "dream" ? getGrasslandNormal(x, z) : getMeadowNormal(x, z);
    }
"""
