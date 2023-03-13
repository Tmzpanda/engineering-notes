```sql
CREATE TABLE page_view(viewTime INT, userid BIGINT, page_url STRING, referrer_url STRING, ip STRING COMMENT 'IP Address of the User')   -- 表类型，字段类型
PARTITIONED BY (dt STRING, country STRING)   -- 分区
CLUSTERED BY(userid) SORTED BY(viewTime) INTO 32 BUCKETS   -- 分桶
STORED AS SEQUENCEFILE;  -- 文件格式

```