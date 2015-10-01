from cfn_pyplates import core
from respawn import util


class Subscription(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Subscription is an embedded property of the AWS::SNS::Topic resource that describes the
    subscription endpoints for a topic.

    :param endpoint: String,
    :param protocol: String
    """
    def __init__(self, **kwargs):
        super(Subscription, self).__init__(None, 'Subscription')
        self._set_property('Endpoint', kwargs.get('endpoint'))
        self._set_property('Protocol', kwargs.get('protocol'))


class SnsTopicProperties(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    keyword arguments available.

    kwargs
        - display_name : String,
        - subscription : [ SNS Subscription, ... ]
        - topic_name : String
    """
    def __init__(self, **kwargs):
        super(SnsTopicProperties, self).__init__(None, 'Properties')

        ''' Available keyword arguments '''

        # DisplayName : A developer-defined string that can be used to identify this SNS topic.
        self._set_property('DisplayName', kwargs.get('display_name'))

        # Subscription : The SNS subscriptions (endpoints) for this topic.
        self._set_property('Subscription', kwargs.get('subscription'))

        # TopicName : A name for the topic. If you don't specify a name,
        # AWS CloudFormation generates a unique physical ID and uses that ID for the topic name.
        self._set_property('TopicName', kwargs.get('topic_name'))


class SnsTopic(core.Resource):
    """
    Creates an Amazon SNS topic.
    """

    def __init__(self,
                 name,
                 **kwargs
                 ):
        super(SnsTopic, self).__init__(name, 'AWS::SNS::Topic')
        kwargs['subscription'] = recurse_kwargs_list('subscription', Subscription, **kwargs)
        self.Properties = SnsTopicProperties(**kwargs)


def transform_attribute(attribute_list):
    updated_attribute_list = []
    for attribute_parameters in attribute_list:
        updated_attribute_list.append(
            {'Name': attribute_parameters.get('name'),
             'Value': attribute_parameters.get('value')})
    return updated_attribute_list


def recurse_kwargs_list(parameter_name, class_name, **kwargs):
    if parameter_name in kwargs:
        parameter_list = kwargs.get(parameter_name)
        param_list = []
        for parameter in parameter_list:
            param_list.append(class_name(**parameter))
        return param_list
    else:
        pass
