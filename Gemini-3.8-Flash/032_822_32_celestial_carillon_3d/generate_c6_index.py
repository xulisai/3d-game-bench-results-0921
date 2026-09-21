import json

medley_data = json.load(open('medley_chart_export.json'))
medley_chords = medley_data['RAW_CHORDS']
medley_notes = medley_data['RAW_CHART_TIMINGS']

# Encore notes & chords (Piece 3 shifted by 93.0s)
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

medley_notes_json = json.dumps(medley_notes)
medley_chords_json = json.dumps(medley_chords)
encore_notes_json = json.dumps(encore_notes)
encore_chords_json = json.dumps(encore_chords)

print(f"Medley notes: {len(medley_notes)}, Encore notes: {len(encore_notes)}")
