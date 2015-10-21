from cfn_pyplates import core, functions
from ec2 import BlockDevice, BlockDeviceMapping


class MetricsCollection(core.JSONableDict):
    """
        Creates a Block Device Mapping

        :param granularity: String
        :param kwargs: metrics - [ String, ... ]
        """

    def __init__(self,
                 granularity,
                 **kwargs
                 ):
        super(MetricsCollection, self).__init__()
        self['Granularity'] = granularity
        if 'metrics' in kwargs:
            self['Metrics'] = kwargs.get('metrics')


class NotificationConfigurations(core.JSONableDict):
    """
        Creates a Block Device Mapping

        :param notifcation_type: [ String, ... ]
        :param topic_arn: String
    """
    def __init__(self,
                 notifcation_type,
                 topic_arn
                 ):
        super(NotificationConfigurations, self).__init__()
        self['NotificationTypes'] = notifcation_type
        self['TopicARN'] = topic_arn


class Tag(core.JSONableDict):
    """
        Create ASG Tag

        :param key: String
        :param value: String
        :param propagate_at_launch: Boolean
        """

    def __init__(self,
                 key,
                 value,
                 propagate_at_launch
                 ):
        super(Tag, self).__init__()
        self['Key'] = key
        self['Value'] = value
        self['PropagateAtLaunch'] = propagate_at_launch


class LaunchConfiguration(core.Resource):
    """
        Creates a Launch Configuration

        :param name: String
        :param ami_id: String
        :param instance_type: String

        kwargs
            - public_ip: Boolean
            - block_devices: [ BlockDeviceMapping, ... ]
            - classic_link_vpc_id: String
            - classic_link_vpc_security_groups: [ String, ... ],
            - ebs_optimized: Boolean
            - iam_role: String
            - instance_id: String
            - monitoring: Boolean
            - kernel_id: String
            - key_pair: String
            - placement_tenancy: String
            - ramdisk_id: String
            - security_groups: [ SecurityGroup, ... ]
            - spot_price: String
            - user_data_script: String
            - attributes: { key: value, ... }
    """
    def __init__(
            self,
            name,
            ami_id,
            instance_type,
            **kwargs
    ):
        if "classic_link_vpc_id" in kwargs and "classic_link_vpc_security_groups" not in kwargs:
            raise RuntimeError("Classic Link VPC Sercurity Groups (classic_link_vpc_security_groups) "
                               "required with Class Link VPC ID (classic_link_vpc_id).")

        attributes = kwargs.get("attributes")

        properties = {
            'ImageId': ami_id,
            'InstanceType': instance_type
        }

        if 'block_devices' in kwargs:
            devices = kwargs.get('block_devices')
            block_devices = []
            for device, args in devices.items():
                if 'ebs' in args:
                    args['ebs'] = BlockDevice(**args['ebs'])
                block_devices.append(BlockDeviceMapping(device, **args))
            properties['BlockDeviceMappings'] = block_devices

        if "public_ip" in kwargs:
            properties['AssociatePublicIpAddress'] = kwargs.get("public_ip")  # default=False
        if "classic_link_vpc_id" in kwargs:
            properties['ClassicLinkVPCId'] = kwargs.get("classic_link_vpc_id")
        if "classic_link_vpc_security_groups" in kwargs:
            properties['ClassicLinkVPCSecurityGroups'] = kwargs.get("classic_link_vpc_security_groups")
        if "ebs_optimized" in kwargs:
            properties['EbsOptimized'] = kwargs.get("ebs_optimized")  # default=False
        if "iam_role" in kwargs:
            properties['IamInstanceProfile'] = kwargs.get("iam_role")
        if "instance_id" in kwargs:
            properties['InstanceId'] = kwargs.get("instance_id")
        if "monitoring" in kwargs:
            properties['InstanceMonitoring'] = kwargs.get("monitoring")  # default=True
        if "kernel_id" in kwargs:
            properties['KernelId'] = kwargs.get("kernel_id")
        if "key_pair" in kwargs:
            properties['KeyName'] = kwargs.get("key_pair")
        if "placement_tenancy" in kwargs:
            properties['PlacementTenancy'] = kwargs.get("placement_tenancy")
        if "private_ip" in kwargs:
            properties['PlacementGroupName'] = kwargs.get("private_ip")
        if "ramdisk_id" in kwargs:
            properties['RamdiskId'] = kwargs.get("ramdisk_id")
        if "security_groups" in kwargs:
            properties['SecurityGroups'] = kwargs.get("security_groups")
        if "spot_price" in kwargs:
            properties['SpotPrice'] = kwargs.get("spot_price")
        if "user_data_script" in kwargs:
            properties['UserData'] = functions.base64(kwargs.get("user_data_script"))

        super(LaunchConfiguration, self).__init__(name, 'AWS::AutoScaling::LaunchConfiguration', properties, attributes)


