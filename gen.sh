#!/bin/bash

# Enter virtual env
if [ -z ${VIRTUAL_ENV} ]; then
	tmpdir=python-virtualenv
	virtualenv ${tmpdir}
	source ${tmpdir}/bin/activate
fi

StackRole=${1:-dev}

# Version control
source version.sh
PATCH=$((PATCH+1))
(
	echo MAJOR=${MAJOR}
	echo MINOR=${MINOR}
	echo PATCH=${PATCH}
) > version.sh
(
	echo MAJOR: ${MAJOR}
	echo MINOR: ${MINOR}
	echo PATCH: ${PATCH}
) > version.yaml

# Install deps
pip install -r py_reqs.txt || exit -2

# Build all of the required templates
for opt in ${StackRole}/*.yaml; do

	opt_name=$(basename ${opt})
	opt_name=${opt_name%.yaml}
	cftName=${StackRole}/${opt_name}.template.json

	# Create the CFT
	echo "Generating ${cftName}..."
	cfn_py_generate gen.py -o ${opt} &> ${cftName}

	# Validate the CFT
	echo "Validating ${cftName}..."
	aws --region us-east-1 cloudformation validate-template --template-body file://${cftName}
	if [ $? != 0 ]; then
		echo "Validation FAILED"
		exit -1
	fi
	echo "Success"
	echo

done

