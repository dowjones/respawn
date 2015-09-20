from cfn_pyplates import functions

DEV='dev'
INT='int'
STG='stag'
PRD='prod'

all=(
    DEV,
    INT,
    STG,
    PRD,
)

def validate(e):
    if e not in all:
        raise KeyError('{} is not a supported environment'.format(e))
    return e

def get_supported():
    return all

