import json, math

def round_time(t):
    return round(t, 5)

# --- PIECE 1: Aurora Prelude (110 BPM, 0 to 40s) ---
# Grid: k * (30/110) = k * (3/11)
def p1_time(k):
    return round_time(k * (3.0 / 11.0))

# 4 Chords in P1 (lanes in {0, 1, 2})
# k values: 18, 38, 70, 100
p1_chords = [
    {"id": 0, "t": p1_time(18), "l1": 0, "l2": 1},
    {"id": 1, "t": p1_time(42), "l1": 1, "l2": 2},
    {"id": 2, "t": p1_time(76), "l1": 0, "l2": 2},
    {"id": 3, "t": p1_time(110), "l1": 0, "l2": 1}
]

# 4 Holds in P1 (dur between 1.0s and 2.5s)
# 1.0s <= dur <= 2.5s -> in 110 BPM grid (3/11 s ≈ 0.2727s), 4 steps = 1.09s, 5 steps = 1.36s, 6 steps = 1.636s, 7 steps = 1.909s
p1_holds = [
    {"type": "hold", "t": p1_time(10), "l": 0, "dur": round_time(5 * (3.0 / 11.0)), "endTime": p1_time(15)}, # 2.727 to 4.091
    {"type": "hold", "t": p1_time(30), "l": 2, "dur": round_time(6 * (3.0 / 11.0)), "endTime": p1_time(36)}, # 8.182 to 9.818
    {"type": "hold", "t": p1_time(60), "l": 1, "dur": round_time(6 * (3.0 / 11.0)), "endTime": p1_time(66)}, # 16.364 to 18.0
    {"type": "hold", "t": p1_time(94), "l": 2, "dur": round_time(6 * (3.0 / 11.0)), "endTime": p1_time(100)} # 25.636 to 27.273
]

# 6 Bass events in P1 (lane 3) (min gap >= 2.0s -> >= 8 grid steps)
p1_bass_k = [6, 24, 52, 84, 118, 136] # times ~ 1.63, 6.54, 14.18, 22.91, 32.18, 37.09
p1_bass = [{"type": "tap", "t": p1_time(k), "l": 3} for k in p1_bass_k]

# Remaining taps in P1: 48 total taps including bass (6 bass + 42 non-bass taps)
# Let's find valid slots for 42 non-bass taps in lanes 0, 1, 2.

print("Piece 1 configured.")
