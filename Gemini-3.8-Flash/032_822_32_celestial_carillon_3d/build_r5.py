import json

data = json.load(open('chart_export.json'))
raw_chords_json = json.dumps(data['RAW_CHORDS'], indent=2)
raw_timings_json = json.dumps(data['RAW_CHART_TIMINGS'])

print(f"Loaded {len(data['RAW_CHORDS'])} chords, {len(data['RAW_CHART_TIMINGS'])} notes.")
