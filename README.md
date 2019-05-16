# elasticsearch_deduplicator
Python script aggregates duplicate docs in an index and removes all except the first one


```
PUT your_index_name/_settings
{
  "max_result_window" : 1000 
}
```
