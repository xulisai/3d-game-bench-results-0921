import json

medley_data = json.load(open('medley_chart_export.json'))
medley_chords = medley_data['RAW_CHORDS']
medley_notes = medley_data['RAW_CHART_TIMINGS']

# Prepare Encore notes and chords (Piece 3 shifted by 93.0s)
encore_notes = []
for n in medley_notes:
    if n.get('piece') == 'Midnight Toccata':
        item = dict(n)
        item['t'] = round(n['t'] - 93.0, 5)
        if 'endTime' in n:
            item['endTime'] = round(n['endTime'] - 93.0, 5)
        encore_notes.append(item)

encore_chords = []
for c in medley_chords:
    if c['t'] >= 93.0:
        item = dict(c)
        item['t'] = round(c['t'] - 93.0, 5)
        encore_chords.append(item)

print(f"Medley: {len(medley_notes)} notes, {len(medley_chords)} chords.")
print(f"Encore: {len(encore_notes)} notes, {len(encore_chords)} chords.")

medley_notes_json = json.dumps(medley_notes)
medley_chords_json = json.dumps(medley_chords)
encore_notes_json = json.dumps(encore_notes)
encore_chords_json = json.dumps(encore_chords)

print("JSON strings formatted.")
