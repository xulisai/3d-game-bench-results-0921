// Verification script for Round 7 full integration
const fs = require('fs');

console.log('Testing index.html syntax and structure...');
const html = fs.readFileSync('index.html', 'utf8');

// Check that required tokens exist
const requiredTokens = [
  'Open Championship',
  'Match Play',
  'Practice Round',
  'ROUND 2 — RAIN',
  'SUDDEN DEATH — HOLE 5',
  'CHAMPION',
  'mode',
  'tournamentRound',
  'cumulativeStrokes',
  'windModifier',
  'rainActive',
  'practiceHole',
  'Digit1',
  'Digit2',
  'Digit3',
  'Backspace'
];

let allPassed = true;
requiredTokens.forEach(tok => {
  if (!html.includes(tok)) {
    console.error('Missing token:', tok);
    allPassed = false;
  } else {
    console.log('Found token:', tok);
  }
});

if (allPassed) {
  console.log('Token check passed.');
} else {
  process.exit(1);
}
