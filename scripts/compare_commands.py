"""
Compare current grammar commands against the Stata reference list.
Outputs missing commands that should be added to the grammar.
"""

import os
import re


def load_current_commands(path):
    """Load commands from current_commands.txt"""
    commands = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                commands.add(line)
    return commands


def load_reference_commands(path):
    """Load commands from stata_reference_commands.txt"""
    commands = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Skip category headers and empty lines
                commands.add(line)
    return commands


def check_abbreviation_coverage(cmd, current_commands):
    """Check if a command might be covered by an abbreviation pattern.

    For example, if 'regress' is the command and 'reg', 'regr', 'regre',
    'regres', 'regress' are all in current_commands, then it's covered.
    """
    # Check if the command itself is in the set
    if cmd in current_commands:
        return True

    # Check if any current command is a prefix of this one
    # (suggesting it's covered by abbreviation)
    for curr in current_commands:
        if cmd.startswith(curr) and len(curr) >= 2:
            return True

    return False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    current_path = os.path.join(script_dir, 'current_commands.txt')
    reference_path = os.path.join(script_dir, 'stata_reference_commands.txt')

    current = load_current_commands(current_path)
    reference = load_reference_commands(reference_path)

    print(f"Current grammar commands: {len(current)}")
    print(f"Reference commands: {len(reference)}")
    print()

    # Find commands in reference but NOT in current
    # Also check abbreviation coverage
    truly_missing = []
    possibly_covered = []

    for cmd in sorted(reference):
        if cmd not in current:
            if check_abbreviation_coverage(cmd, current):
                possibly_covered.append(cmd)
            else:
                truly_missing.append(cmd)

    # Find commands in current but not in reference (potentially deprecated)
    extra = sorted(current - reference)

    # Write results
    output_path = os.path.join(script_dir, 'missing_commands.txt')
    with open(output_path, 'w') as f:
        f.write(f"# Missing Stata commands (not in grammar, not covered by abbreviations)\n")
        f.write(f"# Total: {len(truly_missing)}\n")
        f.write(f"# Generated: 2026-02-11\n\n")
        for cmd in truly_missing:
            f.write(cmd + '\n')

    covered_path = os.path.join(script_dir, 'possibly_covered.txt')
    with open(covered_path, 'w') as f:
        f.write(f"# Commands possibly covered by abbreviation patterns already in grammar\n")
        f.write(f"# Total: {len(possibly_covered)}\n\n")
        for cmd in possibly_covered:
            f.write(cmd + '\n')

    print(f"=== TRULY MISSING (not in grammar at all) ===")
    print(f"Total: {len(truly_missing)}")
    print()
    for cmd in truly_missing:
        print(f"  {cmd}")

    print()
    print(f"=== POSSIBLY COVERED BY ABBREVIATIONS ===")
    print(f"Total: {len(possibly_covered)}")
    print()
    for cmd in possibly_covered:
        print(f"  {cmd}")

    print()
    print(f"Results saved to:")
    print(f"  {output_path}")
    print(f"  {covered_path}")


if __name__ == '__main__':
    main()
