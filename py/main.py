from salallib import config, filetypes, actions

config.initialize()
filetypes.initialize()
actions.initialize()
actions.execute(config.action)
