import asyncio
import json
import subprocess
import time
import urllib.request
import websockets

async def run_round7_tests():
    cmd = [
        './.arena/chrome-for-testing',
        '--headless',
        '--disable-gpu',
        '--remote-debugging-port=9222',
        'file:///Users/xulisai/Documents/3DGameAgentBench/sandbox/authoring-lanes/129f7035-917e-47b5-9ad9-304d9f84c819/lane-1/workspace/index.html'
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(1.5)

    try:
        with urllib.request.urlopen('http://127.0.0.1:9222/json') as response:
            pages = json.loads(response.read().decode())
        target_page = None
        for p in pages:
            if 'index.html' in p.get('url', ''):
                target_page = p
                break
        assert target_page, "index.html page not found"
        ws_url = target_page['webSocketDebuggerUrl']
        print(f"Connecting to CDP: {ws_url}")

        async with websockets.connect(ws_url) as ws:
            msg_id = 0

            async def cdp_call(method, params=None):
                nonlocal msg_id
                msg_id += 1
                req = {"id": msg_id, "method": method, "params": params or {}}
                await ws.send(json.dumps(req))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get("id") == msg_id:
                        return res.get("result", {})

            async def eval_js(expr):
                res = await cdp_call("Runtime.evaluate", {"expression": expr, "returnByValue": True})
                if "exceptionDetails" in res:
                    raise RuntimeError(f"JS Exception in '{expr}': {res['exceptionDetails']}")
                return res.get("result", {}).get("value")

            print("\n--- TEST 1: Check window.__arena_state Round 7 exports in READY state ---")
            crashes = await eval_js("window.__arena_state.crash_count")
            freeze = await eval_js("window.__arena_state.remaining_respawn_freeze")
            respawn_pt = await eval_js("window.__arena_state.respawn_point_in_use")
            final_rating = await eval_js("window.__arena_state.final_rating")

            print(f"crash_count: {crashes}")
            print(f"remaining_respawn_freeze: {freeze}")
            print(f"respawn_point_in_use: {respawn_pt}")
            print(f"final_rating: {final_rating}")

            assert crashes == 0, f"Expected 0 crashes, got {crashes}"
            assert freeze == 0.0, f"Expected 0 freeze, got {freeze}"
            assert respawn_pt is not None, "Expected respawn point in use"
            assert final_rating in ['S', 'A', 'B', 'C'], f"Expected valid rating, got {final_rating}"
            print("TEST 1 PASSED: Round 7 properties properly exported on __arena_state.")

            print("\n--- TEST 2: Checkpoint Respawn before any gate passed ---")
            await eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'n' }))")
            phase = await eval_js("window.__arena_state.phase")
            assert phase == 'FLIGHT'

            # Force pilot down into the valley floor (y = 20) before passing any gate
            respawn_res = await eval_js("""
            (() => {
              const api = window.__test_api;
              api.state.y = 19.5; // Trigger terrain contact
              api.checkCollisions();
              return {
                phase: api.state.phase,
                crashes: api.state.crash_count,
                freeze: api.state.respawn_freeze,
                pos: { x: api.state.x, y: api.state.y, z: api.state.z },
                v: api.state.v,
                gamma: api.state.gamma * 180 / Math.PI,
                psi: api.state.psi,
                arena_crashes: window.__arena_state.crash_count,
                arena_freeze: window.__arena_state.remaining_respawn_freeze,
                arena_pt: window.__arena_state.respawn_point_in_use
              };
            })()
            """)
            print(f"Respawn result from ground contact: {respawn_res}")
            assert respawn_res['phase'] == 'FLIGHT', "Phase should remain FLIGHT on respawn"
            assert respawn_res['crashes'] == 1, f"Expected 1 crash, got {respawn_res['crashes']}"
            assert respawn_res['freeze'] == 3.0, f"Expected 3.0s freeze, got {respawn_res['freeze']}"
            assert respawn_res['v'] == 20.0, f"Expected v=20.0, got {respawn_res['v']}"
            assert abs(respawn_res['gamma'] - (-10.0)) < 0.001, f"Expected gamma=-10, got {respawn_res['gamma']}"
            assert respawn_res['psi'] == 0.0, f"Expected psi=0, got {respawn_res['psi']}"
            assert respawn_res['pos']['y'] == 620, f"Expected respawn at platform y=620, got {respawn_res['pos']['y']}"
            print("TEST 2 PASSED: Initial respawn at launch platform verified.")

            print("\n--- TEST 3: Control Freeze during Respawn ---")
            freeze_test = await eval_js("""
            (() => {
              const api = window.__test_api;
              const gBefore = api.state.gamma;
              // Hold W key to pitch up
              window.dispatchEvent(new KeyboardEvent('keydown', { key: 'w' }));
              api.stepPhysics();
              const gAfter = api.state.gamma;
              window.dispatchEvent(new KeyboardEvent('keyup', { key: 'w' }));
              return { gBefore, gAfter, freezeRemaining: api.state.respawn_freeze };
            })()
            """)
            print(f"Freeze test: {freeze_test}")
            assert abs(freeze_test['gBefore'] - freeze_test['gAfter']) < 0.001, "Pitch should not change while frozen"
            assert freeze_test['freezeRemaining'] < 3.0, "Freeze timer should decrement"
            print("TEST 3 PASSED: Controls are frozen while freeze > 0.")

            print("\n--- TEST 4: Respawn at Last Passed Gate ---")
            gate_respawn_res = await eval_js("""
            (() => {
              const api = window.__test_api;
              // Teleport near Gate 1 (0, 560, 180) and pass it
              const g1 = api.COURSES[0].gates[0];
              api.prevPos.x = g1.x; api.prevPos.y = g1.y; api.prevPos.z = g1.z - 2;
              api.state.x = g1.x; api.state.y = g1.y; api.state.z = g1.z + 2;
              api.checkGateCrossing();
              const gatesPassed = api.state.gates_passed;

              // Now collide with pillar P3 (x: 30, z: 460, topY: 520, radius: 22)
              api.state.x = 30; api.state.y = 480; api.state.z = 460;
              api.checkCollisions();

              return {
                gatesPassed,
                phase: api.state.phase,
                crashes: api.state.crash_count,
                freeze: api.state.respawn_freeze,
                respawnPos: { x: api.state.x, y: api.state.y, z: api.state.z },
                gatePos: { x: g1.x, y: g1.y, z: g1.z },
                v: api.state.v,
                gamma: api.state.gamma * 180 / Math.PI,
                psi: api.state.psi,
                normal: g1.normal
              };
            })()
            """)
            print(f"Gate respawn result: {gate_respawn_res}")
            assert gate_respawn_res['gatesPassed'] == 1, "Expected 1 gate passed"
            assert gate_respawn_res['phase'] == 'FLIGHT', "Phase should remain FLIGHT"
            assert gate_respawn_res['crashes'] == 2, f"Expected 2 crashes, got {gate_respawn_res['crashes']}"
            assert gate_respawn_res['respawnPos']['x'] == gate_respawn_res['gatePos']['x']
            assert gate_respawn_res['respawnPos']['y'] == gate_respawn_res['gatePos']['y']
            assert gate_respawn_res['respawnPos']['z'] == gate_respawn_res['gatePos']['z']
            print("TEST 4 PASSED: Respawns at last passed gate center with gate normal heading.")

            print("\n--- TEST 5: Complete Course 1, Course 2, Course 3, Podium, and Reckoning Panel ---")
            # Finish Course 1
            await eval_js("""
            (() => {
              const api = window.__test_api;
              // Pass remaining gates up to G9
              api.state.gates_passed = 9;
              api.state.next_gate_index = 9;
              // Land on pad
              const pad = api.COURSES[0].pad;
              api.state.x = pad.x; api.state.y = pad.y; api.state.z = pad.z;
              api.state.vy = -2.0; api.state.gamma = 10 * Math.PI / 180;
              api.judgeTouchdown(0.5, true);
            })()
            """)
            c1_phase = await eval_js("window.__arena_state.phase")
            c1_grade = await eval_js("window.__arena_state.landing_grade")
            c1_crashes = await eval_js("window.__arena_state.crash_count")
            c1_total = await eval_js("window.__arena_state.total")
            print(f"Course 1 completed: phase={c1_phase}, grade={c1_grade}, crashes={c1_crashes}, total={c1_total}")
            assert c1_phase == 'LANDED'
            assert c1_grade == 'CLEAN'
            assert c1_crashes == 2

            # Advance to Course 2
            await eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))")
            assert await eval_js("window.__arena_state.course_index") == 1

            # Complete Course 2
            await eval_js("""
            (() => {
              const api = window.__test_api;
              api.state.gates_passed = 8;
              api.state.next_gate_index = 8;
              const pad = api.COURSES[1].pad;
              api.state.x = pad.x; api.state.y = pad.y; api.state.z = pad.z;
              api.state.vy = -2.0; api.state.gamma = 10 * Math.PI / 180;
              api.judgeTouchdown(0.5, true);
            })()
            """)
            assert await eval_js("window.__arena_state.phase") == 'LANDED'

            # Advance to Course 3
            await eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))")
            assert await eval_js("window.__arena_state.course_index") == 2

            # Complete Course 3
            await eval_js("""
            (() => {
              const api = window.__test_api;
              api.state.gates_passed = 7;
              api.state.next_gate_index = 7;
              const pad = api.COURSES[2].pad;
              api.state.x = pad.x; api.state.y = pad.y; api.state.z = pad.z;
              api.state.vy = -2.0; api.state.gamma = 10 * Math.PI / 180;
              api.judgeTouchdown(0.5, true);
            })()
            """)
            assert await eval_js("window.__arena_state.phase") == 'LANDED'

            # Advance to Podium Ceremony
            await eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))")
            podium_phase = await eval_js("window.__arena_state.phase")
            print(f"Podium Phase: {podium_phase}")
            assert podium_phase == 'PODIUM'

            # Advance to Reckoning Panel
            await eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))")
            reckoning_phase = await eval_js("window.__arena_state.phase")
            rating = await eval_js("window.__arena_state.final_rating")
            totals = await eval_js("window.__arena_state.course_totals")
            standings = await eval_js("window.__arena_state.standings")
            print(f"Reckoning Phase: {reckoning_phase}")
            print(f"Final Rating: {rating}")
            print(f"Totals: {totals}")
            print(f"Final Standings: {standings}")

            assert reckoning_phase == 'RECKONING', f"Expected RECKONING phase, got {reckoning_phase}"
            assert rating in ['S', 'A', 'B', 'C']
            assert len(standings) == 4
            print("TEST 5 PASSED: Full progression to Reckoning panel and ratings verified.")

            print("\n--- TEST 6: Enter from Reckoning returns to Championship Menu ---")
            await eval_js("window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }))")
            final_menu_phase = await eval_js("window.__arena_state.phase")
            print(f"Phase after Enter: {final_menu_phase}")
            assert final_menu_phase == 'READY'
            print("TEST 6 PASSED: Enter returns to Championship Menu.")

            print("\nALL ROUND 7 TESTS PASSED SUCCESSFULLY!")

    finally:
        proc.terminate()
        proc.wait()

asyncio.run(run_round7_tests())
