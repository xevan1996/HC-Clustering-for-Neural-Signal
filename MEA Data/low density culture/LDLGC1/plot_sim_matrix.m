function plot_sim_matrix(sim_index, max_value)

    image_mat = pcolor(sim_index);
    set(image_mat, 'EdgeColor', 'none')
    colormap(jet)
    caxis([0 max_value])
    colorbar