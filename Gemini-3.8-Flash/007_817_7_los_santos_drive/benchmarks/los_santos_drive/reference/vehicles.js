/**
 * Vehicles for Los Santos Drive
 * Exactly one car runs full vehicle dynamics (the player's); everything else is kinematic.
 * Loads ferrari.glb for the hero car and traffic vehicles.
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

export class PlayerVehicle {
  constructor(scene, roadGraph) {
    this.scene = scene;
    this.roadGraph = roadGraph;

    // Dynamics State
    this.x = 0;
    this.y = 0.35;
    this.z = 80;
    this.yaw = 0; // heading angle
    this.speed = 0; // m/s (signed)
    this.speedKmh = 0;
    this.steerAngle = 0;
    this.gear = 1;
    this.health = 100;
    this.wrecked = false;

    // Controls
    this.throttle = 0;
    this.brake = 0;
    this.steer = 0;
    this.handbrake = false;

    // Physics parameters
    this.wheelbase = 2.65;
    this.wheelRadius = 0.36;
    this.maxForwardSpeed = 58.0; // ~210 km/h
    this.maxReverseSpeed = -12.0; // ~43 km/h
    this.wheelSpinAngle = 0;

    // Vehicle mesh group
    this.group = new THREE.Group();
    this.group.position.set(this.x, this.y, this.z);
    this.scene.add(this.group);

    // Wheel nodes references
    this.wheels = {
      fl: null,
      fr: null,
      rl: null,
      rr: null
    };

    // Spawn on nearest road lane
    const nearest = this.roadGraph.getNearestLane(0, 80);
    if (nearest) {
      this.x = nearest.point.x;
      this.z = nearest.point.z;
      this.yaw = nearest.heading;
      this.group.position.set(this.x, this.y, this.z);
      this.group.rotation.set(0, this.yaw, 0);
    }

    this.carModelLoaded = false;
    this.lastTrafficHitTime = -10;
    this.onTrafficCollision = null;
    this.loadModel();
  }

  loadModel() {
    const loader = new GLTFLoader();
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('/vendor/three/jsm/libs/draco/gltf/');
    loader.setDRACOLoader(dracoLoader);

    loader.load(
      '/assets/gta5_city/assets/ferrari.glb',
      (gltf) => {
        const car = gltf.scene;
        car.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
          if (child.name === 'wheel_fl') this.wheels.fl = child;
          if (child.name === 'wheel_fr') this.wheels.fr = child;
          if (child.name === 'wheel_rl') this.wheels.rl = child;
          if (child.name === 'wheel_rr') this.wheels.rr = child;
        });

        this.group.add(car);
        this.carModelLoaded = true;
      },
      undefined,
      (err) => {
        console.warn('Failed to load ferrari model, retrying relative path...', err);
        loader.load('./assets/gta5_city/assets/ferrari.glb', (gltf) => {
          this.group.add(gltf.scene);
          this.carModelLoaded = true;
        });
      }
    );
  }

  resetToNearestRoad() {
    const nearest = this.roadGraph.getNearestLane(this.x, this.z);
    if (nearest) {
      this.x = nearest.point.x;
      this.z = nearest.point.z;
      this.yaw = nearest.heading;
      this.speed = 0;
      this.speedKmh = 0;
      this.steer = 0;
      this.steerAngle = 0;
      this.throttle = 0;
      this.brake = 0;
      this.health = 100;
      this.wrecked = false;

      this.group.position.set(this.x, this.y, this.z);
      this.group.rotation.set(0, this.yaw, 0);
    }
  }

  update(dt, city, traffic) {
    if (dt > 0.1) dt = 0.1;

    // Calculate inputs
    const targetSteer = this.steer * 0.45;
    const speedRatio = Math.min(1.0, this.speedKmh / 160);
    const maxAllowedSteer = THREE.MathUtils.lerp(0.55, 0.16, speedRatio);
    const clampedTargetSteer = THREE.MathUtils.clamp(targetSteer, -maxAllowedSteer, maxAllowedSteer);

    // Smooth steering
    this.steerAngle = THREE.MathUtils.lerp(this.steerAngle, clampedTargetSteer, dt * 8.0);

    // Throttle & Engine acceleration
    if (this.health > 0) {
      if (this.throttle > 0) {
        if (this.speed < -0.5) {
          // Braking while reversing
          this.speed += 20.0 * dt;
        } else {
          // Accelerate forward
          let accel = 12.0;
          if (this.speedKmh < 40) accel = 13.5;
          else if (this.speedKmh < 80) accel = 10.0;
          else if (this.speedKmh < 130) accel = 6.5;
          else accel = 3.5;

          this.speed += accel * this.throttle * dt;
          if (this.speed > this.maxForwardSpeed) this.speed = this.maxForwardSpeed;
        }
      }

      // Brake / Reverse
      if (this.brake > 0) {
        if (this.speed > 0.5) {
          // Braking forward
          this.speed -= 22.0 * this.brake * dt;
          if (this.speed < 0) this.speed = 0;
        } else {
          // Reverse
          this.speed -= 7.0 * this.brake * dt;
          if (this.speed < this.maxReverseSpeed) this.speed = this.maxReverseSpeed;
        }
      }
    } else {
      this.wrecked = true;
    }

    // Handbrake
    if (this.handbrake) {
      const friction = 18.0 * dt;
      if (this.speed > 0) {
        this.speed = Math.max(0, this.speed - friction);
      } else if (this.speed < 0) {
        this.speed = Math.min(0, this.speed + friction);
      }
    }

    // Natural drag & rolling resistance
    if (this.throttle === 0 && this.brake === 0) {
      const rollingDrag = 4.0 * dt;
      if (this.speed > 0) {
        this.speed = Math.max(0, this.speed - rollingDrag);
      } else if (this.speed < 0) {
        this.speed = Math.min(0, this.speed + rollingDrag);
      }
    }

    // Aerodynamic drag
    const aeroDrag = 0.0012 * this.speed * Math.abs(this.speed);
    this.speed -= aeroDrag * dt;

    // Turning dynamics
    if (Math.abs(this.speed) > 0.1) {
      const handbrakeDriftMult = this.handbrake ? 1.7 : 1.0;
      const yawRate = (this.speed / this.wheelbase) * Math.tan(this.steerAngle) * handbrakeDriftMult;
      this.yaw += yawRate * dt;
    }

    // Integrate position
    const forwardX = -Math.sin(this.yaw);
    const forwardZ = -Math.cos(this.yaw);

    const prevX = this.x;
    const prevZ = this.z;

    this.x += forwardX * this.speed * dt;
    this.z += forwardZ * this.speed * dt;

    // Speed in km/h
    this.speedKmh = Math.abs(this.speed * 3.6);

    // Gear calculation
    if (this.speed < -0.5) {
      this.gear = 1;
    } else if (this.speedKmh < 35) {
      this.gear = 1;
    } else if (this.speedKmh < 70) {
      this.gear = 2;
    } else if (this.speedKmh < 105) {
      this.gear = 3;
    } else if (this.speedKmh < 145) {
      this.gear = 4;
    } else {
      this.gear = 5;
    }

    // Collision with city buildings
    const col = city.checkCollision(this.x, this.z, 1.6);
    if (col.collided) {
      this.x = prevX + col.normalX * (col.penetration + 0.1);
      this.z = prevZ + col.normalZ * (col.penetration + 0.1);

      const impactSpeed = this.speedKmh;
      if (impactSpeed > 10) {
        const damage = Math.min(30, impactSpeed * 0.4);
        this.health = Math.max(0, this.health - damage);
      }

      this.speed = -this.speed * 0.3;
    }

    // Collision with traffic cars
    if (traffic) {
      for (const tCar of traffic.activeCars) {
        const cdx = this.x - tCar.x;
        const cdz = this.z - tCar.z;
        const distSq = cdx * cdx + cdz * cdz;
        if (distSq < 9.0 && distSq > 0.001) {
          const dist = Math.sqrt(distSq);
          const nx = cdx / dist;
          const nz = cdz / dist;

          this.x += nx * 0.6;
          this.z += nz * 0.6;
          tCar.x -= nx * 0.6;
          tCar.z -= nz * 0.6;

          const relSpeed = Math.abs(this.speed - tCar.speed) * 3.6;
          if (relSpeed > 10) {
            const damage = Math.min(25, relSpeed * 0.35);
            this.health = Math.max(0, this.health - damage);
          }

          this.speed *= 0.5;

          if (this.onTrafficCollision) {
            this.onTrafficCollision(tCar);
          }
        }
      }
    }

    // Update 3D mesh transform
    this.group.position.set(this.x, this.y, this.z);
    this.group.rotation.set(0, this.yaw, 0);

    // Animate wheels
    this.wheelSpinAngle += (this.speed / this.wheelRadius) * dt;
    if (this.wheels.fl) {
      this.wheels.fl.rotation.y = this.steerAngle;
      this.wheels.fl.rotation.x = this.wheelSpinAngle;
    }
    if (this.wheels.fr) {
      this.wheels.fr.rotation.y = this.steerAngle;
      this.wheels.fr.rotation.x = this.wheelSpinAngle;
    }
    if (this.wheels.rl) {
      this.wheels.rl.rotation.x = this.wheelSpinAngle;
    }
    if (this.wheels.rr) {
      this.wheels.rr.rotation.x = this.wheelSpinAngle;
    }
  }
}

export class TrafficSystem {
  constructor(scene, roadGraph) {
    this.scene = scene;
    this.roadGraph = roadGraph;
    this.activeCars = [];
    this.maxCars = 14;

    this.carColors = [
      0x1e56a0, // blue
      0x222222, // dark gray
      0xdddddd, // silver
      0xb83b26, // crimson
      0xf5a623, // orange
      0x1a5336  // forest green
    ];

    this.carBaseMesh = null;
    this.initTrafficCars();
    this.loadBaseModel();
  }

  loadBaseModel() {
    const loader = new GLTFLoader();
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('/vendor/three/jsm/libs/draco/gltf/');
    loader.setDRACOLoader(dracoLoader);

    loader.load(
      '/assets/gta5_city/assets/ferrari.glb',
      (gltf) => {
        this.carBaseMesh = gltf.scene;
        this.attachMeshesToCars();
      },
      undefined,
      (err) => {
        console.warn('Traffic loading relative fallback...', err);
        loader.load('./assets/gta5_city/assets/ferrari.glb', (gltf) => {
          this.carBaseMesh = gltf.scene;
          this.attachMeshesToCars();
        });
      }
    );
  }

  initTrafficCars() {
    for (let i = 0; i < this.maxCars; i++) {
      this.spawnCar();
    }
  }

  spawnCar() {
    const spawnInfo = this.roadGraph.getRandomLanePosition(0.2);
    if (!spawnInfo) return;

    const group = new THREE.Group();
    group.position.set(spawnInfo.x, 0.35, spawnInfo.z);
    group.rotation.y = spawnInfo.heading;
    this.scene.add(group);

    const car = {
      group,
      lane: spawnInfo.lane,
      x: spawnInfo.x,
      y: 0.35,
      z: spawnInfo.z,
      yaw: spawnInfo.heading,
      speed: 8.5 + Math.random() * 3.5, // ~30 - 45 km/h
      targetSpeed: 8.5 + Math.random() * 3.5,
      distAlongLane: (spawnInfo.x - spawnInfo.lane.startX) * spawnInfo.lane.dirX +
                     (spawnInfo.z - spawnInfo.lane.startZ) * spawnInfo.lane.dirZ
    };

    if (this.carBaseMesh) {
      this.attachMeshToSingleCar(car);
    }

    this.activeCars.push(car);
  }

  attachMeshToSingleCar(car) {
    if (!this.carBaseMesh) return;
    const clonedMesh = this.carBaseMesh.clone(true);
    const color = this.carColors[Math.floor(Math.random() * this.carColors.length)];
    clonedMesh.traverse((child) => {
      if (child.isMesh && child.material) {
        child.castShadow = true;
        child.material = child.material.clone();
        if (child.name.toLowerCase().includes('body') || child.material.name.toLowerCase().includes('paint')) {
          child.material.color.setHex(color);
        }
      }
    });
    car.group.add(clonedMesh);
  }

  attachMeshesToCars() {
    for (const car of this.activeCars) {
      if (car.group.children.length === 0) {
        this.attachMeshToSingleCar(car);
      }
    }
  }

  update(dt, playerCar) {
    for (let i = 0; i < this.activeCars.length; i++) {
      const car = this.activeCars[i];
      const lane = car.lane;

      let brakeForObstacle = false;

      // Check distance to player
      const toPlayerX = playerCar.x - car.x;
      const toPlayerZ = playerCar.z - car.z;
      const distToPlayer = Math.hypot(toPlayerX, toPlayerZ);
      const dotPlayer = toPlayerX * lane.dirX + toPlayerZ * lane.dirZ;

      if (distToPlayer < 9.0 && dotPlayer > 0) {
        brakeForObstacle = true;
      }

      // Check distance to other traffic
      for (let j = 0; j < this.activeCars.length; j++) {
        if (i === j) continue;
        const other = this.activeCars[j];
        if (other.lane.id === lane.id) {
          const deltaDist = other.distAlongLane - car.distAlongLane;
          if (deltaDist > 0 && deltaDist < 10.0) {
            brakeForObstacle = true;
            break;
          }
        }
      }

      // Adjust speed
      if (brakeForObstacle) {
        car.speed = Math.max(0, car.speed - 12.0 * dt);
      } else {
        car.speed = Math.min(car.targetSpeed, car.speed + 6.0 * dt);
      }

      // Move along lane
      car.distAlongLane += car.speed * dt;
      car.x = lane.startX + lane.dirX * car.distAlongLane;
      car.z = lane.startZ + lane.dirZ * car.distAlongLane;

      // Check if reached end of lane
      if (car.distAlongLane >= lane.length) {
        const outgoing = this.roadGraph.getOutgoingLanes(lane.toNode);
        if (outgoing.length > 0) {
          const nextLane = outgoing[Math.floor(Math.random() * outgoing.length)];
          car.lane = nextLane;
          car.distAlongLane = 0;
          car.x = nextLane.startX;
          car.z = nextLane.startZ;
          car.yaw = nextLane.heading;
        } else {
          car.distAlongLane = 0;
        }
      }

      // Update 3D mesh
      car.group.position.set(car.x, car.y, car.z);
      car.group.rotation.set(0, car.yaw, 0);
    }
  }
}
