const http = require('http');

http.get('http://127.0.0.1:9222/json', (res) => {
  let raw = '';
  res.on('data', chunk => raw += chunk);
  res.on('end', () => {
    const tabs = JSON.parse(raw);
    const tab = tabs.find(t => t.title.includes('Skyward Command')) || tabs[0];
    console.log('Using WebSocket:', tab.webSocketDebuggerUrl);

    // Connect via ws
    const WebSocket = require('/Users/xulisai/Documents/3DGameAgentBench/node_modules/ws');
    const ws = new WebSocket(tab.webSocketDebuggerUrl);

    let id = 1;
    function send(method, params = {}) {
      return new Promise(resolve => {
        const msgId = id++;
        const handler = (data) => {
          const resp = JSON.parse(data.toString());
          if (resp.id === msgId) {
            ws.off('message', handler);
            resolve(resp.result);
          }
        };
        ws.on('message', handler);
        ws.send(JSON.stringify({ id: msgId, method, params }));
      });
    }

    ws.on('open', async () => {
      console.log('Connected to Chrome CDP!');

      // Evaluate window.__arena_state
      const state1 = await send('Runtime.evaluate', {
        expression: 'JSON.stringify(window.__arena_state)',
        returnByValue: true
      });
      console.log('Initial State:', state1.result.value);

      // Press Enter to start mission
      await send('Runtime.evaluate', {
        expression: 'window.dispatchEvent(new KeyboardEvent("keydown", { code: "Enter", key: "Enter", bubbles: true }))'
      });

      // Wait 1.5 seconds in game
      await new Promise(r => setTimeout(r, 1500));

      const state2 = await send('Runtime.evaluate', {
        expression: 'JSON.stringify(window.__arena_state)',
        returnByValue: true
      });
      console.log('Running State after 1.5s:', state2.result.value);

      // Check base object
      const baseCheck = await send('Runtime.evaluate', {
        expression: 'JSON.stringify({ base: window.__arena_state.base, wave: window.__arena_state.wave })',
        returnByValue: true
      });
      console.log('Base & Wave check:', baseCheck.result.value);

      ws.close();
      process.exit(0);
    });
  });
}).on('error', err => {
  console.error('Error connecting to Chrome:', err);
  process.exit(1);
});
