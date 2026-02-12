"""
Update stata.json by adding missing commands to the built-in commands regex.
This script reads the updated grammars/stata.cson (which already has 176 new
commands) and adds any missing commands to stata.json's built-in regex.
"""

import json
import re
import os


def extract_commands_from_regex(regex_str):
    """Extract plain command names from a pipe-separated regex string."""
    plain = []
    special = []
    for part in regex_str.split('|'):
        part = part.strip()
        if not part:
            continue
        # Special entries contain regex constructs like (?<!\.)
        if '(' in part or '\\s' in part or '\\.' in part:
            special.append(part)
        else:
            plain.append(part)
    return plain, special


def extract_cson_commands(repo_dir):
    """Extract commands from the updated stata.cson built-in regex."""
    cson_path = os.path.join(repo_dir, 'grammars', 'stata.cson')
    with open(cson_path, 'r') as f:
        content = f.read()

    pattern = r"comment:\s*'Built in commands'\s*\n\s*match:\s*'\\\\b\((.+?)\)\\\\b'"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError("Could not find 'Built in commands' pattern in stata.cson")

    regex_body = match.group(1)
    plain, special = extract_commands_from_regex(regex_body)
    return set(plain), special


def update_json_file(json_path, new_commands):
    """Update the stata.json file by adding new commands to the built-in regex."""
    with open(json_path, 'r') as f:
        content = f.read()

    # Parse JSON to find the built-in commands pattern
    data = json.loads(content)

    # Find the built-in commands entry in repository.commands-other.patterns
    commands_patterns = data['repository']['commands-other']['patterns']
    builtin_entry = None
    for entry in commands_patterns:
        if entry.get('comment') == 'Built in commands':
            builtin_entry = entry
            break

    if not builtin_entry:
        raise ValueError("Could not find 'Built in commands' entry in stata.json")

    old_regex = builtin_entry['match']

    # Extract the body between \b( and )\b
    body_match = re.match(r'^\\b\((.+)\)\\b$', old_regex, re.DOTALL)
    if not body_match:
        raise ValueError(f"Unexpected regex format: {old_regex[:80]}...")

    regex_body = body_match.group(1)
    plain_cmds, special_entries = extract_commands_from_regex(regex_body)

    # Add new commands
    existing = set(plain_cmds)
    added = []
    for cmd in new_commands:
        if cmd not in existing:
            plain_cmds.append(cmd)
            added.append(cmd)

    # Sort all plain commands alphabetically
    plain_cmds = sorted(set(plain_cmds))

    # Rebuild with special entries in their alphabetical position
    special_dict = {}
    for entry in special_entries:
        core = re.sub(r'\(\?[<!]+[^)]*\)', '', entry)
        if core:
            special_dict[core] = entry

    all_commands = []
    for cmd in plain_cmds:
        if cmd in special_dict:
            all_commands.append(special_dict[cmd])
            del special_dict[cmd]
        else:
            all_commands.append(cmd)

    # Add any remaining special entries at the end
    for entry in special_dict.values():
        all_commands.append(entry)

    # Build new regex
    new_regex = '\\b(' + '|'.join(all_commands) + ')\\b'

    # Update the entry
    builtin_entry['match'] = new_regex

    # Write the updated JSON with same formatting
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write('\n')

    return sorted(added)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(script_dir)

    # Extract commands from the updated CSON (source of truth)
    cson_commands, _ = extract_cson_commands(repo_dir)
    print(f"Commands in updated stata.cson: {len(cson_commands)}")

    # Update stata.json
    json_path = os.path.join(repo_dir, 'stata.json')
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    added = update_json_file(json_path, cson_commands)

    print(f"Commands added to stata.json: {len(added)}")
    for cmd in added:
        print(f"  + {cmd}")

    print(f"\nUpdated {json_path}")


if __name__ == '__main__':
    main()
