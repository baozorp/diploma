import time
from threading import Thread
import yaml
import os

from generators.generators import start_generators
from recommendation_systems.content_based import content_based
from recommendation_systems.collaborative_system import collaborative_system
from recommendation_systems.distance import distance
from merge_systems.merge_recommendations import merge_recommendations
from merge_systems.interference_to_euristic import interference_to_euristic

# start_generators()

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

threads = []
for target in targets:
    thread = Thread(target=target[0], args=target[1:])
    threads.append(thread)

for thread in threads:
    thread.start()


for thread in threads:
    thread.join()

# collaborative_system(sources_path, results_path)
# content_based(sources_path, results_path)
# distance(sources_path, results_path)

merge_recommendations(results_path)
interference_to_euristic(results_path)
# interference_to_euristic(results_path)
end = time.time() - start
print(f"{end} seconds")
