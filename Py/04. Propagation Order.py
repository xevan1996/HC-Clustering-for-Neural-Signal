import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def order_transform(act_time, outperm, outperm_num):
    dst = pd.read_csv(act_time, header = None)
    act_time_order = dst.to_numpy()
    
    order_dummy = np.zeros((64, 2))
    order_dummy[:, 0] = act_time_order[:, outperm_num]
    order_elec_num_arrange = 1
    order_activated_elec = 0
    order_repeat = 0
    
    while order_repeat < 64:
        if order_dummy[order_repeat, 0] != 0:
            order_activated_elec = order_activated_elec + 1
            
        order_dummy[order_repeat, 1] = order_elec_num_arrange
        order_elec_num_arrange= order_elec_num_arrange + 1
        order_repeat = order_repeat + 1
    
    order_time = np.sort(order_dummy[:,0], 0)
    
    order_repeat = 0
    order_row = 0
    order = np.zeros((order_activated_elec, 1))
    order_activated_num = 0
    
    while order_row < 64:
        order_repeat = 0
        
        if order_time[order_row] != 0: 
            while order_repeat < 64 - order_activated_num:
                if order_time[order_row] == order_dummy[order_repeat, 0]:
                    order[order_activated_num] = order_dummy[order_repeat, 1]
                    order_dummy = np.delete(order_dummy, order_repeat, 0)
                    order_activated_num = order_activated_num + 1
                    
                order_repeat = order_repeat + 1
        order_row = order_row + 1
    
    order_max = len(order)
    
    order_elec_num = 0
    prop_order = np.zeros((2, order_max))
    
    while order_elec_num < order_max:
        wreg_order = order[order_elec_num, 0]
        prop_column = 1
        prop_repeat_count = 1
        
        while prop_column <= 8:
            prop_row = 8
            
            while prop_row >= 1:
                if wreg_order == prop_repeat_count:
                    prop_order[0, order_elec_num] = prop_row
                    prop_order[1, order_elec_num] = prop_column
                    order_elec_num = order_elec_num + 1
                    
                prop_row = prop_row - 1
                prop_repeat_count = prop_repeat_count + 1
                
            prop_column = prop_column + 1
    return order, prop_order

def prop_plot(prop_order):
    def electrode_template():
        x = 1
        template_count = 0
        elect_template = np.zeros((2, 64))

        while x <= 8:
            y = 1
    
            while y <= 8:
                elect_template[0, template_count] = y
                elect_template[1, template_count] = x
                template_count = template_count + 1
                y = y + 1
        
            x = x + 1

        elect_template = np.delete(elect_template, 0, 1)
        elect_template = np.delete(elect_template, 6, 1)
        elect_template = np.delete(elect_template, 54, 1)
        elect_template = np.delete(elect_template, 60, 1)

        plt.plot(elect_template[0, :], elect_template[1, :], 'ko', markerfacecolor='none')
        plt.xlim([0, 9])
        plt.ylim([0, 9])
        plt.show()
        
    color_change = len(prop_order[0]) / 6
    color_change = round(color_change)
    color_choice = ['blue', 'cyan', 'green', 'yellow', 'orange', 'red']

    prop_num_max = len(prop_order[0]) - 1
    prop_num = 0

    while prop_num < prop_num_max:
        if prop_num <= color_change:
            color = color_choice[0]
        elif prop_num > color_change and prop_num <= 2 * color_change:
            color = color_choice[1]
        elif prop_num > 2 * color_change and prop_num <= 3 * color_change:
            color = color_choice[2]
        elif prop_num > 3 * color_change and prop_num <= 4 * color_change:
            color = color_choice[3]
        elif prop_num > 4 * color_change and prop_num <= 5 * color_change:
            color = color_choice[4]
        elif prop_num > 5 * color_change and prop_num <= 6 * color_change:
            color = color_choice[5]
            
        plt.plot(((prop_order[1, prop_num]), (prop_order[1, prop_num + 1])), ((prop_order[0, prop_num]), (prop_order[0, prop_num + 1])), color, linewidth = 0.5)
        prop_num = prop_num + 1
    electrode_template()
    plt.show()
