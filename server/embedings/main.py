# # from transformers import AutoTokenizer, AutoModel
# # import torch

# # # Загрузка предобученной модели и токенизатора
# # model_name = "DeepPavlov/rubert-base-cased"
# # tokenizer = AutoTokenizer.from_pretrained(model_name)
# # model = AutoModel.from_pretrained(model_name)

# # # Пример текста для токенизации
# # text = "Молодой ученый отправился в таинственный лес, чтобы исследовать легенды о магическом существе по имени Леший, и стал его учеником, погрузившись в мир магии и науки."
# # text2 = "Молодой ученый, увлеченный мифами, отправился в лес, где стал учеником Лешего, изучая науку и магию для глубокого понимания мира."
# # text3 = "Однажды ночью молодой астроном, увлеченный поисками внеземной жизни, вышел в открытое поле и установил свой телескоп. Он смотрел в космос, пытаясь найти признаки разумной цивилизации среди звездных скоплений. Внезапно, на грани видимости, он заметил странное свечение, которое двигалось к нему. По мере приближения свет начал приобретать форму, и перед ним появился маленький зеленый инопланетянин. Инопланетянин представился как Глитч и сказал, что прибыл с далекой планеты, чтобы предложить астроному стать его учеником. С этого момента жизнь молодого человека наполнилась космическими приключениями и новыми знаниями о Вселенной."
# # text4 = ";dflksfdfdfsdfsfd"
# # def get_cls_embedings(text:str):
# #     inputs = tokenizer(text, return_tensors="pt")

# #     with torch.no_grad():
# #         outputs = model(**inputs)

# #     last_hidden_states = outputs.last_hidden_state

# #     cls_embedding = last_hidden_states[:, 0, :]
# #     return cls_embedding
# # def sin_similarity(a_embadings,b_embadings):
# #     tops = 0

# #     downa = 0
# #     downb = 0

# #     for a,b in zip(a_embadings,b_embadings):
# #         a = a.item()
# #         b = b.item()
# #         tops += a*b
        
# #         downa += a*a
# #         downb += b*b

# #     down = downa**0.5 + downb**0.5


# #     return (tops/down)

# # a_embadings = get_cls_embedings(text=text)[0]
# # b_embadings = get_cls_embedings(text=text2)[0]
# # b2_embadings = get_cls_embedings(text=text3)[0]
# # b3_em = get_cls_embedings(text4)[0]

# # print(sin_similarity(a_embadings,b_embadings))
# # print(sin_similarity(a_embadings,b2_embadings))
# # print(sin_similarity(a_embadings,b3_em))



# ______________for one text____________________________


# from transformers import AutoTokenizer, AutoModel
# import torch
# import torch.nn.functional as F  

# model_name = "DeepPavlov/rubert-base-cased"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# def get_cls_embedings(text: str):
#     inputs = tokenizer(text, return_tensors="pt")
    
#     with torch.no_grad():
#         outputs = model(**inputs)

#     last_hidden_states = outputs.last_hidden_state

#     cls_embedding = last_hidden_states[:, 0, :]
#     return cls_embedding

# def cosine_similarity(text1: str, text2: str):
#     embed1 = get_cls_embedings(text1)
#     embed2 = get_cls_embedings(text2)

#     similarity = F.cosine_similarity(embed1, embed2)
    
#     return similarity.item()  
# text1 = "Молодой ученый отправился в таинственный лес, чтобы исследовать легенды о магическом существе по имени Леший, и стал его учеником, погрузившись в мир магии и науки."
# text2 = "Молодой ученый, увлеченный мифами, отправился в лес, где стал учеником Лешего, изучая науку и магию для глубокого понимания мира."
# text3 = "Однажды ночью молодой астроном, увлеченный поисками внеземной жизни, вышел в открытое поле и установил свой телескоп. Он смотрел в космос, пытаясь найти признаки разумной цивилизации среди звездных скоплений. Внезапно, на грани видимости, он заметил странное свечение, которое двигалось к нему. По мере приближения свет начал приобретать форму, и перед ним появился маленький зеленый инопланетянин. Инопланетянин представился как Глитч и сказал, что прибыл с далекой планеты, чтобы предложить астроному стать его учеником. С этого момента жизнь молодого человека наполнилась космическими приключениями и новыми знаниями о Вселенной."
# # text4 ="dfssfd"
# # # Пример использования

# similarity_score = cosine_similarity(text1, text2)
# print(f"Косинусное сходство между текстами: {similarity_score}")

# similarity_score = cosine_similarity(text1, text3)

# print(f"Косинусное сходство между текстами: {similarity_score}")



# ___________for a lot texts_______________________________


from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

