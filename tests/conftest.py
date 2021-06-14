import pytest
import os
from xprocess import ProcessStarter
from http import client

@pytest.fixture
def testserver(xprocess, request):
    class Starter(ProcessStarter):
        # startup pattern
        pattern = "Server ready"

        rootdir = str(request.config.rootdir)
        os.environ['PYTHONUNBUFFERED'] = '1'
        os.environ['HOST'] = '127.0.0.1'
        os.environ['HOST_PORT'] = '5000'
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_CONFIG_DEFAULT'] = 'Test'
            
        # command to start process
        args = [
                rootdir+'/venv/bin/gunicorn',
                '--chdir', rootdir,
                '--worker-class', 'eventlet', 
                '-w', '1', 
                '-b', '127.0.0.1:5000', 
                '-t', '600', 
                'wsgi:app']

        # passing extra keyword values to
        # subprocess.Popen constructor
        popen_kwargs = {
            "shell": True,
            "user": "ben",
            "universal_newlines": True,
        }

        # max startup waiting time
        # optional, defaults to 120 seconds
        timeout = 45

        # max lines read from stdout when matching pattern
        # optional, defaults to 50 lines
        max_read_lines = 100

        # When set to True, xprocess will attempt to terminate and
        # clean-up the resources of started processes upon interruption
        # during the test run (e.g. SIGINT, CTRL+C or internal errors).
        # Defaults to False
        terminate_on_interrupt = True

        def startup_check(self):
            """
            Optional callback used to check process responsiveness
            after the provided pattern has been matched. Returned
            value must be a boolean, where:

            True: Process has been sucessfuly started and is ready
                  to answer queries.

            False: Callback failed during process startup.

            This method will be called multiple times to check if the
            process is ready to answer queries. A 'TimeoutError' exception
            will be raised if the provied 'startup_check' does not
            return 'True' before 'timeout' seconds.
            """
            connection = client.HTTPConnection("127.0.0.1", port=5000)

            connection.request('GET', '/upload')
            response = connection.getresponse()

            return response.status == 200

    # ensure process is running and return its logfile
    logfile = xprocess.ensure("testserver", Starter)

    # create a connection to the server
    connection = client.HTTPConnection("127.0.0.1", port=5000)
    yield connection

    # clean up whole process tree afterwards
    xprocess.getinfo("testserver").terminate()
