from cfn_pyplates import core, functions
from environments import DEV, INT, STG, PRD


class ShutDownAtNight(core.Parameter):
    def __init__(self, name, default=None):
        super(ShutDownAtNight, self).__init__(name+'ShutdownAtNight', 'String', {
            "Description": name+' Shutdown at night',
            "Default": "no" if default in (None,False) else "yes",
            "AllowedValues": ["yes", "no"]
        })


class ShutdownAtNightCondition(core.Condition):
    def __init__(self, name, shutdown_at_night_parameter):
        super(ShutdownAtNightCondition, self).__init__(
            name+'ShutdownAtNightCondition',
            functions.c_equals(functions.ref(shutdown_at_night_parameter.name), 'yes')
        )


class StartupTime(core.Parameter):
    def __init__(self, name, cron_line=None):
        if cron_line is None:
            cron_line = "00 11 * * 1-5"
        super(StartupTime, self).__init__(name+'StartupTime', 'String', {
            "Description" : "UTC Start time in cron format",
            "Default"     : cron_line
        })


class ShutdownTime(core.Parameter):
    def __init__(self, name, cron_line=None):
        if cron_line is None:
            cron_line = "00 23 * * *"
        super(ShutdownTime, self).__init__(name+'ShutdownTime', 'String', {
            "Description" : "UTC Stop time in cron format",
            "Default"     : cron_line
        })


class ScheduledActionUp(core.Resource):
    def __init__(self, asg, condition, startup_time_parameter):
        super(ScheduledActionUp, self).__init__(asg.name+'ScheduledActionUp', "AWS::AutoScaling::ScheduledAction", {
                "AutoScalingGroupName": functions.ref(asg.name),
                "MinSize": asg.min,
                "MaxSize": asg.max,
                "DesiredCapacity": asg.desired,
                "Recurrence": functions.ref(startup_time_parameter.name)
            }
        )
        self.update(dict(Condition=condition.name))


class ScheduledActionDown(core.Resource):
    def __init__(self, asg, condition, shutdown_time_parameter):
        super(ScheduledActionDown, self).__init__(asg.name+'ScheduledActionDown', "AWS::AutoScaling::ScheduledAction", {
                "AutoScalingGroupName": functions.ref(asg.name),
                "MinSize": "0",
                "MaxSize": "0",
                "DesiredCapacity": "0",
                "Recurrence": functions.ref(shutdown_time_parameter.name)
            }
        )
        self.update(dict(Condition=condition.name))


def calendar_scale(cft, asg, startup_cron=None, shutdown_cron=None, default=None):
    if default is None:
        default=cft.env() in [DEV, INT, STG]

    # Parameters
    parameter = ShutDownAtNight(asg.name, default=default)
    startup_time = StartupTime(asg.name, startup_cron)
    shutdown_time = ShutdownTime(asg.name, shutdown_cron)
    cft.parameters.add(parameter)
    cft.parameters.add(startup_time)
    cft.parameters.add(shutdown_time)

    # Condition for scaling based on parameter
    condition = ShutdownAtNightCondition(asg.name, parameter)
    cft.conditions.add(condition)

    # Actions (aka Resources)
    cft.resources.add(ScheduledActionUp(asg, condition, startup_time))
    cft.resources.add(ScheduledActionDown(asg, condition, shutdown_time))
