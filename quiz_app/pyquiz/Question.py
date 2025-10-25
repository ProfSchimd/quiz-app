import random


class Figure:
    """Represents a figure with URL and caption."""

    def __init__(self, url, caption=""):
        self.url = url
        self.caption = caption

    def to_dict(self):
        return {"url": self.url, "caption": self.caption}

    @classmethod
    def from_dict(cls, d):
        return cls(d.get("url", ""), d.get("caption", ""))


"""Module containing all Question classes."""


class Question:
    """Contains basic feature of a Question."""

    def __init__(self, id, text, weight, tags=None, figures=None):
        """Initialize Question.

        Args:
            id: Unique question identifier
            text: Question text (may contain variants)
            weight: Point value for scoring
            tags: Optional list of category tags
            figures: Optional list of Figure objects
        """
        self.id = id
        self._text = text
        self._weight = weight
        self._tags = tags if tags is not None else []
        self._figures = figures if figures is not None else []
        self._type = "undefined"

    def __str__(self):
        return f"ID: {self.id} (W: {self._weight})"

    def to_dict(self):
        return {
            "id": self.id,
            "type": self._type,
            "text": self._text,
            "weight": self._weight,
            "tags": self._tags,
            "figures": [fig.to_dict() for fig in self._figures],
        }


class DisplayQuestion(Question):
    """DisplayQuestion are those rendered."""

    def to_dict(self):
        d = super().to_dict()
        d.update(
            {
                "options": self._options,
                "correct": self._correct,
            }
        )
        return d


class CheckboxQuestion(DisplayQuestion):
    def __init__(
        self,
        id,
        text,
        weight,
        options=[],
        correct=[],
        type=None,
        tags=None,
        figures=None,
    ):
        super().__init__(id, text, weight, tags, figures)
        self._options = options
        self._correct = correct
        if type is not None:
            self._type = "single" if type == "single" else "multiple"


class FillQuestion(DisplayQuestion):
    def __init__(
        self, id, text, to_fill, weight, correct=[], type=None, tags=None, figures=None
    ):
        super().__init__(id, text, weight, tags, figures)
        self._correct = correct
        self._to_fill = to_fill
        if type is not None:
            self._type = type


class OpenQuestion(DisplayQuestion):
    def __init__(self, id, text, weight, type=None, figures=None):
        super().__init__(id, text, weight, figures=figures)
        if type is not None:
            self._type = type


class ExerciseQuestion(DisplayQuestion):
    def __init__(self, id, text, weight, sub_questions, type=None, figures=None):
        super().__init__(id, text, weight, figures=figures)
        if type is not None:
            self._type = type
        self._sub_questions = sub_questions


class CompositeQuestion(DisplayQuestion):
    def __init__(self, id, text, weight, questions, type=None, figures=None):
        super().__init__(id, text, weight, figures=figures)
        self._questions = questions
        self._type = type if type else self._type


# Raw classes below


class RawQuestion(Question):
    """Represents (meta) questions before instantiation randomization and substitution."""

    def __init__(self, id, text, weight, figures=None):
        """Initialize RawQuestion."""
        super().__init__(id, text, weight, figures=figures)

    def to_display_question(self):
        return DisplayQuestion(self.id, self._text, self._weight, figures=self._figures)

    def __str__(self):
        return f"[{self.id}] ({self._type} {self.__class__.__name__})"

    @classmethod
    def from_dict(cls, d):
        if d["type"] in ["single", "multiple", "invertible", "multi-variate"]:
            return RawChoiceQuestion.from_dict(d)
        elif d["type"] == "fill":
            return RawFillQuestion.from_dict(d)
        elif d["type"] == "open":
            return RawOpenQuestion.from_dict(d)
        elif d["type"] == "exercise":
            return RawExerciseQuestion.from_dict(d)
        elif d["type"] == "composite":
            return RawCompositeQuestion.from_dict(d)

        figures = parse_figures(d.get("figures", []))

        return cls(d["id"], d["text"], d.get("weight"), figures=figures)


class RawChoiceQuestion(RawQuestion):
    def __init__(
        self, id, text, weight, options, correct, type="single", tags=None, figures=None
    ):
        super().__init__(id, text, weight, figures=figures)
        self._options = options
        self._correct = correct
        self._type = type
        if tags is not None:
            self._tags = tags

    def to_dict(self):
        d = super().to_dict()
        d["type"] = self._type  # not sure if super().to_dict() chooses the correct one
        d["options"] = self._options
        d["correct"] = self._correct
        
        return d

    def to_display_question(self):
        text = None
        # Choose between versions (single -> 1, multiple -> 1, invertible -> 2, ...)
        variant = random.randint(0, len(self._text) - 1)
        text = self._text[variant]
        n = len(self._options)
        # randomize options and correct
        indexes = list(range(n))
        random.shuffle(indexes)
        options = [self._options[i] for i in indexes]
        correct = [self._correct[variant][i] for i in indexes]
        return CheckboxQuestion(
            self.id,
            text,
            self._weight,
            options,
            correct,
            self._type,
            self._tags,
            self._figures,
        )

    @classmethod
    def from_dict(cls, d):
        """Construct RawChoiceQuestion from a dictionary.

        The dictionary should have the exact same structure as the JSON file."""
        text = None
        correct = None
        if d["type"] == "single" or d["type"] == "multiple":
            text = [d["text"]]
            correct = [d["correct"]]
        elif d["type"] == "invertible":
            text = d["text"]
            correct = [d["correct"], [1 - x for x in d["correct"]]]
        elif d["type"] == "multi-variate":
            text = d["text"]
            correct = d["correct"]
        figures = parse_figures(d.get("figures", []))
        return cls(
            d["id"],
            text,
            d.get("weight"),
            d["options"],
            correct,
            type=d["type"],
            tags=d.get("tags"),
            figures=figures,
        )


