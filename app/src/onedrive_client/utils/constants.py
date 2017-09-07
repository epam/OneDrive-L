"""
Common constants
"""

ACTIONS = {
    'start': 'start the service',
    'restart': 'stop and restart the service if the service '
               'is already running, otherwise start the service',
    'stop': 'stop the service',
    'try-restart': 'restart the service if the service '
                   'is already running',
    'reload': 'cause the configuration of the service to be reloaded '
              'without actually stopping and restarting the service',
    'force-reload': 'cause the configuration to be reloaded if the '
                    'service supports this, otherwise restart the '
                    'service if it is running',
    'status': 'print the current status of the service'
}
