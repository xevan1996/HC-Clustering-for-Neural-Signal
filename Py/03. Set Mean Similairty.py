import math
import numpy as np
import pandas as pd
from numpy import heaviside
import matplotlib.pyplot as plt

def mean_activation(outperm, act_matrix):
    mean_column = 0
    Lrow = len(act_matrix)
    Lcol = len(act_matrix[0])
    sorted_act_matrix = np.zeros((Lrow, Lcol))

    while mean_column < Lcol:
        sorted_act_matrix[:, mean_column] = act_matrix[:, outperm[0, mean_column]]
        mean_column = mean_column + 1

    set_size = round(math.sqrt(Lcol))
    burst_mean_set = np.zeros((Lrow, Lcol - set_size + 1))
    ref_row = 0

    while ref_row < Lrow:
        lower_boundary = 0
        upper_boundary = lower_boundary  + set_size - 1
        summation_burst_column = 0

        while upper_boundary < Lcol:
            summation_burst = 0
            repetition_count = 0

            while repetition_count < set_size:
                summation_burst = summation_burst + sorted_act_matrix[ref_row, summation_burst_column]
                summation_burst_column = summation_burst_column + 1
                repetition_count = repetition_count + 1

            burst_mean_set[ref_row, lower_boundary] = summation_burst / set_size;
            lower_boundary = lower_boundary + 1;
            summation_burst_column = lower_boundary;
            upper_boundary = lower_boundary + set_size - 1

        ref_row = ref_row + 1
    return set_size, sorted_act_matrix, burst_mean_set

def mean_similarity(set_size, sorted_act_matrix, burst_mean_set, outperm, time_const):
    Lrow = len(sorted_act_matrix)
    Lcol = len(sorted_act_matrix[0])
    setcol = len(burst_mean_set[0])

    dst = pd.read_csv('Active Electrode.csv', header = None)
    burst_elec = dst.to_numpy()

    mean_sim_index = np.zeros((set_size, setcol))
    lower_boundary = 0
    upper_boundary = lower_boundary + set_size - 1
    sim_burst_column = 0
    sam_column = 0

    while upper_boundary < Lcol:
        repetition_count = 0

        while repetition_count < set_size:
            sam_row = 0
            summation = 0

            act_elec = burst_elec[outperm[0, sam_column], 0]
            formula_elec = act_elec * (act_elec - 1);

            while sam_row < Lrow:
                if sorted_act_matrix[sam_row, sam_column] != 0 and burst_mean_set[sam_row, sim_burst_column] != 0:
                    rela_diff = time_const - abs(sorted_act_matrix[sam_row, sam_column] - burst_mean_set[sam_row, sim_burst_column])
                    heav_step = heaviside(rela_diff, 0)
                    summation = heav_step + summation

                sam_row = sam_row + 1

            mean_sim_index[repetition_count, sim_burst_column] = 1 / formula_elec * summation
            sam_column = sam_column + 1
            repetition_count = repetition_count + 1

        lower_boundary = lower_boundary + 1
        sam_column = lower_boundary;
        upper_boundary = lower_boundary + set_size - 1
        sim_burst_column = sim_burst_column + 1
    return mean_sim_index

def write_sim_index(mean_sim_index):
    np.savetxt('Mean Sim Index.csv', mean_sim_index, delimiter=',')

def read_mean_sim_index(mean_sim_index):
    dst = pd.read_csv(mean_sim_index, header = None)
    mean_sim_index = dst.to_numpy()
    return mean_sim_index

def set_mean(mean_sim_index, set_size):
    mean_sum = 0
    Lcol = len(mean_sim_index[0])
    set_mean_similarity = np.zeros((3, Lcol))

    while mean_sum < Lcol:
        sum_mean_sim = 0
        sum_total = 0

        while sum_mean_sim < set_size:

            sum_total = sum_total + mean_sim_index[sum_mean_sim, mean_sum]
            sum_mean_sim = sum_mean_sim + 1

        set_mean_similarity[0, mean_sum] = sum_total / set_size
        set_mean_similarity[1, mean_sum] = mean_sum
        set_mean_similarity[2, mean_sum] = mean_sum + set_size - 1
        mean_sum = mean_sum + 1
    return set_mean_similarity

def plot_set_mean(set_mean_similarity):
    plt.plot(set_mean_similarity[0,:])
    plt.grid()
    plt.show()

def combine_plot(sorted_sim_matrix, set_mean_similarity, vmin, vmax):
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Reordered Similarity Matrix')

    N = len(sorted_sim_matrix)
    ax1.pcolormesh(sorted_sim_matrix, cmap = 'jet', vmin = vmin, vmax = vmax)
    plt.xlim([0,N])
    plt.ylim([0,N])

    ax2.plot(set_mean_similarity[0,:])
    ax2.grid()
    plt.ylim([0,1])
    plt.show()
