import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(sys.argv[1])))
from cfn_pyplates import core, functions
import djpp

stackName = options['stack_name']
resources = dict()

# Build base injector template
injector = djpp.inject.Injector(**options)
# Build base template
cft = djpp.cloudformation.Template(**options)


def add_lb_dns(name, elb, zones):
    cnt = 1
    for zone, opts in zones.items():
        resource_name = '{0}{1}'.format(name, cnt)
        cnt += 1
        if zone.endswith('.') is False:
            zone += '.'
        record_name = opts.get('record_name', opts.get('record_names'))
        if isinstance(record_name, list):
            opts['record_names'] = opts.pop('record_name')
            cft.add_dns_cnames(resource_name, elb=elb, zone_name=zone, **opts)
        else:
            cft.add_dns_cname(resource_name, elb=elb, zone_name=zone, **opts)


def add_instances_dns_round_robin(zones):
    cnt = 1
    for zone, opts in zones.items():
        resource_name = 'Instances{0}'.format(cnt)
        cnt += 1
        if zone.endswith('.') is False:
            zone += '.'
        opts['values'] = map(transform_reference, opts['values'])
        cft.add_dns_round_robin(resource_name, zone, **opts)


def fetch_reference(name):
    r = resources.get(name, cft.resources.get(name))
    if r is None:
        raise RuntimeError('Resource name {0} not found'.format(name))
    return r


def transform_reference(v):
    if v.startswith('ref('):
        v = v[len('ref('):-1].strip()
        v = functions.ref(fetch_reference(v).name)
    elif v.startswith('get_att('):
        v = [s.strip() for s in v[len('get_att('):-1].split(',')]
        v = functions.get_att(fetch_reference(v[0]).name, v[1])
    return v

'''Picks up the key from YAML for a specific type of load balancer from HTTP, HTTPS, SSL, TCP . injector class then
injects the value and send back the injected value in dictionary as **kwarg. Its then consumed by addLoadBalancer in
cloudformation.py which uses elb.py to structure the values in json and spit it back up. All propreitary values go to inject.py'''
if 'load_balancers' in options:
    valueInjection = dict(
        https_external=injector.https_external_lb,
        https_internal=injector.https_internal_lb,
        generic=injector.generic_lb
    )
    for key in options['load_balancers'].keys():
        makeLoadbalancer = valueInjection[key]
        for name, lb_options in options['load_balancers'][key].items():
            lbInjected = makeLoadbalancer(**lb_options)
        name = lbInjected['name']
        del lbInjected['name']
        lb = cft.add_load_balancer(name, **lbInjected)
        resources[name] = lb
        if 'dns' in lbInjected:
            add_lb_dns(name, lb, lbInjected['dns'])

if 'databases' in options:
    types = dict(
        postgre_sql=cft.addRDSPostgres,
        my_sql=cft.addRDSMySQL
    )
    for key in options['Databases'].keys():
        make_rds = types[key]
        for name, rds_opts in options['Databases'][key].items():
            rds = make_rds(name, **rds_opts)
            resources[name] = rds

if 'instances' in options:
    instances = options['instances']

    dns_zones = None
    if 'dns' in instances:
        dns_zones = instances['dns']
        del instances['dns']

    types = dict(
        linux=cft.add_linux_instance
    )

    for key in instances.keys():
        make_instance = types[key]
        for name, instance_opts in instances[key].items():
            instance_opts_injected = injector.ec2_instance_values(**instance_opts)
            inst = make_instance(name, **instance_opts_injected)
            resources[name] = inst

    if dns_zones is not None:
        print dns_zones
        add_instances_dns_round_robin(dns_zones)

if 'auto_scale_groups' in options:
    for tierName, stack in options['auto_scale_groups'].items():
        name = stackName + tierName
        add_asg = cft.addLinuxAutoScaleGroup

        if 'load_balancer' in stack:
            stack['load_balancer'] = resources[stack['load_balancer']]

        instance_arguments = stack.get('instance_arguments')
        if instance_arguments is not None:
            for k, v in instance_arguments.items():
                instance_arguments[k] = transform_reference(v)

        if 'windows' in stack:
            add_asg = cft.addWindowsAutoScaleGroup
            del stack['windows']

        add_asg(name, **stack)

if 'scheduled_actions' in options:

    scheduled_actions = options['scheduled_actions']

    for name, sa_opts in scheduled_actions.items():
        resources[name] = cft.add_scheduled_action(name, **sa_opts)

if 'rds' in options:
    rds = options['rds']

    for name, rds_opts in rds.items():
        rds_opts_injects = injector.rds_values(name, **rds_opts)
        resources[name] = cft.add_rds(name, **rds_opts_injects)

if 'cloud_watch' in options:
    types = dict(daq=cft.addCloudWatch)
    for key in options['cloud_watch'].keys():
        make_cloudwatch = types[key]
        for name, cloudwatch_opts in options['CloudWatch'][key].items():
            cloudwatch = make_cloudwatch(name, **cloudwatch_opts)
            resources[name] = cloudwatch

if 'network_interface_attachment' in options:
    types = dict(generic=injector.generic_nia)
    for key in options['network_interface_attachment'].keys():
        makeNia = types[key]
        for name, nia_options in options['network_interface_attachment'][key].items():
            niainjected = makeNia(**nia_options)
        name = niainjected['name']
        del niainjected['name']
        nia = cft.add_network_interface_attachment(name, **niainjected)
        resources[name] = nia

if 'parameters' in options:
    for name, parameter_options in options['parameters'].items():
        parameter_injected = injector.parameters(**parameter_options)
        parameters = cft.add_parameters(name, **parameter_injected)

if 'sns_topic' in options:
    SnsTopic = cft.addSnsTopic
    for name, values in options['sns_topic'].items():
        SnsTopicFunction = SnsTopic(name, **values)
        resources[name] = SnsTopicFunction
