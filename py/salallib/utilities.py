import glob
import re
import os
import importlib
import jinja2
from salallib.config import config
from salallib.log import log

class Utilities:

    #---------------------------------------------------------------------------

    @classmethod
    def find_files (cls, directory, extension):
        # Recursively finds all files in the directory indicated by
        # <directory> that have the extension <extension>. Returns a list
        # of paths to these files relative to <directory>.
        result_list = []
        for absolute_path in glob.glob(directory + '**/*.' + extension, recursive = True):
            relative_path = re.match('^' + directory + '(.*)$', absolute_path).group(1)
            result_list.append(relative_path)
        return result_list

    #---------------------------------------------------------------------------

    @classmethod
    def load_handlers (cls, directory):
        # Handlers are a way to determine what processing to carry out in a
        # particular instance based on a 'tag' value. To implement a set
        # of handlers, in <directory> have separate .py files for each
        # handler. Each file should create an object called <handler>.
        # The handler object should have a method <get_tags> that returns
        # a list of the tags that should be associated with this particular
        # handler. This method will real all those files, and return a
        # dict where the keys are all the tags, and the values are the
        # corresponding handler objects. Generally each handler object
        # should have one or more additional methods that carry out the
        # actual processing, but what those are and how they are called
        # is up to the code that calls the <load_handler> method.

        handlers = dict()
        with os.scandir(os.path.join(config.system['salal_root'], directory)) as entries:
            for entry in entries:
                # filter files that start with a period or don't end
                # with .py
                if entry.is_file() and (not entry.name.startswith('.')) and entry.name.endswith('.py') and entry.name != '__init__.py':
                    package_specifier = os.path.normpath(os.path.join(directory, entry.name)).replace(os.sep, '.').replace('.py', '')
                    handler_module = importlib.import_module(package_specifier)
                    for tag in handler_module.handler.get_tags():
                        log.message('TRACE', tag)
                        handlers[tag] = handler_module.handler
        return handlers
    
    #---------------------------------------------------------------------------

    @classmethod
    def substitute_variables (cls, string, variables):
        # Jinja-style variable substitution. Any instances within
        # <string> where {{<identifier>}} occurs are replaced by
        # <variables[identifier]> if it exists, or an empty string
        # otherwise. Any whitespace around the identifier is ignored,
        # so {{ <identifier> }} can be used instead if it improves
        # readability. Returns the resulting string.

        # split the string into literal text and variable references
        substrings = re.split('{{\s*(\S+)\s*}}', string)
        result = ''
        for index, substring in enumerate(substrings):
            # because of how re.split works, matching groups will be found
            # at odd-numbered indices in <substrings>
            if index % 2 == 1:
                # if the identifier in a variable reference isn't in
                # <variables>, it gets replaced with the empty string
                if substring in variables:
                    result += variables[substring]
                else:
                    result += ''
            else:
                result += substring
        return result
            
    #---------------------------------------------------------------------------

    @classmethod
    def expand_template (cls, source_dir, target_dir, file_relative_path):
        # This copies the file pointed to by <file_relative_path> from
        # <source_dir> to <target_dir>, substituting any references to
        # project variables with their current values.
        #
        # For advanced users: Technically, the files get the full Jinja
        # treatment, so you can put anything in them that you can put in a
        # Jinja template.
        env = jinja2.Environment(loader = jinja2.FileSystemLoader(source_dir))
        template = env.get_template(file_relative_path)
        output = template.render(config.project)
        with open(os.path.join(target_dir, file_relative_path), mode = 'w', encoding = 'utf-8', newline = '\n') as output_fh:
            output_fh.write(output)

    #---------------------------------------------------------------------------

utilities = Utilities
