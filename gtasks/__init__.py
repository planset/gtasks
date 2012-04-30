# -*- coding: utf-8 -*-
"""
    gtasks
    ~~~~~~~~~~~~


    :copyright: (c) 2012 by Daisuke Igarashi.
    :license: BSD, see LICENSE for more details.
"""

import os
import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from gtasks import google_tasks_ui
from gtasks import config as gtasks_config

HOME_DIR = os.path.expanduser('~')

DEFAULT_CONFIG_FILENAME = ".gtasks.conf"
config_path = os.path.join(HOME_DIR, DEFAULT_CONFIG_FILENAME)
config = gtasks_config.Config()
if os.path.exists(config_path):
    config.from_pyfile(config_path)


def build_service(config):
    """build google api service
    :param config: instance of Config.
    """
    FLAGS = gflags.FLAGS

    FLOW = OAuth2WebServerFlow(
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='gtasks/0.1')

    FLAGS.auth_local_webserver = False

    storage = Storage(os.path.join(HOME_DIR, '.gtasks.dat'))
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = run(FLOW, storage)

    http = httplib2.Http()
    http = credentials.authorize(http)

    return build(serviceName='tasks', version='v1', http=http,
           #developerKey=config.DEVELOPER_KEY
           )


def main():
    """
    cli loop
    """
    service = build_service(config)
    gtasks = google_tasks_ui.GoogleTasksUI(service)
    while True:
        try:
            gtasks.show_tasks()
            print ""
            c = raw_input('Command: ')
            if c == 'q':
                break
            elif c == 'h':
                gtasks.show_help()
                raw_input('press ENTER')
            elif c in gtasks.actions.keys():
                gtasks.actions[c]()
            else:
                pass
            #gtasks.actions[choice]()
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
    
