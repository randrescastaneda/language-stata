"""
Refined comparison: accounts for commands handled by special patterns
in stata.cson (outside the main 'Built in commands' regex).
"""

import os

# Commands that are handled by SPECIAL PATTERNS in stata.cson
# (not in the main built-in regex, but still highlighted)
HANDLED_ELSEWHERE = {
    # Line 37: conditionals
    'if', 'else',
    # Line 42: scalar
    'scalar',
    # Line 45: merge with m:n syntax
    'merge',
    # Line 74, 86: foreach
    'foreach',
    # Line 104: forvalues
    'forvalues',
    # Line 126: while, continue
    'while', 'continue',
    # Line 132: assert
    'assert',
    # Line 135: prefix commands requiring colon
    'by', 'bysort', 'statsby', 'rolling', 'bootstrap', 'jackknife',
    'permute', 'simulate', 'svy', 'mi', 'nestreg', 'stepwise', 'xi',
    'fp', 'mfp', 'version',
    # Line 142: prefixes not requiring colon
    'quietly', 'noisily', 'capture',
    # Line 145: program
    'program',
    # Line 188-193: syntax
    'syntax',
    # Line 309: save, use, notes, format, destring, tostring
    'save', 'saveold', 'destring', 'tostring', 'use', 'notes', 'format',
    # Line 312: exit, end
    'exit', 'end',
    # Line 329: generate, egen
    'generate', 'egen',
    # Line 342: set type
    # Line 395: label
    'label',
    # Line 401, 417: drop, keep
    'drop', 'keep',
    # Line 459: odbc
    'odbc',
    # Line 1393: built-in variables/keywords (not commands per se)
    # 'obs' is not a command, it's a keyword in some contexts
    'obs',
    # args, tempvar, tempname, tempfile are in programming patterns
    'args', 'tempvar', 'tempname', 'tempfile',
    # macro, gettoken, tokenize
    'macro', 'gettoken', 'tokenize',
    # These are Mata keywords, handled in Mata section
    'mata',
    # These are basic Stata infrastructure
    'display', 'set', 'return', 'creturn', 'sreturn', 'ereturn',
    'mark', 'marksample', 'markout', 'numlist',
    'preserve', 'restore',
    # file is handled
    'file',
    # do, run, include
    'do', 'run', 'include',
    # log, cmdlog
    'log', 'cmdlog',
    # Various other infrastructure
    'profile', 'error',
}

# Commands from the "possibly covered" list that are genuinely NEW commands
# (not abbreviations of existing ones)
FALSE_POSITIVES_IN_POSSIBLY_COVERED = {
    # These are NEW Stata commands, not abbreviations:
    'cate',           # Stata 19: conditional average treatment effects
    'categraph',      # Stata 19: CATE graphs
    'cfprobit',       # control function probit
    'cfregress',      # control function regress
    'ciwidth',        # confidence interval width
    'demandsys',      # demand system estimation
    'didregress',     # difference-in-differences
    'discrim',        # discriminant analysis
    'dsge',           # DSGE models
    'dsgenl',         # nonlinear DSGE
    'dslogit',        # double-selection logit
    'dspoisson',      # double-selection Poisson
    'dsregress',      # double-selection regress
    'eregress',       # extended regress
    'grmap',          # mapping command
    'heckoprobit',    # heckman ordered probit
    'heckpoisson',    # heckman Poisson
    'heckprobit',     # heckman probit
    'hetoprobit',     # heteroskedastic ordered probit
    'hetprobit',      # heteroskedastic probit
    'hetregress',     # heteroskedastic regress
    'insobs',         # insert observations
    'irt',            # item response theory
    'irtgraph',       # IRT graphs
    'margins',        # marginal effects
    'marginsplot',    # margins plot
    'mlexp',          # ML expression evaluator
    'nlsur',          # nonlinear SUR
    'sem',            # structural equation modeling
    'splitsample',    # split sample
    'stcrreg',        # competing risks regression
    'stintcox',       # interval-censored Cox
    'stintreg',       # interval-censored survival
    'stmgintcox',     # marginal interval-censored Cox
    'stteffects',     # survival treatment effects
    'tebalance',      # treatment effects balance
    'teffects',       # treatment effects
    'telasso',        # treatment effects lasso
    'teoverlap',      # treatment effects overlap
    'varmanage',      # variable manager
    'zipfile',        # zip file operations
}


