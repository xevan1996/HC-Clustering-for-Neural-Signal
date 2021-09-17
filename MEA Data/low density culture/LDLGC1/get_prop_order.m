function [order, prop_order] = get_prop_order(burst_channel, burst_index, burst_t0, burstlet_start, burst_burstlets, spks_time, outperm, outperm_num)

    overall_count = 1;
    channel_count = 1;

    while overall_count <= length(burst_channel)
        
        channel_matrix(burst_channel(channel_count), burst_index(channel_count)) = 1;
        channel_count = channel_count + 1;
        overall_count = overall_count + 1;
    end
    
    last_row = 1;
    
    while last_row <= length(burst_t0)
        
        channel_matrix (64, last_row) = 0;
        last_row = last_row + 1;
    end
    
    activation_time_order = channel_matrix;
    time_slot_count = 1;

    while time_slot_count <= length(burst_channel)
	
        if time_slot_count >= 1
            activation_time_order(burst_channel(time_slot_count), burst_index(time_slot_count)) = spks_time(burstlet_start(burst_burstlets(time_slot_count)));
        end

        time_slot_count = time_slot_count + 1;
    end
    
    order_dummy(:, 1) = activation_time_order(:, outperm_num);
    order_elec_num_arrange = 1;
    order_activated_elec = 0;
    order_repeat = 1;
    
    while order_repeat <= 64
        
        if order_dummy(order_repeat, 1) ~= 0
            order_activated_elec = order_activated_elec + 1;
        end
        
        order_dummy(order_repeat, 2) = order_elec_num_arrange;
        order_elec_num_arrange= order_elec_num_arrange + 1;
        order_repeat = order_repeat + 1;
    end
    
    order_time = sort(order_dummy(:,1), 1);
    
    order_row = 1;
    order_activated_num = 1;

    while order_row <= 64
        
        order_repeat = 1;

        if order_time(order_row) ~= 0
            while order_repeat <= 64 - order_activated_num 
                if order_time(order_row) == order_dummy(order_repeat, 1)
                   order(order_activated_num, 1) = order_dummy(order_repeat, 2);
                   order_dummy(order_repeat, :) = [];
                   order_activated_num = order_activated_num + 1;
                end
                
                order_repeat = order_repeat + 1;
            end
        end
        
        order_row = order_row + 1;
    end
    
    sim_elec_num = 1;

        while sim_elec_num <= length(order)

            wreg = order(sim_elec_num);
            prop_column = 1;
            prop_repeat_count = 1;
            flag_check = false;
	
            while prop_column <= 8 && flag_check == false
		
                prop_row = 8;

                while prop_row >= 1 && flag_check == false

                    if order(sim_elec_num) == prop_repeat_count
				
                        prop_order(1, sim_elec_num) = prop_row;
                        prop_order(2, sim_elec_num) = prop_column;	
                        sim_elec_num = sim_elec_num + 1;
                        flag_check = true;
                    end
		
                    if flag_check == false
                        prop_row = prop_row - 1;
                        prop_repeat_count = prop_repeat_count + 1;
                    end
                    
                end
                
                if flag_check == false
                    prop_column = prop_column + 1;
                end
            end
        end
end
    
   