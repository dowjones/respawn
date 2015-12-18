==============================
**Sample YAML**
==============================


**Sample YAML syntax for respawn.** : Please note that this contains most of the resources that respawn supports at
this moment. We will keep adding on as we keep building resource support. 

.. code-block:: yaml


       # Globals
        stack_name: sampleStack
        environment: sampleEnvironment
        team: &team sampleTeam
        default_windows_ami: &win_ami sampleAMI
        multi_az: True
        eap: True
        ebs_optimized: &ebs_optimized false
        periodic_chef: false
        service_name: &service sampleServiceName


        parameters:
          testWeb:
            default: String
            type: String
            description: "Creating test param"
            allowed_values:
              - "value1"
              - "value2"
            allowed_pattern: "[A-Za-z0-9]+"
            no_echo: true
            max_length: String
            min_length: String
            max_value: String
            min_value: String
            constraint_description: "Malformed input-Parameter MyParameter must only contain upper and lower case letters"
          daw0eip1:
            default : String
            type : String
            description : "Creating test param"


        # Default Security Groups
        SgDevsample: &dev_djin_fcm String
        ELBSubnet: &elb_subnet  String

        security_groups:
            Web: &web_sgs
              - *sampleSecurityGroup

        load_balancers:
              SampleLoadBalancer:
                scheme: internet-facing
                connection_settings:
                  idle_timeout: 40
                cross_zone: True
                security_group:
                  - sg-xxxxxxx1
                  - sg-xxxxxxx2
                instances:
                  - ref(SampleInstance)
                policies:
                   - policy_name: SamplePolicyName1
                     attribute:
                        - name: SampleName1
                          value: SampleValue1
                        - name: SampleName2
                          value: SampleValue2
                     instance_ports:
                        - 2121
                        - 2424
                     load_balancer_ports:
                        - 32323
                        - 2424
                     policy_type: SSLNegotiationPolicyType
                   - policy_name: SamplePolicyName2
                     attribute:
                        - name: SampleName1
                          value: SampleValue1
                     instance_ports:
                        - 1212
                        - 4242
                     load_balancer_ports:
                        - 23232
                        - 4141
                app_cookie_stickiness_policy:
                  - policy_name: SamplePolicy1
                    cookie_name: SampleCookie1
                  - policy_name: SamplePolicy2
                    cookie_name: SampleCookie2
                connection_draining_policy:
                  enabled: True
                  timeout: 10
                availability_zones:
                  - "Fn::GetAZs": ""
                health_check:
                  healthy_threshold: 2
                  interval: 10
                  target: /healthcheck
                  timeout: 10
                  unhealthy_threshold: 2
                lb_cookie_stickiness_policy:
                  - policy_name: SamplePolicyName1
                    cookie_expiration_period: 300
                  - policy_name: SamplePolicyName2
                    cookie_expiration_period: 600
                load_balancer_name: SampleLoadBalancer1 # Unique name used by AWS
                access_logging_policy:
                  emit_interval: 20
                  enabled: True
                  s3_bucket_name: SampleS3BucketName
                  s3_bucket_prefix: SampleS3BucketPrefix
                listeners:
                  https:
                    load_balancer_port: 83
                    instance_port: 84
                    instance_protocol: tcp
                  tcp:
                    load_balancer_port: 8443
                    instance_port: 8443
                    instance_protocol: http
                    ssl_certificate_id: SampleSSLARN
                tags:
                  - key: Key1
                    value: Value1
                  - key: Key2
                    value: Value2

        instances:
            SampleInstance:
              hostname: SampleHostname
              instance_type: m3.xlarge
              ami_id: ami-xxxxxxxx
              ebs_optimized: true
              iam_role: SampleIAMRole
              security_groups:
                - sg-00000001
                - sg-00000002
              ramdisk_id: SampleRamDiskID
              source_dest_check: true
              network_interfaces:
                Interface1:
                  public_ip: true
                  delete_on_termination: true
                  device_index: 0
                  subnet_id: subnet-xxxxxxxx
                  private_ips:
                    - private_ip: 1.1.1.1
                      primary: false
                    - private_ip: 2.2.2.2
                      primary: true
              block_devices:
                /dev/sda:
                  ebs:
                    delete_on_termination: false
                    encrypted: false
                    iops: 1000
                    size: 100
                    type: standard
                /dev/sdb:
                  ebs:
                    snapshot_id: snap-xxxxxxxx
                /dev/sdc:
                  virtual_name: ephemeral0
                /dev/sdd:
                  no_device: true
              volumes:
                - device: /dev/sdd
                  volume_id: ref(SampleVolume1)
                - device: /dev/sde
                  volume_id: vol-xxxxxxx
              tags:
                - key: Key1
                  value: Value1
              user_data:
                file: path/to/script.sh  # Jinja2 Template
                params:
                  param1: hello
                  param2: world


        volumes:
            SampleVolume1:
              availability_zone: SampleAZ
              instance: ref(SampleInstance)
              size: 100

            SampleVolume2:
              availability_zone: SampleAZ
              snapshot_id: snap-xxxxxxxx
              size: 1000
              iops: 4000
              kms_key_id: SampleKMSKeyID
              volume_type: standard
              encrypted: true
              tags:
                - key: Key1
                  value: Value1
              deletion_policy: Retain

        auto_scale_groups:
            SampleAutoScaleGroup:
              hostname: sampleTestName
              availability_zones:
                  - AZName1
                  - AZName2
              min_size: 1
              max_size: 10
              desired_capacity: 10
              instance_id: ami-xxxxxxxx
              cooldown: 10
              launch_configuration: LaunchConfigName
              load_balancer_names:
                  - LBName
                  - ref(Sample_LB)
              max_size: 2
              min_size: 1
              metrics_collection:
                  - granularity: 1Minute
                  - granularity: 1Minute
                    metrics:
                        - Metric1
                        - Metric2
              notification_configs:
                  - notification_type:
                        - Type1
                        - Type2
                    topic_arn: "arn:aws:[service]:[region]:[account]:resourceType/resourcePath"
                  - notification_type:
                        - Type3
                    topic_arn: "arn:aws:[service]:[region]:[account]:resourceType/resourcePath"
              placement_group: PlacementGroupName
              tags:
                  - key: Key1
                    value: Value1
                    propagate_at_launch: true
                  - key: Key2
                    value: Value2
                    propagate_at_launch: true
              termination_policies:
                  - Policy1
                  - Policy2
              vpc_zone_identifier:
                  - ZoneIdentifier1
                  - ZoneIdentifier2

        launch_configurations:
            SampleLaunchConfiguration:
              instance_type: t2.small
              ebs_optimized: false
              ami_id: ami-xxxxxxxx
              iam_role: SampleIAMRole
              key_pair: SampleKey
              ramdisk_id: SampleRamDiskID
              public_ip: true
              security_groups:
                - sg-00000001
                - sg-00000002
              block_devices:
                /dev/sda:
                  ebs:
                    delete_on_termination: false
                    encrypted: false
                    iops: 1000
                    size: 100
                    type: standard
                /dev/sdb:
                  ebs:
                    snapshot_id: id-testSnapshot
                /dev/sdc:
                  virtual_name: ephemeral0
                /dev/sdd:
                  no_device: true
              user_data:
                  file: path/to/script.sh  # Jinja2 Template
                  params:
                    param1: hello
                    param2: world

        lifecycle_hooks:
          SampleLifecycleHook:
              asg_name: ref(SampleAutoScaleGroup)
              lifecycle_transition: autoscaling:EC2_INSTANCE_TERMINATING
              notification_target_arn: ref(SampleSNSTopic) # SNS Topic
              role_arn: SampleIAMRole
              heartbeat_timeout: 1800
              default_result: CONTINUE
              notification_metadata: SampleMetadata


        scheduled_actions:
          SampleActionDown:
              asg_name: SampleAutoScaleGroup
              desired_capacity: 0
              max_size: 0
              min_size: 0
              recurrence: 0 7 * * *

          SampleActionUp:
              asg_name: SampleAutoScaleGroup
              desired_capacity: 5
              max_size: 5
              min_size: 5
              recurrence: 0 9 * * *

        rds:
          SampleRDS:
            allocated_storage: 100
            instance_class: db.m1.small
            engine: MySQL
            allow_major_version_upgrade: True
            allow_minor_version_upgrade: True
            availability_zone: SampleAZ
            backup_retention_period: 10
            character_set_name: UTF8
            instance_identifier: SampleRDSName # Unique name used by AWS
            db_name: SampleDB
            db_parameter_group_name: SampleDBParameterGroup
            db_security_groups:
                - SampleSecurityGroup
            snapshot_identifier: SampleSnapshot
            subnet_group_name: SampleSubnetGroup
            engine: MySQL
            engine_version: 1.0.0
            iops: 1000
            kms_key_id: SampleKMSKeyID
            license_model: SampleLicenseModel
            master_username: SampleUsername
            multi_az: False
            option_group_name: SampleOptionGroup
            port: 3306
            preferred_backup_window: Mon:03:00-Mon:11:00
            preferred_maintenance_window: Tue:04:00-Tue:04:30
            publicly_accessible: False
            source_db_instance_identifier: SampleSourceDBIdentifier
            storage_encrypted: True
            vpc_security_groups:
                - SampleVPCSecurityGroup

        network_interfaces:
          SampleNetworkInterface:
            description: "Sample Description"
            group_set:
              - SampleGroup1
              - SampleGroup2
            private_ip_address: 10.20.03.20
            private_ip_addresses:
             - 10.23.23.23
             - 12.13.3.4
            secondary_private_ip_address_count: 4
            source_dest_check: true
            subnet_id: 131.3.13.1
            tags:
                - key: Key1
                  value: Value1
                - key: Key2
                  value: Value2

        network_interface_attachments:
             TestNetworkIntefaceAttachment:
               delete_on_termination: False
               device_index: 1
               instance_id: ref(SampleInstanceName)
               network_interface_id: ref(SampleNetworkInterfaceName)

        sns_topics:
          SampleSNSTopic:
            display_name : SampleSNSTopic
            topic_name : SampleTopic
            subscription:
              - protocol : https
                endpoint : Endpoint1
              - protocol : http
                endpoint : Endpoint2

        cloud_watch:
          SampleCloudWatch:
            actions_enabled: true
            alarm_actions:
              - AlarmAction1
              - AlarmAction2
            alarm_name: SampleAlarm
            alarm_description: "Sample alarm description"
            comparison_operator: GreaterThanOrEqualToThreshold
            dimensions:
              - name: Dimension1
                value: Value1
              - name: Dimension2
                value: Value2
            evaluation_periods: 15
            insufficient_data_actions:
              - InsufficientDataAction1
              - InsufficientDataAction2
            metric_name : SampleName
            namespace : SampleNamespace
            ok_actions :
              - OkAction1
              - OkAction2
            period : 12
            statistic : Average
            threshold : 10
            unit : Milliseconds

        security_group:
          SampleSecurityGroup:
            group_description: SampleDescription
            security_group_egress:
              - from_port: 80
                ip_protocol: http
                to_port: 80
            security_group_ingress:
              - from_port: 443
                ip_protocol: https
                to_port: 443
            tags:
              - key: Key1
                value: Value1
            vpc_id: SampleVPC



