import unittest
from respawn import rds


class TestRds(unittest.TestCase):
    def test_Tag(self):
        sample_kwargs = {'value': 'djin/metadata/test/rds', 'key': 'service_name'}
        v = rds.Tag(**sample_kwargs)
        assert v == {
        "Key": "service_name",
        "Value": "djin/metadata/test/rds"
      }


    def test_DBInstance(self):
        sample_name = 'myTestRDS'
        sample_kwargs = {'engine': 'MySQL', 'realm': 'private', 'tags': [{'value': 'djin/metadata/test/rds', 'key': 'service_name'}], 'service_name': 'djin/metadata/test/rds', 'subnet_group_name': 'djin-int-pri', 'allocated_storage': 100, 'instance_class': 'db.m1.small', 'instance_identifier': 'myTestRDSdb-int'}
        v = rds.DBInstance(sample_name, **sample_kwargs)
        assert v == {
  "Type": "AWS::RDS::DBInstance",
  "Properties": {
    "Engine": "MySQL",
    "Tags": [
      {
        "Key": "service_name",
        "Value": "djin/metadata/test/rds"
      }
    ],
    "AllocatedStorage": 100,
    "DBInstanceClass": "db.m1.small",
    "DBSubnetGroupName": "djin-int-pri",
    "DBInstanceIdentifier": "myTestRDSdb-int"
  }
}
    def test_DBProperties(self):
        sample_name = 'myTestRDS'
        sample_kwargs = {'backup_retention_period': 'string', 'source_db_instance_identifier': 'string', 'availability_zone': 'string', 'service_name': 'djin/metadata/test/rds', 'subnet_group_name': 'string', 'kms_key_id': 'string', 'iops': 1000, 'db_security_groups': 'string', 'master_username': 'string', 'snapshot_identifier': 'string', 'allow_minor_version_upgrade': True, 'vpc_security_groups': ['string'], 'realm': 'private', 'port': 'string', 'preferred_backup_window': 'string', 'engine': 'string', 'db_parameter_group_name': 'string', 'tags': [{'value': 'djin/metadata/test/rds', 'key': 'service_name'}], 'allow_major_version_upgrade': True, 'db_name': 'string', 'license_model': 'string', 'storage_encrypted': True, 'character_set_name': 'string', 'engine_version': 'string', 'option_group_name': 'string', 'multi_az': False, 'instance_identifier': 'string', 'publicly_accessible': False, 'preferred_maintenance_window': 'string',
                         'instance_class': 'db.m1.small', 'allocated_storage': '100'}
        v = rds.DBInstance(sample_name, **sample_kwargs)
        assert v['Properties'] == {
        "DBParameterGroupName": "string",
        "AllowMajorVersionUpgrade": True,
        "MasterUsername": "string",
        "LicenseModel": "string",
        "VPCSecurityGroups": [
          "string"
        ],
        "Engine": "string",
        "MultiAZ": False,
        "DBSecurityGroups": "string",
        "PubliclyAccessible": False,
        "Tags": [
          {
            "Key": "service_name",
            "Value": "djin/metadata/test/rds"
          }
        ],
        "PreferredBackupWindow": "string",
        "DBSnapshotIdentifier": "string",
        "AllocatedStorage": '100',
        "DBSubnetGroupName": "string",
        "DBName": "string",
        "PreferredMaintenanceWindow": "string",
        "EngineVersion": "string",
        "SourceDBInstanceIdentifier": "string",
        "BackupRetentionPeriod": "string",
        "OptionGroupName": "string",
        "CharacterSetName": "string",
        "AvailabilityZone": "string",
        "Iops": 1000,
        "StorageEncrypted": True,
        "KmsKeyId": "string",
        "DBInstanceClass": "db.m1.small",
        "Port": "string",
        "DBInstanceIdentifier": "string"
      }