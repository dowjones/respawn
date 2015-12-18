from cfn_pyplates import core
from respawn import util
from errors import RespawnResourceError


class AccessLoggingPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
        The AccessLoggingPolicy property captures detailed information for all requests made to your load balancer.

        kwargs
            - emit_interval: Integer
            - enabled: Boolean
            - s3_bucket_name: String
            - s3_bucket_prefix: String
        """
    # ----------------------------------------------------------------------------------------------------------
    #  AccessLoggingPolicy
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(AccessLoggingPolicy, self).__init__(None, 'AccessLoggingPolicy')
        self._set_property('EmitInterval', kwargs.get('emit_interval'))
        self._set_property('Enabled', kwargs.get('enabled'))
        self._set_property('S3BucketName', kwargs.get('s3_bucket_name'))
        self._set_property('S3BucketPrefix', kwargs.get('s3_bucket_prefix'))


class AppCookieStickinessPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Generates one or more stickiness policies with sticky session lifetimes that follow that of an application-generated
    cookie. These policies can be associated only with HTTP/HTTPS listeners.

    kwargs
        - cookie_name: String
        - policy_name: String

    """
    # ----------------------------------------------------------------------------------------------------------
    #  AppCookieStickinessPolicy
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(AppCookieStickinessPolicy, self).__init__(None, 'AppCookieStickinessPolicy')
        self._set_property('CookieName', kwargs.get('cookie_name'))
        self._set_property('PolicyName', kwargs.get('policy_name'))


class AvailabilityZones(core.JSONableDict):
    pass


class ConnectionDrainingPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Decides whether deregistered or unhealthy instances can complete all in-flight requests.

    :param enabled: Boolean

    kwargs
        - timeout : Integer
    """
    # ----------------------------------------------------------------------------------------------------------
    #  ConnectionDrainingPolicy
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(ConnectionDrainingPolicy, self).__init__(None, 'ConnectionDrainingPolicy')
        self._set_property('Enabled', kwargs.get('enabled'))
        self._set_property('Timeout', kwargs.get('timeout'))


class ConnectionSettings(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Specifies how long front-end and back-end connections of your load balancer can remain idle.

    :param idle_timeout: Integer
    """
    # ----------------------------------------------------------------------------------------------------------
    #  ConnectionSettings
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, idle_timeout=60, **kwargs):
        super(ConnectionSettings, self).__init__(dict(IdleTimeout=idle_timeout))
        self._set_property('IdleTimeout', kwargs.get('idle_timeout'))


