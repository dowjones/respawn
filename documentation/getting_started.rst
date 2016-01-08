====================
**Getting Started**
====================

This page describes how to download, install and use the basic functionality of respawn.

**Installation**
################


To install respawn, simply:

**Windows/Unix/Mac OS X**
==========================

- Open command prompt and execute pip command :

::

    pip install respawn


**Usage - Template Generation**
################################

to use respawn, in your command prompt/terminal :

::

    $ respawn pathToYAML.yaml

to create & validate the JSON against AWS using `boto <https://github.com/boto/boto>`_ and pipe output to a file:

::

    $ respawn --validate pathToYAML.yaml > pathToJSON.json

to pipe the output to a file :

::

    $ respawn pathToYAML.yaml > pathToJSON.json

where:
 - pathToYAML.yaml = the YAML file that needs to be processed into JSON.
 - pathToJSON.json = the JSON file containing AWS cloudformation.

For exhaustive documentation and help with specific keywords to be used with resources , got to usage section.


**Dependencies**
#################

- boto==2.32.1
- nose==1.3.3
- cfn-pyplates==0.4.3
- Jinja2==2.7.3
- enum34
- pytest==2.7.1

**Next Steps**
###############

That concludes the getting started guide for respawn. Hopefully you're excited about the possibilities of respawn and
ready to begin using respawn with your applications.

We've covered the basics of respawn in this guide. We recommend moving on to the usage next, which serves
as a complete reference to all the features of respawn.