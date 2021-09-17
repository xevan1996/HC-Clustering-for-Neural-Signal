function [set_size, burst_mean_set, mean_sim_index, set_mean_similarity] = get_sim_similarity(burst_t0, burst_elec, time_const, activation_matrix, sorted_activation_matrix, outperm)

    mean_column = 1;

    while mean_column <= length(burst_t0)

        sorted_activation_matrix(1:length(activation_matrix), mean_column) = activation_matrix(:, outperm(mean_column));
        mean_column = mean_column + 1;
    end

    set_size = round(sqrt(length(burst_t0)));
    ref_row = 1;


    while ref_row <= length(sorted_activation_matrix)

        lower_boundary = 1;
        upper_boundary = lower_boundary + set_size - 1;
        summation_burst_column = 1;

        while upper_boundary <= length(burst_t0)

            summation_burst = 0;
            repetition_count = 1;

            while repetition_count <= set_size

                summation_burst = summation_burst + sorted_activation_matrix(ref_row, summation_burst_column);
                summation_burst_column = summation_burst_column + 1;
                repetition_count = repetition_count + 1;
            end
	
            burst_mean_set(ref_row, lower_boundary) = summation_burst / set_size;
            lower_boundary = lower_boundary + 1;
            summation_burst_column = lower_boundary;
            upper_boundary = lower_boundary + set_size - 1;
        end

        ref_row = ref_row + 1;
    end
    
    lower_boundary = 1;
    upper_boundary = lower_boundary + set_size - 1;
    sim_burst_column = 1;
    sam_column = 1;

    while upper_boundary <= length(burst_t0)

        repetition_count = 1;

        while repetition_count <= set_size
	
            sam_row = 1;
            summation = 0;

            act_elec = burst_elec(outperm(sam_column));
            formula_elec = act_elec * (act_elec - 1);

            while sam_row <= length(sorted_activation_matrix)

                if sorted_activation_matrix(sam_row, sam_column) ~= 0 && burst_mean_set(sam_row, sim_burst_column) ~= 0 

                    rela_diff = time_const - abs(sorted_activation_matrix(sam_row, sam_column) - burst_mean_set(sam_row, sim_burst_column));
                    heav_step = heaviside(rela_diff);
                    summation = heav_step + summation;
                end

                sam_row = sam_row + 1;
            end

            mean_sim_index(repetition_count, sim_burst_column) = 1 / formula_elec * summation;
            sam_column = sam_column + 1;
            repetition_count = repetition_count + 1;
        end

        lower_boundary = lower_boundary + 1;
        sam_column = lower_boundary;
        upper_boundary = lower_boundary + set_size - 1;
        sim_burst_column = sim_burst_column + 1;
    end
    
    mean_sum = 1;

    while mean_sum <= length(mean_sim_index)

        sum_mean_sim = 1;
        sum = 0;

        while sum_mean_sim <= set_size
		
            sum = sum + mean_sim_index(sum_mean_sim, mean_sum);
            sum_mean_sim = sum_mean_sim + 1;
        end

        set_mean_similarity(1, mean_sum) = sum / set_size;
        set_mean_similarity(2, mean_sum) = mean_sum;
        set_mean_similarity(3, mean_sum) = mean_sum + set_size - 1;
        mean_sum = mean_sum + 1;
    end