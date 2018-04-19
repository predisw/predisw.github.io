#!/usr/bin/python
from datetime import datetime, timedelta
import commands
import os

"""
version: 1.0.0
date: 2018-04-17

"""

TITLE = "title"
CATEGORIES= "categories"
TAGS = "tags"
ORIGIN_SOURCE = "source/_sources"
BUILD_SOURCE = "source/_posts"

return_code,basePath = commands.getstatusoutput("pwd");
print "build path is "+basePath

get_last_commit_msg= 'git log -1 --pretty="%B"';


def getBuildDatetime():
    utc_dt = datetime.utcnow();
    bj_dt = utc_dt+timedelta(hours=8)
    print "build datetime is {}".format(bj_dt)
    return bj_dt



def getCommitMsgList():
    return_code,output = commands.getstatusoutput(get_last_commit_msg);
    if return_code == 0:
        if TITLE in output:
            return output.split("\n")
    else:
        raise Exception("can't get commit message",output)


def commitMsgToMap(msg):
    print "commit message is '{}'".format(msg)
    heads = dict()
    infos = msg.split(";")
    for info in infos:
        if info:
            heads[info.split(":")[0]] = info.split(":")[1]
    print "heads of blog is {}".format(heads)
    return heads

def writeMsgToFile(msgMap):
    fileName = "{0}/{1}/{2}.md".format(basePath,BUILD_SOURCE,msgMap[TITLE])
    print "fileName is {}".format(fileName)
    with open(fileName,"w") as f:
        headStr = concatBlogHeadFromCommitMsg(msgMap)
        f.write(headStr)


def getCategoriesOrTagsString(msgMap,fieldType):
    if msgMap.has_key(fieldType):
        field = "{}:\n".format(fieldType)
        for fieldValue in msgMap[fieldType].split(","):
            field = field +"- {}\n".format(fieldValue)
        return field

def concatBlogHeadFromCommitMsg(msgMap):
    headStr = "---\n"
    headStr = headStr + "title: {}\n".format(msgMap[TITLE]) + "date: {}\n".format(getBuildDatetime().strftime( '%Y-%m-%d %H:%M:%S'))
    categorys = getCategoriesOrTagsString(msgMap,CATEGORIES)
    if categorys:
        headStr = headStr + categorys
    tags = getCategoriesOrTagsString(msgMap,TAGS)
    if tags:
        headStr = headStr+ tags
    headStr = headStr +"---\n"
    print "headStr is \n{}".format(headStr)
    return headStr


def mergeHeadBodyToBlog(title):
    source_file = os.path.join(basePath,ORIGIN_SOURCE,title+".md")
    posts_file = os.path.join(basePath,BUILD_SOURCE,title+".md")
    with open(posts_file,"a") as f:
        for line in open(source_file,"r").readlines():
            f.write(line)




def addHeadToBlogFromCommitMessage():
    msgsList = getCommitMsgList()
    if msgsList:
        for msg in msgsList:
            if msg:
                msgHeads = commitMsgToMap(msg)
                writeMsgToFile(msgHeads)
                mergeHeadBodyToBlog(msgHeads[TITLE])


if  __name__ == '__main__':
    addHeadToBlogFromCommitMessage()
