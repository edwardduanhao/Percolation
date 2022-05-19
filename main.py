import sys
import grid
import pickle
import numpy as np
import multiprocessing as mp
import pandas as pd
from tqdm import tqdm, trange

def simulate(pid, p, d = 2, n = 10, N_times = 20):
    tqdm_text = "#" + "{}".format(round(p, 3))+"#" + "{}".format(n).zfill(3)
    res = []
    with tqdm(total=N_times, desc=tqdm_text, position=pid) as pbar:
        for i in range(N_times):
            temp = grid.grid(p = p, d = d, n = n)
            res.append(temp.check_path_to_border(tuple([0]*d)))
            pbar.update(1)
    return np.mean(res)


if __name__ == '__main__':
    m = 24;  d= 3;  N_times = 40; n = int(sys.argv[1])*2
    args = [i/m for i in list(range(1, m))]
    pool = mp.Pool(processes = 8)
    jobs = [pool.apply_async(simulate, args=(i, p, d, n, N_times)) for i, p in enumerate(args)]
    results = [job.get() for job in jobs]
    pool.close()
    ans = dict(zip(args, results))
    file_name = './'+ 'd = ' + str(d) + '/'+'n_' + str(n) + '.csv'
    df = pd.DataFrame()
    df.index = list(ans.keys())
    df['n = ' + str(n)] = list(ans.values())
    df.to_csv(file_name)
    
    
    
    
    
        