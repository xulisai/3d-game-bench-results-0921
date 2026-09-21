/**
 * Mission & Job Board System for Los Santos Drive
 * Cycles delivery, checkpoint-sprint, and repo missions.
 * Golden ring serves as signpost; driving through it does NOT auto-accept (KeyM required).
 * Sprint countdown timer is 70 seconds.
 */

import * as THREE from 'three';

export class MissionSystem {
  constructor(scene, roadGraph) {
    this.scene = scene;
    this.roadGraph = roadGraph;

    this.jobsDone = 0;

    this.missionActive = false;
    this.missionKind = null; // 'delivery' | 'sprint' | 'repo' | null
    this.jobIndex = 0;
    this.jobTypes = ['delivery', 'sprint', 'repo'];

    this.currentObjectives = [];
    this.objectiveIndex = 0;
    this.timer = 0; // Countdown timer for sprint missions (70s)

    // Visual waypoint marker in 3D (golden ring + beacon)
    this.markerGroup = new THREE.Group();
    this.scene.add(this.markerGroup);

    this.initMarker();

    // Initial signpost location for the next available job on the road graph
    this.nextJobPreviewPos = this.roadGraph.getRandomLanePosition();
    this.updateMarkerPosition();
  }

  initMarker() {
    // Glowing ground ring
    const ringGeo = new THREE.RingGeometry(2.0, 2.5, 32);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0xffcc00,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.1;
    this.markerGroup.add(ring);
    this.markerRing = ring;

    // Glowing vertical light pillar
    const cylinderGeo = new THREE.CylinderGeometry(2.2, 2.2, 14, 24, 1, true);
    const cylinderMat = new THREE.MeshBasicMaterial({
      color: 0xffbb00,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
      depthWrite: false
    });
    const pillar = new THREE.Mesh(cylinderGeo, cylinderMat);
    pillar.position.y = 7;
    this.markerGroup.add(pillar);

    // Floating diamond beacon
    const diamondGeo = new THREE.OctahedronGeometry(1.2, 0);
    const diamondMat = new THREE.MeshStandardMaterial({
      color: 0xffe600,
      emissive: 0xffaa00,
      emissiveIntensity: 0.8,
      roughness: 0.2
    });
    const diamond = new THREE.Mesh(diamondGeo, diamondMat);
    diamond.position.y = 4.5;
    this.markerGroup.add(diamond);
    this.diamond = diamond;
  }

  acceptJob() {
    if (this.missionActive) return false;

    this.missionKind = this.jobTypes[this.jobIndex % this.jobTypes.length];
    this.jobIndex++;
    this.missionActive = true;
    this.objectiveIndex = 0;
    this.currentObjectives = [];

    if (this.missionKind === 'delivery') {
      const p1 = this.roadGraph.getRandomLanePosition();
      const p2 = this.roadGraph.getRandomLanePosition();
      this.currentObjectives = [
        { x: p1.x, z: p1.z, title: 'Pick up package', desc: 'Drive to the pickup point' },
        { x: p2.x, z: p2.z, title: 'Deliver package', desc: 'Deliver cargo to client destination' }
      ];
    } else if (this.missionKind === 'sprint') {
      this.timer = 70.0; // Sprints get strictly 70 seconds
      const p1 = this.roadGraph.getRandomLanePosition();
      const p2 = this.roadGraph.getRandomLanePosition();
      const p3 = this.roadGraph.getRandomLanePosition();
      this.currentObjectives = [
        { x: p1.x, z: p1.z, title: 'Checkpoint 1/3', desc: 'Hit Checkpoint 1 before time runs out' },
        { x: p2.x, z: p2.z, title: 'Checkpoint 2/3', desc: 'Hit Checkpoint 2' },
        { x: p3.x, z: p3.z, title: 'Finish Line', desc: 'Sprint to the final checkpoint!' }
      ];
    } else if (this.missionKind === 'repo') {
      const p1 = this.roadGraph.getRandomLanePosition();
      const p2 = this.roadGraph.getRandomLanePosition();
      this.currentObjectives = [
        { x: p1.x, z: p1.z, title: 'Locate Target', desc: 'Find the targeted vehicle on the road' },
        { x: p2.x, z: p2.z, title: 'Deliver to Impound', desc: 'Bring vehicle to the impound lot' }
      ];
    }

    this.updateMarkerPosition();
    return true;
  }

  updateMarkerPosition() {
    if (!this.missionActive) {
      // Position marker at next job preview on the road graph
      if (this.nextJobPreviewPos) {
        this.markerGroup.position.set(this.nextJobPreviewPos.x, 0, this.nextJobPreviewPos.z);
        this.markerGroup.visible = true;
      }
      return;
    }

    if (this.objectiveIndex >= this.currentObjectives.length) {
      this.markerGroup.visible = false;
      return;
    }

    const target = this.currentObjectives[this.objectiveIndex];
    this.markerGroup.position.set(target.x, 0, target.z);
    this.markerGroup.visible = true;
  }

  update(dt, playerX, playerZ) {
    // Rotate and animate marker
    if (this.diamond) {
      this.diamond.rotation.y += dt * 2.0;
      this.diamond.position.y = 4.5 + Math.sin(Date.now() * 0.005) * 0.4;
    }
    if (this.markerRing) {
      const scale = 1.0 + Math.sin(Date.now() * 0.008) * 0.15;
      this.markerRing.scale.set(scale, scale, 1);
    }

    // When no mission is active:
    // Rule: "金色任务环只做路标，开车穿过它不再自动接任务——必须按 M 才算接。"
    if (!this.missionActive) {
      if (this.nextJobPreviewPos) {
        this.markerGroup.position.set(this.nextJobPreviewPos.x, 0, this.nextJobPreviewPos.z);
        this.markerGroup.visible = true;
      }
      // Explicitly DO NOT auto-accept on driving through!
      return;
    }

    // Sprint countdown timer (70 seconds limit)
    if (this.missionKind === 'sprint') {
      this.timer -= dt;
      if (this.timer <= 0) {
        // Mission Failed
        this.missionActive = false;
        this.missionKind = null;
        this.nextJobPreviewPos = this.roadGraph.getRandomLanePosition();
        this.updateMarkerPosition();
        return;
      }
    }

    // Check distance to current active objective
    const current = this.currentObjectives[this.objectiveIndex];
    if (current) {
      const dx = playerX - current.x;
      const dz = playerZ - current.z;
      const dist = Math.hypot(dx, dz);

      if (dist < 6.0) {
        // Objective reached
        this.objectiveIndex++;
        if (this.objectiveIndex >= this.currentObjectives.length) {
          // Mission Complete!
          this.jobsDone++;
          this.missionActive = false;
          this.missionKind = null;
          this.nextJobPreviewPos = this.roadGraph.getRandomLanePosition();
          this.updateMarkerPosition();
        } else {
          this.updateMarkerPosition();
        }
      }
    }
  }

  get reputation() {
    return this.jobsDone * 100;
  }

  getCurrentObjectiveInfo() {
    if (!this.missionActive || this.objectiveIndex >= this.currentObjectives.length) {
      return null;
    }
    const obj = this.currentObjectives[this.objectiveIndex];
    return {
      kind: this.missionKind,
      title: obj.title,
      desc: obj.desc,
      x: obj.x,
      z: obj.z,
      timer: this.timer
    };
  }
}
