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
        record_name=opts.get('record_name')
        if record_name is None or isinstance(record_name, str) or isinstance(record_name, unicode):
            cft.add_dns_cname(resource_name, elb=elb, zone_name=zone, **opts)
        else:
            opts['record_names']=opts.pop('record_name')
            cft.add_dns_cnames(resource_name, elb=elb, zone_name=zone, **opts)


def transform_reference(v):
    if v.startswith('ref('):
        v=v[len('ref('):-1].strip()
        v=functions.ref(resources.get(v).name)
    elif v.startswith('get_att('):
        v=[s.strip() for s in v[len('get_att('):-1].split(',')]
        v=functions.get_att(resources.get(v[0]).name, v[1])
    return v


if 'LoadBalancers' in options:
    types=dict(
        Web=cft.addProductWebLoadBalancer,
        App=cft.addApplicationLoadBalancer,
        MessageBus=cft.addMessageBusLoadBalancer,
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
        Postgres=cft.addRDSPostgres
    )
    for key in options['Databases'].keys():
        make_rds=types[key]
        for name, rds_opts in options['Databases'][key].items():
            rds = make_rds(name, **rds_opts)
            resources[name]=rds


if 'Instances' in options:
    types=dict(
        Linux=cft.addInstanceLinux
    )
    for key in options['Instances'].keys():
        make_instance=types[key]
        for name, instance_opts in options['Instances'][key].items():
            inst = make_instance(name, **instance_opts)
            resources[name]=inst


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

