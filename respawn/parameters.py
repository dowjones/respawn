from cfn_pyplates import core


class CustomParameters(core.Parameter):
    def __init__(
            self,
            name,
            **kwargs
    ):
        parameters = {}

        if "default" in kwargs:
            parameters['Default'] = kwargs.get("default")
        if "type" in kwargs:
            parameters['Type'] = kwargs.get("type")
        if "allowed_values" in kwargs:
            parameters['AllowedValues'] = kwargs.get("allowed_values")
        if "description" in kwargs:
            parameters['Description'] = kwargs.get("description")
        if "no_echo" in kwargs:
            parameters['NoEcho'] = kwargs.get("no_echo")
        if "allowed_pattern" in kwargs and kwargs["type"] is "String":
            parameters['AllowedPattern'] = kwargs.get("allowed_pattern")
        if "max_length" in kwargs and kwargs["type"] is "String":
            parameters['MaxLength'] = kwargs.get("max_length")
        if "min_length" in kwargs and kwargs["type"] is "String":
            parameters['MinLength'] = kwargs.get("min_length")
        if "max_value" in kwargs and kwargs["type"] is "Number":
            parameters['MaxValue'] = kwargs.get("max_value")
        if "min_value" in kwargs and kwargs["type"] is "Number":
            parameters['MinValue'] = kwargs.get("min_value")
        if "constraint_description" in kwargs:
            parameters['ConstraintDescription'] = kwargs.get("constraint_description")

        super(CustomParameters, self).__init__(name, parameters['Type'], parameters)
