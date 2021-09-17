import math
import numpy as np
import pandas as pd
from numpy import heaviside
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram

def act_time_import(act_time):
    dst = pd.read_csv(act_time, header = None)
    act_time = dst.to_numpy()
    return act_time

def remove_ground(act_time):
    row_to_delete = [0, 3, 5, 53, 59]
    for row in row_to_delete:
        act_time = np.delete(act_time, row, 0)
    return act_time

def act_matrix(act_matrix):
    dst = pd.read_csv(act_matrix, header = None)
    act_matrix = dst.to_numpy()
    return act_matrix

def sim_matrix_calc(act_elec, burst_elec, act_matrix, time_const):
    dst = pd.read_csv(act_elec, header = None)
    burst_elec = dst.to_numpy()
    Lrow = len(act_matrix)
    Lcol = len(act_matrix[0])
    sim_index = np.zeros((Lcol + 1, Lcol + 1))

    column_ref = 0

    while column_ref < Lcol:
        column_current = 0
        act_elec = burst_elec[column_ref]
        form_elec = act_elec * (act_elec - 1)

        while column_current < Lcol:
            row_compute = 0
            summation = 0

            while row_compute < Lrow:
                if act_matrix[row_compute, column_ref] != 0 and act_matrix[row_compute, column_current] != 0:
                    rela_diff = 0.01 - abs(act_matrix[row_compute, column_ref] - act_matrix[row_compute, column_current])
                    heav_step = heaviside(rela_diff, 0)
                    summation = heav_step + summation
                row_compute = row_compute + 1

            sim_index[column_ref, column_current] = 1 / form_elec * summation
            column_current = column_current + 1

        column_ref = column_ref + 1
        return sim_index

def plot_sim_index(sim_index, vmin, vmax):
    N = len(sim_index)
    fig = plt.figure(figsize = (12, 8), dpi= 100)
    plt.xlim([0,N])
    plt.xlabel('Burst Index', fontsize = 14)
    plt.ylim([0,N])
    plt.ylabel('Burst Index', fontsize = 14)
    fig.suptitle('Similarity Matrix', fontsize = 18)
    plt.pcolormesh(sim_index, cmap = 'jet', vmin = vmin, vmax = vmax)
    plt.colorbar()

def write_sim_index(sim_index):
    np.savetxt('Sim Index.csv', sim_index, delimiter=',')

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
    fig = plt.figure(figsize = (12, 8), dpi= 100)
    plt.xlim([0,N])
    plt.xlabel('Burst Index', fontsize = 14)
    plt.ylim([0,N])
    plt.ylabel('Burst Index', fontsize = 14)
    fig.suptitle('Reordered Similarity Matrix', fontsize = 18)
    plt.pcolormesh(sorted_sim_matrix, cmap = 'jet', vmin = vmin, vmax = vmax)
    plt.colorbar()

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

def mean_similarity(act_elec, set_size, sorted_act_matrix, burst_mean_set, outperm, time_const):
    Lrow = len(sorted_act_matrix)
    Lcol = len(sorted_act_matrix[0])
    setcol = len(burst_mean_set[0])

    dst = pd.read_csv(act_elec, header = None)
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

def write_mean_sim_index(mean_sim_index):
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
    fig = plt.figure(figsize = (12, 8), dpi= 100)
    plt.plot(set_mean_similarity[0,:])
    fig.suptitle('Mean Similarity of Burst Sets', fontsize = 18)
    plt.xlabel('Burst Set', fontsize = 14)
    plt.ylabel('Mean Similarity', fontsize = 14)
    plt.grid()

def combine_plot(sorted_sim_matrix, set_mean_similarity, vmin, vmax):
    fig, (ax1, ax2) = plt.subplots(2, figsize = (12, 8), dpi= 100)

    N = len(sorted_sim_matrix)
    ax1.pcolormesh(sorted_sim_matrix, cmap = 'jet', vmin = vmin, vmax = vmax)
    plt.xlim([0,N])
    plt.ylim([0,N])

    ax2.plot(set_mean_similarity[0,:])
    ax2.grid()
    plt.ylim([0,1])
    plt.show()

