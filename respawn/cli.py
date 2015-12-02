"""
CLI Entry point for respawn
"""

from docopt import docopt
from schema import Schema, Use, Or
from subprocess import check_call, CalledProcessError
from pkg_resources import require
import respawn
import os


def generate():
    """Generate CloudFormation Template from YAML Specifications
Usage:
  respawn <yaml>
  respawn --help
  respawn --version

Options:
  --help
    This usage information
  --version
    Package version
    """

    version = require("respawn")[0].version
    args = docopt(generate.__doc__, version=version)
    scheme = Schema({
        '<yaml>': Use(str),
        '--help': Or(True, False),
        '--version': Or(True, False),
    })
    args = scheme.validate(args)

    # The pyplates library takes a python script that specifies options
    # that is not in scope. As a result, the file cannot be imported, so
    # the path of the library is used and gen.py is appended
    gen_location = os.path.join(os.path.dirname(respawn.__file__), "gen.py")

    try:
        check_call(["cfn_py_generate", gen_location, "-o", args['<yaml>']])
        return 0
    except CalledProcessError:
        return 1