def load_commands(path):
    commands = set()
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                commands.add(line)
    return commands


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current = load_commands(os.path.join(script_dir, 'current_commands.txt'))
    reference = load_commands(os.path.join(script_dir, 'stata_reference_commands.txt'))

    # All commands currently in the grammar (including special patterns)
    all_covered = current | HANDLED_ELSEWHERE

    # Commands that are genuinely missing
    truly_missing = set()
    for cmd in reference:
        if cmd not in all_covered:
            truly_missing.add(cmd)

    # Add false positives from "possibly covered" that are actually new commands
    for cmd in FALSE_POSITIVES_IN_POSSIBLY_COVERED:
        if cmd not in all_covered and cmd in reference:
            truly_missing.add(cmd)

    truly_missing = sorted(truly_missing)

    # Categorize missing commands
    categories = {
        'New estimation commands (Stata 16+)': [],
        'Panel/longitudinal data': [],
        'Multilevel mixed-effects': [],
        'Causal inference & treatment effects': [],
        'Lasso & machine learning': [],
        'Bayesian analysis': [],
        'Tables & collections': [],
        'Data management (frames, etc.)': [],
        'Survival analysis': [],
        'Other new commands': [],
    }

    # Simple categorization rules
    for cmd in truly_missing:
        if cmd.startswith('bayes') or cmd == 'bmaregress':
            categories['Bayesian analysis'].append(cmd)
        elif cmd.startswith('xt') or cmd.startswith('me'):
            categories['Panel/longitudinal data'].append(cmd)
        elif cmd in ('teffects', 'stteffects', 'didregress', 'hdidregress',
                     'xtdidregress', 'xthdidregress', 'eteffects', 'etregress',
                     'etpoisson', 'lateffects', 'mediate', 'telasso', 'cate',
                     'gencohort', 'tebalance', 'teoverlap', 'latebalance',
                     'lateoverlap', 'categraph'):
            categories['Causal inference & treatment effects'].append(cmd)
        elif cmd in ('lasso', 'elasticnet', 'sqrtlasso', 'dsregress', 'dslogit',
                     'dspoisson', 'poregress', 'pologit', 'popoisson',
                     'poivregress', 'xporegress', 'xpologit', 'xpopoisson',
                     'xpoivregress', 'h2oml', 'h2omlgraph', 'h2omltree',
                     'bicplot', 'coefpath', 'cvplot'):
            categories['Lasso & machine learning'].append(cmd)
        elif cmd in ('collect', 'dtable', 'etable'):
            categories['Tables & collections'].append(cmd)
        elif cmd.startswith('frame') or cmd.startswith('fr') or cmd in ('vl', 'dyngen', 'unicode', 'zipfile', 'snapshot', 'splitsample', 'putmata', 'putexcel', 'bcal', 'changeeol', 'icd10', 'icd10cm', 'icd10pcs', 'jdbc', 'varmanage', 'insobs', 'assertnested'):
            categories['Data management (frames, etc.)'].append(cmd)
        elif cmd.startswith('st') and cmd not in categories.get('Causal inference & treatment effects', []):
            categories['Survival analysis'].append(cmd)
        elif cmd.startswith('sp'):
            categories['Other new commands'].append(cmd)
        else:
            # Check if it's a mixed-effects or panel command
            if cmd.startswith('me'):
                categories['Multilevel mixed-effects'].append(cmd)
            else:
                categories['New estimation commands (Stata 16+)'].append(cmd)

    # Write categorized output
    output_path = os.path.join(script_dir, 'missing_commands_categorized.txt')
    with open(output_path, 'w') as f:
        f.write("# Missing Stata Commands — Categorized\n")
        f.write(f"# Total missing: {len(truly_missing)}\n")
        f.write("# These commands should be added to grammars/stata.cson\n")
        f.write("# Generated: 2026-02-11\n\n")

        for category, cmds in categories.items():
            if cmds:
                f.write(f"\n## {category} ({len(cmds)} commands)\n")
                for cmd in sorted(cmds):
                    f.write(f"  {cmd}\n")

    print(f"Total truly missing commands: {len(truly_missing)}")
    print(f"\nSaved categorized list to: {output_path}")
    print()
    for category, cmds in categories.items():
        if cmds:
            print(f"\n## {category} ({len(cmds)})")
            for cmd in sorted(cmds):
                print(f"  {cmd}")


if __name__ == '__main__':
    main()
