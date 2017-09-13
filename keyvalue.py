# (c) 2017, Sean Summers <ssummer3@nd.edu>
#
# This file is part of Ansible
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import functools
import operator

import six

from ansible.errors import AnsibleError
from ansible.module_utils.basic import *


tag_labels = ('Key', 'Value')
tag_getter = operator.itemgetter(*tag_labels)

parameter_labels = ('ParameterKey', 'ParameterValue')
parameter_getter = operator.itemgetter(*parameter_labels)

def dict_to_kv(labels, data):
    '''Convert {key: value,} into [{<key_label>: key, <value_label>: value},]
    '''
    return [dict(zip(labels, values)) for values in six.iteritems(data)]

def kv_to_dict(label_getter, data):
    '''Convert [{<key_label>: key, <value_label>: value},] into {key: value,}
    '''
    return dict(label_getter(value) for value in data)

class FilterModule(object):
    ''' AWS Key Value filters '''

    def filters(self):
        return {
            'to_aws_tags': functools.partial(dict_to_kv, tag_labels),
            'to_aws_parameters': functools.partial(dict_to_kv, parameter_labels),
            'from_aws_tags': functools.partial(kv_to_dict, tag_getter),
            'from_aws_parameters': functools.partial(kv_to_dict, parameter_getter),
        }

