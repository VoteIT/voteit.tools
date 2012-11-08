import colander
import deform
from betahaus.pyracont.decorators import schema_factory
from voteit.core.validators import deferred_check_context_unique_name

from voteit.tools import ToolsMF as _


@schema_factory('CloneMeetingSchema', title = _("Clone meeting content - Warning: Don't use this unless you know what you're doing!"),
                description = _(u"clone_meeting_description",
                                default = u"Warning - this may take a really long time. No status messages or similar will be displayed while processing. "
                                          u"Make sure no heavy activity goes on within the database while you copy, it will fail in that case. "
                                          u"Note that mail notifications might be sent to users."),)
class CloneMeetingSchema(colander.Schema):
    new_name = colander.SchemaNode(colander.String(),
                                   validator = deferred_check_context_unique_name)
    #FIXME: types_to_clone = colander.SchemaNode()
    ignore_attributes = colander.SchemaNode(colander.String(),
                                            description = _(u"ignore_attrs_description",
                                                            default = u"Things not to copy from field_storage."),
                                            widget = deform.widget.TextAreaWidget(cols = 40, rows = 5),
                                            default = "uid",
                                            missing = u"",)
