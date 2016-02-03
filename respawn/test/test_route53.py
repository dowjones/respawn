import pytest
from respawn import route53


def test_record_set():
    # Successful instance
    record_set = route53.RecordSet(name="TestRecordSet", domain_name="test.dowjones.net",
                                   failover="Primary", geolocation=[dict(continent_code="NA"),
                                                                    dict(country_code="US", subdivision_code="NJ")],
                                   health_check_id="1", hosted_zone_id="2", resource_records= ["aaa.dowjones.net",
                                                                                               "bbb.dowjones.net"],
                                   ttl="20", type="CNAME")
    assert record_set == {
        "Type": "AWS::Route53::RecordSet",
        "Properties": {
            "Name": "test.dowjones.net",
            "Failover": "Primary",
            "GeoLocation": [
                {
                    "ContinentCode": "NA",
                },
                {
                    "CountryCode": "US",
                    "SubdivisionCode": "NJ"

                }
            ],
            "HealthCheckId": "1",
            "HostedZoneId": "2",
            "ResourceRecords": [
                "aaa.dowjones.net",
                "bbb.dowjones.net"
            ],
            "TTL": "20",
            "Type": "CNAME"
        }
    }
