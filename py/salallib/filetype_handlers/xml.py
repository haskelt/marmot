import os.path
import jinja2
from lxml import etree as ET
from salallib.config import config

class XMLHandler:

    #---------------------------------------------------------------------------

    name = '.xml'
    
    #---------------------------------------------------------------------------

    @classmethod
    def render_node (cls, node, env, variables, input_dirs):

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
    
    #---------------------------------------------------------------------------

    @classmethod
    def process (cls, source_dir, target_dir, file_stem):

        root = ET.parse(os.path.join(source_dir, file_stem + '.xml')).getroot()
        template_dirs = [os.path.join(config.system['design_root'], config.system['templates_dir'])]
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dirs))
        root.text = cls.render_node(root, env, config.project, [source_dir])

        with open(os.path.join(target_dir, file_stem + '.html'), mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
            output_fh.write(root.text)

    #---------------------------------------------------------------------------

handler = XMLHandler
