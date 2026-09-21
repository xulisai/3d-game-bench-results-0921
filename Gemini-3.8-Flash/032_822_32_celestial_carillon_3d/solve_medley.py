import json, math

def round_time(t):
    return round(t, 5)

def solve_piece(piece_name, start_t, end_t, bpm, num_taps, num_holds, num_chords, num_bass, hold_configs, chord_configs, bass_k):
    step = 30.0 / bpm
    total_steps = int(math.floor((end_t - start_t) / step))
    
    def grid_t(k):
        return round_time(start_t + k * step)
    
    # 1. Chords
    chords = []
    chord_notes = []
    for c in chord_configs:
        t = grid_t(c['k'])
        chords.append({'id': c['id'], 't': t, 'l1': c['l1'], 'l2': c['l2']})
        chord_notes.append({'type': 'tap', 't': t, 'l': c['l1'], 'chordId': c['id'], 'partnerLane': c['l2'], 'piece': piece_name})
        chord_notes.append({'type': 'tap', 't': t, 'l': c['l2'], 'chordId': c['id'], 'partnerLane': c['l1'], 'piece': piece_name})
        
    # 2. Holds
    holds = []
    for h in hold_configs:
        t = grid_t(h['k'])
        dur = round_time(h['dur_steps'] * step)
        endTime = round_time(t + dur)
        holds.append({'type': 'hold', 't': t, 'l': h['l'], 'dur': dur, 'endTime': endTime, 'piece': piece_name})
        
    # 3. Bass taps
    bass_taps = []
    for k in bass_k:
        t = grid_t(k)
        bass_taps.append({'type': 'tap', 't': t, 'l': 3, 'piece': piece_name})
        
    assert len(bass_taps) == num_bass, f"Expected {num_bass} bass taps, got {len(bass_taps)}"
    
    # Target regular taps in lanes 0, 1, 2
    needed_reg_taps = num_taps - num_bass
    
    # Occupied intervals per lane for fixed events:
    lane_occupied = {0: [], 1: [], 2: [], 3: []}
    
    for cn in chord_notes:
        lane_occupied[cn['l']].append((cn['t'] - 0.0001, cn['t'] + 0.0001))
    for h in holds:
        lane_occupied[h['l']].append((h['t'] - 0.0001, h['endTime'] + 0.0001))
    for b in bass_taps:
        lane_occupied[3].append((b['t'] - 0.0001, b['t'] + 0.0001))
        
    # Collect fixed events for density checking:
    # A chord is 1 chart event!
    fixed_event_times = [c['t'] for c in chords] + [h['t'] for h in holds] + [b['t'] for b in bass_taps]
    
    # Candidate slots in lanes 0, 1, 2
    candidates = []
    for k in range(2, total_steps - 2):
        t = grid_t(k)
        # Avoid notes within 0.5s of start_t or end_t to give clean boundary/interlude
        if t < start_t + 0.8 or t > end_t - 0.8:
            continue
        for l in (0, 1, 2):
            # Check overlap with chords/holds in same lane (min gap 0.5s)
            can_place = True
            for occ_s, occ_e in lane_occupied[l]:
                # Gap must be >= 0.5s
                if not (t <= occ_s - 0.499 or t >= occ_e + 0.499):
                    can_place = False
                    break
            if can_place:
                candidates.append((k, l, t))
                
    # Deterministic greedy selection of taps
    selected_taps = []
    curr_event_times = list(fixed_event_times)
    curr_lane_occupied = {l: list(lane_occupied[l]) for l in lane_occupied}
    
    # Sort candidates spread out across time
    # Spread selection using a deterministic stride
    step_stride = len(candidates) // needed_reg_taps
    
    # Let's try multiple offset candidates to find a clean valid set
    best_selection = None
    for offset in range(max(1, step_stride)):
        trial_taps = []
        trial_events = list(fixed_event_times)
        trial_occ = {l: list(lane_occupied[l]) for l in lane_occupied}
        
        # Try picking from candidates
        # Order candidates by round-robin across time
        pool = list(candidates[offset:]) + list(candidates[:offset])
        for k, l, t in pool:
            if len(trial_taps) == needed_reg_taps:
                break
            # Check lane spacing >= 0.5s
            conflict = False
            for occ_s, occ_e in trial_occ[l]:
                if not (t <= occ_s - 0.499 or t >= occ_e + 0.499):
                    conflict = True
                    break
            if conflict:
                continue
                
            # Check density <= 2 events per second in any 1.0s window
            # If we add t as an event:
            test_times = trial_events + [t]
            # Check all windows of length 1.0s around t
            density_ok = True
            # For any window [w_start, w_start + 1.0]
            # Check count of test_times in [w_start, w_start + 1.0]
            # It suffices to check windows starting at each time x in test_times
            for ref_t in test_times:
                count = sum(1 for x in test_times if ref_t - 0.0001 <= x <= ref_t + 1.0001)
                if count > 2:
                    density_ok = False
                    break
            if not density_ok:
                continue
                
            trial_taps.append({'type': 'tap', 't': t, 'l': l, 'piece': piece_name})
            trial_events.append(t)
            trial_occ[l].append((t - 0.0001, t + 0.0001))
            
        if len(trial_taps) == needed_reg_taps:
            best_selection = trial_taps
            break
            
    assert best_selection is not None, f"Failed to select {needed_reg_taps} taps for {piece_name}"
    print(f"[{piece_name}] Successfully selected {len(best_selection)} taps!")
    
    # Combine all notes for this piece
    all_notes = best_selection + bass_taps + holds + chord_notes
    all_notes.sort(key=lambda n: (n['t'], n['l']))
    return chords, all_notes

