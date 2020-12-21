#!/mingw64/bin/python3.exe

import jinja2
from lxml import etree as ET
import salal.config as config

#------------------------------------------------------------------------------

def render_node (node, env, variables, input_dirs):

    # A node can either have children or text, but not both.
    if len(node) > 0 and node.text and node.text.strip():
        raise ValueError('Invalid node structure, has both text and children')

    if node.tag == 'page' and 'modules' in node.attrib:
        process_modules(node, env, input_dirs)

    if node.text and node.text.strip():
        content_template = env.from_string(node.text.strip())
        node.text = content_template.render(variables)
    elif len(node) > 0:
        node.text = ''
        for child in node:
            node.text += render_node(child, env, variables, input_dirs) + '\n'
    else:
        node.text = ''    
            
    render_variables = variables.copy()
    render_variables['this'] = dict()   
    render_variables['this']['content'] = node.text
            
    if node.tag == 'page' and 'model' in node.attrib:
        template = env.get_template(node.attrib['model'] + '.html')
    elif node.tag.startswith('_'):
        template = env.from_string('{{ this.content }}')
    else:
        template = env.get_template(node.tag + '.html')
         
    if node.attrib:
        render_variables['this'].update(node.attrib)
    return template.render(render_variables)
    
#------------------------------------------------------------------------------

def render_page (file_stem):

    input_dir = config.system['content_root']
    output_dir = config.system['build_root'] + config.profile
    root = ET.parse(input_dir + '/' + file_stem + '.xml').getroot()
    template_dirs = [config.system['design_root'] + config.system['templates_dir']]
    env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dirs))
    root.text = render_node(root, env, config.project, [input_dir])

    with open(output_dir + '/' + file_stem + '.html', mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
        output_fh.write(root.text)

#------------------------------------------------------------------------------
