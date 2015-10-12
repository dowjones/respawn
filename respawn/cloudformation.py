import inspect
from cfn_pyplates import core, functions
from respawn import shutdown, ec2, autoscaling, rds, values, sns, cloudwatch, elb, parameters, environments as envs
from time import asctime, gmtime
import jinja2, os


class WaitConditionHandle(core.Resource):
    def __init__(self, wait_handle_name):
        super(WaitConditionHandle, self).__init__(wait_handle_name, 'AWS::CloudFormation::WaitConditionHandle', {})


class WaitCondition(core.Resource):
    def __init__(self, wait_condtion_name, wait_handle_name, timeout, depends_on, count=1):
        wait_condition_properties = {
            'Handle': wait_handle_name,
            'Timeout': timeout,
            'Count': count
        }
        super(WaitCondition, self).__init__(
            wait_condtion_name,
            'AWS::CloudFormation::WaitCondition',
            wait_condition_properties,
            [core.DependsOn([depends_on])]
        )


class Template(core.CloudFormationTemplate):
    def __init__(
            self,
            name=None,
            desc=None,
            opts=None,
            region=None,
            eap=None,
            env=None,
            **kwargs
    ):

        """
        This function does something.

        Kwargs:
           state (bool): Current state to be in.
           stackName (str): Name of the stack that you create with this yaml.
           environment (str): The development environment for building the stack.
           eap (str):
           periodicChef (str):
           useHostnameDispatcherNames (str):

        Raises:
           AttributeError, KeyError

        """
        # Constants
        self.__DEV_ENVS = (envs.DEV, envs.INT)
        self.__PRD_ENVS = (envs.STG, envs.PRD)

        name = kwargs.get('stackName')
        if name is None:
            name = 'unnamedStack'

        self.__region = region
        if region is None:
            self.__region = 'us-east-1'

        env = kwargs.get('environment')
        if env is None:
            self.__env = envs.DEV
        else:
            self.__env = envs.validate(env)

        if desc is None:
            desc = '{name} in {env} ({ts})'.format(name=name, env=env, ts=asctime(gmtime()))

        eap = kwargs.get('EAP')
        if eap is None:
            eap = 'yes' if self.is_production() else 'no'
        else:
            eap = 'yes' if eap is True else 'no'

        self.__periodic_chef = kwargs.get('periodicChef', True)

        # Hack to get some parameters to generate in the proper naming convention for the hostname dispatcher
        self.__use_hostname_dispatcher_names = kwargs.get('useHostnameDispatcherNames', False)

        super(Template, self).__init__(desc, opts)

        # EAP Program
        self.parameters.add(
            core.Parameter('tagEAP', 'String', {
                'Default': eap,
                'Description': 'Does the stack participate in the EAP Program',
                "AllowedValues": ["yes", "no"]
            }))

        # Chef Server URL
        self.parameters.add(
            core.Parameter('chefServerURL', 'String', {
                'Default': values.CHEF_SERVER_URL,
                'Description': 'Chef Server URL'
            }))

        # Chef Validator Key
        self.parameters.add(
            core.Parameter('chefValidationPEM', 'String', {
                'Default': values.CHEF_VALIDATION_PEM,
                'Description': 'Chef Validator Key'
            }))

        # Chef Configuration
        self.parameters.add(
            core.Parameter('chefConfig', 'String', {
                'Default': values.CHEF_CONFIG,
                'Description': 'Chef Configuration URL'
            }))

        # Chef Daemonize Interval in seconds
        self.parameters.add(
            core.Parameter(values.CHEF_INTERVAL_NAME, 'Number', {
                'Description': 'Chef Client run interval in seconds (Zero to disable)',
                'Default': self.default_chef_interval(),
                'MinValue': 0,
                'ConstraintDescription': 'Chef client run interval out of range'
            }))

    def env(self):
        return self.__env

    def transform_reference(self, v):
        if v.startswith('ref('):
            v = v[len('ref('):-1].strip()
            v = functions.ref(self.fetch_reference(self, v).name)
        elif v.startswith('get_att('):
            v = [s.strip() for s in v[len('get_att('):-1].split(',')]
            v = functions.get_att(self.fetch_reference(self, [0]).name, v[1])
        return v

    def fetch_reference(self, name):
        r = gen.resources.get(name, gen.resources.get(name))
        if r is None:
            raise RuntimeError('Resource name {0} not found'.format(name))
        return r

    def original_mapping(self, **kwargs):
        injected_kwargs = dict()
        for key, value in kwargs.iteritems():
            injected_kwargs[key] = value
        return injected_kwargs

    def subnets(self, realm, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return [values.subnets[self.__region][realm][env][i] for i in
                values.availability_zones[self.__region][realm][env]]

    def subnet_group(self, realm, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return values.subnet_group[self.__region][realm][env]

    def generic_security_group(self, realm, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return values.security_groups[self.__region][realm][env]

    def default_security_group(self, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return values.security_groups[self.__region]['default'][env]

    def inet_security_group(self, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return values.security_groups[self.__region]['internet'][env]

    def is_development(self):
        return self.env() in self.__DEV_ENVS

    def is_production(self):
        return self.env() in self.__PRD_ENVS

    def default_chef_interval(self):
        val = 15 * 60
        if self.is_production() or self.periodic_chef() is False:   val = 0
        return val

    def periodic_chef(self):
        return self.__periodic_chef

    def hosted_zone_id(self, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return values.dns_zones[self.__region]['internal'][env]

    def format_elb_resource_name(self, name):
        name = 'Djin{0}{1}'.format(self.env().title(), name)
        name += 'LB' if 'LB' not in name else ''
        return name

    def format_elb_name(self):
        # ToDo: Created at some point to name ELBs however a note about custom names
        # in the AWS docs leads me to believe this may be a bad idea
        # return functions.join('-', 'djin', self.env(), functions.ref('AWS::StackName'))
        return None

    def create_elastic_ip(self, name):
        return self.resources.add(core.Resource(name, 'AWS::EC2::EIP', {"Domain": "vpc"}))

    def assocate_elastic_ips(self, name, instance, elastic_ips):
        for item in elastic_ips:
            eip_name = None
            props = None
            if isinstance(item, dict):
                keys = item.keys()
                if len(keys) > 1:   raise RuntimeError('Elastic IP entry should be the name of the resource only')
                eip_name = keys[0]
                props = item.values()
            else:
                eip_name = item
                props = dict()

            # Create
            if 'AllocationId' not in props:
                eip = self.create_elastic_ip(eip_name)
                # props['EIP']=functions.ref(eip.name)
                props['AllocationId'] = functions.get_att(eip.name, 'AllocationId')

            props['InstanceId'] = functions.ref(instance.name)
            self.resources.add(core.Resource(name + 'EIP', 'AWS::EC2::EIPAssociation', props))

    def __unicode__(self):
        # Before outputting to json, remove private elements
        for attr, mapping in inspect.getmembers(self, predicate=lambda x: inspect.ismethod(x) == False):
            if attr.startswith('_Template__'):
                delattr(self, attr)
        return super(Template, self).__unicode__()

    def prepare_security_groups(self, name, security_groups):
        if security_groups is None: security_groups = list()
        security_groups.append(self.default_security_group())
        security_groups = tuple(set(security_groups))
        security_groups_param = name + 'SecurityGroups'
        self.parameters.add(
            core.Parameter(security_groups_param, 'CommaDelimitedList', {
                'Default': ', '.join(security_groups),
                'Description': 'Security Groups for ' + name + ' AutoScale Group'
            }))
        security_groups = functions.ref(security_groups_param)
        return security_groups

    def prepare_subnets(self, realm, subnets):
        if subnets is None: subnets = self.subnets(realm)
        return tuple(set(subnets))

    def prepare_iam_role(self, name, iam_role):
        if iam_role is not None:
            iam_role_param = name + 'IamRole'
            self.parameters.add(
                core.Parameter(iam_role_param, 'String', {
                    'Default': iam_role,
                    'Description': 'IAM Role for ' + name + ' Instance'
                }))
            iam_role = functions.ref(iam_role_param)
        return iam_role

    def prepare_availability_zone(self, name, availability_zone):
        if availability_zone is not None:
            availability_zone_param = name + "AvailabilityZone"
            self.parameters.add(
                core.Parameter(availability_zone_param, 'String', {
                    'Default': availability_zone,
                    'Description': 'Availability Zone for ' + name + ' Instance'
                }))
            availability_zone = functions.ref(availability_zone_param)
        return availability_zone

    def get_availability_zone(self, name):
        availability_zone_param = name + "AvailabilityZone"
        availability_zone = functions.ref(availability_zone_param)
        return availability_zone

    def prepare_key_pair(self, name, key_pair):
        if key_pair is not None:
            key_pair_param = name + 'KeyPair'
            self.parameters.add(
                core.Parameter(key_pair_param, 'String', {
                    'Default': key_pair,
                    'Description': 'Key Pair for ' + name + ' Instance'
                }))
            key_pair = functions.ref(key_pair_param)
        return key_pair

    def add_dns_round_robin(self, name, zone_name, values, record_name=None, ttl=300):
        dns_zone_param_name = name + 'DNSZone'
        dns_zone_param_ref = functions.ref(dns_zone_param_name)
        dns_name_param_name = name + 'DNSName'
        dns_name_param_ref = functions.ref(dns_name_param_name)
        dns_ttl_param_name = name + 'DNSTimeToLive'
        dns_ttl_param_ref = functions.ref(dns_ttl_param_name)
        dns_name_is_none = name + 'DNSNameUseStackName'
        dns_default_record_name = functions.join('.', functions.ref('AWS::StackName'), dns_zone_param_ref)
        dns_record_name = functions.join('.', dns_name_param_ref, dns_zone_param_ref)

        self.parameters.add(
            core.Parameter(dns_zone_param_name, 'String', {
                'Default': zone_name,
                'Description': 'DNS Zone for instance records'
            }))
        self.parameters.add(
            core.Parameter(dns_name_param_name, 'String', {
                'Default': 'UseStackName' if record_name is None else record_name,
                'Description': 'DNS Record Name without the Zone'
            }))
        self.parameters.add(
            core.Parameter(dns_ttl_param_name, 'String', {
                'Default': ttl,
                'Description': 'DNS Record Name time to live value in seconds'
            }))
        self.conditions.add(
            core.Condition(
                dns_name_is_none,
                functions.c_equals(dns_name_param_ref, 'UseStackName')
            ))

        self.resources.add(core.Resource(name + 'DNS', 'AWS::Route53::RecordSetGroup', {
            'HostedZoneName': dns_zone_param_ref,
            'RecordSets': [
                {
                    'Name': functions.c_if(dns_name_is_none, dns_default_record_name, dns_record_name),
                    'Type': 'A',
                    'TTL': dns_ttl_param_ref,
                    'ResourceRecords': values
                }
            ]
        }))

    def add_dns_cnames(self, name, zone_name, elb, record_names, ttl=300):
        dns_zone_param_name = name + 'DNSZone'
        dns_zone_param_ref = functions.ref(dns_zone_param_name)
        dns_ttl_param_name = name + 'DNSTimeToLive'
        dns_ttl_param_ref = functions.ref(dns_ttl_param_name)

        self.parameters.add(
            core.Parameter(dns_zone_param_name, 'String', {
                'Default': zone_name,
                'Description': 'DNS Zone for loadbalancer records'
            }))
        self.parameters.add(
            core.Parameter(dns_ttl_param_name, 'String', {
                'Default': ttl,
                'Description': 'DNS Record Name time to live value in seconds'
            }))
        record_sets = [
            dict(
                Name=functions.join('.', record_name, dns_zone_param_ref),
                Type='CNAME',
                TTL=dns_ttl_param_ref,
                ResourceRecords=[elb.canonical_hosted_zone_name()]
            )
            for record_name in record_names
            ]
        self.resources.add(core.Resource(name + 'DNS', "AWS::Route53::RecordSetGroup", {
            "HostedZoneName": dns_zone_param_ref,
            "Comment": "Zone apex targeted to " + elb.name,
            "RecordSets": record_sets
        }))

    def add_dns_cname(self, name, zone_name, resource=None, record_name=None, ttl=300, elb=None):
        dns_zone_param_name = name + 'DNSZone'
        dns_zone_param_ref = functions.ref(dns_zone_param_name)
        dns_name_param_name = name + 'DNSName'
        dns_name_param_ref = functions.ref(dns_name_param_name)
        dns_ttl_param_name = name + 'DNSTimeToLive'
        dns_ttl_param_ref = functions.ref(dns_ttl_param_name)
        dns_name_is_none = name + 'DNSNameUseStackName'
        dns_default_record_name = functions.join('.', functions.ref('AWS::StackName'), dns_zone_param_ref)
        dns_record_name = functions.join('.', dns_name_param_ref, dns_zone_param_ref)

        self.parameters.add(
            core.Parameter(dns_zone_param_name, 'String', {
                'Default': zone_name,
                'Description': 'DNS Zone for loadbalancer records'
            }))
        self.parameters.add(
            core.Parameter(dns_name_param_name, 'String', {
                'Default': 'UseStackName' if record_name is None else record_name,
                'Description': 'DNS Record Name without the Zone'
            }))
        self.parameters.add(
            core.Parameter(dns_ttl_param_name, 'String', {
                'Default': ttl,
                'Description': 'DNS Record Name time to live value in seconds'
            }))
        self.conditions.add(
            core.Condition(
                dns_name_is_none,
                functions.c_equals(dns_name_param_ref, 'UseStackName')
            ))

        # Load balancer or EC2
        if resource is None:
            resource = elb
            resource_record = elb.canonical_hosted_zone_name()
            resource_record_type = 'CNAME'
        else:
            resource_record = functions.get_att(resource, 'PrivateIp')
            resource_record_type = 'A'

        self.resources.add(core.Resource(name + 'DNS', "AWS::Route53::RecordSetGroup", {
            "HostedZoneName": dns_zone_param_ref,
            "Comment": "Zone apex targeted to " + resource.name,
            "RecordSets": [
                {
                    "Name": functions.c_if(dns_name_is_none, dns_default_record_name, dns_record_name),
                    "Type": resource_record_type,
                    "TTL": dns_ttl_param_ref,
                    "ResourceRecords": [resource_record]
                }]
        }))

    '''
    Add a generic load balancer which replaces all the product specific load balancers and is fed values(specific to
    the type of lb) from gen.py

    '''

    def add_load_balancer(self, name, **kwargs):

        listener_list = []
        loadbalancer_values = dict()
        for key, value in kwargs.iteritems():
            loadbalancer_values[key] = value

        if kwargs.get('listeners') is None and kwargs.get('custom_listener') is None:
            raise RuntimeError("protocol needs to be present in loadbalancer options")
        elif kwargs.get('listeners') is not None:
            for protocol, protocol_values in (kwargs.get('listeners', dict())).items():
                if protocol in ('https', 'http', 'tcp', 'ssl'):
                    listeners = (elb.ProtocolListener(protocol, protocol_values['instance_port'], protocol_values[
                        'load_balancer_port'], kwargs.get(
                        'certificate_id')))
                else:
                    raise RuntimeError('protocol needs to be one of HTTPS, HTTP, TCP, SSL')
                listener_list.append(listeners)
        # For custom listener (http/https) only
        else:
            listener_list.append(kwargs.get('custom_listener'))

        # if kwargs.get('health_check') is not None:
        #    health_check_param = elb.HealthCheck.build_health_check(kwargs.get('health_check'))
        #    loadbalancer_values[]

        if kwargs.get('health_check_path') is None:
            health_check_path = '/aptest.html'
            loadbalancer_values['health_check_path'] = health_check_path
        security_groups = kwargs.get('security_group')
        realm = kwargs.get('realm')
        subnets = kwargs.get('subnets')
        if subnets is None and realm is not None:
            subnets = self.subnets(realm)
            loadbalancer_values['subnets'] = subnets
        if security_groups is None and realm is not None:
            security_groups = self.generic_security_group(realm)
            loadbalancer_values['security_groups'] = security_groups
        loadbalancer_values['listeners'] = listener_list
        loadbalancer_values['env'] = self.env()
        lb = elb.LoadBalancer(name, **loadbalancer_values)
        self.resources.add(lb)

        return lb

    def add_launch_config(
            self,
            name,
            **kwargs
    ):

        lc_arguments = dict()
        for key, value in kwargs.iteritems():
            lc_arguments[key] = value

        # Security Groups
        security_groups = self.prepare_security_groups(name, kwargs.get("security_groups"))
        if security_groups is not None:
            lc_arguments['security_groups'] = security_groups

        # IAM Role
        iam_role = self.prepare_iam_role(name, kwargs.get("iam_role"))
        if iam_role is not None:
            lc_arguments['iam_role'] = iam_role

        # Key Pair
        key_pair = self.prepare_key_pair(name, kwargs.get("key_pair"))
        if key_pair is not None:
            lc_arguments['key_pair'] = key_pair

        # User Data
        if "user_data" in kwargs:
            user_data = kwargs.get("user_data")
            with open(user_data['file'], "r") as f:
                user_data_script = f.read()
            user_data_script = jinja2.Template(user_data_script)
            lc_arguments['user_data_script'] = user_data_script.render(**user_data['params'])

        lc = autoscaling.LaunchConfiguration(name, **kwargs)

        self.resources.add(lc)
        return lc

    def add_autoscaling_group(
            self,
            name,
            **kwargs
    ):

        asg_arguments = dict()
        for key, value in kwargs.iteritems():
            asg_arguments[key] = value

        # Subnet list
        vpc_zone_identifier = self.prepare_subnets(kwargs.get('realm'), kwargs.get('subnets'))
        asg_arguments['vpc_zone_identifier'] = vpc_zone_identifier

        # Scaling defaults
        if 'min_size' in kwargs:
            min_size_name = name + 'Min'
            self.parameters.add(
                core.Parameter(min_size_name, 'String', {
                    'Default': kwargs.get('min_size'),
                    'Description': 'Scaling Minimum for ' + name + ' AutoScale Group'
                })
            )
            asg_arguments['min_size'] = functions.ref(min_size_name)

        if 'max_size' in kwargs:
            max_size_name = name + 'Max'
            self.parameters.add(
                core.Parameter(max_size_name, 'String', {
                    'Default': kwargs.get('max_size'),
                    'Description': 'Scaling Maximum for ' + name + ' AutoScale Group'
                })
            )
            asg_arguments['max_size'] = functions.ref(max_size_name)

        if 'desired_capacity' in kwargs:
            des_size_name = name + 'Desired'
            self.parameters.add(
                core.Parameter(des_size_name, 'String', {
                    'Default': kwargs.get('desired_capacity'),
                    'Description': 'Scaling desired capacity for ' + name + ' AutoScale Group'
                })
            )
            asg_arguments['desired_capacity'] = functions.ref(des_size_name)

        asg = autoscaling.AutoScalingGroup(name, **asg_arguments)

        self.resources.add(asg)
        return asg

    def add_scheduled_action(
            self,
            name,
            **kwargs
    ):
        sa = autoscaling.ScheduledAction(name, **kwargs)
        self.resources.add(sa)
        return sa

    def add_instance(
            self,
            name,
            **kwargs
    ):

        instance_arguments = dict()
        for key, value in kwargs.iteritems():
            instance_arguments[key] = value

        # Security Groups
        security_groups = self.prepare_security_groups(name, kwargs.get("security_groups"))
        if security_groups is not None:
            instance_arguments['security_groups'] = security_groups

        # IAM Role
        iam_role = self.prepare_iam_role(name, kwargs.get("iam_role"))
        if iam_role is not None:
            instance_arguments['iam_role'] = iam_role

        # Key Pair
        key_pair = self.prepare_key_pair(name, kwargs.get("key_pair"))
        if key_pair is not None:
            instance_arguments['key_pair'] = key_pair

        # Availability Zone
        availability_zone = self.prepare_availability_zone(name, kwargs.get("availability_zone"))
        if availability_zone is not None:
            instance_arguments['availability_zone'] = availability_zone

        # User Data
        if "user_data" in kwargs:
            user_data = kwargs.get("user_data")
            with open(user_data['file'], "r") as f:
                user_data_script = f.read()
            user_data_script = jinja2.Template(user_data_script)
            instance_arguments['user_data_script'] = user_data_script.render(**user_data['params'])

        # The actual instance
        instance = ec2.Instance(name, **instance_arguments)

        # Elastic IP
        if "elastic_ips" in kwargs:
            self.assocate_elastic_ips(name, instance, kwargs.get("elastic_ips"))

        self.resources.add(instance)
        return instance

    def add_volume(
            self,
            name,
            availability_zone,
            **kwargs
    ):
        instance_arguments = dict()
        for key, value in kwargs.iteritems():
            instance_arguments[key] = value

        volume = ec2.Volume(name, availability_zone, **instance_arguments)
        self.resources.add(volume)
        return volume

    def add_rds(
            self,
            name,
            **kwargs
    ):
        dbinstance = rds.DBInstance(name, **kwargs)
        self.resources.add(dbinstance)
        return dbinstance

    def add_cloud_watch(
            self,
            name,
            evaluation_periods,
            comparison_operator,
            period,
            metric_name,
            statistic,
            threshold,
            **kwargs
    ):

        resource_name = '{0}CloudWatch'.format(name)
        cloudwatch_value = self.original_mapping(**kwargs)
        cloudwatch_alarm = cloudwatch.CloudWatchAlarm(resource_name,
                                                      evaluation_periods,
                                                      comparison_operator,
                                                      period,
                                                      metric_name,
                                                      statistic,
                                                      threshold,
                                                      **cloudwatch_value
                                                      )

        self.resources.add(cloudwatch_alarm)
        return cloudwatch_alarm

    def add_network_interface(
            self,
            name,
            **kwargs):
        resource_name = '{0}NetworkInterface'.format(name)
        network_interface_value = self.original_mapping(**kwargs)
        network_interface = ec2.NetworkInterface(resource_name, **network_interface_value)
        self.resources.add(network_interface)
        return network_interface

    def add_network_interface_attachment(
            self,
            name,
            **kwargs):

        networkinterfaceattachment_values = dict()
        for key, value in kwargs.iteritems():
            networkinterfaceattachment_values[key] = value

        nia = ec2.NetworkInterfaceAttachment(name, **networkinterfaceattachment_values)
        self.resources.add(nia)
        return nia

    # quick and dirty on adding custom parameters.
    def add_parameters(
            self,
            name,
            **kwargs):

        parameters_value = self.original_mapping(**kwargs)
        parameter = parameters.CustomParameters(name, **parameters_value)
        self.parameters.add(parameter)
        return parameter

    def add_sns_topic(
            self,
            name,
            **kwargs
    ):

        resource_name = '{0}SnsTopic'.format(name)
        sns_topic_value = self.original_mapping(**kwargs)
        sns_topic = sns.SnsTopic(resource_name, **sns_topic_value)
        self.resources.add(sns_topic)
        return  sns_topic