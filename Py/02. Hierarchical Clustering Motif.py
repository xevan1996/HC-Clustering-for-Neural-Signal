import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram

def hc_dendro(sim_matrix):
    dst = pd.read_csv(sim_matrix, header = None)
    sim_index = dst.to_numpy()

    y= pdist(sim_index)
    z = linkage(y, method = 'single', metric = 'euclidean')
    output_hc = dendrogram(z)
    return output_hc, sim_index
    
def hc_reorder(output_hc, sim_index):
    outperm = np.asarray(output_hc['leaves'])
    outperm = outperm.reshape((-1, 1))
    outperm = outperm.transpose()

    i = 0
    row_ref = 0
    Lrow, Lcol = [len(sim_index), len(sim_index[0])]
    sorted_sim_index = np.zeros((Lrow, Lcol))

    while row_ref < len(sim_index):
        col_ref = 0
        j = 0

        while col_ref < len(sim_index):
            sorted_sim_index[i, j] = sim_index[outperm[0, col_ref], outperm[0, row_ref]]
            col_ref = col_ref + 1
            j = j + 1
        
        row_ref = row_ref + 1
        i = i + 1     
    return outperm, sorted_sim_index

def reorder_matrix_plot(sorted_sim_matrix, vmin, vmax):
    N = len(sorted_sim_matrix)
    plt.pcolormesh(sorted_sim_matrix, cmap = 'jet', vmin = vmin, vmax = vmax)
    plt.colorbar()
    plt.xlim([0,N])
    plt.ylim([0,N])
    plt.show()
    
