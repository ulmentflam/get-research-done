# Validation Exceptions

This document lists intentional references to old command names that should NOT be updated.

## Overview

During the v1.2 Command Unification (Phase 19), stale command references were identified and fixed.
Some references were intentionally preserved for historical or documentation purposes.

## Exceptions List

| File | Line | Old Command | Reason |
|------|------|-------------|--------|
| CHANGELOG.md | * | various | Historical version log - intentionally preserves old names for version history |
| .planning/** | * | various | Planning artifacts - historical context, explicitly out of scope per 19-CONTEXT.md |

## Validation Date

Last validated: 2026-02-02

## How to Re-validate

Run the stale reference detection:
```bash
rg '\b(plan-phase|execute-phase|discuss-phase|verify-work|research-phase|list-phase-assumptions|add-phase|insert-phase|remove-phase)\b' \
  --glob '!.planning/**' \
  --glob '!CHANGELOG.md' \
  --glob '!tests/reports/validation-exceptions.md' \
  -l
```

Any matches should either be fixed or added to this exceptions list with justification.

## Status

As of 2026-02-02:
- All stale references in active documentation have been fixed (Phase 19 Plan 01)
- Integration tests validate all renamed commands exist (Phase 19 Plan 02)
- No additional exceptions identified beyond documented historical references
