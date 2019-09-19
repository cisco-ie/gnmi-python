"""Copyright 2019 Cisco Systems
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 * Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.

The contents of this file are licensed under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

import logging

try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse

from six import string_types
import grpc
from . import proto


def gen_target_netloc(target, netloc_prefix="//", default_port=50051):
    """Parses and validates a supplied target URL for gRPC calls.
    Uses urllib to parse the netloc property from the URL.
    netloc property is, effectively, fqdn/hostname:port.
    This provides some level of URL validation and flexibility.
    Returns netloc property of target.
    """
    if netloc_prefix not in target:
        target = netloc_prefix + target
    parsed_target = urlparse(target)
    if not parsed_target.netloc:
        raise ValueError("Unable to parse netloc from target URL %s!" % target)
    if parsed_target.scheme:
        logging.debug("Scheme identified in target, ignoring and using netloc.")
    target_netloc = parsed_target
    if parsed_target.port is None:
        ported_target = "%s:%i" % (parsed_target.hostname, default_port)
        logging.debug("No target port detected, reassembled to %s.", ported_target)
        target_netloc = gen_target_netloc(ported_target)
    return target_netloc


def validate_proto_enum(value_name, value, enum_name, enum):
    """Helper function to validate an enum against the proto enum wrapper."""
    enum_value = None
    if value not in enum.keys() and value not in enum.values():
        raise Exception(
            "{name}={value} not in {enum_name} enum! Please try any of {options}.".format(
                name=value_name,
                value=str(value),
                enum_name=enum_name,
                options=str(enum.keys()),
            )
        )
    if value in enum.keys():
        enum_value = enum.Value(value)
    else:
        enum_value = value
    return enum_value
