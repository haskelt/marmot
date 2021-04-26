import os
import re
from salal.core.logging import logging
from salal.core.config import config
from salal.core.utilities import utilities 
from salal.core.dependencies import dependencies
from salal.core.file_processing import file_processing

class Build:
    
    #---------------------------------------------------------------------------

    @classmethod
    def get_tags (cls):
        return ['build']
    
    #---------------------------------------------------------------------------

    @classmethod
    def configure_search_dirs (cls, dir_type):
        search_dirs = []
        # check for the appropriate type of directory within the project
        project_search_dir = os.path.join(config.system['paths']['design_root'], config.system['paths'][dir_type + '_dir'])
        if os.path.isdir(project_search_dir):
            search_dirs.insert(0, project_search_dir)
        # check for the appropriate type of directory within the theme
        # directory, if a theme is defined
        if 'theme_root' in config.system['paths']:
            theme_search_dir = os.path.join(config.system['paths']['theme_root'], config.system['paths'][dir_type + '_dir'])
            if os.path.isdir(theme_search_dir):
                search_dirs.insert(0, theme_search_dir)
        return search_dirs
                
    #---------------------------------------------------------------------------

    @classmethod
    def select_files_to_process (cls, file_path_list, file_type):
        logging.message('DEBUG', 'Determining which ' + file_type + ' files pass include and exclude checks') 
        files_selected = []
        for file_path in file_path_list:
            passed_check = True
            if 'build' in config.system and file_type in config.system['build']:
                if 'include' in config.system['build'][file_type]:
                    passed_check = False
                    for pattern in config.system['build'][file_type]['include']:
                        if re.search(pattern, file_path) != None:
                            passed_check = True
                            break
                if passed_check and 'exclude' in config.system['build'][file_type]:
                    for pattern in config.system['build'][file_type]['exclude']:
                        if re.search(pattern, file_path) != None:
                            passed_check = False
                            break
            if passed_check:
                logging.message('TRACE', 'Passed: ' + file_path)
                files_selected.append(file_path)
            else:
                logging.message('TRACE', 'Failed: ' + file_path)
        return files_selected
    
    #---------------------------------------------------------------------------
    
    @classmethod
    def process_files (cls, file_path_list, source_dir, target_dir):
        logging.message('DEBUG', 'Determining which files need to be rebuilt')
        for file_path in file_path_list:
            file_processing.process(source_dir, target_dir, file_path)

    #---------------------------------------------------------------------------
    
    @classmethod
    def process_content (cls):
        content_dir = config.system['paths']['content_root']
        logging.message('DEBUG', 'Processing content files from ' + content_dir)
        content_files = utilities.find_files(config.system['paths']['content_root'])
        files_to_process = cls.select_files_to_process(content_files, 'content')
        cls.process_files(files_to_process, content_dir, config.system['paths']['profile_build_dir'])

    #---------------------------------------------------------------------------
    @classmethod
    def process_resources (cls):
        # Copy all the files in the resources directory to the build
        # directory, processing them according to the appropriate
        # file processing handler.
        #
        # We write files to the same relative path in the build
        # directory as they had in the resources directory. So, for
        # profile <test>, /resources/js/app.js will become
        # /build/test/js/app.js.
        #
        # Theme files get processed first, so they can be overridden
        # by local files. This is accomplished simply by overwriting
        # the theme version of the file.
        resource_dirs = cls.configure_search_dirs('resource')
        for resource_dir in resource_dirs:
            logging.message('DEBUG', 'Processing resources from ' + resource_dir)
            resource_files = utilities.find_files(resource_dir)
            files_to_process = cls.select_files_to_process(resource_files, 'resources')
            cls.process_files(files_to_process, resource_dir, config.system['paths']['profile_build_dir'])

    #---------------------------------------------------------------------------

    @classmethod
    def process_modules (cls):
        # Copy module files to the build directory, processing them
        # according to the appropriate file processing handler.
        #
        # The destination directory is determined based on the file
        # type and module name. So, a file within the modules
        # directory called 'foo/foo.css' will end up as
        # 'css/foo/foo.css' in the build directory.
        #
        # Theme files get processed first, so they can be overridden
        # by local files. This is accomplished simply by overwriting
        # the theme version of the file.
        file_types_to_copy = ['css', 'js', 'py']
        module_dirs = cls.configure_search_dirs('module')
        for module_dir in module_dirs:
            logging.message('DEBUG', 'Processing modules from ' + module_dir)
            module_subdirs = utilities.find_subdirectories(module_dir)
            for module_subdir in module_subdirs:
                logging.message('DEBUG', 'Found module ' + module_subdir)
                for file_type in file_types_to_copy:
                    logging.message('DEBUG', 'Looking for ' + file_type + ' files in ' + module_subdir)
                    source_dir = os.path.join(module_dir, module_subdir)
                    target_dir = os.path.join(config.system['paths']['profile_build_dir'], file_type, module_subdir)
                    module_files = utilities.find_files_by_extension(source_dir, file_type)
                    files_to_process = cls.select_files_to_process(module_files, 'modules')
                    cls.process_files(files_to_process, source_dir, target_dir)
        
    #---------------------------------------------------------------------------

    @classmethod
    def execute (cls, tag):

        file_processing.initialize()
        dependencies.initialize()
        cls.process_content()
        cls.process_resources()
        cls.process_modules()
        logging.message('INFO', str(dependencies.num_files_checked()) + ' file(s) processed, ' + str(dependencies.num_files_built()) + ' file(s) built')
        dependencies.write_log()

    #---------------------------------------------------------------------------

handler = Build
