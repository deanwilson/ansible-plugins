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

try:
    import boto
    import boto.cloudformation
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(cloudformation): module boto is not installed")


class Cloudformation(object):

    def __init__(self, region, stack_name):
        self.region = region
        self.stack_name = stack_name

    def get_output(self, key):
        conn = boto.cloudformation.connect_to_region(self.region)
        stack = conn.describe_stacks(stack_name_or_id=self.stack_name)[0]
        value = [output.value for output in stack.outputs if output.key == key]

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
