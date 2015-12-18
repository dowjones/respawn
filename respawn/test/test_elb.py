import unittest
from respawn import elb, sns, errors


class TestElb(unittest.TestCase):
    def test_accessLoggingPolicy(self):
        sample_kwargs = {'s3_bucket_prefix': 'sampleName', 'enabled': True, 'emit_interval': 20, 's3_bucket_name':
            'sampleName'}
        v = elb.AccessLoggingPolicy(**sample_kwargs)
        assert v == {
            "EmitInterval": 20,
            "Enabled": True,
            "S3BucketName": "sampleName",
            "S3BucketPrefix": "sampleName"
        }

    def test_appCookieStickinessPolicy(self):
        sample_kwargs = {'cookie_name': 'cookie1', 'policy_name': 'policy1'}
        v = elb.AppCookieStickinessPolicy(**sample_kwargs)
        assert v == {
            "CookieName": "cookie1",
            "PolicyName": "policy1"
        }

    def test_availabilityZones(self):
        pass

    def test_connectionDrainingPolicy(self):
        sample_kwargs = {'enabled': True, 'timeout': 10}
        v = elb.ConnectionDrainingPolicy(**sample_kwargs)
        assert v == {"Enabled": True,
                     "Timeout": 10
                     }

    def test_connectionSettings(self):
        sample_kwargs = {'idle_timeout': 40}
        v = elb.ConnectionSettings(**sample_kwargs)
        assert v == {'IdleTimeout': 40}

    def test_healthCheck(self):
        sample_kwargs = {'healthy_threshold': 111111, 'interval': 222222, 'target': 333333, 'timeout': 444444,
                         'unhealthy_threshold': 555555}
        v = elb.HealthCheck(**sample_kwargs)
        assert v == {
            "HealthyThreshold": 111111,
            "Interval": 222222,
            "Timeout": 444444,
            "UnhealthyThreshold": 555555,
            "Target": 333333
        }

    def test_listener(self):
        pass

    def test_httpListener(self):
        pass

    def test_LBCookieStickinessPolicy(self):
        sample_kwargs = {'policy_name': 'sampleName', 'cookie_expiration_period': 2222}
        v = elb.LBCookieStickinessPolicy(**sample_kwargs)
        assert v == {
            "PolicyName": "sampleName",
            "CookieExpirationPeriod": 2222
        }

    def test_policies(self):
        pass

    def test_protocolListener(self):
        pass

    def test_tcpListener(self):
        pass

    def test_Tags(self):
        pass

    def test_loadBalancerProperties(self):
        sample_kwargs = {'health_check_port': 8443,
                         'other_security_groups': 'sampleName', 'health_check_path': '/iisstart.htm',
                         'instances': ['10.23.23.23', '13.12.13.14'], 'cross_zone': True, 'port': 443,
                         'security_groups': ['sg-111111'],
                         'access_logging_policy': {'s3_bucket_prefix': 'sampleName', 'enabled': True, 'emit_interval':
                             20,
                                                   's3_bucket_name': 'sampleName'}, 'realm': 'protected',
                         'scheme': 'internet-facing', 'connection_draining_policy': {'enabled': True, 'timeout': 10},
                         'subnets': ['subnet-111111', 'subnet-222222', 'subnet-3333333'],
                         'health_check': {'healthy_threshold': 3434, 'interval': 343434, 'target': 343434,
                                          'timeout': 434, 'unhealthy_threshold': 343434}, 'env': 'int',
                         'connection_settings': {'idle_timeout': 40},
                         'listeners': {'instance_port': 84, 'instance_protocol': 'tcp', 'load_balancer_port': 83,
                                       'protocol': "HTTPS"}}
        v = elb.LoadBalancerProperties(**sample_kwargs)
        assert v == {
            "AccessLoggingPolicy": {
                "EmitInterval": 20,
                "Enabled": True,
                "S3BucketName": "sampleName",
                "S3BucketPrefix": "sampleName"
            },
            "ConnectionDrainingPolicy": {
                "Enabled": True,
                "Timeout": 10
            },
            "ConnectionSettings": {
                "IdleTimeout": 40
            },
            "CrossZone": True,
            "HealthCheck": {
                "HealthyThreshold": 3434,
                "Interval": 343434,
                "Timeout": 434,
                "UnhealthyThreshold": 343434,
                "Target": 343434
            },
            "Instances": [
                "10.23.23.23",
                "13.12.13.14"
            ],
            "Listeners": {
                "instance_port": 84,
                "instance_protocol": "tcp",
                "load_balancer_port": 83,
                "protocol": "HTTPS"
            },
            "Scheme": "internet-facing",
            "SecurityGroups": [
                "sg-111111"
            ],
            "Subnets": [
                "subnet-111111",
                "subnet-222222",
                "subnet-3333333"
            ]
        }

    def test_loadBalancer(self):
        sample_kwargs = {'health_check_port': 8443,
                         'other_security_groups': 'sg-111111', 'health_check_path': '/iisstart.htm',
                         'listeners': {'instance_port': 84, 'instance_protocol': 'tcp', 'load_balancer_port': 83,
                                       'protocol': "HTTPS"}, 'instances': ['10.23.23.23', '13.12.13.14'],
                         'cross_zone': True, 'port': 443, 'security_groups': ['sg-111111'],
                         'access_logging_policy': {'s3_bucket_prefix': 'sampleName', 'enabled': True, 'emit_interval':
                             20,
                                                   's3_bucket_name': 'sampleName'}, 'realm': 'protected',
                         'app_cookie_stickiness_policy': [{'cookie_name': 'sampleName', 'policy_name':
                             'samplePolicyName'},
                                                          {'cookie_name': 'sampleName', 'policy_name':
                                                              'samplePolicyName'}],
                         'scheme': 'internet-facing', 'connection_draining_policy': {'enabled': True, 'timeout': 10},
                         'health_check': {'healthy_threshold': 3434, 'interval': 343434, 'target': 343434,
                                          'timeout': 434, 'unhealthy_threshold': 343434}, 'env': 'int',
                         'tags': [{'key': 'sampleKey', 'value': 'sampleValue'}, {'key': 'sampleKey1',
                                                                                 'value': 'sampleValue1'}],
                         'connection_settings': {'idle_timeout': 40},
                         'lb_cookie_stickiness_policy': [{'cookie_expiration_period': 2131, 'policy_name':
                             'samplePolicyName'},
                                                         {'cookie_expiration_period': 1313, 'policy_name':
                                                             'samplePolicyName2'}],
                         'policies': [
                             {'attribute': [{'name': 'name1', 'value': 'value2'}, {'name': 'name2', 'value': 'value2'}],
                              'instance_ports': ['2121', '2424'], 'load_balancer_ports': ['32323', '2424'],
                              'policy_type': 'SSLNegotiationPolicyType', 'policy_name': 'sds'},
                             {'attribute': [{'name': 'value1', 'value': 'value2'}], 'instance_ports': ['2121', '2424'],
                              'load_balancer_ports': ['32323', '2424'], 'policy_type': 'SSLNegotiationPolicyType',
                              'policy_name': 'samplePolicyName'}]}

        v = elb.LoadBalancer("name", **sample_kwargs)
        assert v['Properties'] == {
            "AccessLoggingPolicy": {
                "EmitInterval": 20,
                "Enabled": True,
                "S3BucketName": "sampleName",
                "S3BucketPrefix": "sampleName"
            },
            "AppCookieStickinessPolicy": [
                {
                    "CookieName": "sampleName",
                    "PolicyName": "samplePolicyName"
                },
                {
                    "CookieName": "sampleName",
                    "PolicyName": "samplePolicyName"
                }
            ],
            "ConnectionDrainingPolicy": {
                "Enabled": True,
                "Timeout": 10
            },
            "ConnectionSettings": {
                "IdleTimeout": 40
            },
            "CrossZone": True,
            "HealthCheck": {
                "HealthyThreshold": 3434,
                "Interval": 343434,
                "Timeout": 434,
                "UnhealthyThreshold": 343434,
                "Target": 343434
            },
            "Instances": [
                "10.23.23.23",
                "13.12.13.14"
            ],
            "LBCookieStickinessPolicy": [
                {
                    "PolicyName": "samplePolicyName",
                    "CookieExpirationPeriod": 2131
                },
                {
                    "PolicyName": "samplePolicyName2",
                    "CookieExpirationPeriod": 1313
                }
            ],
            "Listeners": {
                "instance_port": 84,
                "instance_protocol": "tcp",
                "load_balancer_port": 83,
                "protocol": "HTTPS"
            },
            "Policies": [
                {
                    "PolicyName": "sds",
                    "Attribute": [
                        {
                            "Name": "name1",
                            "Value": "value2"
                        },
                        {
                            "Name": "name2",
                            "Value": "value2"
                        }
                    ],
                    "InstancePorts": [
                        "2121",
                        "2424"
                    ],
                    "LoadBalancerPorts": [
                        "32323",
                        "2424"
                    ],
                    "PolicyType": "SSLNegotiationPolicyType"
                },
                {
                    "PolicyName": "samplePolicyName",
                    "Attribute": [
                        {
                            "Name": "value1",
                            "Value": "value2"
                        }
                    ],
                    "InstancePorts": [
                        "2121",
                        "2424"
                    ],
                    "LoadBalancerPorts": [
                        "32323",
                        "2424"
                    ],
                    "PolicyType": "SSLNegotiationPolicyType"
                }
            ],
            "Scheme": "internet-facing",
            "SecurityGroups": [
                "sg-111111"
            ],
            "Tags": [
                {
                    "Key": "sampleKey",
                    "Value": "sampleValue"
                },
                {
                    "Key": "sampleKey1",
                    "Value": "sampleValue1"
                }
            ]
        }

    def test_make_web(self):
        pass

    def test_make_internal(self):
        pass

    def test_transform_attribute(self):
        sample_attribute = [{'name': 'x', 'value': 'y'}, {'name': 'xx', 'value': 'yy'}]
        v = elb.transform_attribute(sample_attribute)
        assert v == [{'Name': 'x', 'Value': 'y'}, {'Name': 'xx', 'Value': 'yy'}]

    def test_recurse_kwargs_list(self):
        sample_kwargs = {'topic_name': 'SampleTopic', 'display_name': 'MySnSTopic',
                         'subscription': [{'endpoint': {'ref': 'OpsGenieEndpoint'}, 'protocol': 'https'},
                                          {'endpoint': 'htps://sampleSite.com', 'protocol': 'http'}]}
        sample_kwargs_no_suscription = {'topic_name': 'SampleTopic', 'display_name': 'MySnSTopic'}

        v = sns.recurse_kwargs_list('subscription', sns.Subscription, **sample_kwargs)
        assert str(
            v) == "[Subscription([('Endpoint', {'ref': 'OpsGenieEndpoint'}), ('Protocol', 'https')]), Subscription([('Endpoint', 'htps://sampleSite.com'), ('Protocol', 'http')])]"

        v = sns.recurse_kwargs_list('subscription', sns.Subscription, **sample_kwargs_no_suscription)
        assert v is None
