function plot_prop_order(order, prop_order, color_choice)

    x = 1;
    template_count = 1;

    while x <= 8

        y = 1;

        while y <= 8

            electrode_template(1,template_count) = y;
            electrode_template(2,template_count) = x;
            y = y + 1;
            template_count = template_count + 1;
        end

        x = x + 1;
    end

    gro_cell_del = [1, 7, 55, 61];
    del_num = 1;
    
    for del_num = 1:4
        electrode_template(:, gro_cell_del(del_num)) = [];
        del_num = del_num + 1;
    end
    
    plot(electrode_template(1, :), electrode_template(2, :), 'o');
    axis([0,9,0,9]);
    colormap(jet)
    colorbar
    hold on

    order_repeat = 2;
    color_change = length(order) / 6;
    color_change = round(color_change);

    while order_repeat <= length(order)

        if order_repeat <= color_change
            color_choice_num = 1;
        elseif order_repeat > color_change && order_repeat <= (2 * color_change)
            color_choice_num = 2;
        elseif order_repeat > (2 * color_change) && order_repeat <= (3 * color_change)
            color_choice_num = 3;
        elseif order_repeat > (3 * color_change) && order_repeat <= (4 * color_change)
            color_choice_num = 4;
        elseif order_repeat > (4 * color_change) && order_repeat <= (5 * color_change)
            color_choice_num = 5;
        else
            color_choice_num = 6;
        end

        line([prop_order(2, (order_repeat - 1)),prop_order(2, order_repeat)] , [prop_order(1, (order_repeat - 1)),prop_order(1, order_repeat)], 'Color', color_choice(color_choice_num));
        hold on
        order_repeat = order_repeat + 1;
    end
end
    
   
    
    
