from cfn_pyplates import core, functions
from respawn import util


class BlockDeviceMapping(core.JSONableDict):
    """
        Creates a Block Device Mapping

        :param device_name: String

        kwargs
            - ebs: PrivateIpSpecification
            - no_device: Boolean
            - virtual_name: String
        """
    def __init__(
            self,
            device_name,
            **kwargs
    ):
        if 'ebs' not in kwargs and 'virtual_name' not in kwargs and 'no_device' not in kwargs:
            raise RuntimeError("Ebs (ebs) or Virtual Name (virtual_name) required.")
        if 'ebs' in kwargs and 'virtual_name' in kwargs:
            raise RuntimeError("Only one of Ebs (ebs) and Virtual Name (virtual_name) can be specified.")

        super(BlockDeviceMapping, self).__init__()

        self['DeviceName'] = device_name
        if 'ebs' in kwargs:
            self['Ebs'] = kwargs.get('ebs')
        if 'no_device' in kwargs:
            if kwargs.get('no_device'):
                self['NoDevice'] = {}
        if 'virtual_name' in kwargs:
            self['VirtualName'] = kwargs.get('virtual_name')


class BlockDevice(core.JSONableDict):
    """
        Creates a Block Device

        kwargs
            - delete_on_termination: Boolean
            - iops: Integer
            - snapshot_id: String
            - size: Integer
            - type: String
    """
    def __init__(
            self,
            **kwargs
    ):
        if "snapshot_id" not in kwargs and "size" not in kwargs:
            raise RuntimeError("Block Device requires Snapshot Id (snapshot_id) or Size (size).")
        if "volume_type" in kwargs:
            if kwargs.get("volume_type") == "io1" and "iops" not in kwargs:
                raise RuntimeError("Iops (iops) required if Volume Type is io1.")

        super(BlockDevice, self).__init__()

        if 'delete_on_termination' in kwargs:
            self['DeleteOnTermination'] = kwargs.get('delete_on_termination')
        if 'iops' in kwargs:
            self['Iops'] = kwargs.get('iops')
        if 'snapshot_id' in kwargs:
            self['SnapshotId'] = kwargs.get('snapshot_id')
        if 'size' in kwargs:
            self['VolumeSize'] = kwargs.get('size')
        if 'type' in kwargs:
            self['VolumeType'] = kwargs.get('type')


class NetworkInterfaces(core.JSONableDict):
    """
        Creates a Network Interface

        :param device_index: String

        kwargs
            - public_ip: Boolean
            - delete_on_termination: Boolean
            - description: String
            - device_index:  String
            - group_set:  [ String, ... ]
            - interface_id:  String
            - private_ip:  String
            - private_ips:  [ PrivateIpSpecification, ... ]
            - secondary_private_ip_count:  Integer
            - subnet_id:  String
        """
    def __init__(
            self,
            device_index,
            **kwargs
    ):
        if 'subnet_id' not in kwargs and 'interface_id' not in kwargs:
            raise RuntimeError('NetworkInterface requires Subnet Id (subnet_id) if Interface Id (interface_id) '
                               'not specified')

        super(NetworkInterfaces, self).__init__()

        self['DeviceIndex'] = device_index
        if 'public_ip' in kwargs:
            self['AssociatePublicIpAddress'] = kwargs.get('public_ip')
        if 'delete_on_termination' in kwargs:
            self['DeleteOnTermination'] = kwargs.get('delete_on_termination')
        if 'description' in kwargs:
            self['Description'] = kwargs.get('description')
        if 'group_set' in kwargs:
            self['GroupSet'] = kwargs.get('group_set')
        if 'interface_id' in kwargs:
            self[''] = kwargs.get('interface_id')
        if 'private_ip' in kwargs:
            self['PrivateIpAddress'] = kwargs.get('private_ip')
        if 'private_ips' in kwargs:
            self['PrivateIpAddresses'] = kwargs.get('private_ips')
        if 'secondary_private_ip_count' in kwargs:
            self['SecondaryPrivateIpAddressCount'] = kwargs.get('secondary_private_ip_count')
        if 'subnet_id' in kwargs:
            self['SubnetId'] = kwargs.get('subnet_id')


class PrivateIpSpecification(core.JSONableDict):
    """
        Creates a Private IP Specification

        :param private_ip: String
        :param primary: Boolean
        """
    def __init__(
            self,
            private_ip,
            primary
    ):
        super(PrivateIpSpecification, self).__init__()

        self['PrivateIpAddress'] = private_ip
        self['Primary'] = primary


