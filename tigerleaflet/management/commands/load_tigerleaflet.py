import datetime
import sys
from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

try:
    from django.contrib.gis.utils import LayerMapping
except ImportError:
    print("gdal is required")
    sys.exit(1)

DOWNLOADS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'TIGERLINE_DOWNLOADS'
)
# taken from https://github.com/victor-o-silva/django-brasil-municipios/blob/master/brasil_municipios/management/commands/loadmunicipios.py
def download_from_census(filename):
    folder = os.path.basename(filename).replace('.zip', '')
    zip_file_path = os.path.join(DOWNLOADS_PATH, folder)

    with open(zip_file_path, 'wb') as zip_file:
        ftp = ftplib.FTP('ftp2.census.gov')
        ftp.login('anonymous', 'anonymous')
        ftp.cwd('geo/tiger/TIGER2016/STATE/tl_2016_us_state.zip


class Command(BaseCommand):
    help = 'Installs the 2011-2016 TIGER/LINE files for states and counties'

    def add_arguments(self, parser):
        parser.add_argument('--path', default='', dest='path',
            help='The directory where the TIGER/LINE data is stored.',
        )

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        print("Begin: %s" % datetime.datetime.now())

        call_command('load_states', path=path)
        call_command('load_counties', path=path)

        print("All Finished: %s" % datetime.datetime.now())
