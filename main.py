import time
from threading import Thread
import yaml

from generators.generators import start_generators
from recommendation_systems.content_based import content_based
from recommendation_systems.collaborative_system import collaborative_system
from recommendation_systems.distance import distance
from recommendation_systems.merge_recommendations import merge_recommendations

# start_generators()

start = time.time()

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
sources_path = config['paths']['sources']
results_path = config['paths']['results']

targets = [
    (collaborative_system, sources_path, results_path),
    (content_based, sources_path, results_path),
    (distance, sources_path, results_path)
]

threads = []
for target in targets:
    thread = Thread(target=target[0], args=target[1:])
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

merge_recommendations()

end = time.time() - start
print(f"{end} seconds")
