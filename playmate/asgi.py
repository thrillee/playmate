import os
from sphinx import application

import django
from channels.routing import get_default_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'playmate.settings')
django.setup()
application = get_default_application()