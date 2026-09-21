const fs = require('fs');
const THREE = require('./assets/_shared/three/build/three.min.js');

const SQRT2_INV = 1.0 / Math.SQRT2; // ~0.7071

const HOLES = [
  {
    number: 1,
    par: 4,
    distance: 380,
    tee: new THREE.Vector3(0, 0, 0),
    cup: new THREE.Vector3(0, 0, 380),
    fairwayZMin: 45,
    fairwayZMax: 338,
    fairwayHalfWidth: 18,
    greenRadius: 18.0,
    teeZMin: -15,
    teeZMax: 35,
    teeHalfWidth: 10,
    bunkerCenter1: new THREE.Vector2(-5, 344),
    bunkerRadius1: 9.5,
    bunkerCenter2: new THREE.Vector2(6, 346),
    bunkerRadius2: 8.5,
    bunkerIndent: new THREE.Vector2(0, 350),
    pondCenter: new THREE.Vector2(32, 180),
    pondRadiusX: 14,
    pondRadiusZ: 36,
    dropZone: { x: 0, z: 140 },
    yardMarkers: [250, 200, 150, 100],
    isDogleg: false,
    wind: {
      speed: 0,
      direction: 'Calm',
      arrowRotation: 0,
      vecX: 0,
      vecZ: 0
    },
    slope: {
      isTwoTier: false,
      grade: 4,
      downhill: { x: SQRT2_INV, z: SQRT2_INV } // Northeast (+X, +Z)
    }
  },
  {
    number: 2,
    par: 3,
    distance: 165,
    tee: new THREE.Vector3(150, 0, 0),
    cup: new THREE.Vector3(150, 0, 165),
    fairwayZMin: 30,
    fairwayZMax: 135,
    fairwayHalfWidth: 16,
    greenRadius: 16.0,
    teeZMin: -15,
    teeZMax: 25,
    teeHalfWidth: 9,
    bunkerCenter1: new THREE.Vector2(145, 140),
    bunkerRadius1: 8.0,
    bunkerCenter2: new THREE.Vector2(155, 142),
    bunkerRadius2: 7.5,
    bunkerIndent: new THREE.Vector2(150, 145),
    pondCenter: new THREE.Vector2(178, 85),
    pondRadiusX: 12,
    pondRadiusZ: 24,
    dropZone: { x: 150, z: 58 },
    yardMarkers: [150, 100],
    isDogleg: false,
    wind: {
      speed: 12,
      direction: 'S',
      arrowRotation: 180,
      vecX: 0,
      vecZ: -12
    },
    slope: {
      isTwoTier: false,
      grade: 6,
      downhill: { x: 0, z: -1.0 } // Due South (-Z)
    }
  },
  {
    number: 3,
    par: 5,
    distance: 520,
    tee: new THREE.Vector3(300, 0, 0),
    cup: new THREE.Vector3(300, 0, 520),
    fairwayZMin: 45,
    fairwayZMax: 475,
    fairwayHalfWidth: 20,
    greenRadius: 19.0,
    teeZMin: -15,
    teeZMax: 35,
    teeHalfWidth: 10,
    bunkerCenter1: new THREE.Vector2(294, 480),
    bunkerRadius1: 10.0,
    bunkerCenter2: new THREE.Vector2(307, 482),
    bunkerRadius2: 9.0,
    bunkerIndent: new THREE.Vector2(300, 487),
    pondCenter: new THREE.Vector2(334, 250),
    pondRadiusX: 16,
    pondRadiusZ: 44,
    dropZone: { x: 300, z: 200 },
    yardMarkers: [400, 300, 250, 200, 150, 100],
    isDogleg: false,
    wind: {
      speed: 15,
      direction: 'E',
      arrowRotation: 90,
      vecX: 15,
      vecZ: 0
    },
    slope: {
      isTwoTier: true,
      ridgeZ: 518.0,
      frontTier: {
        grade: 5,
        downhill: { x: -SQRT2_INV, z: -SQRT2_INV } // Southwest (-X, -Z)
      },
      backTier: {
        grade: 3,
        downhill: { x: SQRT2_INV, z: -SQRT2_INV } // Southeast (+X, -Z)
      }
    }
  },
  {
    number: 4,
    par: 4,
    distance: 400,
    tee: new THREE.Vector3(450, 0, 0),
    cup: new THREE.Vector3(420, 0, 400),
    fairwayZMin: 45,
    fairwayZMax: 360,
    fairwayHalfWidth: 22,
    greenRadius: 18.0,
    teeZMin: -15,
    teeZMax: 35,
    teeHalfWidth: 10,
    bunkerCenter1: new THREE.Vector2(415, 365),
    bunkerRadius1: 9.0,
    bunkerCenter2: new THREE.Vector2(426, 368),
    bunkerRadius2: 8.0,
    bunkerIndent: new THREE.Vector2(420, 372),
    pondCenter: new THREE.Vector2(480, 200),
    pondRadiusX: 14,
    pondRadiusZ: 38,
    dropZone: { x: 450, z: 155 },
    yardMarkers: [250, 200, 150, 100],
    isDogleg: true,
    wind: {
      speed: 18,
      direction: 'N',
      arrowRotation: 0,
      vecX: 0,
      vecZ: 18
    },
    slope: {
      isTwoTier: false,
      grade: 3,
      downhill: { x: 0, z: -1.0 } // Toward Front (-Z)
    }
  },
  // Hole 5: Island green par-3, 165 yards
  {
    number: 5,
    par: 3,
    distance: 165,
    tee: new THREE.Vector3(600, 0, 0),
    cup: new THREE.Vector3(600, 0, 165),
    fairwayZMin: 0,
    fairwayZMax: 0, // No fairway approach!
    fairwayHalfWidth: 0,
    greenRadius: 22.0,
    teeZMin: -15,
    teeZMax: 20,
    teeHalfWidth: 12,
    bunkerCenter1: new THREE.Vector2(-999, -999),
    bunkerRadius1: 0,
    bunkerCenter2: new THREE.Vector2(-999, -999),
    bunkerRadius2: 0,
    bunkerIndent: new THREE.Vector2(-999, -999),
    pondCenter: new THREE.Vector2(600, 105),
    pondRadiusX: 45,
    pondRadiusZ: 85,
    dropZone: { x: 600, z: 22 },
    yardMarkers: [150, 100],
    isDogleg: false,
    wind: {
      speed: 0,
      direction: 'Calm',
      arrowRotation: 0,
      vecX: 0,
      vecZ: 0
    },
    slope: {
      isTwoTier: false,
      grade: 4,
      downhill: { x: 0, z: -1.0 } // 4% toward front
    }
  }
];

