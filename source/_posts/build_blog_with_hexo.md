---
title: build-blog-with-hexo
date: 2018-03-25 11:14:09
categories:
- coding
tags:
- hexo

---


### install

1. hexo依赖
- 安装git 和准备github 帐号
- 安装Node.js
node.js 是hexo运行的基础,github 是部署存放blog内容的主机平台.
注意,hexo部署blog内容到github 是通过ssh,所以需要在github 上添加ssh-key.
方法参考: [Generating SSH keys](https://help.github.com/articles/connecting-to-github-with-ssh/)
2. install hexo
```
$ npm install -g hexo-cli  #npm 全称是Node Package Manager
$ hexo init <folder>  #folder 是存放blog 的地方
$ cd <folder>
$ npm install
```
参考: [Hexo Docs](https://hexo.io/docs/index.html)

<!--more-->

### build blog 

1. 写blog文章
`hexo new "标题"`    ***会在source/_posts中生产一个同名.md文件***
2. 生成html静态文件
`hexo generate` 或者是 `hexo g`     ***会生成静态文件到public 文件夹***
3. 启动本地blog服务器
`hexo server` 或 `hexo s`    ***在浏览器输入localhost:4000 就可以看到public文件夹内容***
`hexo s -o`    *自动在浏览器中打开静态html页面`*
4. 部署到github
`hexo deploy` 或者 `hexo d`  ***`hexo d -g` 或者 `hexo g -d`  都会自动重新生成静态文件并部署***
部署的过程是将public 文件夹的内容复制到.deploy_git ,再将.deploy_git 的内容上传到github.
5. 更换主题
可以下载主题到themes文件夹内,使用说明要参考不同的主题.
比较漂亮的主题有:
[next](https://github.com/iissnan/hexo-theme-next)
[yilia](https://github.com/litten/hexo-theme-yilia)


### 命令的理解
- `hexo clean`
会清理db.json 和public 文件夹的静态文件.有时候如果修改了没生效,可以清除了重新生产静态文件.

- `hexo server`
启动本地服务器,加载public 中的内容,如果source/_posts 文件有修改会自动加载修改.
but,实际测试自动侦测和加载修改部分会很慢,还不如取消自动侦测文件的变化:
`hexo server -s` 这个命令表示server只加载public文件夹内容,而不侦测文件的修改.
实际但我们想要看修改的内容是,可以手动更新: `hexo g`


### 配置

**URL静态化**

Hexo 默认 URL 地址为year/month/day/title/形式，而这种形式并不友好，我将之更改为year/month/title.html形式，_config.yml配置如下：
```yaml
permalink: :year/:month/:title.html
```

**去除代码块行号**

修改`_config.yml`配置项如下：
```
line_number: false
```

### 主题 yilia

**yilia 博客文章部分展示效果**
```
在source/_posts/ 中的.md 里添加 <!--more-->， 只有在 <!--more--> 之前的内容才会显示，其余隐藏
```
  
  
<br/>

参考: [启用Hexo开源博客系统](https://www.fanhaobai.com/2017/03/install-hexo.html)