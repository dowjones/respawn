import unittest
from respawn import cloudwatch


class TestCloudwatch(unittest.TestCase):
    def test_transform_attribute(self):
        sample_attribute = [{'name': 'x', 'value': 'y'}, {'name': 'xx', 'value': 'yy'}]
        v = cloudwatch.transform_attribute(sample_attribute)
        assert v == [{'Name': 'x', 'Value': 'y'}, {'Name': 'xx', 'Value': 'yy'}]

    def test_cloudwatchProperties(self):
        sample_kwargs = {'alarm_actions': ['String1', 'String2'], 'ok_actions': ['String', 'String2'],
                         'alarm_description': 'sample description', 'namespace': 'sampleNamespace',
                         'alarm_name': 'test_alarm', 'actions_enabled': True,
                         'insufficient_data_actions': ['String', 'String2'], 'unit': 'String'}
        v = cloudwatch.CloudWatchProperties(10, 10, 10, "sample", 10,10, **sample_kwargs)
        assert v == {
            "ActionsEnabled": True,
            "AlarmActions": [
                "String1",
                "String2"
            ],
            "AlarmDescription": "sample description",
            "AlarmName": "test_alarm",
            "InsufficientDataActions": [
                "String",
                "String2"
            ],
            "Namespace": "sampleNamespace",
            "OKActions": [
                "String",
                "String2"
            ],
            "Unit": "String",
            'ComparisonOperator': 10,
            'EvaluationPeriods': 10,
            'MetricName': 'sample',
            'Period': 10,
            'Statistic': 10,
            'Threshold': 10
            }
