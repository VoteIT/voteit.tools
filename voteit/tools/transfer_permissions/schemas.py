import colander
import deform
from pyramid.traversal import find_root
from betahaus.pyracont.decorators import schema_factory
from voteit.core.validators import deferred_check_context_unique_name

from voteit.tools import ToolsMF as _


@colander.deferred
def meeting_choices_widget(node, kw):
    context = kw['context']
    root = find_root(context)
    meeting_choices = set()
    for meeting in root.get_content(content_type='Meeting'):
        meeting_choices.add((meeting.__name__, meeting.title))
    return deform.widget.SelectWidget(values=meeting_choices)


@schema_factory('TransferPermissionsSchema', title = _("Transfer Permissions - Warning: Don't use this unless you know what you're doing!"),
                description = _(u"transfer_permissions_description",
                                default = u"Copy another meetings permissions and make them identical here. "
                                          u"This will replace local permissions with the ones from the other meeting! "),)
class CloneMeetingSchema(colander.Schema):
    from_meeting = colander.SchemaNode(colander.String(),
                                       widget = meeting_choices_widget)
