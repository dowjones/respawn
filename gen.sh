#!/bin/bash

# Enter virtual env
if [ -z ${VIRTUAL_ENV} ]; then
	tmpdir=python-virtualenv
	virtualenv ${tmpdir}
	source ${tmpdir}/bin/activate
fi

validate=0
OPTIND=1
while getopts ":v" arg; do
  case $arg in
    v)
		validate=1
		;;
    \?)
		echo "Invalid option: -$OPTARG" >&2
		exit 1
		;;
    :)
		echo "Option -$OPTARG requires an argument." >&2
		exit 2
		;;
  esac
done
shift $((OPTIND-1))

StackRole=${1:-dev}
YamlSpec=${2:-*.yaml}

# Install deps
pip install -r py_reqs.txt || exit -3

# Build all of the required templates
for opt in ${StackRole}/${YamlSpec}; do

	opt_name=$(basename ${opt})
	opt_name=${opt_name%.yaml}
	cftName=${StackRole}/${opt_name}.template.json

	# Create the CFT
	echo "Generating ${cftName}..."
	cfn_py_generate gen.py -o ${opt} > ${cftName} 2> /dev/tty

	# Validate the CFT
	if [[ ${validate} -gt 0 ]]; then
		echo "Validating ${cftName}..."
		aws --region us-east-1 cloudformation validate-template --template-body file://${cftName}
		if [ $? != 0 ]; then
			echo "Validation FAILED"
			exit -4
		fi
	fi
	echo "Success"
	echo

done

