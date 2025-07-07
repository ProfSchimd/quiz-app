import unittest

import pyquiz.Question as qst
import pyquiz.rendering.latex_rendering as latex

class RendererTest(unittest.TestCase):
    def test_latex_ordered_list_render(self):
        t,_ = latex.latex_render_strings([q_fill_ol], None,1,False)
        self.assertIn("\\begin{enumerate}", t, "Can't find start of enumerate")
        self.assertIn("\\end{enumerate}", t, "Can't find end of enumerate")
        self.assertEqual(t.count("\\item"), 3, "Unmatched number of list items")
    
    def test_latex_exam_ordered_list_render(self):
        t,_ = latex.latex_render_strings([q_fill_ol], None,1,True)
        self.assertIn("\\begin{enumerate}", t, "Can't find start of enumerate")
        self.assertIn("\\end{enumerate}", t, "Can't find end of enumerate")
        self.assertEqual(t.count("\\item"), 3, "Unmatched number of list items")
    
    
q_fill_ol = qst.RawFillQuestion.from_dict({
    "id": "011",
    "type": "fill",
    "text": "Complete.<br>",
    "tofill": "Do<ol><li>1 {{0}}</li><li>Two {{1}}</li><li>Thr33 {{2}</li></ol>Suffix",
    "correct": ["A", "b", "C"],
    "weight": 3,
    "tags": ["Test", "Fill", "ol"]
        
})