#
# All extensions are defined here. They are initialized by Empty if
# required in your project's configuration. Check EXTENSIONS.
#

import os

from flask_security import Security
from flask_marshmallow import Marshmallow
from flask_jsglue import JSGlue
from flask_socketio import SocketIO
from flask_rq2 import RQ

toolbar = None

if os.environ['FLASK_ENV'] == 'development':
    # only works in development mode
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension()

ma = Marshmallow()
glue = JSGlue()
io = SocketIO()
rq = RQ()
security = Security()


def security_init_kwargs():
    """
    **kwargs arguments passed down during security extension initialization by
    "empty" package.
    """
    return dict()