.. respawn documentation master file, created by
   sphinx-quickstart on Fri Sep 18 13:28:01 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
Respawn
========

Contents:

.. toctree::
   :maxdepth: 2

   getting_started
   usage
   source_code
   sample_yaml


Overview
########

Infrastructure templates and utilities for building AWS CloudFormation stacks. Respawn uses `cfn-pyplates <https://github.com/seandst/cfn-pyplates/tree/master/cfn_pyplates>`_ to
generate CloudFormation templates. A pyplate is a class-based python representation of a JSON CloudFormation template and resources, with the goal of generating CloudFormation templates based on input python templates (pyplates!) that reflect the CloudFormation template hierarchy.

Respawn is a Python package that provides interfaces to Amazon Web Services - Cloudformation. It allows for easier and more user friendly and concise YAML keywords to create resources/parameters/userdata in CloudFormation stacks. This is used in Dow Jones professional information business pipeline and with success and has been modified to be as generic and serve all. Currently the library supports Python 2.7 because of its dependency on cfn-pyplates.

Summary
#######

Respawn is template and utility for spawning AWS CloudFormation stacks from simpler YAML specifications. Respawn will consume a YAML file with documented keywords and spit out a CloudFormation stack json specification.


Key Features
#################

The key features of Respawn are:

- Automatic CloudFormation creation: Respawn detects your application type and builds a CloudFormation JSON for your application tailored to your use based on your YAML. It supports multiple resources/parameters/user-data that AWS supports. Please go through usage to see the list of resources respawn supports.

- Validates CloudFormation: Respawn validates the JSON created against AWS resources to confirm the correctness of your CloudFormation script. It utilizes boto3 and AWS credentials stored in your environment.






