/**
 * Day/Night Cycle and Lighting Controller for Los Santos Drive
 * Starts at dusk: hour = 17.25
 */

import * as THREE from 'three';

export class DayNightClock {
  constructor(scene) {
    this.scene = scene;
    this.startHour = 17.25; // 17:15 Dusk
    this.hour = 17.25;
    this.totalSeconds = 0;
    // 1 real second = 0.03 game hours (1 full 24h cycle in 800 seconds)
    this.timeScale = 0.03;

    this.litMaterials = []; // Materials whose emissive properties respond to night/dusk
    this.streetLights = []; // Street light sources

    this.initLighting();
  }

  initLighting() {
    // Ambient light
    this.ambientLight = new THREE.AmbientLight(0xddeeff, 0.6);
    this.scene.add(this.ambientLight);

    // Sun / Moon directional light
    this.dirLight = new THREE.DirectionalLight(0xfffaed, 1.2);
    this.dirLight.position.set(100, 150, 100);
    this.dirLight.castShadow = true;
    this.dirLight.shadow.mapSize.width = 2048;
    this.dirLight.shadow.mapSize.height = 2048;
    this.dirLight.shadow.camera.near = 10;
    this.dirLight.shadow.camera.far = 400;
    const d = 120;
    this.dirLight.shadow.camera.left = -d;
    this.dirLight.shadow.camera.right = d;
    this.dirLight.shadow.camera.top = d;
    this.dirLight.shadow.camera.bottom = -d;
    this.dirLight.shadow.bias = -0.0005;
    this.scene.add(this.dirLight);

    // Fog for atmospheric depth
    this.scene.fog = new THREE.FogExp2(0x181c2b, 0.0025);
  }

  registerLitMaterial(material, baseColor = 0xffe680) {
    this.litMaterials.push({ material, baseColor });
  }

  registerStreetLight(light) {
    this.streetLights.push(light);
  }

  update(dt) {
    this.totalSeconds += dt;
    this.hour = (this.startHour + this.totalSeconds * this.timeScale) % 24;

    // Calculate time of day factors
    // 6.0: Dawn, 12.0: Noon, 17.25: Dusk, 20.0+: Night
    const h = this.hour;

    // Dusk factor: 1.0 during dusk/night (17.5 to 6.0), 0.0 at midday (11.0 to 15.0)
    let nightFactor = 0;
    if (h >= 17.0 && h <= 19.5) {
      // Dusk transition from 17.0 to 19.5
      nightFactor = (h - 17.0) / 2.5;
    } else if (h > 19.5 || h < 5.0) {
      // Full night
      nightFactor = 1.0;
    } else if (h >= 5.0 && h <= 7.0) {
      // Dawn transition
      nightFactor = 1.0 - (h - 5.0) / 2.0;
    } else {
      // Daytime
      nightFactor = 0.0;
    }

    // Windows specifically come on at dusk (starts ramping at 17.20, full at 18.0)
    let windowGlow = 0;
    if (h >= 17.20 && h <= 18.2) {
      windowGlow = (h - 17.20) / 1.0;
    } else if (h > 18.2 || h < 6.0) {
      windowGlow = 1.0;
    } else if (h >= 6.0 && h <= 7.0) {
      windowGlow = 1.0 - (h - 6.0);
    } else {
      windowGlow = 0.05; // tiny ambient reflection in daytime
    }

    // Update lit materials (building windows)
    for (const item of this.litMaterials) {
      if (item.material.emissive) {
        item.material.emissive.setHex(item.baseColor);
        item.material.emissiveIntensity = THREE.MathUtils.lerp(0.05, 1.8, windowGlow);
      }
    }

    // Update street lights
    for (const light of this.streetLights) {
      light.intensity = THREE.MathUtils.lerp(0.0, 1.2, windowGlow);
    }

    // Update Sun & Moon positions
    // Sun angle based on 24h
    const sunAngle = ((h - 6.0) / 24.0) * Math.PI * 2;
    const sunDist = 200;
    const sunY = Math.sin(sunAngle) * sunDist;
    const sunX = Math.cos(sunAngle) * sunDist;

    if (sunY > -10) {
      // Sun is up
      this.dirLight.position.set(sunX, Math.max(sunY, 15), 80);
      const sunRatio = Math.max(0, sunY / sunDist);
      // Sunset orange at dusk
      if (h >= 16.5 && h <= 19.0) {
        this.dirLight.color.setHex(0xff7733);
        this.dirLight.intensity = Math.max(0.2, (19.0 - h) / 2.5 * 1.2);
        this.ambientLight.color.setHex(0x554455);
        this.ambientLight.intensity = 0.45;
        this.scene.background = new THREE.Color(0x3a2538);
        this.scene.fog.color.setHex(0x3a2538);
      } else {
        // Day
        this.dirLight.color.setHex(0xfffaed);
        this.dirLight.intensity = 1.2 * sunRatio;
        this.ambientLight.color.setHex(0xaaccff);
        this.ambientLight.intensity = 0.6;
        this.scene.background = new THREE.Color(0x6aa0d8);
        this.scene.fog.color.setHex(0x6aa0d8);
      }
    } else {
      // Moon / Night
      this.dirLight.position.set(-sunX, -sunY * 0.7 + 20, -60);
      this.dirLight.color.setHex(0x8899cc);
      this.dirLight.intensity = 0.25;
      this.ambientLight.color.setHex(0x1a223a);
      this.ambientLight.intensity = 0.35;
      this.scene.background = new THREE.Color(0x0a0d18);
      this.scene.fog.color.setHex(0x0a0d18);
    }
  }

  getFormattedTime() {
    const totalMinutes = Math.floor(this.hour * 60);
    const hh = Math.floor(totalMinutes / 60) % 24;
    const mm = totalMinutes % 60;
    return `${hh.toString().padStart(2, '0')}:${mm.toString().padStart(2, '0')}`;
  }
}
