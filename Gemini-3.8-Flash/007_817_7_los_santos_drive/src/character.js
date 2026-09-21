/**
 * On-Foot Character Controller for Los Santos Drive
 * Renders player character using xbot.glb with idle, walk, run, and jump animations.
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';

export class OnFootCharacter {
  constructor(scene) {
    this.scene = scene;

    this.x = 0;
    this.y = 0;
    this.z = 0;
    this.yaw = 0;
    this.vy = 0;
    this.isGrounded = true;

    this.walkSpeed = 3.8;
    this.runSpeed = 7.5;
    this.gravity = 18.0;
    this.jumpForce = 6.2;

    this.mesh = null;
    this.mixer = null;
    this.actions = {};
    this.currentActionName = 'idle';

    this.visible = false;
    this.loadModel();
  }

  loadModel() {
    const loader = new GLTFLoader();
    loader.load(
      '/assets/gta5_city/assets/xbot.glb',
      (gltf) => {
        this.initMesh(gltf);
      },
      undefined,
      (err) => {
        console.warn('Character relative fallback...', err);
        loader.load('./assets/gta5_city/assets/xbot.glb', (gltf) => {
          this.initMesh(gltf);
        });
      }
    );
  }

  initMesh(gltf) {
    this.mesh = SkeletonUtils.clone(gltf.scene);
    this.mesh.traverse((child) => {
      if (child.isMesh) child.castShadow = true;
    });

    this.mesh.visible = this.visible;
    this.scene.add(this.mesh);

    this.mixer = new THREE.AnimationMixer(this.mesh);

    for (const clip of gltf.animations) {
      const act = this.mixer.clipAction(clip);
      this.actions[clip.name] = act;
    }

    if (this.actions['idle']) {
      this.actions['idle'].play();
      this.currentActionName = 'idle';
    }
  }

  spawnAt(x, y, z, yaw) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.yaw = yaw;
    this.vy = 0;
    this.isGrounded = true;
    this.visible = true;

    if (this.mesh) {
      this.mesh.position.set(this.x, this.y, this.z);
      this.mesh.rotation.set(0, this.yaw, 0);
      this.mesh.visible = true;
    }

    this.playAction('idle');
  }

  hide() {
    this.visible = false;
    if (this.mesh) {
      this.mesh.visible = false;
    }
  }

  playAction(name) {
    if (!this.actions[name] || this.currentActionName === name) return;

    const prev = this.actions[this.currentActionName];
    const next = this.actions[name];

    if (prev) prev.fadeOut(0.2);
    next.reset().fadeIn(0.2).play();
    this.currentActionName = name;
  }

  update(dt, keys, city) {
    if (!this.visible) return;
    if (dt > 0.1) dt = 0.1;

    const forward = keys['KeyW'] || keys['ArrowUp'];
    const backward = keys['KeyS'] || keys['ArrowDown'];
    const left = keys['KeyA'] || keys['ArrowLeft'];
    const right = keys['KeyD'] || keys['ArrowRight'];
    const sprint = keys['ShiftLeft'] || keys['ShiftRight'];
    const jump = keys['Space'];

    // Rotate character with A / D
    if (left) this.yaw += 3.2 * dt;
    if (right) this.yaw -= 3.2 * dt;

    // Movement direction
    let moveForward = 0;
    if (forward) moveForward += 1;
    if (backward) moveForward -= 1;

    const speed = sprint ? this.runSpeed : this.walkSpeed;
    const isMoving = moveForward !== 0;

    // Jumping physics
    if (jump && this.isGrounded) {
      this.vy = this.jumpForce;
      this.isGrounded = false;
    }

    // Apply gravity
    if (!this.isGrounded) {
      this.vy -= this.gravity * dt;
      this.y += this.vy * dt;
      if (this.y <= 0) {
        this.y = 0;
        this.vy = 0;
        this.isGrounded = true;
      }
    }

    // Move forward/back along yaw
    if (isMoving) {
      const forwardX = -Math.sin(this.yaw);
      const forwardZ = -Math.cos(this.yaw);

      const prevX = this.x;
      const prevZ = this.z;

      this.x += forwardX * moveForward * speed * dt;
      this.z += forwardZ * moveForward * speed * dt;

      // Collision with city buildings
      if (city) {
        const col = city.checkCollision(this.x, this.z, 0.4);
        if (col.collided) {
          this.x = prevX + col.normalX * (col.penetration + 0.05);
          this.z = prevZ + col.normalZ * (col.penetration + 0.05);
        }
      }

      // Animation selection
      if (sprint) {
        this.playAction('run');
      } else {
        this.playAction('walk');
      }
    } else {
      this.playAction('idle');
    }

    // Update mesh transform
    if (this.mesh) {
      this.mesh.position.set(this.x, this.y, this.z);
      this.mesh.rotation.set(0, this.yaw, 0);
    }

    if (this.mixer) {
      this.mixer.update(dt);
    }
  }
}
