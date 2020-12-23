from salallib import config, file_processing, actions

config.initialize()
file_processing.initialize()
actions.initialize()
actions.execute(config.action)
