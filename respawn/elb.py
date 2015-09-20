from cfn_pyplates import core, functions
from respawn import util


class AccessLoggingPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(AccessLoggingPolicy, self).__init__(None, 'AccessLoggingPolicy')
        self._set_property('EmitInterval', kwargs.get('emit_interval'))
        self._set_property('Enabled', kwargs.get('enabled'))
        self._set_property('S3BucketName', kwargs.get('s3_bucket_name'))
        self._set_property('S3BucketPrefix', kwargs.get('s3_bucket_prefix'))


class AppCookieStickinessPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(AppCookieStickinessPolicy, self).__init__(None, 'AppCookieStickinessPolicy')
        self._set_property('CookieName', kwargs.get('cookie_name'))
        self._set_property('PolicyName', kwargs.get('policy_name'))


class AvailabilityZones(core.JSONableDict):
    pass


class ConnectionDrainingPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(ConnectionDrainingPolicy, self).__init__(None, 'ConnectionDrainingPolicy')
        self._set_property('Enabled', kwargs.get('enabled'))
        self._set_property('Timeout', kwargs.get('timeout'))


class ConnectionSettings(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, idle_timeout=60, **kwargs):
        super(ConnectionSettings, self).__init__(dict(IdleTimeout=idle_timeout))
        self._set_property('IdleTimeout', kwargs.get('idle_timeout'))


class HealthCheck(core.JSONableDict):
    def __init__(self, **kwargs):
        super(HealthCheck, self).__init__(None, 'HealthCheck')
        self['HealthyThreshold'] = kwargs.get('healthy_threshold', 3)
        self['Interval'] = kwargs.get('interval', 30)
        self['Timeout'] = kwargs.get('timeout', 5)
        self['UnhealthyThreshold'] = kwargs.get('unhealthy_threshold', 3)
        self['Target'] = str(kwargs.get('target'))


class HealthCheckTCP(HealthCheck):
    def __init__(self, port, is_secure=False, **kwargs):
        items = ['SSL' if is_secure else 'TCP', ':', str(port)]
        kwargs['Target'] = ''.join(items)
        super(HealthCheckTCP, self).__init__(**kwargs)


class HealthCheckHTTP(HealthCheck):
    def __init__(self, port, path, is_secure=False, **kwargs):
        items = ['https' if is_secure else 'http', ':', str(port), path]
        kwargs['Target'] = ''.join(items)
        super(HealthCheckHTTP, self).__init__(**kwargs)


