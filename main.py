import time
from threading import Thread
import yaml
import os
from julia import Main as jl
from multiprocessing import Process

from generators.generators import start_generators
from recommendation_systems.content_based import content_based
from recommendation_systems.collaborative_system import collaborative_system
from recommendation_systems.distance import distance
from merge_systems.merge_recommendations import merge_recommendations
from merge_systems.interference_to_euristic import interference_to_euristic

# start_generators()
if __name__ == "__main__":
    print("Start process")
    start = time.time()

    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    sources_path = config['paths']['sources']
    results_path = config['paths']['results']

    if not os.path.exists(sources_path):
        raise FileNotFoundError(f"Exhibit folder {sources_path} not found.")

    if not os.path.exists(results_path):
        try:
            os.makedirs(results_path)
        except OSError as e:
            raise OSError(f"Failed to create directory: {results_path}") from e

    targets = [
        (content_based, sources_path, results_path),
        (distance, sources_path, results_path),
        (collaborative_system, sources_path, results_path)
    ]

    processes = []

    for target in targets:
        process = Thread(target=target[0], args=target[1:])
        processes.append(process)

    for process in processes:
        process.start()

    if not os.path.isfile(results_path + "heuristic.csv"):
        jl.include("julia/heuristic.jl")

    for process in processes:
        process.join()

    merge_recommendations(sources_path, results_path)
    interference_to_euristic(results_path)

    end = time.time() - start
    print(f"Process end with {end} seconds")
