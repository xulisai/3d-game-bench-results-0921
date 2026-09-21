const sim = require('./sim_engine.js');
const { testSequence, findApproach } = require('./solve_all_ai.js');
const THREE = require('./assets/_shared/three/build/three.min.js');

// Round 2 conditions: windMod = 8, isRain = true
// Targets:
// Hole 1: Par 4 -> +1 (5 strokes)
// Hole 2: Par 3 -> Par (3 strokes)
// Hole 3: Par 5 -> +1 (6 strokes)
// Hole 4: Par 4 -> Par (4 strokes)

const windMod2 = 8;
const isRain2 = true;

console.log('--- SOLVING ROUND 2 ---');

// H1: Par 4 -> 5 strokes (+1)
// 1. Driver tee shot
// 2. 7-Iron
// 3. Wedge
// 4. Putter
// 5. Putter
const r2_h1 = [
  { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: '7-Iron', power: 75, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Pitching Wedge', power: 70, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R2 H1:', testSequence(0, r2_h1, windMod2, isRain2));

// H2: Par 3 -> 3 strokes (Par)
// 1. 7-Iron
// 2. Putter
// 3. Putter
const r2_h2 = [
  { club: '7-Iron', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R2 H2:', testSequence(1, r2_h2, windMod2, isRain2));

// H3: Par 5 -> 6 strokes (+1)
// 1. Driver
// 2. 3-Wood
// 3. 7-Iron
// 4. Pitching Wedge
// 5. Putter
// 6. Putter
const r2_h3 = [
  { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -25 },
  { club: '3-Wood', power: 90, offset: 0, shape: null, aimOffsetDeg: -25 },
  { club: '7-Iron', power: 85, offset: 0, shape: null, aimOffsetDeg: -20 },
  { club: 'Pitching Wedge', power: 70, offset: 0, shape: null, aimOffsetDeg: -15 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R2 H3:', testSequence(2, r2_h3, windMod2, isRain2));

// H4: Par 4 -> 4 strokes (Par)
// 1. Driver
// 2. Pitching Wedge
// 3. Putter
// 4. Putter
const r2_h4 = [
  { club: 'Driver', power: 95, offset: 0, shape: 'draw', aimOffsetDeg: 30 },
  { club: 'Pitching Wedge', power: 75, offset: 0, shape: null, aimOffsetDeg: -5 },
  { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
  { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
];
console.log('R2 H4:', testSequence(3, r2_h4, windMod2, isRain2));