const CUP_RADIUS = 0.3;
const CUP_MAX_SPEED = 3.0;
const TREE_TRUNK_RADIUS = 1.2;

const CLUBS = {
  'Driver': { name: 'Driver', key: '1', baseDistance: 260, launchAngle: 0.24, spinRating: 0.18, isWedge: false, isPutter: false },
  '3-Wood': { name: '3-Wood', key: '2', baseDistance: 235, launchAngle: 0.26, spinRating: 0.22, isWedge: false, isPutter: false },
  '7-Iron': { name: '7-Iron', key: '3', baseDistance: 165, launchAngle: 0.35, spinRating: 0.32, isWedge: false, isPutter: false },
  'Pitching Wedge': { name: 'Pitching Wedge', key: '4', baseDistance: 110, launchAngle: 0.44, spinRating: 0.42, isWedge: true, bunkerMultiplier: 0.65, isPutter: false },
  'Sand Wedge': { name: 'Sand Wedge', key: '5', baseDistance: 70, launchAngle: 0.52, spinRating: 0.48, isWedge: true, bunkerMultiplier: 0.55, isPutter: false },
  'Putter': { name: 'Putter', key: '6', baseDistance: 25, launchAngle: 0.0, spinRating: 0.0, isWedge: false, isPutter: true }
};

function getGreenGradientAt(hole, x, z) {
  const sl = hole.slope;
  if (!sl.isTwoTier) {
    return {
      grade: sl.grade,
      downhill: sl.downhill,
      tier: null
    };
  } else {
    const tier = (z < sl.ridgeZ) ? 'front' : 'back';
    const tierData = (tier === 'front') ? sl.frontTier : sl.backTier;
    return {
      grade: tierData.grade,
      downhill: tierData.downhill,
      tier: tier
    };
  }
}

