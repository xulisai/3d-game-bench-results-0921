import math, json

def time_sec0(k):
    return round(k * 0.3, 4)

def time_sec1(k):
    return round(30.0 + k * (3.0 / 13.0), 5)

def time_sec2(k):
    return round(55.0 + k * 0.1875, 4)

# 1. 13 Bass taps (lane 3)
bass_events = [
    (time_sec0(7), 3),   # 2.1
    (time_sec0(26), 3),  # 7.8
    (time_sec0(45), 3),  # 13.5
    (time_sec0(64), 3),  # 19.2
    (time_sec0(83), 3),  # 24.9
    (time_sec1(2), 3),   # 30.46154
    (time_sec1(27), 3),  # 36.23077
    (time_sec1(52), 3),  # 42.0
    (time_sec1(77), 3),  # 47.76923
    (time_sec2(3), 3),   # 55.5625
    (time_sec2(32), 3),  # 61.0
    (time_sec2(61), 3),  # 66.4375
    (time_sec2(96), 3)   # 73.0
]

# 2. 12 Holds (lanes 0, 1, 2)
# (t, lane, dur, end_time)
holds = [
    (time_sec0(10), 0, round(5 * 0.3, 4), time_sec0(15)),   # 3.0 to 4.5
    (time_sec0(29), 1, round(5 * 0.3, 4), time_sec0(34)),   # 8.7 to 10.2
    (time_sec0(48), 2, round(5 * 0.3, 4), time_sec0(53)),   # 14.4 to 15.9
    (time_sec0(68), 0, round(6 * 0.3, 4), time_sec0(74)),   # 20.4 to 22.2
    (time_sec0(88), 1, round(5 * 0.3, 4), time_sec0(93)),   # 26.4 to 27.9
    (time_sec1(8), 2, round(6 * (3.0/13.0), 5), time_sec1(14)),   # 31.846 to 33.231
    (time_sec1(33), 0, round(6 * (3.0/13.0), 5), time_sec1(39)),  # 37.615 to 39.0
    (time_sec1(58), 1, round(6 * (3.0/13.0), 5), time_sec1(64)),  # 43.385 to 44.769
    (time_sec1(83), 2, round(7 * (3.0/13.0), 5), time_sec1(90)),  # 49.154 to 50.769
    (time_sec2(10), 0, round(8 * 0.1875, 4), time_sec2(18)),      # 56.875 to 58.375
    (time_sec2(38), 1, round(8 * 0.1875, 4), time_sec2(46)),      # 62.125 to 63.625
    (time_sec2(68), 2, round(8 * 0.1875, 4), time_sec2(76))       # 67.75 to 69.25
]

# 3. 10 Chords (lanes in {0, 1, 2})
chords = [
    {"id": 0, "t": time_sec0(18), "l1": 1, "l2": 2},  # 5.4
    {"id": 1, "t": time_sec0(38), "l1": 0, "l2": 2},  # 11.4
    {"id": 2, "t": time_sec0(58), "l1": 0, "l2": 1},  # 17.4
    {"id": 3, "t": time_sec0(78), "l1": 1, "l2": 2},  # 23.4
    {"id": 4, "t": time_sec1(18), "l1": 0, "l2": 1},  # 34.15385
    {"id": 5, "t": time_sec1(43), "l1": 0, "l2": 2},  # 39.92308
    {"id": 6, "t": time_sec1(68), "l1": 1, "l2": 2},  # 45.69231
    {"id": 7, "t": time_sec2(22), "l1": 0, "l2": 1},  # 59.125
    {"id": 8, "t": time_sec2(50), "l1": 0, "l2": 2},  # 64.375
    {"id": 9, "t": time_sec2(78), "l1": 0, "l2": 1}   # 69.625
]

# Fixed occupied intervals per lane:
lane_intervals = {0: [], 1: [], 2: [], 3: []}

for t, l in bass_events:
    lane_intervals[l].append((t, t))

for t, l, dur, end_t in holds:
    lane_intervals[l].append((t, end_t))

for c in chords:
    lane_intervals[c["l1"]].append((c["t"], c["t"]))
    lane_intervals[c["l2"]].append((c["t"], c["t"]))

# Existing event times for density checking:
# A chord is 1 chart event at time t. A hold is 1 chart event at time t. A bass tap is 1 chart event.
fixed_event_times = [t for t, l in bass_events] + [t for t, l, dur, end_t in holds] + [c["t"] for c in chords]

# Candidate grid slots in Sec 0, 1, 2
# Sec 0: k from 2 to 98
# Sec 1: k from 0 to 106
# Sec 2: k from 0 to 95

