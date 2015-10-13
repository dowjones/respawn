from cfn_pyplates import functions
from environments import DEV, INT, STG, PRD

zones_by_region = {
    'us-east-1': ('us-east-1b', 'us-east-1c', 'us-east-1d'),
}

dns_zones = {
    'us-east-1': {
        'internal': {
            DEV: '/hostedzone/ZXF118A4FC1GW',  # fdev.dowjones.net
            INT: '/hostedzone/ZXF118A4FC1GW',  # fint.dowjones.net
            STG: '',  # fstag.dowjones.net
            PRD: '',  # fprod.dowjones.net
        },
    },
}

availability_zones = {
    'us-east-1': {
        'internet': {
            DEV: zones_by_region['us-east-1'][:2],
            INT: zones_by_region['us-east-1'],
            STG: zones_by_region['us-east-1'],
            PRD: zones_by_region['us-east-1'],
        },
        'protected': {
            DEV: zones_by_region['us-east-1'][:2],
            INT: zones_by_region['us-east-1'],
            STG: zones_by_region['us-east-1'],
            PRD: zones_by_region['us-east-1'],
        }
    }
}

security_groups = {
    'us-east-1': {
        'internet': {
            DEV: 'sg-11a80d75',  # djin.dev-fc-product-inet-elb
            INT: 'sg-0976ac6d',  # djin.int-fc-product-inet-elb
            STG: 'sg-4470c520',  # djin.stag-fc-product-inet-elb
            PRD: 'sg-586adf3c',  # djin.prod-fc-product-inet-elb
        },
        'default': {
            DEV: 'sg-f50d6690',  # djin.dev-default
            INT: 'sg-afa582ca',  # djin.int-default
            STG: 'sg-f2f2d197',  # djin.stag-default
            PRD: 'sg-060c6763',  # djin.prod-default
        },
        'protected': {
            DEV: ['sg-008a9962'],  # Deprecated DO NOT USE
            INT: ['sg-008a9962'],  # Deprecated DO NOT USE
            STG: ['sg-stag-prot-unknown'],  # Deprecated DO NOT USE
            PRD: ['sg-prod-prot-unknown'],  # Deprecated DO NOT USE
        }
    }
}

subnets = {
    'us-east-1': {
        'internet': {
            DEV: {
                'us-east-1b': 'subnet-13b2b73b',  # (10.201.44.0/24) | djin-dev-inet-1b
                'us-east-1c': 'subnet-2e1de659'  # (10.201.45.0/24) | djin-dev-inet-1c
            },
            INT: {
                'us-east-1b': 'subnet-6527204d',  # (10.201.80.0/24) | djin-int-inet-1b
                'us-east-1c': 'subnet-8c9653fb',  # (10.201.81.0/24) | djin-int-inet-1c
                'us-east-1d': 'subnet-1291764b'  # (10.201.82.0/24) | djin-int-inet-1d
            },
            STG: {
                'us-east-1b': 'subnet-a32b398b',  # (10.192.112.0/24) | djin-stag-inet-1b
                'us-east-1c': 'subnet-66e03011',  # (10.192.113.0/24) | djin-stag-inet-1c
                'us-east-1d': 'subnet-1f9e6c46'  # (10.192.114.0/24) | djin-stag-inet-1d
            },
            PRD: {
                'us-east-1b': 'subnet-8cefa5a4',  # (10.192.46.0/24) | djin-prod-inet-1b
                'us-east-1c': 'subnet-6f434b1b',  # (10.192.47.0/24) | djin-prod-inet-1c
                'us-east-1d': 'subnet-8959a9d0'  # (10.192.43.0/24) | djin-prod-inet-1d
            }
        },
        'protected': {
            DEV: {
                'us-east-1b': 'subnet-f49d429b',  # (10.201.32.0/22) | djin-dev-pro-1b
                'us-east-1c': 'subnet-999d42f6'  # (10.201.36.0/22) | djin-dev-pro-1c
            },
            INT: {
                'us-east-1b': 'subnet-6d272045',  # (10.201.88.0/24) | djin-int-pro-1b
                'us-east-1c': 'subnet-8e9653f9',  # (10.201.89.0/24) | djin-int-pro-1c
                'us-east-1d': 'subnet-1591764c'  # (10.201.90.0/24) | djin-int-pro-1d
            },
            STG: {
                'us-east-1b': 'subnet-a12b3989',  # (10.192.120.0/24) | djin-stag-pro-1b
                'us-east-1c': 'subnet-65e03012',  # (10.192.121.0/24) | djin-stag-pro-1c
                'us-east-1d': 'subnet-1d9e6c44'  # (10.192.122.0/24) | djin-stag-pro-1d
            },
            PRD: {
                'us-east-1b': 'subnet-a39a43c2',  # (10.192.32.0/22) | djin-prod-pro-1b
                'us-east-1c': 'subnet-349d4455',  # (10.192.36.0/22) | djin-prod-pro-1c
                'us-east-1d': 'subnet-4dddf90b'  # (10.192.44.0/24) | djin-prod-pro-1d
            }
        }
    }
}

subnet_group = {
    'us-east-1': {
        'private': {
            DEV: 'djin-int-pri',
            INT: 'djin-int-pri',
            STG: 'djin-stag-pri',
            PRD: 'djin-prod-pri'
        }
    }
}

instance_prefix = {
    'us-east-1': {
        'internet': {
            DEV: 'virdin',
            INT: 'virqin',
            STG: 'virsin',
            PRD: 'virpin'
        },
        'protected': {
            DEV: 'virdin',
            INT: 'virqin',
            STG: 'virsin',
            PRD: 'virpin'
        }
    }
}

AWS_STACK_NAME_REF = functions.ref('AWS::StackName')
AWS_REGION_REF = functions.ref('AWS::Region')
AWS_STACK_ID_REF = functions.ref('AWS::StackId')
CHEF_SERVER_URL = 'https://djin-chef01.dowjones.net'
CHEF_CONFIG = 'http://djcentosrepo.dowjones.net/pub/misc/chef/djinchefconfig.sh'
CHEF_VALIDATION_PEM = 'http://djcentosrepo.dowjones.net/pub/misc/chef/djin-validation.pem'
CHEF_CONFIG_REF = functions.ref('chefConfig')
CHEF_SERVER_URL_REF = functions.ref('ChefServerURL')
CHEF_VALIDATION_PEM_REF = functions.ref('ChefValidationPEM')
CHEF_INTERVAL_NAME = 'ChefIntervalInSecs'
CHEF_INTERVAL_REF = functions.ref(CHEF_INTERVAL_NAME)
