import pytest
from respawn import ec2, errors


def test_tag():
    # Successful creation of tag
    tag = ec2.Tag("Key1", "Value1")
    assert tag == {"Key": "Key1", "Value": "Value1"}

    # Extra arguments
    with pytest.raises(TypeError):
        ec2.Tag("Key1", "Value1", True)


def test_block_device():
    # Successful creation of block device
    block_device = ec2.BlockDevice(snapshot_id="snap-xxxxxxxx", size=100,
                                   volume_type="io1", iops=1000, delete_on_termination=True)
    assert block_device == {
        "SnapshotId": "snap-xxxxxxxx",
        "VolumeSize": 100,
        "VolumeType": "io1",
        "Iops": 1000,
        "DeleteOnTermination": True}

    # No snapshot_id or size
    with pytest.raises(errors.RespawnResourceError):
        ec2.BlockDevice(volume_type="io1", iops=1000, delete_on_termination=True)

    # No iops with volume_type io1
    with pytest.raises(errors.RespawnResourceError):
        ec2.BlockDevice(snapshot_id="test_snapshot", size=100,
                        volume_type="io1", delete_on_termination=True)


def test_block_device_mapping():
    # Ebs block device mapping
    block_device_mapping = ec2.BlockDeviceMapping("/dev/sda", ebs=ec2.BlockDevice(**{"snapshot_id": "snap-xxxxxxxx"}))
    assert block_device_mapping == {"DeviceName": "/dev/sda", "Ebs": {"SnapshotId": "snap-xxxxxxxx"}}

    # Virtual name block device mapping
    block_device_mapping = ec2.BlockDeviceMapping("/dev/sda", virtual_name="ephemeral0")
    assert block_device_mapping == {"DeviceName": "/dev/sda", "VirtualName": "ephemeral0"}

    # No device block device mapping
    block_device_mapping = ec2.BlockDeviceMapping("/dev/sda", no_device=True)

    assert block_device_mapping == {"DeviceName": "/dev/sda", "NoDevice": {}}

    # Both ebs and virtual_name
    with pytest.raises(errors.RespawnResourceError):
        ec2.BlockDeviceMapping("/dev/sda",
                               ebs=dict(ec2.BlockDevice(**{"snapshot_id": "snap-xxxxxxxx"})),
                               virtual_name="ephemeral0")

    # No ebs, virtual_name, or no_device
    with pytest.raises(errors.RespawnResourceError):
        ec2.BlockDeviceMapping("/dev/sda")


def test_private_ip_specification():
    # Successful creation of private ip specification
    private_ip_specification = ec2.PrivateIpSpecification("1.1.1.1", True)
    assert private_ip_specification == {"PrivateIpAddress": "1.1.1.1", "Primary": True}

    # Extra arguments
    with pytest.raises(TypeError):
        ec2.PrivateIpSpecification("1.1.1.1", True, True)


def test_embedded_network_interface():
    # Successful creation of embedded network interface
    embedded_network_interface = ec2.EmbeddedNetworkInterface("1", public_ip=True, delete_on_termination=True,
                                                              description="test_description",
                                                              group_set=["test_group"],
                                                              interface_id="id-interface-test",
                                                              private_ip="1.1.1.1",
                                                              private_ips=[
                                                                  dict(ec2.PrivateIpSpecification("2.2.2.2", True))],
                                                              secondary_private_ip_count=2, subnet_id="id-subnet-test")

    assert embedded_network_interface == {
        "DeviceIndex": "1",
        "AssociatePublicIpAddress": True,
        "DeleteOnTermination": True,
        "Description": "test_description",
        "GroupSet": ["test_group"],
        "NetworkInterfaceId": "id-interface-test",
        "PrivateIpAddress": "1.1.1.1",
        "PrivateIpAddresses": [{"PrivateIpAddress": "2.2.2.2", "Primary": True}],
        "SecondaryPrivateIpAddressCount": 2,
        "SubnetId": "id-subnet-test"
    }

    # No subnet_id or interface_id
    with pytest.raises(errors.RespawnResourceError):
        ec2.EmbeddedNetworkInterface("1", public_ip=True, delete_on_termination=True,
                                     description="test_description",
                                     group_set=["test_group"],
                                     private_ip="1.1.1.1",
                                     private_ips=[dict(ec2.PrivateIpSpecification("2.2.2.2", True))],
                                     secondary_private_ip_count=2)


