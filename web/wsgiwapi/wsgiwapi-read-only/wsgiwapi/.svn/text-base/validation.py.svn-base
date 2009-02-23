# Copyright (c) 2009 Richard Boulton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
r"""Support for validation of request parameters.

"""
__docformat__ = "restructuredtext en"

import re
from wsgisupport import HTTPNotFound

class ValidationError(Exception):
    """Exception used to indicate that parameters failed validation.

    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "ValidationError(\"%s\")" % self.message.\
            replace('\\', '\\\\').\
            replace('"', '\"')

def validate_param(key, vals, minreps, maxreps, pattern,
                   compiled_pattern, default, doc):
    """Validate a particular parameter.

    """
    l = len(vals)

    # If not present, and there is a default, set vals to default
    if l == 0 and default is not None:
        vals = default

    # Check we've got an acceptable number of values.
    if l < minreps:
        raise ValidationError(u"Too few instances of %r supplied "
                              u"(needed %d, got %d)" %
                              (key, minreps, l))
    if maxreps is not None and l > maxreps:
        raise ValidationError(u"Too many instances of %r supplied "
                              u"(maximum %d, got %d)" %
                              (key, maxreps, l))

    if compiled_pattern is not None:
        # Check the regexp pattern matches
        for val in vals:
            if not compiled_pattern.match(val):
                raise ValidationError(u"Invalid parameter value for %r" % key)

    return vals

def validate_params(requestobj, constraints):
    """Validate parameters, raising ValidationError for problems.

    `constraints` is a dict of tuples, one for each field.  Unknown fields
    raise an error.

    """
    p = {}

    # Check for missing parameters - add if they have a default, otherwise give
    # an error.
    missing_params = set()
    for key, constraint in constraints.iteritems():
        if constraint[4] is not None:
            if key not in requestobj:
                p[key] = constraint[4]
        else:
            # check for missing params
            if constraint[0] > 0 and key not in requestobj:
                missing_params.add(key)

    if len(missing_params) != 0:
        # We trust the list of missing_params not to be trying to hack us.
        raise ValidationError(u"Missing required parameters %s" %
                              u', '.join(u"'%s'" % p for p in missing_params))

    for key in requestobj:
        constraint = constraints.get(key, None)
        if constraint is None:
            if re.match('\w+$', key):
                # No potentially dangerous characters
                raise ValidationError(u"Unknown parameter %r supplied" % key)
            else:
                raise ValidationError(u"Unknown parameter supplied")
        p[key] = validate_param(key, requestobj[key], *constraint)

    return p

def check_valid_params(request, props):
    constraints = props.get('valid_params', None)
    if constraints != None:
        request.params = validate_params(request.params, constraints)
    return request

def check_no_params(request, props):
    if len(request.params) != 0:
        raise ValidationError(u"This resource does not accept parameters")
    return request


def validate_pathinfo_params(request, param_rules):
    """Check that the pathinfo satisfies the supplied rules.

    """
    index = 0
    for name, pattern, compiled_pattern, default, required in param_rules:
        if len(request.pathinfo.tail) <= index:
            if required:
                raise HTTPNotFound(request.path)
            # Put default value into dictionary.
            request.pathinfo[name] = default
            index += 1
            continue
        param = request.pathinfo.tail[index]
        index += 1
        # Validate the param, and put it into the dictionary.
        if compiled_pattern is not None:
            if not compiled_pattern.match(param):
                raise HTTPNotFound(request.path)
        request.pathinfo[name] = param
    request.pathinfo.tail = request.pathinfo.tail[index:]

def validate_pathinfo_tail(request, tail_rules):
    """Check that the pathinfo tail satisfies the supplied rules.

    """
    if tail_rules is None:
        if len(request.pathinfo.tail) > 0:
            raise HTTPNotFound(request.path)
        else:
            return
    minreps, maxreps, pattern, compiled_pattern, default, doc = tail_rules
    # FIXME - validate pathinfo

def check_pathinfo(request, props):
    """Check the pathinfo for validity, and populate the pathinfo dictionary.

    """
    param_rules = props['pathinfo_params_rules']
    tail_rules = props['pathinfo_tail_rules']

    validate_pathinfo_params(request, param_rules)
    validate_pathinfo_tail(request, tail_rules)

    return request

def _pad_none(args, length):
    """Pad a list of arguments with None to specified length.

    """
    return (list(args) + [None] * length)[:length]

def parse_pathinfo_rules(pathinfo_items, tail_rules):
    """Parse pathinfo rules.

    """
    # Build the parameter validation rules from the args.
    param_rules = []
    previous_required = True
    for pathinfo_item in pathinfo_items:
        if len(pathinfo_item) < 1 or len(pathinfo_item) > 3:
            raise TypeError("pathinfo decorator arguments must be "
                            "sequences of length 1 to 3 items - got %d"
                            " items" % len(pathinfo_item))
        required = False
        if len(pathinfo_item) < 3:
            # No default specified, so a required parameter.
            required = True
            if not previous_required:
                raise TypeError("required parameter in pathinfo decorator"
                                " following non-required parameter")
            previous_required = True
        name, pattern, default = _pad_none(pathinfo_item, 3)
        compiled_pattern = None
        if pattern is not None:
            compiled_pattern = re.compile(pattern)
        param_rules.append((name, pattern, compiled_pattern, default, required))

    # Check the "tail" keyword argument.
    if not tail_rules is None:
        if len(tail_rules) > 5:
            raise TypeError("pathinfo tail argument must be "
                            "sequence of length 0 to 5 items - got %d "
                            "items" % len(tail_rules))
        tail_rules = _pad_none(tail_rules, 5)
        pattern = tail_rules[2]
        compiled_pattern = None
        if pattern is not None:
            compiled_pattern = re.compile(pattern)
        tail_rules = tail_rules[:2] + [compiled_pattern] + tail_rules[2:]

    return param_rules, tail_rules

# vim: set fileencoding=utf-8 :
