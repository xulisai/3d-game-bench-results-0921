/**
 * Pedestrians for Los Santos Drive
 * Loads xbot.glb rigged pedestrian character with walk/idle animations.
 * Walks along sidewalks and crosswalks, reacts to player collisions.
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

export class PedestrianSystem {
  constructor(scene, roadGraph) {
    this.scene = scene;
    this.roadGraph = roadGraph;
    this.activePeds = [];
    this.maxPeds = 14;

    this.baseGltf = null;
    this.walkClip = null;
    this.idleClip = null;
    this.onPedKnockedDown = null;

    this.initSidewalkWaypoints();
    this.initPedsPlaceholder();
    this.loadModel();
  }

  initSidewalkWaypoints() {
    this.sidewalkPaths = [];
    const coords = [-160, -80, 0, 80, 160];
    const roadWidth = 14;
    const swOffset = roadWidth / 2 + 1.2;

    for (let bx = 0; bx < coords.length - 1; bx++) {
      for (let bz = 0; bz < coords.length - 1; bz++) {
        const xMin = coords[bx] + swOffset;
        const xMax = coords[bx + 1] - swOffset;
        const zMin = coords[bz] + swOffset;
        const zMax = coords[bz + 1] - swOffset;

        const loop = [
          { x: xMin, z: zMin },
          { x: xMax, z: zMin },
          { x: xMax, z: zMax },
          { x: xMin, z: zMax }
        ];
        this.sidewalkPaths.push(loop);
      }
    }
  }

  initPedsPlaceholder() {
    for (let i = 0; i < this.maxPeds; i++) {
      const path = this.sidewalkPaths[i % this.sidewalkPaths.length];
      const wpIndex = Math.floor(Math.random() * path.length);
      const startWp = path[wpIndex];
      const nextWp = path[(wpIndex + 1) % path.length];
      const t = Math.random();
      const x = startWp.x + (nextWp.x - startWp.x) * t;
      const z = startWp.z + (nextWp.z - startWp.z) * t;

      this.activePeds.push({
        mesh: null,
        mixer: null,
        path,
        targetWpIndex: (wpIndex + 1) % path.length,
        x,
        y: 0.25,
        z,
        yaw: 0,
        speed: 1.35 + Math.random() * 0.4,
        isKnockedDown: false,
        knockdownTimer: 0
      });
    }
  }

  loadModel() {
    const loader = new GLTFLoader();
    loader.load(
      '/assets/gta5_city/assets/xbot.glb',
      (gltf) => {
        this.baseGltf = gltf;
        for (const clip of gltf.animations) {
          if (clip.name === 'walk') this.walkClip = clip;
          if (clip.name === 'idle') this.idleClip = clip;
        }
        this.attachMeshesToPeds();
      },
      undefined,
      (err) => {
        console.warn('Fallback loading relative xbot.glb...', err);
        loader.load('./assets/gta5_city/assets/xbot.glb', (gltf) => {
          this.baseGltf = gltf;
          for (const clip of gltf.animations) {
            if (clip.name === 'walk') this.walkClip = clip;
            if (clip.name === 'idle') this.idleClip = clip;
          }
          this.attachMeshesToPeds();
        });
      }
    );
  }

  attachMeshesToPeds() {
    if (!this.baseGltf) return;

    for (const ped of this.activePeds) {
      if (ped.mesh) continue;

      const pedMesh = SkeletonUtils.clone(this.baseGltf.scene);
      pedMesh.position.set(ped.x, 0.25, ped.z);
      pedMesh.scale.set(1.0, 1.0, 1.0);
      pedMesh.traverse((child) => {
        if (child.isMesh) child.castShadow = true;
      });

      this.scene.add(pedMesh);

      const mixer = new THREE.AnimationMixer(pedMesh);
      if (this.walkClip) {
        const action = mixer.clipAction(this.walkClip);
        action.timeScale = 1.0 + (Math.random() * 0.3 - 0.15);
        action.play();
      }

      ped.mesh = pedMesh;
      ped.mixer = mixer;
    }
  }

  update(dt, playerCar) {
    for (let i = 0; i < this.activePeds.length; i++) {
      const ped = this.activePeds[i];

      if (ped.isKnockedDown) {
        ped.knockdownTimer += dt;
        if (ped.mesh) {
          ped.mesh.rotation.x = THREE.MathUtils.lerp(ped.mesh.rotation.x, -Math.PI / 2, dt * 10);
          ped.mesh.position.y = THREE.MathUtils.lerp(ped.mesh.position.y, 0.1, dt * 10);
        }

        // Respawn after 4.5 seconds
        if (ped.knockdownTimer > 4.5) {
          if (ped.mesh) this.scene.remove(ped.mesh);
          const path = this.sidewalkPaths[Math.floor(Math.random() * this.sidewalkPaths.length)];
          const wp = path[0];
          ped.x = wp.x;
          ped.z = wp.z;
          ped.y = 0.25;
          ped.targetWpIndex = 1;
          ped.isKnockedDown = false;
          ped.knockdownTimer = 0;
          ped.mesh = null;
          ped.mixer = null;
          this.attachMeshesToPeds();
        }
        continue;
      }

      // Check collision with player car
      const dx = playerCar.x - ped.x;
      const dz = playerCar.z - ped.z;
      const distSq = dx * dx + dz * dz;

      if (distSq < 3.2) {
        ped.isKnockedDown = true;
        ped.knockdownTimer = 0;
        if (ped.mixer) ped.mixer.stopAllAction();

        if (this.onPedKnockedDown) {
          this.onPedKnockedDown(ped);
        }
        continue;
      }

      // Normal walking path
      const targetWp = ped.path[ped.targetWpIndex];
      const tx = targetWp.x - ped.x;
      const tz = targetWp.z - ped.z;
      const dist = Math.hypot(tx, tz);

      if (dist < 0.8) {
        ped.targetWpIndex = (ped.targetWpIndex + 1) % ped.path.length;
      } else {
        const ux = tx / dist;
        const uz = tz / dist;

        ped.x += ux * ped.speed * dt;
        ped.z += uz * ped.speed * dt;

        ped.yaw = Math.atan2(ux, uz);
        if (ped.mesh) {
          ped.mesh.position.set(ped.x, ped.y, ped.z);
          ped.mesh.rotation.set(0, ped.yaw, 0);
        }
      }

      if (ped.mixer) {
        ped.mixer.update(dt);
      }
    }
  }
}
