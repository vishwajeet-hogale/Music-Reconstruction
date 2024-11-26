# TempoFitnessFunction

def tempoFitness(population):
    gene=1
    T=[]
    for child in population:
        for i in range(0,4):
            T[i]=child[gene][11]
            tempo_sum += T[i]
        tempo_mean = tempo_sum/4
        for j in range(0,4):
            if child[gene][11]-tempo_mean==(2*tempo_mean or tempo_mean/2):
                #decide how many fit genes are required in order to pass for fit population
            