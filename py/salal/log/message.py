import sys

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

logging_level = 2

#-------------------------------------------------------------------------------

def message(category, text):
    if message_categories[category]['level'] <= logging_level:
        print(message_categories[category]['prefix'] + text, file = sys.stderr)
        if message_categories[category]['fatal']:
            sys.exit(1)

#-------------------------------------------------------------------------------