class AutoScalingGroup(core.Resource):
    """
        Creates an AutoScaling Group

        :param name: String
        :param max_size: String
        :param min_size: String

        kwargs
            - availability_zones: [ String, ... ]
            - cooldown: String
            - desired_capacity: String
            - health_check_grace_period: Integer
            - health_check_type: String
            - instance_id: String
            - launch_configuration: String
            - load_balancer_names: [ String, ... ]
            - metrics_collection: [ MetricsCollection, ... ]
            - notification_configs: [ NotificationConfigurations, ... ]
            - placement_group: String
            - tags: [ Tag, ...]
            - termination_policies: [ String, ..., ]
            - vpc_zone_identifier: [ String, ... ]
            - attributes: { key: value, ... }
    """
    def __init__(
            self,
            name,
            max_size,
            min_size,
            **kwargs
    ):
        if "instance_id" not in kwargs and "launch_configuration" not in kwargs:
            raise RuntimeError(
                "Instance ID (instance_id) or Launch Configuration Name (launch_configuration) required.")

        if "availability_zones" not in kwargs and "vpc_zone_identifier" not in kwargs:
            raise RuntimeError("Availability Zones (availability_zones) or VPC Zone Identifier (vpc_zone_identifier) "
                               "required.")

        attributes = kwargs.get("attributes", dict())

        properties = {
            'MaxSize': max_size,
            'MinSize': min_size
        }
        if "metrics_collection" in kwargs:
            metrics_collection = kwargs.get('metrics_collection')
            metrics_collections = []
            for collection in metrics_collection:
                metrics_collections.append(MetricsCollection(**collection))
            properties['MetricsCollection'] = metrics_collections

        if "notification_configs" in kwargs:
            notification_configs = kwargs.get("notification_configs")
            configs = []
            for config in notification_configs:
                configs.append(NotificationConfigurations(**config))
            properties['NotificationConfigurations'] = configs

        if "launch_configuration" in kwargs:
            launch_configuration = kwargs.get("launch_configuration")
            try:
                for key in launch_configuration.keys():
                    if key == "ref":
                        properties['LaunchConfigurationName'] = functions.ref(launch_configuration[key])
                    elif key == "name":
                        properties['LaunchConfigurationName'] = launch_configuration[key]
            except:
                properties['LaunchConfigurationName'] = kwargs.get("launch_configuration")

        if "load_balancer_names" in kwargs:
            load_balancers = []
            load_balancer_names = kwargs.get("load_balancer_names")
            try:
                for key, values in load_balancer_names.items():
                    for value in values:
                        if key == "ref":
                            load_balancers.append(functions.ref(value))
                        elif key == "name":
                            load_balancers.append(value)
                properties['LoadBalancerNames'] = load_balancers
            except:
                properties['LoadBalancerNames'] = kwargs.get("load_balancer_names")

        if 'tags' in kwargs:
            t = kwargs.get('tags')
            tags = []
            for tag in t:
                tags.append(Tag(**tag))
            properties['Tags'] = tags

        if "availability_zones" in kwargs:
            properties['AvailabilityZones'] = kwargs.get("availability_zones")
        if "cooldown" in kwargs:
            properties['Cooldown'] = kwargs.get("cooldown")
        if "desired_capacity" in kwargs:
            properties['DesiredCapacity'] = kwargs.get("desired_capacity")
        if "health_check_grace_period" in kwargs:
            properties['HealthCheckGracePeriod'] = kwargs.get("health_check_grace_period")
        if "health_check_type" in kwargs:
            properties['HealthCheckType'] = kwargs.get("health_check_type")
        if "instance_id" in kwargs:
            properties['InstanceId'] = kwargs.get("instance_id")
        if "placement_group" in kwargs:
            properties['PlacementGroup'] = kwargs.get("placement_group")
        if "termination_policies" in kwargs:
            properties['TerminationPolicies'] = kwargs.get("termination_policies")
        if "vpc_zone_identifier" in kwargs:
            properties['VPCZoneIdentifier'] = kwargs.get("vpc_zone_identifier")

        super(AutoScalingGroup, self).__init__(name, 'AWS::AutoScaling::AutoScalingGroup', properties, attributes)


class ScalingPolicy(core.Resource):
    """
        Creates an AutoScaling Group

        :param adjustment_type: String
        :param asg_name: String
        :param scaling_adjustment: String

        kwargs
         - cooldown: String
         - in_adjustment_step: String
    """
    def __init__(
            self,
            name,
            adjustment_type,
            asg_name,
            scaling_adjustment,
            **kwargs
    ):
        attributes = kwargs.get("attributes", dict())

        properties = {
            'AdjustmentType': adjustment_type,
            'AutoScalingGroupName': asg_name,
            'ScalingAdjustment': scaling_adjustment
        }

        if "cooldown" in kwargs:
            properties['Cooldown'] = kwargs.get("cooldown")
        if "min_adjustment_step" in kwargs:
            properties['MinAdjustmentStep'] = kwargs.get("min_adjustment_step")

        super(ScalingPolicy, self).__init__(name, 'AWS::AutoScaling::ScalingPolicy', properties, attributes)


class ScheduledAction(core.Resource):
    """
        Creates an AutoScaling Group

        :param asg_name: String

        kwargs
             - desired_capacity: Integer
             - end_time: Time stamp (e.g. 2010-06-01T00:00:00Z)
             - max_size: Integer
             - min_size: Integer
             - recurrence: String (e.g. cron)
             - start_time: Time stamp (e.g. 2010-06-01T00:00:00Z)
    """
    def __init__(
            self,
            name,
            asg_name,
            **kwargs
    ):
        attributes = kwargs.get("attributes", dict())

        properties = {
            'AutoScalingGroupName': asg_name
        }

        if "desired_capacity" in kwargs:
            properties['DesiredCapacity'] = kwargs.get("desired_capacity")
        if "end_time" in kwargs:
            properties['EndTime'] = kwargs.get("end_time")
        if "max_size" in kwargs:
            properties['MaxSize'] = kwargs.get("max_size")
        if "min_size" in kwargs:
            properties['MinSize'] = kwargs.get("min_size")
        if "recurrence" in kwargs:
            properties['Recurrence'] = kwargs.get("recurrence")
        if "start_time" in kwargs:
            properties['StartTime'] = kwargs.get("start_time")

        super(ScheduledAction, self).__init__(name, 'AWS::AutoScaling::ScheduledAction', properties, attributes)
