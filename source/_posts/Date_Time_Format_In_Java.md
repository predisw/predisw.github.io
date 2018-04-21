---
title: Date_Time_Format_In_Java
date: 2018-04-21 11:10:03
categories:
- coding
tags:
- java
---
### Date Time Format in Java

Before Java8 we always use SimpleDateFormat to format Datetime. What we should take caution is :

1. Never use this kind of object as static
2. the String Pattern of SimpleDateFormat adapts to Least Match Principle ,it means:
```java
    @Test
    public void SimpleDateFormatT() throws ParseException {
        SimpleDateFormat sd = new SimpleDateFormat();
        //sd.applyPattern("yyyy-MM-DD HH:mm:ss X"); // can not parse the string without timeZone info

        sd.applyPattern("yyyy-MM-DD HH:mm:ss");  // can parse the string with timeZone info

        String timeStr_noTZ = "2018-09-01 23:32:10";
        String timeStr_TZ07 = "2018-09-01 23:32:10 +07:00";
        String timeStr_TZ09 = "2018-09-01 23:32:10 +09:00";

        Date time_noTZ = sd.parse(timeStr_noTZ); 
        Date time_TZ07 = sd.parse(timeStr_TZ07); // it doesn't throw exception ,but it ignore the timezone info 
        Date time_TZ09 = sd.parse(timeStr_TZ09); // as the string pattern doesn't specify the timezone required.

        Assert.assertTrue(time_noTZ.compareTo(time_TZ07) == 0);
        Assert.assertTrue(time_TZ07.equals(time_TZ09));

        System.out.println(time_noTZ);
        System.out.println(time_TZ07);
        System.out.println(time_TZ09);
    }
```

3. the object of `java.util.Date` is a time value from `1970-01-01 00:00:00 +00:00`,the unit of value is millisecond.So it is a timezone-non-related value which any timezone datetime can translate into `java.unit.Date` kind of Object and compare.
Below is the explanation of the `java.util.Date`  constructor from JDK.

> public Date(long date)
> 
> Allocates a Date object and initializes it to represent the specified number of milliseconds since the standard base time known as "the epoch", namely January 1, 1970, 00:00:00 GMT.


Now let us start to travel around the java8's dateTime world.

the design thought of java8 time api

learn by referring to https://zhuanlan.zhihu.com/p/28133858


`LocalDateTime`
This class does not store or represent a time-zone. Instead, it is a description of the date, as used for birthdays, combined with the local time as seen on a wall clock. It cannot represent an instant on the time-line without additional information such as an offset or time-zone.

** example to format datetime **
```java
public class DataTimeConverter {

    public static String dateFormatConverter(long dateLong) {
        OffsetDateTime duration = OffsetDateTime.ofInstant(Instant.ofEpochMilli(dateLong), ZoneId.systemDefault());
        return duration.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
    }

    public static long getDateTime(String dateString) throws Exception {
        OffsetDateTime duration = OffsetDateTime.parse(dateString, DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        return duration.toInstant().toEpochMilli();
    }
}

```
