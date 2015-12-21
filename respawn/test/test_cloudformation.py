import unittest
from respawn import cloudformation


class TestCloudformation(unittest.TestCase):
    def test_add_launchconfig(self):
        sample_kwargs = {'ami_id': 'testAMIWin01', 'realm': 'protected', 'availability_zone': 'us-east-1d'
            , 'ebs_optimized': False, 'public_ip': True,
                         'instance_type': 't2.small', 'block_devices': {'/dev/sdd': {'no_device': True}, '/dev/sdb': {
                'ebs': {'snapshot_id': 'id-testSnapshot'}}, '/dev/sdc': {'virtual_name': 'ephemeral0'},
                                                                        '/dev/sda': {
                                                                            'ebs': {'encrypted': False, 'iops': 1000,
                                                                                    'type': 'standard',
                                                                                    'delete_on_termination': False,
                                                                                    'size': 100}}},
                         'key_pair': 'testKey', 'security_groups': ['sg-test01', 'sg-test02'],
                         'security_group_ids': ['sg-test01', 'sg-test02'], 'iam_role': 'sampleIamRole',
                         "user_data_script": "sample_user_data_script"}
        cft = cloudformation.Template()
        v = cft.add_launch_config("name", **sample_kwargs)
        assert v['Properties'] == {
            "UserData": {
                "Fn::Base64": "sample_user_data_script"
            },
            "ImageId": "testAMIWin01",
            "KeyName": {
                "Ref": "nameKeyPair"
            },
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sdd",
                    "NoDevice": {}
                },
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs": {
                        "SnapshotId": "id-testSnapshot"
                    }
                },
                {
                    "DeviceName": "/dev/sdc",
                    "VirtualName": "ephemeral0"
                },
                {
                    "DeviceName": "/dev/sda",
                    "Ebs": {
                        "DeleteOnTermination": False,
                        "Iops": 1000,
                        "VolumeSize": 100
                    }
                }
            ],
            "EbsOptimized": False,
            "SecurityGroups": [
                "sg-test01",
                "sg-test02"
            ],
            "IamInstanceProfile": {
                "Ref": "nameIamRole"
            },
            "InstanceType": "t2.small",
            "AssociatePublicIpAddress": True
        }

    def test_add_autoscaling(self):
        sample_kwargs = {'hostname': 'testASGInstance', 'realm': 'protected',
                         'vpc_zone_identifier': ['subnet-0000000', 'subnet-1111111', 'subnet-2222222'], 'tags': [
                {'propagate_at_launch': True, 'value': 'sample/service/name', 'key': 'service_name'},
                {'propagate_at_launch': True, 'value': 'int', 'key': 'env'},
                {'propagate_at_launch': True, 'value': {'Ref': 'TagEAP'}, 'key': 'eap'},
                {'propagate_at_launch': True, 'value': {'Fn::Join': ['', ['virsin', 'sampleName']]}, 'key': 'Name'}],
                         'service_name': 'sample/service/name',
                         'load_balancer_names': {'ref': ['testWeb'], 'name': ['testWebLBName']},
                         'launch_configuration': {'ref': 'testWindowsLaunchConfig1'}, 'min_size': 1,
                         'desired_capacity': 10, 'availability_zones': ['us-east-1b', 'us-east-1c', 'us-east-1d'],
                         'max_size': 10}

        cft = cloudformation.Template()
        v = cft.add_autoscaling_group("name", **sample_kwargs)
        assert v['Properties'] == {"DesiredCapacity": 10,
                                   "Tags": [
                                       {
                                           "Key": "service_name",
                                           "Value": "sample/service/name",
                                           "PropagateAtLaunch": True
                                       },
                                       {
                                           "Key": "env",
                                           "Value": "int",
                                           "PropagateAtLaunch": True
                                       },
                                       {
                                           "Key": "eap",
                                           "Value": {
                                               "Ref": "TagEAP"
                                           },
                                           "PropagateAtLaunch": True
                                       },
                                       {
                                           "Key": "Name",
                                           "Value": {
                                               "Fn::Join": [
                                                   "",
                                                   [
                                                       "virsin",
                                                       "sampleName"
                                                   ]
                                               ]
                                           },
                                           "PropagateAtLaunch": True
                                       }
                                   ],
                                   "LoadBalancerNames": {
                                       "ref": [
                                           "testWeb"
                                       ],
                                       "name": [
                                           "testWebLBName"
                                       ]
                                   },
                                   "MinSize": 1,
                                   "MaxSize": 10,
                                   "VPCZoneIdentifier": [
                                       "subnet-0000000",
                                       "subnet-1111111",
                                       "subnet-2222222"
                                   ],
                                   "LaunchConfigurationName": {
                                       "ref": "testWindowsLaunchConfig1"
                                   },
                                   "AvailabilityZones": [
                                       "us-east-1b",
                                       "us-east-1c",
                                       "us-east-1d"
                                   ]
                                   }

    def test_add_instance(self):
        sample_kwargs = {'ami_id': 'sampleAmiId', 'realm': 'protected',
                         'tags': [{'key': 'testTag1', 'value': 'testTagValue1'}],
                         'service_name': 'djin/metdata/test/svc', 'hostname': 'testInstance',
                         'instance_type': 'm3.xlarge', 'block_devices': {'/dev/sdd': {'no_device': True},
                                                                         '/dev/sdb': {
                                                                             'ebs': {'snapshot_id': 'id-testSnapshot'}},
                                                                         '/dev/sdc': {'virtual_name': 'ephemeral0'},
                                                                         '/dev/sda': {
                                                                             'ebs': {'encrypted': False, 'iops': 1000,
                                                                                     'type': 'standard',
                                                                                     'delete_on_termination': False,
                                                                                     'size': 100}}},
                         'iam_role': 'sampleIamRole',
                         'volumes': [{'device': 'testvolume', 'volume_id': {'ref': '/dev/sdk'}},
                                     {'device': 'sample_dev', 'volume_id': 'sample_vol'}], 'network_interfaces': {
                'Network Interface 1': {'public_ip': True, 'subnet_id': 'id-testSubnet1', 'device_index': 0,
                                        'private_ips': [{'private_ip': '1.1.1.1', 'primary': False},
                                                        {'private_ip': '2.2.2.2', 'primary': True}],
                                        'delete_on_termniation': True}}, 'ebs_optimized': True,
                         'ramdisk_id': 'testRamDiskID', 'source_dest_check': True}

        cft = cloudformation.Template()
        v = cft.add_instance("name", **sample_kwargs)
        assert v['Properties'] == {
            "SourceDestCheck": True,
            "Tags": [
                {
                    "Key": "testTag1",
                    "Value": "testTagValue1"
                }
            ],
            "ImageId": "sampleAmiId",
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sdd",
                    "NoDevice": {}
                },
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs": {
                        "SnapshotId": "id-testSnapshot"
                    }
                },
                {
                    "DeviceName": "/dev/sdc",
                    "VirtualName": "ephemeral0"
                },
                {
                    "DeviceName": "/dev/sda",
                    "Ebs": {
                        "DeleteOnTermination": False,
                        "Iops": 1000,
                        "VolumeSize": 100
                    }
                }
            ],
            "EbsOptimized": True,
            "Volumes": [
                {
                    "Device": "testvolume",
                    "VolumeId": {
                        "ref": "/dev/sdk"
                    }
                },
                {
                    "Device": "sample_dev",
                    "VolumeId": "sample_vol"
                }
            ],
            "RamdiskId": "testRamDiskID",
            "IamInstanceProfile": {
                "Ref": "nameIamRole"
            },
            "InstanceType": "m3.xlarge",
            "NetworkInterfaces": [
                {
                    "DeviceIndex": 0,
                    "AssociatePublicIpAddress": True,
                    "Description": "Network Interface 1",
                    "PrivateIpAddresses": [
                        {
                            "PrivateIpAddress": "1.1.1.1",
                            "Primary": False
                        },
                        {
                            "PrivateIpAddress": "2.2.2.2",
                            "Primary": True
                        }
                    ],
                    "SubnetId": "id-testSubnet1"
                }
            ]
        }

    def test_add_load_balancer(self):
        sample_attribute = {'service_name': 'service/name', 'instances': ['10.23.23.23', '13.12.13.14'],
                            'cross_zone': True, 'security_groups': ['sg-1111111', 'sg-2222222'],
                            'access_logging_policy': {'s3_bucket_prefix': 's3_bucket_prefix1', 'enabled': True,
                                                      'emit_interval': 20, 's3_bucket_name': 's3_bucket_name1'},
                            'availability_zones': [{'Fn::GetAZs': ''}, 'availability zone 2'], 'realm': 'protected',
                            'load_balancer_name': 'unique_name', 'app_cookie_stickiness_policy': [
                {'cookie_name': 'cookie_name1', 'policy_name': 'policy_name1'},
                {'cookie_name': 'cookie_name2', 'policy_name': 'policy_name2'}],
                            'scheme': 'internet-facing', 'connection_draining_policy': {'enabled': True, 'timeout': 10},
                            'health_check': {'healthy_threshold': 'String', 'interval': 'String', 'target': 'String',
                                             'timeout': 'String', 'unhealthy_threshold': 'String'},
                            'tags': [{'key': 'key1', 'value': 'value1'}, {'key': 'key2', 'value': 'value2'}],
                            'connection_settings': {'idle_timeout': 40}, 'lb_cookie_stickiness_policy': [
                {'cookie_expiration_period': 'String', 'policy_name': 'policy_name1'},
                {'cookie_expiration_period': 'String', 'policy_name': 'policy_name2'}], 'listeners': {
                'https': {'instance_port': 84, 'instance_protocol': 'tcp', 'load_balancer_port': 83},
                'tcp': {'instance_port': 8443, 'instance_protocol': 'http', 'load_balancer_port': 8443}}, 'policies': [
                {'attribute': [{'name': 'name1', 'value': 'value1'}, {'name': 'name2', 'value': 'value2'}],
                 'instance_ports': ['2121', '2424'], 'load_balancer_ports': ['32323', '2424'],
                 'policy_type': 'SSLNegotiationPolicyType', 'policy_name': 'policy_name'},
                {'attribute': [{'name': 'value1', 'value': 'value2'}], 'instance_ports': ['2121', '2424'],
                 'load_balancer_ports': ['32323', '2424'], 'policy_type': 'SSLNegotiationPolicyType',
                 'policy_name': 'policy_name1'}]}
        cft = cloudformation.Template()
        v = cft.add_load_balancer("name", **sample_attribute)
        assert v['Properties'] == {
            "AccessLoggingPolicy": {
                "EmitInterval": 20,
                "Enabled": True,
                "S3BucketName": "s3_bucket_name1",
                "S3BucketPrefix": "s3_bucket_prefix1"
            },
            "AppCookieStickinessPolicy": [
                {
                    "CookieName": "cookie_name1",
                    "PolicyName": "policy_name1"
                },
                {
                    "CookieName": "cookie_name2",
                    "PolicyName": "policy_name2"
                }
            ],
            "AvailabilityZones": [
                {
                    "Fn::GetAZs": ""
                },
                "availability zone 2"
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
                "HealthyThreshold": "String",
                "Interval": "String",
                "Timeout": "String",
                "UnhealthyThreshold": "String",
                "Target": "String"
            },
            "Instances": [
                "10.23.23.23",
                "13.12.13.14"
            ],
            "LBCookieStickinessPolicy": [
                {
                    "PolicyName": "policy_name1",
                    "CookieExpirationPeriod": "String"
                },
                {
                    "PolicyName": "policy_name2",
                    "CookieExpirationPeriod": "String"
                }
            ],
            "LoadBalancerName": "unique_name",
            "Listeners": [
                {
                    "InstancePort": 8443,
                    "InstanceProtocol": "http",
                    "LoadBalancerPort": 8443,
                    "Protocol": "TCP"
                },
                {
                    "InstancePort": 84,
                    "InstanceProtocol": "tcp",
                    "LoadBalancerPort": 83,
                    "Protocol": "HTTPS"
                }
            ],
            "Policies": [
                {
                    "PolicyName": "policy_name",
                    "Attribute": [
                        {
                            "Name": "name1",
                            "Value": "value1"
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
                    "PolicyName": "policy_name1",
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
                "sg-1111111",
                "sg-2222222"
            ],
            "Tags": [
                {
                    "Key": "key1",
                    "Value": "value1"
                },
                {
                    "Key": "key2",
                    "Value": "value2"
                }
            ]
        }

    def test_add_volume(self):
        sample_kwargs = {'availability_zone': 'testAZ', 'encrypted': True, 'kms_key_id': 'testKMSKey',
                         'volume_type': 'standard', 'iops': 4000, 'deletion_policy': 'Retain',
                         'snapshot_id': 'testSnapshotID', 'tags': [{'key': 'testTag2', 'value': 'testTagValue2'}],
                         'size': 1000}
        cft = cloudformation.Template()
        v = cft.add_volume("name", **sample_kwargs)
        assert v['Properties'] == {
            "AvailabilityZone": "testAZ",
            "Tags": [
                {
                    "Key": "testTag2",
                    "Value": "testTagValue2"
                }
            ],
            "Encrypted": True,
            "VolumeType": "standard",
            "KmsKeyId": "testKMSKey",
            "SnapshotId": "testSnapshotID",
            "Iops": 4000,
            "Size": 1000
        }

    def test_add_cloudwatch(self):
        sample_kwargs = {'alarm_actions': ['String1', 'String2'], 'ok_actions': ['String', 'String2'],
                         'dimensions': [{'name': 'Metric dimension', 'value': 123},
                                        {'name': 'sampleName', 'value': {'ref': 'test_name'}}],
                         'evaluation_periods': 15,
                         'alarm_description': 'sample description', 'namespace': 'some_namespace',
                         'alarm_name': 'test_alarm', 'period': 12, 'actions_enabled': True,
                         'insufficient_data_actions': ['String', 'String2'], 'statistic': 'Average', 'threshold': 10,
                         'comparison_operator': 'String', 'unit': 'String', 'metric_name': 'some_name'}
        cft = cloudformation.Template()
        v = cft.add_cloud_watch_alarm("name", **sample_kwargs)
        assert v['Properties'] == {
            "ActionsEnabled": True,
            "AlarmActions": [
                "String1",
                "String2"
            ],
            "AlarmDescription": "sample description",
            "AlarmName": "test_alarm",
            "ComparisonOperator": "String",
            "EvaluationPeriods": 15,
            "InsufficientDataActions": [
                "String",
                "String2"
            ],
            "MetricName": "some_name",
            "Namespace": "some_namespace",
            "OKActions": [
                "String",
                "String2"
            ],
            "Period": 12,
            "Statistic": "Average",
            "Threshold": 10,
            "Unit": "String"
        }

    def test_add_network_interface(self):
        sample_kwargs = {'description': 'sample description',
                         'tags': [{'key': 'testTag2', 'value': 'testTagValue2'}, {'key': 'sampleKey',
                                                                                  'value': 'sampleValue'}],
                         'subnet_id': '131.3.13.1', 'group_set': ['group1', 'group2'],
                         'private_ips': [{'private_ip': '10.23.23.23', 'primary': True},
                                         {'private_ip': '12.13.3.4', 'primary': True}],
                         'private_ip': '10.20.03.20',
                         'secondary_private_ip_count': 4, 'source_dest_check': True}
        cft = cloudformation.Template()
        v = cft.add_network_interface("name", **sample_kwargs)

        assert v == {
            "Type": "AWS::EC2::NetworkInterface",
            "Properties": {
                "SourceDestCheck": True,
                "GroupSet": [
                    "group1",
                    "group2"
                ],
                "Description": "sample description",
                "Tags": [
                    {
                        "Key": "testTag2",
                        "Value": "testTagValue2"
                    },
                    {
                        "Key": "sampleKey",
                        "Value": "sampleValue"
                    }
                ],
                "PrivateIpAddresses": [
                    {
                        "Primary": True,
                        "PrivateIpAddress": "10.23.23.23"
                    },
                    {
                        "Primary": True,
                        "PrivateIpAddress": "12.13.3.4"
                    }
                ],
                "SecondaryPrivateIpAddressCount": 4,
                "SubnetId": "131.3.13.1",
                "PrivateIpAddress": "10.20.03.20"
            }
        }

    def test_add_network_interface_attachment(self):
        sample_kwargs = {'instance_id': 'sampleId', 'network_interface_id': ['sg-111111'], 'device_index': '1',
                         'delete_on_termination': False}
        cft = cloudformation.Template()
        v = cft.add_network_interface_attachment("name", **sample_kwargs)
        assert v['Properties'] == {
            "InstanceId": "sampleId",
            "DeviceIndex": "1",
            "NetworkInterfaceId": [
                "sg-111111"
            ],
            "DeleteOnTermination": False
        }

    def test_add_sns_topic(self):
        sample_kwargs = {'topic_name': 'SampleTopic', 'display_name': 'MySnSTopic',
                         'subscription': [{'endpoint': {'ref': 'OpsGenieEndpoint'}, 'protocol': 'https'},
                                          {'endpoint': 'htps://sampleSite.com', 'protocol': 'http'}]}
        cft = cloudformation.Template()
        v = cft.add_sns_topic("name", **sample_kwargs)
        assert v['Properties'] == {
            "DisplayName": "MySnSTopic",
            "Subscription": [
                {
                    "Endpoint": {
                        "ref": "OpsGenieEndpoint"
                    },
                    "Protocol": "https"
                },
                {
                    "Endpoint": "htps://sampleSite.com",
                    "Protocol": "http"
                }
            ],
            "TopicName": "SampleTopic"
        }

    def test_add_scheduled_action(self):
        sample_kwargs = {'min_size': 10, 'desired_capacity': 10, 'asg_name': 'sampleAsgName', 'max_size': 10,
                         'recurrence': '0 9 * * *'}
        cft = cloudformation.Template()
        v = cft.add_scheduled_action("name", **sample_kwargs)
        assert v['Properties'] == {
            "MinSize": 10,
            "Recurrence": "0 9 * * *",
            "MaxSize": 10,
            "AutoScalingGroupName": "sampleAsgName",
            "DesiredCapacity": 10
        }

    def test_add_parameter(self):
        sample_kwargs = {'default': '10.201.22.32', 'type': 'String', 'description': 'Creating test param'}
        cft = cloudformation.Template()
        v = cft.add_parameter("name", **sample_kwargs)
        assert v == {
            "Default": "10.201.22.32",
            "Type": "String",
            "Description": "Creating test param"
        }

    def test_add_rds(self):
        sample_kwargs = {'allocated_storage': 100, 'instance_class': 'db.m1.small', "engine": "mysql"}
        cft = cloudformation.Template()
        v = cft.add_rds_instance("name", **sample_kwargs)
        assert v == {
            "Type": "AWS::RDS::DBInstance",
            "Properties": {
                "Engine": "mysql",
                "DBInstanceClass": "db.m1.small",
                "AllocatedStorage": 100
            }
        }

    def test_add_lifecycle_hook(self):
        sample_kwargs = {'role_arn': 'SampleIAMRole', 'asg_name': {'Ref': 'SampleAutoScaleGroup'},
                         'lifecycle_transition': 'autoscaling:EC2_INSTANCE_TERMINATING',
                         'notification_target_arn': {'Ref': 'SampleSNSTopic'}}
        cft = cloudformation.Template()
        v = cft.add_lifecycle_hook("name", **sample_kwargs)
        assert v['Properties'] == {
            "NotificationTargetARN": {
                "Ref": "SampleSNSTopic"
            },
            "AutoScalingGroupName": {
                "Ref": "SampleAutoScaleGroup"
            },
            "RoleARN": "SampleIAMRole",
            "LifecycleTransition": "autoscaling:EC2_INSTANCE_TERMINATING"
        }

    def test_avail_zone(self):
        cft = cloudformation.Template()
        v = cft.create_availability_zone_param("name", "us-east-1")
        assert v == {'Ref': 'nameAvailabilityZone'}
