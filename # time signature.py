# time signature
from collections import Counter
def score_time_signature(self, individual):
    time_signatures = [ind.get('time_signature') for ind in individual[:5]]
    counts=Counter(time_signatures) # count occurences of each time signature
    max_freq = max(counts.values()) # get the highest frequency of time signature

    if max_freq==5:
        score=100
    elif max_freq==4:
        score = 80
    elif max_freq==3:
        score = 60
    elif max_freq==2:
        score = 40
    else:
        score = 20

    return score