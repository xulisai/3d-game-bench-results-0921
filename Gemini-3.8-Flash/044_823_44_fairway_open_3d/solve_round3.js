const sim = require('./sim_engine.js');
const { testSequence } = require('./solve_all_ai.js');
const THREE = require('./assets/_shared/three/build/three.min.js');

// Round 3 conditions: windMod = 15, isRain = false
// Target scores:
// Hole 1: Par 4 -> +1 (5 strokes)
// Hole 2: Par 3 -> +1 (4 strokes)
// Hole 3: Par 5 -> Par (5 strokes)
// Hole 4: Par 4 -> +1 (5 strokes)

const windMod3 = 15;
const isRain3 = false;

console.log('--- SOLVING ROUND 3 ---');

// H1: Par 4 -> 5 strokes (+1)
const r3_h1 = [
  { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: '7-Iron', power: 75, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Pitching Wedge', power: 70, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R3 H1:', testSequence(0, r3_h1, windMod3, isRain3));

// H2: Par 3 -> 4 strokes (+1)
const r3_h2 = [
  { club: '7-Iron', power: 85, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Sand Wedge', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R3 H2:', testSequence(1, r3_h2, windMod3, isRain3));

// H3: Par 5 -> 5 strokes (Par)
// Wind on Hole 3 is East (crosswind +X). Base 15 mph + 15 = 30 mph crosswind!
// High crosswind drifts right heavily, so aim left (-aimOffsetDeg)
const r3_h3 = [
  { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -35 },
  { club: '3-Wood', power: 90, offset: 0, shape: null, aimOffsetDeg: -35 },
  { club: 'Pitching Wedge', power: 75, offset: 0, shape: null, aimOffsetDeg: -30 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R3 H3:', testSequence(2, r3_h3, windMod3, isRain3));

// H4: Par 4 -> 5 strokes (+1)
// Wind on Hole 4 is North (tailwind). Base 18 mph + 15 = 33 mph tailwind!
const r3_h4 = [
  { club: 'Driver', power: 90, offset: 0, shape: 'draw', aimOffsetDeg: 30 },
  { club: '7-Iron', power: 70, offset: 0, shape: null, aimOffsetDeg: -5 },
  { club: 'Sand Wedge', power: 65, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R3 H4:', testSequence(3, r3_h4, windMod3, isRain3));

// Playoff Hole 5 (windMod 0, isRain false)
// Target: Par (3 strokes)
const r_h5 = [
  { club: '7-Iron', power: 85, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('Playoff H5:', testSequence(4, r_h5, 0, false));
