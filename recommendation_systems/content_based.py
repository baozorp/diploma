import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import os
# Function to recommend similar wines


def content_based(sources_path, results_path):

    user_data_path = sources_path + "current_user.csv"
    exhibits_path = sources_path + "wine_museum_exhibits.csv"

    if not os.path.isfile(user_data_path):
        raise FileNotFoundError(f"Current user data file {user_data_path} not found.")
    if not os.path.isfile(exhibits_path):
        raise FileNotFoundError(f"Wine museum exhibits data file {user_data_path} not found.")

    current_user = pd.read_csv(user_data_path)
    # Get the ID of the last object visited by user 0
    last_object_id = current_user.iloc[-1]['object_id']

    # Load the wine database into a DataFrame
    df = pd.read_csv(exhibits_path, usecols=lambda column: column != 'ID')

    # Select relevant features for similarity calculations

    features = df.columns.tolist()

    # Encode categorical variables as numeric
    gf = pd.get_dummies(df, columns=features)
    # Calculate pairwise cosine similarity between all wines
    similarity = cosine_similarity(gf)
    list_of_wines = _recommend_wines(last_object_id, similarity, df)

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
        list_of_wines.to_csv(f"{results_path}recs_content_based.csv", index=False)
    else:
        print("Content based had a validation error")


def _recommend_wines(id, similarity, df):
    # Get the similarity scores of all other wines
    scores = list(enumerate(similarity[id]))

    # Sort by similarity using a vectorized operation
    sorted_indexes = np.argsort(similarity[id])[::-1]
    scores = np.array(scores)[sorted_indexes]

    # Create a DataFrame of the sorted scores
    result = pd.DataFrame({'ID': scores[:, 0], 'similarity': scores[:, 1]})

    return result
