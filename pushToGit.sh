#!/bin/bash

last_commit_msg=`git log -1 --pretty="%B"`;
echo "$last_commit_msg";

is_push=$(echo "$last_commit_msg" |grep "title")
echo "$is_push";

if [ "$is_push" != "" ];then
  hexo clean;
  git checkout source
  git add .;
  git commit -m "push to source either after edit";
  git branch -a;
  git branch -u origin/source
  git push https://"$GH_TOKEN"@"$GH_REF" origin source
fi


