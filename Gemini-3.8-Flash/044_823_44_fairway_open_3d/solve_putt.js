const sim = require('./sim_engine.js');
const THREE = require('./assets/_shared/three/build/three.min.js');

// Given a current ball position on green, find a putt (power & aimOffsetDeg) that drops into the cup!
function solvePutt(pos, hole, windMod, isRain) {
  const baseAim = Math.atan2(hole.cup.x - pos.x, hole.cup.z - pos.z);
  const dist = Math.hypot(hole.cup.x - pos.x, hole.cup.z - pos.z);
  
  // Power typically between 5 and 100
  // aimOffsetDeg typically -30 to +30
  let best = null;
  let minD = 999;

  for (let aimDeg = -25; aimDeg <= 25; aimDeg += 0.5) {
    for (let p = 5; p <= 100; p += 1) {
      const aimRad = baseAim + THREE.MathUtils.degToRad(aimDeg);
      const shot = sim.calculateInitialVelocity('Putter', p, 0, 'Green', aimRad, null, hole, windMod, isRain);
      const res = sim.simulateShot(pos, shot, sim.CLUBS['Putter'], hole, isRain);
      if (res.holedOut) {
        return { club: 'Putter', power: p, offset: 0, shape: null, aimOffsetDeg: aimDeg };
      }
      const d = Math.hypot(res.pos.x - hole.cup.x, res.pos.z - hole.cup.z);
      if (d < minD) {
        minD = d;
        best = { club: 'Putter', power: p, offset: 0, shape: null, aimOffsetDeg: aimDeg, dist: d };
      }
    }
  }

  // Refine around best
  if (best) {
    for (let aimDeg = best.aimOffsetDeg - 1.0; aimDeg <= best.aimOffsetDeg + 1.0; aimDeg += 0.1) {
      for (let p = Math.max(5, best.power - 2); p <= Math.min(100, best.power + 2); p += 0.2) {
        const aimRad = baseAim + THREE.MathUtils.degToRad(aimDeg);
        const shot = sim.calculateInitialVelocity('Putter', p, 0, 'Green', aimRad, null, hole, windMod, isRain);
        const res = sim.simulateShot(pos, shot, sim.CLUBS['Putter'], hole, isRain);
        if (res.holedOut) {
          return { club: 'Putter', power: parseFloat(p.toFixed(1)), offset: 0, shape: null, aimOffsetDeg: parseFloat(aimDeg.toFixed(1)) };
        }
      }
    }
  }
  return null;
}

module.exports = { solvePutt };
