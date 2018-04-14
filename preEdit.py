#!/usr/bin/python
import os
import commands

return_code,output = commands.getstatusoutput("pwd");
print "path is "+output
git_cmd = 'git log --pretty="%s"';

return_code,output = commands.getstatusoutput(git_cmd);
print "git output is \n"+output


