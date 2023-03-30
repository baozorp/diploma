import pandas as pd
import numpy as np


def _recommend_distances(objects, room_distance_matrix, current_object):
    # Initialize an empty matrix with the same number of rows and columns as the number of objects
    num_objects = len(objects)

    distance_array = np.zeros(num_objects)

    # Iterate through each pair of objects
    for i in range(num_objects):
        if objects[i]['room_id'] == objects[current_object]['room_id']:
            distance = np.hypot(objects[current_object]['x'] - objects[i]['x'], objects[current_object]['y'] - objects[i]['y'])
        else:
            room_distance = room_distance_matrix[objects[i]['room_id']][objects[current_object]['room_id']]
            distance = room_distance + _calculate_distance(objects[i]['x'], objects[i]['y'], 0, 0) + _calculate_distance(objects[current_object]['x'], objects[current_object]['y'], 0, 0)
        distance_array[i] = distance

    # Create DataFrame from distance matrix and set the index to be the object IDs
    df = pd.DataFrame({'distances': distance_array})
    df.loc[current_object, 'distances'] = 14
    df = df.sort_values(by='distances', ascending=True)
    #df = df.drop(current_object)
    # Save DataFrame to CSV file
    df.to_csv('results/recs_distances.csv', index_label='ID')
    return df


def _calculate_distance(x1, y1, x2, y2):
    distance = np.hypot(x2 - x1, y2 - y1)
    return distance


def distance(sources_path, results_path):

    # Load objects from CSV
    objects_df = pd.read_csv(f"{sources_path}/coordinates.csv")

    # Convert DataFrame to list of objects
    objects = objects_df.to_dict('records')

    # Load room distance matrix from CSV
    room_distance_matrix_df = pd.read_csv(f"{sources_path}/room_distance_matrix.csv", index_col=0)
    room_distance_matrix_df.columns = room_distance_matrix_df.columns.astype(int)

    # Convert DataFrame to room distance matrix
    room_distance_matrix = room_distance_matrix_df.to_dict()

    current_object = 231
    results = _recommend_distances(objects, room_distance_matrix, current_object)
    # Save DataFrame to CSV file
    results.to_csv(f"{results_path}/recs_distances.csv", index_label='ID')