function isInsidePondForHole(h, x, z) {
  if (h.number === 5) {
    const isTeePeninsula = (z >= h.teeZMin - 2 && z <= h.teeZMax + 6 && Math.abs(x - h.tee.x) <= h.teeHalfWidth + 3);
    const isGreenIsland = Math.hypot(x - h.cup.x, z - h.cup.z) <= (h.islandLandRadius || (h.greenRadius + 6.0));
    if (isTeePeninsula || isGreenIsland) return false;
    const dx = (x - h.pondCenter.x) / h.pondRadiusX;
    const dz = (z - h.pondCenter.y) / h.pondRadiusZ;
    return (dx * dx + dz * dz) <= 1.0;
  }
  const dx = (x - h.pondCenter.x) / h.pondRadiusX;
  const dz = (z - h.pondCenter.y) / h.pondRadiusZ;
  return (dx * dx + dz * dz) <= 1.0;
}

function isInsideBunkerForHole(h, x, z) {
  if (!h.bunkerRadius1) return false;
  const d1 = Math.hypot(x - h.bunkerCenter1.x, z - h.bunkerCenter1.y);
  const d2 = Math.hypot(x - h.bunkerCenter2.x, z - h.bunkerCenter2.y);
  if (d1 <= h.bunkerRadius1 || d2 <= h.bunkerRadius2) {
    const dIndent = Math.hypot(x - h.bunkerIndent.x, z - h.bunkerIndent.y);
    if (dIndent < 3.2 && z > (h.cup.z - 30)) return false;
    return true;
  }
  return false;
}

function isInsideGreenForHole(h, x, z) {
  return Math.hypot(x - h.cup.x, z - h.cup.z) <= h.greenRadius;
}

function isInsideTeeForHole(h, x, z) {
  return (z >= h.teeZMin && z <= h.teeZMax && Math.abs(x - h.tee.x) <= h.teeHalfWidth);
}

function getFairwayCenterlineForHole(h, z) {
  if (h.number === 5) return h.tee.x;
  if (!h.isDogleg) {
    return h.tee.x + Math.sin(z * 0.03) * 3.5;
  } else {
    if (z <= 180) {
      return h.tee.x;
    } else if (z >= 360) {
      return h.cup.x;
    } else {
      const t = (z - 180) / (360 - 180);
      const bend = (1 - Math.cos(t * Math.PI)) / 2;
      return h.tee.x + (h.cup.x - h.tee.x) * bend;
    }
  }
}

function isInsideFairwayForHole(h, x, z) {
  if (h.number === 5) return false;
  if (z >= h.fairwayZMin && z <= h.fairwayZMax) {
    const cl = getFairwayCenterlineForHole(h, z);
    return Math.abs(x - cl) <= h.fairwayHalfWidth;
  }
  return false;
}

function getLieZone(h, x, z, isOpening = false) {
  if (isInsidePondForHole(h, x, z)) return 'Water';
  if (isInsideBunkerForHole(h, x, z)) return 'Bunker';
  if (isInsideGreenForHole(h, x, z)) return 'Green';
  if (isOpening && isInsideTeeForHole(h, x, z)) return 'Tee';
  if (isInsideFairwayForHole(h, x, z)) return 'Fairway';
  return 'Rough';
}

function getTerrainHeight(x, z) {
  let h = Math.sin(x * 0.035) * 0.4 + Math.cos(z * 0.02) * 0.5 - 0.2;
  for (let i = 0; i < HOLES.length; i++) {
    const hole = HOLES[i];
    const dGreen = Math.hypot(x - hole.cup.x, z - hole.cup.z);
    if (dGreen < hole.greenRadius + 8) {
      const blend = Math.max(0, Math.min(1, (dGreen - (hole.greenRadius - 3)) / 11));
      const dx_cup = x - hole.cup.x;
      const dz_cup = z - hole.cup.z;
      const grad = getGreenGradientAt(hole, x, z);
      const slopeHeightOffset = -(dx_cup * grad.downhill.x + dz_cup * grad.downhill.z) * (grad.grade / 100.0);
      const greenH = 0.08 + slopeHeightOffset;
      h = greenH * (1 - blend) + h * blend;
    }
    if (isInsideBunkerForHole(hole, x, z)) {
      h = -0.3;
    }
    if (isInsidePondForHole(hole, x, z)) {
      h = -1.2;
    }
    if (z >= hole.teeZMin - 2 && z <= hole.teeZMax + 2 && Math.abs(x - hole.tee.x) <= hole.teeHalfWidth + 2) {
      h = 0.0;
    }
  }
  return h;
}

