import re

# Test line from the file
test_line = "| 1 | **BioPartner 5, Leiden / Oegstgeest** | ★★★★★ | NL | Built | Reused structural steel from the former Gorlaeus high-rise becomes the main supporting structure / donor skeleton. | Furniture and fit-out reuse should not affect the rating; the rating is based on structural steel reuse. | Leiden University; Leiden Bio Science Park; Popma ter Steege / IMd sources |"

print("Test line:", test_line[:100])

# Try pattern that matches the table structure
# Tables have format: | priority | **Project** | rating | country | status | reasoning | caveat | sources |
pattern = r'^\|\s*(\d+)\s*\|\s*\*\*(.+?)\*\*\s*\|\s*([★☆]+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'

match = re.match(pattern, test_line)
if match:
    print('Match found!')
    for i, g in enumerate(match.groups()):
        print(f'Group {i}: {g[:50]}')
else:
    print('No match with first pattern')
    
    # Simpler pattern - just split by |
    parts = test_line.split('|')
    print(f'Split by | gives {len(parts)} parts')
    for i, p in enumerate(parts):
        print(f'{i}: "{p.strip()}"')
