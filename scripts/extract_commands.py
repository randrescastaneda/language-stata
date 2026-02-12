"""
Extract current commands from stata.cson grammar file.
Outputs a sorted list of all built-in commands to current_commands.txt
"""

import re

def extract_commands(cson_path):
    with open(cson_path, 'r') as f:
        content = f.read()

    # Find the "Built in commands" match pattern
    # The regex is between \\b( and )\\b on the line(s) after "Built in commands"
    builtin_match = re.search(
        r"comment:\s*'Built in commands'\s*\n\s*match:\s*'\\\\b\((.+?)\)\\\\b'",
        content,
        re.DOTALL
    )

    if not builtin_match:
        print("ERROR: Could not find 'Built in commands' pattern")
        return []

    raw = builtin_match.group(1)
    # Split on pipe, clean up any regex-specific entries
    commands = []
    for cmd in raw.split('|'):
        cmd = cmd.strip()
        # Skip regex constructs (lookbehinds, etc.)
        if cmd.startswith('(?') or cmd.startswith('\\'):
            # But extract the actual command after the lookahead/behind
            # e.g., (?<!\\.)log -> log
            inner = re.sub(r'\(\?[<!]+[^)]*\)', '', cmd)
            if inner:
                commands.append(inner)
            continue
        # Skip entries with regex special chars (whitespace patterns, etc.)
        if '\\s' in cmd or '\\.' in cmd:
            commands.append(cmd.replace('\\s', ' ').replace('\\.', '.'))
            continue
        commands.append(cmd)

    # Also extract "Add on commands"
    addon_match = re.search(
        r"comment:\s*'Add on commands'\s*\n\s*match:\s*'\\\\b\((.+?)\)\\\\b'",
        content,
        re.DOTALL
    )

    addon_commands = []
    if addon_match:
        addon_commands = [c.strip() for c in addon_match.group(1).split('|')]

    return sorted(set(commands)), sorted(set(addon_commands))


if __name__ == '__main__':
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)
    cson_path = os.path.join(repo_dir, 'grammars', 'stata.cson')

    builtin, addon = extract_commands(cson_path)

    # Write built-in commands
    output_path = os.path.join(script_dir, 'current_commands.txt')
    with open(output_path, 'w') as f:
        f.write(f"# Built-in commands extracted from stata.cson\n")
        f.write(f"# Total: {len(builtin)}\n\n")
        for cmd in builtin:
            f.write(cmd + '\n')

    # Write add-on commands
    addon_path = os.path.join(script_dir, 'current_addon_commands.txt')
    with open(addon_path, 'w') as f:
        f.write(f"# Add-on commands extracted from stata.cson\n")
        f.write(f"# Total: {len(addon)}\n\n")
        for cmd in addon:
            f.write(cmd + '\n')

    print(f"Extracted {len(builtin)} built-in commands -> {output_path}")
    print(f"Extracted {len(addon)} add-on commands -> {addon_path}")
