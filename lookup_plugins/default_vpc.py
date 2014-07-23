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

from ansible import errors

try:
    import boto
    import boto.ec2
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(default_vpc): module boto is not installed")


class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        region = terms.split()[0]

        conn = boto.ec2.connect_to_region(region)
        attrs = conn.describe_account_attributes('default-vpc')
        vpc_id = attrs[0].attribute_values[0]

        return [vpc_id]
