---
title: AOP-learning
date: 2018-03-25 20:14:09
categories:
- coding
tags:
- java
- aop

---

## Limitations of Spring Aop:

* it can only be applied to beans that are managed by a Spring container.
* Can not advise static methods
* Can only advise non-private methods
* Can only apply aspects to Spring Beans
* When using Spring Aop , suppose method a() calls method b() on the same class/interface, advice will never be executed for method b()

### Because of:

Spring AOP is a proxy-based AOP framework. This means that to implement aspects to the target objects, it’ll create proxies of that object. This is achieved using either of two ways:

1. JDK dynamic proxy – the preferred way for Spring AOP. Whenever the targeted object implements even one interface, then JDK dynamic proxy will be used
2. CGLIB proxy – if the target object doesn’t implement an interface, then CGLIB proxy can be used

We cannot apply cross-cutting concerns (or aspects) across classes that are “final” because they cannot be overridden and thus it would result in a runtime exception. 
The same applies for static and final methods. Spring aspects cannot be applied to them because they cannot be overridden. 

spring aop isn't applied to the method called within the same class.That’s obviously because when we call a method within the same class, then we aren’t calling the method of the proxy that Spring AOP supplies.
<!--more-->
## What are the supported AspectJ pointcut designators in Spring AOP?

Execution
This
Target
Args
@target
@args
@within
@annotation


### example:

```java
@Component
@Aspect
public class TxLogAspect {

    @Pointcut("execution(public * com.ericsson.sep.scef.common.http.HttpHelper.*(..))")
    public void pointCutEnable(){}

    @AfterThrowing(pointcut = "pointCutEnable() && @annotation(txLog)",throwing = "ex")
    public void handleAfterThrowException(JoinPoint jp, Exception ex, TxLog txLog){
        ......
    }

    @Pointcut("execution (* com.ericsson.sep.scef.monitor..*(..))")
    public void publicEndPointMethod() {
        //pointcut
    }

    @AfterReturning(value = "publicEndPointMethod() && @annotation(uplinkLog)",returning = "results")
    public void afterEndPointReturn(UplinkLog uplinkLog,Map<Long, MonitorEventReportResult> results) {
        ......
    }
}

```


### AspectJ:

AspectJ is the original AOP technology which aims to provide complete AOP solution. It is more robust but also significantly more complicated than Spring AOP. It’s also worth noting that AspectJ can be applied across all domain objects.
However, to use AspectJ, we’re required to introduce the AspectJ compiler (ajc) and re-package all our libraries (unless we switch to post-compile or load-time weaving).

[Comparing Spring AOP and AspectJ](http://www.baeldung.com/spring-aop-vs-aspectj)
