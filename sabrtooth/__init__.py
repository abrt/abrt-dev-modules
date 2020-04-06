# -*- coding: UTF-8 -*-

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

import platform
import sys
import traceback
import urllib.parse

import distro
import requests


def _handle_exception(etype, value, tb, name, version, url):
    # Not (yet) available on PyPI, so RTD builds fail.
    import satyr

    try:
        stack_trace = "".join(traceback.format_exception(etype, value, tb))
        report = satyr.Report()

        report.component_name = name
        report.report_type = "python"
        report.stacktrace = satyr.PythonStacktrace(stack_trace)
        report.operating_system = satyr.OperatingSystem(distro.id(), distro.version(), platform.machine())

        url = urllib.parse.urljoin(url, "reports/new/")
        headers = {
            "accept": "application/json",
        }
        files = {
            "file": ("file", report.to_json()),
        }

        requests.post(url, headers=headers, files=files)

    except:
        # Silently ignore any error in this hook,
        # to not interfere with other scripts
        pass

    return sys.__excepthook__(etype, value, tb)


def register(name: str, version: str, url: str):
    """
    Registers an exception handler that sends a report to ABRT Analytics.

    :param name: Name of the project.
    :param version: Current version of the project.
    :param url: Address to a running instance of ABRT Analytics.
    """
    sys.excepthook = lambda etype, value, tb: _handle_exception(etype, value, tb, name, version, url)
