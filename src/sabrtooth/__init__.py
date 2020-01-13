# Copyright (c) 2020 Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Module for the ABRT exception handling hook
"""

import sys
import os


def syslog(msg):
    """Log message to system logger (journal)"""

    from systemd import journal

    # required as a workaround for rhbz#1023041
    # where journal tries to log into non-existent log
    # and fails (during %check in mock)
    #
    # try/except block should be removed when the bug is fixed

    try:
        journal.send(msg)
    except:
        pass


def send(data):
    """Send data to abrtd"""

    response = ""

    try:
        import socket
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect("/var/run/abrt/abrt.socket")
        pre = "POST / HTTP/1.1\r\n\r\n"
        pre += "type=Python3\0"
        pre += "analyzer=abrt-python3-handler\0"
        s.sendall(pre.encode())
        s.sendall(data.encode())

        s.shutdown(socket.SHUT_WR)

        while True:
            buf = s.recv(256)
            if not buf:
                break
            response += buf.decode()

        s.close()

    except socket.timeout as ex:
        syslog("communication with ABRT daemon failed: {0}".format(ex))

    except Exception as ex:
        syslog("can't communicate with ABRT daemon, is it running? {0}"
               .format(ex))

    return response


def write_dump(tb_text, tb):
    if sys.argv[0][0] == "/":
        executable = os.path.abspath(sys.argv[0])
    else:
        # We don't know the path.
        # (BTW, we *can't* assume the script is in current directory.)
        executable = sys.argv[0]

    data = "pid={0}\0".format(os.getpid())
    data += "executable={0}\0".format(executable)
    data += "reason={0}\0".format(tb_text.splitlines()[0])
    data += "backtrace={0}\0".format(tb_text)

    response = send(data)
    parts = response.split()
    if (len(parts) < 2
            or (not parts[0].startswith("HTTP/"))
            or (not parts[1].isdigit())
            or (int(parts[1]) >= 400)):
        syslog("error sending data to ABRT daemon: {0}".format(response))


def require_abs_path():
    """
    Return True if absolute path requirement is enabled
    in configuration
    """

    import problem

    try:
        conf = problem.load_plugin_conf_file("python3.conf")
    except OsError:
        return False

    return conf.get("RequireAbsolutePath", "yes") == "yes"


def handle_exception(etype, value, tb):
    """
    The exception handling function.

    progname - the name of the application
    version  - the version of the application
    """

    try:
        # Restore original exception handler
        sys.excepthook = sys.__excepthook__  # pylint: disable-msg=E1101

        import errno

        # Ignore Ctrl-C
        # SystemExit rhbz#636913 -> this exception is not an error
        if etype in [KeyboardInterrupt, SystemExit]:
            return sys.__excepthook__(etype, value, tb)

        # Ignore EPIPE: it happens all the time
        # Testcase: script.py | true, where script.py is:
        ## #!/usr/bin/python
        ## import os
        ## import time
        ## time.sleep(1)
        ## os.write(1, "Hello\n")  # print "Hello" wouldn't be the same
        #
        if etype == IOError or etype == OSError:
            if value.errno == errno.EPIPE:
                return sys.__excepthook__(etype, value, tb)

        # Ignore interactive Python and similar
        # Check for first "-" is meant to catch "-c" which appears in this case:
        ## $ python -c 'import sys; print "argv0 is:%s" % sys.argv[0]'
        ## argv0 is:-c
        # Are there other cases when sys.argv[0][0] is "-"?
        if not sys.argv[0] or sys.argv[0][0] == "-":
            einfo = "" if not sys.argv[0] else " (python {0} ...)".format(sys.argv[0])
            syslog("detected unhandled Python exception in 'interactive mode{0}'"
                   .format(einfo))
            raise Exception

        # Ignore scripts with relative path unless "RequireAbsolutePath = no".
        # (In this case we can't reliably determine package)
        syslog("detected unhandled Python exception in '{0}'"
               .format(sys.argv[0]))

        if sys.argv[0][0] != "/":
            if require_abs_path():
                raise Exception

        import traceback

        elist = traceback.format_exception(etype, value, tb)

        if tb is not None and etype != IndentationError:
            tblast = traceback.extract_tb(tb, limit=None)
            if tblast:
                tblast = tuple(tblast[-1])
            extxt = traceback.format_exception_only(etype, value)
            if tblast and len(tblast) > 3:
                ll = []
                ll.extend(tblast[:3])
                ll[0] = os.path.basename(tblast[0])
                tblast = ll

            text = ""
            for t in tblast:
                text += "{0}:".format(t)

            text += "{0}\n{1}".format(extxt[0], "".join(elist))

            trace = tb
            while trace.tb_next:
                trace = trace.tb_next
            frame = trace.tb_frame
            text += ("\nLocal variables in innermost frame:\n")
            try:
                for (key, val) in frame.f_locals.items():
                    text += "{0}: {1}\n".format(key, repr(val))
            except:
                pass
        else:
            text = "{0}\n\n{1}".format(value, "".join(elist))

        # Send data to the daemon
        write_dump(text, tb)

    except:
        # Silently ignore any error in this hook,
        # to not interfere with other scripts
        pass

    return sys.__excepthook__(etype, value, tb)


sys.excepthook = lambda etype, value, tb: handle_exception(etype, value, tb)
