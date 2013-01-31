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
                                        button_save,)
from voteit.core.views.base_edit import BaseEdit
from voteit.groups.interfaces import IGroupRecommendations

from voteit.tools import ToolsMF as _


class RecToDiscussionsView(BaseEdit):

    @view_config(name = "rec_to_discussions", context = IMeeting, permission = security.MANAGE_SERVER,
                 renderer = 'voteit.core.views:templates/base_edit.pt')
    def rec_to_discussions_form(self):
        """ Note: This is far from finished, don't use this unless you really know what you're doing! """
        schema = createSchema('PopulateFromRecommendationsSchema').bind(context = self.context, request = self.request)
        add_csrf_token(self.context, self.request, schema)  
        form = deform.Form(schema, buttons=(button_save,))
        self.api.register_form_resources(form)

        post = self.request.POST
        if 'save' in post:
            controls = post.items()
            try:
                appstruct = form.validate(controls)
            except deform.ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            adjust_wf = appstruct['adjust_wf']
            group = appstruct['group']
            userid = appstruct['userid']
            dry_run = appstruct['dry_run']
            created_discussion_posts = 0
            wf_adjusted_proposals = 0
            proposals_and_rec = self.get_proposals_and_rec(group)
            handled_props = len(proposals_and_rec)
            for (prop, rec) in proposals_and_rec:
                if rec['text']:
                    created_discussion_posts += 1
                    text = "%s\n%s" % (rec['text'], u"".join([u'#%s' % x for x in prop.get_tags()]))
                    post = createContent('DiscussionPost', creators = [userid], text = text)
                    name = post.suggest_name(prop.__parent__)
                    prop.__parent__[name] = post
                if rec['state'] and adjust_wf:
                    wf_adjusted_proposals += 1
                    prop.workflow.initialize(prop)
                    prop.set_workflow_state(self.request, rec['state'])
            self.api.flash_messages.add(_(u"Done - handled ${count} proposals",
                                          mapping = {'count': handled_props}))
            self.api.flash_messages.add(_(u"${count} new discussion posts added",
                                          mapping = {'count': created_discussion_posts}))
            if wf_adjusted_proposals:
                self.api.flash_messages.add(_(u"${count} proposals workflow adjusted",
                                              mapping = {'count': wf_adjusted_proposals}))    
            if dry_run:
                from transaction import abort
                abort()
                self.api.flash_messages.add(_(u"DRY RUN - transaction aborted and nothing saved!"))
            return HTTPFound(location = self.request.resource_url(self.context))
            
        self.response['form'] = form.render()
        return self.response

    def get_proposals_and_rec(self, group):
        """ Return all proposals that have recommendations from selected group. """
        results = set()
        for docid in self.api.search_catalog(context = self.context, content_type = 'Proposal')[1]:
            prop = self.api.resolve_catalog_docid(docid)
            recs = self.request.registry.getAdapter(prop, IGroupRecommendations)
            recommendation = recs.get_group_data(group)
            if recommendation is not None:
                results.add((prop, recommendation))
        return results


@view_action('meeting', 'rec_to_discussions', title = _(u"Recommendations to discussions"), permission = security.MANAGE_SERVER)
def menu_link(context, request, va, **kw):
    api = kw['api']
    url = request.resource_url(api.meeting, 'rec_to_discussions')
    return """<li><a href="%s">%s</a></li>""" % (url, api.translate(va.title))