def test_mount_point():
    # Successful mount point
    mount_point = ec2.MountPoint("/dev/sda", "id-volume-test")
    assert mount_point == {"Device": "/dev/sda", "VolumeId": "id-volume-test"}

    # Extra arguments
    with pytest.raises(TypeError):
        ec2.MountPoint("/dev/sda", "id-volume-test", True)


def test_security_group_egress():
    # Successful security group egress with cidr_ip
    security_group_egress = ec2.SecurityGroupEgress(from_port="80", ip_protocol="tcp",
                                                    to_port="443", cidr_ip="10.0.0.0/8")
    assert dict(security_group_egress) == {
        "FromPort": "80",
        "IpProtocol": "tcp",
        "ToPort": "443",
        "CidrIp": "10.0.0.0/8"}

    # Successful security group egress with destination_security_group_id
    security_group_egress = ec2.SecurityGroupEgress(from_port="80", ip_protocol="tcp",
                                                    to_port="443", destination_security_group_id="id-test")
    assert dict(security_group_egress) == {
        "FromPort": "80",
        "IpProtocol": "tcp",
        "ToPort": "443",
        "DestinationSecurityGroupId": "id-test"}

    # Both cidr_ip and destination_security_group_id
    with pytest.raises(errors.RespawnResourceError):
        ec2.SecurityGroupEgress(from_port="80", ip_protocol="tcp", to_port="443",
                                cidr_ip="10.0.0.0/8", destination_security_group_id="id-test")


def test_security_group_ingress():
    # Successful security group ingress with cidr_ip
    security_group_ingress = ec2.SecurityGroupIngress(from_port="80", ip_protocol="tcp", to_port="443",
                                                      cidr_ip="10.0.0.0/8")
    assert dict(security_group_ingress) == {
        "FromPort": "80",
        "IpProtocol": "tcp",
        "ToPort": "443",
        "CidrIp": "10.0.0.0/8"}

    # Successful security group ingress with source_security_group_name
    security_group_ingress = ec2.SecurityGroupIngress(from_port="80", ip_protocol="tcp", to_port="443",
                                                      source_security_group_name="test-sg",
                                                      source_security_group_owner_id="sg-owner-id-test")
    assert dict(security_group_ingress) == {
        "FromPort": "80",
        "IpProtocol": "tcp",
        "ToPort": "443",
        "SourceSecurityGroupName": "test-sg",
        "SourceSecurityGroupOwnerId": "sg-owner-id-test"}

    # Successful security group ingress with source_security_group_id
    security_group_ingress = ec2.SecurityGroupIngress(from_port="80", ip_protocol="tcp", to_port="443",
                                                      source_security_group_id="sg-id-test")
    assert dict(security_group_ingress) == {
        "FromPort": "80",
        "IpProtocol": "tcp",
        "ToPort": "443",
        "SourceSecurityGroupId": "sg-id-test"}

    # Both cidr_ip and source_security_group_name
    with pytest.raises(errors.RespawnResourceError):
        ec2.SecurityGroupIngress(from_port="80", ip_protocol="tcp", to_port="443", cidr_ip="10.0.0.0/8",
                                 source_security_group_name="test-sg")

    # Both cidr_ip and source_security_group_id
    with pytest.raises(errors.RespawnResourceError):
        ec2.SecurityGroupIngress(from_port="80", ip_protocol="tcp", to_port="443", cidr_ip="10.0.0.0/8",
                                 source_security_group_id="sg-id-test")

    # Both source_security_group_id and source_security_group_name
    with pytest.raises(errors.RespawnResourceError):
        ec2.SecurityGroupIngress(from_port="80", ip_protocol="tcp", to_port="443",
                                 source_security_group_name="test-sg",
                                 source_security_group_id="sg-id-test")


