# QuizApp
A simple App to support teaching with instant quiz creation, share, and feedback.

## Routes
The following routes are fully or partially implemented
* `/` Home page: still basic needs menu and summary information (or dashboard)
* `/tag/new` Creates new tag 
* `/subject/new` Creates new subject
* `/question/show/<int>`Shows the question with the given `<int>` id. Needs to work on *not found* id. The *Submit* button must be properly managed: hidden if not needed and correctly behaving when present.
* `/question/show` Shows all questions allowing the creation of a JSON file from select ones.
* `/question/export`
* `/question/new`
* `/question/upload`
* `/question/upload/confirm`
* `/collection/from_questions`
* `/collection/<int>`


## Roadmap
See [detailed plan below](#detailed-plan) for more information.

1. Take assignment with submit (NTH save and timer)
2. Summary statistics on answers, for a given assignment
3. Automatic feedback
4. Add question with permissions constraints
5. Add collection with permissions constraints
   - Collection from JSON file
6. Add assignment with permissions constraints

Notice that those views that are available in the Django admin site have lower priority since we can temporarily use the default provided ones.


## Detailed Plan

### `QUESTION.ADD`
Implementation of the UI for the insertion of a new Question
1. Implement the view
   - Tags should be suggested from existing ones or added when not present
   - Subject must be inserted before hand
2. Add the content to the DB

Pre-requisites:
* Tags and subjects