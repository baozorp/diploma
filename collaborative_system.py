import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import random


def collaborative_system():
    # Load in the exhibit data
    exhibit_data = pd.read_csv("sources/exhibit_data.csv")
    current_user = pd.read_csv("sources/current_user.csv")
    if current_user.shape[0] < 20:
        return
    # Clip the time_spent values to 100 scores
    exhibit_data = pd.concat([exhibit_data, current_user], ignore_index=True)
    exhibit_data['time_spent'] = exhibit_data['time_spent'].clip(upper=300)

    # Create a pivot table of the exhibit data to get a matrix of user-item interactions
    user_item_matrix = exhibit_data.pivot_table(values='time_spent', index='user_id', columns='object_id').fillna(0)
    # Compute user similarity based on user-item interactions
    # Here, we are using cosine similarity as the similarity metric
    user_similarity = 1 - pairwise_distances(user_item_matrix, metric='cosine')
    user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

    # Validate the collaborative filtering system using a random subset of the data
    collaborative_validation(user_item_matrix, user_similarity_df, exhibit_data)

    # Get collaborative filtering recommendations for a specific user and save the results to a CSV file
    user_id = exhibit_data['user_id'].min()

    prediction = get_collaborative_filtering_recs(user_id, user_item_matrix, user_similarity_df)
    prediction = prediction.sort_values(ascending=False)
    prediction_df = pd.DataFrame(prediction, columns=['seconds'])
    prediction_df.reset_index(inplace=True)
    prediction_df.rename(columns={'object_id': 'ID'}, inplace=True)
    prediction_df.to_csv('results/recs_collaborative.csv', index=False)


def get_collaborative_filtering_recs(user_id, user_item_matrix, user_similarity_df, start_from=1, end_with=11, with_validation=False):
    # Get the user's interactions
    user_interactions = user_item_matrix.loc[user_id]

    # Get the similarity scores for the user
    user_similarities = user_similarity_df[user_id]

    # Get the top recommendations
    top_recs = user_similarities

    # Sort the recommendations by scores
    top_recs = top_recs.sort_values(ascending=False)

    # Get the top recommendations within the specified range
    cf_recs = top_recs[start_from:end_with]

    # Create a new matrix containing only the users in cf_recs
    new_matrix = user_item_matrix.loc[cf_recs.index]

    # Multiply new_matrix by the sum of user similarities in cf_recs
    coeff = cf_recs.sum()
    new_matrix = new_matrix.mul(cf_recs, axis=0)

    # Sum the columns in new_matrix
    prediction = new_matrix.sum(axis=0)

    # Exclude items that the user has already rated
    user_interactions = user_item_matrix.loc[user_id]
    user_interactions = user_interactions[user_interactions > 0] if with_validation else user_interactions[user_interactions == False]
    prediction = prediction[user_interactions.index] / coeff
    return prediction


def collaborative_validation(user_item_matrix, user_similarity_df, exhibit_data):
    # Get 5 random user IDs from the list
    user_ids = exhibit_data['user_id'].unique()
    random_user_ids = random.sample(user_ids.tolist(), 5)

    # Calculate the number of users in each part of the dataset
    part = int(len(user_ids) / len(random_user_ids))

    # Initialize validation_result to True
    validation_result = True

    # Iterate over each sample user
    for i in random_user_ids:
        prev = 0
        mean_score_array = [0]
        start_from = 1 - part
        end_with = 0

        # Iterate over each part of the dataset
        for j in range(len(random_user_ids)):
            # Get the collaborative filtering recommendations for a sample user
            start_from += part
            end_with += part
            user_interactions = user_item_matrix.loc[i]
            user_interactions = user_interactions[user_interactions > 0]
            prediction = get_collaborative_filtering_recs(i, user_item_matrix, user_similarity_df, start_from, end_with, with_validation=True)

            # Calculate the mean absolute error between the predicted and actual ratings
            prediction = prediction / user_interactions
            prediction = (prediction - 1).abs()

            # Add up the results and divide by the length of prediction
            mean_score = prediction.sum() / len(prediction)

            # Check if the current mean_score is greater than the previous mean_score in the array
            validation_result = validation_result and (mean_score > max(mean_score_array))

            # Append the current mean_score to the array
            mean_score_array.append(mean_score)

    # Print the validation result
    if validation_result:
        print("Collaborative filtering has been successfully validated")
    else:
        print("Collaborative filtering had a validation error")