# --- SOLVE ALL 3 PIECES ---

# Piece 1: 0 to 40s (110 BPM, step = 3/11 s ≈ 0.2727s)
# 48 taps (6 bass), 4 holds, 4 chords
p1_hold_configs = [
    {'k': 10, 'dur_steps': 5, 'l': 0}, # ~2.73s, dur 1.36s
    {'k': 32, 'dur_steps': 5, 'l': 2}, # ~8.73s, dur 1.36s
    {'k': 64, 'dur_steps': 6, 'l': 1}, # ~17.45s, dur 1.64s
    {'k': 96, 'dur_steps': 5, 'l': 0}  # ~26.18s, dur 1.36s
]
p1_chord_configs = [
    {'id': 0, 'k': 20, 'l1': 0, 'l2': 1}, # ~5.45s
    {'k': 48, 'id': 1, 'l1': 1, 'l2': 2}, # ~13.09s
    {'k': 80, 'id': 2, 'l1': 0, 'l2': 2}, # ~21.82s
    {'k': 112, 'id': 3, 'l1': 0, 'l2': 1}  # ~30.55s
]
p1_bass_k = [6, 26, 56, 88, 120, 138] # min gap >= 20 steps (~5.4s) >= 2.0s
p1_chords, p1_notes = solve_piece("Aurora Prelude", 0.0, 40.0, 110, 48, 4, 4, 6, p1_hold_configs, p1_chord_configs, p1_bass_k)

# Interlude 1: 40.0s to 44.0s (4s)

# Piece 2: 44.0s to 89.0s (140 BPM, step = 3/14 s ≈ 0.2143s)
# 50 taps (8 bass), 6 holds, 6 chords
# 45s = ~210 steps
p2_hold_configs = [
    {'k': 12, 'dur_steps': 6, 'l': 1}, # ~46.57s, dur 1.29s
    {'k': 44, 'dur_steps': 7, 'l': 0}, # ~53.43s, dur 1.50s
    {'k': 78, 'dur_steps': 6, 'l': 2}, # ~60.71s, dur 1.29s
    {'k': 112, 'dur_steps': 7, 'l': 1},# ~68.00s, dur 1.50s
    {'k': 146, 'dur_steps': 6, 'l': 0},# ~75.29s, dur 1.29s
    {'k': 180, 'dur_steps': 7, 'l': 2} # ~82.57s, dur 1.50s
]
p2_chord_configs = [
    {'id': 4, 'k': 24, 'l1': 0, 'l2': 2}, # ~49.14s
    {'id': 5, 'k': 58, 'l1': 1, 'l2': 2}, # ~56.43s
    {'id': 6, 'k': 92, 'l1': 0, 'l2': 1}, # ~63.71s
    {'id': 7, 'k': 126, 'l1': 0, 'l2': 2},# ~71.00s
    {'id': 8, 'k': 160, 'l1': 1, 'l2': 2},# ~78.29s
    {'id': 9, 'k': 194, 'l1': 0, 'l2': 1} # ~85.57s
]
p2_bass_k = [6, 32, 66, 100, 134, 168, 190, 202] # min gap >= 12 steps (~2.57s) >= 2.0s
p2_chords, p2_notes = solve_piece("Comet Waltz", 44.0, 89.0, 140, 50, 6, 6, 8, p2_hold_configs, p2_chord_configs, p2_bass_k)

# Interlude 2: 89.0s to 93.0s (4s)

# Piece 3: 93.0s to 128.0s (170 BPM, step = 3/17 s ≈ 0.1765s)
# 40 taps (6 bass), 2 holds, 8 chords
# 35s = ~198 steps
p3_hold_configs = [
    {'k': 30, 'dur_steps': 8, 'l': 1}, # ~98.29s, dur 1.41s
    {'k': 110, 'dur_steps': 8, 'l': 0} # ~112.41s, dur 1.41s
]
p3_chord_configs = [
    {'id': 10, 'k': 16, 'l1': 0, 'l2': 1}, # ~95.82s
    {'id': 11, 'k': 44, 'l1': 1, 'l2': 2}, # ~100.76s
    {'id': 12, 'k': 68, 'l1': 0, 'l2': 2}, # ~105.00s
    {'id': 13, 'k': 92, 'l1': 0, 'l2': 1}, # ~109.24s
    {'id': 14, 'k': 124, 'l1': 1, 'l2': 2},# ~114.88s
    {'id': 15, 'k': 144, 'l1': 0, 'l2': 2},# ~118.41s
    {'id': 16, 'k': 164, 'l1': 0, 'l2': 1},# ~121.94s
    {'id': 17, 'k': 184, 'l1': 1, 'l2': 2} # ~125.47s
]
p3_bass_k = [8, 40, 76, 116, 152, 180] # min gap >= 28 steps (~4.94s) >= 2.0s
p3_chords, p3_notes = solve_piece("Midnight Toccata", 93.0, 128.0, 170, 40, 2, 8, 6, p3_hold_configs, p3_chord_configs, p3_bass_k)

all_chords = p1_chords + p2_chords + p3_chords
all_notes = p1_notes + p2_notes + p3_notes

print(f"Total Chords: {len(all_chords)}")
print(f"Total Notes: {len(all_notes)}")

# Save to json
with open('medley_chart_export.json', 'w') as f:
    json.dump({'RAW_CHORDS': all_chords, 'RAW_CHART_TIMINGS': all_notes}, f, indent=2)
print("Saved medley_chart_export.json successfully!")
