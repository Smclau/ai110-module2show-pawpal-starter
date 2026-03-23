# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

I will create three classes: walkSchedule, dailyTask, and addPet
Under each function I will create the logic behind implementing each task so that the UI reflects my UX vision.

- What classes did you include, and what responsibilities did you assign to each?

Pet, Task, and Planner

Pet: Name of the Pet, Type of Pet (Dog or Cat).
Possible Attributes: pet_name, pet_type, pet_age (maybe?)
Possible Methods: add_task(task), rmv_task(task_name), get_pet_info(), show_tasks()

Task: Will cover things such as feeding times, bathing times, play times, walk times, and lights out times. Will be responsible for allowing the user to enter data such as when their dog needs to do on their morning, afternoon or evening walks and the average time they typically potty.
Possible Attributes: task_name("feed", "walk", "bath"), time, duration, due, complete
Possible Methods: mark_complete(), edit_time(new_time), edit_priority(new_priority), display_task()

Schedule: Responsible for organizing and generating a daily plan based on a pet’s tasks, priorities, and available time.
Possible Attributes: pet, task, available_time, morning_walk, afternoon_walk, evening_walk
Possible Methods: generate_schedule(), sort_task_by_priority(), check_conflicts(), show_schedule()

**b. Design changes**

- Did your design change during implementation?

Yes

- If yes, describe at least one change and why you made it.

Renamed Task.duration to Task.duration_minutes
   - duration had no unit — could be minutes or hours, causing silent calculation errors
   - duration_minutes makes the unit explicit and prevents Owner.available_hours mismatches

Created an Owner Class as well when I originally was going to only have 3 classes instead of four.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