class Listener(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(Listener, self).__init__(None, 'Listener')
        self._set_property("InstancePort", kwargs.get('InstancePort'))
        self._set_property("InstanceProtocol", kwargs.get('InstanceProtocol'))
        self._set_property("LoadBalancerPort", kwargs.get('LoadBalancerPort'))
        self._set_property("Protocol", kwargs.get('Protocol'))
        self._set_property("PolicyNames", kwargs.get('PolicyNames'))
        self._set_property("SSLCertificateId", kwargs.get('SSLCertificateId'))


class HttpListener(Listener):
    def __init__(self, port, egres_port, certificateId=None):
        protocol = 'HTTP' if certificateId is None else 'HTTPS'
        kwargs = dict(
            Protocol=protocol,
            LoadBalancerPort=port,
            InstancePort=egres_port,
            InstanceProtocol=protocol,
            SSLCertificateId=certificateId
        )
        super(HttpListener, self).__init__(**kwargs)


class HttpListener(Listener):
    def __init__(self, port, egres_port, certificateId=None):
        protocol = 'HTTP' if certificateId is None else 'HTTPS'
        kwargs = dict(
            Protocol=protocol,
            LoadBalancerPort=port,
            InstancePort=egres_port,
            InstanceProtocol=protocol,
            SSLCertificateId=certificateId
        )
        super(HttpListener, self).__init__(**kwargs)


class LBCookieStickinessPolicy(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(LBCookieStickinessPolicy, self).__init__(None, 'LBCookieStickinessPolicy')
        self._set_property("PolicyName", kwargs.get('policy_name'))
        self._set_property("CookieExpirationPeriod", kwargs.get('cookie_expiration_period'))


class Policies(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(Policies, self).__init__(None, 'Policies')
        self._set_property('PolicyName', kwargs.get('policy_name'))
        self._set_property('Attribute', transform_attribute(kwargs.get('attribute')))
        self._set_property('InstancePorts', kwargs.get('instance_ports'))
        self._set_property('LoadBalancerPorts', kwargs.get('load_balancer_ports'))
        self._set_property('PolicyType', kwargs.get('policy_type'))


class ProtocolListener(Listener):
    def __init__(self, protocol, port, egres_port, certificateId=None):
        kwargs = dict(
            Protocol=protocol,
            LoadBalancerPort=port,
            InstancePort=egres_port,
            InstanceProtocol=protocol,
            SSLCertificateId=certificateId
        )
        super(ProtocolListener, self).__init__(**kwargs)


class TcpListener(Listener):
    def __init__(self, port, egres_port, certificateId=None):
        protocol = 'TCP' if certificateId is None else 'SSL'
        kwargs = dict(
            Protocol=protocol,
            LoadBalancerPort=port,
            InstancePort=egres_port,
            InstanceProtocol=protocol,
            SSLCertificateId=certificateId
        )
        super(TcpListener, self).__init__(**kwargs)


class Tags(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(Tags, self).__init__(None, 'Tags')
        self._set_property('Key', kwargs.get('key'))
        self._set_property('Value', kwargs.get('value'))


class LoadBalancerProperties(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    def __init__(self, **kwargs):
        super(LoadBalancerProperties, self).__init__(None, 'Properties')

        ''' Available keyword arguments '''

        # AccessLoggingPolicy : Default is none
        self._set_property('AccessLoggingPolicy', AccessLoggingPolicy(**kwargs.get('access_logging_policy')))

        # AppCookieStickinessPolicy : Default is none
        self._set_property('AppCookieStickinessPolicy', kwargs.get('app_cookie_stickiness_policy'))

        # AvailabilityZones : Zones (use Subnets instead) - You can specify
        # the AvailabilityZones or Subnets property but not both.
        self._set_property('AvailabilityZones', kwargs.get('availability_zones'))

        # ConnectionDrainingPolicy : Default is none
        self._set_property('ConnectionDrainingPolicy', ConnectionDrainingPolicy(**kwargs.get(
            'connection_draining_policy')))

        # ConnectionSettings : Default is 60 seconds
        self._set_property('ConnectionSettings', ConnectionSettings(**kwargs.get('connection_settings')))

        # CrossZone : Default is True for Cross AZ Load balancing
        self._set_property('CrossZone', kwargs.get('cross_zone', False))

        # HealthCheck : 
        self._set_property('HealthCheck', HealthCheck(**kwargs.get('health_check')))

        # Instances : 
        self._set_property('Instances', kwargs.get('instances'))

        # LBCookieStickinessPolicy :
        self._set_property('LBCookieStickinessPolicy', kwargs.get('lb_cookie_stickiness_policy'))

        # LoadBalancerName : If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses
        # that ID for the load balancer.
        self._set_property('LoadBalancerName', kwargs.get('load_balancer_name'))

        # Listeners : 
        self._set_property('Listeners', kwargs.get('listeners'))

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

    def is_internal(self):
        return self['Scheme'] == 'internal'


class LoadBalancer(core.Resource):
    def __init__(self, name, **kwargs):
        super(LoadBalancer, self).__init__(name, 'AWS::ElasticLoadBalancing::LoadBalancer')

        env = kwargs.get('env')
        if env is None:
            raise ValueError('env parameter is required for properly tagging an ELB')

        service_name = kwargs.get('service_name')
        if service_name is None:
            raise ValueError('service_name parameter is required for properly tagging an ELB')

        availibility_zone = kwargs.get("availability_zones")
        subnets = kwargs.get("subnets")
        if availibility_zone is not None and subnets is not None:
            raise ValueError("You can specify the AvailabilityZones or Subnets property in the load balancer, "
                             "but not both.")
        elif availibility_zone is not None and subnets is None:
            kwargs['availibility_zones'] = recurse_kwargs_list('availibility_zones', AvailabilityZones, **kwargs)
        else:
            # handle subnets here
            pass

        kwargs['tags'] = recurse_kwargs_list('tags', Tags, **kwargs)
        kwargs['tags'].append({'Value': env, 'Key': 'env'})
        kwargs['tags'].append({'Value': service_name, 'Key': 'servicename'})

        kwargs['app_cookie_stickiness_policy'] = recurse_kwargs_list('app_cookie_stickiness_policy',
                                                                     AppCookieStickinessPolicy, **kwargs)
        kwargs['lb_cookie_stickiness_policy'] = recurse_kwargs_list('lb_cookie_stickiness_policy',
                                                                    LBCookieStickinessPolicy, **kwargs)
        kwargs['policies'] = recurse_kwargs_list('policies', Policies, **kwargs)
        self.Properties = LoadBalancerProperties(**kwargs)

    def canonical_hosted_zone_name(self):
        attr_name = 'DNSName' if self.Properties.is_internal() else 'CanonicalHostedZoneName'
        return functions.get_att(self.name, attr_name)

    def canonical_hosted_zone_id(self):
        return functions.get_att(self.name, "CanonicalHostedZoneNameID")


def transform_attribute(attribute_list):
    updated_attribute_list = []
    for attribute_parameters in attribute_list:
        updated_attribute_list.append(
            {'Name': attribute_parameters.get('name'),
             'Value': attribute_parameters.get('value')})
    return updated_attribute_list


def recurse_kwargs_list(parameter_name, class_name, **kwargs):
    if parameter_name in kwargs:
        parameter_list = kwargs.get(parameter_name)
        param_list = []
        for parameter in parameter_list:
            param_list.append(class_name(**parameter))
        return param_list
    else:
        pass


def make_web(
        name,
        port,
        health_check_path,
        security_groups,
        subnets,
        health_check_port=None,
        egres_port=None,
        certificateId=None
):
    if egres_port is None:
        egres_port = port

    if health_check_port is None:
        health_check_port = egres_port

    return LoadBalancer(
        name,
        Listeners=[HttpListener(port, egres_port, certificateId)],
        HealthCheck=HealthCheckHTTP(port, health_check_path),
        Scheme='internet-facing',
        SecurityGroups=security_groups,
        Subnets=subnets
    )


def make_internal(
        name,
        port,
        health_check_path,
        security_groups,
        subnets,
        health_check_port=None,
        egres_port=None,
        certificateId=None
):
    if egres_port is None:
        egres_port = port

    if health_check_port is None:
        health_check_port = egres_port

    return LoadBalancer(
        name,
        Listeners=[HttpListener(port, egres_port, certificateId)],
        HealthCheck=HealthCheckHTTP(port, health_check_path),
        Scheme='internal',
        SecurityGroups=security_groups,
        Subnets=subnets
    )
