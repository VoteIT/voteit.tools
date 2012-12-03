
def includeme(config):
    """ Include transfer users """
    config.scan('voteit.tools.transfer_permissions')
