import json

data = json.load(open('medley_chart_export.json'))
chords = data['RAW_CHORDS']
notes = data['RAW_CHART_TIMINGS']

# Group by piece
pieces = {
    "Aurora Prelude": {'start': 0.0, 'end': 40.0, 'bpm': 110, 'exp_taps': 48, 'exp_holds': 4, 'exp_chords': 4, 'exp_bass': 6, 'exp_judg': 64},
    "Comet Waltz": {'start': 44.0, 'end': 89.0, 'bpm': 140, 'exp_taps': 50, 'exp_holds': 6, 'exp_chords': 6, 'exp_bass': 8, 'exp_judg': 74},
    "Midnight Toccata": {'start': 93.0, 'end': 128.0, 'bpm': 170, 'exp_taps': 40, 'exp_holds': 2, 'exp_chords': 8, 'exp_bass': 6, 'exp_judg': 60}
}

for name, cfg in pieces.items():
    p_notes = [n for n in notes if n.get('piece') == name or (cfg['start'] <= n['t'] < cfg['end'])]
    p_chords = [c for c in chords if cfg['start'] <= c['t'] < cfg['end']]
    
    taps = [n for n in p_notes if n['type'] == 'tap' and 'chordId' not in n]
    chord_taps = [n for n in p_notes if n['type'] == 'tap' and 'chordId' in n]
    holds = [n for n in p_notes if n['type'] == 'hold']
    bass = [n for n in p_notes if n['l'] == 3]
    judgments = len(taps) + len(chord_taps) + len(holds)*2
    
    print(f"=== {name} ===")
    print(f"Taps: {len(taps)} (Exp {cfg['exp_taps'] - len(bass)} non-bass + {len(bass)} bass = {len(taps) + len(chord_taps)} total tap items)")
    print(f"Chord taps: {len(chord_taps)} across {len(p_chords)} chords (Exp {cfg['exp_chords']*2} across {cfg['exp_chords']})")
    print(f"Holds: {len(holds)} (Exp {cfg['exp_holds']})")
    print(f"Bass events: {len(bass)} (Exp {cfg['exp_bass']})")
    print(f"Judgments: {judgments} (Exp {cfg['exp_judg']})")
    
    assert len(taps) + len(bass) - len([t for t in taps if t['l'] == 3]) == cfg['exp_taps'], "Tap count mismatch"
    assert len(p_chords) == cfg['exp_chords'], "Chord count mismatch"
    assert len(holds) == cfg['exp_holds'], "Hold count mismatch"
    assert len(bass) == cfg['exp_bass'], "Bass count mismatch"
    assert judgments == cfg['exp_judg'], "Judgment count mismatch"
    
    # Quantization
    step = 30.0 / cfg['bpm']
    for n in p_notes:
        grid_k = round((n['t'] - cfg['start']) / step)
        expected_t = round(cfg['start'] + grid_k * step, 5)
        assert abs(n['t'] - expected_t) < 0.001, f"Note at {n['t']} not quantized to grid step {step}"
        if n['type'] == 'hold':
            assert 1.0 <= n['dur'] <= 2.5, f"Hold dur {n['dur']} outside 1.0-2.5s"

# Interlude checks
int1_notes = [n for n in notes if 40.0 <= n['t'] < 44.0 or (n['type'] == 'hold' and n['t'] < 40.0 and n['endTime'] > 40.0)]
int2_notes = [n for n in notes if 89.0 <= n['t'] < 93.0 or (n['type'] == 'hold' and n['t'] < 89.0 and n['endTime'] > 89.0)]
assert len(int1_notes) == 0, f"Notes crossing Interlude 1: {int1_notes}"
assert len(int2_notes) == 0, f"Notes crossing Interlude 2: {int2_notes}"
print("Interludes strictly empty: PASSED.")

# Total judgments
tot_judg = sum(2 if n['type'] == 'hold' else 1 for n in notes)
print(f"TOTAL MEDLEY JUDGMENTS: {tot_judg} (Exp: 198)")
assert tot_judg == 198, "Total judgments must be 198"

# Check density: <= 2 chart events per second in every 1.0s window
# Chart events: distinct (t, chordId if chord else l)
events = []
for c in chords:
    events.append(c['t'])
for n in notes:
    if 'chordId' not in n:
        events.append(n['t'])
events.sort()
print(f"Total chart events: {len(events)}")
for i, t in enumerate(events):
    count = sum(1 for x in events if t - 0.0001 <= x <= t + 1.0001)
    assert count <= 2, f"Density violation at t={t}: {count} events in 1.0s window"
print("Density limit (<= 2 events/sec): PASSED.")

# Check lane spacing >= 0.5s
for l in range(4):
    l_notes = [n for n in notes if n['l'] == l]
    l_notes.sort(key=lambda x: x['t'])
    for i in range(len(l_notes) - 1):
        n1 = l_notes[i]
        n2 = l_notes[i+1]
        end1 = n1.get('endTime', n1['t'])
        gap = n2['t'] - end1
        assert gap >= 0.499, f"Lane {l} spacing violation between {n1['t']} and {n2['t']}, gap={gap}"
print("Lane spacing (>= 0.5s): PASSED.")

# Check bass spacing >= 2.0s
b_notes = [n for n in notes if n['l'] == 3]
b_notes.sort(key=lambda x: x['t'])
for i in range(len(b_notes) - 1):
    gap = b_notes[i+1]['t'] - b_notes[i].get('endTime', b_notes[i]['t'])
    assert gap >= 1.999, f"Bass spacing violation between {b_notes[i]['t']} and {b_notes[i+1]['t']}, gap={gap}"
print("Bass spacing (>= 2.0s): PASSED.")

print("\n*** ALL MEDLEY CHART CONSTRAINTS PERFECTLY VERIFIED! ***\n")