def test_instance():
    # Successful instance
    instance = ec2.Instance(name="TestInstance", ami_id="ami-test", availability_zone="us-east1",
                            block_devices={"/dev/sda": dict(ebs=dict(snapshot_id="snap-xxxxxxxx"))},
                            disable_api_termination=True, ebs_optimized=True, iam_role="iam-test",
                            instance_shutdown_behavior="test_shutdown_behavior", instance_type="t2.micro",
                            kernel_id="kernel-test", key_pair="keypair-test", monitoring=True,
                            network_interfaces={"Interface1": dict(device_index="1", public_ip=True,
                                                                   delete_on_termination=True,
                                                                   group_set=["test_group"],
                                                                   interface_id="id-interface-test",
                                                                   private_ip="1.1.1.1",
                                                                   private_ips=[
                                                                       dict(private_ip="2.2.2.2", primary=True)],
                                                                   secondary_private_ip_count=2,
                                                                   subnet_id="id-subnet-test")},
                            placement_group="placementgroup-test", private_ip="1.1.1.1",
                            ramdisk_id="ramdisk-test", security_group_ids=["sg-test"], security_groups=["sgs-test"],
                            source_dest_check=True, subnet="subnet-test", tags=[dict(key="Key1", value="Value1")],
                            tenancy="tenancy-test", user_data_script="test_script",
                            volumes=[dict(volume_id="vol-xxxxxxx", device="/dev/sde")], attributes={"a": "val1"})

    assert instance == {
        "Type": "AWS::EC2::Instance",
        "Properties": {
            "Monitoring": True,
            "EbsOptimized": True,
            "RamdiskId": "ramdisk-test",
            "PrivateIpAddress": "1.1.1.1",
            "Tags": [
                {
                    "Key": "Key1",
                    "Value": "Value1"
                }
            ],
            "PlacementGroupName": "placementgroup-test",
            "ImageId": "ami-test",
            "KeyName": "keypair-test",
            "SecurityGroups": [
                "sgs-test"
            ],
            "SubnetId": "subnet-test",
            "InstanceType": "t2.micro",
            "NetworkInterfaces": [
                {
                    "DeviceIndex": "1",
                    "GroupSet": [
                        "test_group"
                    ],
                    "Description": "Interface1",
                    "NetworkInterfaceId": "id-interface-test",
                    "PrivateIpAddresses": [
                        {
                            "Primary": True,
                            "PrivateIpAddress": "2.2.2.2"
                        }
                    ],
                    "DeleteOnTermination": True,
                    "AssociatePublicIpAddress": True,
                    "SubnetId": "id-subnet-test",
                    "PrivateIpAddress": "1.1.1.1",
                    "SecondaryPrivateIpAddressCount": 2
                }
            ],
            "SourceDestCheck": True,
            "InstanceInitiatedShutdownBehavior": "test_shutdown_behavior",
            "SecurityGroupIds": [
                "sg-test"
            ],
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda",
                    "Ebs": {
                        "SnapshotId": "snap-xxxxxxxx"
                    }
                }
            ],
            "Volumes": [
                {
                    "Device": "/dev/sde",
                    "VolumeId": "vol-xxxxxxx"
                }
            ],
            "KernelId": "kernel-test",
            "IamInstanceProfile": "iam-test",
            "UserData": {
                "Fn::Base64": "test_script"
            },
            "AvailabilityZone": "us-east1",
            "Tenancy": "tenancy-test",
            "DisableApiTermination": True
        }
    }


