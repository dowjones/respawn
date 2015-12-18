import unittest
from respawn import parameters


class TestParameters(unittest.TestCase):
    def test_CustomParameters(self):
        sample_kwargs = {
            'constraint_description': 'Malformed input-Parameter MyParameter must only contain upper and lower case letters',
            'description': 'sample description', 'default': '10.201.22.33', 'max_value': 34, 'min_value': 12,
            'allowed_values': ['sampleValue1', 'sampleValue2'], 'type': 'String', 'no_echo': True}
        v = parameters.CustomParameters("name", **sample_kwargs)
        assert v == {'Description': 'sample description', 'Default': '10.201.22.33', 'Type': 'String',
                     'AllowedValues': ['sampleValue1', 'sampleValue2'], 'NoEcho': True,
                     'ConstraintDescription': 'Malformed input-Parameter MyParameter must only contain upper and lower case letters'}
