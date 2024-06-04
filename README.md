# QuizApp
A simple App to support teaching with instant quiz creation, share, and feedback.

## Routes
The following routes are fully or partially implemented
* `/` Home page: still basic needs menu and summary information (or dashboard)
* `/tag/new` Creates new tag needs 
* `/subject/new`
* `/question/show/<int>`
* `/question/show`
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