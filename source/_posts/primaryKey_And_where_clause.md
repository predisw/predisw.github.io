---
title: primaryKey_And_where_clause
date: 2018-06-08 18:26:11
categories:
- db
tags:
- cassandra
---
primary key And Where clause

### primary key And partition key

primary key consist of partition key which is the first component and clustering key which is the other components of primary key.

`partition key`  ：由一个或多个column 组成，决定partition

`clustering key` (clustering columns): 由一个或多个column 组成，决定数据在partition 内的排序，默认按照字母表排序 


The first component of a table's primary key is the partition key; within a partition, rows are clustered by the remaining columns of the key. Other columns can be indexed separately from the primary key. 
Clustering is a storage engine process that sorts data within each partition based on the definition of the clustering columns. 

Cassandra stores an entire row of data on a node by partition key and can order the data for retrieval with clustering columns.

** Keep in mind that only the primary key can be specified when retrieving data from the table. **

** Data is retrieved using the partition key. Keep in mind that to retrieve data from the table, values for all columns defined in the partition key have to be supplied.**

The table shown uses race_year and race_name in the primary key, as a composition partition key. To retrieve data, both parameters must be identified.
```
cqlsh> CREATE TABLE cycling.rank_by_year_and_name ( 
  race_year int, 
  race_name text, 
  cyclist_name text, 
  rank int, 
  PRIMARY KEY ((race_year, race_name), rank) 
);
```

Both `race_year` and `race_name`  comprise the partition key.
rank is the clustering key

```
cqlsh> SELECT * FROM cycling.rank_by_year_and_name WHERE race_year=2015;
```

上面这句执行会报错，因为条件语句只使用了部分 partition key.
但如果给race_year 创建索引，就可以正确查询。
```
cqlsh> CREATE INDEX ryear ON cycling.rank_by_year_and_name (race_year);
SELECT * FROM cycling.rank_by_year_and_name WHERE race_year=2015;
```

clustering key 也可以创建索引
```
cqlsh> CREATE INDEX rrank ON cycling.rank_by_year_and_name (rank);
SELECT * FROM cycling.rank_by_year_and_name WHERE rank = 1;

```


** Both partition key and clustering key can be indexed. **


### Why have to add primary key in where clause ?

这个和cassandra 的存储数据的实现机制有关。
当插入一条数据的时候，Partitioner 先根据 partition key 的hash code 给它分配parttion（就是哪个virtual node，或者哪一段token），然后再根据这条数据的 clustering columns 的值给它在partition 内排序。这样就决定了这条数据存储的位置。

当使用select 语句去定位一条数据的时候， 就必须先指定这条数据的partition key 去确定这条数据是在哪个partition。所以在select 语句中，partition key 条件必须要用 等号（=）来确定。然后clustering columns 部分可以使用 =，>,< 的比较符号进行比较，或者使用order by 进去排序。

如果在select 语句中不使用partition key ，只用 clustering clounms 来做条件查询，那么就会报如下的错：
```
create table if not exists test.monitor_event_group(
	globalId        uuid,
	currentTime     timestamp,
	zoneId          int,
	groupId         varchar,
	data            text,
	PRIMARY KEY (globalId, currentTime)
)

scef@cqlsh:test>  SELECT *  from test.monitor_event_group where currentTime > '2018-06-08 05:40:00.000 +0000' and currentTime< '2018-06-08 05:42:00.000 +0000';

InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"

```

就是必须使用 ALLOW FILTERING.

`ALLOW FILTERING ` 的意思是指 允许cassandra 扫描所有partition 去过滤出符合条件的数据，这样当然会非常没有效率和高延迟。

另外一个解决方法 是给 currentTime 这个column 创建index。This is due to the fact that Cassandra can use the secondary index on the currentTime column to find the matching rows and does not need to perform any filtering.


References:

[Partition keys](https://docs.datastax.com/en/dse/6.0/cql/cql/cql_using/wherePK.html)
[ALLOW FILTERING explained](https://www.datastax.com/dev/blog/allow-filtering-explained-2)

