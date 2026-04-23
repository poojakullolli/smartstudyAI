"""
Fix-style_utils script: truncates style_utils.py at the first clean
'return' line of create_navbar (line 1364) and removes all dead code below.
"""
import pathlib

target = pathlib.Path(__file__).parent / "style_utils.py"
lines  = target.read_text(encoding="utf-8").splitlines(keepends=True)

# Find the closing return line of the NEW create_navbar function
# The correct line looks like:
#     return " ".join(line.strip() for line in html.splitlines())
# It appears TWICE; we want the FIRST occurrence after line 1063

search  = '    return " ".join(line.strip() for line in html.splitlines())\n'
cut_at  = None

for i, line in enumerate(lines):
    if i < 1060:        # skip the old create_quick_action_button return
        continue
    if line == search:
        cut_at = i + 1  # keep this line, cut everything after
        break

if cut_at is None:
    print("ERROR: could not find target return line")
else:
    new_content = "".join(lines[:cut_at]) + "\n"
    target.write_text(new_content, encoding="utf-8")
    print(f"SUCCESS: truncated to {cut_at} lines ({len(new_content):,} bytes)")