class RawFillQuestion(RawQuestion):
    def __init__(
        self, id, text, weight, to_fill, correct, type, tags=None, figures=None
    ):
        super().__init__(id, text, weight, figures=figures)
        self._to_fill = to_fill
        self._correct = correct
        self._type = type
        if tags is not None:
            self._tags = tags

    def to_dict(self):
        d = super().to_dict()
        d["type"] = self._type
        d["tofill"] = self._to_fill
        d["correct"] = self._correct
        return d

    def to_display_question(self):
        return FillQuestion(
            self.id,
            self._text,
            self._to_fill,
            self._weight,
            self._correct,
            self._type,
            self._tags,
            self._figures,
        )

    @classmethod
    def from_dict(cls, d):
        figures = parse_figures(d.get("figures", []))
        return cls(
            d["id"],
            d["text"],
            d.get("weight"),
            d["tofill"],
            d["correct"],
            d["type"],
            tags=d.get("tags"),
            figures=figures,
        )


class RawOpenQuestion(RawQuestion):
    def __init__(self, id, text, weight, variants, type, figures=None):
        super().__init__(id, text, weight, figures=figures)
        self._variants = variants
        self._type = type

    def to_dict(self):
        d = super().to_dict()
        d["type"] = self._type
        d["variants"] = self._variants
        return d

    def to_display_question(self):
        text = fill_alternative(self._text, self._variants)
        return OpenQuestion(self.id, text, self._weight, self._type, self._figures)

    @classmethod
    def from_dict(cls, d):
        figures = parse_figures(d.get("figures", []))
        return cls(
            d["id"],
            d["text"],
            d.get("weight"),
            d["variants"],
            d["type"],
            figures=figures,
        )


class RawExerciseQuestion(RawQuestion):
    """An exercise is a text followed by several questions."""

    def __init__(
        self, id, text, weight, text_variants, sub_questions, type, figures=None
    ):
        super().__init__(id, text, weight, figures=figures)
        self._type = type
        self._text_variants = text_variants
        self._sub_questions = sub_questions

    def to_dict(self):
        d = super().to_dict()
        d["type"] = self._type
        d["text-variants"] = self._text_variants
        d["sub-questions"] = [sub_q.to_dict() for sub_q in self._sub_questions]
        return d

    def to_display_question(self):
        text = fill_alternative(self._text, self._text_variants)
        n_sub = len(self._sub_questions)
        sub_questions = []
        for i in range(n_sub):
            sub_questions.append(
                fill_alternative(
                    self._sub_questions[i]["question"],
                    self._sub_questions[i]["variants"],
                )
            )

        return ExerciseQuestion(
            self.id,
            text,
            self._weight,
            sub_questions,
            type=self._type,
            figures=self._figures,
        )

    @classmethod
    def from_dict(cls, d):
        figures = parse_figures(d.get("figure", []))
        return cls(
            d["id"],
            d["text"],
            d.get("weight"),
            d["text-variants"],
            d["sub-questions"],
            d["type"],
            figures=figures,
        )


class RawCompositeQuestion(RawQuestion):
    """A composite is essentially a list of questions."""

    def __init__(self, id, text, weight, questions, type, figures=None):
        super().__init__(id, text, weight)
        self._type = type
        self._questions = questions

    def to_display_question(self):
        questions = [q.to_display_question() for q in self._questions]
        return CompositeQuestion(
            self.id, self._text, self._weight, questions, type=self._type, figures=self._figures
        )

    @classmethod
    def from_dict(cls, d):
        questions = [RawQuestion.from_dict(q) for q in d["questions"]]
        figures = parse_figures(d.get("figures", []))
        return cls(d["id"], d["text"], d.get("weight"), questions, d["type"], figures=figures)


# Next are util functions


def fill_alternative(template, variants):
    n_variants = len(variants)
    for i in range(n_variants):
        n_opts = len(variants[i])
        choice = random.randint(0, n_opts - 1)
        selected = variants[i][choice]
        template = template.replace(f"{{{{{i}}}}}", selected)
    return template


def parse_figures(figures_data):
    """Helper function to parse figures from dictionary data.

    Args:
        figures_data: List of dicts with 'url' and 'caption' keys

    Returns:
        List of Figure objects
    """
    if not figures_data:
        return []
    return [Figure.from_dict(fig) for fig in figures_data]
