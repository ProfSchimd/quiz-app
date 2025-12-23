# To Do
This is a list of the next tasks to perform.

- Wizard: complete the download and add permanent saving
- pyquiz: Add configuration from json --config (see output of download view)
- Wizard: The Reset button in 'files' route does nothing, implement it
- Wizard: Review layout for better sectioning and better UX
- Wizard: Add a wizard home for various tasks
- Wizard: Add optional 'description' field to QuizFile model which can then be used when displaying
- General: Create home page and add controls for all pages/routes

## What I'm doing
Currently working on completing wizard Download. We have just finished passing all options through the views chain. Next we need to properly setup saving directories and downloading.

## Improvements
This is a section that contains ideas to improve the codebase, most of this are non-functional features that could improve code, performance, or UX but don't represent new functionality.

### Wizard

#### Code refactoring
- `QuizGenWeb/views.py`: the current way in which variables are shared among views is with dictionaries created from *hidden inputs* and passed to template through contexts. A refactoring idea is to **make the whole code more manageable by defining a common dictionary with the names of the keys used** (for example `tracks`, `seed`, `render`). Doing thus would allow easy update of variables and better readability of code.