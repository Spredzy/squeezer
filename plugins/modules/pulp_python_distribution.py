#!/usr/bin/python
# -*- coding: utf-8 -*-

# copyright (c) 2019, Matthias Dellweg
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: pulp_python_distribution
short_description: Manage python distributions of a pulp api server instance
description:
  - "This performs CRUD operations on python distributions in a pulp api server instance."
options:
  name:
    description:
      - Name of the distribution to query or manipulate
    type: str
    required: false
  base_path:
    description:
      - Base path to distribute a publication
    type: str
    required: false
  publication:
    description:
      - Href of the publication to be served
    type: str
    required: false
  content_guard:
    description:
      - Name of the content guard for the served content
      - "Warning: This feature is not yet supported."
    type: str
    required: false
extends_documentation_fragment:
  - mdellweg.squeezer.pulp
  - mdellweg.squeezer.pulp.entity_state
author:
  - Matthias Dellweg (@mdellweg)
'''

EXAMPLES = r'''
- name: Read list of python distributions
  pulp_python_distribution:
    api_url: localhost:24817
    username: admin
    password: password
  register: distribution_status
- name: Report pulp python distributions
  debug:
    var: distribution_status

- name: Create a python distribution
  pulp_python_distribution:
    api_url: localhost:24817
    username: admin
    password: password
    name: new_python_distribution
    base_path: new/python/dist
    publication: /pub/api/v3/publications/python/python/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/
    state: present

- name: Delete a python distribution
  pulp_python_distribution:
    api_url: localhost:24817
    username: admin
    password: password
    name: new_python_distribution
    state: absent
'''

RETURN = r'''
  distributions:
    description: List of python distributions
    type: list
    returned: when no name is given
  distribution:
    description: Python distribution details
    type: dict
    returned: when name is given
'''


from ansible_collections.mdellweg.squeezer.plugins.module_utils.pulp_helper import PulpEntityAnsibleModule
from ansible_collections.mdellweg.squeezer.plugins.module_utils.pulp_python_helper import PulpPythonDistribution


def main():
    with PulpEntityAnsibleModule(
        argument_spec=dict(
            name=dict(),
            base_path=dict(),
            publication=dict(),
            content_guard=dict(),
        ),
        required_if=[
            ('state', 'present', ['name', 'base_path']),
            ('state', 'absent', ['name']),
        ],
    ) as module:

        if module.params['content_guard']:
            raise Exception("Content guard features are not yet supported in this module.")

        natural_key = {
            'name': module.params['name'],
        }
        desired_attributes = {
            key: module.params[key] for key in ['base_path', 'content_guard', 'publication'] if module.params[key] is not None
        }

        PulpPythonDistribution(module, natural_key, desired_attributes).process()


if __name__ == '__main__':
    main()