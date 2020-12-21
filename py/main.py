from salal import config, actions

config.initialize()
actions.initialize()
actions.execute(config.action)
