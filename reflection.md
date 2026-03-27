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

-----

I changed alot of things when it came to the class names I realized pretty early on the the names of each class should be way less complicated then I made it, as the responsibility needed to be clearer to avoid confusion later on.

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

time budget (available_hours), priority (HIGH/MEDIUM/LOW), and duration (duration_minutes)

- How did you decide which constraints mattered most?

2a. How did I decide which contraints mattered most? I looked at edgecases, we cant have negative time or complicated ways of telling time for user friendliness. and the priority should have purpose unlike what it was like before, where it didn't affect placement on the list and schedule ranking. I used the time object instead of asking users to type strings. Then for priority I actually wanted it to affect scheduling as the original skeleton just had the label with no actual impact. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The scheduler takes priority task first and fulls the day until the users time budget dies. If that happens high priority task can fully push medium level task into the background, Even if the multiple shorter task had for value as a whole if put together
- Why is that tradeoff reasonable for this scenario?
Its a reasonable tradeoff because pet care task arent fully interchangable. Something like a vet trip SHOULD def be put ahead of multiple walks or a bath thrown in yk. Its more important that the priority reflects reality in a way.

---

## 3. AI Collaboration

**a. How you used AI**

- 

design and brainstorming was a huge part of my use of AI. Many errors I ran into I also used AI to help me debug and there were so many bugs I ran into as well. The most helpful use was helping me with OOP and making everything organized.
- What kinds of prompts or questions were most helpful?

"Help me understand these functions that I know I need but don't fully understand implimentation in unison with the made-up methods." 

"How can I improve mt structure"

"Where is this bug occuring"

"test..."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

I did not accept when AI wanted to add things that I did not plan for in the project such as a history chart..

- How did you evaluate or verify what the AI suggested?

I would use my own knowledge and read the code line by line or use google to back up Ai's fixes.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

Marking a task complete flips its status
Adding a task to a pet grows the task list
A task with zero duration raises an error (edge case validation)
Tasks that exceed the owner's available hours go to overflow instead of being silently dropped
An empty pet generates an empty schedule without crashing
Tasks sort in HIGH → MEDIUM → LOW order
Scheduled tasks display in chronological time order
Overlapping task windows get flagged as conflicts
Sequential non-overlapping tasks produce no false conflicts
Two tasks at the exact same start time are caught as a conflict
A daily recurring task generates a next occurrence due the following day
Completing a recurring task creates a fresh pending instance for the next day
A non-recurring task returns nothing when asked for a next occurrence

- Why were these tests important?

he most important ones are overflow, conflict detection, and recurring tasks which those are the core behaviors. If any of those silently broke, the owner would get a wrong schedule with no warning. Testing edge cases like zero duration and empty pets made sure the app doesn't crash on bad input.

**b. Confidence**

- How confident are you that your scheduler works correctly?

8/10. It handles well but im learning that there will always be bugs and I can't aim for perfection here.

- What edge cases would you test next if you had more time?

I would test if there is a limit to adding task because I have to assume a user would try to add 1Billion task just to break the app.
---

## 5. Reflection

**a. What went well**

- I learned so much, it went well during the structuring the most and I learned to much about the app development process.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the base, and try to account for more issues that came up later such as duplications which I believe I fixed with implimenting a history tab alot earlier in the development cycle.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

AI can either be your greatest friend or greatest foe
