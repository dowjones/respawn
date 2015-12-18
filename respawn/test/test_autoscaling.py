import pytest
from respawn import autoscaling


def test_metrics_collection():
    # Successful creation of metrics collection
    metrics_collection = autoscaling.MetricsCollection("sample-gran", **{"metrics": "sample-metrics"})
    assert metrics_collection == {"Granularity": "sample-gran", "Metrics": "sample-metrics"}

    # Extra arguments
    with pytest.raises(TypeError):
        autoscaling.MetricsCollection("sample-gran", "Value1", True)


def test_notification_configurations():
    # Successful creation of notification configuration
    notification_configuration = autoscaling.NotificationConfigurations("sampleNotificationTypes", "sampleTopicArn")
    assert notification_configuration == ({"NotificationTypes": "sampleNotificationTypes", "TopicARN":
        "sampleTopicArn"})


def test_lifecycle_hooks():
    # Successful creation of hooks
    lifecycle_hooks = autoscaling.LifecycleHook("sampleName", "sampleASG", "sampleLifeCycle", "sampleNotTarget",
                                                "sampleRoleARN", **{"default_result": "sampleDefaultResult",
                                                                    "heartbeat_timeout": "sampleHeartBeat",
                                                                    "notification_metadata": "sampleNotificationMet"})
    assert lifecycle_hooks['Properties'] == {
        'AutoScalingGroupName': "sampleASG",
        'LifecycleTransition': "sampleLifeCycle",
        'NotificationTargetARN': "sampleNotTarget",
        'RoleARN': "sampleRoleARN",
        'DefaultResult': "sampleDefaultResult",
        "HeartbeatTimeout": "sampleHeartBeat",
        "NotificationMetadata": "sampleNotificationMet"
    }


def test_auto_scaling_policy():
    # successful auto scaling policy creation
    autoscaling_policy = autoscaling.AutoScalingGroup("name", "max", "min", **{"metrics_collection": [{'granularity':
                                                                                                           '1Minute'},
                                                                                                      {'metrics': [
                                                                                                          'Metric1',
                                                                                                          'Metric2'],
                                                                                                          'granularity': '1Minute'}],
                                                                               "notification_configs": [{
                                                                                   'notification_type': [
                                                                                       'Type1',
                                                                                       'Type2'],
                                                                                   'topic_arn': 'arn:aws:[service]:['
                                                                                                'region]:['
                                                                                                'account]:resourceType/resourcePath'}],
                                                                               "cooldown": "sampleCooldown",
                                                                               "health_check_grace_period":
                                                                                   "sampleCheckGracePeriod",
                                                                               "health_check_type":
                                                                                   "sampleHealthCheck",
                                                                               "instance_id": "sampleInstanceId",
                                                                               "placement_group":
                                                                                   "samplePlacementGroup",
                                                                               "termination_policies":
                                                                                   "sampleTerminationPolicy",
                                                                               "vpc_zone_identifier": "sampleVPC"})
    assert autoscaling_policy['Properties'] == {
        "VPCZoneIdentifier": "sampleVPC",
        "PlacementGroup": "samplePlacementGroup",
        "NotificationConfigurations": [
            {
                "NotificationTypes": [
                    "Type1",
                    "Type2"
                ],
                "TopicARN": "arn:aws:[service]:[region]:[account]:resourceType/resourcePath"
            }
        ],
        "InstanceId": "sampleInstanceId",
        "MinSize": "min",
        "MaxSize": "max",
        "Cooldown": "sampleCooldown",
        "TerminationPolicies": "sampleTerminationPolicy",
        "MetricsCollection": [
            {
                "Granularity": "1Minute"
            },
            {
                "Granularity": "1Minute",
                "Metrics": [
                    "Metric1",
                    "Metric2"
                ]
            }
        ],
        "HealthCheckGracePeriod": "sampleCheckGracePeriod",
        "HealthCheckType": "sampleHealthCheck"
    }


def test_scaling_policy():
    # testing scaling policy
    scaling_policy = autoscaling.ScalingPolicy("name", "sampleAdjustT", "sampleASG", "sampleScaling",
                                               **{"cooldown": "sampleCool", "min_adjustment_step": "MinAdjStep"})
    assert scaling_policy['Properties'] == {
        'AdjustmentType': "sampleAdjustT",
        'AutoScalingGroupName': "sampleASG",
        'ScalingAdjustment': "sampleScaling",
        'Cooldown': "sampleCool",
        'MinAdjustmentStep': "MinAdjStep"
    }


def test_launch_configuration():
    # testing launch configuration
    launch_config = autoscaling.LaunchConfiguration("name", "sampleAMI", "sampleInstance", **{"classic_link_vpc_id":
                                                                                                  "sample_classic_link_vpc_id",
                                                                                              "classic_link_vpc_security_groups": "sample_classicGroups",
                                                                                              "instance_id": "sample_instance_id",
                                                                                              "monitoring":
                                                                                                  "sample_monitoring",
                                                                                              "kernel_id":
                                                                                                  "sample_kernel_id",
                                                                                              "placement_tenancy":
                                                                                                  "sample_placementTenancy",
                                                                                              "private_ip": "samplePIP",
                                                                                              "ramdisk_id": "sampleRamdisk",
                                                                                              "spot_price":
                                                                                                  "SampleSpotPrice",
                                                                                              "user_data_script": "sample_user_data_script"})
    assert launch_config['Properties'] == {
        'ImageId': "sampleAMI",
        'InstanceType': "sampleInstance",
        'ClassicLinkVPCId': "sample_classic_link_vpc_id",
        'ClassicLinkVPCSecurityGroups': "sample_classicGroups",
        'InstanceId': "sample_instance_id",
        'InstanceMonitoring': "sample_monitoring",
        'KernelId': "sample_kernel_id",
        'PlacementTenancy': "sample_placementTenancy",
        'PlacementGroupName': "samplePIP",
        'RamdiskId': "sampleRamdisk",
        'SpotPrice': "SampleSpotPrice",
        'UserData': {'Fn::Base64': 'sample_user_data_script'}}
