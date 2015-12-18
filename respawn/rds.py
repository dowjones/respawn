from cfn_pyplates import core
from errors import RespawnResourceError


class Tag(core.JSONableDict):
    """
        Creates RDS Tag

        :param key: String
        :param value: String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  Tag
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self,
                 key,
                 value
                 ):
        super(Tag, self).__init__()
        self['Key'] = key
        self['Value'] = value


class DBInstance(core.Resource):
    """
        Creates a Database Instance

        :param name: String
        :param allocated_storage: String
        :param instance_class: String

        kwargs
            - allow_major_version_upgrade: Boolean
            - auto_minor_version_upgrade: Boolean
            - availability_zone: String
            - backup_retention_period: String
            - character_set_name: String
            - instance_identifier: String
            - db_name: String
            - db_parameter_group_name: String
            - db_security_groups: [ String, ... ]
            - snapshot_identifier: String
            - subnet_group_name: String
            - engine: String
            - engine_version: String
            - iops: Number
            - kms_key_id: String
            - license_model: String
            - master_username: String
            - master_password: String
            - multi_az: Boolean
            - option_group_name: String
            - port: String
            - preferred_backup_window: String
            - preferred_maintenance_window: String
            - publicly_accessible: Boolean
            - source_db_instance_identifier: String
            - storage_encrypted: Boolean
            - storage_type: String
            - tags: [ Tag, ... ]
            - vpc_security_groups: [ String, ... ]
        """
    # ----------------------------------------------------------------------------------------------------------
    #  DB Instance Properties
    # ----------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            name,
            allocated_storage,
            instance_class,
            **kwargs
    ):
        if "snapshot_identifier" not in kwargs and "engine" not in kwargs:
            raise RespawnResourceError("Engine (engine) required if Snapshot Identifier (snapshot_identifier) not "
                                       "specified.", "DBSnapshotIdentifier/Engine")

        if kwargs.get("storage_type") == "io1" and "iops" not in kwargs:
            raise RespawnResourceError("Iops (iops) required for Storage Type (storage_type) io1.", "Iops")

        attributes = kwargs.get("attributes", dict())

        properties = {
            'AllocatedStorage': allocated_storage,
            'DBInstanceClass': instance_class
        }

        if 'tags' in kwargs:
            t = kwargs.get('tags')
            tags = []
            for tag in t:
                tags.append(Tag(**tag))
            properties['Tags'] = tags

        if "allow_major_version_upgrade" in kwargs:
            properties['AllowMajorVersionUpgrade'] = kwargs.get("allow_major_version_upgrade")
        if "auto_minor_version_upgrade" in kwargs:
            properties['AutoMinorVersionUpgrade'] = kwargs.get("auto_minor_version_upgrade")
        if "availability_zone" in kwargs:
            properties['AvailabilityZone'] = kwargs.get("availability_zone")
        if "backup_retention_period" in kwargs:
            properties['BackupRetentionPeriod'] = kwargs.get("backup_retention_period")
        if "character_set_name" in kwargs:
            properties['CharacterSetName'] = kwargs.get("character_set_name")
        if "instance_identifier" in kwargs:
            properties['DBInstanceIdentifier'] = kwargs.get("instance_identifier")
        if "db_name" in kwargs:
            properties['DBName'] = kwargs.get("db_name")
        if "db_parameter_group_name" in kwargs:
            properties['DBParameterGroupName'] = kwargs.get("db_parameter_group_name")
        if "db_security_groups" in kwargs:
            properties['DBSecurityGroups'] = kwargs.get("db_security_groups")
        if "snapshot_identifier" in kwargs:
            properties['DBSnapshotIdentifier'] = kwargs.get("snapshot_identifier")
        if "subnet_group_name" in kwargs:
            properties['DBSubnetGroupName'] = kwargs.get("subnet_group_name")
        if "engine" in kwargs:
            properties['Engine'] = kwargs.get("engine")
        if "engine_version" in kwargs:
            properties['EngineVersion'] = kwargs.get("engine_version")
        if "iops" in kwargs:
            properties['Iops'] = kwargs.get("iops")
        if "kms_key_id" in kwargs:
            properties['KmsKeyId'] = kwargs.get("kms_key_id")
        if "license_model" in kwargs:
            properties['LicenseModel'] = kwargs.get("license_model")
        if "master_username" in kwargs:
            properties['MasterUsername'] = kwargs.get("master_username")
        if "multi_az" in kwargs:
            properties['MultiAZ'] = kwargs.get("multi_az")
        if "option_group_name" in kwargs:
            properties['OptionGroupName'] = kwargs.get("option_group_name")
        if "port" in kwargs:
            properties['Port'] = kwargs.get("port")
        if "preferred_backup_window" in kwargs:
            properties['PreferredBackupWindow'] = kwargs.get("preferred_backup_window")
        if "preferred_maintenance_window" in kwargs:
            properties['PreferredMaintenanceWindow'] = kwargs.get("preferred_maintenance_window")
        if "publicly_accessible" in kwargs:
            properties['PubliclyAccessible'] = kwargs.get("publicly_accessible")
        if "source_db_instance_identifier" in kwargs:
            properties['SourceDBInstanceIdentifier'] = kwargs.get("source_db_instance_identifier")
        if "storage_encrypted" in kwargs:
            properties['StorageEncrypted'] = kwargs.get("storage_encrypted")
        if "storage_type" in kwargs:
            properties['StorageType'] = kwargs.get("storage_type")
        if "vpc_security_groups" in kwargs:
            properties['VPCSecurityGroups'] = kwargs.get("vpc_security_groups")

        super(DBInstance, self).__init__(name, 'AWS::RDS::DBInstance', properties, attributes)
