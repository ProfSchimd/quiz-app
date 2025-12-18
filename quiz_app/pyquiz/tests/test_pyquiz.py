import json
import os
from pathlib import Path
import tempfile
import unittest


import pyquiz.pyquiz as pyquiz
import pyquiz.Question as qst
import pyquiz.util as util


class PyquizTest(unittest.TestCase):
    def test_json_to_questions(self):
        with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
            fp.write(raw_json.encode("utf-8"))
            fp.close()
            questions = pyquiz.json_to_questions(fp.name)
            n_single = len([q for q in questions if q["type"] == "single"])
            self.assertEqual(len(questions), 7, "Incorrect question count")
            self.assertEqual(
                n_single, 4, "Incorrect total questions of type 'single'"
            )

            questions_path = pyquiz.json_to_questions(Path(fp.name))
            self.assertEqual(
                str(questions),
                str(questions_path),
                "Unmatched loads from str and Path",
            )

    def test_load_questions(self):
        with tempfile.NamedTemporaryFile(delete_on_close=False) as fp1:
            with tempfile.NamedTemporaryFile(delete_on_close=False) as fp2:
                fp1.write(raw_json.encode("utf-8"))
                fp2.write(raw_json_2.encode("utf-8"))
                fp1.close()
                fp2.close()

                questions = pyquiz.load_questions([fp1.name, fp2.name])
                self.assertEqual(
                    len(questions), 9, "Incorrect total question count"
                )
                self.assertEqual(
                    len([q for q in questions if q["type"] == "fill"]),
                    3,
                    "Incorrect total questions of type 'fill'",
                )
                
    def test_parse_question_json(self):
        questions = pyquiz.parse_question_json(json.loads(raw_json))
        ids = [q.id for q in questions]
        self.assertEqual(
            len(questions),
            7,
            "Wrong number of questions list."
        )
        self.assertIn("001", ids, "Expected id not present")
        self.assertNotIn("123", ids, "Unexpected question id")
        
    def test_question_to_json(self):
        raw = json.loads(raw_json)
        questions = [
            qst.RawQuestion.from_dict(raw[0]).to_display_question(),
            qst.RawQuestion.from_dict(raw[1]).to_display_question(),
            qst.RawQuestion.from_dict(raw[2]).to_display_question(),
        ]
        _, path = tempfile.mkstemp()
        pyquiz.questions_to_json(questions, path)
        with open(path) as fp:
            loaded = json.load(fp)
        os.remove(path)
        
        self.assertEqual(
            set([q["id"] for q in loaded]),
            set(q.id for q in questions),
            "Set of id don't match",
        )
            
    def test_add_question(self):
        _, path = tempfile.mkstemp()
        original = json.loads(raw_json)
        with open(path, "w") as fp:
            fp.write(raw_json)
        
        pyquiz.add_question_to_json(path, extra_q_1)
        with open(path) as fp:
            loaded = json.load(fp)
        os.remove(path)
        
        
        self.assertEqual(
            set([q["id"] for q in original]) | {extra_q_1.id},
            set([q["id"] for q in loaded]),
            "Set of id's don't match"
        )
        
        self.assertIn(
            extra_q_1.to_dict(),
            loaded,
            "Can't find whole added element"
        )
        
    def test_add_with_replace(self):
        _, path = tempfile.mkstemp()
        original = json.loads(raw_json)
        with open(path, "w") as fp:
            fp.write(raw_json)
        pyquiz.add_question_to_json(path, extra_q_2, True)
        with open(path) as fp:
            loaded = json.load(fp)
        os.remove(path)
        self.assertEqual(
            set([q["id"] for q in original]),
            set([q["id"] for q in loaded]),
            "Id sets don't correspond"
        )

    def test_update_question(self):
        _, path = tempfile.mkstemp()
        old_q = json.loads(raw_json_2)
        with open(path, "w") as fp:
            json.dump(old_q, fp)
        # create the updated version
        new_q = qst.RawQuestion.from_dict(old_q[1])
        new_q._text = "This is a brand new text for the question!"
        # call update
        pyquiz.update_question_on_json(path, new_q.id, new_q)
        with open(path) as fp:
            loaded = json.load(fp)
        os.remove(path)
        
        inserted = next((d for d in loaded if d.get("id") == new_q.id), None)
        self.assertIsNotNone(inserted, "Couldn't find updated id")
        # verify correct update
        self.assertEqual(
            inserted["text"],
            new_q._text,
            "Didn't update 'text' field."
        )
        
        # verify id set is not changed
        self.assertEqual(
            set([q["id"] for q in old_q]),
            set([q["id"] for q in loaded]),
            "Sets of id don't match"
        )

    def test_delete_question(self):
        _, path = tempfile.mkstemp()
        old_q = json.loads(raw_json_2)
        with open(path, "w") as fp:
            json.dump(old_q, fp)
        removed_id = old_q[-1]["id"]
        pyquiz.delete_from_json(path, removed_id)
        with open(path) as fp:
            loaded = json.load(fp)
        self.assertNotIn(
            old_q[-1],
            loaded,
            "Question not deleted",
        )    
        os.remove(path)



class RenderTest(unittest.TestCase):
    pass


class QuestionTest(unittest.TestCase):
    pass