class HealthCheck(core.JSONableDict):
    """
    Creates application health check for the instances.

    :param healthy_threshold: String
    :param interval: String
    :param target: String
    :param timeout: String
    :param unhealthy_threshold: String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  HealthCheck
    # ----------------------------------------------------------------------------------------------------------

    def __init__(self, **kwargs):
        super(HealthCheck, self).__init__(None, 'HealthCheck')
        self['HealthyThreshold'] = kwargs.get('healthy_threshold', 3)
        self['Interval'] = kwargs.get('interval', 30)
        self['Timeout'] = kwargs.get('timeout', 5)
        self['UnhealthyThreshold'] = kwargs.get('unhealthy_threshold', 3)
        self['Target'] = kwargs.get('target')


class Listener(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    One or more listeners for this load balancer. Each listener must be registered for a specific port,
    and you cannot have more than one listener for a given port.

    :param instance_port: String
    :param load_balancer_port: String
    :param protocol: String

    kwargs
        - instance_protocol: String
        - policy_names:  [ String, ... ]
        - sSL_certificate_id: String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  Listener
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Listener, self).__init__(None, 'Listener')
        self._set_property("InstancePort", kwargs.get('InstancePort'))
        self._set_property("InstanceProtocol", kwargs.get('InstanceProtocol'))
        self._set_property("LoadBalancerPort", kwargs.get('LoadBalancerPort'))
        self._set_property("Protocol", kwargs.get('Protocol'))
        self._set_property("PolicyNames", kwargs.get('PolicyNames'))
        self._set_property("SSLCertificateId", kwargs.get('SSLCertificateId'))


class LBCookieStickinessPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Generates a stickiness policy with sticky session lifetimes controlled by the lifetime of the browser
    (user-agent), or by a specified expiration period. This policy can be associated only with HTTP/HTTPS listeners.

    kwargs
        - cookie_expiration_period: String
        - policy_name: String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  LBCookieStickinessPolicy
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(LBCookieStickinessPolicy, self).__init__(None, 'LBCookieStickinessPolicy')
        self._set_property("PolicyName", kwargs.get('policy_name'))
        self._set_property("CookieExpirationPeriod", kwargs.get('cookie_expiration_period'))


class Policies(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    A list of elastic load balancing policies to apply to this elastic load balancer.

    :param policy_name: String
    :param policy_type: String

    kwargs
        - attributes : [ { "Name" : String, "Value" : String }, ... ]
        - instance_ports : [ String, ... ]
        - load_balancer_ports" : [ String, ... ]
        - policy_name : String
        - Policy_type : String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  Policies
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Policies, self).__init__(None, 'Policies')
        self._set_property('PolicyName', kwargs.get('policy_name'))
        self._set_property('Attribute', transform_attribute(kwargs.get('attribute')))
        self._set_property('InstancePorts', kwargs.get('instance_ports'))
        self._set_property('LoadBalancerPorts', kwargs.get('load_balancer_ports'))
        self._set_property('PolicyType', kwargs.get('policy_type'))


class ProtocolListener(Listener):
    # ----------------------------------------------------------------------------------------------------------
    #  ProtocolListener
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, protocol, port, egres_port, certificateId=None, **protocol_values):
        protocol_dict = {"http": "HTTP", "https": "HTTPS", "tcp": "TCP", "ssl": "SSL"}
        if protocol_values.get('instance_protocol') is not None:
            protocol = protocol_dict[protocol]
            kwargs = dict(Protocol=protocol,
                          LoadBalancerPort=port,
                          InstancePort=egres_port,
                          InstanceProtocol=protocol_values.get('instance_protocol'),
                          SSLCertificateId=certificateId,
                          PolicyNames=protocol_values.get('policy_names')
                          )
        else:
            protocol = protocol_dict[protocol]
            kwargs = dict(Protocol=protocol,
                          LoadBalancerPort=port,
                          InstancePort=egres_port,
                          InstanceProtocol=protocol_values.get('instance_protocol'),
                          SSLCertificateId=certificateId,
                          PolicyNames=protocol_values.get('policy_names')
                          )
        super(ProtocolListener, self).__init__(**kwargs)


class Tags(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    An arbitrary set of tags (key-value pairs) for this load balancer.

    :param key: String
    :param value: String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  Tags
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(Tags, self).__init__(None, 'Tags')
        self._set_property('Key', kwargs.get('key'))
        self._set_property('Value', kwargs.get('value'))


class LoadBalancerProperties(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Available keyword arguments.
    """
    # ----------------------------------------------------------------------------------------------------------
    #  LoadBalancerProperties
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(LoadBalancerProperties, self).__init__(None, 'Properties')

        # AccessLoggingPolicy : Default is none
        if kwargs.get('access_logging_policy') is not None:
            self._set_property('AccessLoggingPolicy', AccessLoggingPolicy(**kwargs.get('access_logging_policy')))

        # AppCookieStickinessPolicy : Default is none
        self._set_property('AppCookieStickinessPolicy', kwargs.get('app_cookie_stickiness_policy'))

        # AvailabilityZones : Zones (use Subnets instead) - You can specify
        # the AvailabilityZones or Subnets property but not both.
        self._set_property('AvailabilityZones', kwargs.get('availability_zones'))

        # ConnectionDrainingPolicy : Default is none
        if kwargs.get('connection_draining_policy') is not None:
            self._set_property('ConnectionDrainingPolicy', ConnectionDrainingPolicy(**kwargs.get(
                'connection_draining_policy')))

        # ConnectionSettings : Default is 60 seconds
        if kwargs.get('connection_settings') is not None:
            self._set_property('ConnectionSettings', ConnectionSettings(**kwargs.get('connection_settings')))

        # CrossZone : Default is True for Cross AZ Load balancing
        self._set_property('CrossZone', kwargs.get('cross_zone', False))

        # HealthCheck
        if kwargs.get('health_check') is not None:
            self._set_property('HealthCheck', HealthCheck(**kwargs.get('health_check')))

        # Instances
        self._set_property('Instances', kwargs.get('instances'))

        # LBCookieStickinessPolicy
        self._set_property('LBCookieStickinessPolicy', kwargs.get('lb_cookie_stickiness_policy'))

        # LoadBalancerName : If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses
        # that ID for the load balancer.
        self._set_property('LoadBalancerName', kwargs.get('load_balancer_name'))

        # Listeners :
        if kwargs.get('listeners') is not None:
            self._set_property('Listeners', kwargs.get('listeners'))
        else:
            raise RespawnResourceError("listeners parameter is required for creating an ELB", 'Listeners')

        # Policies : Default is none
        self._set_property('Policies', kwargs.get('policies'))

        # Scheme : 
        self._set_property('Scheme', kwargs.get('scheme'))

        # SecurityGroups : Default is none
        self._set_property('SecurityGroups', kwargs.get('security_groups'))

        # Subnets : 
        self._set_property('Subnets', kwargs.get('subnets'))

        # Tags : 
        self._set_property('Tags', kwargs.get('tags'))


