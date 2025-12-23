import re
from pathlib import Path

vtt_path = Path('CoCreateAI Biochar_wesley.vtt')
out_path = vtt_path.with_suffix('.txt')
out_lines = []
speaker = None

with vtt_path.open('r', encoding='utf-8') as f:
    for raw in f:
        line = raw.strip()
        if not line or line == 'WEBVTT' or '-->' in line:
            continue
        if re.match(r'^[0-9a-fA-F-]+/\d+-\d+$', line):
            continue
        m = re.match(r'<v\s+([^>]+)>(.*)</v>', line)
        if m:
            speaker = m.group(1).strip()
            text = m.group(2).strip()
            out_lines.append(f"{speaker}: {text}")
            continue
        m = re.match(r'<v\s+([^>]+)>(.*)', line)
        if m:
            speaker = m.group(1).strip()
            text = m.group(2).strip()
            out_lines.append(f"{speaker}: {text}")
            continue
        if speaker:
            out_lines.append(f"{speaker}: {line}")
        else:
            out_lines.append(line)

with out_path.open('w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print('wrote', out_path.name, 'lines', len(out_lines))
