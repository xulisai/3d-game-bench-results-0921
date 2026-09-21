/**
 * Police Pursuit System for Los Santos Drive
 * Handles police spawning, Dijkstra road graph routing, direct chase within 45m,
 * siren lights, ramming collisions, and heat decay rules.
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

export class PoliceSystem {
  constructor(scene, roadGraph) {
    this.scene = scene;
    this.roadGraph = roadGraph;
    this.copCars = [];
    this.copBaseMesh = null;

    // Siren lights materials
    this.sirenRedMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    this.sirenBlueMat = new THREE.MeshBasicMaterial({ color: 0x0066ff });
    this.sirenOffMat = new THREE.MeshBasicMaterial({ color: 0x222222 });

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
        this.copBaseMesh = gltf.scene;
        this.attachMeshToAllCops();
      },
      undefined,
      (err) => {
        console.warn('Police relative fallback...', err);
        loader.load('./assets/gta5_city/assets/ferrari.glb', (gltf) => {
          this.copBaseMesh = gltf.scene;
          this.attachMeshToAllCops();
        });
      }
    );
  }

  createCopMesh() {
    const group = new THREE.Group();
    if (!this.copBaseMesh) return group;

    const cloned = this.copBaseMesh.clone(true);
    // Police black & white livery
    cloned.traverse((child) => {
      if (child.isMesh && child.material) {
        child.castShadow = true;
        child.material = child.material.clone();
        const n = child.name.toLowerCase();
        if (n.includes('door') || n.includes('roof')) {
          child.material.color.setHex(0xf5f5f5); // white doors/roof
        } else if (n.includes('body') || child.material.name.toLowerCase().includes('paint')) {
          child.material.color.setHex(0x111316); // black cruiser body
        }
      }
    });
    group.add(cloned);

    // Lightbar on roof
    const barGeo = new THREE.BoxGeometry(0.9, 0.1, 0.22);
    const barMat = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.8 });
    const bar = new THREE.Mesh(barGeo, barMat);
    bar.position.set(0, 1.18, 0.15);

    // Left red light
    const redLight = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.09, 0.18), this.sirenRedMat);
    redLight.position.set(-0.25, 0.05, 0);
    bar.add(redLight);

    // Right blue light
    const blueLight = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.09, 0.18), this.sirenBlueMat);
    blueLight.position.set(0.25, 0.05, 0);
    bar.add(blueLight);

    // Point lights for flashing
    const pointRed = new THREE.PointLight(0xff0000, 1.2, 20);
    pointRed.position.set(-0.25, 0.2, 0);
    bar.add(pointRed);

    const pointBlue = new THREE.PointLight(0x0066ff, 1.2, 20);
    pointBlue.position.set(0.25, 0.2, 0);
    bar.add(pointBlue);

    group.add(bar);

    group.userData.redLight = redLight;
    group.userData.blueLight = blueLight;
    group.userData.pointRed = pointRed;
    group.userData.pointBlue = pointBlue;

    return group;
  }

  attachMeshToAllCops() {
    for (const cop of this.copCars) {
      if (cop.group.children.length === 0) {
        const mesh = this.createCopMesh();
        cop.group.add(mesh);
        cop.meshGroup = mesh;
      }
    }
  }

  spawnCop(playerX, playerZ) {
    // Find road node far enough from player (e.g. 80-140m)
    let bestNode = null;
    let bestDist = 0;

    const nodeEntries = Array.from(this.roadGraph.nodes.values());
    // Filter nodes between 70m and 160m away
    const validNodes = nodeEntries.filter(n => {
      const d = Math.hypot(n.x - playerX, n.z - playerZ);
      return d >= 65 && d <= 170;
    });

    if (validNodes.length > 0) {
      bestNode = validNodes[Math.floor(Math.random() * validNodes.length)];
    } else {
      bestNode = nodeEntries[Math.floor(Math.random() * nodeEntries.length)];
    }

    const group = new THREE.Group();
    group.position.set(bestNode.x, 0.35, bestNode.z);
    this.scene.add(group);

    const cop = {
      group,
      meshGroup: null,
      x: bestNode.x,
      y: 0.35,
      z: bestNode.z,
      yaw: 0,
      speed: 12.0, // ~43 km/h
      maxSpeed: 21.0, // ~75 km/h in chase
      currentNodeId: bestNode.id,
      path: [],
      mode: 'route', // 'route' (Dijkstra) or 'chase' (direct ram)
      flashPhase: 0,
      lastRamTime: -10
    };

    if (this.copBaseMesh) {
      const mesh = this.createCopMesh();
      group.add(mesh);
      cop.meshGroup = mesh;
    }

    this.copCars.push(cop);
    return cop;
  }

  despawnCop(index) {
    const cop = this.copCars[index];
    if (!cop) return;
    this.scene.remove(cop.group);
    this.copCars.splice(index, 1);
  }

  getMinCopDistance(playerX, playerZ) {
    if (this.copCars.length === 0) return Infinity;
    let minDist = Infinity;
    for (const cop of this.copCars) {
      const d = Math.hypot(cop.x - playerX, cop.z - playerZ);
      if (d < minDist) minDist = d;
    }
    return minDist;
  }

  update(dt, playerCar, wantedStars, onCrime, currentTime) {
    // Desired number of pursuit cars based on wanted_stars (0 stars = 0 cops)
    const targetCops = wantedStars > 0 ? Math.min(5, wantedStars) : 0;

    // Spawn cops if needed
    while (this.copCars.length < targetCops) {
      this.spawnCop(playerCar.x, playerCar.z);
    }

    // Despawn excess cops if wanted level dropped
    while (this.copCars.length > targetCops) {
      // Despawn furthest cop
      let furthestIdx = 0;
      let maxDist = -1;
      for (let i = 0; i < this.copCars.length; i++) {
        const d = Math.hypot(this.copCars[i].x - playerCar.x, this.copCars[i].z - playerCar.z);
        if (d > maxDist) {
          maxDist = d;
          furthestIdx = i;
        }
      }
      this.despawnCop(furthestIdx);
    }

    // Update each cop car
    for (let i = 0; i < this.copCars.length; i++) {
      const cop = this.copCars[i];

      // Flash siren lights
      cop.flashPhase += dt * 8.0;
      const isRedPhase = Math.sin(cop.flashPhase) > 0;
      if (cop.meshGroup && cop.meshGroup.userData.redLight) {
        const ud = cop.meshGroup.userData;
        ud.redLight.material = isRedPhase ? this.sirenRedMat : this.sirenOffMat;
        ud.blueLight.material = isRedPhase ? this.sirenOffMat : this.sirenBlueMat;
        ud.pointRed.intensity = isRedPhase ? 2.0 : 0.0;
        ud.pointBlue.intensity = isRedPhase ? 0.0 : 2.0;
      }

      const dx = playerCar.x - cop.x;
      const dz = playerCar.z - cop.z;
      const distToPlayer = Math.hypot(dx, dz);

      // Rule: Dijkstra pursuit along road graph before switching to direct chase inside 45m
      if (distToPlayer <= 45.0) {
        cop.mode = 'chase';
        // Direct chase: turn directly towards player
        const targetYaw = Math.atan2(-dx, -dz);
        // Smoothly rotate yaw toward player
        let angleDiff = targetYaw - cop.yaw;
        while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
        while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;
        cop.yaw += THREE.MathUtils.clamp(angleDiff, -3.5 * dt, 3.5 * dt);

        // Chase acceleration
        cop.speed = Math.min(cop.maxSpeed, cop.speed + 15.0 * dt);

        // Check ramming collision with player
        if (distToPlayer < 3.4) {
          // Ram player!
          const nx = dx / (distToPlayer || 1);
          const nz = dz / (distToPlayer || 1);

          playerCar.x += nx * 1.2;
          playerCar.z += nz * 1.2;
          cop.x -= nx * 0.8;
          cop.z -= nz * 0.8;

          // Damage player car
          playerCar.health = Math.max(0, playerCar.health - 15);
          cop.speed *= 0.3;

          // Crime: Ramming a police car / police ram adds 0.6 heat
          if (currentTime - cop.lastRamTime > 1.0) {
            cop.lastRamTime = currentTime;
            if (onCrime) onCrime('ram_cop', 0.6);
          }
        }
      } else {
        cop.mode = 'route';
        // Dijkstra road graph routing
        // Find nearest road node to player
        const playerLane = this.roadGraph.getNearestLane(playerCar.x, playerCar.z);
        const targetNodeId = playerLane ? playerLane.lane.toNode : 'node_2_2';

        // Find nearest node to cop
        const copLane = this.roadGraph.getNearestLane(cop.x, cop.z);
        const copStartNodeId = copLane ? copLane.lane.toNode : 'node_0_0';

        // Recompute path periodically
        if (!cop.path || cop.path.length === 0 || Math.random() < 0.05) {
          cop.path = this.roadGraph.findPathDijkstra(copStartNodeId, targetNodeId);
        }

        // Steer towards next path waypoint or player node
        let targetX = playerCar.x;
        let targetZ = playerCar.z;

        if (cop.path && cop.path.length > 0) {
          const nextNode = this.roadGraph.nodes.get(cop.path[0].toNode);
          if (nextNode) {
            targetX = nextNode.x;
            targetZ = nextNode.z;
            if (Math.hypot(nextNode.x - cop.x, nextNode.z - cop.z) < 5.0) {
              cop.path.shift();
            }
          }
        }

        const tdx = targetX - cop.x;
        const tdz = targetZ - cop.z;
        const targetYaw = Math.atan2(-tdx, -tdz);

        let angleDiff = targetYaw - cop.yaw;
        while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
        while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;
        cop.yaw += THREE.MathUtils.clamp(angleDiff, -2.8 * dt, 2.8 * dt);

        cop.speed = Math.min(cop.maxSpeed * 0.85, cop.speed + 10.0 * dt);
      }

      // Move cop car forward
      const forwardX = -Math.sin(cop.yaw);
      const forwardZ = -Math.cos(cop.yaw);
      cop.x += forwardX * cop.speed * dt;
      cop.z += forwardZ * cop.speed * dt;

      // Update 3D mesh transform
      cop.group.position.set(cop.x, cop.y, cop.z);
      cop.group.rotation.set(0, cop.yaw, 0);
    }
  }
}
