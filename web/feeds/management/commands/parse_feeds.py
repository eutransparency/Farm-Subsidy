import django
from django.core.management.base import NoArgsCommand, CommandError
import sys
sys.path.append('../../../')
from feeds import parse

class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    parse.parse()