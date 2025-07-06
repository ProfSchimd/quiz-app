"""Main module."""

import argparse
import json
import os.path
import pathlib
import random
import sys
from typing import Any

from . import Question as qst
from .rendering.gift_rendering import gift_render
from .rendering.html_rendering import html_render
from .rendering.json_rendering import json_render
from .rendering.latex_rendering import latex_render
from .rendering.text_rendering import text_render
from .util import get_similarity_matrix


class QuestionFilter:
    def __init__(self, args=None):
        self._hidden = False
        if args is not None:
            self._hidden = args.include_hidden

    def accepts(self, q: dict):
        is_ok = True
        # checks for the --include-hidden
        if enabled := q.get("status"):
            if enabled == "hidden":
                is_ok &= self._hidden
            elif enabled == "active":
                is_ok &= True
            else:
                is_ok &= False  # could be `return False`
        return is_ok


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate random quiz from input JSON files."
    )
    parser.add_argument(
        "--number",
        dest="n",
        type=int,
        default=-1,
        help="Number of questions, if -1 (default) use all",
    )
    parser.add_argument(
        "--input",
        nargs="+",
        dest="input",
        required=True,
        help="Space separated list of JSON file(s) with questions",
    )
    parser.add_argument(
        "--output",
        dest="output",
        default="text",
        help="Name of the output (text) file, without extension",
    )
    parser.add_argument(
        "--solution",
        dest="solution",
        default="solution",
        help="Name of the output (solution) file, without extension",
    )
    parser.add_argument(
        "--destination",
        dest="destination",
        default=".",
        help="Directory where the output files will be put",
    )
    parser.add_argument(
        "--tracks",
        dest="tracks",
        type=int,
        default=1,
        help="Number of tracks (default 1)",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        default=None,
        help="Integer value for seeding randomization (default is no seeding)",
    )
    parser.add_argument(
        "--render",
        dest="render",
        default="latex",
        help="Defines the rendering type: latex, text (default is latex)",
    )
    parser.add_argument(
        "--template", dest="template", help="Indicates the template file"
    )
    parser.add_argument(
        "--render-meta",
        dest="render_meta",
        action="store_true",
        help="If activated, renders meta information in the quiz.",
    )
    parser.add_argument(
        "--include-hidden",
        dest="include_hidden",
        action="store_true",
        help="If activated, includes questions that are hidden",
    )
    parser.add_argument(
        "--test",
        dest="test",
        type=int,
        default=0,
        help="Used for developing purpose",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        type=int,
        default=0,
        help="Indicate the verbosity level (0, 1, 2) of output (default is 0)",
    )
    return parser.parse_args()


def json_to_questions(json_file: Any) -> list:
    """Parses a JSON file into a list of question dictionaries.

    Args:
        json_file (Any): path of the JSON file (string or Path)

    Returns:
        list: The parsed JSON (a list of dictionaries if the file is well formed) 
    """
    questions = []
    if type(json_file) is str:
        json_file = pathlib.Path(json_file)
    with open(json_file.expanduser(), "r") as fp:
        questions = json.load(fp)
    return questions


def load_questions(question_files: list[str]) -> list:
    """Loads questions from file, but doesn't randomize it.

    This function contains the logic to open file(s), merge them
    (if multiple are indicated)."""
    all_questions = []
    for i, q in enumerate(question_files):
        file_questions = json_to_questions(pathlib.Path(q))
        # Check uniqueness of id's (only for information purpose)
        id_set = set()
        for question in file_questions:
            current_id = question.get("id")
            id_set.add(current_id)
            # we don't expect this to happen
            if current_id is None:
                print(f"[WARNING] Found empty id in {q}")
                current_id = random.randint(1000, 9999)
            question["id"] = f"{i}.{current_id}"
        all_questions += file_questions
        if len(id_set) < len(file_questions):
            print(f"[WARNING] There seem to be duplicated ids in {q}")
    return all_questions


def parse_question_json(json_questions: list, filter: QuestionFilter = None) -> list:
    """Returns a list of `Question` objects obtained parsing the input
    JSON applying the (optional) given filter.

    Args:
        json_questions (list): JSON with raw questions
        filter (QuestionFilter, optional): Filters to apply. Defaults to None.

    Returns:
        list: The parsed list of `Question` objects.
    """
    if filter is None:
        filter = QuestionFilter()
    return [qst.RawQuestion.from_dict(q) for q in json_questions if filter.accepts(q)]


def questions_to_json(questions: list, path: str, pretty_print=True):
    """Saves the given list of Question object into a JSON file.

    Args:
        questions (list): the list of Question objects to save
        path (str): the path of the JSON file
        pretty_print (bool, optional): If set prints in human readable format. Defaults to True.
    """
    with open(path, "w") as fp:
        indent = 4 if pretty_print else None
        json.dump([q.to_dict() for q in questions], fp, indent=indent)
        
        
def add_question_to_json(path: str, question: qst.Question, replace: bool=False):
    questions = parse_question_json(json_to_questions(path))
    # if replace, remove ALL questions with the same id as the inserted
    if replace:
        questions = [q for q in questions if q.id != question.id]
    questions.append(question)
    # print([q.id for q in questions])
    questions_to_json(questions, path, True)

