"""Regenerate browser data, full narrative, and no-JavaScript leave-behind."""
import json
from pathlib import Path
from html import escape as e
p = Path(__file__).resolve().parent
beats = json.loads((p / 'beats.json').read_text())
assert len({b['id'] for b in beats}) == len(beats)
(p / 'beats.js').write_text('window.BEATS = ' + json.dumps(beats, indent=2) + ';\n')
(p / 'NARRATION.md').write_text('# Presenter narrative\n\nApproximate duration: 6 minutes 20 seconds at the planned 38 seconds per beat; actual delivery varies. No generated audio is included.\n\n' + '\n\n'.join('## ' + str(i+1) + '. ' + b['title'].replace('\n', ' ') + '\n\n' + b['notes'] for i,b in enumerate(beats)))
parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Develotype — static leave-behind</title><link rel="stylesheet" href="styles.css"></head><body class="static"><header><img class="logo" src="assets/logo.png" alt="Develotype"><a href="index.html">Interactive presentation ↗</a></header><main>']
for b in beats:
    source = f'<a href="{e(b["evidence"])}">develotype.com</a> — interpretation for this demonstration.' if b['evidence'].startswith('https') else e(b['evidence'])
    media = f'<video controls playsinline preload="metadata" style="width:min(100%,640px)" src="{e(b["video"])}">Local generation video requires the sibling video folder.</video>' if b['video'] else ''
    parts.append(f'<section class="beat"><p class="eyebrow">{e(b["eyebrow"])}</p><h2>{e(b["title"])}</h2><p class="intro">{e(b["body"])}</p><ul>' + ''.join('<li>'+e(t)+'</li>' for t in b['items']) + '</ul>' + media + f'<p class="speaker">{e(b["notes"])}</p><p class="source">{source}</p></section>')
parts.append('</main></body></html>')
(p / 'static.html').write_text('\n'.join(parts))
print(f'Synced {len(beats)} beats.')