const GRAVITY = 9.81 * 3.0;
const AIR_DRAG = 0.0032;
const GROUND_ROLL_FRICTION_PUTTER = 0.82;
const GROUND_ROLL_FRICTION_FAIRWAY = 0.42;
const GROUND_ROLL_FRICTION_ROUGH = 0.15;
const GROUND_BOUNCE_RESTITUTION = 0.28;

const treePositions = [];
for (let tz = 210; tz <= 245; tz += 6.5) {
  const tx = 450 - ((tz - 210) / (245 - 210)) * 26.0;
  treePositions.push({ x: tx, z: tz, radius: TREE_TRUNK_RADIUS });
}

function checkTreeCollisions(pPrev, pNext) {
  for (let i = 0; i < treePositions.length; i++) {
    const tree = treePositions[i];
    const segX = pNext.x - pPrev.x;
    const segZ = pNext.z - pPrev.z;
    const segLenSq = segX * segX + segZ * segZ;
    let u = 0;
    if (segLenSq > 1e-6) {
      u = ((tree.x - pPrev.x) * segX + (tree.z - pPrev.z) * segZ) / segLenSq;
      u = Math.max(0, Math.min(1, u));
    }
    const closestX = pPrev.x + u * segX;
    const closestZ = pPrev.z + u * segZ;
    const dSq = (closestX - tree.x) * (closestX - tree.x) + (closestZ - tree.z) * (closestZ - tree.z);
    if (dSq <= tree.radius * tree.radius) {
      return { hit: true, x: closestX, z: closestZ };
    }
  }
  return { hit: false };
}

