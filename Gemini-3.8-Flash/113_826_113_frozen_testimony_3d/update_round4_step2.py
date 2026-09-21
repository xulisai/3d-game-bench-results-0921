import re

with open('c4_step1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 6. Update createTallMirror to track mirrors and create 3D silhouette mesh groups
old_create_mirror = """      // Tall Corridor Mirrors in carved gold frames
      function createTallMirror(x, y, z, rotY) {
        const mirrorGroup = new THREE.Group();
        mirrorGroup.position.set(x, y, z);
        mirrorGroup.rotation.y = rotY;

        const frame = new THREE.Mesh(new THREE.BoxGeometry(1.4, 2.6, 0.1), matGoldTrim);
        frame.castShadow = true;
        mirrorGroup.add(frame);

        const glass = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 2.35), matMirrorGlass);
        glass.position.z = 0.06;
        mirrorGroup.add(glass);

        scene.add(mirrorGroup);
        addBoxCollider({
          minX: x - 0.7, maxX: x + 0.7,
          minZ: z - 0.7, maxZ: z + 0.7,
          minY: y - 1.3, maxY: y + 1.3
        });
      }
      createTallMirror(-4.95, 2.0, 3.8, Math.PI / 2);
      createTallMirror(4.95, 2.0, 3.8, -Math.PI / 2);"""

new_create_mirror = """      // Tall Corridor Mirrors in carved gold frames with Time View Silhouettes
      const corridorMirrors = [];

      function createTallMirror(x, y, z, rotY, locationName) {
        const mirrorGroup = new THREE.Group();
        mirrorGroup.position.set(x, y, z);
        mirrorGroup.rotation.y = rotY;

        const frame = new THREE.Mesh(new THREE.BoxGeometry(1.4, 2.6, 0.1), matGoldTrim);
        frame.castShadow = true;
        mirrorGroup.add(frame);

        // Mirror glass with faint sheen (roughness 0.08, metalness 0.95)
        const glassMat = new THREE.MeshStandardMaterial({
          color: 0x98b8d4,
          roughness: 0.08,
          metalness: 0.95,
          transparent: true,
          opacity: 0.92
        });
        const glass = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 2.35), glassMat);
        glass.position.z = 0.06;
        mirrorGroup.add(glass);

        // Faint moonlight sheen overlay
        const sheenPlane = new THREE.Mesh(
          new THREE.PlaneGeometry(1.12, 2.32),
          new THREE.MeshBasicMaterial({ color: 0x88bbff, transparent: true, opacity: 0.12, depthWrite: false })
        );
        sheenPlane.position.z = 0.065;
        mirrorGroup.add(sheenPlane);

        // Silhouette container inside mirror glass depth
        const silhouetteContainer = new THREE.Group();
        silhouetteContainer.position.set(0, -0.2, 0.07);
        silhouetteContainer.scale.set(0.68, 0.68, 0.68);
        mirrorGroup.add(silhouetteContainer);

        // Material for dark silhouette tableau figures
        const silMat = new THREE.MeshBasicMaterial({ color: 0x091220 });
        const silPropMat = new THREE.MeshBasicMaterial({ color: 0x142032 });

        // Five silhouette scenes
        const sceneMeshes = [];

        // 1. 19:00 — Butler crossing with a tray, making for the kitchen
        const scene1Group = new THREE.Group();
        const bHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 10), silMat);
        bHead.position.set(0, 1.6, 0);
        scene1Group.add(bHead);
        const bTorso = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.62, 0.26), silMat);
        bTorso.position.set(0, 1.25, 0);
        scene1Group.add(bTorso);
        const bLegs = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.9, 0.22), silMat);
        bLegs.position.set(0, 0.5, 0);
        scene1Group.add(bLegs);
        // Tray carried in front
        const bTray = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.02, 12), silPropMat);
        bTray.position.set(0.18, 1.2, 0.22);
        bTray.rotation.z = 0.1;
        scene1Group.add(bTray);
        scene1Group.visible = false;
        silhouetteContainer.add(scene1Group);
        sceneMeshes.push(scene1Group);

        // 2. 19:20 — Doctor heading for the study stairs
        const scene2Group = new THREE.Group();
        const dHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 10), silMat);
        dHead.position.set(0, 1.62, 0);
        scene2Group.add(dHead);
        const dTorso = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.64, 0.26), silMat);
        dTorso.position.set(0, 1.25, 0);
        scene2Group.add(dTorso);
        const dLeg1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.07, 0.95, 8), silMat);
        dLeg1.position.set(-0.12, 0.52, 0.1);
        dLeg1.rotation.x = -0.3; // Stepping posture
        scene2Group.add(dLeg1);
        const dLeg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.07, 0.95, 8), silMat);
        dLeg2.position.set(0.12, 0.52, -0.1);
        dLeg2.rotation.x = 0.3;
        scene2Group.add(dLeg2);
        // Small medical bag
        const dBag = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.22, 0.18), silPropMat);
        dBag.position.set(-0.3, 0.95, 0.05);
        scene2Group.add(dBag);
        scene2Group.visible = false;
        silhouetteContainer.add(scene2Group);
        sceneMeshes.push(scene2Group);

        // 3. 19:40 — Lady walking toward the drawing room
        const scene3Group = new THREE.Group();
        const lHead = new THREE.Mesh(new THREE.SphereGeometry(0.17, 10, 10), silMat);
        lHead.position.set(0, 1.6, 0);
        scene3Group.add(lHead);
        const lTorso = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 0.55, 10), silMat);
        lTorso.position.set(0, 1.25, 0);
        scene3Group.add(lTorso);
        const lSkirt = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.52, 1.0, 12), silMat);
        lSkirt.position.set(0, 0.52, 0);
        scene3Group.add(lSkirt);
        // Extended arm walking
        const lArm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.04, 0.55, 8), silMat);
        lArm.position.set(-0.25, 1.2, 0.1);
        lArm.rotation.x = -0.4;
        scene3Group.add(lArm);
        scene3Group.visible = false;
        silhouetteContainer.add(scene3Group);
        sceneMeshes.push(scene3Group);

        // 4. 20:00 — Gardener carrying a pail toward the kitchen
        const scene4Group = new THREE.Group();
        const gHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 10), silMat);
        gHead.position.set(0, 1.6, 0);
        scene4Group.add(gHead);
        const gCap = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.22, 0.06, 10), silMat);
        gCap.position.set(0, 1.74, 0.03);
        scene4Group.add(gCap);
        const gTorso = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.62, 0.28), silMat);
        gTorso.position.set(0, 1.25, 0);
        scene4Group.add(gTorso);
        const gLegs = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.9, 0.24), silMat);
        gLegs.position.set(0, 0.5, 0);
        scene4Group.add(gLegs);
        // Metal Pail held in hand
        const gPail = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.11, 0.28, 10), silPropMat);
        gPail.position.set(0.32, 0.75, 0.08);
        scene4Group.add(gPail);
        scene4Group.visible = false;
        silhouetteContainer.add(scene4Group);
        sceneMeshes.push(scene4Group);

        // 5. 20:20 — Guest stepping toward the garden door
        const scene5Group = new THREE.Group();
        const guHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 10, 10), silMat);
        guHead.position.set(0, 1.62, 0);
        scene5Group.add(guHead);
        const guTorso = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.64, 0.26), silMat);
        guTorso.position.set(0, 1.25, 0);
        scene5Group.add(guTorso);
        const guLeg1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.07, 0.95, 8), silMat);
        guLeg1.position.set(-0.12, 0.52, 0.12);
        guLeg1.rotation.x = -0.35;
        scene5Group.add(guLeg1);
        const guLeg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.07, 0.95, 8), silMat);
        guLeg2.position.set(0.12, 0.52, -0.12);
        guLeg2.rotation.x = 0.35;
        scene5Group.add(guLeg2);
        scene5Group.visible = false;
        silhouetteContainer.add(scene5Group);
        sceneMeshes.push(scene5Group);

        scene.add(mirrorGroup);
        addBoxCollider({
          minX: x - 0.7, maxX: x + 0.7,
          minZ: z - 0.7, maxZ: z + 0.7,
          minY: y - 1.3, maxY: y + 1.3
        });

        corridorMirrors.push({
          pos: new THREE.Vector3(x, y, z),
          locationName,
          mirrorGroup,
          glassMat,
          sheenPlane,
          silhouetteContainer,
          sceneMeshes
        });
      }

      // West Corridor mirror (near drawing room archway)
      createTallMirror(-4.95, 2.0, 3.8, Math.PI / 2, 'West Corridor Mirror');
      // East Corridor mirror (near kitchen archway)
      createTallMirror(4.95, 2.0, 3.8, -Math.PI / 2, 'East Corridor Mirror');"""

assert old_create_mirror in html, "old_create_mirror not matched"
html = html.replace(old_create_mirror, new_create_mirror)

print("Mirror creation & silhouette meshes replaced successfully")
with open('c4_step2.html', 'w', encoding='utf-8') as f:
    f.write(html)
