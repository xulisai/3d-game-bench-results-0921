import math, json

# Re-run solve_chart logic and export final chart array
with open("solve_chart.py") as f:
    code = f.read()

# Let's inspect res
exec(compile(code, "solve_chart.py", "exec"))

selected_taps = res

# Build the complete note list:
# 13 bass taps
# 82 melody taps
# 12 holds
# 10 chords (20 tap notes)

chart_notes = []

# Taps (95 total: 13 bass + 82 melody)
for t, l in bass_events:
    chart_notes.append({"type": "tap", "t": t, "l": l})

for t, l in selected_taps:
    chart_notes.append({"type": "tap", "t": t, "l": l})

# Holds (12 total)
for t, l, dur, end_t in holds:
    chart_notes.append({"type": "hold", "t": t, "l": l, "dur": dur, "endTime": end_t})

# Chords (10 chords -> 20 notes)
for c in chords:
    chart_notes.append({"type": "tap", "t": c["t"], "l": c["l1"], "chordId": c["id"], "partnerLane": c["l2"]})
    chart_notes.append({"type": "tap", "t": c["t"], "l": c["l2"], "chordId": c["id"], "partnerLane": c["l1"]})

chart_notes.sort(key=lambda n: (n["t"], n["l"]))

print("--- VERIFYING CHART CONSTRAINTS ---")

# 1. Total notes and breakdown
taps_only = [n for n in chart_notes if n["type"] == "tap" and "chordId" not in n]
chord_notes = [n for n in chart_notes if "chordId" in n]
hold_notes = [n for n in chart_notes if n["type"] == "hold"]
bass_notes = [n for n in chart_notes if n["l"] == 3]

print(f"Single taps: {len(taps_only)} (Expected: 95)")
assert len(taps_only) == 95, f"Expected 95 single taps, got {len(taps_only)}"

print(f"Chord notes: {len(chord_notes)} (Expected: 20 across 10 chords)")
assert len(chord_notes) == 20, f"Expected 20 chord notes, got {len(chord_notes)}"

print(f"Holds: {len(hold_notes)} (Expected: 12)")
assert len(hold_notes) == 12, f"Expected 12 holds, got {len(hold_notes)}"

print(f"Bass lane events: {len(bass_notes)} (Expected: 13)")
assert len(bass_notes) == 13, f"Expected 13 bass events, got {len(bass_notes)}"

total_judgments = len(taps_only) + len(chord_notes) + len(hold_notes) * 2
print(f"Total judgments: {total_judgments} (Expected: 139)")
assert total_judgments == 139, f"Expected 139 judgments, got {total_judgments}"

# 2. Check hold durations
for h in hold_notes:
    assert 1.0 <= h["dur"] <= 2.5, f"Hold dur out of range: {h}"
    assert abs(h["t"] + h["dur"] - h["endTime"]) < 1e-4, f"Hold timing mismatch: {h}"
print("Hold durations valid: 1.0s to 2.5s.")

# 3. Check section quantizations
for n in chart_notes:
    t = n["t"]
    if t < 30.0:
        k = round(t / 0.3)
        assert abs(t - k * 0.3) < 1e-3, f"Sec 0 quantization failed for {n}"
    elif t < 55.0:
        k = round((t - 30.0) / (3.0 / 13.0))
        assert abs(t - (30.0 + k * (3.0 / 13.0))) < 1e-3, f"Sec 1 quantization failed for {n}"
    else:
        k = round((t - 55.0) / 0.1875)
        assert abs(t - (55.0 + k * 0.1875)) < 1e-3, f"Sec 2 quantization failed for {n}"
print("All note hit times strictly quantized to section eighth-note grids.")

# 4. Check density limits: <= 2 chart events per second overall
# Collect chart event times: a chord is 1 event at time t
event_times = []
seen_chords = set()
for n in chart_notes:
    if "chordId" in n:
        if n["chordId"] not in seen_chords:
            seen_chords.add(n["chordId"])
            event_times.append(n["t"])
    else:
        event_times.append(n["t"])

event_times.sort()
print(f"Total distinct chart events: {len(event_times)}")

for i in range(len(event_times)):
    t0 = event_times[i]
    # Check count in [t0, t0 + 1.0]
    cnt = sum(1 for t in event_times if t0 <= t <= t0 + 1.0 + 1e-5)
    assert cnt <= 2, f"Density violated at t={t0}: {cnt} events in 1.0s!"
print("Density limit PASSED: <= 2 chart events per second in every 1.0s window.")

# 5. Check lane spacing: never two events in same lane closer than 0.5s (hold occupies lane for whole duration)
for lane in range(4):
    lane_items = [n for n in chart_notes if n["l"] == lane]
    lane_items.sort(key=lambda x: x["t"])
    for i in range(len(lane_items) - 1):
        curr = lane_items[i]
        nxt = lane_items[i+1]
        curr_end = curr["endTime"] if curr["type"] == "hold" else curr["t"]
        gap = nxt["t"] - curr_end
        assert gap >= 0.4999, f"Lane {lane} spacing violated between {curr} and {nxt}, gap={gap}"
print("Lane spacing PASSED: >= 0.5s spacing between all events in every lane.")

# 6. Check bass lane: consecutive notes never closer than 2.0s
bass_items = [n for n in chart_notes if n["l"] == 3]
bass_items.sort(key=lambda x: x["t"])
for i in range(len(bass_items) - 1):
    gap = bass_items[i+1]["t"] - bass_items[i]["t"]
    assert gap >= 1.999, f"Bass spacing violated: gap={gap} between {bass_items[i]} and {bass_items[i+1]}"
print(f"Bass lane spacing PASSED: min gap = {min(bass_items[i+1]['t'] - bass_items[i]['t'] for i in range(len(bass_items)-1)):.2f}s >= 2.0s.")

# 7. Check chords: never involve bass lane and never overlap a hold in either lane
for c in chords:
    assert c["l1"] != 3 and c["l2"] != 3, f"Chord in bass lane: {c}"
    for h in hold_notes:
        if h["l"] in (c["l1"], c["l2"]):
            assert not (h["t"] - 0.4999 <= c["t"] <= h["endTime"] + 0.4999), f"Chord overlaps hold: {c} and {h}"
print("Chord rules PASSED: never bass lane, never overlap holds.")

# Output JSON for inclusion in index.html
with open("chart_export.json", "w") as f:
    json.dump({
        "RAW_CHORDS": chords,
        "RAW_CHART_TIMINGS": chart_notes
    }, f, indent=2)

print("Exported chart_export.json successfully!")