function calculateInitialVelocity(clubName, powerVal, offsetVal, lieZone, aimRad, shapeIntent, hole, windMod = 0, isRain = false) {
  const club = CLUBS[clubName];
  let baseDist = club.baseDistance;

  let shapeCurveDeg = 0.0;
  if (shapeIntent === 'draw') shapeCurveDeg = -12.0;
  else if (shapeIntent === 'fade') shapeCurveDeg = 12.0;

  const absOffset = Math.abs(offsetVal);
  let distMult = 1.0;
  let missCurveDeg = 0.0;
  let isShank = false;

  if (absOffset <= 3) {
    distMult = 1.0;
    missCurveDeg = 0.0;
  } else if (absOffset <= 40) {
    distMult = 1.0 - (absOffset - 3) * 0.012;
    missCurveDeg = (absOffset - 3) * 0.35;
    if (offsetVal < 0) missCurveDeg = -missCurveDeg;
  } else {
    distMult = 0.25;
    missCurveDeg = (offsetVal >= 0 ? 40 : -40);
    isShank = true;
  }

  // Bunker
  if (lieZone === 'Bunker') {
    if (club.isWedge) {
      const bunkerMult = club.bunkerMultiplier;
      let dist = (baseDist * bunkerMult) * (powerVal / 100.0);
      let totalCurveDeg = isShank ? missCurveDeg : (shapeCurveDeg + missCurveDeg);
      const totalDist = Math.max(1.0, dist * distMult);

      const launchAngle = 0.62;
      const launchSpeed = Math.sqrt((totalDist / 0.85) * GRAVITY / Math.sin(2 * launchAngle));
      const vy = launchSpeed * Math.sin(launchAngle);
      const flightDuration = Math.max(0.5, (2 * vy) / GRAVITY);

      let windDistAdj = 0.0;
      let windCurveDeg = 0.0;
      const effWindSpeed = (hole.wind.speed > 0 || windMod > 0) ? (hole.wind.speed + windMod) : 0;
      if (effWindSpeed > 0) {
        let dirX = 0, dirZ = 0;
        if (hole.wind.speed > 0) {
          dirX = hole.wind.vecX / hole.wind.speed;
          dirZ = hole.wind.vecZ / hole.wind.speed;
        }
        const wx = dirX * effWindSpeed;
        const wz = dirZ * effWindSpeed;
        const aimAx = Math.sin(aimRad);
        const aimAz = Math.cos(aimRad);
        const w_parallel = wx * aimAx + wz * aimAz;
        if (w_parallel > 0) {
          windDistAdj = 0.3 * w_parallel * flightDuration;
        } else {
          windDistAdj = -0.6 * Math.abs(w_parallel) * flightDuration;
        }
        const w_perp = wx * aimAz - wz * aimAx;
        windCurveDeg = 0.4 * w_perp * flightDuration;
      }

      const finalDist = Math.max(1.0, totalDist + windDistAdj);
      const finalLaunchSpeed = Math.sqrt((finalDist / 0.85) * GRAVITY / Math.sin(2 * launchAngle));
      const vHoriz = finalLaunchSpeed * Math.cos(launchAngle);
      const vVert = finalLaunchSpeed * Math.sin(launchAngle);

      const finalCurveDeg = totalCurveDeg + windCurveDeg;
      const curveRad = THREE.MathUtils.degToRad(finalCurveDeg);
      const lateralDist = finalDist * Math.sin(curveRad);
      const latAccMag = (2 * lateralDist) / (flightDuration * flightDuration);
      const latDir = new THREE.Vector3(Math.cos(aimRad), 0, -Math.sin(aimRad));

      return {
        vel: new THREE.Vector3(Math.sin(aimRad) * vHoriz, vVert, Math.cos(aimRad) * vHoriz),
        latAcc: latDir.multiplyScalar(latAccMag),
        spinLift: club.spinRating * 5.0,
        isBunker: true,
        minimalRoll: true,
        flightDuration: flightDuration
      };
    } else {
      const chunkDist = baseDist * 0.15;
      const launchAngle = 0.12;
      const launchSpeed = Math.sqrt((chunkDist / 0.90) * GRAVITY / Math.sin(2 * launchAngle));
      const vHoriz = launchSpeed * Math.cos(launchAngle);
      const vVert = launchSpeed * Math.sin(launchAngle);

      return {
        vel: new THREE.Vector3(Math.sin(aimRad) * vHoriz, vVert, Math.cos(aimRad) * vHoriz),
        latAcc: new THREE.Vector3(0, 0, 0),
        spinLift: 0.1,
        isBunker: true,
        minimalRoll: false,
        flightDuration: (2 * vVert) / GRAVITY
      };
    }
  }

  let lieMultiplier = 1.0;
  let isRough = false;
  if (lieZone === 'Rough') {
    lieMultiplier = 0.85;
    isRough = true;
  }

  if (isRain && (lieZone === 'Fairway' || lieZone === 'Rough')) {
    lieMultiplier *= 0.92;
  }

  let dist = (baseDist * lieMultiplier) * (powerVal / 100.0);
  let curveBeforeWind = isShank ? missCurveDeg : (shapeCurveDeg + missCurveDeg);
  if (isRough) {
    curveBeforeWind *= 2.0;
  }

  const totalDist = Math.max(1.0, dist * distMult);

  if (club.isPutter) {
    const lambda = -Math.log(GROUND_ROLL_FRICTION_PUTTER);
    const rollSpeed = totalDist * lambda;
    const aimWithCurve = aimRad + THREE.MathUtils.degToRad(curveBeforeWind);
    return {
      vel: new THREE.Vector3(Math.sin(aimWithCurve) * rollSpeed, 0, Math.cos(aimWithCurve) * rollSpeed),
      latAcc: new THREE.Vector3(0, 0, 0),
      isBunker: false,
      minimalRoll: false,
      flightDuration: 0
    };
  }

  const launchAngle = club.launchAngle;
  const carryTarget = Math.max(1.0, totalDist - 16.0);
  const launchSpeed = Math.sqrt((carryTarget / 0.77) * GRAVITY / Math.sin(2 * launchAngle));
  const vVertical = launchSpeed * Math.sin(launchAngle);
  const flightDuration = Math.max(0.5, (2 * vVertical) / GRAVITY);

  let windDistAdj = 0.0;
  let windCurveDeg = 0.0;
  const effWindSpeed = (hole.wind.speed > 0 || windMod > 0) ? (hole.wind.speed + windMod) : 0;
  if (effWindSpeed > 0) {
    let dirX = 0, dirZ = 0;
    if (hole.wind.speed > 0) {
      dirX = hole.wind.vecX / hole.wind.speed;
      dirZ = hole.wind.vecZ / hole.wind.speed;
    }
    const wx = dirX * effWindSpeed;
    const wz = dirZ * effWindSpeed;
    const aimAx = Math.sin(aimRad);
    const aimAz = Math.cos(aimRad);
    const w_parallel = wx * aimAx + wz * aimAz;
    if (w_parallel > 0) {
      windDistAdj = 0.3 * w_parallel * flightDuration;
    } else {
      windDistAdj = -0.6 * Math.abs(w_parallel) * flightDuration;
    }
    const w_perp = wx * aimAz - wz * aimAx;
    windCurveDeg = 0.4 * w_perp * flightDuration;
  }

  const finalDist = Math.max(1.0, totalDist + windDistAdj);
  const finalCarryTarget = Math.max(1.0, finalDist - 16.0);
  const finalLaunchSpeed = Math.sqrt((finalCarryTarget / 0.77) * GRAVITY / Math.sin(2 * launchAngle));
  const vHoriz = finalLaunchSpeed * Math.cos(launchAngle);
  const vVert = finalLaunchSpeed * Math.sin(launchAngle);

  const vx = Math.sin(aimRad) * vHoriz;
  const vz = Math.cos(aimRad) * vHoriz;
  const vy = vVert;

  const totalCurveDeg = (isShank ? missCurveDeg : curveBeforeWind) + windCurveDeg;
  const curveRad = THREE.MathUtils.degToRad(totalCurveDeg);
  const lateralDist = finalDist * Math.sin(curveRad);
  const latAccMag = (2 * lateralDist) / (flightDuration * flightDuration);
  const latDir = new THREE.Vector3(Math.cos(aimRad), 0, -Math.sin(aimRad));
  const latAcc = latDir.clone().multiplyScalar(latAccMag);

  return {
    vel: new THREE.Vector3(vx, vy, vz),
    latAcc: latAcc,
    spinLift: club.spinRating * 4.2,
    isBunker: false,
    minimalRoll: false,
    flightDuration: flightDuration
  };
}

