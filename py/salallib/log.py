import sys

class Log:

    #---------------------------------------------------------------------------

    message_categories = {
        'error': {
            'level': 1,
            'prefix': '! ',
            'fatal': True
        },
        'info': {
            'level': 2,
            'prefix': '',
            'fatal': False
        },
        'debug': {
            'level': 3,
            'prefix': '%% ',
            'fatal': False
        }
    }

    logging_level = 3

    #---------------------------------------------------------------------------

    @classmethod
    def message(self, category, text):
        if self.message_categories[category]['level'] <= self.logging_level:
            print(self.message_categories[category]['prefix'] + text, file = sys.stderr)
            if self.message_categories[category]['fatal']:
                sys.exit(1)

    #---------------------------------------------------------------------------

log = Log
