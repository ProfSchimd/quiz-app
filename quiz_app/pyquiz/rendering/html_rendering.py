
fill_placeholder ='<input type="textbox" style="padding: 1px">'

def question_header(i):
    return f'<h2>Domanda {i}</h2>\n'

def html_render_choices(q):
    content_text = ''
    content_solution = ''
    text = q._text
    options = q._options
    correct = q._correct
	
    content_text += f'<p>{text}</p>\n'
    content_solution += f'<p>{text}</p>\n'
    
    for j in range(len(options)):
        opt = f'<p class="option"><input type="checkbox" id="ans-{j}">\n<label for="ans-{j}">{options[j]}</label></p>'
        content_text += opt
        checked = 'checked' if correct[j] == 1 else ''
        opt = f'<p class="option"><input type="checkbox" id="ans-{j}" disabled {checked}>\n<label for="ans-{j}">{options[j]}</label></p>'
        content_solution += opt
        j += 1
    content_text += '\n'
    content_solution += '\n'
    
    return content_text, content_solution

def html_render_open(q):
    content_text = q._text
    content_solution = q._text
    return content_text, content_solution
    
def html_render_fill(q):
    content_text = ''
    content_solution = ''
    correct = q._correct
    content_text += f'<p>{q._text}</p>\n\n'
    content_solution += f'<p>{q._text}</p>\n\n'
    to_fill = q._to_fill
    sol_filled = to_fill
    for j in range(len(correct)):
        sol_filled = sol_filled.replace(f'{{{{{j}}}}}', f'<b>{correct[j]}</b>')
        to_fill = to_fill.replace(f'{{{{{j}}}}}', fill_placeholder)

    content_text += f'<p>{to_fill}</p>\n\n'
    content_solution += f'<p>{sol_filled}</p>\n\n'

    return content_text, content_solution

def html_render_exercise(q):
    content_text = q._text
    content_solution = q._text
    
    content_text += '<ol>\n'
    content_solution += '<ol>\n'
    for sub_q in q._sub_questions:
        content_text += f'<li>{sub_q}</li>\n'
        content_solution += f'<li>{sub_q}</li>\n'
    content_text += '</ol>\n'
    content_solution += '</ol>\n'
    
    return content_text, content_solution

def html_render_composite(q, heading='Esercizio'):
    text = q._text + '\n'
    solution = q._text + '\n'
    i = 1
    for sub_q in q._questions:
        score = f'({sub_q._weight} Punti)'
        text += f'<h3>{heading} {i} {score}</h3>\n'
        solution += f'<h3>{heading} {i}</h3>\n'
        sub_text, sub_solution = html_render_by_type(sub_q)
        text += sub_text
        solution += sub_solution
        i += 1
    return text, solution

def html_render_by_type(q):
    text = ''
    solution = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text, solution = html_render_choices(q)
    elif q._type == 'open':
        text, solution = html_render_open(q)
    elif q._type == 'fill':
        text, solution = html_render_fill(q)
    elif q._type =='exercise':
        text, solution = html_render_exercise(q)
    elif q._type == 'composite':
        text, solution = html_render_composite(q)
    return text, solution


def html_render_strings(questions: list, template: str, track_n: str):
    if template is None:
        template = html_template_raw
    text_content = ''
    solved_content = ''
    i = 1
    for q in questions:
        text_content += question_header(i)
        solved_content += question_header(i)
        text, solution = html_render_by_type(q)
        text_content += text
        solved_content += solution
        i += 1
        
    out_text = template.replace("{% CONTENT %}", text_content).replace("{% FOOTRIGHT %}", f"T:{track_n}")
    out_solution = template.replace("{% CONTENT %}", solved_content).replace("{% FOOTRIGHT %}", f"T:{track_n}")
    
    return (out_text, out_solution)


def html_render(questions, template_file, text_file, solution_file, track_n):

    text_content, solved_content = html_render_strings(questions, open(template_file).read(), track_n)

    # Text output
    open(text_file, 'w').write(text_content)
    # Solution output
    open(solution_file, 'w').write(solved_content)


html_template_raw = r"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Verifica</title>
        <style>
        @media only screen {
            body {
                color: #333333;
                text-align: justify;
                line-height: 1.5rem;
                margin-top: 40px;
                margin-left: 8%;
                margin-right: 8%;
                font-family: "Open Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            }
            code {
                background-color: #EEEEEE;
                color: #555577;
                padding: 3px;
                border-radius: 4px;
            }
            h2 {
                font-size: 1.8rem;
                margin-top: 30px;
                margin-bottom: 10px;
            }
            h3 {
                font-size: 1.3rem;
                margin-top: 1.5rem;
                margin-bottom: 0.3rem;
            }
            ol {
                margin-right: 30px;
                
            }
            ol li {
                margin-top: 5px;
                margin-bottom: 10px;
                margin-left: 15px;
                margin-right: 50px;
            }
            p.option {
                padding-bottom: 1px;
                padding-left: 30px;
            }
        }
        .head-name {
            width: 45%;
        }
        .head-more {
            width: 13%;
        }
        .alert-red {
            border: 1px solid;
            padding: 5px;
            color: red
        }
        </style>
    </head>
    <body>
        <h4>Cognome Nome: <input type="text" class="head-name"> Classe: <input type="text" class="head-more"> Data: <input type="text" class="head-more"></h4>
        <div class="alert-red">
			<h2>Regole di comportamento</h2>
			<ul>
				<li>È possibile usare il <u>proprio</u> quaderno degli appunti, ma non materiali esterni o strumenti di comunicazioni come chat, email o altro.</li>
				<li>È vietato usare strumenti come ChatGPT, Gemini o simili.</li>
				<li>Telefono e <u>tutti</u> i dispositivi elettronici vanno tenuti spenti nello zaino.</li>
				<li>Nel caso si venisse sorpresi a violare una delle regole sopra: la prova verrà annullata con valutazione <b>2</b> sul registro elettronico e con nota disciplinare indicante il motivo del voto. In tal caso <u>non è prevista alcuna prova di recupero del voto</u>.</li>
			</ul>
		</div>
        {% CONTENT %}
    </body>
</html>"""
