"""
Calculating lengths of fiber optic cables
Author Adam Kapala
version Alpha
receiver sensitivity needs to be updated/add GUI
"""


import math

# create a table with keys and data

# ask about the type of connection on point A

# ask about the length of connection

# patching points number - by default 2

# ask about the type of connection on point B

file_dictionary = {'overview': 'overview.txt', 'maximum_distance': 'maximum_distance.txt'}

# Attentuation table with average optical fiber losses for multimode in dB/km
multimode_attentuation_dB = {'850': 3, '1300': 1}

# Attentuation table with average optical fiber losses for multimode in dB/km
singlemode_attentuation_dB = {'1310': 0.3, '1550': 0.2}

# Initial global parameters

optical_output_power_dBM = 0
receiver_sensitivity_dBM = 0
receiver_saturation_dBM = 0
power_budget_total = 0
losses_total = 0
net_budget_total = 0
Connector_Loss_dB = 0.5
Splice_Loss_db = 0.1
SingleMode = False
MultiMode = False
SafetyMargin = 3

# Function to search inside dictionary
def item_searching(item_required, item_list):
    # List of files, need to be created
    item = None
    if item_required in item_list :              # Checking if the key is in the dictionary
        item = item_list.get(item_required)      # Get item by key
    else:
        print("Error")
    return item

# Converting average value to peak

def convert_avg_to_peak(avg):

    peak = avg + 3

    return peak


# Converting peak to average value

def convert_peak_to_avg(peak):

    avg = peak - 3

    return avg


# Calculating power budget

def power_budget_calculation(output_power, receiver_sensitivity):

    power_budget = output_power - receiver_sensitivity
    print("Your power budget is: ", power_budget)
    return power_budget


# Calculating net optical power budget

def net_optical_power_budget(power_budget, power_losses):

    net_power_budget = power_budget - power_losses
    print("Your net power budget is: ", net_power_budget)
    return net_power_budget

# Multimode or single mode
def mode_select() :

    global SingleMode
    global MultiMode

    mode = int(input("What is the type of the fiber?\n"
                 "1 = Single Mode\n"
                 "2 = MultiMode\n"))

    if mode is 1:
        SingleMode = True
        MultiMode = False

    elif mode is 2:

        MultiMode = True
        SingleMode = False

    else:
        print("Wrong input")

    return None

# Calculating optical loss
def optical_loss_calculation(length, attentuation_local, splices=2, connectors=2):

    loss = (length * attentuation_local) + (splices * Splice_Loss_db) + (connectors * Connector_Loss_dB)
    total_loss = loss + SafetyMargin
    return total_loss

# ############################################################################################################
# This is actual code for the program with choices and menus
#

  # Call to write overview
file_opened = open(item_searching('overview',file_dictionary))                # Open file to file_opened object
contents = file_opened.read()                                                 # Read object to contents
print(contents)                                                               # Print contents

optical_output_power_dBM = int(input("What is power of your output?\n"))
receiver_sensitivity_dBM = int(input("What is your receiver sensitivity?\n"))


mode_select()

if SingleMode is True:
    attentuation = item_searching(input("What is the wavelength? 1310 Or 1550nm?\n"), singlemode_attentuation_dB)
elif MultiMode is True :
    attentuation = item_searching(input("What is the wavelength? 850 Or 1300nm?\n"), multimode_attentuation_dB)
else :
    attentuation = 0.2
    print("Something went wrong with wavelength\n")


length_of_connection = int(input("What is the length of connection in KM?\n"))


number_of_splices = int(input("How many splices?\n"
                              "Default is 2"))


number_of_connectors = int(input("How many connectors?\n"
                                 "Default is 2"))

print("Optical loss on the length "+str(length_of_connection)+" km is :")
losses_total = optical_loss_calculation(length_of_connection, attentuation, number_of_splices, number_of_connectors)
print(losses_total)

power_budget_total = power_budget_calculation(optical_output_power_dBM, receiver_sensitivity_dBM)


net_budget_total = net_optical_power_budget(power_budget_total, losses_total)
