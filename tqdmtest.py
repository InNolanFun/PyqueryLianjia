from time import sleep
from tqdm import tqdm
with tqdm(total=100) as pbar:
    for i in range(10):
        pbar.update(10)
        sleep(0.1)