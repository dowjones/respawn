"""
CLI Entry point for respawn
"""

from __future__ import print_function
from docopt import docopt
from schema import Schema, Use, Or, Optional
from subprocess import Popen, PIPE
from pkg_resources import require
import respawn
import os
import sys
import boto3

def generate():
    """Generate CloudFormation Template from YAML Specifications
Usage:
  respawn <yaml> [--validate]
  respawn --help
  respawn --version

Options:
  --validate
    Validates template with Amazon Web Services
  --help
    This usage information
  --version
    Package version
    """

    version = require("respawn")[0].version
    args = docopt(generate.__doc__, version=version)
    scheme = Schema({
        '<yaml>': Use(str),
        '--validate': Or(True, False),
        '--help': Or(True, False),
        '--version': Or(True, False),
    })
    args = scheme.validate(args)

    # The pyplates library takes a python script that specifies options
    # that is not in scope. As a result, the file cannot be imported, so
    # the path of the library is used and gen.py is appended
    gen_location = os.path.join(os.path.dirname(respawn.__file__), "gen.py")

    try:
        p = Popen(["cfn_py_generate", gen_location, "-o", args['<yaml>']], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        return_code = p.returncode
        if return_code == 0:
            print(output, file=sys.stdout)
            try:
                # Validate template
                if args['--validate']:
                    client = boto3.client('cloudformation')
                    client.validate_template(TemplateBody=output)
                    print("---------------------------------------", file=sys.stderr)
                    print("Template Validation Successful", file=sys.stderr)
                    print("---------------------------------------", file=sys.stderr)
            except Exception as e:
                print("Template Validation Failed:", e, file=sys.stderr)
        else:
            print(err, file=sys.stderr)
        return return_code
    except Exception as e:
        print(e, file=sys.stderr)
        return 1
