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


class TransferPermissionsView(BaseEdit):

    @view_config(name = "transfer_permissions", context = IMeeting, permission = security.MANAGE_SERVER,
                 renderer = 'voteit.core.views:templates/base_edit.pt')
    def transfer_permissions_form(self):
        schema = createSchema('TransferPermissionsSchema').bind(context = self.context, request = self.request)
        add_csrf_token(self.context, self.request, schema)  
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
            from_meeting = self.api.root[appstruct['from_meeting']]
            value = from_meeting.get_security()
            self.api.meeting.set_security(value)
            self.api.flash_messages.add(_(u"Permissions transfered"))
            return HTTPFound(location = self.request.resource_url(self.api.meeting))
            
        self.response['form'] = form.render()
        return self.response

@view_action('meeting', 'transfer_permissions', title = _(u"Transfer permissions"), link = "transfer_permissions",
             permission = security.MANAGE_SERVER)
def menu_link(context, request, va, **kw):
    api = kw['api']
    url = request.resource_url(api.meeting, va.kwargs['link'])
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))

