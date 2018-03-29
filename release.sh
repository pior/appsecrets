#!/bin/bash

VERSION=$1
if [[ -z "${VERSION}" ]]; then
	echo "Usage: $0 VERSION"
	exit 1
fi

BRANCH=`git rev-parse --abbrev-ref HEAD`
if [[ "${BRANCH}" != "master" ]]; then
	echo "Error: not on the master branch."
	exit 1
fi

git diff-index --quiet HEAD --
if [[ "$?" -ne 0 ]]; then
	echo "Error: there is some uncommited changes."
	exit 1
fi

set -e

echo " ✭ create release commit"
git commit --allow-empty -m "Release ${VERSION}"

echo " ✭ create tag"
git tag  -a "${VERSION}" -m "Release ${VERSION}"

echo " ✭ push to origin"
git push --follow-tags
