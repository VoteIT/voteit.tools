from pyramid.i18n import TranslationStringFactory

ToolsMF = TranslationStringFactory('voteit.tools')


def includeme(config):
    """ Include all voteit.tools componenets """
    config.scan('voteit.tools')