function simulateShot(pos, shot, club, hole, isRain = false) {
  const dt = 1 / 60;
  const substeps = 4;
  const subDt = dt / substeps;
  const curPos = pos.clone();
  const curVel = shot.vel.clone();
  let activeLatAcc = shot.latAcc ? shot.latAcc.clone() : null;

  for (let frame = 0; frame < 900; frame++) {
    for (let s = 0; s < substeps; s++) {
      const prevPos = curPos.clone();
      if (club.isPutter) {
        const grad = getGreenGradientAt(hole, curPos.x, curPos.z);
        let a_slope = 9.8 * (grad.grade / 100.0) * 0.4;
        if (isRain) {
          a_slope *= 0.7;
        }
        curVel.x += grad.downhill.x * a_slope * subDt;
        curVel.z += grad.downhill.z * a_slope * subDt;

        const frictionFactor = Math.pow(GROUND_ROLL_FRICTION_PUTTER, subDt);
        curVel.x *= frictionFactor;
        curVel.z *= frictionFactor;

        curPos.x += curVel.x * subDt;
        curPos.z += curVel.z * subDt;
        curPos.y = getTerrainHeight(curPos.x, curPos.z) + 0.1;

        const hit = checkTreeCollisions(prevPos, curPos);
        if (hit.hit) {
          curPos.x = hit.x;
          curPos.z = hit.z;
          curPos.y = getTerrainHeight(hit.x, hit.z) + 0.1;
          curVel.set(0, 0, 0);
          return { pos: curPos, holedOut: false, inWater: false };
        }

        const dx = curPos.x - hole.cup.x;
        const dz = curPos.z - hole.cup.z;
        const horizDist = Math.hypot(dx, dz);
        const horizSpeed = Math.hypot(curVel.x, curVel.z);
        if (horizDist <= CUP_RADIUS && horizSpeed <= CUP_MAX_SPEED) {
          curPos.set(hole.cup.x, getTerrainHeight(hole.cup.x, hole.cup.z) - 0.22, hole.cup.z);
          return { pos: curPos, holedOut: true, inWater: false };
        }

        if (curVel.length() < 0.08) {
          return { pos: curPos, holedOut: false, inWater: false };
        }
      } else {
        const lift = (curVel.y > 0) ? shot.spinLift * (curVel.y / 20) : 0;
        curVel.y -= (GRAVITY - lift) * subDt;
        if (activeLatAcc) {
          curVel.addScaledVector(activeLatAcc, subDt);
        }
        curVel.x *= (1.0 - AIR_DRAG * subDt * 60);
        curVel.z *= (1.0 - AIR_DRAG * subDt * 60);

        const nextPos = curPos.clone().addScaledVector(curVel, subDt);
        const hit = checkTreeCollisions(curPos, nextPos);
        if (hit.hit) {
          curPos.x = hit.x;
          curPos.z = hit.z;
          curPos.y = getTerrainHeight(hit.x, hit.z) + 0.1;
          curVel.set(0, 0, 0);
          return { pos: curPos, holedOut: false, inWater: false };
        }

        curPos.copy(nextPos);
        const groundH = getTerrainHeight(curPos.x, curPos.z) + 0.1;
        if (curPos.y <= groundH) {
          activeLatAcc = null;
          curPos.y = groundH;

          if (isInsidePondForHole(hole, curPos.x, curPos.z)) {
            return { pos: curPos, holedOut: false, inWater: true };
          }

          if (isInsideBunkerForHole(hole, curPos.x, curPos.z)) {
            curVel.y = 0;
            curVel.multiplyScalar(0.15);
          } else {
            if (shot.minimalRoll) {
              curVel.y = 0;
              curVel.multiplyScalar(0.08);
            } else if (Math.abs(curVel.y) > 2.0) {
              curVel.y = -curVel.y * GROUND_BOUNCE_RESTITUTION;
              curVel.x *= 0.72;
              curVel.z *= 0.72;
            } else {
              curVel.y = 0;
              const rollFriction = (getLieZone(hole, curPos.x, curPos.z) === 'Rough')
                ? Math.pow(GROUND_ROLL_FRICTION_ROUGH, subDt)
                : Math.pow(GROUND_ROLL_FRICTION_FAIRWAY, subDt);
              curVel.x *= rollFriction;
              curVel.z *= rollFriction;
            }
          }

          const dx = curPos.x - hole.cup.x;
          const dz = curPos.z - hole.cup.z;
          const horizDist = Math.hypot(dx, dz);
          const horizSpeed = Math.hypot(curVel.x, curVel.z);
          if (horizDist <= CUP_RADIUS && horizSpeed <= CUP_MAX_SPEED) {
            curPos.set(hole.cup.x, getTerrainHeight(hole.cup.x, hole.cup.z) - 0.22, hole.cup.z);
            return { pos: curPos, holedOut: true, inWater: false };
          }

          if (curVel.length() < 0.15) {
            return { pos: curPos, holedOut: false, inWater: false };
          }
        }
      }
    }
  }
  return { pos: curPos, holedOut: false, inWater: false };
}

