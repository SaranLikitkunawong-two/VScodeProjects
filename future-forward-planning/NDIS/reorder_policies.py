"""
Reorder Policy Suite so that the first 4 policies are:
  1 — Incident Management          (was Policy 2, PM-POL-002)
  2 — Complaints and Feedback      (was Policy 3, PM-POL-003)
  3 — Risk Management              (was Policy 4, PM-POL-004)
  4 — Human Resources              (was Policy 5, PM-POL-005)
  5 — Privacy and Confidentiality  (was Policy 1, PM-POL-001)
  6-17 — unchanged

Also applies the same PM-POL renumbering to all other NDIS markdown files.
"""

import re
import os

BASE = r'C:\Users\Saran Likitkunawong\VScode\NDIS'
SUITE = os.path.join(BASE, 'Policy Suite - Draft Templates.md')

# Old policy number → new policy number (for positions 1-5 only)
NEW_ORDER = [2, 3, 4, 5, 1] + list(range(6, 18))   # old nums in desired new order

# PM-POL mapping  (old suffix → new suffix)
PMPOL_MAP = {
    '001': '005',   # Privacy:     001 → 005
    '002': '001',   # Incident:    002 → 001
    '003': '002',   # Complaints:  003 → 002
    '004': '003',   # Risk:        004 → 003
    '005': '004',   # HR:          005 → 004
}

# Required Policy List rows in new order (rebuilt from scratch for accuracy)
POLICY_TABLE_ROWS = [
    ('1',  'Incident Management',                          '1.9, NDIS Incident Rules 2018'),
    ('2',  'Complaints and Feedback Management',           '1.10'),
    ('3',  'Risk Management',                              '1.7'),
    ('4',  'Human Resources and Worker Screening',         '1.8'),
    ('5',  'Privacy and Confidentiality',                  '1.3, Privacy Act 1988, APPs'),
    ('6',  'Code of Conduct',                              'NDIS Code of Conduct'),
    ('7',  'Record Keeping and Information Management',    '1.11'),
    ('8',  'Participant Rights and Responsibilities',      '1.1–1.5'),
    ('9',  'Continuity of Supports',                      '1.6'),
    ('10', 'Financial Management (Plan Management)',       'PM Supplementary Module'),
    ('11', 'Fraud Prevention and Detection',               'PM Supplementary Module, Integrity Act 2025'),
    ('12', 'Conflict of Interest',                        '1.6, NDIS Code of Conduct'),
    ('13', 'Worker Qualifications and Professional Development', 'PM Verification Module (Oct 2025)'),
    ('14', 'Whistleblower Protection',                    'NDIS Amendment (Integrity and Safeguarding) Act 2025'),
    ('15', 'Cyber Security and Data Protection',          '1.7, Privacy Act 1988'),
    ('16', 'Marketing, Referrals and Anti-Inducement',    'NDIS Amendment (Integrity and Safeguarding) Act 2025'),
    ('17', 'Governance and Continuous Improvement',       'NDIS Verification Module, Practice Standards 1.2'),
]


def apply_pmpol_remap(text):
    """Two-pass PM-POL renumber using temp markers to avoid collisions."""
    for old, _ in PMPOL_MAP.items():
        text = text.replace(f'PM-POL-{old}', f'TMPOL-{old}')
    for old, new in PMPOL_MAP.items():
        text = text.replace(f'TMPOL-{old}', f'PM-POL-{new}')
    return text


def rebuild_policy_table():
    header = '| # | Policy | NDIS Standard / Basis |\n|---|--------|-----------------------|'
    rows = '\n'.join(f'| {n} | {title} | {std} |' for n, title, std in POLICY_TABLE_ROWS)
    return header + '\n' + rows


def reorder_suite():
    with open(SUITE, encoding='utf-8') as f:
        content = f.read()

    # ── 1. Split into header + 17 policy sections ──────────────────────────────
    policy_starts = [
        (m.start(), int(m.group(1)))
        for m in re.finditer(r'^# POLICY (\d+):', content, re.MULTILINE)
    ]

    preamble = content[:policy_starts[0][0]]

    sections = {}
    for i, (start, num) in enumerate(policy_starts):
        end = policy_starts[i + 1][0] if i + 1 < len(policy_starts) else len(content)
        sections[num] = content[start:end]

    # ── 2. Rebuild Required Policy List table in preamble ──────────────────────
    new_table = rebuild_policy_table()
    preamble = re.sub(
        r'\| # \| Policy \| NDIS Standard.*?(?=\n\n|\n---|\Z)',
        new_table,
        preamble,
        flags=re.DOTALL,
    )

    # ── 3. Reassemble sections in new order, updating # POLICY N: headers ──────
    new_body_parts = []
    for new_num, old_num in enumerate(NEW_ORDER, start=1):
        section = sections[old_num]
        # Replace the POLICY header number
        section = re.sub(
            r'^(# POLICY )\d+(:)',
            rf'\g<1>{new_num}\2',
            section,
            count=1,
            flags=re.MULTILINE,
        )
        new_body_parts.append(section)

    new_content = preamble + ''.join(new_body_parts)

    # ── 4. Remap all PM-POL-001..005 references ────────────────────────────────
    new_content = apply_pmpol_remap(new_content)

    with open(SUITE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'Policy Suite updated: {SUITE}')


def update_supporting_files():
    """Apply PM-POL renumbering to all other NDIS markdown files."""
    md_files = [
        f for f in os.listdir(BASE)
        if f.endswith('.md') and f != 'Policy Suite - Draft Templates.md'
    ]
    for filename in md_files:
        path = os.path.join(BASE, filename)
        with open(path, encoding='utf-8') as f:
            text = f.read()
        updated = apply_pmpol_remap(text)
        if updated != text:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f'  Updated: {filename}')
        else:
            print(f'  No changes: {filename}')


if __name__ == '__main__':
    print('Reordering Policy Suite...')
    reorder_suite()
    print('\nUpdating supporting files...')
    update_supporting_files()
    print('\nDone.')