candidates = []

for k in range(2, 98):
    t = time_sec0(k)
    for l in (0, 1, 2):
        candidates.append((t, l))

for k in range(0, 107):
    t = time_sec1(k)
    for l in (0, 1, 2):
        candidates.append((t, l))

for k in range(0, 96):
    t = time_sec2(k)
    for l in (0, 1, 2):
        candidates.append((t, l))

# Filter candidates that violate >= 0.5s lane rule with existing intervals:
def is_lane_valid(t, l, current_intervals):
    for st, en in current_intervals[l]:
        # If interval is [st, en], distance from point t must be >= 0.5
        # If t < st: st - t >= 0.4999
        # If t > en: t - en >= 0.4999
        # If st <= t <= en: false
        if t >= st - 0.4999 and t <= en + 0.4999:
            return False
    return True

valid_candidates = [(t, l) for (t, l) in candidates if is_lane_valid(t, l, lane_intervals)]

print(f"Total valid candidate slots: {len(valid_candidates)}")

# We need to select exactly 82 taps from valid_candidates!
# Let's greedily pick slots distributed across time while maintaining:
# 1) Lane spacing >= 0.5s among picked taps
# 2) Overall event density <= 2 events in any 1-second window

# Let's do a backtracking or greedy search with step spacing
target_count = 82

# Target distribution:
# Sec 0 (30s): ~32 taps
# Sec 1 (25s): ~27 taps
# Sec 2 (20s): ~23 taps
# 32 + 27 + 23 = 82 taps!

import random
# Deterministic seed for Python search
rng = random.Random(12345)

# Sort valid candidates by time
valid_candidates.sort(key=lambda x: (x[0], x[1]))

# Group by time
by_time = {}
for t, l in valid_candidates:
    by_time.setdefault(t, []).append(l)

sorted_times = sorted(by_time.keys())

# Let's search
def check_density(all_times):
    # Check max 2 events in any 1.0s window
    times = sorted(all_times)
    n = len(times)
    for i in range(n):
        t0 = times[i]
        j = i
        while j < n and times[j] <= t0 + 1.0001:
            j += 1
        if j - i > 2:
            return False
    return True

print("Checking fixed events density...")
print("Fixed events density valid?", check_density(fixed_event_times))

# Now let's pick 82 times from sorted_times such that:
# - at each picked time, choose 1 lane that satisfies lane spacing
# - density of (fixed_event_times + picked_times) <= 2 in any 1.0s window
# - exactly 82 picked

def solve():
    # Let's use a dynamic programming / greedy approach across sorted_times
    # We can filter sorted_times to those where adding an event doesn't violate density with fixed_event_times
    # In any [t, t+1.0] window, count(fixed) + count(picked) <= 2
    # Notice: if we ensure between any two events in (fixed + picked) the distance is >= 0.45s, then in 1.0s there can be at most 2 events!
    # Let's check: if min distance between ANY two chart events is >= 0.45s (e.g. 0.46s), then 3 events would require >= 2*0.46 = 0.92s,
    # wait: 3 events at 0.0, 0.46, 0.92 would be 3 in 0.92 <= 1.0s!
    # So to have at most 2 events in 1.0s, between every pair of events the average spacing is >= 0.5s, or density check is strictly <= 2.
    
    # Let's run a backtracking search
    selected = [] # list of (t, l)
    cur_lane_intervals = {0: list(lane_intervals[0]), 1: list(lane_intervals[1]), 2: list(lane_intervals[2])}
    cur_event_times = list(fixed_event_times)
    
    # We want 82 notes. Let's step through time:
    # 75s / (82 + 13 + 12 + 10) = 75 / 117 = ~0.64s per event!
    last_t = 0.0
    
    for t in sorted_times:
        if len(selected) == target_count:
            break
        # Density check if we add t:
        test_times = cur_event_times + [t]
        if not check_density(test_times):
            continue
        
        # Try available lanes at t:
        avail_lanes = [l for l in by_time[t] if is_lane_valid(t, l, cur_lane_intervals)]
        if not avail_lanes:
            continue
        
        # Choose lane (round robin or lane with lowest current count)
        lane_counts = {l: sum(1 for _, sl in selected if sl == l) for l in avail_lanes}
        best_lane = min(avail_lanes, key=lambda l: lane_counts[l])
        
        selected.append((t, best_lane))
        cur_lane_intervals[best_lane].append((t, t))
        cur_event_times.append(t)
    
    print(f"Selected {len(selected)} taps.")
    return selected

res = solve()