function testAISequence(roundNum, holeIdx, shots, windMod, isRain) {
  const hole = HOLES[holeIdx];
  let curPos = new THREE.Vector3(hole.tee.x, getTerrainHeight(hole.tee.x, hole.tee.z) + 0.1, hole.tee.z);
  let strokes = 0;
  let holedOut = false;

  for (let sIdx = 0; sIdx < shots.length; sIdx++) {
    strokes++;
    const s = shots[sIdx];
    const isOpening = (sIdx === 0);
    const lie = getLieZone(hole, curPos.x, curPos.z, isOpening);
    const baseAim = Math.atan2(hole.cup.x - curPos.x, hole.cup.z - curPos.z);
    const aimAngle = baseAim + THREE.MathUtils.degToRad(s.aimOffsetDeg || 0);

    const shot = calculateInitialVelocity(s.club, s.power, s.offset || 0, lie, aimAngle, s.shape || null, hole, windMod, isRain);
    const res = simulateShot(curPos, shot, CLUBS[s.club], hole, isRain);
    curPos = res.pos;
    if (res.holedOut) {
      holedOut = true;
      break;
    }
    if (res.inWater) {
      console.log('Water hit on shot ' + (sIdx + 1));
      break;
    }
  }

  const distToPin = Math.hypot(curPos.x - hole.cup.x, curPos.z - hole.cup.z);
  const diff = strokes - hole.par;
  return { holedOut, strokes, par: hole.par, diff, distToPin, finalPos: curPos };
}

module.exports = {
  HOLES,
  CLUBS,
  calculateInitialVelocity,
  simulateShot,
  testAISequence,
  getLieZone,
  getTerrainHeight,
  CUP_RADIUS,
  CUP_MAX_SPEED
};
