import util
from tqdm import trange


class BruteForceExtractor():
    def __init__(self):
        pass

    def extract(self, timeseries, labels, min_len=None, max_len=None, 
                nr_shapelets=1, metric=util.calculate_ig):
        shapelets = []
        for j in trange(len(timeseries), desc='timeseries', position=0):
            # We will extract shapelet candidates from S
            S = timeseries[j, :]
            for l in range(min_len, max_len):  
                for i in range(len(S) - l + 1):
                    candidate = S[i:i+l]
                    # Compute distances to all other timeseries
                    L = []  # The orderline, to calculate entropy, only for IG
                    for k in range(len(timeseries)):
                        D = timeseries[k, :]
                        dist = util.sdist(candidate, D)
                        L.append((dist, labels[k]))
                    score = metric(L)
                    shapelets.append((list(candidate), list(score), [j, i, l]))

        shapelets = sorted(shapelets, key=key)
        best_shapelets = [x[0] for x in shapelets[:nr_shapelets]]
        return best_shapelets