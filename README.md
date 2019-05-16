# elasticsearch_deduplicator
Python script aggregates duplicate docs in an index and removes all except the first one


```
PUT your_index_name/_settings
{
  "max_inner_result_window" : 1000 
}
```

```
PUT _template/default
{
  "index_patterns": ["*"],
  "order": -1,
  "settings": {
    "number_of_shards": "6",
    "number_of_replicas": "1"
  }
}
```
```
GET _cat/indices?pretty&v&s=index

GET /_cat/indices?v&s=store.size:desc

GET signal_v6/_search
{
  "size": 0,
  "aggs": {
    "duplicateCount": {
      "terms": {
        "field": "created",
        "min_doc_count": 2,
        "size": 10
      },
      "aggs": {
        "duplicateDocuments": {
          "top_hits": {
            "size": 10
          }}
    }
  }
}
}

POST /signal_v6/_forcemerge?only_expunge_deletes=true

PUT signal_v5/_settings
{
  "max_inner_result_window" : 1000 
}

POST _reindex
{
  "conflicts": "proceed",
  "source": {
    "index": ["restored_backup_signal_6", "restored_crypto_signal_v6"]
  },
  "dest": {
    "index": "signal_v6",
    "op_type": "create"
  }
}

PUT atest

PUT signal_v14/_settings
{
  "index.mapping.total_fields.limit": 2000
}

POST signal_v5/_delete_by_query
{
  "query": { 
    "match": {
      "created": "2019-05-14T18:05:16.694Z"
    }
  }
}

GET _tasks


GET _tasks?actions=*byquery&detailed

GET /_snapshot/
GET /_snapshot/_all
GET /_snapshot/snapshot-repository/snapshot_5/_status

GET /_snapshot/snapshot-repository/_current

PUT _template/default
{
  "index_patterns": ["*"],
  "order": -1,
  "settings": {
    "number_of_shards": "2",
    "number_of_replicas": "0"
  }
}
```
