#!/usr/bin/env python

import os.path
import sys

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

# activate virtualenv
USE_VIRTUAL_ENV=True
VIRTUALENV_ACTIVATE_THIS=os.path.join(os.path.dirname(CURRENT_PATH), 'bin', 'activate_this.py')

if USE_VIRTUAL_ENV:
    execfile(VIRTUALENV_ACTIVATE_THIS, dict(__file__=VIRTUALENV_ACTIVATE_THIS))


from django.core import management
import os
os.chdir(CURRENT_PATH)

def main():
    print sys.argv[1]
    management.call_command(sys.argv[1])
    
if __name__ == '__main__':
    import settings
    management.setup_environ(settings)
    main()
