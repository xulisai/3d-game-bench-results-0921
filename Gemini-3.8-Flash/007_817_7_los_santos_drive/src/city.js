/**
 * City Generator for Los Santos Drive
 * Renders roads, sidewalks, buildings with illuminated windows at dusk, streetlights, and collisions.
 * Uses benchmark-local texture assets under /assets/los_santos_drive/assets/textures/*.
 */

import * as THREE from 'three';

export class City {
  constructor(scene, roadGraph, clock) {
    this.scene = scene;
    this.roadGraph = roadGraph;
    this.clock = clock;
    this.buildingColliders = [];

    this.texLoader = new THREE.TextureLoader();
    this.loadTextures();
    this.initCity();
  }

  loadTextures() {
    const texPath = '/assets/los_santos_drive/assets/textures/';

    const loadTex = (rel, repeatX = 1, repeatY = 1) => {
      const tex = this.texLoader.load(texPath + rel);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(repeatX, repeatY);
      return tex;
    };

    this.textures = {
      grass: loadTex('aerial_grass_rock/diff.jpg', 30, 30),
      asphalt: loadTex('asphalt_02/diff.jpg', 6, 20),
      asphaltNorm: loadTex('asphalt_02/nor_gl.jpg', 6, 20),
      sidewalk: loadTex('pavement_02/diff.jpg', 12, 12),
      brick: loadTex('brick_wall_10/diff.jpg', 4, 6),
      concrete: loadTex('concrete_wall_008/diff.jpg', 4, 8),
      plaster: loadTex('painted_plaster_wall/diff.jpg', 4, 6)
    };
  }

  initCity() {
    this.createGround();
    this.createRoads();
    this.createBlocksAndBuildings();
    this.createStreetFurniture();
  }

  createGround() {
    const groundGeo = new THREE.PlaneGeometry(800, 800);
    const groundMat = new THREE.MeshStandardMaterial({
      map: this.textures.grass,
      roughness: 0.95,
      metalness: 0.05
    });
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.05;
    ground.receiveShadow = true;
    this.scene.add(ground);
  }

  createRoads() {
    const roadGroup = new THREE.Group();
    const roadMat = new THREE.MeshStandardMaterial({
      map: this.textures.asphalt,
      normalMap: this.textures.asphaltNorm,
      color: 0x33363d,
      roughness: 0.8,
      metalness: 0.15
    });
    const lineMatYellow = new THREE.MeshBasicMaterial({ color: 0xffcc00 });
    const lineMatWhite = new THREE.MeshBasicMaterial({ color: 0xf0f0f0 });

    const roadWidth = 14;
    const coords = [-160, -80, 0, 80, 160];

    // Horizontal roads (along X)
    for (const z of coords) {
      const roadGeo = new THREE.PlaneGeometry(360, roadWidth);
      const road = new THREE.Mesh(roadGeo, roadMat);
      road.rotation.x = -Math.PI / 2;
      road.position.set(0, 0.01, z);
      road.receiveShadow = true;
      roadGroup.add(road);

      // Yellow centerline
      const lineGeo = new THREE.PlaneGeometry(360, 0.3);
      const line = new THREE.Mesh(lineGeo, lineMatYellow);
      line.rotation.x = -Math.PI / 2;
      line.position.set(0, 0.02, z);
      roadGroup.add(line);

      // White lane borders
      const borderNorth = new THREE.Mesh(new THREE.PlaneGeometry(360, 0.25), lineMatWhite);
      borderNorth.rotation.x = -Math.PI / 2;
      borderNorth.position.set(0, 0.02, z + roadWidth / 2 - 0.2);
      roadGroup.add(borderNorth);

      const borderSouth = new THREE.Mesh(new THREE.PlaneGeometry(360, 0.25), lineMatWhite);
      borderSouth.rotation.x = -Math.PI / 2;
      borderSouth.position.set(0, 0.02, z - roadWidth / 2 + 0.2);
      roadGroup.add(borderSouth);
    }

    // Vertical roads (along Z)
    for (const x of coords) {
      const roadGeo = new THREE.PlaneGeometry(roadWidth, 360);
      const road = new THREE.Mesh(roadGeo, roadMat);
      road.rotation.x = -Math.PI / 2;
      road.position.set(x, 0.01, 0);
      road.receiveShadow = true;
      roadGroup.add(road);

      // Yellow centerline
      const lineGeo = new THREE.PlaneGeometry(0.3, 360);
      const line = new THREE.Mesh(lineGeo, lineMatYellow);
      line.rotation.x = -Math.PI / 2;
      line.position.set(x, 0.02, 0);
      roadGroup.add(line);

      // White lane borders
      const borderEast = new THREE.Mesh(new THREE.PlaneGeometry(0.25, 360), lineMatWhite);
      borderEast.rotation.x = -Math.PI / 2;
      borderEast.position.set(x + roadWidth / 2 - 0.2, 0.02, 0);
      roadGroup.add(borderEast);

      const borderWest = new THREE.Mesh(new THREE.PlaneGeometry(0.25, 360), lineMatWhite);
      borderWest.rotation.x = -Math.PI / 2;
      borderWest.position.set(x - roadWidth / 2 + 0.2, 0.02, 0);
      roadGroup.add(borderWest);
    }

    // Crosswalk zebra stripes at intersections
    for (const x of coords) {
      for (const z of coords) {
        this.addCrosswalk(roadGroup, x, z, roadWidth);
      }
    }

    this.scene.add(roadGroup);
  }

