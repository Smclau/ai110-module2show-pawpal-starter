# PawPal+

PawPal+ is a Streamlit app that helps pet owners plan and track daily care tasks for their pets. Enter your availability, build a task list, and generate a prioritized schedule — with automatic conflict detection and recurring task support.

---

## Features

### Owner & Pet Profiles
- Set your name and daily available hours
- Register a pet with name, species, and age
- Reset the profile at any time with the Create Profile button

### Task Management
- Add tasks with a title, duration, priority, scheduled time, and repeat frequency
- Filter tasks by status: `all`, `pending`, `complete`, or `overdue`
- Remove any task from the list
- Mark tasks complete — recurring tasks automatically generate the next occurrence

### Smart Scheduling
- **Priority sorting** — tasks are scheduled highest priority first; ties are broken by shortest duration so more tasks fit in the day
- **Sort by time** — the generated schedule displays tasks in chronological order; flexible tasks (no fixed time) appear at the end
- **Time budget enforcement** — tasks that exceed available hours are moved to an overflow list instead of being silently dropped
- **Overdue detection** — tasks past their due date are flagged with a warning banner

### Recurring Tasks
- Tasks can repeat `daily` or `weekly`
- Marking a recurring task complete automatically creates a fresh pending instance for the next occurrence
- Non-recurring tasks are completed once and stay in history

### Conflict Detection
- **Same-pet conflicts** — flags any two tasks whose time windows overlap within one pet's schedule
- **Cross-pet conflicts** — detects cases where tasks for different pets are scheduled at the same time, catching situations where the owner can't be in two places at once
- Conflict warnings appear above the schedule table as `st.warning` banners

---

## 📸 Demo

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Run the tests

```bash
python3 -m pytest tests/test_pawpal.py -v
```

---

## Tests

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

**Confidence: ★★★★☆ (4/5)**

Core scheduling logic is fully tested across 13 tests. Cross-pet conflict detection and the Streamlit UI layer are not covered by automated tests, and timezone edge cases in `is_overdue()` are noted but untested.

---

## Project Structure

```
pawpal_systems.py   — backend classes (Task, Pet, Owner, Schedule)
app.py              — Streamlit UI
main.py             — standalone demo/test script
tests/              — pytest test suite
reflection.md       — project reflection
uml_final.png       — final UML class diagram
```
