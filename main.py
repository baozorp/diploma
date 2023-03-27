import time
from threading import Thread

from generators import start_generators
from content_based import content_based
from collaborative_system import collaborative_system
from distance import distance
from merge_recommendations import merge_recommendations

#start_generators()

start = time.time()

targets = (collaborative_system, content_based, distance)

threads = []
for i in targets:
    threads.append(Thread(target=i))

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

merge_recommendations()

end = time.time() - start
print(f"{end} seconds")
