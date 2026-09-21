import json

# Grid steps:
# Sec 0: 0.3s (100 BPM 8th note). Valid k: 1 to 98 (0.3s to 29.4s)
# Sec 1: 3/13 s (130 BPM 8th note). Valid k: 0 to 106 (30.0s to 54.46s)
# Sec 2: 0.1875s (160 BPM 8th note). Valid k: 0 to 96 (55.0s to 73.0s)

def time_sec0(k):
    return round(k * 0.3, 4)

def time_sec1(k):
    return round(30.0 + k * (3.0 / 13.0), 5)

def time_sec2(k):
    return round(55.0 + k * 0.1875, 4)

# 13 bass notes (lane 3):
# Sec 0 (5 bass): k = 7 (2.1), k = 26 (7.8), k = 45 (13.5), k = 64 (19.2), k = 83 (24.9)
# Sec 1 (4 bass): k = 2 (30.46154), k = 27 (36.23077), k = 52 (42.0), k = 77 (47.76923)
# Sec 2 (4 bass): k = 3 (55.5625), k = 32 (61.0), k = 61 (66.4375), k = 94 (72.625)

# 12 Holds (between 1.0 and 2.5s duration):
# Sec 0 (5 holds):
# 1. k=10 (3.0), dur = 5*0.3 = 1.5, end=4.5, lane 0
# 2. k=28 (8.4), dur = 5*0.3 = 1.5, end=9.9, lane 1
# 3. k=48 (14.4), dur = 5*0.3 = 1.5, end=15.9, lane 2
# 4. k=68 (20.4), dur = 6*0.3 = 1.8, end=22.2, lane 0
# 5. k=88 (26.4), dur = 5*0.3 = 1.5, end=27.9, lane 1

# Sec 1 (4 holds):
# 6. k=8 (31.84615), dur = 6*(3/13)=1.38462, end=33.23077, lane 2
# 7. k=33 (37.61538), dur = 6*(3/13)=1.38462, end=39.0, lane 0
# 8. k=58 (43.38462), dur = 6*(3/13)=1.38462, end=44.76923, lane 1
# 9. k=83 (49.15385), dur = 7*(3/13)=1.61538, end=50.76923, lane 2

# Sec 2 (3 holds):
# 10. k=10 (56.875), dur = 8*0.1875 = 1.5, end=58.375, lane 0
# 11. k=38 (62.125), dur = 8*0.1875 = 1.5, end=63.625, lane 1
# 12. k=68 (67.75), dur = 8*0.1875 = 1.5, end=69.25, lane 2

# 10 Chords (lanes in {0, 1, 2}):
# Sec 0 (4 chords):
# c0: k=18 (5.4), l1=1, l2=2
# c1: k=38 (11.4), l1=0, l2=2
# c2: k=58 (17.4), l1=0, l2=1
# c3: k=78 (23.4), l1=1, l2=2

# Sec 1 (3 chords):
# c4: k=18 (34.15385), l1=0, l2=1
# c5: k=43 (39.92308), l1=0, l2=2
# c6: k=68 (45.69231), l1=1, l2=2

# Sec 2 (3 chords):
# c7: k=20 (58.75), l1=0, l2=1
# c8: k=48 (64.0), l1=0, l2=2
# c9: k=78 (69.625), l1=1, l2=2

print('Base structure defined. Designing complete note set...')
