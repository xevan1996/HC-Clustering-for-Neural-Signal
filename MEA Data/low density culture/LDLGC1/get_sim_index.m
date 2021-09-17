function sim_index = get_sim_index(activation_matrix, time_const, burst_elec, burst_t0)

    column_ref = 1;
    time_const = 0.1;
    while column_ref <= length(burst_t0)

        column_current = 1;

        act_elec = burst_elec(column_ref);
        formula_elec = act_elec * (act_elec - 1);
	
        while column_current <= length(burst_t0)
			
            row_compute = 1;
            summation = 0;

            while row_compute <= length(activation_matrix)

                if activation_matrix(row_compute, column_ref) ~= 0 && activation_matrix(row_compute, column_current) ~= 0 
                    rela_diff = time_const - abs(activation_matrix(row_compute, column_ref) - activation_matrix(row_compute, column_current));
                    heav_step = heaviside(rela_diff);
                    summation = heav_step + summation;
                end

                row_compute = row_compute + 1;
            end
            
            sim_index(column_ref, column_current) = 1 / formula_elec * summation;
            column_current = column_current + 1;
            
        end
		
        column_ref = column_ref + 1;

    end
