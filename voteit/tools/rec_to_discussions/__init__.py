

def includeme(config):
    """ Include recommendations to discussions """
    config.scan('voteit.tools.rec_to_discussions')
