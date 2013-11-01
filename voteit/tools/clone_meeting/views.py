from copy import deepcopy

import deform
from pyramid.view import view_config
from pyramid.traversal import resource_path
from pyramid.httpexceptions import HTTPFound
from betahaus.viewcomponent.decorators import view_action
from betahaus.pyracont.factories import createSchema
from betahaus.pyracont.factories import createContent
from voteit.core import security
from voteit.core.models.interfaces import IMeeting
from voteit.core.models.schemas import (add_csrf_token,
                                        button_save,
                                        button_cancel,)
from voteit.core.views.base_edit import BaseEdit

from voteit.tools import ToolsMF as _


class CloneMeetingView(BaseEdit):

    @view_config(name = "clone_meeting", context = IMeeting, permission = security.MANAGE_SERVER,
                 renderer = 'voteit.core.views:templates/base_edit.pt')
    def clone_form(self):
        """ Note: This is far from finished, don't use this unless you really know what you're doing! """
        schema = createSchema('CloneMeetingSchema')
        add_csrf_token(self.context, self.request, schema)
        schema = schema.bind(context = self.context, request = self.request)
        form = deform.Form(schema, buttons=(button_save, button_cancel,))
        self.api.register_form_resources(form)
        post = self.request.POST
        if 'save' in post:
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e: #pragma : no cover
                self.response['form'] = e.render()
                return self.response
            new_name = appstruct['new_name']
            new_meeting = createContent('Meeting', title = "Clone of %s" % self.context.title)
            self.api.root[new_name] = new_meeting
            if hasattr(self.context, '__proposal_ids__'):
                new_meeting.__proposal_ids__ = deepcopy(self.context.__proposal_ids__)
            ignore_attributes = appstruct['ignore_attributes'].splitlines()
            self.process_meeting_structure(new_meeting, ignore_attributes)
            self.api.flash_messages.add(_(u"Cloned meeting"))
            return HTTPFound(location = self.request.resource_url(new_meeting))
        self.response['form'] = form.render()
        return self.response

    def process_meeting_structure(self, new_meeting, ignore_attributes):
        for ai in self.context.get_content(content_type = 'AgendaItem'):
            new_ai = createContent('AgendaItem')
            for (k, v) in ai.field_storage.items():
                if k in ignore_attributes:
                    continue
                new_ai.field_storage[k] = v
            new_meeting[ai.__name__] = new_ai
            self.process_ai(ai, new_ai, ignore_attributes)

    def process_ai(self, ai, new_ai, ignore_attributes):
        #FIXME: This should be dynamic later on
        for obj in ai.get_content(content_type = 'Proposal'):
            new_obj = createContent('Proposal')
            for (k, v) in obj.field_storage.items():
                if k in ignore_attributes:
                    continue
                new_obj.field_storage[k] = v
            if hasattr(obj, '__tags__'):
                new_obj.__tags__ = deepcopy(obj.__tags__)
            new_ai[obj.__name__] = new_obj


@view_action('meeting', 'clone_meeting', title = _(u"Clone meeting"), link = "clone_meeting", permission = security.MANAGE_SERVER)
def menu_link(context, request, va, **kw):
    api = kw['api']
    url = request.resource_url(api.meeting, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))

