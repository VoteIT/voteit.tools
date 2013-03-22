import colander
import deform
from pyramid.traversal import find_interface
from betahaus.pyracont.decorators import schema_factory
from voteit.core.models.interfaces import IMeeting
from voteit.core.schemas.permissions import deferred_autocompleting_userid_widget
from voteit.core.validators import deferred_existing_userid_validator

from voteit.tools import ToolsMF as _


@colander.deferred
def deferred_groups_widget(node, kw):
    context = kw['context']
    meeting = find_interface(context, IMeeting)
    groups = meeting.get('groups', {})
    choices = []
    for (name, group) in groups.items():
        choices.append((name, group.title))
    if choices:
        choices.insert(0, ('', _(u"<select>")))
    else:
        choices.append(('', _(u"<No groups available!>")))
    return deform.widget.SelectWidget(values = choices)


@schema_factory('PopulateFromRecommendationsSchema',
                title = _("Populate a meeting based on group recommendations"),
                description = _(u"populate_from_recommendations_description",
                                default = u"Create discussions and adjust proposals according to group recommendations. "
                                          u"Warning - this may take a really long time. No status messages or similar will be displayed while processing. "
                                          u"Make sure no heavy activity goes on within the database while you copy, it will fail in that case. "
                                          u"Note that mail notifications might be sent to users."),)
class PopulateFromRecommendationsSchema(colander.Schema):
    userid = colander.SchemaNode(
        colander.String(),
        title = _(u"UserID to post as"),
        validator=deferred_existing_userid_validator,
        widget = deferred_autocompleting_userid_widget,
    )
    group = colander.SchemaNode(
        colander.String(),
        title = _(u"Group to use"),
        description = _(u"group_to_use_description",
                       default = u"Base discussion posts and proposal workflow changes on this groups recommendations"),
        widget = deferred_groups_widget,
    )
    adjust_wf = colander.SchemaNode(
        colander.Bool(),
        title = _(u"Adjust workflow of proposals according to recommendation"),
        description = _(u"Warning - will reset workflow states for all touched proposals!"),
    )
    dry_run = colander.SchemaNode(
        colander.Bool(),
        title = _(u"Dry run"),
        description = _(u"Display results but don't create any content"),
    )
