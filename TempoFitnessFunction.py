# TempoFitnessFunction


def tempoFitness(population):
    gene=0
    T=[]
    points=[]
    for child in population:
        for i in range(0,5):
            T[i]=child[gene][11]
            tempo_sum += T[i]
            gene +=1
        tempo_mean = tempo_sum/4
        gene=0
        for j in range(0,5):
            diff = child[gene][11]-tempo_mean
            points[i]=100-diff
            gene +=1

    return points
            

            
