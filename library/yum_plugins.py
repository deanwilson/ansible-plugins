#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Dean Wilson <dean.wilson@gmail.com>
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


import glob
import re
import os

DOCUMENTATION = '''
---
module: yum_plugins
short_description: Retrieve yum plugin details
description:
  - Retrieve yum plugin details
author: Dean Wilson
options:
  config_dir:
    description:
      - The plugin config directory. Defaults to /etc/yum/pluginconf.d
    required: false
    default: '/etc/yum/pluginconf.d'
    aliases: []
'''

EXAMPLES = '''
  - name: Retrieve yum plugin details
    yum_plugins:

  - debug: var=yum_plugins
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            config_dir=dict(default='/etc/yum/pluginconf.d', required=False)
        )
    )

    config_dir = module.params['config_dir']
    regexp = re.compile(r'enabled\s*=\s*1')

    plugins = {
        'plugin': [],
        'enabled': [],
        'disabled': []
    }

    files = glob.glob(config_dir + '/*.conf')

    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]

        plugins['plugin'].append(filename)

        with open(file, 'r') as f:
            content = f.read()
            if regexp.search(content) is not None:
                plugins['enabled'].append(filename)
            else:
                plugins['disabled'].append(filename)

    # sort the values
    for key in plugins:
        plugins[key].sort()

    results = {
        'yum_plugins': plugins
    }

    module.exit_json(ansible_facts=results)

from ansible.module_utils.basic import *
main()
