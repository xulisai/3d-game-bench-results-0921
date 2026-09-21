import json, re

# Load verified chart data
chart_data = json.load(open('chart_export.json'))
raw_chords_json = json.dumps(chart_data['RAW_CHORDS'], indent=2)
raw_timings_json = json.dumps(chart_data['RAW_CHART_TIMINGS'])

print("Chart data loaded successfully.")