class UtilTest(unittest.TestCase):
    def test_block_code(self):
        self.assertTrue(
            util.is_code_block("<code>This is code</code>"),
            "Unidentified code block",
        )
        self.assertFalse(
            util.is_code_block("Not code <code>a</code>"),
            "Identified non-code block",
        )

    def test_similarity_matrix(self):
        one = qst.Question("001", "Text1", 1, ["A"])
        two = qst.Question("002", "Text11", 1, ["B"])
        three = qst.Question("003", "text111", 1, ["C"])

        list = [[one, two], [two, three], [one, two]]

        matrix = util.get_similarity_matrix(list)
        for i in range(2):
            self.assertEqual(matrix[i][i], 1, "Diagonal values are not 1")
        self.assertEqual(
            matrix[0][1], matrix[1][0], "Asymmetric matrix (0,1)!=(1,0)"
        )

extra_q_1 = qst.RawChoiceQuestion.from_dict({
    "id": "101",
    "type": "single",
    "text": "This is a test question",
    "options": ["One", "Two", "Three"],
    "correct": [0,1,0],
    "weight": 1,
    "tags": ["Test"],
})

extra_q_2 = qst.RawChoiceQuestion.from_dict({
    "id": "001",
    "type": "single",
    "text": "This is a test question",
    "options": ["One", "Two", "Three"],
    "correct": [0,1,0],
    "weight": 1,
    "tags": ["Test"],
})

raw_json = """[
    {
        "id": "001",
        "type": "single",
        "text": "In Python come si accede ai parametri della linea di comando?",
        "options": [
            "Variabile globale <code>argv</code>",
            "Dal modulo <code>main</code> con <code>main.argv</code>",
            "Con un parametro del <code>main</code>",
            "Dal modulo <code>sys</code> con <code>sys.argv</code>"
        ],
        "correct": [
            0,
            0,
            0,
            1
        ],
        "weight": 2
    },
    {
        "id": "002",
        "type": "single",
        "text": "Quale è la prima istruzione eseguita da un programma Python?",
        "options": [
            "La prima istruzione della prima funzione definita nel file <code>.py</code> invocato",
            "La prima istruzione della funzione main presente nel file <code>.py</code> invocato.",
            "La prima istruzione presente nel file <code>.py</code> invocato con il comando <code>python</code>",
            "La prima istruzione del metodo <code>main</code> della classe presente nel file <code>.py</code> invocato"
        ],
        "correct": [
            0,
            0,
            1,
            0
        ],
        "review": [
            "No",
            "No",
            "Si",
            "No"
        ],
        "weight": 1
    },
    {
        "id": "003",
        "type": "single",
        "text": "Quale è la lista degli argomenti per il comando <code>python programma.py Via Roma 33</code>?",
        "options": [
            "<code>['programma.py', 'Via', 'Roma', '33']</code>",
            "<code>[Via', 'Roma', '33']</code>",
            "<code>['programma.py', 'Via Roma', '33']</code>",
            "<code>['programma.py', 'Via Roma 33']</code>"
        ],
        "correct": [
            1,
            0,
            0,
            0
        ],
        "weight": 2
    },
    {
        "id": "004",
        "type": "single",
        "text": "Qual'è l'istruzione Python per stampare sulla console?",
        "options": [
            "<code>System.out.println</code>",
            "<code>cout</code>",
            "<code>print</code>",
            "<code>console.log</code>"
        ],
        "correct": [
            0,
            0,
            1,
            0
        ],
        "weight": 1
    },
    {
        "id": "005",
        "type": "invertible",
        "text": [
            "Indica quali operatori sono presenti in Python",
            "Indica quali operatori <u>non</u> sono presenti in Python"
        ],
        "options": [
            "Somma <code>+</code>",
            "Inverso <code>|</code>",
            "Prodotto <code>*</code>",
            "Divisone intera <code>//</code>"
        ],
        "correct": [
            1,
            0,
            1,
            1
        ],
        "weight": 2
    },
    {
        "id": "008",
        "type": "fill",
        "text": "Completa l'istruzione per stampare a video la stringa <code>Ciao</code>",
        "tofill": "{{0}}<code>('Ciao')</code>", 
        "correct": [
            "print"
        ],
        "weight": 1
    },
    {
        "id": "009",
        "type": "fill",
        "text": "Complete",
        "tofill": "<code>[i*i {{0}} i in range(10)]</code>",
        "correct": [
            "for"
        ],
        "weight": 1
    }

]"""

raw_json_2 = """[
    {
        "id": "006",
        "type": "multiple",
        "text": "Indica quale delle seguenti variabili è di tipo <code>float</code>.",
        "options": [
            "<code>a = 3</code>",
            "<code>a = 3.5</code>",
            "<code>a = 7 / 2</code>",
            "<code>a = float(3)</code>",
            "<code>a = 7 // 2</code>",
            "<code>a = 3 + 2.5</code>"
        ],
        "correct": [
            0,
            1,
            1,
            1,
            0,
            1
        ],
        "weight": 3
    },
    {
    	"id": "007",
    	"type": "fill",
    	"text": "Completa il seguente frammento di codice in modo che compili e non generi errori runtime",
    	"tofill": "<code>class Persona {<br>  String nome;<br>  String cognome;<br>  {{0}} lavoro;<br>  Persona({{1}}, {{2}}); // inizializza nome e cognome<br>}</code>",
    	"correct": [
    		"String?",
			"required String nome",
			"required String cognome"
    	],
    	"weight": 1
    }
]"""