class MountPoint(core.JSONableDict):
    """
        Create Mount Point

        :param device: String
        :param volume_id: String
        """
    def __init__(
            self,
            device,
            volume_id
    ):
        super(MountPoint, self).__init__()

        self['Device'] = device
        self['VolumeId'] = volume_id


class SecurityGroupIngress(core.JSONableDict):
    def __init__(
            self,
            from_port,
            ip_protocol,
            to_port,
            **kwargs
    ):
        """
        Create Security Group Ingress

        :param from_port: String
        :param ip_protocol: String
        :param to_port: String

        kwargs
            - cidr_ip: String
            - source_security_group_id: String
            - source_security_group_name: String
            - source_security_group_owner_id: String
        """

        if "cider_ip" in kwargs and ("source_security_group_name" in kwargs or "source_security_group_id" in kwargs):
            raise RuntimeError("Source Security Group Name (source_security_group_name) or Source Security Group Id "
                               "(source_security_group_id) cannot be specified with Cider IP (cider_ip)")

        if "source_security_group_name" in kwargs and "source_security_group_id" in kwargs:
            raise RuntimeError("Source Security Group Name (source_security_group_name) or Source Security Group Id "
                               "(source_security_group_id) cannot both be specified.")

        super(SecurityGroupIngress, self).__init__()

        self['FromPort'] = from_port
        self['IpProtocol'] = ip_protocol
        self['ToPort'] = to_port

        if "cider_ip" in kwargs:
            self['CidrIp'] = kwargs.get("cider_ip")
        if "source_security_group_name" in kwargs:
            self['SourceSecurityGroupName'] = kwargs.get("source_security_group_name")
        if "source_security_group_id" in kwargs:
            self['SourceSecurityGroupId'] = kwargs.get("source_security_group_id")
        if "source_security_group_owner_id" in kwargs:
            self['SourceSecurityGroupOwnerId'] = kwargs.get("source_security_group_owner_id")


class SecurityGroupEgress(core.JSONableDict):
    def __init__(
            self,
            from_port,
            ip_protocol,
            to_port,
            **kwargs
    ):
        """
        Create Security Group Egress

        :param from_port: String
        :param ip_protocol: String
        :param to_port: String

        kwargs
            - cidr_ip: String
            - destination_security_group_id:  String
        """

        if "cider_ip" in kwargs and "destination_security_group_id" in kwargs:
            raise RuntimeError("Destination Security Group Id (destination_security_group_id) cannot be specified "
                               "with Cider IP (cider_ip)")

        super(SecurityGroupEgress, self).__init__()

        self['FromPort'] = from_port
        self['IpProtocol'] = ip_protocol
        self['ToPort'] = to_port

        if "cider_ip" in kwargs:
            self['CidrIp'] = kwargs.get("cider_ip")
        if "destination_security_group_id" in kwargs:
            self['DestinationSecurityGroupId'] = kwargs.get("destination_security_group_id")


class Tag(core.JSONableDict):
    """
        Create EC2 Tag

        :param key: String
        :param value: String
        """

    def __init__(
            self,
            key,
            value
    ):
        super(Tag, self).__init__()
        self['Key'] = key
        self['Value'] = value


