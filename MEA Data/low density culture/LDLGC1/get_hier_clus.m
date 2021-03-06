function [outperm, sorted_sim_index] = get_hier_clus(sim_index)

    Y = pdist(sim_index);
    Z = linkage(Y, 'single');
    [H,T,outperm] = dendrogram(Z, 0);


    i = 1;
    row_ref = 1;

    while row_ref <= length(sim_index)

        column_ref = 1;
        j = 1;

        while column_ref <= length(sim_index)

            sorted_sim_index(i, j) = sim_index(outperm(row_ref), outperm(column_ref));
            column_ref = column_ref + 1;
            j = j + 1;
        end

        row_ref = row_ref + 1;
        i = i + 1;
    end