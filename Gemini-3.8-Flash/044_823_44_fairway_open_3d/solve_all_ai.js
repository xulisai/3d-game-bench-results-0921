const sim = require('./sim_engine.js');
const { solvePutt } = require('./solve_putt.js');
const THREE = require('./assets/_shared/three/build/three.min.js');

// Function to simulate a shot list and return final status
function testSequence(holeIdx, shots, windMod, isRain) {
  const hole = sim.HOLES[holeIdx];
  let curPos = new THREE.Vector3(hole.tee.x, sim.getTerrainHeight(hole.tee.x, hole.tee.z) + 0.1, hole.tee.z);
  let strokes = 0;
  let holedOut = false;

  for (let sIdx = 0; sIdx < shots.length; sIdx++) {
    strokes++;
    const s = shots[sIdx];
    const isOpening = (sIdx === 0);
    const lie = sim.getLieZone(hole, curPos.x, curPos.z, isOpening);
    const baseAim = Math.atan2(hole.cup.x - curPos.x, hole.cup.z - curPos.z);
    const aimAngle = baseAim + THREE.MathUtils.degToRad(s.aimOffsetDeg || 0);

    const shot = sim.calculateInitialVelocity(s.club, s.power, s.offset || 0, lie, aimAngle, s.shape || null, hole, windMod, isRain);
    const res = sim.simulateShot(curPos, shot, sim.CLUBS[s.club], hole, isRain);
    curPos = res.pos;
    if (res.holedOut) {
      holedOut = true;
      break;
    }
    if (res.inWater) {
      return { holedOut: false, inWater: true, strokes, distToPin: 999, pos: curPos };
    }
  }

  const distToPin = Math.hypot(curPos.x - hole.cup.x, curPos.z - hole.cup.z);
  const diff = strokes - hole.par;
  return { holedOut, strokes, par: hole.par, diff, distToPin, pos: curPos };
}

// Search for approach shots
function findApproach(curPos, hole, targetDist, allowedClubs, windMod, isRain) {
  const baseAim = Math.atan2(hole.cup.x - curPos.x, hole.cup.z - curPos.z);
  let best = null;
  let minD = 999;

  for (const clubName of allowedClubs) {
    for (let p = 40; p <= 100; p += 2) {
      for (let aimDeg = -10; aimDeg <= 10; aimDeg += 2) {
        const aimRad = baseAim + THREE.MathUtils.degToRad(aimDeg);
        const lie = sim.getLieZone(hole, curPos.x, curPos.z, false);
        const shot = sim.calculateInitialVelocity(clubName, p, 0, lie, aimRad, null, hole, windMod, isRain);
        const res = sim.simulateShot(curPos, shot, sim.CLUBS[clubName], hole, isRain);
        if (res.inWater) continue;
        const d = Math.hypot(res.pos.x - hole.cup.x, res.pos.z - hole.cup.z);
        if (d < minD) {
          minD = d;
          best = { club: clubName, power: p, offset: 0, shape: null, aimOffsetDeg: aimDeg, dist: d, pos: res.pos };
        }
      }
    }
  }
  return best;
}

// Verify Round 1
const R1_SHOTS = [
  // H1: Par 4 -> 4 strokes (Par)
  [
    { club: 'Driver', power: 96, offset: 0, shape: null, aimOffsetDeg: 0 },
    { club: '7-Iron', power: 74, offset: 0, shape: null, aimOffsetDeg: 0 },
    { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 20 },
    { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: -5 }
  ],
  // H2: Par 3 -> 4 strokes (+1)
  [
    { club: '7-Iron', power: 80, offset: 0, shape: null, aimOffsetDeg: 0 },
    { club: 'Sand Wedge', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
    { club: 'Putter', power: 28, offset: 0, shape: null, aimOffsetDeg: 0 },
    { club: 'Putter', power: 18, offset: 0, shape: null, aimOffsetDeg: 0 }
  ],
  // H3: Par 5 -> 5 strokes (Par)
  [
    { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -23 },
    { club: '7-Iron', power: 95, offset: 0, shape: null, aimOffsetDeg: -23 },
    { club: 'Pitching Wedge', power: 80, offset: 0, shape: null, aimOffsetDeg: -20 },
    { club: 'Putter', power: 29, offset: 0, shape: null, aimOffsetDeg: -3 },
    { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: -9 }
  ],
  // H4: Par 4 -> 3 strokes (-1)
  [
    { club: 'Driver', power: 95, offset: 0, shape: 'draw', aimOffsetDeg: 29.28 },
    { club: 'Pitching Wedge', power: 72, offset: 0, shape: null, aimOffsetDeg: -5 },
    { club: 'Putter', power: 16, offset: 0, shape: null, aimOffsetDeg: 0 }
  ]
];

console.log('--- ROUND 1 ---');
R1_SHOTS.forEach((shots, idx) => {
  const res = testSequence(idx, shots, 0, false);
  console.log(`Hole ${idx+1}: strokes=${res.strokes}, par=${res.par}, diff=${res.diff}`);
});

module.exports = { testSequence, findApproach, R1_SHOTS };
