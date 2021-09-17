function [activation_time, activation_matrix] = get_act_matrix(burst_channel, burst_index, burst_t0, burst_burstlets, burstlet_start, spks_time)
    
    overall_count = 1;
    channel_count = 1;

    while overall_count <= length(burst_channel)
        channel_matrix (burst_channel(channel_count), burst_index(channel_count)) = 1;
        channel_count = channel_count + 1;
        overall_count = overall_count + 1;
    end
    
    last_row = 1;
    while last_row <= length(burst_t0)
        channel_matrix (64, last_row) = 0;
        last_row = last_row + 1;
    end
    
    activation_time = channel_matrix;
    time_slot_count = 1;

    while time_slot_count <= length(burst_channel)
	
        if time_slot_count >= 1
            activation_time(burst_channel(time_slot_count), burst_index(time_slot_count)) = spks_time(burstlet_start(burst_burstlets(time_slot_count)));
        end

        time_slot_count = time_slot_count + 1;
    end
    
    gro_cell_del = [1, 4, 6, 54, 60];
    del_num = 1;
    
    for del_num = 1:5
        activation_time(gro_cell_del(del_num),:) = [];
        del_num = del_num + 1;
    end

    
    channel_count = 1;
    matrix_row = 1;
    burst_column = 1;
    activation_slot = 1;
    [Lrow, Lcol] = size(activation_time);
    
    while burst_column <= Lcol

        while channel_count <= Lrow

            while matrix_row <= Lrow
                if activation_time(channel_count, burst_column) ~= 0 && activation_time(matrix_row, burst_column) ~= 0 	&& channel_count ~= matrix_row	
                    activation_matrix(activation_slot, burst_column) = activation_time(channel_count, burst_column) - activation_time(matrix_row, burst_column);
                end

                matrix_row = matrix_row + 1;
                activation_slot = activation_slot + 1;
            end
	
            channel_count = channel_count + 1;
            matrix_row = 1;
        end
	
        channel_count = 1;
        burst_column = burst_column + 1;
        activation_slot = 1;
	
    end

    activation_matrix(3481, :) = 0;
end