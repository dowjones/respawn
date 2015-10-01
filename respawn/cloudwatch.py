from cfn_pyplates import core
from respawn import util


class CloudWatchProperties(util.SetNonEmptyPropertyMixin, core.JSONableDict):
    """
    Available keyword arguments
    """
    def __init__(self, **kwargs):
        super(CloudWatchProperties, self).__init__(None, 'Properties')

        # ActionsEnabled : whether or not actions should be executed during any changes to the alarm's state.
        self._set_property('ActionsEnabled', kwargs.get('actions_enabled'))

        # AlarmActions : Actions to execute when this alarm transitions into an ALARM state from any other state.
        self._set_property('AlarmActions', kwargs.get('alarm_actions'))

        # AlarmDescription : The description for the alarm.
        self._set_property('AlarmDescription', kwargs.get('alarm_description'))

        # AlarmName : A name for the alarm. If not specify a name, AWS CloudFormation generates a unique physical ID
        self._set_property('AlarmName', kwargs.get('alarm_name'))

        # ComparisonOperator : You can specify the following values: GreaterThanOrEqualToThreshold
        # GreaterThanThreshold | LessThanThreshold | LessThanOrEqualToThreshold
        self._set_property('ComparisonOperator', kwargs.get('comparison_operator'))

        if kwargs.get('Dimensions') is not None:
            # Dimensions : The dimensions for the alarm's associated metric.
            self._set_property('Dimensions', transform_attribute(kwargs.get('dimensions')))

        # EvaluationPeriods : The number of periods over which data is compared to the specified threshold.
        self._set_property('EvaluationPeriods', kwargs.get('evaluation_periods'))

        # InsufficientDataActions : The list of actions to execute when this alarm transitions into an
        #  INSUFFICIENT_DATA state from any other state.
        self._set_property('InsufficientDataActions', kwargs.get('insufficient_data_actions'))

        # MetricName : The name for the alarm's associated metric.
        self._set_property('MetricName', kwargs.get('metric_name'))

        # Namespace : The namespace for the alarm's associated metric.
        self._set_property('Namespace', kwargs.get('namespace'))

        # OKActions : The list of actions to execute when this alarm transitions into an OK state from any other state.
        self._set_property('OKActions', kwargs.get('ok_actions'))

        # Period : The time over which the specified statistic is applied.
        # You must specify a time in seconds that is also a multiple of 60.
        self._set_property('Period', kwargs.get('period'))

        # Statistic : The statistic to apply to the alarm's associated metric.
        self._set_property('Statistic', kwargs.get('statistic'))

        # Threshold : The value against which the specified statistic is compared.
        self._set_property('Threshold', kwargs.get('threshold'))

        # Unit : The unit for the alarm's associated metric.
        self._set_property('Unit', kwargs.get('unit'))


class CloudWatchAlarm(core.Resource):
    """
    Creates cloudwatch alarm.

    :param evaluation_period
    :param namespace
    :param period
    :param statistics
    :param threshold
    :param comparison_operator

    kwargs
        - actions_enabled: Boolean
        - alarm_actions: [ String, ... ]
        - alarm_description: String
        - alarm_name: String
        - dimensions: [ Metric dimension, ... ]
        - insufficient_data_actions: [ String, ... ],
        - metric_name: String,
        - ok_actions: [ String, ... ],
        - unit: String
    """
    def __init__(self,
                 name,
                 evaluation_periods,
                 comparison_operator,
                 period,
                 metric_name,
                 statistic,
                 threshold,
                 **kwargs
                 ):
        super(CloudWatchAlarm, self).__init__(name, 'AWS::CloudWatch::Alarm')
        self.Properties = CloudWatchProperties(**kwargs)


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
