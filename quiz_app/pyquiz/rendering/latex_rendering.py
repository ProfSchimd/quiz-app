from .. import util

# TODO: In order to add 'exam' class support we need to make some changes to the code.
# - (DONE) Add 'use_exam_class' flag that distinguished "standard" LaTeX and 'exam' class 
# - (DONE) Template file for 'exam' class 
# - Switch from \section to \question using points
# - Replace the multiple choice rendering: (i) itemize becomes (ii) use \choice and \CorrectChoice
# - (DONE) Replace fill rendering to use \fillin
# - (DONE) Implement solution with \printsolutions toggled
# - Review the general layout of the resulting file
# 

fill_placeholder = ".................."


def question_header(i: int, header_text: str="Domanda", use_exam_class: bool=False) -> str:
    if use_exam_class:
        return '\n\\question\n'
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


def latex_render_choices(q, use_exam_class=False):
    
    list_environment = "itemize"
    if use_exam_class:
        list_environment = "checkboxes"
    
    text = q._text
    options = q._options
    correct = q._correct
	
    content_text = f'{html_to_latex(text)}\n\\begin{{{list_environment}}}\n'
    content_solution = f'{html_to_latex(text)}\n\\begin{{{list_environment}}}\n'
    for j, o in enumerate(options):
        if use_exam_class:
            content_text += '  \\CorrectChoice ' if correct[j] == 1 else f'  \\choice ' 
            content_text += f'{html_to_latex(o)}\n'
            content_solution += '  \\CorrectChoice ' if correct[j] == 1 else f'  \\choice ' 
            content_solution += f'{html_to_latex(o)}\n'
        else:
            content_text += f'  \\item[$\\square$] {html_to_latex(o)}\n'
            mark = '$\\square$'
            if correct[j] == 1:
                mark = '$\\checkmark$'
            content_solution += f'  \\item[{mark}] {html_to_latex(o)}\n'

    content_text += f'\\end{{{list_environment}}}\n'
    content_solution += f'\\end{{{list_environment}}}\n'
    return content_text, content_solution


def latex_render_fill(q, use_exam_class=False):
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
        if use_exam_class:
            to_fill = to_fill.replace(f'{{{{{j}}}}}', f'\\fillin[{c}]')
            sol_filled = to_fill
        else:
            # Attention: order of replacements is important
            sol_filled = sol_filled.replace(f'{{{{{j}}}}}', '{\\bf ' + c + '}')
            to_fill = to_fill.replace(f'{{{{{j}}}}}', fill_placeholder)

    content_text += to_fill
    content_solution += sol_filled
    return content_text, content_solution


def latex_render_open(q, use_exam_class=False):
    return q._text, q._text


def latex_render_exercise(q, use_exam_class=False):
    environment = "parts" if use_exam_class  else "enumerate"
    item = "part" if use_exam_class else "item"
    content_text = f'{html_to_latex(q._text)}\n\\begin{{{environment}}}\n'
    content_solution = f'{html_to_latex(q._text)}\n\\begin{{{environment}}}\n'
    for sub_q in q._sub_questions:
        sub_q = html_to_latex(sub_q)
        content_text += f'\\{item} {sub_q}\n'
        content_solution += f'\\{item} {sub_q}\n'
        
    content_text += f'\\end{{{environment}}}\n'
    content_solution += f'\\end{{{environment}}}\n'
    return content_text, content_solution


def latex_render_composite(q, heading="Esercizio", use_exam_class=False):
    text = html_to_latex(q._text) + '\n'
    solution = html_to_latex(q._text) + '\n'
    for i, sub_q in enumerate(q._questions,1):
        text += f'\\subsection*{{{heading} {i} ({sub_q._weight} Punti)}}\n'
        solution += f'\\subsection*{{{heading} {i} ({sub_q._weight} Punti)}}\n'
        sub_text, sub_solution = latex_render_by_type(sub_q)
        text += sub_text
        solution += sub_solution
    return text, solution

def latex_render_by_type(q, use_exam_class=False):
    text = ''
    solution = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text, solution = latex_render_choices(q, use_exam_class)
    elif q._type == 'open':
        text, solution = latex_render_open(q)
    elif q._type == 'fill':
        text, solution = latex_render_fill(q, use_exam_class=use_exam_class)
    elif q._type =='exercise':
        text, solution = latex_render_exercise(q, use_exam_class)
    elif q._type == 'composite':
        text, solution = latex_render_composite(q, use_exam_class)
    return text, solution

# Same as latex_render, but uses strings in place of files (template, text, and solution)

def latex_render_strings(questions: list, template: str, track_n: str, use_exam_class: bool=False):
    if template is None:
        template = latex_exam_template_raw if use_exam_class else latex_template_raw
        
    text_content = ''
    solved_content = ''
    if use_exam_class:
        text_content += '\\begin{questions}\n'
        solved_content += '\\begin{questions}\n'
        
    for i, q in enumerate(questions, 1):
        text_content += question_header(i, use_exam_class=use_exam_class)
        solved_content += question_header(i, use_exam_class=use_exam_class)
        text, solution = latex_render_by_type(q, use_exam_class)
        text_content += text
        solved_content += solution
    
    if use_exam_class:
        text_content += '\\end{questions}\n'
        solved_content += '\\end{questions}\n'
        
    out_text = template.replace('%%--CONTENT--%%', text_content).replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    out_solution = template.replace('%%--CONTENT--%%', solved_content).replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    if use_exam_class:
        out_solution = out_solution.replace("%\\printanswers","").replace("%%--PREAMBLE--%%", "\\printanswers")
    return (out_text, out_solution)


def latex_render(questions: list, template_file: str, text_file: str, solution_file: str, track_n: str, use_exam_class: bool=False):
    text_content, solved_content = latex_render_strings(questions, open(template_file).read(), track_n, use_exam_class)

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

latex_exam_template_raw=r"""\documentclass[a4paper,10pt]{exam}
\usepackage[left=2.00cm, right=2.00cm, top=3.00cm, bottom=2.00cm]{geometry}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{clrscode3e}
\usepackage{setspace}
% Uncomment for Verdana font
% \usepackage{DejaVuSansCondensed}
% \renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif

\onehalfspacing
\checkboxchar{\raisebox{-.2em}{\Large$\square$}}
\checkedchar{\raisebox{-.2em}{\Large$\checkmark$}}
\setlength\fillinlinelength{1in}
\qformat{\large{\textbf{Domanda \thequestion}}\\}

%%--PREAMBLE--%%
%\printanswers


\pagestyle{headandfoot}
\firstpageheadrule 
% \runningheadrule

\firstpageheader{\Large Cognome e Nome}{}
{\Large Classe\enspace\makebox[1.5cm]~{Data} \enspace\makebox[2.5cm]}
\lfoot{%%--LEFTFOOT--%%
}
\cfoot{%%--CENTERFOOT--%%
}
\rfoot{%%--FOOTRIGHT--%%
}

\begin{document}
% Uncomment for the grading table
% \begin{center}
%     {\small
%     \begin{tabular}{|c|c|c|c||c|c|}
%         \hline
%         Conoscenze & Competenze & Completezza & Spiegazione & \textbf{~Punti~} & \textbf{~~Voto~~}\\
%         \hline
%         & & & & &\\
%         & & & & &\\
%         & & & & &\\
%         \hline
%     \end{tabular}
%     }
% \end{center}

%%--CONTENT--%%

\end{document}

"""
