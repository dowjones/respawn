import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(sys.argv[1])))
from yaml import load as yaml_load
from cfn_pyplates import core, functions
import djpp

Version='.'.join(map(str, yaml_load(file('version.yaml', 'r')).values()))
stackName=options['StackName']
resources=dict()

# Build base template
cft = djpp.cloudformation.Template(version=Version, **options)


def add_lb_dns(name, elb, zones):
    cnt=1
    for zone, opts in zones.items():
        resource_name='{0}{1}'.format(name,cnt)
        cnt +=1
        if zone.endswith('.') is False:
            zone +='.'
        record_name=opts.get('record_name', opts.get('record_names'))
        if isinstance(record_name, list):
            opts['record_names']=opts.pop('record_name')
            cft.add_dns_cnames(resource_name, elb=elb, zone_name=zone, **opts)
        else:
            cft.add_dns_cname(resource_name, elb=elb, zone_name=zone, **opts)


def add_instances_dns_round_robin(zones):
    cnt=1
    for zone, opts in zones.items():
        resource_name='Instances{0}'.format(cnt)
        cnt +=1
        if zone.endswith('.') is False:
            zone +='.'
        opts['values']=map(transform_reference, opts['values'])
        cft.add_dns_round_robin(resource_name, zone, **opts)


def fetch_reference(name):
    r=resources.get(name, cft.resources.get(name))
    if r is None:
        raise RuntimeError('Resource name {0} not found'.format(name))
    return r


def transform_reference(v):
    if v.startswith('ref('):
        v=v[len('ref('):-1].strip()
        v=functions.ref(fetch_reference(v).name)
    elif v.startswith('get_att('):
        v=[s.strip() for s in v[len('get_att('):-1].split(',')]
        v=functions.get_att(fetch_reference(v[0]).name, v[1])
    return v


if 'LoadBalancers' in options:
    types=dict(
        Web=cft.addProductWebLoadBalancer,
        App=cft.addApplicationLoadBalancer,
        MessageBus=cft.addMessageBusLoadBalancer,
        IDS=cft.addIDSLoadBalancer,
    )
    for key in options['LoadBalancers'].keys():
        make_loadbalancer=types[key]
        for name, lb_opts in options['LoadBalancers'][key].items():
            lb = make_loadbalancer(name, **lb_opts)
            resources[name]=lb
            if 'DNS' in lb_opts:
                add_lb_dns(name, lb, lb_opts['DNS'])


if 'Databases' in options:
    types=dict(
        Postgres=cft.addRDSPostgres,
        MySQL=cft.addRDSMySQL
    )
    for key in options['Databases'].keys():
        make_rds=types[key]
        for name, rds_opts in options['Databases'][key].items():
            rds = make_rds(name, **rds_opts)
            resources[name]=rds


if 'Instances' in options:
    dns_zones=None
    if 'DNS' in options['Instances']:
        dns_zones=options['Instances']['DNS']
        del options['Instances']['DNS']

    types=dict(
        Linux=cft.addInstanceLinux
    )
    for key in options['Instances'].keys():
        make_instance=types[key]
        for name, instance_opts in options['Instances'][key].items():
            inst = make_instance(name, **instance_opts)
            resources[name]=inst

    if dns_zones is not None:
        add_instances_dns_round_robin(dns_zones)



if 'AutoScaleGroups' in options:
    for tierName, stack in options['AutoScaleGroups'].items():
        name=stackName+tierName
        add_asg=cft.addLinuxAutoScaleGroup

        if 'load_balancer' in stack:
            stack['load_balancer']=resources[stack['load_balancer']]

        instance_arguments=stack.get('instance_arguments')
        if instance_arguments is not None:
            for k,v in instance_arguments.items():
                instance_arguments[k]=transform_reference(v)

        if 'Windows' in stack:
            add_asg=cft.addWindowsAutoScaleGroup
            del stack['Windows']

        add_asg(name, **stack)



if 'CloudWatch' in options:
    types=dict(DAQ=cft.addCloudWatch)
    for key in options['CloudWatch'].keys():
        make_cloudwatch=types[key]
        for name, cloudwatch_opts in options['CloudWatch'][key].items():
            cloudwatch = make_cloudwatch(name, **cloudwatch_opts)
            resources[name]=cloudwatch


if 'NetworkInterfaceAttachment' in options:
    networkInterfaceAttachment = cft.networkInterfaceAttachment
    for name, networkInterfaceOptions in options['NetworkInterfaceAttachment'].items():
        networkInterface = networkInterfaceAttachment(name, **networkInterfaceOptions)
        resources[name] = networkInterface


if 'Parameters' in options:
    for tierName, stack in options['Parameters'].items():
        name=tierName
        add_asg=cft.addCustomParameters
        add_asg(name, **stack)
