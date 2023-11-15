# %%
import requests
import json
# %%
"""
Simple retrieval from elastic search database.
"""

def safe_post_request(url, params):
    for _ in range(10):
        try:
            return requests.post(url, json=params, headers={'Connection':'close'})
            # return requests.post(url, json=params)
        except:
            print("Post request didn't succeed. Will wait 20s and retry.")
            time.sleep(20)
    raise Exception("Post request couldn't succeed after several attempts.")

# %%
# Define the Elasticsearch endpoint
url = "http://localhost:9200/hotpotqa/_search"
keyword = "Which is farther west, Sheridan County, Montana or Chandra Taal?"
# keyword = "Do Tropical Fish Hobbyist and Curve cover the same topic?"
# keyword = "Between Aspidistra and Cyrtanthus, which genus of plant belongs to the Subfamily Amaryllidoideae?"

# Define the query
query = {
    "query": {
        "match": {
            "paragraph_text": keyword
        }
    }
}
print("Query: ", query["query"]["match"]["paragraph_text"])


# # Set the Elasticsearch query
# query = {
#     "query": {
#         "bool": {
#             "must": {
#                 "match": {
#                     "content": keyword
#                 }
#             },
#             "filter": {
#                 "range": {
#                     "relevance": {
#                         "gte": relevance_threshold
#                     }
#                 }
#             }
#         }
#     },
#     "size": 10
# }


# Send the request
response = requests.post(url, json=query)

# Parse the response to JSON
data = response.json()

# Print the response and the relevance score for each paragraph
results = data["hits"]["hits"]
max_score = results[0]["_score"]
min_score = results[0]["_score"]
max_text = results[0]["_source"]["paragraph_text"]
min_text = results[0]["_source"]["paragraph_text"]

for result in results:
    # print(result["_source"]["paragraph_text"])
    # print(result["_score"], "\n")
    if result["_score"] > max_score:
        max_score = result["_score"]
        max_text = result["_source"]["paragraph_text"]

    if result["_score"] < min_score:
        min_score = result["_score"]
        min_text = result["_source"]["paragraph_text"]

print("Max score: ", max_score)
print("Min score: ", min_score)
print("Max text: ", max_text)
print("Min text: ", min_text)
print("Number of results: ", len(results))

# %%
"""
Print indices information
"""

# url = "http://localhost:9200/_cat/indices?v" # print information about all indices
url = "http://localhost:9200/hotpotqa/_mapping" # print mapping for hotpotqa index

response = requests.get(url)

# Check if the response is not empty and is in JSON format
if response.text:
    try:
        # Print the response with indent
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print("Invalid JSON")



# %%
""" 
Print shards information of hotpotqa index 
"""

url = "http://localhost:9200/_cat/shards/hotpotqa?v" # print information about shards for hotpotqa index

# Send the GET request
response = requests.get(url)

# Check if the response is not empty and is in JSON format
if response.text:
    try:
        # Print the response with indent
        print(response.text)
    except ValueError:
        print("Invalid JSON")
else:
    print("Empty Response")

# %%
"""
Generate the mapping question_id -> question_text for the dev set of HotpotQA
1. Collect all keys from ircot_exp2/ircot/predictions/oner_hotpotqa_similarity_90____prompt_set_1___bm25_retrieval_count__15/prediction__hotpotqa_to_hotpotqa__dev_subsampled.json as question_ids
2. Generate their corresponding question texts according to ircot_exp2/ircot/processed_data/hotpotqa/dev_subsampled.jsonl
"""
# Step 1: Extract question_ids from prediction__hotpotqa_to_hotpotqa__dev_subsampled.json
with open("predictions/oner_hotpotqa_similarity_90____prompt_set_1___bm25_retrieval_count__15/prediction__hotpotqa_to_hotpotqa__dev_subsampled.json") as f:
    data = json.load(f)
    question_ids = list(data.keys())

# Step 2: Extract corresponding question text for each question_id
questions = {}
with open("processed_data/hotpotqa/dev_subsampled.jsonl") as f:
    for line in f:
        data = json.loads(line)
        questions[data["question_id"]] = data["question_text"]

# Step 3: Save this mapping to a file in 
with open("processed_data/hotpotqa/question_id_to_text_mapping.json", "w") as f:
    json.dump(questions, f, indent=4)

print(f"Saved {len(questions)} question_id -> question_text mappings to processed_data/hotpotqa/question_id_to_text_mapping.json")

# %%
"""
A function to map a question_id to the real text of the question
"""

def map_question_id_to_text(question_id):
    with open("processed_data/hotpotqa/question_id_to_text_mapping.json") as f:
        data = json.load(f)
        return data[question_id]

# %%
"""
Test the function
"""

# read question text of id 5ae28c0a554299495565daaa
print(map_question_id_to_text("5ae28c0a554299495565daaa"))

# %%
