import random
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 한국어 모델 불러오기
model = SentenceTransformer("jhgan/ko-sroberta-multitask")
df = pd.read_csv("data/ChatbotData.csv")

# 데이터 임베딩 생성 후 csv 저장
# embedding_list = []
# for temp in df["q"]:
#     embed_temp = model.encode(temp)
#     embedding_list.append(embed_temp)

# df_embedding = pd.DataFrame(embedding_list)
# df_embedding.to_csv("data/ChatbotData_embedding.csv", index=False, header=False)

df_embedding = pd.read_csv("data/ChatbotData_embedding.csv", header=None)


def ai_chatbot(text):
    em_result = model.encode(text)
    co_result = []

    for temp in range(len(df_embedding)):
        data = df_embedding.iloc[temp]
        co_result.append(cosine_similarity([em_result], [data])[0][0])

    df["cos"] = co_result
    df_result = df.sort_values(by="cos", ascending=False)
    r = random.randint(0, 5)

    return df_result.iloc[r]["A"]
