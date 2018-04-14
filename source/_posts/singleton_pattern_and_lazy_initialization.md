---
title: singleton-pattern-and-lazy-initialization
date: 2018-03-25 21:14:09
categories:
- coding
tags:
- java
- design_pattern

---



单例模式 的实现方式之一：
```
public class Singleton {
    private static Singleton instance = new Singleton();
    private Singleton(){
        System.out.println("Singleton is instantiated");
    }
    public static Singleton getInstance() {
        return instance;
    }
}
```
为什么很多人不推荐这种实现方式？认为会在`类加载的时候就实例化 instance 了`。
**但是如果只是在其他类里声明这个类，构造函数里的字符串是不会被打印的。**如`Singleton singleton  = null;`类在被声明的时候肯定是被Classloader 加载了。
<!--more-->

***那如果是这样的话，什么才是lazy initialization ? 好处是什么呢？***

```java
public class Singleton {
    private static Singleton instance = new Singleton();
    private Singleton(){
        System.out.println("Singleton is instantiated");
    }
    public static Singleton getInstance() {
        return instance;
    }
    public static void doSomething(){
        System.out.println("do something");
    }
}

    @Test
    public void testLazyInitialization(){
        Singleton.doSomething();
    }

output:
Singleton is instantiated
do something

```
假如在`Singleton` 类加多一个其他的静态方法，当这个静态方法被调用时，就会触发`Singleton` 的静态域的初始化，这时就会实例化`instance` 了，但是这个`instance`实际是不需要的，因而这样就创建了一个无用的实例，消耗了资源。

这个时候就需要使用到lazy initialization 的技术，这样就只有需要的时候才会实例化，而不会受其他因素而触发实例化。
```
public class Singleton {
    private Singleton(){
        System.out.println("Singleton is instantiated");
    }
    private static class SingletonHolder{
        private static Singleton instance = new Singleton();
    }
    public static Singleton getInstance() {
        return SingletonHolder.instance;
    }
    public static void doSomething(){
        System.out.println("do something");
    }
}
```
这里使用到的是`Initialization-on-demand holder idiom` 这种技术，参看[Initialization-on-demand holder idiom](https://en.wikipedia.org/wiki/Initialization-on-demand_holder_idiom)

如果需要lazy initialization 的域是**非静态**的，也就是实例域的话可以使用`double-check locking` 这种技术，但是这种技术需要给实例域加上 `volatile` 这个修饰符，以避免不可见的问题。
```
public class Singleton {
    private volatile Singleton instance;
    private Singleton(){};
    public Singleton getInstance() {
        if(instance == null){  // A
            synchronized (this){
                if(instance == null){ // double check
                    return new Singleton(); // B
                }
            }
        }
        return instance;
    }
}
```
`volatile` 这里的作用是避免：当thread1 在B 步骤创建Singleton 还没完成时，thread2  在A 步骤却已经看到instance 非null 了，然后返回了一个没有创建完毕的对象，然后调用时出错。

**结论:**
如果没有必要延时初始化，就用eager initialization 的方法实现单例就好。
