#!/bin/bash

if [ "$IS_PUSH" == "yes" ];then
  hexo clean;
  git add .;
  git commit -m "push to source either after edit";
  git push https://"$GH_TOKEN"@"$GH_REF"
fi


