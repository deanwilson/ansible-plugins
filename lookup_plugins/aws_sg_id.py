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
from ansible.plugins.lookup import LookupBase


try:
    import boto
    import boto.ec2
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(aws_sg_id): module boto is not installed")


class AWSSecurityGroupID(object):

    def __init__(self, region):
        self.region = region

    def get_group_id(self, group_name):

        # TODO error checking
        conn = boto.ec2.connect_to_region(self.region)

        sgs = conn.get_all_security_groups()
        filtered = filter(lambda x: x.name==group_name, sgs)[0]

        return [filtered.id]


class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        region, group_name = terms[0].split('/')

        self.sg = AWSSecurityGroupID(region)

        return self.sg.get_group_id(group_name)