def update_question_on_json(path: str, id: str, question: qst.Question, add_if_not_found=False) -> bool:
    """Updates the question with given id from the file with indicated path. The provided Question entirely replaces the one if the given id (no incremental update). It is possible to add the question anew when id is not found.

    Args:
        path (str): The path of the JSON with the questions
        id (str): id of the question to update
        question (qst.Question): the question that will replace the updated one
        add_if_not_found (bool, optional): If True, adds the given question if one with given id is not found. Defaults to False.

    Returns:
        bool: True if the operations updates or adds
    """
    questions = parse_question_json(json_to_questions(path))
    for i, q in enumerate(questions):
        if q.id == id:
            questions[i] = question
            break # substitute only the first one, if more are present
    else: # append if not found (only if set in the options)
        if add_if_not_found:
            questions.append(question)
        else:
            return False
    questions_to_json(questions, path)
    return True

def delete_from_json(path: str, id: str) -> bool:
    """Deletes the question(s) with given id from the file with indicated path. Notice that if more questions with the given id are found, they are deleted. If no questions with the given id are found, the indicated file is untouched.

    Args:
        path (str): The path of the JSON file from which delete the question.
        id (str): The id of the question to delete.

    Returns:
        bool: True if one or more questions are delete. False if no questions are delete.
    """
    questions = parse_question_json(json_to_questions(path))
    new_questions = [q for q in questions if q.id != id]
    if len(new_questions) < len(questions):
        questions_to_json(questions, path)
        return True
    return False
    

def create_quiz(questions: list, count: int, shuffle: bool = True) -> list:
    quiz = [q.to_display_question() for q in questions]
    if shuffle:
        random.shuffle(quiz)
    return quiz[:count]


def render_quiz(
    quiz: list,
    template: str,
    text: str,
    solution: str,
    track_n: int,
    render: str,
    destination: str,
):
    extensions = {
        "latex": "tex",
        "latex-exam": "exam.tex",
        "text": "txt",
        "html": "html",
        "gift": "gift",
    }
    ext = extensions.get(render, "")
    text_path: str = os.path.join(destination, f"{text}.{ext}")
    solution_path: str = os.path.join(destination, f"{solution}.{ext}")
    template: str = (
        template
        if template is not None
        else f"{os.path.dirname(__file__)}/template.{ext}"
    )

    if render.lower() == "latex":
        latex_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == "latex-exam":
        latex_render(quiz, template, text_path, solution_path, track_n, True)
    elif render.lower() == "text":
        text_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == "html":
        html_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == "json":
        json_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == "gift":
        gift_render(quiz, template, text_path)


def print_output(info: dict, verbosity: int, file: str = None):
    s = ""
    if verbosity == 0:
        return
    s += f'Input:  {len(info["files"])} file(s) {len(info["questions"])} question(s)\n'
    s += f'Seed:   {info["seed"]}\n'
    s += f'Tracks: {info["tracks"]}\n'
    s += f'Number: {info["number"]}\n'
    table = {"header": [], "weights": [], "questions": []}
    for i, quiz in enumerate(info["tests"]):
        table["header"].append(f"T{i}")
        table["weights"].append(f"W={sum([q._weight for q in quiz])}")
        table["questions"].append(
            [f"{q.id} ({q._type[0].upper()}:{q._weight})" for q in quiz]
        )
    s += "".join([f"{t:^12}" for t in table["header"]]) + "\n"
    s += "".join([f"{t:^12}" for t in table["weights"]]) + "\n"
    if verbosity > 1:
        # Print summary of questions with IDs
        for r in zip(*table["questions"]):
            s += "".join([f"{t:^12}" for t in r]) + "\n"
        # Print a similarity matrix
        matrix = get_similarity_matrix(info["tests"])
        n = len(info["tests"])
        
        s += "\n    " + "".join([f" T{i:<4} " for i in range(n)]) + "\n"
        for i in range(n):
            row = f"T{i:<3}"
            for j in range(n):
                row += f" {matrix[i][j]:^5.2} "
            s += row + "\n"
    if verbosity > 2:
        for track, quiz in enumerate(info["tests"]):
            s += f"Track {track}\n"
            for i, q in enumerate(quiz):
                s += f"Question {i} (id={q.id}): {q._type} ({q._weight}) #"
                s += " #".join(q._tags,) + "\n"
    if file:
        with open(file, "w") as f:
            f.write(s)
    else:
        print(s)


def run(args):
    # Load JSON file, filters questions, and convert to raw questions
    question_filter = QuestionFilter()
    json_questions = load_questions(args.input)
    questions = parse_question_json(json_questions, filter=question_filter)
    # Adjust the number of question in the quiz
    max_number = args.n
    if max_number < 0 or max_number > len(questions):
        max_number = len(questions)

    # We always use a seed to allow reproducibility
    if args.seed is None:
        # Convert int to string to be consistent with the seed parameter
        args.seed = str(random.randint(0, 2**30))
    random.seed(args.seed)
    
    info = {
        "files": args.input,
        "questions": questions,
        "seed": args.seed,
        "tracks": args.tracks,
        "number": max_number,
        "tests": [],
    }

    for track in range(args.tracks):
        # Create quiz
        quiz = create_quiz(questions, max_number)
        info["tests"].append(quiz)
        # File naming and rendering
        out_file = args.output
        sol_file = args.solution
        if args.tracks > 1:
            out_file += f"_{track}"
            sol_file += f"_{track}"
        render_quiz(
            quiz,
            args.template,
            out_file,
            sol_file,
            track,
            args.render,
            os.path.expanduser(args.destination),
        )

    return info


def main():
    args = parse_arguments()
    try:
        info = run(args)
    except FileNotFoundError as e:
        print(f"CRITICAL ERROR: {e} (Terminating)")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"CRITICAL ERROR (JSON): {e} (Terminating)")
        sys.exit(1)
    print_output(info, args.verbosity)


if __name__ == "__main__":
    main()
    
def dummy():
    pass
