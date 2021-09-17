function plot_combine(sorted_sim_index, set_mean_similarity, max_value)

    figure
    subplot(2,1,1)
    plot_sim_matrix(sorted_sim_index, max_value);
    subplot(2,1,2)
    plot(set_mean_similarity(1,:))