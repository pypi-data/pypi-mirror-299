# -*- coding: utf-8 -*-
"""Defines the "HasStatus" mixin"""

from ga4gh.testbed.report.status import Status

class HasStatus(object):
    """Mixin for report components that have a status

    Defines a single attribute "status", with Status enum values allowed.
    Can be used to apply "status" attribute to report tests, cases, phases,
    etc.

    Attributes:
        status (Status): status of report component
    """

    def __initialize_status(self):
        self.status = Status.UNKNOWN

    def set_status_unknown(self):
        self.status = Status.UNKNOWN

    def set_status_pass(self):
        self.status = Status.PASS
    
    def set_status_warn(self):
        self.status = Status.WARN

    def set_status_fail(self):
        self.status = Status.FAIL
    
    def set_status_skip(self):
        self.status = Status.SKIP
    
    def get_status(self):
        return self.status
