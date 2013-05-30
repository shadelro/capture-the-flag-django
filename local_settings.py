# -*- coding: utf-8 -*-

import warnings
import exceptions
warnings.filterwarnings("ignore", category=exceptions.RuntimeWarning, module='django.db.backends.sqlite3', lineno=50)

DEPLOYMENT_MODE = 'local'

SITE_ROOT_URI = 'http://capturetheflag.com:8001/'

DEBUG = True
