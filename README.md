# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Smarter Scheduling

The following features were added beyond the base requirements:

- **Sort by time** — the generated schedule displays tasks in chronological order, with flexible (no fixed time) tasks placed at the end
- **Filter by status** — tasks can be filtered by `pending`, `complete`, or `overdue` in both the UI and backend
- **Recurring tasks** — tasks can repeat `daily` or `weekly`; marking one complete automatically creates a new instance for the next occurrence
- **Same-pet conflict detection** — the scheduler checks for overlapping time windows within a single pet's schedule and reports warnings
- **Cross-pet conflict detection** — `Schedule.check_cross_pet_conflicts()` catches cases where tasks for different pets are scheduled at the same time, flagging that the owner can't be in two places at once

## Testing PawPal+

### Run the tests

```bash
python3 -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | What it verifies |
|---|---|
| `test_mark_complete` | Task status flips from pending to complete |
| `test_add_task` | Pet task list grows when a task is added |
| `test_invalid_duration_raises` | `duration_minutes=0` raises a `ValueError` |
| `test_schedule_overflow` | Tasks that exceed available hours go to `overflow_tasks` |
| `test_schedule_no_tasks` | Empty pet produces an empty schedule without crashing |
| `test_priority_sort_order` | Tasks are ordered HIGH → MEDIUM → LOW |
| `test_sort_scheduled_by_time` | Scheduled tasks appear in chronological time order |
| `test_conflict_detection` | Overlapping task windows are flagged as conflicts |
| `test_no_conflict_non_overlapping` | Sequential tasks produce no conflicts |
| `test_conflict_same_start_time` | Two tasks at the exact same time are flagged |
| `test_recurring_next_occurrence` | A DAILY task produces a next occurrence due the following day |
| `test_mark_complete_daily_creates_next_task` | Completing a recurring task creates a fresh task for the next day |
| `test_non_recurring_no_next` | A non-recurring task returns `None` for next occurrence |

### Confidence level

★★★★☆ (4/5)

Core scheduling logic — priority sorting, overflow handling, conflict detection, and recurring tasks — is fully tested and passing across 13 tests. Confidence is not a 5 because cross-pet conflict detection and the Streamlit UI layer are not covered by automated tests, and timezone edge cases in `is_overdue()` are noted but untested.

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
