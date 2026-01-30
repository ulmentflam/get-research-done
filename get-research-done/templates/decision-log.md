# Decision Log Template

Template for `human_eval/decision_log.md` — central chronological record of all human evaluation decisions.

---

## File Template

```markdown
# Human Evaluation Decision Log

This log tracks all human evaluation decisions for this research project.

| Timestamp | Run | Decision | Key Metric | Reference |
|-----------|-----|----------|------------|-----------|
```

---

## Usage Notes

- **Append-only:** New entries always added at the bottom (chronological order)
- **Timestamp:** YYYY-MM-DD HH:MM format (local time)
- **Run:** Run directory name (e.g., run_003_tuned)
- **Decision:** One of Seal, Iterate, Archive
- **Key Metric:** Primary metric with value (e.g., F1=0.85)
- **Reference:** Relative path to run directory

## Example Entries

| Timestamp | Run | Decision | Key Metric | Reference |
|-----------|-----|----------|------------|-----------|
| 2026-01-30 14:23 | run_003_tuned | Seal | F1=0.85 | experiments/run_003_tuned/ |
| 2026-01-29 10:15 | run_002_baseline | Iterate | F1=0.76 | experiments/run_002_baseline/ |
| 2026-01-28 16:45 | run_001_initial | Archive | F1=0.65 | experiments/archive/2026-01-28_hypothesis_v1/ |

## Navigation

- For full decision context, see DECISION.md in each run directory
- For archived runs, see ARCHIVE_REASON.md in archive directory
- Log created automatically on first /grd:evaluate decision

---

## Integration

This template is used by `/grd:evaluate` command in Phase 4 (Decision Logging).

**Creation:**
- Created automatically when first decision is logged
- Initialized with header and table structure

**Updates:**
- Each human decision appends one row
- Order: chronological (newest at bottom)
- No deletion or modification of existing entries

**Log references run only, no bidirectional links** — per 05-CONTEXT.md decision
