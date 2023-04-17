import pandas as pd
import os


def merge_recommendations(path):
    # Load the three recommendation CSV files

    df2 = pd.read_csv(path + '/recs_content_based.csv')
    df3 = pd.read_csv(path + '/recs_distances.csv')

    similarity_top = df2["similarity"].max()
    df2["score"] = 100 * df2["similarity"] / similarity_top

    distances_top = df3["distances"].min()
    df3["score"] = 100 * distances_top / df3["distances"]

    if os.path.exists('results/recs_collaborative.csv'):
        df1 = pd.read_csv('results/recs_collaborative.csv')
        # Calculate the scores for each recommendation
        seconds_top = df1["seconds"].max()
        df1["score"] = 100 * df1["seconds"] / seconds_top
    else:
        df1 = pd.DataFrame(columns=["ID", "Ыcore"])
        missing_ids = set(df2["ID"]).union(set(df3["ID"])) - set(df1["ID"])
        missing_df1 = pd.DataFrame({"ID": list(missing_ids), "score": 0})
        df1 = pd.concat([missing_df1, df1], ignore_index=True)
        current_user = pd.read_csv('current_user.csv')
        mask = ~df1["ID"].isin(current_user["object_id"].values)
        df1 = df1[mask]

    # Combine the three dataframes by id
    df = pd.merge(df1[["ID", "score"]], df2[["ID", "score"]], on="ID", suffixes=("_1", "_2"))
    df = pd.merge(df, df3[["ID", "score"]], on="ID")
    # Sum the scores for each ID
    df["score"] = df["score_1"] + df["score_2"] + df["score"]
    df = df.drop(columns=['score_1', 'score_2'])
    # Sort by score
    df = df.rename(columns={'score': 'merge_scores'})
    df = df.sort_values(by="merge_scores", ascending=False)
    df.to_csv('results/merged_recommendations.csv', index=False)
    print("Successfully merged")
