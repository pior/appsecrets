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

git tag --list | egrep -q "^v${VERSION}$"
if [[ "$?" -eq 0 ]]; then
	echo "Error: a tag already exists for this version."
	exit 1
fi

set -ex

echo -e "\n ✭ update version in setup.py"
sed -i '' "s/version='[^']*'/version='${VERSION}'/" setup.py
sed -i '' "s/version=\"[^\"]*\"/version=\"${VERSION}\"/" setup.py

exit 0

echo -e "\n ✭ create release commit"
git commit -m "Release v${VERSION}"

echo -e "\n ✭ create tag"
git tag  "${VERSION}"

echo -e "\n ✭ push to origin"
git push --follow-tags
