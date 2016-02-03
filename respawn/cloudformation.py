import jinja2
from cfn_pyplates import core, functions
from respawn import ec2, autoscaling, rds, sns, cloudwatch, elb, parameters
from time import asctime, gmtime
from errors import RespawnResourceError


class WaitConditionHandle(core.Resource):
    def __init__(self, wait_handle_name):
        super(WaitConditionHandle, self).__init__(wait_handle_name, 'AWS::CloudFormation::WaitConditionHandle')


class WaitCondition(core.Resource):
    def __init__(self, wait_condition_name, wait_handle_name, timeout, depends_on, count=1):
        wait_condition_properties = {
            'Handle': wait_handle_name,
            'Timeout': timeout,
            'Count': count
        }
        super(WaitCondition, self).__init__(wait_condition_name,
                                            'AWS::CloudFormation::WaitCondition',
                                            wait_condition_properties,
                                            [core.DependsOn([depends_on])]
                                            )


class Template(core.CloudFormationTemplate):
    def __init__(self, **kwargs):
        """
        Creates CloudFormation Template
        """

        name = kwargs.get('stack_name', 'unnamed_stack')

        self.__region = kwargs.get('region', 'us-east-1')

        self.__env = kwargs.get('environment', 'dev')

        self.__description = kwargs.get('description',
                                        '{name} in {env} ({ts})'.format(name=name,
                                                                        env=self.__env,
                                                                        ts=asctime(gmtime())
                                                                        )
                                        )

        super(Template, self).__init__(self.__description, kwargs)

    def create_iam_role_param(self, name, iam_role):
        iam_role_param = name + 'IamRole'
        self.parameters.add(
            core.Parameter(iam_role_param, 'String', {
                'Default': iam_role,
                'Description': 'IAM Role for ' + name
            }))
        iam_role = functions.ref(iam_role_param)
        return iam_role

    def create_availability_zone_param(self, name, availability_zone):
        availability_zone_param = name + "AvailabilityZone"
        self.parameters.add(
            core.Parameter(availability_zone_param, 'String', {
                'Default': availability_zone,
                'Description': 'Availability Zone for ' + name
            }))
        availability_zone = functions.ref(availability_zone_param)
        return availability_zone

    def create_key_pair_param(self, name, key_pair):
        key_pair_param = name + 'KeyPair'
        self.parameters.add(
            core.Parameter(key_pair_param, 'String', {
                'Default': key_pair,
                'Description': 'Key Pair for ' + name
            }))
        key_pair = functions.ref(key_pair_param)
        return key_pair

    # ----------------------------------------------------------------------------------------------------------
    #  Load Balancer
    # ----------------------------------------------------------------------------------------------------------
    def add_load_balancer(self, name, **kwargs):
        listener_list = []
        loadbalancer_values = dict()

        for key, value in kwargs.iteritems():
            loadbalancer_values[key] = value

        # Check for presence of listener
        if kwargs.get('listeners') is None :
            raise RespawnResourceError("listeners needs to be present in loadbalancer options", "Listeners")

        # Recursing through multiple listeners of same/different protocol.
        if kwargs.get('listeners') is not None:
            for protocol, protocol_values in (kwargs.get('listeners', dict())).items():
                if protocol in ('https', 'http', 'tcp', 'ssl'):
                    if not isinstance(protocol_values, list):
                        listeners = (elb.ProtocolListener(protocol, protocol_values['load_balancer_port'], protocol_values[
                            'instance_port'], protocol_values.get('ssl_certificate_id'), **protocol_values))
                        listener_list.append(listeners)
                    else:
                        for protocol_value in protocol_values:
                            listeners = (elb.ProtocolListener(protocol, protocol_value['load_balancer_port'], protocol_value[
                                'instance_port'], protocol_value.get('ssl_certificate_id'), **protocol_value))
                            listener_list.append(listeners)
                else:
                    raise RespawnResourceError('protocol needs to be one of HTTPS, HTTP, TCP, SSL', "Protocol")

        if kwargs.get('health_check_path') is None:
            health_check_path = '/aptest.html'
            loadbalancer_values['health_check_path'] = health_check_path

        loadbalancer_values['listeners'] = listener_list
        loadbalancer_values['env'] = self.__env
        lb = elb.LoadBalancer(name, **loadbalancer_values)
        self.resources.add(lb)
        return lb

    # ----------------------------------------------------------------------------------------------------------
    #  Launch Config
    # ----------------------------------------------------------------------------------------------------------
    def add_launch_config(self, name, **kwargs):
        lc_arguments = kwargs

        security_groups = lc_arguments.get('security_groups')
        if security_groups is not None:
            lc_arguments['security_groups'] = security_groups

        # IAM Role
        iam_role = self.create_iam_role_param(name, kwargs.get("iam_role"))
        if iam_role is not None:
            lc_arguments['iam_role'] = iam_role

        # Key Pair
        key_pair = kwargs.get("key_pair", None)
        if key_pair is not None:
            key_pair = self.create_key_pair_param(name, key_pair)
            lc_arguments['key_pair'] = key_pair

        # User Data
        if "user_data" in kwargs:
            user_data = kwargs.get("user_data")
            with open(user_data['file'], "r") as f:
                user_data_script = f.read()
            user_data_script = jinja2.Template(user_data_script)
            lc_arguments['user_data_script'] = user_data_script.render(**user_data.get('params', dict()))

        lc = autoscaling.LaunchConfiguration(name, **lc_arguments)

        self.resources.add(lc)
        return lc

    # ----------------------------------------------------------------------------------------------------------
    #  Autoscaling Group
    # ----------------------------------------------------------------------------------------------------------
    def add_autoscaling_group(self, name, **kwargs):
        asg_arguments = kwargs
        asg = autoscaling.AutoScalingGroup(name, **asg_arguments)
        self.resources.add(asg)
        return asg

    # ----------------------------------------------------------------------------------------------------------
    #  Scheduled Action
    # ----------------------------------------------------------------------------------------------------------
    def add_scheduled_action(self, name, **kwargs):
        sa_arguments = kwargs
        sa = autoscaling.ScheduledAction(name, **sa_arguments)
        self.resources.add(sa)
        return sa

    # ----------------------------------------------------------------------------------------------------------
    #  Lifecycle Hook
    # ----------------------------------------------------------------------------------------------------------
    def add_lifecycle_hook(self, name, **kwargs):
        lh_arguments = kwargs
        lh = autoscaling.LifecycleHook(name, **lh_arguments)
        self.resources.add(lh)
        return lh

    # ---------------------------------------------------------------------------------------------------------
    # Route53 Record
    # ---------------------------------------------------------------------------------------------------------
    def add_route53_record_set(
            self,
            name,
            **kwargs
    ):
        record_set_arguments = dict()
        for key, value in kwargs.iteritems():
            record_set_arguments[key] = value
        record_set = ec2.Instance(name, **record_set_arguments)
        self.resources.add(record_set)
        return record_set

    # ----------------------------------------------------------------------------------------------------------
    #  Instance
    # ----------------------------------------------------------------------------------------------------------
    def add_instance(self, name, **kwargs):
        instance_arguments = kwargs

        # IAM Role
        iam_role = instance_arguments.get("iam_role", None)
        if iam_role is not None:
            iam_role = self.create_iam_role_param(name, iam_role)
            instance_arguments['iam_role'] = iam_role

        # Key Pair
        key_pair = instance_arguments.get("key_pair", None)
        if key_pair is not None:
            key_pair = self.create_key_pair_param(name, key_pair)
            instance_arguments['key_pair'] = key_pair

        # Availability Zone
        availability_zone = instance_arguments.get("availability_zone", None)
        if availability_zone is not None:
            availability_zone = self.create_availability_zone_param(name, availability_zone)
            instance_arguments['availability_zone'] = availability_zone

        # User Data
        if "user_data" in instance_arguments:
            user_data = instance_arguments.get("user_data")
            with open(user_data['file'], "r") as f:
                user_data_script = f.read()
            user_data_script = jinja2.Template(user_data_script)
            instance_arguments['user_data_script'] = user_data_script.render(**user_data.get('params', dict()))

        instance = ec2.Instance(name, **instance_arguments)

        self.resources.add(instance)
        return instance

    # ----------------------------------------------------------------------------------------------------------
    #  Volume
    # ----------------------------------------------------------------------------------------------------------
    def add_volume(self, name, availability_zone, **kwargs):
        volume_arguments = kwargs
        volume = ec2.Volume(name, availability_zone, **volume_arguments)
        self.resources.add(volume)
        return volume

    # ----------------------------------------------------------------------------------------------------------
    #  RDS
    # ----------------------------------------------------------------------------------------------------------
    def add_rds_instance(self, name, **kwargs):
        rds_args = kwargs
        dbinstance = rds.DBInstance(name, **rds_args)
        self.resources.add(dbinstance)
        return dbinstance

    # ----------------------------------------------------------------------------------------------------------
    #  Cloud Watch Alarm
    # ----------------------------------------------------------------------------------------------------------
    def add_cloud_watch_alarm(self,
                              name,
                              evaluation_periods,
                              comparison_operator,
                              period,
                              metric_name,
                              statistic,
                              threshold,
                              **kwargs):
        cloudwatch_arguments = kwargs
        cloudwatch_alarm = cloudwatch.CloudWatchAlarm(name,
                                                      evaluation_periods,
                                                      comparison_operator,
                                                      period,
                                                      metric_name,
                                                      statistic,
                                                      threshold,
                                                      **cloudwatch_arguments
                                                      )
        self.resources.add(cloudwatch_alarm)
        return cloudwatch_alarm

    # ----------------------------------------------------------------------------------------------------------
    #  Network Interface
    # ----------------------------------------------------------------------------------------------------------
    def add_network_interface(self, name, **kwargs):
        ni_arguments = kwargs
        network_interface = ec2.NetworkInterface(name, **ni_arguments)
        self.resources.add(network_interface)
        return network_interface

    # ----------------------------------------------------------------------------------------------------------
    #  Network Interface Attachment
    # ----------------------------------------------------------------------------------------------------------
    def add_network_interface_attachment(self, name, **kwargs):
        nia_arguments = kwargs
        nia = ec2.NetworkInterfaceAttachment(name, **nia_arguments)
        self.resources.add(nia)
        return nia

    # ----------------------------------------------------------------------------------------------------------
    #  Parameters
    # ----------------------------------------------------------------------------------------------------------
    def add_parameter(self, name, **kwargs):
        parameter_arguments = kwargs
        parameter = parameters.CustomParameters(name, **parameter_arguments)
        self.parameters.add(parameter)
        return parameter

    # ----------------------------------------------------------------------------------------------------------
    #  SNS Topic
    # ----------------------------------------------------------------------------------------------------------
    def add_sns_topic(self, name, **kwargs):
        sns_arguments = kwargs
        sns_topic = sns.SnsTopic(name, **sns_arguments)
        self.resources.add(sns_topic)
        return sns_topic

    # ----------------------------------------------------------------------------------------------------------
    #  Security Group
    # ----------------------------------------------------------------------------------------------------------
    def add_security_group(self, name, **kwargs):
        security_args = kwargs
        security_group = ec2.SecurityGroup(name, **security_args)
        self.resources.add(security_group)
        return security_group
