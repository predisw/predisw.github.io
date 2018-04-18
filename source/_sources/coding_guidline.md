# coding guideline 

### Part one -- code format style
> Test enviroment is IntelliJ IDEA 17.3

Use `google code style` to unify coding style.Check the google code style project from https://github.com/google/styleguide
For idea we can import `intellij-java-google-style.xml`
For eclipse need to use `eclipse-java-google-style.xml` 

Can try plugin `eclipse code formatter` if want to use the `eclipse-java-google-style.xml` in idea. But after testing , the effect using `eclipse-java-google-style.xml`  in `eclipse code formatter` is different with using  `intellij-java-google-style.xml` directly in idea.

So just suggest to use by each in different IDE.

But before we start to use the `intellij-java-google-style.xml`, we need to change some settings to comply with our custom.

- `indent = 2` in default to `indent = 4`  in custom
- `tab = 2` in default to `tab = 4`  in custom
- `line length = 100` in default to `line length = 120`  in custom

Import the `intellij-java-google-style.xml` by settings -> Editor -> Code Style -> Java -> Scheme.
After that we can use Ctrl + Alt + L to format the code



### Part two -- coding guideline

Install plugin -- alibaba java coding guidelines
The plugin will detect the breaking rule codes automatically.
But the flaw is that it can only work on maven source codes but not the test.

And the rules the plugin will comply with can disable/enable by settings -> Editor -> Inspections -> Ali-Check.

The more details about rules/guidelines described in document can refer to  https://github.com/alibaba/p3c.
Here below are some of the rules/guidelines in chinese:


### 编程规约

【强制】创建线程或线程池时请指定有意义的线程名称，方便出错时回溯

【推荐】线程资源必须通过线程池提供，不允许在应用中自行显式创建线程。

【推荐】线程池不允许使用 Executors 去创建，而是通过ThreadPoolExecutor的方去创建 ,因为这样可以更加明白线程池的工作方式，设置线程名，和避免资源耗尽问题。如线程缓存队列允许的请求队列长度为 Integer.MAX_VALUE，可能会堆积大量的请求，从而导致 OOM 。

【强制】SimpleDateFormat 是线程不安全的类，一般不要定义为static变量，如果定义为static，必须加锁。
亦推荐如下处理:
```java
private static final ThreadLocal<DateFormat> df = new ThreadLocal<DateFormat>() {
    @Override
    protected DateFormat initialValue() {
        return new SimpleDateFormat("yyyy-MM-dd");
    }
};
```
说明：如果是JDK8的应用，可以使用Instant代替Date，LocalDateTime代替Calendar，DateTimeFormatter代替SimpleDateFormat，官方给出的解释：simple beautiful strong immutable thread-safe。


【说明】子线程抛出异常堆栈，不能在主线程 try-catch 到

【推荐】避免 Random 实例被多线程使用，虽然共享该实例是线程安全的，但会因竞争同一seed 导致的性能下降。
说明： Random 实例包括 java.util.Random 的实例或者 Math.random()的方式。
正例： 在 JDK7 之后，可以直接使用 API ThreadLocalRandom， 而在 JDK7 之前， 需要编码保证每个线程持有一个实例

【推荐】表达异常的分支时，少用if-else方式，这种方式可以改写成：
```java
if (condition) {
    ...
    return obj;
}
// 接着写else的业务逻辑代码;
```
说明：如果非得使用if()...else if()...else...方式表达逻辑，【强制】避免后续代码维护困难，请勿超过3层。
正例：超过3层的 if-else 的逻辑判断代码可以使用卫语句、策略模式、状态模式等来实现，其中卫语句示例如下：
```java
public void today() {
    if (isBusy()) {
        System.out.println(“change time.”);
        return;
    }

    if (isFree()) {
        System.out.println(“go to travel.”);
        return;
    }

    System.out.println(“stay at home to learn Alibaba Java Coding Guidelines.”);
    return;
}
```

【强制】类、类属性、类方法的注释必须使用Javadoc规范，使用/**内容*/格式，不得使用// xxx方式。 
    说明：在IDE编辑窗口中，Javadoc方式会提示相关注释，生成Javadoc可以正确输出相应注释；在IDE中，工程调用方法时，不进入方法即可悬浮提示方法、参数、返回值的意义，提高阅读效率。

【强制】所有的抽象方法（包括接口中的方法）必须要用Javadoc注释、除了返回值、参数、异常说明外，还必须指出该方法做什么事情，实现什么功能。     说明：对子类的实现要求，或者调用注意事项，请一并说明。

【参考】对于注释的要求：第一、能够准确反应设计思想和代码逻辑；第二、能够描述业务含义，使别的程序员能够迅速了解到代码背后的信息。完全没有注释的大段代码对于阅读者形同天书，注释是给自己看的，即使隔很长时间，也能清晰理解当时的思路；注释也是给继任者看的，使其能够快速接替自己的工作。

【强制】捕获异常是为了处理它，不要捕获了却什么都不处理而抛弃之，如果不想处理它，请将该异常抛给它的调用者。最外层的业务使用者，必须处理异常，将其转化为用户可以理解的内容。
    说明：例如输入参数错误，这种是无法处理的，将其抛出；如连接超时异常，可以尝试重新发送。

【强制】不要在 finally块中使用 return。 
说明： finally块中的 return返回后方法结束执行，不会再执行try块中的 return语句。

【参考】对于公司外的http/api开放接口必须使用“错误码”；而应用内部推荐异常抛出；跨应用间RPC调用优先考虑使用Result方式，封装isSuccess()方法、“错误码”、“错误简短信息”。 
    说明：关于RPC方法返回方式使用Result方式的理由：
    - 使用抛异常返回方式，调用方如果没有捕获到就会产生运行时错误。 
    - 如果不加栈信息，只是new自定义异常，加入自己的理解的error message，对于调用端解决问题的帮助不会太多。如果加了栈信息，在频繁调用出错的情况下，数据序列化和传输的性能损耗也是问题。

### 日志规约

【强制】对trace/debug/info级别的日志输出，必须使用条件输出形式或者使用占位符的方式。
    说明：logger.debug("Processing trade with id: " + id + " and symbol: " + symbol); 如果日志级别是warn，上述日志不会打印，但是会执行字符串拼接操作，如果symbol是对象，会执行toString()方法，浪费了系统资源，执行了上述操作，最终日志却没有打印。 

    正例：（条件）
    if (logger.isDebugEnabled()) {
        logger.debug("Processing trade with id: " + id + " and symbol: " + symbol);
    }
    正例：（占位符）
    logger.debug("Processing trade with id: {} and symbol : {} ", id, symbol);


【推荐】谨慎地记录日志。生产环境禁止输出debug日志；有选择地输出info日志；一定要注意日志输出量的问题，避免把服务器磁盘撑爆，并记得及时删除这些观察日志。 
    说明：大量地输出无效日志，不利于系统性能提升，也不利于快速定位错误点。记录日志时请思考：这些日志真的有人看吗？看到这条日志你能做什么？能不能给问题排查带来好处？

### 单元测试

【推荐】编写单元测试代码遵守BCDE原则，以保证被测试模块的交付质量。
B：Border，边界值测试，包括循环、 特殊取，边界值测试包括循环、 特殊取特殊时间点、数据顺序等。 C：Correct，正确的输入，并得到预期结果。 ，正确的输入并得到预期结果。
D：Design，与设计文档相结合，来编写单元测试。 ，与设计文档相结合来编写单元测试。 E：Error，强制错误信息输入（如：非法数据、异常流程业务允许等），并得到预期结果。
