import numpy as np
import pandas as pd
from numpy import heaviside
import matplotlib.pyplot as plt

def act_time_import(act_time):
    dst = pd.read_csv(act_time, header = None)
    act_time = dst.to_numpy()
    return act_time

def remove_ground(act_time):
    row_to_delete = [0, 3, 5, 53, 59]
    for row in row_to_delete:
        act_time = np.delete(act_time, row, 0)
    return act_time

def act_matrix_calc(act_time):
    channel_count = 0
    matrix_row = 0
    burst_column = 0
    activation_slot = 0

    Lrow = len(act_time)
    Lcol = len(act_time[0])
    act_matrix = np.zeros((Lrow * Lrow, Lcol))

    while burst_column < Lcol:

        while channel_count < Lrow:

            while matrix_row < Lrow:

                if act_time[channel_count, burst_column] != 0 and act_time[matrix_row, burst_column] != 0 and channel_count != matrix_row:
                    act_matrix[activation_slot, burst_column] = act_time[channel_count, burst_column] - act_time[matrix_row, burst_column]

                matrix_row = matrix_row + 1
                activation_slot = activation_slot + 1

            channel_count = channel_count + 1
            matrix_row = 0

        burst_column = burst_column + 1
        channel_count = 0
        activation_slot = 0

    return act_matrix

def sim_matrix_calc(burst_elec, act_matrix, time_const):
    dst = pd.read_csv('Active Electrode.csv', header = None)
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
                    rela_diff = time_const - abs(act_matrix[row_compute, column_ref] - act_matrix[row_compute, column_current])
                    heav_step = heaviside(rela_diff, 0)
                    summation = heav_step + summation
                row_compute = row_compute + 1

            sim_index[column_ref, column_current] = 1 / form_elec * summation
            column_current = column_current + 1

        column_ref = column_ref + 1
        return sim_index

def plot_sim_index(sim_index):
    N = len(sim_index)
    plt.pcolormesh(sim_index, cmap = 'jet', vmin = 0, vmax = 1)
    plt.colorbar()
    plt.xlim([0,N])
    plt.ylim([0,N])
    plt.show()

def write_sim_index(sim_index):
    np.savetxt('Sim Index.csv', sim_index, delimiter=',')
