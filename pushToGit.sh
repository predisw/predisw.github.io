#!/bin/bash

last_commit_msg=`git log -1 --pretty="%B"`;

is_push=$(echo "$last_commit_msg" |grep "title")
echo "$is_push";

if [ "$is_push" != "" ];then
  git checkout -b tmp;
  git add .;
  git commit -m "push to source either after edit";
  git checkout source;
  git merge tmp;
  cat .git/HEAD;
  cat .git/refs/heads/source;
  cat .git/refs/remotes/origin/HEAD;
  cp .git/refs/heads/source .git/refs/remotes/origin/source;
  cat .git/refs/remotes/origin/source;

  git push -u https://"$GH_TOKEN"@"$GH_REF";
  if [ "$?" != "0" ];then
    exit -1;
  fi
fi