class LoadBalancer(core.Resource):
    # ----------------------------------------------------------------------------------------------------------
    #  LoadBalancer
    # ----------------------------------------------------------------------------------------------------------
    def __init__(self, name, **kwargs):
        super(LoadBalancer, self).__init__(name, 'AWS::ElasticLoadBalancing::LoadBalancer')

        env = kwargs.get('env')
        if env is None:
            raise RespawnResourceError("env parameter is required for properly tagging an ELB", 'Environment')

        availibility_zone = kwargs.get("availability_zones")

        subnets = kwargs.get("subnets")
        if availibility_zone is not None and subnets is not None:
            raise RespawnResourceError("You can specify the AvailabilityZones or Subnets property in the load "
                                       "balancer, but not both.", 'AvailabilityZone/Subnets', subnets)
        elif availibility_zone is not None and subnets is None:
            kwargs['availibility_zones'] = recurse_kwargs_list('availibility_zones', AvailabilityZones, **kwargs)
        else:
            # handle subnets here
            pass

        kwargs['tags'] = recurse_kwargs_list('tags', Tags, **kwargs)
        kwargs['app_cookie_stickiness_policy'] = recurse_kwargs_list('app_cookie_stickiness_policy',
                                                                     AppCookieStickinessPolicy, **kwargs)
        kwargs['lb_cookie_stickiness_policy'] = recurse_kwargs_list('lb_cookie_stickiness_policy',
                                                                    LBCookieStickinessPolicy, **kwargs)
        kwargs['policies'] = recurse_kwargs_list('policies', Policies, **kwargs)
        self.Properties = LoadBalancerProperties(**kwargs)


def transform_attribute(attribute_list):
    """
    Transforms tag attributes.

    kwargs
        - name: String
        - value: String
    """
    # ----------------------------------------------------------------------------------------------------------
    #  Transform attribute from lower case to upper case.
    # ----------------------------------------------------------------------------------------------------------
    updated_attribute_list = []
    for attribute_parameters in attribute_list:
        updated_attribute_list.append(
            {'Name': attribute_parameters.get('name'),
             'Value': attribute_parameters.get('value')})
    return updated_attribute_list


def recurse_kwargs_list(parameter_name, class_name, **kwargs):
    """
    Recurses through a list of kwargs.
    """
    if parameter_name in kwargs:
        parameter_list = kwargs.get(parameter_name)
        param_list = []
        for parameter in parameter_list:
            param_list.append(class_name(**parameter))
        return param_list
    else:
        pass
