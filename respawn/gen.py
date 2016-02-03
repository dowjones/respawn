from __future__ import print_function
from cfn_pyplates import functions
import respawn
import sys


def standardize_refs(d):
    """
    Recursively transform all ref's and get_att's in dictionary to CloudFormation references.
    """
    for k, v in d.iteritems():
        if isinstance(v, dict):
            standardize_refs(v)
        elif isinstance(v, list):
            for i in range(len(v)):
                if isinstance(v[i], dict):
                    standardize_refs(v[i])
                elif isinstance(v[i], str):
                    v[i] = transform_reference(v[i])
        elif isinstance(v, str):
            d[k] = transform_reference(v)


def transform_reference(v):
    """
    Transform ref and ref_att in dictionary to CloudFormation ref or get_att
    """
    if v.startswith('ref('):
        v = v[len('ref('):-1].strip()
        v = functions.ref(v)
    elif v.startswith('get_att('):
        v = [s.strip() for s in v[len('get_att('):-1].split(',')]
        v = functions.get_att(v[0], v[1])
    return v


# Initialize dictionary for resources
resources = dict()

# Build base template utilizing library
cft = respawn.cloudformation.Template(**options)

# Standardize all references
standardize_refs(options)


# ----------------------------------------------------------------------------------------------------------
# Load Balancers
# ----------------------------------------------------------------------------------------------------------
try:
    if 'load_balancers' in options:
        for name, lb_opts in options['load_balancers'].items():
            lb = cft.add_load_balancer(name, **lb_opts)
            resources[name] = lb
except Exception as e:
    raise RuntimeError("Required arguments missing from Load Balancer: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Instances
# ----------------------------------------------------------------------------------------------------------
try:
    if 'instances' in options:
        for name, instance_opts in options['instances'].items():
            resources[name] = cft.add_instance(name, **instance_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Instance. Exception: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Volumes
# ----------------------------------------------------------------------------------------------------------
try:
    if 'volumes' in options:
        volumes = options['volumes']
        for name, volume_opts in volumes.items():
            resources[name] = cft.add_volume(name, **volume_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Volume. Exception: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Auto-scaling Groups
# ----------------------------------------------------------------------------------------------------------
try:
    if 'auto_scale_groups' in options:
        auto_scale_groups = options['auto_scale_groups']
        for name, asg_opts in auto_scale_groups.items():
            resources[name] = cft.add_autoscaling_group(name, **asg_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Autoscaling Group: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Launch Configurations
# ----------------------------------------------------------------------------------------------------------
try:
    if 'launch_configurations' in options:
        launch_configurations = options['launch_configurations']
        for name, lc_opts in launch_configurations.items():
            resources[name] = cft.add_launch_config(name, **lc_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Launch Configuration: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Scheduled Actions
# ----------------------------------------------------------------------------------------------------------
try:
    if 'scheduled_actions' in options:
        scheduled_actions = options['scheduled_actions']
        for name, sa_opts in scheduled_actions.items():
            resources[name] = cft.add_scheduled_action(name, **sa_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Scheduled Action: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Lifecycle Hooks
# ----------------------------------------------------------------------------------------------------------
try:
    if 'lifecycle_hooks' in options:
        lifecycle_hooks = options['lifecycle_hooks']
        for name, lh_opts in lifecycle_hooks.items():
            resources[name] = cft.add_lifecycle_hook(name, **lh_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Lifecycle Hook: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# RDS
# ----------------------------------------------------------------------------------------------------------
try:
    if 'rds' in options:
        rds = options['rds']
        for name, rds_opts in rds.items():
            resources[name] = cft.add_rds_instance(name, **rds_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from RDS: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# CloudWatch
# ----------------------------------------------------------------------------------------------------------
try:
    if 'cloud_watch' in options:
        for name, cloud_watch_opts in options['cloud_watch'].items():
            resources[name] = cft.add_cloud_watch_alarm(name, **cloud_watch_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Cloud Watch: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Network Interfaces
# ----------------------------------------------------------------------------------------------------------
try:
    if 'network_interfaces' in options:
        for name, network_interface_opts in options['network_interfaces'].items():
            resources[name] = cft.add_network_interface(name, **network_interface_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Network Interface: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Network Interface Attachments
# ----------------------------------------------------------------------------------------------------------
try:
    if 'network_interface_attachments' in options:
        for name, nia_opts in options['network_interface_attachments'].items():
            resources[name] = cft.add_network_interface_attachment(name, **nia_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Network Interface Attachment: {0}: Exception: {1}".format(name, e))

# ----------------------------------------------------------------------------------------------------------
# Security Groups
# ----------------------------------------------------------------------------------------------------------
try:
    if 'security_group' in options:
        for name, sg_opts in options['security_group'].items():
            resources[name] = cft.add_security_group(name, **sg_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Security Group: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------------------------------------------
try:
    if 'parameters' in options:
        for name, parameter_opts in options['parameters'].items():
            cft.add_parameter(name, **parameter_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from Parameters")


# ----------------------------------------------------------------------------------------------------------
# SNS Topics
# ----------------------------------------------------------------------------------------------------------
try:
    if 'sns_topics' in options:
        for name, sns_opts in options['sns_topics'].items():
            resources[name] = cft.add_sns_topic(name, **sns_opts)
except Exception as e:
    raise RuntimeError("Required arguments missing from SNS Topic: {0}: Exception: {1}".format(name, e))


# ----------------------------------------------------------------------------------------------------------
# Route53 Record
# ----------------------------------------------------------------------------------------------------------
try:
    if 'record_set' in options:
        for name, values in options['record_set'].items():
            resources[name] = cft.add_route53_record_set(name, **values)
except Exception as e:
    raise RuntimeError("Required arguments missing from SNS Topic. Exception: ", e)
