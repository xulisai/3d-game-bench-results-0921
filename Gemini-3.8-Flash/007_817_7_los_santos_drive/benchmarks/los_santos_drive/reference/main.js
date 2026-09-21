/**
 * Main Game Loop for Los Santos Drive
 * Renders Three.js scene, updates world systems, binds controls, and exposes window.__arena_state every frame.
 */

import * as THREE from 'three';
import { RoadGraph } from './roads.js';
import { DayNightClock } from './clock.js';
import { City } from './city.js';
import { PlayerVehicle, TrafficSystem } from './vehicles.js';
import { PedestrianSystem } from './pedestrians.js';
import { MissionSystem } from './missions.js';
import { PoliceSystem } from './police.js';
import { OnFootCharacter } from './character.js';

export class Game {
  constructor() {
    this.container = document.getElementById('canvas-container');

    // 1. Scene, Camera, Renderer
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(
      65,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );

    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: 'high-performance'
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.container.appendChild(this.renderer.domElement);

    // 2. Core Game Systems
    this.clock = new DayNightClock(this.scene);
    this.roadGraph = new RoadGraph();
    this.city = new City(this.scene, this.roadGraph, this.clock);
    this.playerCar = new PlayerVehicle(this.scene, this.roadGraph);
    this.traffic = new TrafficSystem(this.scene, this.roadGraph);
    this.pedestrians = new PedestrianSystem(this.scene, this.roadGraph);
    this.missions = new MissionSystem(this.scene, this.roadGraph);
    this.police = new PoliceSystem(this.scene, this.roadGraph);
    this.character = new OnFootCharacter(this.scene);

    // Player Mode ('drive' or 'foot')
    this.mode = 'drive';

    // Heat & Crime state (Round 2 wanted system)
    this.heat = 0.0;
    this.wantedStars = 0;
    this.lastCrimeTime = -100.0;
    this.lastTrafficCrimeTime = -100.0;
    this.escapeTimer = 0.0;

    this.addCrime = (type, amount) => {
      this.heat = Math.min(5.0, this.heat + amount);
      this.wantedStars = Math.min(5, Math.floor(this.heat));
      this.lastCrimeTime = this.elapsedTime;
      this.escapeTimer = 0.0;
    };

    // Knocking down a pedestrian adds 1.2 heat
    this.pedestrians.onPedKnockedDown = () => {
      this.addCrime('ped', 1.2);
    };

    // Colliding with traffic car adds 0.28 heat
    this.playerCar.onTrafficCollision = () => {
      if (this.elapsedTime - this.lastTrafficCrimeTime > 0.8) {
        this.lastTrafficCrimeTime = this.elapsedTime;
        this.addCrime('traffic', 0.28);
      }
    };

    // 3. Timing
    this.lastFrameTime = performance.now();
    this.elapsedTime = 0;

    // 4. Input Management
    this.keys = {};
    this.setupInputListeners();

    // 5. HUD References
    this.initHUD();

    // 6. Camera smooth follow vectors
    this.camTargetPos = new THREE.Vector3();
    this.camLookAtPos = new THREE.Vector3();

    // Resize handler
    window.addEventListener('resize', () => this.onWindowResize());

    // Start loop
    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  setupInputListeners() {
    const onKeyDown = (e) => {
      this.keys[e.code] = true;
      if (e.key) this.keys[e.key] = true;

      // Accept mission with M
      if (e.code === 'KeyM' || e.key === 'm' || e.key === 'M') {
        this.missions.acceptJob();
      }

      // Recover wrecked car with R
      if (e.code === 'KeyR' || e.key === 'r' || e.key === 'R') {
        if (this.mode === 'drive') {
          this.playerCar.resetToNearestRoad();
        } else {
          const nearest = this.roadGraph.getNearestLane(this.character.x, this.character.z);
          if (nearest) {
            this.character.x = nearest.point.x;
            this.character.z = nearest.point.z;
            this.character.yaw = nearest.heading;
          }
        }
      }

      // Enter / Exit vehicle with KeyF
      if (e.code === 'KeyF' || e.key === 'f' || e.key === 'F') {
        const now = performance.now();
        if (now - (this.lastFTime || 0) < 250) return;
        this.lastFTime = now;
        this.togglePlayerMode();
      }
    };

    const onKeyUp = (e) => {
      this.keys[e.code] = false;
    };

    // Listen on both window and document for automated harness support
    window.addEventListener('keydown', onKeyDown, { passive: false });
    document.addEventListener('keydown', onKeyDown, { passive: false });
    window.addEventListener('keyup', onKeyUp);
    document.addEventListener('keyup', onKeyUp);
  }

  togglePlayerMode() {
    if (this.mode === 'drive') {
      // Rule: "车速低于 25 km/h 时按 F 下车，变成第三人称步行"
      if (this.playerCar.speedKmh < 25.0) {
        this.mode = 'foot';
        // Spawn character on driver side of car
        const leftX = -Math.cos(this.playerCar.yaw) * 1.8;
        const leftZ = Math.sin(this.playerCar.yaw) * 1.8;
        this.character.spawnAt(
          this.playerCar.x + leftX,
          0.1,
          this.playerCar.z + leftZ,
          this.playerCar.yaw
        );
        this.playerCar.speed = 0;
        this.playerCar.speedKmh = 0;
        this.playerCar.throttle = 0;
        this.playerCar.brake = 0;
      }
    } else {
      // In foot mode: "走到任何车旁边按 F 就能上车开走——抢有主的车会被举报加热度，借停着的车不会。"
      const px = this.character.x;
      const pz = this.character.z;

      // 1. Check distance to parked hero car
      const distToHero = Math.hypot(px - this.playerCar.x, pz - this.playerCar.z);
      if (distToHero <= 4.5) {
        // Enter hero car: no heat added!
        this.character.hide();
        this.mode = 'drive';
        return;
      }

      // 2. Check distance to traffic cars
      let nearestTraffic = null;
      let minTrafficDist = 4.5;
      for (const tCar of this.traffic.activeCars) {
        const d = Math.hypot(px - tCar.x, pz - tCar.z);
        if (d < minTrafficDist) {
          minTrafficDist = d;
          nearestTraffic = tCar;
        }
      }

      if (nearestTraffic) {
        // Jack traffic car: "抢有主的车会被举报加热度" (+0.28 heat)
        this.addCrime('carjack', 0.28);

        // Take over this car: move playerCar to its spot
        this.playerCar.x = nearestTraffic.x;
        this.playerCar.z = nearestTraffic.z;
        this.playerCar.yaw = nearestTraffic.yaw;
        this.playerCar.speed = 0;
        this.playerCar.speedKmh = 0;
        this.playerCar.health = 100;
        this.playerCar.wrecked = false;
        this.playerCar.group.position.set(nearestTraffic.x, 0.35, nearestTraffic.z);
        this.playerCar.group.rotation.set(0, nearestTraffic.yaw, 0);

        // Respawn the traffic car elsewhere so traffic_count stays constant
        const idx = this.traffic.activeCars.indexOf(nearestTraffic);
        if (idx >= 0) {
          this.traffic.scene.remove(nearestTraffic.group);
          this.traffic.activeCars.splice(idx, 1);
          this.traffic.spawnCar();
        }

        this.character.hide();
        this.mode = 'drive';
      }
    }
  }

  initHUD() {
    this.hudClock = document.getElementById('clock-display');
    this.hudHour = document.getElementById('hour-val');
    this.hudHealthText = document.getElementById('health-text');
    this.hudHealthBar = document.getElementById('health-bar-fill');
    this.hudJobsDone = document.getElementById('jobs-done-val');
    this.hudReputation = document.getElementById('reputation-val');
    this.hudTraffic = document.getElementById('traffic-count-val');
    this.hudPeds = document.getElementById('peds-count-val');
    this.hudMissionStatus = document.getElementById('mission-status');
    this.hudSpeed = document.getElementById('speed-display');
    this.hudGear = document.getElementById('gear-display');

    this.missionBanner = document.getElementById('mission-banner');
    this.missionTitle = document.getElementById('mission-title');
    this.missionDesc = document.getElementById('mission-desc');
    this.missionTimer = document.getElementById('mission-timer');

    this.hudPlayerMode = document.getElementById('player-mode-val');
    this.hudWantedStars = document.getElementById('wanted-stars-val');
    this.hudHeat = document.getElementById('heat-val');
    this.hudCops = document.getElementById('cops-count-val');
  }

  updateInputs() {
    if (this.mode === 'drive') {
      const forward = this.keys['KeyW'] || this.keys['ArrowUp'];
      const backward = this.keys['KeyS'] || this.keys['ArrowDown'];
      const left = this.keys['KeyA'] || this.keys['ArrowLeft'];
      const right = this.keys['KeyD'] || this.keys['ArrowRight'];
      const space = this.keys['Space'];

      this.playerCar.throttle = forward ? 1.0 : 0.0;
      this.playerCar.brake = backward ? 1.0 : 0.0;
      this.playerCar.steer = (left ? -1.0 : 0.0) + (right ? 1.0 : 0.0);
      this.playerCar.handbrake = Boolean(space);
    } else {
      this.playerCar.throttle = 0;
      this.playerCar.brake = 0;
      this.playerCar.steer = 0;
      this.playerCar.handbrake = true;
    }
  }

  updateCamera(dt) {
    if (this.mode === 'foot') {
      const forwardX = -Math.sin(this.character.yaw);
      const forwardZ = -Math.cos(this.character.yaw);

      const targetX = this.character.x - forwardX * 4.2;
      const targetY = this.character.y + 2.2;
      const targetZ = this.character.z - forwardZ * 4.2;

      this.camTargetPos.set(targetX, targetY, targetZ);
      this.camera.position.lerp(this.camTargetPos, Math.min(1.0, dt * 10.0));

      const lookX = this.character.x + forwardX * 2.0;
      const lookY = this.character.y + 1.4;
      const lookZ = this.character.z + forwardZ * 2.0;

      this.camLookAtPos.set(lookX, lookY, lookZ);
      this.camera.lookAt(this.camLookAtPos);
    } else {
      const forwardX = -Math.sin(this.playerCar.yaw);
      const forwardZ = -Math.cos(this.playerCar.yaw);

      const targetX = this.playerCar.x - forwardX * 6.5;
      const targetY = this.playerCar.y + 2.4;
      const targetZ = this.playerCar.z - forwardZ * 6.5;

      this.camTargetPos.set(targetX, targetY, targetZ);
      this.camera.position.lerp(this.camTargetPos, Math.min(1.0, dt * 10.0));

      const lookX = this.playerCar.x + forwardX * 6.0;
      const lookY = this.playerCar.y + 1.2;
      const lookZ = this.playerCar.z + forwardZ * 6.0;

      this.camLookAtPos.set(lookX, lookY, lookZ);
      this.camera.lookAt(this.camLookAtPos);
    }
  }

  updateHUD() {
    if (this.hudClock) this.hudClock.textContent = this.clock.getFormattedTime();
    if (this.hudHour) this.hudHour.textContent = this.clock.hour.toFixed(2);

    const health = Math.round(this.playerCar.health);
    if (this.hudHealthText) this.hudHealthText.textContent = `${health}%`;
    if (this.hudHealthBar) {
      this.hudHealthBar.style.width = `${Math.max(0, health)}%`;
      if (health > 60) {
        this.hudHealthBar.style.background = '#00ff66';
      } else if (health > 30) {
        this.hudHealthBar.style.background = '#ffbb00';
      } else {
        this.hudHealthBar.style.background = '#ff3333';
      }
    }

    if (this.hudJobsDone) this.hudJobsDone.textContent = this.missions.jobsDone;
    if (this.hudReputation) this.hudReputation.textContent = this.missions.reputation;
    if (this.hudTraffic) this.hudTraffic.textContent = this.traffic.activeCars.length;
    if (this.hudPeds) this.hudPeds.textContent = this.pedestrians.activePeds.length;

    if (this.hudPlayerMode) {
      this.hudPlayerMode.textContent = this.mode.toUpperCase();
      this.hudPlayerMode.style.color = this.mode === 'drive' ? '#00ffcc' : '#ffea00';
    }

    const currentSpeed = this.mode === 'foot' ? 0 : Math.round(this.playerCar.speedKmh);
    if (this.hudSpeed) this.hudSpeed.textContent = currentSpeed;
    if (this.hudGear) {
      if (this.mode === 'foot') {
        this.hudGear.textContent = 'ON FOOT';
      } else if (this.playerCar.speed < -0.5) {
        this.hudGear.textContent = 'GEAR: R';
      } else {
        this.hudGear.textContent = `GEAR: ${this.playerCar.gear}`;
      }
    }

    if (this.hudWantedStars) {
      const stars = '★'.repeat(this.wantedStars) + '☆'.repeat(5 - this.wantedStars);
      this.hudWantedStars.textContent = stars;
    }
    if (this.hudHeat) this.hudHeat.textContent = this.heat.toFixed(2);
    if (this.hudCops) this.hudCops.textContent = this.police.copCars.length;

    // Mission HUD
    const objInfo = this.missions.getCurrentObjectiveInfo();
    if (objInfo) {
      if (this.missionBanner) this.missionBanner.style.display = 'block';
      if (this.missionTitle) this.missionTitle.textContent = `${objInfo.kind.toUpperCase()}: ${objInfo.title}`;
      if (this.missionDesc) this.missionDesc.textContent = objInfo.desc;

      if (objInfo.kind === 'sprint' && this.missionTimer) {
        this.missionTimer.style.display = 'block';
        this.missionTimer.textContent = `Time remaining: ${Math.max(0, Math.ceil(objInfo.timer))}s`;
      } else if (this.missionTimer) {
        this.missionTimer.style.display = 'none';
      }

      if (this.hudMissionStatus) {
        this.hudMissionStatus.textContent = `Objective: ${objInfo.title}`;
        this.hudMissionStatus.style.color = '#ffcc00';
      }
    } else {
      if (this.missionBanner) this.missionBanner.style.display = 'none';
      if (this.hudMissionStatus) {
        this.hudMissionStatus.textContent = 'Press [M] to accept a job';
        this.hudMissionStatus.style.color = '#88aaff';
      }
    }
  }

  updateStateContract() {
    // Mandate: Every animation frame, assign a fresh plain object literal to window.__arena_state.
    // Do not mutate a previously published object, no getters/setters/Proxy.
    const isFoot = this.mode === 'foot';
    window.__arena_state = {
      time: Number(this.elapsedTime.toFixed(3)),
      hour: Number(this.clock.hour.toFixed(3)),
      player_x: isFoot ? Number(this.character.x.toFixed(3)) : Number(this.playerCar.x.toFixed(3)),
      player_z: isFoot ? Number(this.character.z.toFixed(3)) : Number(this.playerCar.z.toFixed(3)),
      speed_kmh: isFoot ? 0 : Number(this.playerCar.speedKmh.toFixed(2)),
      gear: isFoot ? 0 : Number(this.playerCar.gear),
      car_health: Math.max(0, Number(this.playerCar.health.toFixed(1))),
      jobs_done: Number(this.missions.jobsDone),
      mission_kind: this.missions.missionKind,
      mission_active: Boolean(this.missions.missionActive),
      traffic_count: Number(this.traffic.activeCars.length),
      peds_count: Number(this.pedestrians.activePeds.length),
      wanted_stars: Number(this.wantedStars),
      heat: Number(this.heat.toFixed(3)),
      cops_active: Number(this.police.copCars.length),
      mode: this.mode,
      reputation: Number(this.missions.reputation)
    };
  }

  onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  animate() {
    requestAnimationFrame(this.animate);

    const now = performance.now();
    let dt = (now - this.lastFrameTime) / 1000;
    this.lastFrameTime = now;
    if (dt > 0.1) dt = 0.1;
    this.elapsedTime += dt;

    // 1. Inputs
    this.updateInputs();

    // 2. Update Systems
    this.clock.update(dt);
    if (this.mode === 'drive') {
      this.playerCar.update(dt, this.city, this.traffic);
    } else {
      this.character.update(dt, this.keys, this.city);
    }
    this.traffic.update(dt, this.playerCar);
    this.pedestrians.update(dt, this.mode === 'drive' ? this.playerCar : this.character);
    const pX = this.mode === 'foot' ? this.character.x : this.playerCar.x;
    const pZ = this.mode === 'foot' ? this.character.z : this.playerCar.z;
    this.missions.update(dt, pX, pZ);

    // Heat decay logic:
    // "热度只有在 170 米内没有任何警车、且 6 秒内没有新罪行时才会衰减，衰减前还要 4 秒逃脱确认，之后每秒掉 0.22"
    const minCopDist = this.police.getMinCopDistance(pX, pZ);
    const noCopNearby = minCopDist > 170.0;
    const noRecentCrime = (this.elapsedTime - this.lastCrimeTime) >= 6.0;

    if (noCopNearby && noRecentCrime && this.heat > 0) {
      this.escapeTimer += dt;
      if (this.escapeTimer >= 4.0) {
        this.heat = Math.max(0, this.heat - 0.22 * dt);
      }
    } else {
      this.escapeTimer = 0.0;
    }
    this.wantedStars = Math.min(5, Math.floor(this.heat));

    this.police.update(dt, this.playerCar, this.wantedStars, (t, amt) => this.addCrime(t, amt), this.elapsedTime);

    // 3. Camera
    this.updateCamera(dt);

    // 4. HUD
    this.updateHUD();

    // 5. Expose State Contract
    this.updateStateContract();

    // 6. Render
    this.renderer.render(this.scene, this.camera);
  }
}

// Boot game when DOM is loaded
window.addEventListener('DOMContentLoaded', () => {
  window.__game = new Game();
});
