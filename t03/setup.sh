#!/bin/sh

current_dir="`dirname $0`"
copy_targets="t03-hosts.tmpl"

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 USERNAME" >&2
  exit 1
fi

if [ -e "$1" ]; then
  echo "$1 already exists" >&2
  exit 1
fi

username="$1"
mkdir "${username}"

(cd "${current_dir}" \
  && for d in ${copy_targets}; do
    cp -R "$d" "${username}/`basename $d .tmpl`"
  done
)
