import unittest
from respawn import sns


class TestSns(unittest.TestCase):
    def test_subscription(self):
        sample_attribute = {'endpoint': 'x', 'protocol': 'y'}
        v = sns.Subscription(**sample_attribute)
        assert v == {'Endpoint': 'x', 'Protocol': 'y'}

    def test_SnsTopicProperties(self):
        sample_kwargs = {'topic_name': 'SampleTopic', 'display_name': 'MySnSTopic'}
        v = sns.SnsTopicProperties(**sample_kwargs)

        assert v == {
            "DisplayName": "MySnSTopic",
            "TopicName": "SampleTopic"
        }

    def test_SnsTopic(self):
        pass

    def test_recurse_kwargs_list(self):
        sample_kwargs = {'topic_name': 'SampleTopic', 'display_name': 'MySnSTopic',
                         'subscription': [{'endpoint': {'ref': 'OpsGenieEndpoint'}, 'protocol': 'https'},
                                          {'endpoint': 'https://sampleSite.com', 'protocol': 'http'}]}
        sample_kwargs_no_suscription = {'topic_name': 'SampleTopic', 'display_name': 'MySnSTopic'}

        v = sns.recurse_kwargs_list('subscription', sns.Subscription, **sample_kwargs)
        assert str(
            v) == "[Subscription([('Endpoint', {'ref': 'OpsGenieEndpoint'}), ('Protocol', 'https')]), Subscription([('Endpoint', 'https://sampleSite.com'), ('Protocol', 'http')])]"

        v = sns.recurse_kwargs_list('subscription', sns.Subscription, **sample_kwargs_no_suscription)
        assert v is None