  addCrosswalk(group, ix, iz, roadWidth) {
    const stripeMat = new THREE.MeshBasicMaterial({ color: 0xdddddd });
    const offsets = [
      { dx: 0, dz: roadWidth / 2 + 1.5, rot: 0 },
      { dx: 0, dz: -(roadWidth / 2 + 1.5), rot: 0 },
      { dx: roadWidth / 2 + 1.5, dz: 0, rot: Math.PI / 2 },
      { dx: -(roadWidth / 2 + 1.5), dz: 0, rot: Math.PI / 2 }
    ];

    for (const off of offsets) {
      const cw = new THREE.Group();
      cw.position.set(ix + off.dx, 0.025, iz + off.dz);
      cw.rotation.y = off.rot;

      for (let s = -5; s <= 5; s += 1.4) {
        const stripe = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 2.5), stripeMat);
        stripe.rotation.x = -Math.PI / 2;
        stripe.position.set(s, 0, 0);
        cw.add(stripe);
      }
      group.add(cw);
    }
  }

  createBlocksAndBuildings() {
    const coords = [-160, -80, 0, 80, 160];
    const roadWidth = 14;
    const sidewalkWidth = 2.5;

    // Create window texture with lighted grid
    const canvas = document.createElement('canvas');
    canvas.width = 128;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#1c2128';
    ctx.fillRect(0, 0, 128, 128);
    ctx.fillStyle = '#ffd666';
    for (let r = 0; r < 8; r++) {
      for (let c = 0; c < 8; c++) {
        // Randomly lit or unlit windows
        if ((r + c) % 3 !== 0) {
          ctx.fillRect(c * 16 + 3, r * 16 + 3, 10, 10);
        }
      }
    }
    const windowTex = new THREE.CanvasTexture(canvas);
    windowTex.wrapS = THREE.RepeatWrapping;
    windowTex.wrapT = THREE.RepeatWrapping;

    // Window lit material - responds to dusk/night clock
    const windowLitMat = new THREE.MeshStandardMaterial({
      color: 0x22262e,
      roughness: 0.3,
      metalness: 0.7,
      emissive: new THREE.Color(0xffd666),
      emissiveIntensity: 0.8,
      emissiveMap: windowTex
    });
    this.clock.registerLitMaterial(windowLitMat, 0xffd666);

    const buildingPalette = [
      new THREE.MeshStandardMaterial({ map: this.textures.concrete, roughness: 0.7 }),
      new THREE.MeshStandardMaterial({ map: this.textures.brick, roughness: 0.8 }),
      new THREE.MeshStandardMaterial({ map: this.textures.plaster, color: 0xddeeff, roughness: 0.6 }),
      new THREE.MeshStandardMaterial({ map: this.textures.concrete, color: 0x8899aa, roughness: 0.5 }),
      new THREE.MeshStandardMaterial({ map: this.textures.brick, color: 0xbb8877, roughness: 0.75 })
    ];

    const sidewalkMat = new THREE.MeshStandardMaterial({
      map: this.textures.sidewalk,
      roughness: 0.85
    });

    // 4x4 city blocks between the 5x5 intersection grid
    for (let bx = 0; bx < coords.length - 1; bx++) {
      for (let bz = 0; bz < coords.length - 1; bz++) {
        const x1 = coords[bx] + roadWidth / 2;
        const x2 = coords[bx + 1] - roadWidth / 2;
        const z1 = coords[bz] + roadWidth / 2;
        const z2 = coords[bz + 1] - roadWidth / 2;

        const blockW = x2 - x1;
        const blockD = z2 - z1;
        const centerX = (x1 + x2) / 2;
        const centerZ = (z1 + z2) / 2;

        // Sidewalk curb platform
        const sidewalkGeo = new THREE.BoxGeometry(blockW, 0.25, blockD);
        const sidewalk = new THREE.Mesh(sidewalkGeo, sidewalkMat);
        sidewalk.position.set(centerX, 0.125, centerZ);
        sidewalk.receiveShadow = true;
        this.scene.add(sidewalk);

        // Place 1 to 4 buildings on this block
        const usableW = blockW - sidewalkWidth * 2;
        const usableD = blockD - sidewalkWidth * 2;

        // Subdivide block into 2x2 lots or single large skyscraper
        const isSkyscraper = (bx + bz) % 3 === 0;

        if (isSkyscraper) {
          const bH = 50 + ((bx * 7 + bz * 13) % 45);
          const bGeo = new THREE.BoxGeometry(usableW * 0.85, bH, usableD * 0.85);
          const bMesh = new THREE.Mesh(bGeo, [
            windowLitMat,
            windowLitMat,
            buildingPalette[0],
            buildingPalette[0],
            windowLitMat,
            windowLitMat
          ]);
          bMesh.position.set(centerX, bH / 2 + 0.25, centerZ);
          bMesh.castShadow = true;
          bMesh.receiveShadow = true;
          this.scene.add(bMesh);

          const halfW = (usableW * 0.85) / 2;
          const halfD = (usableD * 0.85) / 2;
          this.buildingColliders.push({
            minX: centerX - halfW,
            maxX: centerX + halfW,
            minZ: centerZ - halfD,
            maxZ: centerZ + halfD
          });
        } else {
          // 4 smaller buildings
          const subW = usableW * 0.44;
          const subD = usableD * 0.44;
          const offsets = [
            { ox: -subW * 0.55, oz: -subD * 0.55, h: 22 + (bx * 5) % 18 },
            { ox: subW * 0.55, oz: -subD * 0.55, h: 28 + (bz * 6) % 20 },
            { ox: -subW * 0.55, oz: subD * 0.55, h: 32 + (bx * 9) % 24 },
            { ox: subW * 0.55, oz: subD * 0.55, h: 20 + (bz * 11) % 15 }
          ];

          offsets.forEach((off, idx) => {
            const bGeo = new THREE.BoxGeometry(subW, off.h, subD);
            const mat = buildingPalette[(bx + bz + idx) % buildingPalette.length];
            const bMesh = new THREE.Mesh(bGeo, [
              windowLitMat,
              windowLitMat,
              mat,
              mat,
              windowLitMat,
              windowLitMat
            ]);
            const px = centerX + off.ox;
            const pz = centerZ + off.oz;
            bMesh.position.set(px, off.h / 2 + 0.25, pz);
            bMesh.castShadow = true;
            bMesh.receiveShadow = true;
            this.scene.add(bMesh);

            this.buildingColliders.push({
              minX: px - subW / 2,
              maxX: px + subW / 2,
              minZ: pz - subD / 2,
              maxZ: pz + subD / 2
            });
          });
        }
      }
    }
  }

  createStreetFurniture() {
    const coords = [-160, -80, 0, 80, 160];
    const lampPoleMat = new THREE.MeshStandardMaterial({ color: 0x333842, metalness: 0.8, roughness: 0.3 });
    const lampHeadMat = new THREE.MeshStandardMaterial({
      color: 0xfff0bb,
      emissive: new THREE.Color(0xffd477),
      emissiveIntensity: 1.5
    });
    this.clock.registerLitMaterial(lampHeadMat, 0xffd477);

    for (let ix = 0; ix < coords.length; ix++) {
      for (let iz = 0; iz < coords.length; iz++) {
        const x = coords[ix];
        const z = coords[iz];

        // 4 corner streetlamps at each intersection
        const corners = [
          { dx: 9, dz: 9 },
          { dx: -9, dz: 9 },
          { dx: 9, dz: -9 },
          { dx: -9, dz: -9 }
        ];

        for (const c of corners) {
          const lamp = new THREE.Group();
          lamp.position.set(x + c.dx, 0.25, z + c.dz);

          // Pole
          const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.16, 6, 8), lampPoleMat);
          pole.position.y = 3;
          pole.castShadow = true;
          lamp.add(pole);

          // Arm & Head
          const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 8, 8), lampHeadMat);
          head.position.y = 6;
          lamp.add(head);

          // Point light
          const light = new THREE.PointLight(0xffea9f, 0.8, 25);
          light.position.y = 5.8;
          lamp.add(light);
          this.clock.registerStreetLight(light);

          this.scene.add(lamp);
        }
      }
    }
  }

  /**
   * Check collision between a bounding box or point with city buildings.
   */
  checkCollision(x, z, radius = 1.6) {
    for (const b of this.buildingColliders) {
      if (
        x + radius >= b.minX &&
        x - radius <= b.maxX &&
        z + radius >= b.minZ &&
        z - radius <= b.maxZ
      ) {
        // Collision detected
        const overlapLeft = (x + radius) - b.minX;
        const overlapRight = b.maxX - (x - radius);
        const overlapTop = (z + radius) - b.minZ;
        const overlapBottom = b.maxZ - (z - radius);

        const minOverlap = Math.min(overlapLeft, overlapRight, overlapTop, overlapBottom);
        let normalX = 0;
        let normalZ = 0;

        if (minOverlap === overlapLeft) normalX = -1;
        else if (minOverlap === overlapRight) normalX = 1;
        else if (minOverlap === overlapTop) normalZ = -1;
        else normalZ = 1;

        return {
          collided: true,
          normalX,
          normalZ,
          penetration: minOverlap
        };
      }
    }
    return { collided: false };
  }
}
