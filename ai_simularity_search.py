import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from database import get_all_events_description_and_message_id

async def init_model():
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')
    model = BertModel.from_pretrained('bert-large-uncased')
    return model, tokenizer


async def generate_embedding(text: str, model, tokenizer):
    encodedInput = tokenizer(text, return_tensors='pt')
    
    with torch.no_grad():
        output = model(**encodedInput)
    
    outputEmbeddings = torch.mean(output.last_hidden_state, dim=1)

    return outputEmbeddings


def get_simularity_score(query: str, eventDescription: str, model, tokenizer):
    embQ = generate_embedding(query, model, tokenizer)
    embD = generate_embedding(eventDescription, model, tokenizer)

    simularityScore = cosine_similarity(embQ, embD)

    return simularityScore[0][0]
    

def get_all_events_simularity_score(query: str, model, tokenizer):
    allEvents = get_all_events_description_and_message_id()

    eventScores = []
    for event in allEvents:
        score = get_simularity_score("query", event[0], model, tokenizer)
        eventScores.append((event, score))

    return eventScores


def sort_events_by_simularity(query: str, model, tokenizer):
    eventScores = get_all_events_simularity_score(query, model, tokenizer)
    eventScores.sort(key=lambda x: x[1], reverse=True)

    return eventScores
