const sim = require('./sim_engine.js');
const THREE = require('./assets/_shared/three/build/three.min.js');

// Hole 5 configuration
sim.HOLES[4].greenRadius = 22.0;
sim.HOLES[4].islandLandRadius = 28.0;

const AI_TOURNAMENT_SHOTS = {
  1: [
    // Hole 1: Par 4 -> Par (4 strokes)
    [
      { club: 'Driver', power: 96, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: '7-Iron', power: 74, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 20 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: -5 }
    ],
    // Hole 2: Par 3 -> +1 (4 strokes)
    [
      { club: '7-Iron', power: 80, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Sand Wedge', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 28, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 18, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 3: Par 5 -> Par (5 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -23 },
      { club: '7-Iron', power: 95, offset: 0, shape: null, aimOffsetDeg: -23 },
      { club: 'Pitching Wedge', power: 80, offset: 0, shape: null, aimOffsetDeg: -20 },
      { club: 'Putter', power: 29, offset: 0, shape: null, aimOffsetDeg: -3 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: -9 }
    ],
    // Hole 4: Par 4 -> -1 (3 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: 'draw', aimOffsetDeg: 29.28 },
      { club: 'Pitching Wedge', power: 72, offset: 0, shape: null, aimOffsetDeg: -5 },
      { club: 'Putter', power: 16, offset: 0, shape: null, aimOffsetDeg: 0 }
    ]
  ],
  2: [
    // Hole 1: Par 4 -> +1 (5 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: '7-Iron', power: 75, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Pitching Wedge', power: 70, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 2: Par 3 -> Par (3 strokes)
    [
      { club: '7-Iron', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 3: Par 5 -> +1 (6 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -25 },
      { club: '3-Wood', power: 90, offset: 0, shape: null, aimOffsetDeg: -25 },
      { club: '7-Iron', power: 85, offset: 0, shape: null, aimOffsetDeg: -20 },
      { club: 'Pitching Wedge', power: 70, offset: 0, shape: null, aimOffsetDeg: -15 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 4: Par 4 -> Par (4 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: 'draw', aimOffsetDeg: 30 },
      { club: 'Pitching Wedge', power: 75, offset: 0, shape: null, aimOffsetDeg: -5 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ]
  ],
  3: [
    // Hole 1: Par 4 -> +1 (5 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: '7-Iron', power: 75, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Pitching Wedge', power: 70, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 2: Par 3 -> +1 (4 strokes)
    [
      { club: '7-Iron', power: 85, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Sand Wedge', power: 90, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 3: Par 5 -> Par (5 strokes)
    [
      { club: 'Driver', power: 95, offset: 0, shape: null, aimOffsetDeg: -35 },
      { club: '3-Wood', power: 90, offset: 0, shape: null, aimOffsetDeg: -35 },
      { club: 'Pitching Wedge', power: 75, offset: 0, shape: null, aimOffsetDeg: -30 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ],
    // Hole 4: Par 4 -> +1 (5 strokes)
    [
      { club: 'Driver', power: 90, offset: 0, shape: 'draw', aimOffsetDeg: 30 },
      { club: '7-Iron', power: 70, offset: 0, shape: null, aimOffsetDeg: -5 },
      { club: 'Sand Wedge', power: 65, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 25, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 15, offset: 0, shape: null, aimOffsetDeg: 0 }
    ]
  ],
  playoff: [
    // Hole 5: Par 3 -> Par (3 strokes)
    [
      { club: '7-Iron', power: 88.8, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 70, offset: 0, shape: null, aimOffsetDeg: 0 },
      { club: 'Putter', power: 40, offset: 0, shape: null, aimOffsetDeg: 0 }
    ]
  ]
};

console.log('=== VERIFYING ALL ROUNDS AND TARGET RELATIVE-TO-PAR SCORES ===');

// Round 1
console.log('--- ROUND 1 (windMod=0, rain=false) Expected: par, +1, par, -1 ---');
AI_TOURNAMENT_SHOTS[1].forEach((shots, idx) => {
  const res = sim.testAISequence(1, idx, shots, 0, false);
  console.log(`Hole ${idx+1}: strokes=${res.strokes}, par=${res.par}, diff=${res.diff}`);
});

// Round 2
console.log('--- ROUND 2 (windMod=8, rain=true) Expected: +1, par, +1, par ---');
AI_TOURNAMENT_SHOTS[2].forEach((shots, idx) => {
  const res = sim.testAISequence(2, idx, shots, 8, true);
  console.log(`Hole ${idx+1}: strokes=${res.strokes}, par=${res.par}, diff=${res.diff}`);
});

// Round 3
console.log('--- ROUND 3 (windMod=15, rain=false) Expected: +1, +1, par, +1 ---');
AI_TOURNAMENT_SHOTS[3].forEach((shots, idx) => {
  const res = sim.testAISequence(3, idx, shots, 15, false);
  console.log(`Hole ${idx+1}: strokes=${res.strokes}, par=${res.par}, diff=${res.diff}`);
});

// Playoff Hole 5
console.log('--- PLAYOFF HOLE 5 (windMod=0, rain=false) Expected: par ---');
const res5 = sim.testAISequence('playoff', 4, AI_TOURNAMENT_SHOTS.playoff[0], 0, false);
console.log(`Hole 5: strokes=${res5.strokes}, par=${res5.par}, diff=${res5.diff}`);

module.exports = { AI_TOURNAMENT_SHOTS };
