from elasticsearch import Elasticsearch

host = "127.0.0.1"
port = 9200
timeout = 1000
index = "index"
doc_type = "type"
size = 1000

es = Elasticsearch(
    [
        {
            'host': host,
            'port': port
        }
    ],
    timeout=timeout
)

# terms_size and top_hits_size can be up to 100; higher values lead to Read timed out exception
# index.max_inner_result_window should be changed to increase size of top_hits_size, otherwise 100 is max for top_hits_size
# if 100 for terms_size and top_hits_size fails, try to decrease number a bit (e.g. 99 for both can work, depends on your server)
def get_docs(index, doc_type, terms_size, top_hits_size):
  result = es.search(
    index=index, 
    doc_type=doc_type, 
    body={
    "size": 0,
    "aggs": {
      "duplicateCount": {
        "terms": {
          "field": "created",
          "min_doc_count": 2,
          "size": terms_size
        },
        "aggs": {
          "duplicateDocuments": {
            "top_hits": {
              "size": top_hits_size
            }}
          }
        }
      }
     }
   )['aggregations']['duplicateCount']['buckets']
  return result
  
def delete_duplicates(index, doc_type, result):
  for res in result:
    keys = res['duplicateDocuments']['hits']['hits']
    
    for key_id in keys[1:]: # [1:] <- first one is skipped, so it will be kept
        print(es.delete(index=index, doc_type=doc_type, id=key_id['_id']))
        
def mp_delete_duplicates(index, doc_type, keys):
    for key_id in keys[1:]: # [1:] <- first one is skipped, so it will be kept
        try:
            print(es.delete(index=index, doc_type=doc_type, id=key_id['_id']))
        except Exception as e:
            print(e)
        
def main():
    documents = get_docs()
    jobs = []
    for docs in documents:
        keys = docs['duplicateDocuments']['hits']['hits']
        proc = Process(target=mp_delete_duplicates, args=('signal_v5', 'info', keys), daemon=True)
        jobs.append(proc)
    for j in jobs:
        j.start()
    
        

