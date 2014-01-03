# (c) 2014, Dean Wilson <dean.wilson(at)gmail.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from ansible import utils, errors
import os

HAVE_BOTO=False
try:
    import boto
    import boto.cloudformation
    HAVE_BOTO=True
except ImportError:
    raise errors.AnsibleError("Can't LOOKUP(cloudformation): module boto is not installed")


class Cloudformation(object):

    def __init__(self, region, stack_name):
        self.region      = region
        self.stack_name  = stack_name

        self.aws_secret_key = os.environ['AWS_SECRET_KEY']
        self.aws_access_key = os.environ['AWS_ACCESS_KEY']

    def get_output(self, key):
        conn = boto.cloudformation.connect_to_region(self.region,
            aws_access_key_id=self.aws_access_key, 
            aws_secret_access_key=self.aws_secret_key)

        stack = conn.describe_stacks(stack_name_or_id=self.stack_name)[0]

        value = [ output.value for output in stack.outputs if output.key == key ]

        return value


class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        region, stack, value_type, key = terms.split('/')

        self.cfn = Cloudformation(region, stack)

        value = False
        if value_type == 'output':
            value = self.cfn.get_output(key)

        return value
