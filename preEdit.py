#!/usr/bin/python
from datetime import datetime, timedelta
import commands


TITLE = "title"
CATEGORIES= "categories"
TAGS = "tags"
ORIGIN_SOURCE = "source/_source"
BUILD_SOURCE = "source/_posts"

return_code,path = commands.getstatusoutput("pwd");
print "build path is "+path

git_cmd = 'git log -1 --pretty="%B"';


def getBuildDatetime():
    utc_dt = datetime.utcnow();
    bj_dt = utc_dt+timedelta(hours=8)
    print "build datetime is {}".format(bj_dt)
    return bj_dt



def getCommitMsgList():
    return_code,output = commands.getstatusoutput(git_cmd);
    if return_code == 0:
        if TITLE in output:
            return output.split()
    else:
        raise Exception("can't get commit message",output)


def commitMsgToMap(msg):
    print "commit message is '{}'".format(msg)
    heads = dict()
    infos = msg.split(";")
    for info in infos:
        heads[info.split(":")[0]] = info.split(":")[1]
    print "heads of blog is {}".format(heads)
    return heads

def writeMsgToFile(msgMap):
    fileName = "{0}/{1}/{2}.md".format(path,BUILD_SOURCE,msgMap[TITLE])
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




def main():
    msgsList = getCommitMsgList()
    if msgsList:
        for msg in msgsList:
            msgHeads = commitMsgToMap(msg)
            writeMsgToFile(msgHeads)



if  __name__ == '__main__':
    main()
