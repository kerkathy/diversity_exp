# %%
import json
    
def generate_mapping_file(source_file_path, mapping_file_path):
    """
    Get the question text from a question_id
    """
    questions = {}
    with open(source_file_path) as f:
        assert source_file_path.endswith(".jsonl"), "source_file_path must be a jsonl file"
        for line in f:
            data = json.loads(line)
            questions[data["question_id"]] = data["question_text"]
    
    with open(mapping_file_path, "w") as f:
        json.dump(questions, f, indent=4)

    print(f"Saved mapping to {mapping_file_path}")

    
def collect_predictions(prediction_file_path):
    """
    Collect dict of {question_id: [{"title": title, "paragraph_text": paragraph_text}, ...], ...}
    """
    with open(prediction_file_path) as f:
        predictions = json.load(f)
        return predictions

def map_question_ids_to_text(question_ids, mapping_file_path):
    """
    Map question_ids to question texts
    """
    question_id_to_text = {}
    # read mapping_file_path if its json file
    assert os.path.exists(mapping_file_path), "mapping_file_path does not exist"
    assert mapping_file_path.endswith(".json"), "mapping_file_path must be a json or jsonl file"
    with open(mapping_file_path) as f:
        question_id_to_text = json.load(f)

    question_texts = [question_id_to_text[question_id] for question_id in question_ids]
    # for question_id in question_ids:
    #     question_texts.append(question_id_to_text[question_id])
    
    return question_texts

# %%
"""
Test the function
"""

# read question text of id 5ae28c0a554299495565daaa

split = "test_subsampled"
source_file_path = f"../processed_data/hotpotqa/{split}.jsonl"
mapping_file_path = source_file_path.replace(".jsonl", "_mapping.json")
prediction_file_path = f"../predictions_archived/oner/count50/oner_hotpotqa_similarity_20____oner____hotpotqa_to_hotpotqa__best/prediction__hotpotqa_to_hotpotqa__{split}.json"

generate_mapping_file(source_file_path, mapping_file_path)
predictions = collect_predictions(prediction_file_path)
question_ids = list(predictions.keys())

# question_ids = collect_predictions(f"../predictions_archived/oner/count50/oner_hotpotqa_similarity_20____oner____hotpotqa_to_hotpotqa__best/prediction__hotpotqa_to_hotpotqa__test_subsampled.json")
# question_ids = collect_predictions(f"../predictions/oner_hotpotqa_similarity_90____prompt_set_1___bm25_retrieval_count__15/prediction__hotpotqa_to_hotpotqa__{split}_subsampled.json")
question_texts = map_question_ids_to_text(question_ids, mapping_file_path)

print(len(question_texts))
print(len(question_ids))
print(question_texts[0])
# %%