def order_transform(act_time, outperm, outperm_num):
    dst = pd.read_csv(act_time, header = None)
    act_time_order = dst.to_numpy()

    order_dummy = np.zeros((64, 2))
    order_dummy[:, 0] = act_time_order[:, outperm_num]
    order_elec_num_arrange = 1
    order_activated_elec = 0
    order_repeat = 0

    while order_repeat < 64:
        if order_dummy[order_repeat, 0] != 0:
            order_activated_elec = order_activated_elec + 1

        order_dummy[order_repeat, 1] = order_elec_num_arrange
        order_elec_num_arrange= order_elec_num_arrange + 1
        order_repeat = order_repeat + 1

    order_time = np.sort(order_dummy[:,0], 0)

    order_repeat = 0
    order_row = 0
    order = np.zeros((order_activated_elec, 1))
    order_activated_num = 0

    while order_row < 64:
        order_repeat = 0

        if order_time[order_row] != 0:
            while order_repeat < 64 - order_activated_num:
                if order_time[order_row] == order_dummy[order_repeat, 0]:
                    order[order_activated_num] = order_dummy[order_repeat, 1]
                    order_dummy = np.delete(order_dummy, order_repeat, 0)
                    order_activated_num = order_activated_num + 1

                order_repeat = order_repeat + 1
        order_row = order_row + 1

    order_max = len(order)

    order_elec_num = 0
    prop_order = np.zeros((2, order_max))

    while order_elec_num < order_max:
        wreg_order = order[order_elec_num, 0]
        prop_column = 1
        prop_repeat_count = 1

        while prop_column <= 8:
            prop_row = 8

            while prop_row >= 1:
                if wreg_order == prop_repeat_count:
                    prop_order[0, order_elec_num] = prop_row
                    prop_order[1, order_elec_num] = prop_column
                    order_elec_num = order_elec_num + 1

                prop_row = prop_row - 1
                prop_repeat_count = prop_repeat_count + 1

            prop_column = prop_column + 1
    return order, prop_order

def prop_plot(prop_order):
    def electrode_template():
        x = 1
        template_count = 0
        elect_template = np.zeros((2, 64))

        while x <= 8:
            y = 1

            while y <= 8:
                elect_template[0, template_count] = y
                elect_template[1, template_count] = x
                template_count = template_count + 1
                y = y + 1

            x = x + 1

        elect_template = np.delete(elect_template, 0, 1)
        elect_template = np.delete(elect_template, 6, 1)
        elect_template = np.delete(elect_template, 54, 1)
        elect_template = np.delete(elect_template, 60, 1)
        plt.plot(elect_template[0, :], elect_template[1, :], 'ko', markerfacecolor='none')
        plt.xlim([0, 9])
        plt.ylim([0, 9])
        plt.show()

    color_change = len(prop_order[0]) / 6
    color_change = round(color_change)
    color_choice = ['blue', 'cyan', 'green', 'yellow', 'orange', 'red']

    prop_num_max = len(prop_order[0]) - 1
    prop_num = 0

    while prop_num < prop_num_max:
        if prop_num <= color_change:
            color = color_choice[0]
        elif prop_num > color_change and prop_num <= 2 * color_change:
            color = color_choice[1]
        elif prop_num > 2 * color_change and prop_num <= 3 * color_change:
            color = color_choice[2]
        elif prop_num > 3 * color_change and prop_num <= 4 * color_change:
            color = color_choice[3]
        elif prop_num > 4 * color_change and prop_num <= 5 * color_change:
            color = color_choice[4]
        elif prop_num > 5 * color_change and prop_num <= 6 * color_change:
            color = color_choice[5]

        plt.plot(((prop_order[1, prop_num]), (prop_order[1, prop_num + 1])), ((prop_order[0, prop_num]), (prop_order[0, prop_num + 1])), color, linewidth = 0.5)
        prop_num = prop_num + 1
    electrode_template()
    plt.show()