model_name = "DeepPavlov/rubert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_mean_embedings(text: str):
    inputs = tokenizer(text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)

    last_hidden_states = outputs.last_hidden_state

    mean_embedding = torch.mean(last_hidden_states, dim=1)
    return mean_embedding

def find_most_similar(texts, candidate_texts):
    embeddings = [get_mean_embedings(text) for text in texts]

    average_embedding = torch.mean(torch.stack(embeddings), dim=0)

    similarities = []
    for candidate in candidate_texts:
        candidate_embedding = get_mean_embedings(candidate)
        similarity = F.cosine_similarity(average_embedding, candidate_embedding)
        similarities.append(similarity.item())

    # most_similar_index = similarities.index(max(similarities))
    return (dict(zip( candidate_texts, similarities)))

text1 = "Он шел в лесу"
text2 = "Он гулял на улице"
text3 = "Он плавал в воде"

candidate_texts = [
    "Астрономия — это наука о звездах и планетах",
    "Магия и мифология всегда вдохновляли ученых",
    "Мальчик прыгал с крыши"
]

similarities = find_most_similar([text1, text2, text3], candidate_texts)

print()
# print(f"Наиболее схожий текст: {most_similar_text}")
# print(f"Косинусное сходство: {similarity_score}")




# ______________for text____________________________


# import torch
# from transformers import AutoTokenizer, AutoModel
# from torch.nn.functional import cosine_similarity

# # Модель для получения эмбеддингов (например, BERT)
# model_name = "bert-base-uncased"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)

# # Тексты для сравнения
# text1 = "Молодой ученый отправился в таинственный лес, чтобы исследовать легенды о магическом существе по имени Леший, и стал его учеником, погрузившись в мир магии и науки."
# # text2 = "Молодой ученый, увлеченный мифами, отправился в лес, где стал учеником Лешего, изучая науку и магию для глубокого понимания мира."
# text2 = "Однажды ночью молодой астроном, увлеченный поисками внеземной жизни, вышел в открытое поле и установил свой телескоп. Он смотрел в космос, пытаясь найти признаки разумной цивилизации среди звездных скоплений. Внезапно, на грани видимости, он заметил странное свечение, которое двигалось к нему. По мере приближения свет начал приобретать форму, и перед ним появился маленький зеленый инопланетянин. Инопланетянин представился как Глитч и сказал, что прибыл с далекой планеты, чтобы предложить астроному стать его учеником. С этого момента жизнь молодого человека наполнилась космическими приключениями и новыми знаниями о Вселенной."

# # Функция для получения эмбеддингов текста
# def get_embeddings(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     embeddings = outputs.last_hidden_state.mean(dim=1)  
#     return embeddings

# embeddings1 = get_embeddings(text1)
# embeddings2 = get_embeddings(text2)

# cos_sim = cosine_similarity(embeddings1, embeddings2)

# # Результат
# print(f"Косинусное сходство: {cos_sim.item():.4f}")


# # ______________sklearn for text____________________________




# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity

# # # Два текста для сравнения
# # text1 = "Молодой ученый отправился в таинственный лес, чтобы исследовать легенды о магическом существе по имени Леший, и стал его учеником, погрузившись в мир магии и науки."
# # text2 = "Молодой ученый, увлеченный мифами, отправился в лес, где стал учеником Лешего, изучая науку и магию для глубокого понимания мира."
# # text3 = "Однажды ночью молодой астроном, увлеченный поисками внеземной жизни, вышел в открытое поле и установил свой телескоп. Он смотрел в космос, пытаясь найти признаки разумной цивилизации среди звездных скоплений. Внезапно, на грани видимости, он заметил странное свечение, которое двигалось к нему. По мере приближения свет начал приобретать форму, и перед ним появился маленький зеленый инопланетянин. Инопланетянин представился как Глитч и сказал, что прибыл с далекой планеты, чтобы предложить астроному стать его учеником. С этого момента жизнь молодого человека наполнилась космическими приключениями и новыми знаниями о Вселенной."


# # # Преобразование текстов в TF-IDF векторы
# # vectorizer = TfidfVectorizer()
# # tfidf_matrix = vectorizer.fit_transform([text1, text2])

# # # Вычисление косинусного сходства
# # cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

# # # Результат
# # print(f"Косинусное сходство: {cos_sim[0][0]:.4f}")

# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity
# # import numpy as np

# # # Исходные 4 текста
# # target_texts = [
# #     "Косинусное сходство измеряет угол между векторами.",
# #     "Косинусное сходство помогает сравнить схожесть текстов.",
# #     "Метод TF-IDF позволяет представлять текст как числовой вектор.",
# #     "TF-IDF используется для вычисления важности слов в тексте."
# # ]

