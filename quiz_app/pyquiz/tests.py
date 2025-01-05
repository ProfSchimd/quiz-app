from pathlib import Path
import tempfile
import unittest

from . import pyquiz

class PyquizTest(unittest.TestCase):
        
    def test_json_to_questions(self):
        with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
            fp.write(raw_json.encode("utf-8"))
            fp.close()
            questions = pyquiz.json_to_questions(fp.name)
            n_single = len([q for q in questions if q["type"] == "single"])
            self.assertEqual(len(questions), 7, "Incorrect question count")
            self.assertEqual(
                n_single,
                4,
                "Incorrect total questions of type 'single'"
            )
            
            questions_path = pyquiz.json_to_questions(Path(fp.name))
            self.assertEqual(
                str(questions),
                str(questions_path),
                "Unmatched loads from str and Path"
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
                    len(questions),
                    9,
                    "Incorrect total question count")
                self.assertEqual(
                    len([q for q in questions if q["type"] == "fill"]), 
                    3,
                    "Incorrect total questions of type 'fill'"
                )


class RenderTest(unittest.TestCase):
    pass


class QuestionTest(unittest.TestCase):
    pass


raw_json="""[
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