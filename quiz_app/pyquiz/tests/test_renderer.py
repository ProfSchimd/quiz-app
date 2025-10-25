import unittest

import pyquiz.Question as qst
import pyquiz.rendering.latex_rendering as latex
import pyquiz.rendering.html_rendering as html

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

class TestHtmlRenderFigures(unittest.TestCase):
    """Test suite for html_render_figures function."""
    
    def test_html_render_figures_empty(self):
        """Test that empty list returns empty string."""
        result = html.html_render_figures([])
        self.assertEqual(result, "")
        
    def test_html_render_figures_single_with_caption(self):
        """Test rendering a single figure with caption."""
        figures = [qst.Figure(url='https://example.com/img.png', caption='Test caption')]
        result = html.html_render_figures(figures)
        
        self.assertIn('<div class="figure">', result)
        self.assertIn('<img src="https://example.com/img.png"', result)
        self.assertIn('Test caption', result)
        self.assertIn('</div>', result)

    def test_html_render_figures_single_no_caption(self):
        """Test rendering a figure without caption."""
        figures = [qst.Figure(url='https://example.com/img.png', caption='')]
        result = html.html_render_figures(figures)
        
        self.assertIn('<img src="https://example.com/img.png"', result)
        # Caption paragraph should still exist but be empty or not rendered
        self.assertIn('<div class="figure">', result)
        
    def test_html_render_multiple_figures(self):
        """Test rendering multiple figures."""
        figures = [
            qst.Figure(url='https://example.com/img1.png', caption='Figure 1'),
            qst.Figure(url='https://example.com/img2.png', caption='Figure 2'),
            qst.Figure(url='https://example.com/img3.png', caption='Figure 3')
        ]
        result = html.html_render_figures(figures)
        
        # Check all figures are present
        self.assertIn('img1.png', result)
        self.assertIn('img2.png', result)
        self.assertIn('img3.png', result)
        self.assertIn('Figure 1', result)
        self.assertIn('Figure 2', result)
        self.assertIn('Figure 3', result)
        
        # Count number of figure divs
        self.assertEqual(result.count('<div class="figure">'), 3)