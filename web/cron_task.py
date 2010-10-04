#!/usr/bin/env python

# To be called every 5 minutes.  Add any commands below.

commands = (
        'process_search_queue', # Updates the xaipain index
        )
    

import os.path

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
    for c in commands:
        management.call_command(c)
    
if __name__ == '__main__':
    import settings
    management.setup_environ(settings)
    main()
