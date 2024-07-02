from .. import util

# TODO: In order to add 'exam' class support we need to make some changes to the code.
# - Add 'use_exam_class' flag that distinguished "standard" LaTeX and 'exam' class
# - Template file for 'exam' class
# - Switch from \section to \question using points
# - Replace the multiple choice rendering: (i) itemize becomes (ii) use \choice and \CorrectChoice
# - Replace fill rendering to use \fillin
# - Implement solution with \printsolutions toggled
# - Review the general layout of the resulting file
# 

fill_placeholder = ".................."


def question_header(i: int, header_text: str="Domanda") -> str:
    return f'\n\\subsection*{{{header_text} {i}}}\n'


def html_to_latex(s: str) -> str:
    s = s.replace('</code>', '}')
    s = s.replace('<code>', '\\texttt{')
    s = s.replace('<br>', '\\\\')
    s = s.replace('</strong>', '}')
    s = s.replace('<strong>', '\\textbf{')
    s = s.replace('</b>', '}')
    s = s.replace('<b>', '\\textbf{')
    s = s.replace('</u>', '}')
    s = s.replace('<u>', '\\underline{')
    s = s.replace('</i>', '}')
    s = s.replace('<i>', '\\emph{')
    s = s.replace('</ul>', '\\end{itemize}\n')
    s = s.replace('<ul>', '\n\\begin{itemize}')
    s = s.replace('</li>', '\n')
    s = s.replace('<li>', '  \\item ')
    return s


def latex_render_choices(q):
    text = q._text
    options = q._options
    correct = q._correct
	
    content_text = f'{html_to_latex(text)}\n\\begin{{itemize}}\n'
    content_solution = f'{html_to_latex(text)}\n\\begin{{itemize}}\n'
    for j, o in enumerate(options):
        content_text += f'  \\item[$\\square$] {html_to_latex(o)}\n'
        mark = '$\\square$'
        if correct[j] == 1:
            mark = '$\\checkmark$'
        content_solution += f'  \\item[{mark}] {html_to_latex(o)}\n'

    content_text += '\\end{itemize}\n'
    content_solution += '\\end{itemize}\n'
    return content_text, content_solution


def latex_render_fill(q):
    content_text = f'{html_to_latex(q._text)}\n\n\\noindent\n'
    content_solution = f'{html_to_latex(q._text)}\n\n\\noindent\n'
    to_fill = html_to_latex(q._to_fill)
    # in case of code block we better use verbatim environment
    # it is important to check the original _to_fill since the
    # to_fill was cleaned by the above call
    if util.is_code_block(q._to_fill):
        to_fill = q._to_fill \
            .replace('<code>', '\\begin{verbatim}\n') \
            .replace('</code>', '\n\\end{verbatim}\n') \
            .replace('<br>', '\n')
    sol_filled = to_fill
    for j, c in enumerate(q._correct):
        # Attention: order of replacements is important
        sol_filled = sol_filled.replace(f'{{{{{j}}}}}', '{\\bf ' + c + '}')
        to_fill = to_fill.replace(f'{{{{{j}}}}}', fill_placeholder)

    content_text += to_fill
    content_solution += sol_filled
    return content_text, content_solution


def latex_render_open(q):
    return q._text, q._text


def latex_render_exercise(q):
    content_text = f'{html_to_latex(q._text)}\n\\begin{{enumerate}}\n'
    content_solution = f'{html_to_latex(q._text)}\n\\begin{{enumerate}}\n'
    for sub_q in q._sub_questions:
        sub_q = html_to_latex(sub_q)
        content_text += f'\\item {sub_q}\n'
        content_solution += f'\\item {sub_q}\n'
        
    content_text += '\\end{enumerate}\n'
    content_solution += '\\end{enumerate}\n'
    return content_text, content_solution


def latex_render_composite(q, heading="Esercizio"):
    text = html_to_latex(q._text) + '\n'
    solution = html_to_latex(q._text) + '\n'
    for i, sub_q in enumerate(q._questions,1):
        text += f'\\subsection*{{{heading} {i} ({sub_q._weight} Punti)}}\n'
        solution += f'\\subsection*{{{heading} {i} ({sub_q._weight} Punti)}}\n'
        sub_text, sub_solution = latex_render_by_type(sub_q)
        text += sub_text
        solution += sub_solution
    return text, solution

def latex_render_by_type(q):
    text = ''
    solution = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text, solution = latex_render_choices(q)
    elif q._type == 'open':
        text, solution = latex_render_open(q)
    elif q._type == 'fill':
        text, solution = latex_render_fill(q)
    elif q._type =='exercise':
        text, solution = latex_render_exercise(q)
    elif q._type == 'composite':
        text, solution = latex_render_composite(q)
    return text, solution

# Same as latex_render, but uses strings in place of files (template, text, and solution)

def latex_render_strings(questions: list, template: str, track_n: str):
    if template is None:
        template = latex_template_raw
    text_content = ''
    solved_content = ''
    for i, q in enumerate(questions, 1):
        text_content += question_header(i)
        solved_content += question_header(i)
        text, solution = latex_render_by_type(q)
        text_content += text
        solved_content += solution
    out_text = template.replace('%%--CONTENT--%%', text_content).replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    out_solution = template.replace('%%--CONTENT--%%', solved_content).replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    
    return (out_text, out_solution)


def latex_render(questions: list, template_file: str, text_file: str, solution_file: str, track_n: str):
    text_content, solved_content = latex_render_strings(questions, open(template_file).read(), track_n)

    # Text output
    open(text_file, 'w').write(text_content)
    # Solution output
    open(solution_file, 'w').write(solved_content)



latex_template_raw = r"""
\documentclass{article}
% \documentclass{exam}
\usepackage[a4paper, total={7in, 8.5in}]{geometry}
\usepackage[utf8]{inputenc}
% Uncomment for Verdana font
% \usepackage{DejaVuSansCondensed}
% \renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\usepackage{amssymb}
\usepackage{array}
\usepackage{fancyhdr}
\renewcommand{\headrulewidth}{0pt}

% Uncomment \usepackage below for the page background pattern (to help students)
% Patterns: std, dot ruled
% Colorsets: std, ghostly
% \usepackage[pattern=dot, colorset=ghostly, textarea]{gridpapers}

\title{Quiz}

\begin{document}

\pagestyle{fancy}
\fancyhf{}
\fancyhf[HC]{
    \begin{tabular}{|m{3.5in}|m{1.25in}|m{1.75in}|}
    \hline 
    &&\\[-9pt]
    Cognome e Nome & Classe  & Data\\[3pt]
    \hline
    \end{tabular}
}
\fancyhf[FR]{
    %%--FOOTRIGHT--%%
}

%%--CONTENT--%%

% \fillwithdottedlines{\stretch{1}}
% \pagebreak
% \fillwithdottedlines{\stretch{1}}

\end{document}
"""
