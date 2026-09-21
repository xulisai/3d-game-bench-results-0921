const fs = require('fs');
let code = fs.readFileSync('test_speed2.js', 'utf8');

// Add console.log inside loop when stall triggers
code = code.replace(
  'if (kestrel.v < stallEnterV) kestrel.stall = true;',
  'if (kestrel.v < stallEnterV) { kestrel.stall = true; console.log("Stalled at t=", kestrel.run_clock.toFixed(1), "v=", kestrel.v.toFixed(1)); }'
);

fs.writeFileSync('temp_stall.js', code);
require('./temp_stall.js');
