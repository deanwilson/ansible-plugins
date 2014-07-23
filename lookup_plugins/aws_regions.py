# (c) 2014, Dean Wilson <dean.wilson(at)gmail.com>
# this is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from ansible import errors

try:
    import boto
    import boto.ec2
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(aws_regions): module boto is not installed")


class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms=None, inject=None, **kwargs):
        regions = [r.name for r in boto.ec2.regions() if "gov" not in r.name]

        return regions
