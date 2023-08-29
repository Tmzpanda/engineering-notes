-- DDL
CREATE TABLE page_view(viewTime INT, userid BIGINT, page_url STRING, referrer_url STRING, ip STRING COMMENT 'IP Address of the User') 
PARTITIONED BY (dt STRING, country STRING)   -- partition
CLUSTERED BY(userid) SORTED BY(viewTime) INTO 32 BUCKETS   -- bucket
STORED AS SEQUENCEFILE;  -- format

