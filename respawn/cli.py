"""
CLI Entry point for respawn
"""

from docopt import docopt
from schema import Schema, Use, Or
from subprocess import check_call, CalledProcessError
from pkg_resources import require
import respawn


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

    gen_location = "/".join(respawn.__file__.split("/")[:-1]) + "/gen.py"
    print gen_location

    try:
        check_call(["cfn_py_generate", gen_location, "-o", args['<yaml>']])
        return 0
    except CalledProcessError, e:
        return 1
