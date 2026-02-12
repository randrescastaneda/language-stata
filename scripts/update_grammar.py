"""
Update stata.cson by adding missing commands to the built-in commands regex.
This script reads the current grammar, extracts the command regex,
adds new commands in alphabetical order, and writes the updated file.
"""

import re
import os


def load_missing_commands(path):
    """Load missing commands from the categorized file."""
    commands = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('##'):
                commands.add(line)
    return commands


def extract_and_update_regex(cson_content, new_commands):
    """Find the built-in commands regex and add new commands."""

    # Find the built-in commands match line
    pattern = r"(comment:\s*'Built in commands'\s*\n\s*match:\s*'\\\\b\()(.+?)(\)\\\\b')"

    match = re.search(pattern, cson_content, re.DOTALL)
    if not match:
        raise ValueError("Could not find 'Built in commands' pattern in grammar")

    prefix = match.group(1)
    current_regex = match.group(2)
    suffix = match.group(3)

    # Extract current commands
    current_commands = []
    for cmd in current_regex.split('|'):
        cmd = cmd.strip()
        current_commands.append(cmd)

    # Separate regex-special entries (lookbehinds, etc.) from plain commands
    plain_commands = []
    special_entries = []
    for cmd in current_commands:
        if '(' in cmd or '\\s' in cmd or '\\.' in cmd:
            special_entries.append(cmd)
        else:
            plain_commands.append(cmd)

    # Add new commands
    plain_set = set(plain_commands)
    added = []
    for cmd in new_commands:
        if cmd not in plain_set:
            plain_commands.append(cmd)
            added.append(cmd)

    # Sort all plain commands alphabetically
    plain_commands = sorted(set(plain_commands))

    # Rebuild: special entries first (they need specific positions),
    # then plain commands
    # Actually, let's keep the special entries in their alphabetical position
    # The only special entry is (?<!\\.)log which should stay at 'log' position
    all_commands = []
    special_dict = {}
    for entry in special_entries:
        # Extract the "core" command name for sorting
        core = re.sub(r'\(\?[<!]+[^)]*\)', '', entry)
        if core:
            special_dict[core] = entry

    for cmd in plain_commands:
        if cmd in special_dict:
            all_commands.append(special_dict[cmd])
            del special_dict[cmd]
        else:
            all_commands.append(cmd)

    # Add any remaining special entries
    for entry in special_dict.values():
        all_commands.append(entry)

    # Rebuild the regex
    new_regex = '|'.join(all_commands)

    # Replace in the content
    start = match.start()
    end = match.end()
    new_match = prefix + new_regex + suffix
    updated_content = cson_content[:start] + new_match + cson_content[end:]

    return updated_content, added


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)

    # Load missing commands
    missing_path = os.path.join(script_dir, 'missing_commands_categorized.txt')
    new_commands = load_missing_commands(missing_path)

    # Some commands from the missing list should NOT be added to the main regex
    # because they are prefix/special commands or already handled elsewhere
    # Let's filter out ones that overlap with special patterns
    exclude = {
        'datetime',  # Not a command, it's a concept/function set
        'import',    # Handled as part of special import patterns
        'export',    # Handled as part of special export patterns
    }
    new_commands -= exclude

    print(f"Commands to add: {len(new_commands)}")

    # Read the grammar file
    cson_path = os.path.join(repo_dir, 'grammars', 'stata.cson')
    with open(cson_path, 'r') as f:
        content = f.read()

    # Update the grammar
    updated_content, added = extract_and_update_regex(content, new_commands)

    print(f"Actually added (not already present): {len(added)}")
    for cmd in sorted(added):
        print(f"  + {cmd}")

    # Write the updated grammar
    with open(cson_path, 'w') as f:
        f.write(updated_content)

    print(f"\nUpdated {cson_path}")


if __name__ == '__main__':
    main()
