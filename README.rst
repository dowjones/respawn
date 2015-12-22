.. image:: Logo/PNG/respawn-logo-2.png
   :align: center

****************
Version History
****************

:Version: v1.0.0

* Initial release

************
Introduction
************
Infrastructure templates and utilities for building AWS CloudFormation stacks. Respawn uses `cfn-pyplates <https://github.com/seandst/cfn-pyplates/tree/master/cfn_pyplates>`_ to
generate CloudFormation templates. A pyplate is a class-based python representation of a JSON CloudFormation template and resources, with the goal of generating CloudFormation templates based on input python templates (pyplates!) that reflect the CloudFormation template hierarchy.

Respawn is a Python package that provides interfaces to Amazon Web Services - Cloudformation. It allows for easier and more user friendly and concise yaml keywords to create resources/parameters/userdata in CloudFormation stacks. This is used in Dow Jones pipeline and with success and has been modified to be as generic and serve all. Currently the library supports Python 2.7.

************
Authors
************
Respawn has been written by the following `authors <https://github.com/dowjones/respawn/graphs/contributors>`_. The
logo for respawn has been designed by `Gregor Louden <http://www.gregorlouden.com>`_.

*************
Documentation
*************
Documentation is written in sphinx and hosted on `readthedocs <https://github.dowjones
.net/pages/djin-productivity/respawn/index.html>`_

********
Services
********

At the moment, respawn supports:

* AutoScaling

  * AutoScalingGroup
  * LifecycleHook
  * ScalingPolicy
  * ScheduledAction

* CloudWatch

  * Alarm

* Elastic Compute Cloud (EC2)

  * Instance
  * NetworkInterface
  * NetworkInterfaceAttachment
  * SecurityGroup
  * Volume

* Elastic Load Balancing (ELB)

  * LoadBalancer

* Relational Database Service (RDS)

  * DBInstance

* Simple Notification Service (SNS)

  * Topic

The goal of respawn is to support the full breadth and depth of Amazon Web Services - resources. respawn is developed mainly using Python 2.7.x on Mac OSX and Ubuntu. It is known to work on Linux Distributions, Mac
OS X and Windows.


*************
Installation
*************

To install respawn, simply:

Windows/Unix/Mac OS X
######################

- Open command prompt and execute pip command :

::

    pip install respawn


****************************
Usage - Template Generation
****************************

to use respawn, in your command prompt/terminal :

::

    $ respawn pathToYAML.yaml

to create & validate the JSON against AWS using `boto <https://github.com/boto/boto>`_ and pipe output to a file:

::

    $ respawn --validate pathToYAML.yaml > pathToJSON.json

to pipe the output to a file :

::

    $ respawn pathToYAML.yaml > pathToJSON.json



****************************
Developing and Contribution
****************************
We'd love to get contributions from you! Take a look at the `CONTRIBUTING.rst <https://github
.com/dowjones/respawn/blob/master/CONTRIBUTING.rst>`_ to see how to get your changes merged in.

************
License
************
`ISC <https://github.com/dowjones/respawn/blob/master/LICENSE.md>`_