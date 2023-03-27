import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

# Function to recommend similar wines


def recommend_wines(id, similarity, df):
    # Get the similarity scores of all other wines
    scores = list(enumerate(similarity[id]))

    # Sort by similarity using a vectorized operation
    sorted_indexes = np.argsort(similarity[id])[::-1]
    scores = np.array(scores)[sorted_indexes]

    # Create a DataFrame of the sorted scores
    result = pd.DataFrame({'ID': scores[:, 0], 'similarity': scores[:, 1]})

    result.to_csv("results/recs_content_based.csv", index=False)
    return result


def content_based():

    current_user = pd.read_csv("sources/current_user.csv")

    # Get the ID of the last object visited by user 0
    last_object_id = current_user.iloc[-1]['object_id']

    # Load the wine database into a DataFrame
    df = pd.read_csv('sources/wine_museum_exhibits.csv')

    # Select relevant features for similarity calculations

    features = df.columns.tolist()
    df = df[features]

    # Encode categorical variables as numeric
    gf = pd.get_dummies(df, columns=features)
    # Calculate pairwise cosine similarity between all wines
    similarity = cosine_similarity(gf)
    list_of_wines = recommend_wines(last_object_id, similarity, df)

    # Validation
    sorted_indexes = list_of_wines['ID'].tolist()  # Get sorted indexes
    gf_sorted = gf.loc[sorted_indexes]  # Sort gf by the sorted indexes
    item_vector = gf.loc[last_object_id]
    gf_sorted = gf_sorted.drop(labels=last_object_id)
    gf_split = np.array_split(gf_sorted, 5)

    similarities = []
    for split in gf_split:
        split_similarities = []
        for index, row in split.iterrows():
            split_vector = row.values
            cos_sim = np.dot(split_vector, item_vector) / (np.linalg.norm(split_vector) * np.linalg.norm(item_vector))
            split_similarities.append(cos_sim)
        average_similarity = sum(split_similarities) / len(split)
        similarities.append(average_similarity)
    validation_result = (similarities == sorted(similarities, reverse=True))
    if validation_result:
        print("Content based has been successfully validated")
    else:
        print("Content based had a validation error")
