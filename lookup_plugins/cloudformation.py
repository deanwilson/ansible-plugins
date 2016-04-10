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
# Refactored for Ansible 2.0 by Josh Quint  josh at turinggroup.com

from ansible import errors
from ansible.plugins.lookup import LookupBase
import sys
from traceback import format_exception

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

    def get_item(self, resource_type, key):
        conn = boto.cloudformation.connect_to_region(self.region)
        stack = conn.describe_stacks(stack_name_or_id=self.stack_name)[0]
        if resource_type in ['parameter', 'output']:
            attr = "{0}s".format(resource_type)
            return [item.value for item in
                    getattr(stack, attr) if item.key == key]
        elif resource_type == 'resource_id':
            return [stack.describe_resources(key)[0].physical_resource_id]
        else:
            raise errors.AnsibleError(
                "unknown resource type {0}".format(resource_type))


class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        try:
            region, stack, value_type, key = terms[0].split('/')
            self.cfn = Cloudformation(region, stack)
            value = self.cfn.get_item(value_type, key)
            return value
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise errors.AnsibleError(
                format_exception(exc_type, exc_value, exc_traceback))
