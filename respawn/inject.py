from respawn import elb, values, environments as envs
import random
from cfn_pyplates import core, functions


class Injector:
    def __init__(
            self,
            name=None,
            version=None,
            desc=None,
            opts=None,
            region=None,
            env=None,
            eap=None,
            **kwargs
    ):

        self.__DEV_ENVS = (envs.DEV, envs.INT)
        self.__PRD_ENVS = (envs.STG, envs.PRD)
        self.__region = region
        if region is None:  self.__region = 'us-east-1'
        env = kwargs.get('environment')
        if env is None:
            self.__env = envs.DEV
        else:
            self.__env = envs.validate(env)

            # super(injector, self).__init__(desc,opts)

    def original_mapping(self, **kwargs):
        injected_kwargs = dict()
        for key, value in kwargs.iteritems():
            injected_kwargs[key] = value
        return injected_kwargs

    def env(self):
        return self.__env

    def region(self):
        return self.__region

    def subnets(self, realm, env=None):
        if env is None:
            env = self.env()
        else:
            env = envs.validate(env)
        return [values.subnets[self.__region][realm][env][i] for i in
                values.availability_zones[self.__region][realm][env]]

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

    def format_elb_resource_name(self, name):
        name = 'Djin{0}{1}'.format(self.env().title(), name)
        name += 'LB' if 'LB' not in name else ''
        return name

    def format_nia_resource_name(self, name):
        name = 'Djin{0}'.format(self.env().title(), name)
        name += 'NIA' if 'NIA' not in name else ''
        return name

    def format_elb_name(self):
        # ToDo: Created at some point to name ELBs however a note about custom names
        # in the AWS docs leads me to believe this may be a bad idea
        # return functions.join('-', 'djin', self.env(), functions.ref('AWS::StackName'))
        return None

    def format_ec2_instance_name(self, name, realm):
        return values.instance_prefix[self.__region][realm][self.__env] + name

    def generic_nia(self, **kwargs):
        injected_kwargs = self.original_mapping(**kwargs)
        name = self.format_nia_resource_name(kwargs.get('name'))
        injected_kwargs['name'] = name

        return injected_kwargs

    '''Add a generic lb for multi protocol listeners - this shall be used for both DJ/open source '''

    def generic_lb(self, **kwargs):

        injected_kwargs = self.original_mapping(**kwargs)
        name = self.format_elb_resource_name(kwargs.get('name'))
        injected_kwargs['name'] = name

        return injected_kwargs

    ''' Add an HTTPS load balancer which is internet facing and uses 80/443 <-> 80/443 '''

    def https_external_lb(
            self,
            certificate_id=None,
            health_check_port=None,
            health_check_path=None,
            secure_health_check=True,
            **kwargs
    ):
        injected_kwargs = self.original_mapping(**kwargs)
        name = self.format_elb_resource_name(kwargs.get('name'))
        if health_check_port is None:
            if secure_health_check in (None, False):
                health_check_port = 80
            else:
                health_check_port = 443
        if health_check_path is None:
            health_check_path = '/aptest.html'
        listener = {'http': [elb.ProtocolListener('http', 80, 80)]}
        if certificate_id is not None:
            listener.update({'https': [elb.ProtocolListener('https', 443, 443, certificate_id)]})
        # scheme = kwargs.get('scheme', 'internet-facing' if self.is_production() else 'internal')
        injected_kwargs['name'] = name
        injected_kwargs['health_check_port'] = health_check_port
        injected_kwargs['health_check_path'] = health_check_path
        injected_kwargs['custom_listener'] = listener
        # injected_kwargs['scheme'] = scheme

        return injected_kwargs

    '''
    Add an HTTPS load balancer which is internal and uses 8443<->8443
    '''

    def https_internal_lb(
            self,
            certificate_id=None,
            health_check_path=None,
            security_group=None,
            realm=None,
            **kwargs
    ):
        injected_kwargs = self.original_mapping(**kwargs)
        name = self.format_elb_resource_name(kwargs.get('name'))
        health_check_port = 8443
        secure_health_check = True
        if certificate_id is None:
            health_check_port = 8080
            secure_health_check = False
        if realm is None:
            realm = 'protected'
        if health_check_path is None:
            health_check_path = '/aptest.html'

        listener = {'http': [elb.ProtocolListener('http', 8080, 8080)]}
        if certificate_id is not None:
            listener.update({'https': [elb.ProtocolListener('https', 8443, 8443, certificate_id)]})

        security_groups = [security_group]
        if "other_security_groups" in kwargs:
            security_groups += kwargs["other_security_groups"]
        injected_kwargs['name'] = name
        injected_kwargs['health_check_port'] = health_check_port
        injected_kwargs['health_check_path'] = health_check_path
        injected_kwargs['custom_listener'] = listener
        injected_kwargs['security_groups'] = security_groups
        injected_kwargs['secure_health_check'] = secure_health_check
        injected_kwargs['realm'] = realm

        return injected_kwargs

    def parameters(self, **kwargs):

        injected_kwargs = self.original_mapping(**kwargs)
        # restricting type to be string, number, comma delimited list and list<> only.
        if "type" not in kwargs or kwargs["type"] not in ['String', 'Number', 'CommaDelimitedList']:
            raise ValueError("type needs to be present for parameters and can be of one of the following : String,"
                             "Number, List<>, CommaDelimitedList or AWS-specific param. ")
        return injected_kwargs

    def volume_values(self, **kwargs):
        return kwargs

    def ec2_instance_values(self, **kwargs):

        injected_kwargs = self.original_mapping(**kwargs)

        if "hostname" not in kwargs:
            raise RuntimeError("Hostname required.")

        if "realm" not in kwargs:
            raise RuntimeError("Realm (realm) required. (private, internet, protected)")
        realm = kwargs.get('realm')
        if realm not in {"private", "internet", "protected"}:
            raise RuntimeError("Invalid realm specified. (private, internet, protected)")

        if "service_name" not in kwargs:
            raise RuntimeError("Service Name (service_name) required.")
        service_name = kwargs.get("service_name")

        tags = kwargs.get('tags', [])
        tags.append({'key': 'service_name', 'value': service_name})
        tags.append({'key': 'env', 'value': self.__env})
        tags.append({'key': 'eap', 'value': functions.ref('tagEAP')})
        rts_role = False
        for tag in tags:
            if tag['key'] == 'RTSRole':
                rts_role = False
                break

        if not rts_role:
            tags.append(
                {'key': 'Name', 'value': self.format_ec2_instance_name(kwargs.get("hostname"), kwargs.get("realm"))})

        if 'availability_zone' not in kwargs:
            availability_zone = random.choice(values.availability_zones[self.__region][realm][self.__env])
        else:
            availability_zone = kwargs['availability_zone']

        security_group_ids = kwargs.get("security_group_ids", self.default_security_group())
        subnet = kwargs.get("subnet", values.subnets[self.__region][realm][self.__env][availability_zone])
        if "chef_run_list" in kwargs and "chef_env" in kwargs:
            user_data_script = self.linux_ud(kwargs.get("chef_run_list"), kwargs.get("chef_env"),
                                             extra=kwargs.get("instance_arguments"))
            injected_kwargs['user_data_script'] = user_data_script

        injected_kwargs['realm'] = realm
        injected_kwargs['tags'] = tags
        injected_kwargs['availability_zone'] = availability_zone
        injected_kwargs['security_group_ids'] = security_group_ids
        injected_kwargs['subnet'] = subnet
        injected_kwargs['iam_role'] = kwargs.get("iam_role")

        return injected_kwargs

    """
    if "service_name" not in kwargs:
            raise RuntimeError("Service Name (service_name) required.")
        service_name = kwargs.get("service_name")

        tags = kwargs.get('tags', dict())
        tags['service_name'] = service_name
        tags['env'] = self.__env
        tags['eap'] = functions.ref('TagEAP')
        functions.join("", values.instance_prefix[region][realm][environment], instance_name.lower())
        tags['Name'] = self.format_ec2_instance_name(kwargs.get("host_name"), kwargs.get("realm"))
        if 'RTSRole' in tags:
            del tags['Name']
    """

    def auto_scaling_group_values(self, name, **kwargs):

        injected_kwargs = self.original_mapping(**kwargs)

        if "hostname" not in kwargs:
            raise RuntimeError("Hostname required.")

        if "realm" not in kwargs:
            raise RuntimeError("Realm (realm) required. (private, internet, protected)")
        realm = kwargs.get('realm')
        if realm not in {"private", "internet", "protected"}:
            raise RuntimeError("Invalid realm specified. (private, internet, protected)")

        if "service_name" not in kwargs:
            raise RuntimeError("Service Name (service_name) required.")
        service_name = kwargs.get("service_name")

        tags = kwargs.get('tags', [])
        tags.append({'key': 'service_name', 'value': service_name, 'propagate_at_launch': True})
        tags.append({'key': 'env', 'value': self.__env, 'propagate_at_launch': True})
        tags.append({'key': 'eap', 'value': functions.ref('TagEAP'), 'propagate_at_launch': True})

        rts_role = False
        for tag in tags:
            if tag['key'] == 'RTSRole':
                rts_role = False
                break
        if not rts_role:
            tags.append({'key': 'Name',
                         'value': functions.join("", values.instance_prefix[self.__region][realm][self.__env],
                                                 name.lower()), 'propagate_at_launch': True})

        if 'availability_zones' not in kwargs:
            availability_zones = zones = values.availability_zones[self.__region][realm][self.__env]
        else:
            availability_zones = kwargs['availability_zones']

        subnets = [values.subnets[self.__region][realm][self.__env][zone] for zone in zones]

        if "chef_run_list" in kwargs and "chef_env" in kwargs:
            if kwargs.get("windows", False):
                user_data_script = self.windows_ud_no_cfn_init(name, kwargs.get("chef_run_list"),
                                                               kwargs.get("chef_env"))
            else:
                user_data_script = self.linux_ud(kwargs.get("chef_run_list"), kwargs.get("chef_env"),
                                                 extra=kwargs.get("instance_arguments"))

            injected_kwargs['user_data_script'] = user_data_script

        injected_kwargs['realm'] = realm
        injected_kwargs['tags'] = tags
        injected_kwargs['availability_zones'] = availability_zones
        injected_kwargs['vpc_zone_identifier'] = subnets

        return injected_kwargs

    def launch_configuration_values(self, name, **kwargs):

        injected_kwargs = self.original_mapping(**kwargs)

        if "realm" not in kwargs:
            raise RuntimeError("Realm (realm) required. (private, internet, protected)")
        realm = kwargs.get('realm')
        if realm not in {"private", "internet", "protected"}:
            raise RuntimeError("Invalid realm specified. (private, internet, protected)")

        if 'availability_zone' not in kwargs:
            availability_zone = random.choice(values.availability_zones[self.__region][realm][self.__env])
        else:
            availability_zone = kwargs['availability_zone']

        security_groups = kwargs.get("security_groups", self.default_security_group())
        subnet = kwargs.get("subnet", values.subnets[self.__region][realm][self.__env][availability_zone])
        if "chef_run_list" in kwargs and "chef_env" in kwargs:
            if kwargs.get("windows", False):
                user_data_script = self.windows_ud_no_cfn_init(name, kwargs.get("chef_run_list"),
                                                               kwargs.get("chef_env"))
            else:
                user_data_script = self.linux_ud(kwargs.get("chef_run_list"), kwargs.get("chef_env"),
                                                 extra=kwargs.get("instance_arguments"))

            injected_kwargs['user_data_script'] = user_data_script

        injected_kwargs['realm'] = realm
        injected_kwargs['availability_zone'] = availability_zone
        injected_kwargs['security_group_ids'] = security_groups
        injected_kwargs['subnet'] = subnet
        injected_kwargs['iam_role'] = kwargs.get("iam_role")

        return injected_kwargs

    def rds_values(self, name, **kwargs):

        injected_kwargs = self.original_mapping(**kwargs)

        if "realm" not in kwargs:
            raise RuntimeError("Realm (realm) required. (private, internet, protected)")
        realm = kwargs.get('realm')
        if realm not in {"private", "internet", "protected"}:
            raise RuntimeError("Invalid realm specified. (private, internet, protected)")

        if "service_name" not in kwargs:
            raise RuntimeError("Service Name (service_name) required.")
        service_name = kwargs.get("service_name")

        if "instance_identifier" not in kwargs:
            injected_kwargs['instance_identifier'] = '{0}db-{1}'.format(name, self.env())

        if "subnet_group_name" not in kwargs:
            injected_kwargs['subnet_group_name'] = values.subnet_group[self.__region][realm][self.env()]

        tags = kwargs.get('tags', [])
        tags.append({'key': 'service_name', 'value': service_name})

        injected_kwargs['realm'] = realm
        injected_kwargs['service_name'] = service_name
        injected_kwargs['tags'] = tags

        return injected_kwargs

    # USER DATA
    def linux_ud(self, run_list, chef_env, extra=None):
        lines = [
            '#!/bin/bash -v\n'
            'CHEF_CONFIG=', values.CHEF_CONFIG_REF, '\n',
            'CHEF_RUNLIST=', run_list, '\n',
            'CHEF_ENV=', chef_env, '\n',
            'INTERVAL=', values.CHEF_INTERVAL_REF, '\n',
        ]

        if extra is not None:
            lines.append('declare -A EXTRA\n')
            for k, v in extra.iteritems():
                lines.append('EXTRA[{0}]='.format(k))
                lines.append(v)
                lines.append('\n')

        lines.append("""
    INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
    HOSTNAME=$(hostname)
    NODE_ID="${INSTANCE_ID}--${HOSTNAME}"
    curl $CHEF_CONFIG | bash
    cat <<<"{\\\"run_list\\\" : \\\"$CHEF_RUNLIST\\\"}" > /etc/chef/first-boot.json
    cat <<<"
    environment             \\\"$CHEF_ENV\\\"
    json_attribs            \\\"/etc/chef/first-boot.json\\\"
    node_name               \\\"$NODE_ID\\\"
    " >> /etc/chef/client.rb

    (
        cnt=0
        echo "{"
        for key in ${!EXTRA[@]};
        do
            [ $cnt -gt 0 ] && echo ","
            echo -n "\\\"${key}\\\" : \\\"${EXTRA[$key]}\\\""
            cnt=$((cnt+1))
        done
        echo
        echo "}"
        echo
    ) > /tmp/respawn.params.json

    mkdir /etc/dj/
    cp /tmp/respawn.params.json /etc/dj/respawn.params.json

    if [ ${INTERVAL} -gt 0 ]; then
        /usr/bin/chef-client -d -i ${INTERVAL}
    else
        /usr/bin/chef-client
    fi
    """
                     )
        return functions.join("", *lines)

    def windows_ud_no_cfn_init(self, lc_name, run_list, chef_env):
        return functions.join("", "<powershell>\n",
                              # AWS Input arguments

                              "$version = (Get-CimInstance Win32_OperatingSystem).Caption\n"
                              "If ($version -match '2012') {\n"
                              "$source = \"http://djin-artifact01.dowjones.net:8081/artifactory/ext-release-local/chef/fcm_chef/1.0.0/fcm_chef-1.0.0.ps1\"\n"
                              "}\n"
                              "ElseIf($version -match '2008') {\n"
                              "$source = \"http://djin-artifact01.dowjones.net:8081/artifactory/repo/chef/djinchefconfig/1.0.0/djinchefconfig-1.0.0.ps1\"\n"
                              "}\n"
                              "else {\n"
                              "$source = \"http://djin-artifact01.dowjones.net:8081/artifactory/repo/chef/djinchefconfig/1.0.0/djinchefconfig-1.0.0.ps1\"\n"
                              "}\n"

                              "$destination = \"c:\\cfn\\runchef.ps1\"\n"

                              "Invoke-WebRequest $source -OutFile $destination\n"

                              "Invoke-Expression \"$destination ",
                              " -REGION ", values.AWS_REGION_REF,
                              " -STACK_NAME ", values.AWS_STACK_NAME_REF,
                              " -STACK_ID ", values.AWS_STACK_ID_REF,
                              " -LC_NAME ", lc_name,
                              " -CHEF_RUNLIST ", run_list,
                              " -CHEF_ENV ", chef_env,
                              "\"\n"
                              "</powershell>"
                              )