class Volumes(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Volumes is an embedded property of the AWS::EC2::Instance resource that describes the
    subscription endpoints for a topic.

    :param endpoint: String,
    :param protocol: String
    """
    def __init__(self, **kwargs):
        super(Volumes, self).__init__(None, 'Volumes')
        self._set_property('Device', kwargs.get('device'))
        try:
            for key in kwargs.get('volume_id').keys():
                    if key == "ref":
                        self._set_property('VolumeId', functions.ref(kwargs.get('volume_id')[key]))
                    elif key == "name":
                        self._set_property('VolumeId', kwargs.get('volume_id')[key])
        except:
            self._set_property('VolumeId', kwargs.get('volume_id'))


class Instance(core.Resource):
    """
        Creates an EC2 Instance

        :param name: String
        :param ami_id: String

        kwargs
            - availability_zone: String
            - block_devices: [ BlockDeviceMapping , ... ]
            - disable_api_termination: Boolean
            - ebs_optimized: Boolean
            - iam_role: String
            - instance_shutdown_behavior: String
            - instance_type: String
            - kernel_id: String
            - key_pair: String
            - monitoring: Boolean
            - network_interfaces: [ NetworkInterface, ... ]
            - placement_group: String
            - private_ip: String
            - ramdisk_id: String
            - security_group_ids: [ String, ... ]
            - security_groups: [ String, ... ]
            - source_dest_check: Boolean
            - subnet: String
            - tags: [ Tag, ... ]
            - tenancy: String
            - user_data_script: String
            - volumes: [ MountPoint, ...]
            - attributes: { key: value, ... }
        """

    def __init__(
            self,
            name,
            ami_id,
            **kwargs
    ):
        properties = {
            'ImageId': ami_id,
        }

        if 'block_devices' in kwargs:
            devices = kwargs.get('block_devices')
            block_devices = []
            for device, args in devices.items():
                if 'ebs' in args:
                    args['ebs'] = BlockDevice(**args['ebs'])
                block_devices.append(BlockDeviceMapping(device, **args))
            properties['BlockDeviceMappings'] = block_devices

        if 'network_interfaces' in kwargs:
            interfaces = kwargs.get('network_interfaces')
            network_interfaces_list = []
            for interface, args in interfaces.items():
                if 'private_ips' in args:
                    private_ips = args['private_ips']
                    for i in range(len(private_ips)):
                        private_ips[i] = PrivateIpSpecification(**private_ips[i])
                network_interfaces_list.append(NetworkInterfaces(description=interface, **args))
            properties['NetworkInterfaces'] = network_interfaces_list

        if 'volumes' in kwargs:
            properties['Volumes'] = recurse_kwargs_list('volumes', Volumes, **kwargs)

        if 'tags' in kwargs:
            t = kwargs.get('tags')
            tags = []
            for tag in t:
                tags.append(Tag(**tag))
            properties['Tags'] = tags

        if "availability_zone" in kwargs:
            properties['AvailabilityZone'] = kwargs.get("availability_zone")
        if "disable_api_termination" in kwargs:
            properties['DisableApiTermination'] = kwargs.get("disable_api_termination")  # default=False
        if "ebs_optimized" in kwargs:
            properties['EbsOptimized'] = kwargs.get("ebs_optimized")  # default=False
        if "iam_role" in kwargs:
            properties['IamInstanceProfile'] = kwargs.get("iam_role")
        if "instance_shutdown_behavior" in kwargs:
            properties['InstanceInitiatedShutdownBehavior'] = kwargs.get("instance_shutdown_behavior")
        if "instance_type" in kwargs:
            properties['InstanceType'] = kwargs.get("instance_type")
        if "kernel_id" in kwargs:
            properties['KernelId'] = kwargs.get("kernel_id")
        if "key_pair" in kwargs:
            properties['KeyName'] = kwargs.get("key_pair")
        if "monitoring" in kwargs:
            properties['Monitoring'] = kwargs.get("monitoring")  # default=False
        if "placement_group" in kwargs:
            properties['PlacementGroupName'] = kwargs.get("placement_group")
        if "private_ip" in kwargs:
            properties['PrivateIpAddress'] = kwargs.get("private_ip")
        if "ramdisk_id" in kwargs:
            properties['RamdiskId'] = kwargs.get("ramdisk_id")
        if "security_group_ids" in kwargs:
            properties['SecurityGroupIds'] = kwargs.get("security_group_ids")
        if "security_groups" in kwargs:
            properties['SecurityGroups'] = kwargs.get("security_groups")
        if "source_dest_check" in kwargs:
            properties['SourceDestCheck'] = kwargs.get("source_dest_check")  # default=True
        if "subnet" in kwargs:
            properties['SubnetId'] = kwargs.get("subnet")
        if "tenancy" in kwargs:
            properties['Tenancy'] = kwargs.get("tenancy")  # default="default"
        if "user_data_script" in kwargs:
            properties['UserData'] = functions.base64(kwargs.get("user_data_script"))

        attributes = kwargs.get("attributes")

        super(Instance, self).__init__(name, 'AWS::EC2::Instance', properties, attributes)


def recurse_kwargs_list(parameter_name, class_name, **kwargs):
    if parameter_name in kwargs:
        parameter_list = kwargs.get(parameter_name)
        param_list = []
        for parameter in parameter_list:
            param_list.append(class_name(**parameter))
        return param_list
    else:
        pass


class Volume(core.Resource):
    """
        Creates an EC2 Volume

        :param name: String
        :param availability_zone: String

        kwargs
            - encrypted: Boolean
            - iops: Integer
            - kms_key_id: String
            - size: String
            - snapshot_id: String
            - tags:  [ Tag, ...]
            - volume_type:  String
            - attributes: { key: value, ... }
        """

    def __init__(
            self,
            name,
            availability_zone,
            **kwargs
    ):
        if kwargs.get("volume_type") == "io1" and "iops" not in kwargs:
            raise RuntimeError("Iops not specified for VolumeType of io1.")

        if "snapshot_id" not in kwargs and "size" not in kwargs:
            raise RuntimeError("Size of Volume not specified.")

        attributes = kwargs.get("attributes", dict())

        properties = {
            'AvailabilityZone': availability_zone,
        }

        if 'tags' in kwargs:
            t = kwargs.get('tags')
            tags = []
            for tag in t:
                tags.append(Tag(**tag))
            properties['Tags'] = tags

        if "encrypted" in kwargs:
            properties['Encrypted'] = kwargs.get("encrypted")  # default=False
        if "iops" in kwargs:
            properties['Iops'] = kwargs.get("iops")
        if "kms_key_id" in kwargs:
            properties['KmsKeyId'] = kwargs.get("kms_key_id")
        if "size" in kwargs:
            properties['Size'] = kwargs.get("size")
        if "snapshot_id" in kwargs:
            properties['SnapshotId'] = kwargs.get("snapshot_id")
        if "volume_type" in kwargs:
            properties['VolumeType'] = kwargs.get("volume_type")
        if "DeletionPolicy" not in attributes:
            attributes['DeletionPolicy'] = kwargs.get("deletion_policy", "Delete")  # Delete, Retain, Snapshot

        super(Volume, self).__init__(name, 'AWS::EC2::Volume', properties, attributes)


def transform_tags(attribute_list):
    updated_attribute_list = []
    for attribute_parameters in attribute_list:
        updated_attribute_list.append(
            {'Value': attribute_parameters.get('value'),
             'Key': attribute_parameters.get('key')})
    return updated_attribute_list


class NetworkInterface(core.Resource):
    def __init__(self,
                 name,
                 **kwargs
                 ):
        properties = {
            'Description': kwargs.get("description"),
            'GroupSet': kwargs.get("group_set"),
            'PrivateIpAddress': kwargs.get("private_ip_address"),
            'PrivateIPAddresses': kwargs.get("private_ip_addresses"),
            'SecondaryPrivateIpAddressCount': kwargs.get("secondary_private_ip_address_count"),
            'SourceDestCheck': kwargs.get("source_dest_check"),
            'SubnetId': kwargs.get("subnet_id"),
            'Tags': transform_tags(kwargs.get("tags"))
        }
        super(NetworkInterface, self).__init__(name, 'AWS::EC2::NetworkInterface', properties)


class NetworkInterfaceAttachment(core.Resource):
    def __init__(
            self,
            name,
            **kwargs
    ):

        if "device_index" not in kwargs and "instance_id" not in kwargs and "network_interface_id" not in kwargs:
            raise ValueError('DeviceIndex/InstanceId/NetworkInterfaceId parameters for NetworkInterfaceAttachment '
                             'are required to hook up a network interface to an instance.')

        properties = {
            'DeviceIndex': kwargs.get("device_index"),
            'InstanceId': kwargs.get("instance_id"),
            'NetworkInterfaceId': kwargs.get("network_interface_id")
        }

        if "delete_on_termination" in kwargs:
            properties['DeleteOnTermination'] = kwargs.get("delete_on_termination")  # default=False

        super(NetworkInterfaceAttachment, self).__init__(name, 'AWS::EC2::NetworkInterfaceAttachment', properties)


class SecurityGroup(core.Resource):
    """
        Creates a Security Group

        :param name: String
        :param group_description: String

        kwargs
            - security_group_egress: [ Security Group Rule, ... ]
            - security_group_ingress: [ Security Group Rule, ... ]
            - tags: [ Tag, ... ]
            - vpc_id: String
        """

    def __init__(
            self,
            name,
            group_description,
            **kwargs
    ):
        attributes = kwargs.get("attributes", dict())

        properties = {
            'GroupDescription': group_description
        }

        if "security_group_egress" in kwargs:
            security_group_egress = []
            for sg in kwargs.get("security_group_egress").items():
                security_group_egress.append(SecurityGroupEgress(**sg))
            properties['SecurityGroupEgress'] = security_group_egress

        if "security_group_ingress" in kwargs:
            security_group_ingress = []
            for sg in kwargs.get("security_group_ingress").items():
                security_group_ingress.append(SecurityGroupIngress(**sg))
            properties['SecurityGroupIngress'] = security_group_ingress

        if 'tags' in kwargs:
            t = kwargs.get('tags')
            tags = []
            for tag in t:
                tags.append(Tag(**tag))
            properties['Tags'] = tags

        if "vpc_id" in kwargs:
            properties['VpcId'] = kwargs.get("vpc_id")

        super(SecurityGroup, self).__init__(name, 'AWS::EC2::SecurityGroup', properties, attributes)