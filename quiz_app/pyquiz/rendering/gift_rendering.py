
def gift_render_choice(q):
    text = q._text
    options = q._options
    correct = q._correct
    
    content_text = f'{text}\n{{\n'
    
    
    
    correct_perc = 100.0 / sum(correct)
    wrong_perc = -100.0 / (len(correct) - sum(correct))
    
    for j in range(len(options)):
        symbol = '=' if correct[j] else '~'
        points = ''
        if q._type != 'single':
            points = f'{correct_perc}' if correct[j] else f'{wrong_perc}'
            points += "%"
            symbol = '~%'
        content_text += f'{symbol}{points}{options[j]}\n'
        
    content_text += '}\n'
    return content_text

def gift_render_fill(q):
    text = q._text
    correct = q._correct
    to_fill = q._to_fill
    
    content_text = f'{text}\n{{\n'
    
    
    for j in range(len(correct)):
       to_fill = to_fill.replace(f'{{{{{j}}}}}', f'{{={correct[j]}}}')
        
        
    content_text += f'{to_fill}\n}}\n'
    return content_text
    

def gift_render_open(q):
    pass


def gift_render_exercise(q):
    pass

def gift_render_composite(q):
    pass

def gift_render_by_type(q):
    text = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text = gift_render_choice(q)
    elif q._type == 'fill':
        text = gift_render_fill(q)
    elif q._type == 'open':
        text = gift_render_open(q)
    elif q._type =='exercise':
         text = gift_render_exercise(q)
    elif q._type == 'composite':
         text = gift_render_composite(q)
    return text

def gift_render(questions: list, template_file: str, text_file: str):
    text_content = ''
    for i, q in enumerate(questions, 1):
        text = gift_render_by_type(q)
        text_content += f'::Domanda {i}::\n{text}\n\n'

    # Text output
    out = open(template_file).read()
    out += text_content
    open(text_file, 'w').write(out)