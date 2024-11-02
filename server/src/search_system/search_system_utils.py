import torch
import torch.nn.functional as F

from server.src.books.books_models import Book
from server.src.ml_connect import tokenizer,model

def get_mean_embedings(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)

    last_hidden_states = outputs.last_hidden_state

    mean_embedding = torch.mean(last_hidden_states, dim=1)
    return mean_embedding

def find_most_similar(texts:list[str], candidate_texts:list[Book]):
    if texts:
        embeddings = [get_mean_embedings(text) for text in texts]

        average_embedding = torch.mean(torch.stack(embeddings), dim=0)

        similarities = []
        for candidate in candidate_texts:
            sum_rating = 0 
            if len(candidate.ratings)>0:
                for i2 in candidate.ratings: 
                    sum_rating += i2.rating
                rate = sum_rating/len(candidate.ratings)
            else:
                rate = 0
            
            book = {"id":candidate.id,
                    "title":candidate.title,
                    "author":candidate.author,
                    "desc":candidate.desc,
                    "writen_date":candidate.writen_date,
                    "age_of_book":candidate.age_of_book,
                    "similarity":1,
                    "ganres":[i.ganre for i in candidate.ganres],
                    "ratings":rate}
            candidate_embedding = get_mean_embedings(candidate.zip_text)
            similarity = F.cosine_similarity(average_embedding, candidate_embedding)
            if similarity.item() > 0.7:
                book["similarity"] = similarity.item()
                similarities.append(book)


        # most_similar_index = similarities.index(max(similarities))
        return similarities
    texts= []
    for candidate in candidate_texts:
        sum_rating = 0 
        if len(candidate.ratings)>0:
            for i2 in candidate.ratings: 
                sum_rating += i2.rating
            rate = sum_rating/len(candidate.ratings)
        else:
            rate = 0
        book = {"id":candidate.id,
                    "title":candidate.title,
                    "author":candidate.author,
                    "desc":candidate.desc,
                    "writen_date":candidate.writen_date,
                    "age_of_book":candidate.age_of_book,
                    "similarity":1,
                    "ganres":[i.ganre for i in candidate.ganres],
                    "ratings":rate}
        texts.append(book)

    return texts