import os
import re
import glob


def get_available_filename(out_file):
    base, ext = os.path.splitext(out_file)
    base_escaped = re.escape(base)
    # Pattern to match filenames like 'output.txt', 'output(1).txt', 'output(2).txt', etc.
    pattern = f"^{base_escaped}(\\((\\d+)\\))?{re.escape(ext)}$"
    existing_files = glob.glob(f"{base}*{ext}")
    max_index = 0

    for filename in existing_files:
        match = re.match(pattern, filename)
        if match:
            index = int(match.group(2)) if match.group(2) else 0
            max_index = max(max_index, index)

    if max_index == 0 and not os.path.exists(out_file):
        return out_file
    else:
        new_index = max_index + 1
        return f"{base}({new_index}){ext}"