def test_volume():
    # Successful volume
    volume = ec2.Volume(name="TestVolume", availability_zone="TestAZ", snapshot_id="test_snapshot",
                        size=1000, iops=4000, kms_key_id="TestKMS", volume_type="io1", encrypted=True,
                        tags=[dict(key="Key1", value="Value1")], deletion_policy="Retain")

    assert volume == {
        "Type": "AWS::EC2::Volume",
        "Properties": {
            "AvailabilityZone": "TestAZ",
            "Tags": [
                {
                    "Key": "Key1",
                    "Value": "Value1"
                }
            ],
            "Encrypted": True,
            "VolumeType": "io1",
            "KmsKeyId": "TestKMS",
            "SnapshotId": "test_snapshot",
            "Iops": 4000,
            "Size": 1000
        }
    }

    # No snapshot_id or size
    with pytest.raises(errors.RespawnResourceError):
        ec2.Volume(name="TestVolume", availability_zone="TestAZ", volume_type="io1", iops=1000,
                   delete_on_termination=True)

    # No iops with volume_type io1
    with pytest.raises(errors.RespawnResourceError):
        ec2.Volume(name="TestVolume", availability_zone="TestAZ", snapshot_id="test_snapshot", size=1000,
                   volume_type="io1", delete_on_termination=True)


def test_network_interface():
    # Successful network interface
    network_interface = ec2.NetworkInterface(name="TestNetworkInterface", public_ip=True, delete_on_termination=True,
                                             description="test_description",
                                             group_set=["test_group"],
                                             private_ip="1.1.1.1",
                                             private_ips=[
                                                 dict(private_ip="2.2.2.2", primary=True)],
                                             secondary_private_ip_count=2, subnet_id="id-subnet-test")

    assert network_interface == {
        "Type": "AWS::EC2::NetworkInterface",
        "Properties": {
            "GroupSet": [
                "test_group"
            ],
            "Description": "test_description",
            "PrivateIpAddresses": [
                {
                    "Primary": True,
                    "PrivateIpAddress": "2.2.2.2"
                }
            ],
            "SecondaryPrivateIpAddressCount": 2,
            "SubnetId": "id-subnet-test",
            "PrivateIpAddress": "1.1.1.1"
        }
    }


def test_network_interface_attachment():
    # Successful network interface attachment
    network_interface_attachment = ec2.NetworkInterfaceAttachment(name="TestNetworkInterfaceAttachment",
                                                                  device_index="deviceindex-test",
                                                                  instance_id="instanceid-test",
                                                                  network_interface_id="networkinterfaceid-test",
                                                                  delete_on_termination=True)

    assert network_interface_attachment == {
        "Type": "AWS::EC2::NetworkInterfaceAttachment",
        "Properties": {
            "InstanceId": "instanceid-test",
            "DeviceIndex": "deviceindex-test",
            "NetworkInterfaceId": "networkinterfaceid-test",
            ""
            "DeleteOnTermination": True
        }
    }


def test_security_group():
    # Successful security group
    security_group = ec2.SecurityGroup(name="TestSecurityGroup", group_description="Description",
                                       security_group_ingress=[dict(from_port="80",
                                                                    ip_protocol="tcp",
                                                                    to_port="443",
                                                                    source_security_group_name="test-sg")],
                                       security_group_egress=[dict(from_port="80", ip_protocol="tcp",
                                                                   to_port="443", cidr_ip="10.0.0.0/8")],
                                       vpc_id="TestVPC", tags=[dict(key="Key1", value="Value1")])

    assert security_group == {
        "Type": "AWS::EC2::SecurityGroup",
        "Properties": {
            "SecurityGroupIngress": [
                {
                    "FromPort": "80",
                    "IpProtocol": "tcp",
                    "ToPort": "443",
                    "SourceSecurityGroupName": "test-sg"
                }
            ],
            "VpcId": "TestVPC",
            "Tags": [
                {
                    "Key": "Key1",
                    "Value": "Value1"
                }
            ],
            "GroupDescription": "Description",
            "SecurityGroupEgress": [
                {
                    "FromPort": "80",
                    "IpProtocol": "tcp",
                    "ToPort": "443",
                    "CidrIp": "10.0.0.0/8"
                }
            ]
        }
    }
