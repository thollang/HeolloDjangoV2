from .common import *
 
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = ['*']
HAYSTACK_CONNECTIONS['default']['URL'] = 'http://hellodjangov2:9200/'
