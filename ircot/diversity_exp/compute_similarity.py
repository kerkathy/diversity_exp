# %%
from sentence_transformers import SentenceTransformer, util
import torch
import os
import json
from question_mapping import collect_predictions, map_question_ids_to_text

def build_embedding(question_ids=[], questions_texts=[], model_name='multi-qa-MiniLM-L6-cos-v1', output_pt_file='embeddings.pt'):
    """
    Build the embedding for the questions
    """
    model = SentenceTransformer(model_name)

    # Compute embedding for both lists, so that we can later 
    embeddings = model.encode(questions_texts, convert_to_tensor=True)
    # save embeddings with corresponding question_ids
    if os.path.exists(os.path.dirname(output_pt_file)):
        print(f"Overwriting {output_pt_file}")
    torch.save(dict(zip(question_ids, embeddings)), output_pt_file)

def load_embedding(output_pt_file='embeddings.pt'):
    """
    Load the embedding for the questions
    """
    embeddings = torch.load(output_pt_file)
    return embeddings

def get_question_embedding(question_id, embeddings):
    """
    Get the embedding for the question
    """
    return embeddings[question_id]

def on_the_fly_embedding(text, model_name='multi-qa-MiniLM-L6-cos-v1') -> torch.Tensor:
    """
    Get the embedding for the text
    """
    model = SentenceTransformer(model_name)
    return model.encode(text, convert_to_tensor=True)

def get_similarity_score(question_id, texts, question_embeddings) -> torch.Tensor:
    """
    Get the similarity score of each text to the question
    """
    query_embedding = question_embeddings[question_id]
    passage_embedding = on_the_fly_embedding(texts)
    cos_scores = util.cos_sim(query_embedding, passage_embedding)[0]
    return cos_scores


# %%
# Collect questions
similarities = [30, 50, 70, 90, 99]
split = "dev_subsampled"
for similarity in similarities:
    prediction_file = f"../predictions/oner_hotpotqa_similarity_{similarity}____prompt_set_1___bm25_retrieval_count__15/prediction__hotpotqa_to_hotpotqa__dev_subsampled.json"
    mapping_file = "../processed_data/hotpotqa/dev_subsampled_mapping.json"
    predictions = collect_predictions(prediction_file)
    question_ids = list(predictions.keys())
    question_texts = map_question_ids_to_text(question_ids, mapping_file)

    # Build the embedding (only need to run once)
    # build_embedding(question_ids, question_texts, output_pt_file='embeddings.pt')

    # Load the embedding
    question_embeddings = load_embedding(output_pt_file='embeddings.pt')
    # print(get_question_embedding(question_ids[0], question_embeddings))

    # For each prediction, compute the similarity score of each paragraph_text to the question
    similarity_file_name = prediction_file.replace(".json", "_similarity.json")

    for question_id, prediction in predictions.items():
        # TODO: modify into [title, paragraph_text]
        texts = [item["paragraph_text"] for item in prediction]
        cos_scores = get_similarity_score(question_id, texts, question_embeddings)
        for i, item in enumerate(prediction):
            item["similarity_score"] = cos_scores[i].item()

    with open(similarity_file_name, "w") as f:
        json.dump(predictions, f, indent=4)

    print(f"Saved similarity scores to {similarity_file_name}")

# %%

# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# query_embedding = model.encode('How many people live in London?')

# #The passages are encoded as [ [title1, text1], [title2, text2], ...]
# passage_embedding = model.encode([['London', 'London has 9,787,426 inhabitants at the 2011 census.'], ['Paris', 'Paris has 2,140,526 inhabitants in 2019.']])

# print("Similarity:", util.cos_sim(query_embedding, passage_embedding))

# %%
# %%
