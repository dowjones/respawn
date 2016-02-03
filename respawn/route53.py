from cfn_pyplates import core
from errors import RespawnResourceError


class AliasTarget(core.JSONableDict):
    """
        Creates an Alias Target
        :param dns_name: String
        :param hosted_zone_id: String
        kwargs
            - evaluate_target_health: Boolean
    """
    def __init__(
            self,
            dns_name,
            hosted_zone_id,
            **kwargs
    ):
        super(AliasTarget, self).__init__()

        self['DNSName'] = dns_name
        self['HostedZoneId'] = hosted_zone_id
        if 'evaluate_target_health' in kwargs:
            self['evaluate_target_health'] = kwargs.get('evaluate_target_health')


class GeoLocation(core.JSONableDict):
    """
        Creates a GeoLocation
        kwargs
            - continent_code: String
            - country_code: String
            - subdivision_code: String
    """
    def __init__(
            self,
            **kwargs
    ):
        super(GeoLocation, self).__init__()

        if 'continent_code' in kwargs:
            self['ContinentCode'] = kwargs.get('continent_code')
        if 'country_code' in kwargs:
            self['CountryCode'] = kwargs.get('country_code')
        if 'subdivision_code' in kwargs:
            self['SubdivisionCode'] = kwargs.get('subdivision_code')


class RecordSet(core.Resource):
    """
        Creates a Route53 RecordSet
        :param name: String
        :param domain_name: String
        kwargs
            - alias_target: AliasTarget
            - failover: String
            - geolocation: [ GeoLocation, ... ]
            - health_check_id: String
            - hosted_zone_id: String
            - hosted_zone_name: String
            - region: String,
            - resource_records: [ String, ...]
            - set_identifier: String
            - ttl: String
            - type: String
            - weight: String
        """

    def __init__(
            self,
            name,
            domain_name,
            **kwargs
    ):
        if "alias_target" in kwargs and "ttl" not in kwargs:
            raise RespawnResourceError("TTL (ttl) cannot be specified with AliasTarget (alias_target).", name)

        if "hosted_zone_id" in kwargs and "hosted_zone_name" in kwargs:
            raise RespawnResourceError("Only one of HostedZoneId (hosted_zone_id) or HostedZoneName (hosted_zone_name) "
                                       "can be specified.", name)

        attributes = kwargs.get("attributes", dict())

        properties = {
            'Name': domain_name,
        }

        if "alias_target" in kwargs:
            properties['AliasTarget'] = AliasTarget(**kwargs.get("alias_target"))
        if "failover" in kwargs:
            properties['Failover'] = kwargs.get("failover")
        if "geolocation" in kwargs:
            geolocations = [GeoLocation(**geolocation) for geolocation in kwargs.get("geolocation")]
            properties['GeoLocation'] = geolocations
        if "health_check_id" in kwargs:
            properties['HealthCheckId'] = kwargs.get("health_check_id")
        if "hosted_zone_id" in kwargs:
            properties['HostedZoneId'] = kwargs.get("hosted_zone_id")
        if "hosted_zone_name" in kwargs:
            properties['HostedZoneName'] = kwargs.get("hosted_zone_name")
        if "region" in kwargs:
            properties['Region'] = kwargs.get("region")
        if "resource_records" in kwargs:
            properties['ResourceRecords'] = kwargs.get("resource_records")
        if "set_identifier" in kwargs:
            properties['SetIdentifier'] = kwargs.get("set_identifier")
        if "ttl" in kwargs:
            properties['TTL'] = kwargs.get("ttl")
        if "type" in kwargs:
            properties['Type'] = kwargs.get("type")  # A | AAAA | CNAME | MX | NS | PTR | SOA | SPF | SRV | TXT
        if "weight" in kwargs:
            properties['Weight'] = kwargs.get("region")

        super(RecordSet, self).__init__(name, 'AWS::Route53::RecordSet', properties, attributes)
