import PropOrder as po
import matplotlib.pyplot as plt

raw_data = 'Data/HDHGC3 Activation Time.csv'
act_time = po.act_time_import(raw_data)
act_time  = po.remove_ground(act_time)

data_matrix = 'Data/HDHGC3 Activation Matrix.csv'
act_matrix = po.act_matrix(data_matrix)

#act_elec = 'Data/LDLGC1 Active Electrode.csv'
#sim_index = po.sim_matrix_calc(act_elec, act_matrix, 0.01)
#po.write_sim_index(sim_index)

data = 'Data/HDHGC3 Sim Index.csv'
plt.figure(figsize = (12, 8), dpi= 100)
output_hc, sim_matrix = po.hc_dendro(data)
outperm, sorted_sim_matrix = po.hc_reorder(output_hc, sim_matrix)

po.reorder_matrix_plot(sim_matrix, 0, 1)
po.reorder_matrix_plot(sorted_sim_matrix, 0, 1)

set_size, sorted_act_matrix, burst_mean_set = po.mean_activation(outperm, act_matrix)

act_elec = 'Data/HDHGC3 Active Electrode.csv'
mean_sim_index = po.mean_similarity(act_elec, set_size, sorted_act_matrix, burst_mean_set, outperm, 0.01)
po.write_mean_sim_index(mean_sim_index)

mean_sim_index = po.read_mean_sim_index('Data/HDHGC3 Mean Sim Index.csv')

set_mean_similarity = po.set_mean(mean_sim_index, set_size)

po.plot_set_mean(set_mean_similarity)
po.combine_plot(sorted_sim_matrix, set_mean_similarity, 0, 1)

order, prop_order = po.order_transform('LDLGC1 Activation Time.csv', outperm, 124)

po.prop_plot(prop_order)
