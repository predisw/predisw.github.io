#!/bin/bash

last_commit_msg=`git log -1 --pretty="%B"`;

is_push=$(echo "$last_commit_msg" |grep "title")
echo "$is_push";

if [ "$is_push" != "" ];then
  hexo clean;
  git log -n 3;
  git checkout -b tmp;
  git add .;
  git commit -m "push to source either after edit";
  git checkout source;
  git merge tmp;
  git log -n 3;
  git branch -a;
  cat .git/HEAD;
  cat .git/refs/heads/source;
  cat .git/refs/remotes/origin/HEAD;
  ls .git/refs/remotes/origin/;
  cp .git/refs/heads/source .git/refs/remotes/origin/source;
  cat .git/refs/remotes/origin/source;

  git push -u https://"$GH_TOKEN"@"$GH_REF" origin source;
  if [ "$?" != "0" ];then
    exit -1;
  fi
fi

