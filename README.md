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