# # # Большой набор текстов для поиска схожих
# # all_texts = [
# #     "Косинусное сходство используется в обработке естественного языка.",
# #     "Этот метод полезен для сравнения текстов по их содержанию.",
# #     "TF-IDF также помогает исключить слишком частые слова.",
# #     "Анализ сходства текстов важен в информационном поиске.",
# #     "Косинусное сходство сравнивает углы между векторами текстов.",
# #     "TF-IDF часто применяется в классификации текстов.",
# #     "Алгоритмы, такие как TF-IDF, могут улучшить точность поиска.",
# #     "Косинусное сходство вычисляется через скалярное произведение."
# #     # Добавьте больше текстов в этот список, чтобы сделать его значительным
# # ]

# # # Преобразование текстов в TF-IDF векторы
# # vectorizer = TfidfVectorizer()

# # # Соединяем все тексты: сначала целевые, затем набор для поиска
# # combined_texts = target_texts + all_texts

# # # Преобразуем все тексты в векторы
# # tfidf_matrix = vectorizer.fit_transform(combined_texts)

# # # Разделяем векторные матрицы для целевых текстов и всех текстов
# # target_matrix = tfidf_matrix[:len(target_texts)]  # Векторы для целевых текстов
# # all_matrix = tfidf_matrix[len(target_texts):]     # Векторы для всех текстов

# # # Вычисление косинусного сходства
# # cos_sim_matrix = cosine_similarity(target_matrix, all_matrix)

# # # Функция для поиска топ-4 наиболее похожих текстов для каждого целевого текста
# # def find_top_similar(cos_sim_matrix, all_texts, top_n=4):
# #     results = []
# #     for idx, row in enumerate(cos_sim_matrix):
# #         # Находим индексы топ-N самых похожих текстов
# #         top_indices = np.argsort(row)[-top_n:][::-1]
# #         top_texts = [(all_texts[i], row[i]) for i in top_indices]
# #         results.append((f"Исходный текст {idx + 1}", top_texts))
# #     return results

# # # Получаем результаты
# # top_similar_texts = find_top_similar(cos_sim_matrix, all_texts)

# # # Выводим результаты
# # for target, similars in top_similar_texts:
# #     print(target)
# #     for i, (text, similarity) in enumerate(similars, 1):
# #         print(f"  Похожий текст {i}: {text} (Сходство: {similarity:.4f})")
# #     print()


# # import pandas as pd
# # from surprise import Dataset, Reader
# # from surprise import KNNBasic
# # from surprise.model_selection import train_test_split
# # from surprise import accuracy

# # # Пример данных (можно заменить на реальный набор данных)
# # # DataFrame с колонками: 'userId', 'itemId', 'rating'
# # data_dict = {
# #     'userId': [1, 1, 1, 2, 2, 3, 3, 4, 4, 5],
# #     'itemId': [101, 102, 103, 101, 102, 103, 104, 101, 105, 102],
# #     'rating': [4, 5, 3, 2, 4, 5, 4, 3, 5, 4]
# # }
# # df = pd.DataFrame(data_dict)

# # # Переход к формату, необходимому для surprise
# # reader = Reader(rating_scale=(1, 5))
# # data = Dataset.load_from_df(df[['userId', 'itemId', 'rating']], reader)
# # print
# # # Разделяем на тренировочный и тестовый наборы данных
# # trainset, testset = train_test_split(data, test_size=0.25)

# # # Используем KNN алгоритм для коллаборативной фильтрации
# # algo = KNNBasic(sim_options={'name': 'cosine', 'user_based': True})

# # # Обучаем модель
# # algo.fit(trainset)

# # # Предсказания на тестовом наборе
# # predictions = algo.test(testset)

# # # Оценка точности
# # accuracy.rmse(predictions)

# # # Функция для получения рекомендаций для пользователя
# # def get_top_n_recommendations(predictions, n=5):
# #     # Переводим предсказания в словарь, где ключ - пользователь, а значение - список рекомендуемых элементов
# #     top_n = {}
# #     for uid, iid, true_r, est, _ in predictions:
# #         if uid not in top_n:
# #             top_n[uid] = []
# #         top_n[uid].append((iid, est))

# #     # Сортируем по предсказанным рейтингам и берем топ-N для каждого пользователя
# #     for uid, user_ratings in top_n.items():
# #         user_ratings.sort(key=lambda x: x[1], reverse=True)
# #         top_n[uid] = user_ratings[:n]

# #     return top_n

# # # Получаем топ-5 рекомендаций для каждого пользователя
# # top_n_recommendations = get_top_n_recommendations(predictions, n=5)

# # # Выводим рекомендации
# # for uid, user_ratings in top_n_recommendations.items():
# #     print(f"Рекомендации для пользователя {uid}:")
# #     for iid, rating in user_ratings:
# #         print(f"  Рекомендуемый элемент {iid} с предсказанным рейтингом {rating:.2f}")
