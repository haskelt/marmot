from salal.salallib import config, file_processing, actions
print(__name__)
config.initialize()
file_processing.initialize()
actions.initialize()
actions.execute(config.action)
