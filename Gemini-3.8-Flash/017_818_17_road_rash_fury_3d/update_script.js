const fs = require('fs');

let src = fs.readFileSync('index.html', 'utf8');

console.log('Original src lines:', src.split('\n').length);
