# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 10:00:08 2024

@author: nikit
"""
######## FILTERING ############################################################

# # Define the run number that you want to filter by
# # specific_values = ['value1', 'value2']
# run_number = [5000]

# # Filter the DataFrame and access following columns:
# # REPORT-INFORMED-INDIVIDUALS, [run number]
# filtered_column_B = data[data['[run number]'].isin(run_number)][['REPORT-INFORMED-INDIVIDUALS' , '[run number]']]

# print(filtered_column_B)

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'       # Set font family
# plt.rcParams['font.size'] = 12             # Set font size
# plt.rcParams['font.weight'] = 'bold'       # Set font weight
import pandas as pd
import seaborn as sns


###############################################################################
######## EXPERIMENT 1 #########################################################
###############################################################################

# Network type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment1 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 1.csv"

data_experiment1 = pd.read_csv(file_path_experiment1 , delimiter=',' , skiprows=6 , quotechar='"')

# Display the first few rows
print(data_experiment1.head())

# Get a summary of numerical columns
print(data_experiment1.describe())

# Check for missing values
print(data_experiment1.isnull().sum())

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp1 = data_experiment1.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp1 = max_per_run_exp1.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp1.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 1: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp1 = data_experiment1.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp1 = steps_per_run_exp1.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp1.index, mean_nr_steps_per_reach_exp1.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 1: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp1 = data_experiment1.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp1 = mean_trans_rate_per_run_exp1.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp1.index, mean_trans_rate_per_reach_exp1.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 1: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 2 #########################################################
###############################################################################

# Network type: Circle
# Source Reach: 20
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment2 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 2.csv"

data_experiment2 = pd.read_csv(file_path_experiment2 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp2 = data_experiment2.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp2 = max_per_run_exp2.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp2.index, mean_max_per_weight_exp2.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 2: Information Coverage as a Function of Weight [Network: Circle, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp2 = data_experiment2.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp2 = steps_per_run_exp2.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp2.index, mean_nr_steps_per_weight_exp2.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 2: Speed as a Function of Weight [Network: Circle, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp2 = data_experiment2.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp2 = mean_trans_rate_per_run_exp2.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp2.index, mean_trans_rate_per_weight_exp2.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 2: Transmission Rate as a Function of Weight [Network: Circle, Source Reach: 20]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 3 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Lower Weight Limit: 0.2
# Upper Weight Limit: 0.8

######## DATA IMPORT ##########################################################

file_path_experiment3 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 3.csv"

data_experiment3 = pd.read_csv(file_path_experiment3 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp3 = data_experiment3.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp3 = max_per_run_exp3.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp3.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 3: Information Coverage as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp3 = data_experiment3.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp3 = steps_per_run_exp3.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp3.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 3: Speed as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp3 = data_experiment3.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp3 = mean_trans_rate_per_run_exp3.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp3.index, mean_trans_rate_per_reach_exp3.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 3: Transmission Rate as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 4 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.4

######## DATA IMPORT ##########################################################

file_path_experiment4 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 4.csv"

data_experiment4 = pd.read_csv(file_path_experiment4 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp4 = data_experiment4.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp4 = max_per_run_exp4.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp4.index, mean_max_per_reach_exp4.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 4: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.4]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp4 = data_experiment4.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp4 = steps_per_run_exp4.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp4.index, mean_nr_steps_per_reach_exp4.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 4: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.4]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp4 = data_experiment4.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp4 = mean_trans_rate_per_run_exp4.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp4.index, mean_trans_rate_per_reach_exp4.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 4: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.4]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 5 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.3

######## DATA IMPORT ##########################################################

file_path_experiment5 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 5.csv"

data_experiment5 = pd.read_csv(file_path_experiment5 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp5 = data_experiment5.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp5 = max_per_run_exp5.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp5.index, mean_max_per_reach_exp5.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 5: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp5 = data_experiment5.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp5 = steps_per_run_exp5.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp5.index, mean_nr_steps_per_reach_exp5.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 5: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp5 = data_experiment5.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp5 = mean_trans_rate_per_run_exp5.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp5.index, mean_trans_rate_per_reach_exp5.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 5: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 6 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.2

######## DATA IMPORT ##########################################################

file_path_experiment6 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 6.csv"

data_experiment6 = pd.read_csv(file_path_experiment6 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp6 = data_experiment6.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp6 = max_per_run_exp6.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp6.index, mean_max_per_reach_exp6.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 6: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.2]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp6 = data_experiment6.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp6 = steps_per_run_exp6.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp6.index, mean_nr_steps_per_reach_exp6.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 6: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.2]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp6 = data_experiment6.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp6 = mean_trans_rate_per_run_exp6.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp6.index, mean_trans_rate_per_reach_exp6.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 6: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.2]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 7 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.1

######## DATA IMPORT ##########################################################

file_path_experiment7 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 7.csv"

data_experiment7 = pd.read_csv(file_path_experiment7 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp7 = data_experiment7.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp7 = max_per_run_exp7.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp7.index, mean_max_per_reach_exp7.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 7: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp7 = data_experiment7.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp7 = steps_per_run_exp7.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp7.index, mean_nr_steps_per_reach_exp7.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 7: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp7 = data_experiment7.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp7 = mean_trans_rate_per_run_exp7.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp7.index, mean_trans_rate_per_reach_exp7.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 7: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 8 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.6

######## DATA IMPORT ##########################################################

file_path_experiment8 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 8.csv"

data_experiment8 = pd.read_csv(file_path_experiment8 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp8 = data_experiment8.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp8 = max_per_run_exp8.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp8.index, mean_max_per_reach_exp8.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 8: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.6]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp8 = data_experiment8.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp8 = steps_per_run_exp8.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp8.index, mean_nr_steps_per_reach_exp8.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 8: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.6]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp8 = data_experiment8.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp8 = mean_trans_rate_per_run_exp8.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp8.index, mean_trans_rate_per_reach_exp8.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 8: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.6]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 9 #########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.9

######## DATA IMPORT ##########################################################

file_path_experiment9 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 9.csv"

data_experiment9 = pd.read_csv(file_path_experiment9 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp9 = data_experiment9.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp9 = max_per_run_exp9.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp9.index, mean_max_per_reach_exp9.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 9: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp9 = data_experiment9.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp9 = steps_per_run_exp9.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp9.index, mean_nr_steps_per_reach_exp9.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 9: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp9 = data_experiment9.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp9 = mean_trans_rate_per_run_exp9.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp9.index, mean_trans_rate_per_reach_exp9.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 9: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 10 ########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Lower Weight Limit: 0.2
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment10 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 10.csv"

data_experiment10 = pd.read_csv(file_path_experiment10 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp10 = data_experiment10.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp10 = max_per_run_exp10.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp10.index, mean_max_per_reach_exp10.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 10: Information Coverage as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.2 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp10 = data_experiment10.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp10 = steps_per_run_exp10.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp10.index, mean_nr_steps_per_reach_exp10.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 10: Speed as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.2 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp10 = data_experiment10.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp10 = mean_trans_rate_per_run_exp10.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp10.index, mean_trans_rate_per_reach_exp10.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 10: Transmission Rate as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.2 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 11 ########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment11 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 11.csv"

data_experiment11 = pd.read_csv(file_path_experiment11 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp11 = data_experiment11.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp11 = max_per_run_exp11.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp11.index, mean_max_per_reach_exp11.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 11: Information Coverage as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp11 = data_experiment11.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp11 = steps_per_run_exp11.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp11.index, mean_nr_steps_per_reach_exp11.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 11: Speed as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp11 = data_experiment11.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp11 = mean_trans_rate_per_run_exp11.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp11.index, mean_trans_rate_per_reach_exp11.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 11: Transmission Rate as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 12 ########################################################
###############################################################################

# Network type: Circle
# Source Reach: 1
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment12 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 12.csv"

data_experiment12 = pd.read_csv(file_path_experiment12 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp12 = data_experiment12.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp12 = max_per_run_exp12.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp12.index, mean_max_per_weight_exp12.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 12: Information Coverage as a Function of Weight [Network: Circle, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp12 = data_experiment12.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp12 = steps_per_run_exp12.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp12.index, mean_nr_steps_per_weight_exp12.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 12: Speed as a Function of Weight [Network: Circle, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp12 = data_experiment12.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp12 = mean_trans_rate_per_run_exp12.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp12.index, mean_trans_rate_per_weight_exp12.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 12: Transmission Rate as a Function of Weight [Network: Circle, Source Reach: 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 13 ########################################################
###############################################################################

# Network type: Circle
# Source Reach: 5
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment13 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 13.csv"

data_experiment13 = pd.read_csv(file_path_experiment13 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp13 = data_experiment13.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp13 = max_per_run_exp13.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp13.index, mean_max_per_weight_exp13.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 13: Information Coverage as a Function of Weight [Network: Circle, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp13 = data_experiment13.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp13 = steps_per_run_exp13.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp13.index, mean_nr_steps_per_weight_exp13.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 13: Speed as a Function of Weight [Network: Circle, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp13 = data_experiment13.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp13 = mean_trans_rate_per_run_exp13.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp13.index, mean_trans_rate_per_weight_exp13.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 13: Transmission Rate as a Function of Weight [Network: Circle, Source Reach: 5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 14 ########################################################
###############################################################################

# Network type: Circle
# Source Reach: 10
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment14 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 14.csv"

data_experiment14 = pd.read_csv(file_path_experiment14 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp14 = data_experiment14.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp14 = max_per_run_exp14.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp14.index, mean_max_per_weight_exp14.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 14: Information Coverage as a Function of Weight [Network: Circle, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp14 = data_experiment14.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp14 = steps_per_run_exp14.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp14.index, mean_nr_steps_per_weight_exp14.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 14: Speed as a Function of Weight [Network: Circle, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp14 = data_experiment14.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp14 = mean_trans_rate_per_run_exp14.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp14.index, mean_trans_rate_per_weight_exp14.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 14: Transmission Rate as a Function of Weight [Network: Circle, Source Reach: 10]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 15 ########################################################
###############################################################################

# Network type: Circle
# Source Reach: 30
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment15 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 15.csv"

data_experiment15 = pd.read_csv(file_path_experiment15 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp15 = data_experiment15.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp15 = max_per_run_exp15.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp15.index, mean_max_per_weight_exp15.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 15: Information Coverage as a Function of Weight [Network: Circle, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp15 = data_experiment15.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp15 = steps_per_run_exp15.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp15.index, mean_nr_steps_per_weight_exp15.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 15: Speed as a Function of Weight [Network: Circle, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp15 = data_experiment15.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp15 = mean_trans_rate_per_run_exp15.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp15.index, mean_trans_rate_per_weight_exp15.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 15: Transmission Rate as a Function of Weight [Network: Circle, Source Reach: 30]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 16 ########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Lower Weight Limit: 0.3
# Upper Weight Limit: 0.6

######## DATA IMPORT ##########################################################

file_path_experiment16 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 16.csv"

data_experiment16 = pd.read_csv(file_path_experiment16 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp16 = data_experiment16.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp16 = max_per_run_exp16.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp16.index, mean_max_per_reach_exp16.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 16: Information Coverage as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp16 = data_experiment16.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp16 = steps_per_run_exp16.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp16.index, mean_nr_steps_per_reach_exp16.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 16: Speed as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp16 = data_experiment16.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp16 = mean_trans_rate_per_run_exp16.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp16.index, mean_trans_rate_per_reach_exp16.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 16: Transmission Rate as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 17 ########################################################
###############################################################################

# Network type: Royal Family
# Source Reach: Central node
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment17 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 17.csv"

data_experiment17 = pd.read_csv(file_path_experiment17 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp17 = data_experiment17.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp17 = max_per_run_exp17.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp17.index, mean_max_per_weight_exp17.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp17 = data_experiment17.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp17 = steps_per_run_exp17.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp17.index, mean_nr_steps_per_weight_exp17.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp17 = data_experiment17.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp17 = mean_trans_rate_per_run_exp17.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp17.index, mean_trans_rate_per_weight_exp17.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.grid(True)
plt.show()



###############################################################################
######## ROYAL FAMILY (Exp. 18, 19, 20, 21, 22, 25) ###########################
###############################################################################

# Network type: Royal Family
# Source Reach: Central node
# Weight: Different upper and lower limits on the otherwise random weight
# (0.2-0.8, 0.2-1, 0-1, 0.3-0.6, 0.5-1, 0-0.5)

######## DATA IMPORT ##########################################################

file_path_experiment18 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 18.csv"

data_experiment18 = pd.read_csv(file_path_experiment18 , delimiter=',' , skiprows=6 , quotechar='"')

file_path_experiment19 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 19.csv"

data_experiment19 = pd.read_csv(file_path_experiment19 , delimiter=',' , skiprows=6 , quotechar='"')

file_path_experiment20 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 20.csv"

data_experiment20 = pd.read_csv(file_path_experiment20 , delimiter=',' , skiprows=6 , quotechar='"')

file_path_experiment21 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 21.csv"

data_experiment21 = pd.read_csv(file_path_experiment21 , delimiter=',' , skiprows=6 , quotechar='"')

file_path_experiment22 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 22.csv"

data_experiment22 = pd.read_csv(file_path_experiment22 , delimiter=',' , skiprows=6 , quotechar='"')

file_path_experiment25 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 25.csv"

data_experiment25 = pd.read_csv(file_path_experiment25 , delimiter=',' , skiprows=6 , quotechar='"')

# Merge the individual data from the experiments into one dataframe through vertical stacking
data_experimentROYALFAMILY = pd.concat([data_experiment18, 
                                        data_experiment19, 
                                        data_experiment20,
                                        data_experiment21,
                                        data_experiment22,
                                        data_experiment25], ignore_index=True)
data_experimentROYALFAMILY['weight setting'] = data_experimentROYALFAMILY['lower-limit-weight'].astype(str) + "-" + data_experimentROYALFAMILY['upper-limit-weight'].astype(str)

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per weight setting
max_per_run_expROYALFAMILY = data_experimentROYALFAMILY.groupby(['[run number]', 'weight setting'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Plotting
# This box plot shows the Information Coverage for the Royal Family-Network for different parameters of variable weight
plt.figure(figsize=(16, 10))
sns.boxplot(data=max_per_run_expROYALFAMILY, 
            x='weight setting', 
            y='REPORT-INFORMED-INDIVIDUALS',
            palette='Set2', 
            width=0.5,
            showmeans=True, 
            meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Variable Weight', 
           fontsize=14)
plt.ylabel('Information Coverage', 
           fontsize=14)
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each run
steps_per_run_expROYALFAMILY = data_experimentROYALFAMILY.groupby(['[run number]', 'weight setting'])['[step]'].max().reset_index()

# Plotting
# This box plot shows the Speed for the Royal Family-Network for different parameters of variable weight
plt.figure(figsize=(16, 10))
sns.boxplot(data=steps_per_run_expROYALFAMILY, 
            x='weight setting', 
            y='[step]',
            palette='Set2', 
            width=0.5,
            showmeans=True, 
            meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Variable Weight', 
           fontsize=14)
plt.ylabel('Nr of Steps (Inverse Speed)', 
           fontsize=14)
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_expROYALFAMILY = data_experimentROYALFAMILY.groupby(['[run number]', 'weight setting'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Plotting
# This box plot shows the Transmission Rate for the Royal Family-Network for different parameters of variable weight
plt.figure(figsize=(16, 10))
sns.boxplot(data=mean_trans_rate_per_run_expROYALFAMILY, 
            x='weight setting', 
            y='REPORT-AVERAGE-TRANSMISSION-RATE',
            palette='Set2', 
            width=0.5,
            showmeans=True, 
            meanprops={"marker": "o", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Variable Weight', 
           fontsize=14)
plt.ylabel('Avg Transmission Rate per Cycle', 
           fontsize=14)
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()



###############################################################################
######## EXPERIMENT 23 ########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Lower Weight Limit: 0.5
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment23 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 23.csv"

data_experiment23 = pd.read_csv(file_path_experiment23 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp23 = data_experiment23.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp23 = max_per_run_exp23.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp23.index, mean_max_per_reach_exp23.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 23: Information Coverage as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp23 = data_experiment23.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp23 = steps_per_run_exp23.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp23.index, mean_nr_steps_per_reach_exp23.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 23: Speed as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp23 = data_experiment23.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp23 = mean_trans_rate_per_run_exp23.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp23.index, mean_trans_rate_per_reach_exp23.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 23: Transmission Rate as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 24 ########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment24 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 24.csv"

data_experiment24 = pd.read_csv(file_path_experiment24 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp24 = data_experiment24.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp24 = max_per_run_exp24.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp24.index, mean_max_per_reach_exp24.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 24: Information Coverage as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp24 = data_experiment24.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp24 = steps_per_run_exp24.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp24.index, mean_nr_steps_per_reach_exp24.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 24: Speed as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp24 = data_experiment24.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp24 = mean_trans_rate_per_run_exp24.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp24.index, mean_trans_rate_per_reach_exp24.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 24: Transmission Rate as a Function of Source Reach [Network: Circle, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 26 ########################################################
###############################################################################

# Network type: Fully connected
# Source Reach: 1-100
# Uniform Weight: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment26 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 26.csv"

data_experiment26 = pd.read_csv(file_path_experiment26 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp26 = data_experiment26.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp26 = max_per_run_exp26.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp26.index, mean_max_per_reach_exp26.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 26: Information Coverage as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp26 = data_experiment26.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp26 = steps_per_run_exp26.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp26.index, mean_nr_steps_per_reach_exp26.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 26: Speed as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp26 = data_experiment26.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp26 = mean_trans_rate_per_run_exp26.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp26.index, mean_trans_rate_per_reach_exp26.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 26: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 27 ########################################################
###############################################################################

# Network type: Fully connected
# Source Reach: 1-100
# Uniform Weight: 0.1

######## DATA IMPORT ##########################################################

file_path_experiment27 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 27.csv"

data_experiment27 = pd.read_csv(file_path_experiment27 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp27 = data_experiment27.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp27 = max_per_run_exp27.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp27.index, mean_max_per_reach_exp27.values, marker='o', color='b', linestyle='-')
plt.ylim(99.985, 100)
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 27: Information Coverage as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp27 = data_experiment27.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp27 = steps_per_run_exp27.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp27.index, mean_nr_steps_per_reach_exp27.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 27: Speed as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp27 = data_experiment27.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp27 = mean_trans_rate_per_run_exp27.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp27.index, mean_trans_rate_per_reach_exp27.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 27: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 28 ########################################################
###############################################################################

# Network type: Fully connected
# Source Reach: 1-100
# Uniform Weight: 0.9

######## DATA IMPORT ##########################################################

file_path_experiment28 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 28.csv"

data_experiment28 = pd.read_csv(file_path_experiment28 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp28 = data_experiment28.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp28 = max_per_run_exp28.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp28.index, mean_max_per_reach_exp28.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 28: Information Coverage as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp28 = data_experiment28.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp28 = steps_per_run_exp28.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp28.index, mean_nr_steps_per_reach_exp28.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 28: Speed as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp28 = data_experiment28.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp28 = mean_trans_rate_per_run_exp28.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp28.index, mean_trans_rate_per_reach_exp28.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 28: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 29 ########################################################
###############################################################################

# Network Type: Fully Connected
# Source Reach: 1-100
# Lower Weight Limit: 0.2
# Upper Weight Limit: 0.8

######## DATA IMPORT ##########################################################

file_path_experiment29 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 29.csv"

data_experiment29 = pd.read_csv(file_path_experiment29 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp29 = data_experiment29.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp29 = max_per_run_exp29.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp29.index, mean_max_per_reach_exp29.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 29: Information Coverage as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp29 = data_experiment29.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp29 = steps_per_run_exp29.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp29.index, mean_nr_steps_per_reach_exp29.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 29: Speed as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp29 = data_experiment29.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp29 = mean_trans_rate_per_run_exp29.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp29.index, mean_trans_rate_per_reach_exp29.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 29: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 30 ########################################################
###############################################################################

# Network Type: Fully Connected
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment30 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 30.csv"

data_experiment30 = pd.read_csv(file_path_experiment30 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp30 = data_experiment30.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp30 = max_per_run_exp30.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp30.index, mean_max_per_reach_exp30.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 30: Information Coverage as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp30 = data_experiment30.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp30 = steps_per_run_exp30.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp30.index, mean_nr_steps_per_reach_exp30.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 30: Speed as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp30 = data_experiment30.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp30 = mean_trans_rate_per_run_exp30.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp30.index, mean_trans_rate_per_reach_exp30.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 30: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 31 ########################################################
###############################################################################

# Network Type: Fully Connected
# Source Reach: 1-100
# Lower Weight Limit: 0.5
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment31 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 31.csv"

data_experiment31 = pd.read_csv(file_path_experiment31 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp31 = data_experiment31.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp31 = max_per_run_exp31.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp31.index, mean_max_per_reach_exp31.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 31: Information Coverage as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp31 = data_experiment31.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp31 = steps_per_run_exp31.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp31.index, mean_nr_steps_per_reach_exp31.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 31: Speed as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp31 = data_experiment31.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp31 = mean_trans_rate_per_run_exp31.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp31.index, mean_trans_rate_per_reach_exp31.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 31: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 32 ########################################################
###############################################################################

# Network type: Fully Connected
# Source Reach: 20
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment32 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 32.csv"

data_experiment32 = pd.read_csv(file_path_experiment32 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp32 = data_experiment32.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp32 = max_per_run_exp32.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp32.index, mean_max_per_weight_exp32.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 32: Information Coverage as a Function of Weight [Network: Fully Connected, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp32 = data_experiment32.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp32 = steps_per_run_exp32.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp32.index, mean_nr_steps_per_weight_exp32.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 32: Speed as a Function of Weight [Network: Fully Connected, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp32 = data_experiment32.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp32 = mean_trans_rate_per_run_exp32.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp32.index, mean_trans_rate_per_weight_exp32.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 32: Transmission Rate as a Function of Weight [Network: Fully Connected, Source Reach: 20]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 33 ########################################################
###############################################################################

# Network type: Fully Connected
# Source Reach: 1
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment33 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 33.csv"

data_experiment33 = pd.read_csv(file_path_experiment33 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp33 = data_experiment33.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp33 = max_per_run_exp33.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp33.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 33: Information Coverage as a Function of Weight [Network: Fully Connected, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp33 = data_experiment33.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp33 = steps_per_run_exp33.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp33.index, mean_nr_steps_per_weight_exp33.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 33: Speed as a Function of Weight [Network: Fully Connected, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp33 = data_experiment33.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp33 = mean_trans_rate_per_run_exp33.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp33.index, mean_trans_rate_per_weight_exp33.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 33: Transmission Rate as a Function of Weight [Network: Fully Connected, Source Reach: 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 34 ########################################################
###############################################################################

# Network type: Fully Connected
# Source Reach: 5
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment34 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 34.csv"

data_experiment34 = pd.read_csv(file_path_experiment34 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp34 = data_experiment34.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp34 = max_per_run_exp34.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp34.index, mean_max_per_weight_exp34.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 34: Information Coverage as a Function of Weight [Network: Fully Connected, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp34 = data_experiment34.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp34 = steps_per_run_exp34.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp34.index, mean_nr_steps_per_weight_exp34.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 34: Speed as a Function of Weight [Network: Fully Connected, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp34 = data_experiment34.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp34 = mean_trans_rate_per_run_exp34.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp34.index, mean_trans_rate_per_weight_exp34.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 34: Transmission Rate as a Function of Weight [Network: Fully Connected, Source Reach: 5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 35 ########################################################
###############################################################################

# Network type: Fully Connected
# Source Reach: 10
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment35 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 35.csv"

data_experiment35 = pd.read_csv(file_path_experiment35 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp35 = data_experiment35.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp35 = max_per_run_exp35.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp35.index, mean_max_per_weight_exp35.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 35: Information Coverage as a Function of Weight [Network: Fully Connected, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp35 = data_experiment35.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp35 = steps_per_run_exp35.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp35.index, mean_nr_steps_per_weight_exp35.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 35: Speed as a Function of Weight [Network: Fully Connected, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp35 = data_experiment35.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp35 = mean_trans_rate_per_run_exp35.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp35.index, mean_trans_rate_per_weight_exp35.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 35: Transmission Rate as a Function of Weight [Network: Fully Connected, Source Reach: 10]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 36 ########################################################
###############################################################################

# Network type: Fully Connected
# Source Reach: 30
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment36 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 36.csv"

data_experiment36 = pd.read_csv(file_path_experiment36 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp36 = data_experiment36.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp36 = max_per_run_exp36.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp36.index, mean_max_per_weight_exp36.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 36: Information Coverage as a Function of Weight [Network: Fully Connected, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp36 = data_experiment36.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp36 = steps_per_run_exp36.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp36.index, mean_nr_steps_per_weight_exp36.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 36: Speed as a Function of Weight [Network: Fully Connected, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp36 = data_experiment36.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp36 = mean_trans_rate_per_run_exp36.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp36.index, mean_trans_rate_per_weight_exp36.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 36: Transmission Rate as a Function of Weight [Network: Fully Connected, Source Reach: 30]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 37 ########################################################
###############################################################################

# Network type: Fully Connected
# Source Reach: 50
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment37 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 37.csv"

data_experiment37 = pd.read_csv(file_path_experiment37 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp37 = data_experiment37.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp37 = max_per_run_exp37.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp37.index, mean_max_per_weight_exp37.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 37: Information Coverage as a Function of Weight [Network: Fully Connected, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp37 = data_experiment37.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp37 = steps_per_run_exp37.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp37.index, mean_nr_steps_per_weight_exp37.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 37: Speed as a Function of Weight [Network: Fully Connected, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp37 = data_experiment37.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp37 = mean_trans_rate_per_run_exp37.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp37.index, mean_trans_rate_per_weight_exp37.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 37: Transmission Rate as a Function of Weight [Network: Fully Connected, Source Reach: 50]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 38 ########################################################
###############################################################################

# Network Type: Fully Connected
# Source Reach: 1-100
# Lower Weight Limit: 0.3
# Upper Weight Limit: 0.6

######## DATA IMPORT ##########################################################

file_path_experiment38 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 38.csv"

data_experiment38 = pd.read_csv(file_path_experiment38 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp38 = data_experiment38.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp38 = max_per_run_exp38.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp38.index, mean_max_per_reach_exp38.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 38: Information Coverage as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp38 = data_experiment38.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp38 = steps_per_run_exp38.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp38.index, mean_nr_steps_per_reach_exp38.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 38: Speed as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp38 = data_experiment38.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp38 = mean_trans_rate_per_run_exp38.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp38.index, mean_trans_rate_per_reach_exp38.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 38: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 39 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 1-100
# Uniform Weight: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment39 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 39.csv"

data_experiment39 = pd.read_csv(file_path_experiment39 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp39 = data_experiment39.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp39 = max_per_run_exp39.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp39.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 39: Information Coverage as a Function of Source Reach [Network: Star, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp39 = data_experiment39.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp39 = steps_per_run_exp39.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp39.index, mean_nr_steps_per_reach_exp39.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 39: Speed as a Function of Source Reach [Network: Star, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp39 = data_experiment39.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp39 = mean_trans_rate_per_run_exp39.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp39.index, mean_trans_rate_per_reach_exp39.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 39: Transmission Rate as a Function of Source Reach [Network: Star, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 40 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 1-100
# Uniform Weight: 0.1

######## DATA IMPORT ##########################################################

file_path_experiment40 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 40.csv"

data_experiment40 = pd.read_csv(file_path_experiment40 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp40 = data_experiment40.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp40 = max_per_run_exp40.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp40.index, mean_max_per_reach_exp40.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 40: Information Coverage as a Function of Source Reach [Network: Star, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp40 = data_experiment40.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp40 = steps_per_run_exp40.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp40.index, mean_nr_steps_per_reach_exp40.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 40: Speed as a Function of Source Reach [Network: Star, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp40 = data_experiment40.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp40 = mean_trans_rate_per_run_exp40.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp40.index, mean_trans_rate_per_reach_exp40.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 40: Transmission Rate as a Function of Source Reach [Network: Star, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 41 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 1-100
# Uniform Weight: 0.9

######## DATA IMPORT ##########################################################

file_path_experiment41 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 41.csv"

data_experiment41 = pd.read_csv(file_path_experiment41 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp41 = data_experiment41.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp41 = max_per_run_exp41.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp41.index, mean_max_per_reach_exp41.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 41: Information Coverage as a Function of Source Reach [Network: Star, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp41 = data_experiment41.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp41 = steps_per_run_exp41.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp41.index, mean_nr_steps_per_reach_exp41.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 41: Speed as a Function of Source Reach [Network: Star, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp41 = data_experiment41.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp41 = mean_trans_rate_per_run_exp41.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp41.index, mean_trans_rate_per_reach_exp41.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 41: Transmission Rate as a Function of Source Reach [Network: Star, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 42 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 20
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment42 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 42.csv"

data_experiment42 = pd.read_csv(file_path_experiment42 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp42 = data_experiment42.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp42 = max_per_run_exp42.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp42.index, mean_max_per_weight_exp42.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 42: Information Coverage as a Function of Weight [Network: Star, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp42 = data_experiment42.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp42 = steps_per_run_exp42.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp42.index, mean_nr_steps_per_weight_exp42.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 42: Speed as a Function of Weight [Network: Star, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp42 = data_experiment42.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp42 = mean_trans_rate_per_run_exp42.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp42.index, mean_trans_rate_per_weight_exp42.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 42: Transmission Rate as a Function of Weight [Network: Star, Source Reach: 20]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 43 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 1
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment43 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 43.csv"

data_experiment43 = pd.read_csv(file_path_experiment43 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp43 = data_experiment43.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp43 = max_per_run_exp43.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp43.index, mean_max_per_weight_exp43.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 43: Information Coverage as a Function of Weight [Network: Star, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp43 = data_experiment43.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp43 = steps_per_run_exp43.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp43.index, mean_nr_steps_per_weight_exp43.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 43: Speed as a Function of Weight [Network: Star, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp43 = data_experiment43.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp43 = mean_trans_rate_per_run_exp43.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp43.index, mean_trans_rate_per_weight_exp43.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 43: Transmission Rate as a Function of Weight [Network: Star, Source Reach: 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 44 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 5
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment44 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 44.csv"

data_experiment44 = pd.read_csv(file_path_experiment44 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp44 = data_experiment44.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp44 = max_per_run_exp44.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp44.index, mean_max_per_weight_exp44.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 44: Information Coverage as a Function of Weight [Network: Star, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp44 = data_experiment44.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp44 = steps_per_run_exp44.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp44.index, mean_nr_steps_per_weight_exp44.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 44: Speed as a Function of Weight [Network: Star, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp44 = data_experiment44.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp44 = mean_trans_rate_per_run_exp44.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp44.index, mean_trans_rate_per_weight_exp44.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 44: Transmission Rate as a Function of Weight [Network: Star, Source Reach: 5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 45 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 30
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment45 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 45.csv"

data_experiment45 = pd.read_csv(file_path_experiment45 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp45 = data_experiment45.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp45 = max_per_run_exp45.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp45.index, mean_max_per_weight_exp45.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 45: Information Coverage as a Function of Weight [Network: Star, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp45 = data_experiment45.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp45 = steps_per_run_exp45.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp45.index, mean_nr_steps_per_weight_exp45.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 45: Speed as a Function of Weight [Network: Star, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp45 = data_experiment45.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp45 = mean_trans_rate_per_run_exp45.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp45.index, mean_trans_rate_per_weight_exp45.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 45: Transmission Rate as a Function of Weight [Network: Star, Source Reach: 30]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 46 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 1-100
# Uniform Weight: 0.3

######## DATA IMPORT ##########################################################

file_path_experiment46 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 46.csv"

data_experiment46 = pd.read_csv(file_path_experiment46 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp46 = data_experiment46.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp46 = max_per_run_exp46.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp46.index, mean_max_per_reach_exp46.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 46: Information Coverage as a Function of Source Reach [Network: Star, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp46 = data_experiment46.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp46 = steps_per_run_exp46.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp46.index, mean_nr_steps_per_reach_exp46.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 46: Speed as a Function of Source Reach [Network: Star, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp46 = data_experiment46.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp46 = mean_trans_rate_per_run_exp46.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp46.index, mean_trans_rate_per_reach_exp46.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 46: Transmission Rate as a Function of Source Reach [Network: Star, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 47 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 1-100
# Uniform Weight: 0.7

######## DATA IMPORT ##########################################################

file_path_experiment47 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 47.csv"

data_experiment47 = pd.read_csv(file_path_experiment47 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp47 = data_experiment47.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp47 = max_per_run_exp47.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp47.index, mean_max_per_reach_exp47.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 47: Information Coverage as a Function of Source Reach [Network: Star, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp47 = data_experiment47.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp47 = steps_per_run_exp47.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp47.index, mean_nr_steps_per_reach_exp47.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 47: Speed as a Function of Source Reach [Network: Star, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp47 = data_experiment47.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp47 = mean_trans_rate_per_run_exp47.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp47.index, mean_trans_rate_per_reach_exp47.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 47: Transmission Rate as a Function of Source Reach [Network: Star, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 48 ########################################################
###############################################################################

# Network Type: Star
# Source Reach: 1-100
# Lower Weight Limit: 0.2
# Upper Weight Limit: 0.8

######## DATA IMPORT ##########################################################

file_path_experiment48 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 48.csv"

data_experiment48 = pd.read_csv(file_path_experiment48 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp48 = data_experiment48.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp48 = max_per_run_exp48.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp48.index, mean_max_per_reach_exp48.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 48: Information Coverage as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp48 = data_experiment48.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp48 = steps_per_run_exp48.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp48.index, mean_nr_steps_per_reach_exp48.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 48: Speed as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp48 = data_experiment48.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp48 = mean_trans_rate_per_run_exp48.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp48.index, mean_trans_rate_per_reach_exp48.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 48: Transmission Rate as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 49 ########################################################
###############################################################################

# Network Type: Star
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment49 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 49.csv"

data_experiment49 = pd.read_csv(file_path_experiment49 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp49 = data_experiment49.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp49 = max_per_run_exp49.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp49.index, mean_max_per_reach_exp49.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 49: Information Coverage as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp49 = data_experiment49.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp49 = steps_per_run_exp49.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp49.index, mean_nr_steps_per_reach_exp49.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 49: Speed as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp49 = data_experiment49.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp49 = mean_trans_rate_per_run_exp49.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp49.index, mean_trans_rate_per_reach_exp49.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 49: Transmission Rate as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 50 ########################################################
###############################################################################

# Network Type: Star
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment50 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 50.csv"

data_experiment50 = pd.read_csv(file_path_experiment50 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp50 = data_experiment50.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp50 = max_per_run_exp50.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp50.index, mean_max_per_reach_exp50.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 50: Information Coverage as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp50 = data_experiment50.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp50 = steps_per_run_exp50.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp50.index, mean_nr_steps_per_reach_exp50.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 50: Speed as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp50 = data_experiment50.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp50 = mean_trans_rate_per_run_exp50.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp50.index, mean_trans_rate_per_reach_exp50.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 50: Transmission Rate as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 51 ########################################################
###############################################################################

# Network Type: Star
# Source Reach: 1-100
# Lower Weight Limit: 0.5
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment51 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 51.csv"

data_experiment51 = pd.read_csv(file_path_experiment51 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp51 = data_experiment51.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp51 = max_per_run_exp51.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp51.index, mean_max_per_reach_exp51.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 51: Information Coverage as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp51 = data_experiment51.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp51 = steps_per_run_exp51.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp51.index, mean_nr_steps_per_reach_exp51.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 51: Speed as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp51 = data_experiment51.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp51 = mean_trans_rate_per_run_exp51.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp51.index, mean_trans_rate_per_reach_exp51.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 51: Transmission Rate as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 52 ########################################################
###############################################################################

# Network Type: Star
# Source Reach: 1-100
# Lower Weight Limit: 0.3
# Upper Weight Limit: 0.6

######## DATA IMPORT ##########################################################

file_path_experiment52 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 52.csv"

data_experiment52 = pd.read_csv(file_path_experiment52 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp52 = data_experiment52.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp52 = max_per_run_exp52.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp52.index, mean_max_per_reach_exp52.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 52: Information Coverage as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp52 = data_experiment52.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp52 = steps_per_run_exp52.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp52.index, mean_nr_steps_per_reach_exp52.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 52: Speed as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp52 = data_experiment52.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp52 = mean_trans_rate_per_run_exp52.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp52.index, mean_trans_rate_per_reach_exp52.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 52: Transmission Rate as a Function of Source Reach [Network: Star, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 53 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 1-100
# Uniform Weight: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment53 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 53.csv"

data_experiment53 = pd.read_csv(file_path_experiment53 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp53 = data_experiment53.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp53 = max_per_run_exp53.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp53.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 53: Information Coverage as a Function of Source Reach [Network: Small World, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp53 = data_experiment53.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp53 = steps_per_run_exp53.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp53.index, mean_nr_steps_per_reach_exp53.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 53: Speed as a Function of Source Reach [Network: Small World, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp53 = data_experiment53.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp53 = mean_trans_rate_per_run_exp53.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp53.index, mean_trans_rate_per_reach_exp53.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 53: Transmission Rate as a Function of Source Reach [Network: Small World, Uniform Weight: 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 54 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 1-100
# Uniform Weight: 0.1

######## DATA IMPORT ##########################################################

file_path_experiment54 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 54.csv"

data_experiment54 = pd.read_csv(file_path_experiment54 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp54 = data_experiment54.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp54 = max_per_run_exp54.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp54.index, mean_max_per_reach_exp54.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 54: Information Coverage as a Function of Source Reach [Network: Small World, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp54 = data_experiment54.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp54 = steps_per_run_exp54.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp54.index, mean_nr_steps_per_reach_exp54.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 54: Speed as a Function of Source Reach [Network: Small World, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp54 = data_experiment54.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp54 = mean_trans_rate_per_run_exp54.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp54.index, mean_trans_rate_per_reach_exp54.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 54: Transmission Rate as a Function of Source Reach [Network: Small World, Uniform Weight: 0.1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 55 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 1-100
# Uniform Weight: 0.9

######## DATA IMPORT ##########################################################

file_path_experiment55 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 55.csv"

data_experiment55 = pd.read_csv(file_path_experiment55 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp55 = data_experiment55.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp55 = max_per_run_exp55.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp55.index, mean_max_per_reach_exp55.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 55: Information Coverage as a Function of Source Reach [Network: Small World, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp55 = data_experiment55.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp55 = steps_per_run_exp55.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp55.index, mean_nr_steps_per_reach_exp55.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 55: Speed as a Function of Source Reach [Network: Small World, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp55 = data_experiment55.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp55 = mean_trans_rate_per_run_exp55.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp55.index, mean_trans_rate_per_reach_exp55.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 55: Transmission Rate as a Function of Source Reach [Network: Small World, Uniform Weight: 0.9]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 56 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 1-100
# Uniform Weight: 0.3

######## DATA IMPORT ##########################################################

file_path_experiment56 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 56.csv"

data_experiment56 = pd.read_csv(file_path_experiment56 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp56 = data_experiment56.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp56 = max_per_run_exp56.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp56.index, mean_max_per_reach_exp56.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 56: Information Coverage as a Function of Source Reach [Network: SMall World, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp56 = data_experiment56.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp56 = steps_per_run_exp56.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp56.index, mean_nr_steps_per_reach_exp56.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 56: Speed as a Function of Source Reach [Network: Small World, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp56 = data_experiment56.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp56 = mean_trans_rate_per_run_exp56.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp56.index, mean_trans_rate_per_reach_exp56.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 56: Transmission Rate as a Function of Source Reach [Network: Small World, Uniform Weight: 0.3]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 57 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 1-100
# Uniform Weight: 0.7

######## DATA IMPORT ##########################################################

file_path_experiment57 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 57.csv"

data_experiment57 = pd.read_csv(file_path_experiment57 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp57 = data_experiment57.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp57 = max_per_run_exp57.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the fully connected network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp57.index, mean_max_per_reach_exp57.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 57: Information Coverage as a Function of Source Reach [Network: SMall World, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp57 = data_experiment57.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp57 = steps_per_run_exp57.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp57.index, mean_nr_steps_per_reach_exp57.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 57: Speed as a Function of Source Reach [Network: Small World, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp57 = data_experiment57.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp57 = mean_trans_rate_per_run_exp57.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp57.index, mean_trans_rate_per_reach_exp57.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 57: Transmission Rate as a Function of Source Reach [Network: Small World, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 58 ########################################################
###############################################################################

# Network Type: Small World
# Source Reach: 1-100
# Lower Weight Limit: 0.2
# Upper Weight Limit: 0.8

######## DATA IMPORT ##########################################################

file_path_experiment58 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 58.csv"

data_experiment58 = pd.read_csv(file_path_experiment58 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp58 = data_experiment58.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp58 = max_per_run_exp58.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp58.index, mean_max_per_reach_exp58.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 58: Information Coverage as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp58 = data_experiment58.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp58 = steps_per_run_exp58.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp58.index, mean_nr_steps_per_reach_exp58.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 58: Speed as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp58 = data_experiment58.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp58 = mean_trans_rate_per_run_exp58.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp58.index, mean_trans_rate_per_reach_exp58.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 58: Transmission Rate as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.2 and 0.8]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 59 ########################################################
###############################################################################

# Network Type: Small World
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 0.5

######## DATA IMPORT ##########################################################

file_path_experiment59 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 59.csv"

data_experiment59 = pd.read_csv(file_path_experiment59 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp59 = data_experiment59.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp59 = max_per_run_exp59.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp59.index, mean_max_per_reach_exp59.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 59: Information Coverage as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp59 = data_experiment59.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp59 = steps_per_run_exp59.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp59.index, mean_nr_steps_per_reach_exp59.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 59: Speed as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp59 = data_experiment59.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp59 = mean_trans_rate_per_run_exp59.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp59.index, mean_trans_rate_per_reach_exp59.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 59: Transmission Rate as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0 and 0.5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 60 ########################################################
###############################################################################

# Network Type: Small World
# Source Reach: 1-100
# Lower Weight Limit: 0.5
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment60 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 60.csv"

data_experiment60 = pd.read_csv(file_path_experiment60 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp60 = data_experiment60.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp60 = max_per_run_exp60.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp60.index, mean_max_per_reach_exp60.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 60: Information Coverage as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp60 = data_experiment60.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp60 = steps_per_run_exp60.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp60.index, mean_nr_steps_per_reach_exp60.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 60: Speed as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp60 = data_experiment60.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp60 = mean_trans_rate_per_run_exp60.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp60.index, mean_trans_rate_per_reach_exp60.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 60: Transmission Rate as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.5 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 61 ########################################################
###############################################################################

# Network Type: Small World
# Source Reach: 1-100
# Lower Weight Limit: 0.3
# Upper Weight Limit: 0.6

######## DATA IMPORT ##########################################################

file_path_experiment61 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 61.csv"

data_experiment61 = pd.read_csv(file_path_experiment61 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp61 = data_experiment61.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp61 = max_per_run_exp61.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp61.index, mean_max_per_reach_exp61.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 61: Information Coverage as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp61 = data_experiment61.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp61 = steps_per_run_exp61.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp61.index, mean_nr_steps_per_reach_exp61.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 61: Speed as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp61 = data_experiment61.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp61 = mean_trans_rate_per_run_exp61.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp61.index, mean_trans_rate_per_reach_exp61.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 61: Transmission Rate as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0.3 and 0.6]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 62 ########################################################
###############################################################################

# Network Type: Small World
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment62 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 62.csv"

data_experiment62 = pd.read_csv(file_path_experiment62 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp62 = data_experiment62.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp62 = max_per_run_exp62.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp62.index, mean_max_per_reach_exp62.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 62: Information Coverage as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp62 = data_experiment62.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp62 = steps_per_run_exp62.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp62.index, mean_nr_steps_per_reach_exp62.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 62: Speed as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp62 = data_experiment62.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp62 = mean_trans_rate_per_run_exp62.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp62.index, mean_trans_rate_per_reach_exp62.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 62: Transmission Rate as a Function of Source Reach [Network: Small World, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 63 ########################################################
###############################################################################

# Network Type: Fully Connected
# Source Reach: 1-100
# Lower Weight Limit: 0
# Upper Weight Limit: 1

######## DATA IMPORT ##########################################################

file_path_experiment63 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 63.csv"

data_experiment63 = pd.read_csv(file_path_experiment63 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp63 = data_experiment63.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp63 = max_per_run_exp63.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp63.index, mean_max_per_reach_exp63.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 63: Information Coverage as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp63 = data_experiment63.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp63 = steps_per_run_exp63.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp63.index, mean_nr_steps_per_reach_exp63.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 63: Speed as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp63 = data_experiment63.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp63 = mean_trans_rate_per_run_exp63.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp63.index, mean_trans_rate_per_reach_exp63.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 63: Transmission Rate as a Function of Source Reach [Network: Fully Connected, Weight: Uniformly distributed between 0 and 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 64 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 20
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment64 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 64.csv"

data_experiment64 = pd.read_csv(file_path_experiment64 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp64 = data_experiment64.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp64 = max_per_run_exp64.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp64.index, mean_max_per_weight_exp64.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 64: Information Coverage as a Function of Weight [Network: Small World, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp64 = data_experiment64.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp64 = steps_per_run_exp64.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp64.index, mean_nr_steps_per_weight_exp64.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 64: Speed as a Function of Weight [Network: Small World, Source Reach: 20]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp64 = data_experiment64.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp64 = mean_trans_rate_per_run_exp64.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp64.index, mean_trans_rate_per_weight_exp64.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 64: Transmission Rate as a Function of Weight [Network: Small World, Source Reach: 20]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 65 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 1
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment65 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 65.csv"

data_experiment65 = pd.read_csv(file_path_experiment65 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp65 = data_experiment65.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp65 = max_per_run_exp65.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp65.index, mean_max_per_weight_exp65.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 65: Information Coverage as a Function of Weight [Network: Small World, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp65 = data_experiment65.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp65 = steps_per_run_exp65.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp65.index, mean_nr_steps_per_weight_exp65.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 65: Speed as a Function of Weight [Network: Small World, Source Reach: 1]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp65 = data_experiment65.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp65 = mean_trans_rate_per_run_exp65.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp65.index, mean_trans_rate_per_weight_exp65.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 65: Transmission Rate as a Function of Weight [Network: Small World, Source Reach: 1]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 66 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 5
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment66 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 66.csv"

data_experiment66 = pd.read_csv(file_path_experiment66 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp66 = data_experiment66.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp66 = max_per_run_exp66.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp66.index, mean_max_per_weight_exp66.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 66: Information Coverage as a Function of Weight [Network: Small World, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp66 = data_experiment66.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp66 = steps_per_run_exp66.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp66.index, mean_nr_steps_per_weight_exp66.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 66: Speed as a Function of Weight [Network: Small World, Source Reach: 5]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp66 = data_experiment66.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp66 = mean_trans_rate_per_run_exp66.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp66.index, mean_trans_rate_per_weight_exp66.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 66: Transmission Rate as a Function of Weight [Network: Small World, Source Reach: 5]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 67 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 30
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment67 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 67.csv"

data_experiment67 = pd.read_csv(file_path_experiment67 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp67 = data_experiment67.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp67 = max_per_run_exp67.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp67.index, mean_max_per_weight_exp67.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 67: Information Coverage as a Function of Weight [Network: Small World, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp67 = data_experiment67.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp67 = steps_per_run_exp67.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp66.index, mean_nr_steps_per_weight_exp66.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 67: Speed as a Function of Weight [Network: Small World, Source Reach: 30]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp67 = data_experiment67.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp67 = mean_trans_rate_per_run_exp67.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp67.index, mean_trans_rate_per_weight_exp67.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 67: Transmission Rate as a Function of Weight [Network: Small World, Source Reach: 30]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 68 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 10
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment68 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 68.csv"

data_experiment68 = pd.read_csv(file_path_experiment68 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp68 = data_experiment68.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp68 = max_per_run_exp68.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp68.index, mean_max_per_weight_exp68.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 68: Information Coverage as a Function of Weight [Network: Small World, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp68 = data_experiment68.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp68 = steps_per_run_exp68.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp68.index, mean_nr_steps_per_weight_exp68.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 68: Speed as a Function of Weight [Network: Small World, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp68 = data_experiment68.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp68 = mean_trans_rate_per_run_exp68.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp68.index, mean_trans_rate_per_weight_exp68.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 68: Transmission Rate as a Function of Weight [Network: Small World, Source Reach: 10]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 69 ########################################################
###############################################################################

# Network type: Small World
# Source Reach: 50
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment69 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 69.csv"

data_experiment69 = pd.read_csv(file_path_experiment69 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp69 = data_experiment69.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp69 = max_per_run_exp69.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp69.index, mean_max_per_weight_exp69.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 69: Information Coverage as a Function of Weight [Network: Small World, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp69 = data_experiment69.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp69 = steps_per_run_exp69.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp69.index, mean_nr_steps_per_weight_exp69.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 69: Speed as a Function of Weight [Network: Small World, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp69 = data_experiment69.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp69 = mean_trans_rate_per_run_exp69.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp69.index, mean_trans_rate_per_weight_exp69.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 69: Transmission Rate as a Function of Weight [Network: Small World, Source Reach: 50]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 70 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 10
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment70 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 70.csv"

data_experiment70 = pd.read_csv(file_path_experiment70 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp70 = data_experiment70.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp70 = max_per_run_exp70.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp70.index, mean_max_per_weight_exp70.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 70: Information Coverage as a Function of Weight [Network: Star, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp70 = data_experiment70.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp70 = steps_per_run_exp70.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp70.index, mean_nr_steps_per_weight_exp70.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 70: Speed as a Function of Weight [Network: Star, Source Reach: 10]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp70 = data_experiment70.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp70 = mean_trans_rate_per_run_exp70.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp70.index, mean_trans_rate_per_weight_exp70.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 70: Transmission Rate as a Function of Weight [Network: Star, Source Reach: 10]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 71 ########################################################
###############################################################################

# Network type: Star
# Source Reach: 50
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment71 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 71.csv"

data_experiment71 = pd.read_csv(file_path_experiment71 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp71 = data_experiment71.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp71 = max_per_run_exp71.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp71.index, mean_max_per_weight_exp71.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 71: Information Coverage as a Function of Weight [Network: Star, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp71 = data_experiment71.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp71 = steps_per_run_exp71.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp71.index, mean_nr_steps_per_weight_exp71.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 71: Speed as a Function of Weight [Network: Star, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp71 = data_experiment71.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp71 = mean_trans_rate_per_run_exp71.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp71.index, mean_trans_rate_per_weight_exp71.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 71: Transmission Rate as a Function of Weight [Network: Star, Source Reach: 50]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 72 ########################################################
###############################################################################

# Network Type: Circle
# Source Reach: 1-100
# Uniform Weight: 0.7

######## DATA IMPORT ##########################################################

file_path_experiment72 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 72.csv"

data_experiment72 = pd.read_csv(file_path_experiment72 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Source Reach #################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per source-reach value across runs
max_per_run_exp72 = data_experiment72.groupby(['[run number]', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each source-reach
mean_max_per_reach_exp72 = max_per_run_exp72.groupby('source-reach')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp72.index, mean_max_per_reach_exp72.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 72: Information Coverage as a Function of Source Reach [Network: Circle, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()

######## Speed by Source Reach ################################################

# Calculate the number of steps in each unique run + source-reach combination
steps_per_run_exp72 = data_experiment72.groupby(['[run number]', 'source-reach'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each source-reach
mean_nr_steps_per_reach_exp72 = steps_per_run_exp72.groupby('source-reach')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of source reach. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp72.index, mean_nr_steps_per_reach_exp72.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 72: Speed as a Function of Source Reach [Network: Circle, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()

######## Transmission Rate by Source Reach ####################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp72 = data_experiment72.groupby(['[run number]', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each source-reach
mean_trans_rate_per_reach_exp72 = mean_trans_rate_per_run_exp72.groupby('source-reach')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp72.index, mean_trans_rate_per_reach_exp72.values, marker='o', color='b', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 72: Transmission Rate as a Function of Source Reach [Network: Circle, Uniform Weight: 0.7]')
plt.grid(True)
plt.show()



###############################################################################
######## EXPERIMENT 73 ########################################################
###############################################################################

# Network type: Circle
# Source Reach: 50
# Uniform Weight: 0.01-1

######## DATA IMPORT ##########################################################

file_path_experiment73 = "C:/Users/nikit/Documents/Studium/Frankfurt School of Finance & Management/Bachelorthese/Simulationsdaten/Information Diffusion V3_Experiment 73.csv"

data_experiment73 = pd.read_csv(file_path_experiment73 , delimiter=',' , skiprows=6 , quotechar='"')

######## Informed Individuals by Weight #######################################

# Calculate the maximum of REPORT-INFORMED-INDIVIDUALS per uniform-weight value across runs
max_per_run_exp73 = data_experiment73.groupby(['[run number]', 'uniform-weight'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()

# Calculate the mean of the maximum REPORT-INFORMED-INDIVIDUALS for each uniform-weight
mean_max_per_weight_exp73 = max_per_run_exp73.groupby('uniform-weight')['REPORT-INFORMED-INDIVIDUALS'].mean()

# Plotting
# This graph shows the mean Information Coverage for the circle network as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp73.index, mean_max_per_weight_exp73.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Information Coverage')
plt.title('Experiment 73: Information Coverage as a Function of Weight [Network: Circle, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Speed by Weight ######################################################

# Calculate the number of steps in each unique run + uniform-weight combination
steps_per_run_exp73 = data_experiment73.groupby(['[run number]', 'uniform-weight'])['[step]'].max().reset_index()

# Calculate the mean number of steps for each uniform-weight
mean_nr_steps_per_weight_exp73 = steps_per_run_exp73.groupby('uniform-weight')['[step]'].mean()

# Plotting
# This graph shows the average number of steps until stabilisation as a function of weight. 
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp73.index, mean_nr_steps_per_weight_exp73.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Number of Steps (Time)')
plt.title('Experiment 73: Speed as a Function of Weight [Network: Circle, Source Reach: 50]')
plt.grid(True)
plt.show()

######## Transmission Rate by Weight ##########################################

# Calculate the average transmission rate for each run
mean_trans_rate_per_run_exp73 = data_experiment73.groupby(['[run number]', 'uniform-weight'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()

# Calculate the average of the average transmission rates for each uniform-weight
mean_trans_rate_per_weight_exp73 = mean_trans_rate_per_run_exp73.groupby('uniform-weight')['REPORT-AVERAGE-TRANSMISSION-RATE'].mean()

# Plotting
# This graph shows the average transmission rate in a run as a function of source reach.
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp73.index, mean_trans_rate_per_weight_exp73.values, marker='o', color='b', linestyle='-')
plt.xlabel('Weight')
plt.ylabel('Mean Transmission Rate in a Run')
plt.title('Experiment 73: Transmission Rate as a Function of Weight [Network: Circle, Source Reach: 50]')
plt.grid(True)
plt.show()



###############################################################################
######## SPECIAL PLOTS AND ANALYSES ###########################################
###############################################################################



######## Information Coverage by Source Reach #################################

# The following graph shows information coverage as a function of source reach
# for the circle network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp9.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp72.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp1.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp5.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp7.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the circle network for given values of uniform weight and for a 
# logarithmically scaled x-axis
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp9.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp72.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp1.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp5.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp1.index, mean_max_per_reach_exp7.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xscale('log')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the fully connected network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp27.index, mean_max_per_reach_exp28.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp27.index, mean_max_per_reach_exp26.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp27.index, mean_max_per_reach_exp27.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.ylim(99.985, 100)
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the star network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp41.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp47.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp39.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp46.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp40.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the star network for given values of uniform weight and for
# a logarithmic scale on x-axis
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp41.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp47.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp39.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp46.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp39.index, mean_max_per_reach_exp40.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xscale('log')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('A.3: Information Coverage as a Function of Source Reach for Given Uniform Weight [Network: Star; logarithmic scaling on x-axis]')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the small world network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp55.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp57.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp53.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp56.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp54.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the small world network for given values of uniform weight and for a 
# logarithmically scaled x-axis
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp55.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp57.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp53.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp56.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp53.index, mean_max_per_reach_exp54.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xscale('log')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.title('A.4: Information Coverage as a Function of Source Reach for Given Uniform Weight [Network: Small World; logarithmic scaling on x-axis]')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the circle network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp3.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp10.values, label='weight = 0.2-1', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp11.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp16.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp23.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_reach_exp3.index, mean_max_per_reach_exp24.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the fully connected network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp29.index, mean_max_per_reach_exp29.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp29.index, mean_max_per_reach_exp63.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp29.index, mean_max_per_reach_exp38.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp29.index, mean_max_per_reach_exp31.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_reach_exp29.index, mean_max_per_reach_exp30.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the star network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp48.index, mean_max_per_reach_exp48.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp48.index, mean_max_per_reach_exp49.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp48.index, mean_max_per_reach_exp52.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp48.index, mean_max_per_reach_exp51.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_reach_exp48.index, mean_max_per_reach_exp50.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of source reach
# for the small world network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_reach_exp58.index, mean_max_per_reach_exp58.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_reach_exp58.index, mean_max_per_reach_exp62.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_reach_exp58.index, mean_max_per_reach_exp61.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_max_per_reach_exp58.index, mean_max_per_reach_exp60.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_reach_exp58.index, mean_max_per_reach_exp59.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()



######## Information Coverage by Uniform Weight ###############################

# The following graph shows information coverage as a function of uniform
# weight for the circle network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp12.index, mean_max_per_weight_exp12.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_weight_exp12.index, mean_max_per_weight_exp13.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_weight_exp12.index, mean_max_per_weight_exp14.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_weight_exp12.index, mean_max_per_weight_exp15.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_weight_exp12.index, mean_max_per_weight_exp73.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of uniform
# weight for the fully connected network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp33.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp34.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp35.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp36.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp37.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Information Coverage')
plt.title('B.2: Information Coverage as a Function of Uniform Weight for Given Source Reach [Network: Fully Connected]')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of uniform
# weight for the fully connected network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp33.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp34.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp35.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp36.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_weight_exp33.index, mean_max_per_weight_exp37.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlim(0,0.1)
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of uniform
# weight for the star network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp43.index, mean_max_per_weight_exp43.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_weight_exp43.index, mean_max_per_weight_exp44.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_weight_exp43.index, mean_max_per_weight_exp70.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_weight_exp43.index, mean_max_per_weight_exp45.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_weight_exp43.index, mean_max_per_weight_exp71.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows information coverage as a function of uniform
# weight for the small world network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_max_per_weight_exp65.index, mean_max_per_weight_exp65.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_max_per_weight_exp65.index, mean_max_per_weight_exp66.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_max_per_weight_exp65.index, mean_max_per_weight_exp68.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_max_per_weight_exp65.index, mean_max_per_weight_exp67.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_max_per_weight_exp65.index, mean_max_per_weight_exp69.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Information Coverage')
plt.legend()
plt.grid(True)
plt.show()



######## Information Coverage by Network Type #################################

# The following bar chart shows the mean information coverage for the different
# types of network and combinations of source reach (1) and 
# uniform weight (0.1, 0.5, 0.9).
data_coverageByNetwork = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Coverage' : [1.25, 3, 21.1,
                                      1.69, 32.27, 100,
                                      2.17, 61.51, 99.91,
                                      12.85, 77.67, 99.86,
                                      100, 100, 100]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_coverageByNetwork, x='Network', y='Coverage', hue='Uniform Weight', palette='dark', legend=False)
ax1 = sns.barplot(data=data_coverageByNetwork, x='Network', y='Coverage', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Information Coverage')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax1.containers:
    ax1.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the information coverage for the different
# types of network and combinations of source reach (1) and 
# uniform weight (0.1, 0.5, 0.9).
data_coverageByNetworkBoxplot = pd.concat([data_experiment7,
                                           data_experiment1,
                                           data_experiment9,
                                           data_experiment53,
                                           data_experiment54,
                                           data_experiment55,
                                           data_experiment39,
                                           data_experiment40,
                                           data_experiment41,
                                           data_experiment17,
                                           data_experiment26,
                                           data_experiment27,
                                           data_experiment28])
max_per_run_coverageByNetworkBoxplot = data_coverageByNetworkBoxplot.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()
max_per_run_coverageByNetworkBoxplot = max_per_run_coverageByNetworkBoxplot[(max_per_run_coverageByNetworkBoxplot['uniform-weight'].isin([0.1, 0.5, 0.9])) & (max_per_run_coverageByNetworkBoxplot['source-reach'].isin([1]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=max_per_run_coverageByNetworkBoxplot,
            x='type-of-network',
            y='REPORT-INFORMED-INDIVIDUALS',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Network')
plt.ylabel('Information Coverage')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()

# The following bar chart shows the mean information coverage for the different
# types of network and combinations of source reach (30) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_coverageByNetwork2 = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Coverage' : [34.26, 58.79, 94.81,
                                      39.8, 89.77, 99.95,
                                      41.88, 87.22, 99.95,
                                      12.85, 77.67, 99.86,
                                      100, 100, 100]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_coverageByNetwork2, x='Network', y='Coverage', hue='Uniform Weight', palette='dark', legend=False)
ax2 = sns.barplot(data=data_coverageByNetwork2, x='Network', y='Coverage', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Information Coverage')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax2.containers:
    ax2.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the information coverage for the different
# types of network and combinations of source reach (30) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_coverageByNetworkBoxplot2 = pd.concat([data_experiment7,
                                           data_experiment1,
                                           data_experiment9,
                                           data_experiment53,
                                           data_experiment54,
                                           data_experiment55,
                                           data_experiment39,
                                           data_experiment40,
                                           data_experiment41,
                                           data_experiment17,
                                           data_experiment26,
                                           data_experiment27,
                                           data_experiment28])
max_per_run_coverageByNetworkBoxplot2 = data_coverageByNetworkBoxplot2.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()
max_per_run_coverageByNetworkBoxplot2 = max_per_run_coverageByNetworkBoxplot2[(max_per_run_coverageByNetworkBoxplot2['uniform-weight'].isin([0.1, 0.5, 0.9])) & (max_per_run_coverageByNetworkBoxplot2['source-reach'].isin([30]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=max_per_run_coverageByNetworkBoxplot2,
            x='type-of-network',
            y='REPORT-INFORMED-INDIVIDUALS',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Network')
plt.ylabel('Information Coverage')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()


# The following bar chart shows the mean information coverage for the different
# types of network and combinations of source reach (50) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_coverageByNetwork3 = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Coverage' : [54.73, 78.33, 98.47,
                                      60.98, 95.17, 99.99,
                                      61.35, 91.95, 99.96,
                                      12.85, 77.67, 99.86,
                                      100, 100, 100]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_coverageByNetwork3, x='Network', y='Coverage', hue='Uniform Weight', palette='dark', legend=False)
ax3 = sns.barplot(data=data_coverageByNetwork3, x='Network', y='Coverage', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Information Coverage')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax3.containers:
    ax3.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the information coverage for the different
# types of network and combinations of source reach (50) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_coverageByNetworkBoxplot3 = pd.concat([data_experiment7,
                                           data_experiment1,
                                           data_experiment9,
                                           data_experiment53,
                                           data_experiment54,
                                           data_experiment55,
                                           data_experiment39,
                                           data_experiment40,
                                           data_experiment41,
                                           data_experiment17,
                                           data_experiment26,
                                           data_experiment27,
                                           data_experiment28])
max_per_run_coverageByNetworkBoxplot3 = data_coverageByNetworkBoxplot3.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['REPORT-INFORMED-INDIVIDUALS'].max().reset_index()
max_per_run_coverageByNetworkBoxplot3 = max_per_run_coverageByNetworkBoxplot3[(max_per_run_coverageByNetworkBoxplot3['uniform-weight'].isin([0.1, 0.5, 0.9])) & (max_per_run_coverageByNetworkBoxplot3['source-reach'].isin([50]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=max_per_run_coverageByNetworkBoxplot3,
            x='type-of-network',
            y='REPORT-INFORMED-INDIVIDUALS',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Network')
plt.ylabel('Information Coverage')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()



######## Speed (Nr of Steps) by Source Reach ##################################

# The following graph shows speed (nr of steps) as a function of source reach
# for the circle network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp1.index, mean_nr_steps_per_reach_exp9.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp1.index, mean_nr_steps_per_reach_exp72.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp1.index, mean_nr_steps_per_reach_exp1.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp1.index, mean_nr_steps_per_reach_exp5.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp1.index, mean_nr_steps_per_reach_exp7.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the star network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp41.index, mean_nr_steps_per_reach_exp41.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp41.index, mean_nr_steps_per_reach_exp47.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp41.index, mean_nr_steps_per_reach_exp39.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp41.index, mean_nr_steps_per_reach_exp46.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp41.index, mean_nr_steps_per_reach_exp40.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the fully connected network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp28.index, mean_nr_steps_per_reach_exp28.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp28.index, mean_nr_steps_per_reach_exp26.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp28.index, mean_nr_steps_per_reach_exp27.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the small world network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp55.index, mean_nr_steps_per_reach_exp55.values, label='uniform weight = 0.9', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp55.index, mean_nr_steps_per_reach_exp57.values, label='uniform weight = 0.7', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp55.index, mean_nr_steps_per_reach_exp53.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp55.index, mean_nr_steps_per_reach_exp56.values, label='uniform weight = 0.3', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp55.index, mean_nr_steps_per_reach_exp54.values, label='uniform weight = 0.1', marker='o', color='blue', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the circle network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp3.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp10.values, label='weight = 0.2-1', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp11.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp16.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp23.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp3.index, mean_nr_steps_per_reach_exp24.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the star network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp48.index, mean_nr_steps_per_reach_exp48.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp48.index, mean_nr_steps_per_reach_exp49.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp48.index, mean_nr_steps_per_reach_exp52.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp48.index, mean_nr_steps_per_reach_exp51.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp48.index, mean_nr_steps_per_reach_exp50.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the fully connected network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp29.index, mean_nr_steps_per_reach_exp29.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp29.index, mean_nr_steps_per_reach_exp63.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp29.index, mean_nr_steps_per_reach_exp38.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp29.index, mean_nr_steps_per_reach_exp31.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp29.index, mean_nr_steps_per_reach_exp30.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed (nr of steps) as a function of source reach
# for the small world network for given varied weight limits
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_reach_exp58.index, mean_nr_steps_per_reach_exp58.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp58.index, mean_nr_steps_per_reach_exp62.values, label='weight = 0-1', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp58.index, mean_nr_steps_per_reach_exp61.values, label='weight = 0.3-0.6', marker='o', color='green', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp58.index, mean_nr_steps_per_reach_exp60.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_reach_exp58.index, mean_nr_steps_per_reach_exp59.values, label='weight = 0-0.5', marker='o', color='magenta', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()



######## Speed (Nr of Steps) by Uniform Weight ################################

# The following graph shows speed as a function of uniform
# weight for the circle network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp12.index, mean_nr_steps_per_weight_exp12.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp12.index, mean_nr_steps_per_weight_exp13.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp12.index, mean_nr_steps_per_weight_exp14.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp12.index, mean_nr_steps_per_weight_exp15.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp12.index, mean_nr_steps_per_weight_exp73.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed as a function of uniform
# weight for the star network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp43.index, mean_nr_steps_per_weight_exp43.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp43.index, mean_nr_steps_per_weight_exp44.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp43.index, mean_nr_steps_per_weight_exp70.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp43.index, mean_nr_steps_per_weight_exp45.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp43.index, mean_nr_steps_per_weight_exp71.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed as a function of uniform
# weight for the fully connected network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp33.index, mean_nr_steps_per_weight_exp33.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp33.index, mean_nr_steps_per_weight_exp34.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp33.index, mean_nr_steps_per_weight_exp35.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp33.index, mean_nr_steps_per_weight_exp36.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp33.index, mean_nr_steps_per_weight_exp37.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows speed as a function of uniform
# weight for the small world network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_nr_steps_per_weight_exp65.index, mean_nr_steps_per_weight_exp65.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp65.index, mean_nr_steps_per_weight_exp66.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp65.index, mean_nr_steps_per_weight_exp68.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp65.index, mean_nr_steps_per_weight_exp67.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_nr_steps_per_weight_exp65.index, mean_nr_steps_per_weight_exp69.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Nr of Steps (Inverse of Speed)')
plt.legend()
plt.grid(True)
plt.show()



######## Speed by Network Type ################################################

# The following bar chart shows the mean nr of steps (speed) for the different
# types of network and combinations of source reach (1) and 
# uniform weight (0.1, 0.5, 0.9).
data_speedByNetwork = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Steps' : [0.24, 1.64, 14.76,
                                   0.6, 10.29, 10.73,
                                   0.46, 4.31, 3.31,
                                   2.02, 4.01, 2.25,
                                   3.13, 2, 2]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_speedByNetwork, x='Network', y='Steps', hue='Uniform Weight', palette='dark', legend=False)
ax4 = sns.barplot(data=data_speedByNetwork, x='Network', y='Steps', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Mean Nr of Steps (Inverse Speed)')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax4.containers:
    ax4.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the speed for the different
# types of network and combinations of source reach (1) and 
# uniform weight (0.1, 0.5, 0.9).
data_speedByNetworkBoxplot = pd.concat([data_experiment7,
                                           data_experiment1,
                                           data_experiment9,
                                           data_experiment53,
                                           data_experiment54,
                                           data_experiment55,
                                           data_experiment39,
                                           data_experiment40,
                                           data_experiment41,
                                           data_experiment17,
                                           data_experiment26,
                                           data_experiment27,
                                           data_experiment28])
steps_per_run_speedByNetworkBoxplot = data_speedByNetworkBoxplot.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['[step]'].max().reset_index()
steps_per_run_speedByNetworkBoxplot = steps_per_run_speedByNetworkBoxplot[(steps_per_run_speedByNetworkBoxplot['uniform-weight'].isin([0.1, 0.5, 0.9])) & (steps_per_run_speedByNetworkBoxplot['source-reach'].isin([1]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=steps_per_run_speedByNetworkBoxplot,
            x='type-of-network',
            y='[step]',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Network')
plt.ylabel('Nr of Steps (Inverse Speed)')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()

# The following bar chart shows the mean nr of steps (speed) for the different
# types of network and combinations of source reach (30) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_speedByNetwork2 = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Steps' : [1.26, 3.61, 6.8,
                                   2.06, 4.79, 3.09,
                                   2.41, 3.79, 2.68,
                                   2.02, 4.01, 2.25,
                                   1.95, 1, 1]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_speedByNetwork2, x='Network', y='Steps', hue='Uniform Weight', palette='dark', legend=False)
ax5 = sns.barplot(data=data_speedByNetwork2, x='Network', y='Steps', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Mean Nr of Steps (Inverse Speed)')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax5.containers:
    ax5.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following bar chart shows the mean nr of steps (speed) for the different
# types of network and combinations of source reach (50) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_speedByNetwork3 = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Steps' : [1.2, 2.91, 4.05,
                                   1.92, 3.19, 2.11,
                                   1.98, 2.83, 2.1,
                                   2.02, 4.01, 2.25,
                                   1.27, 1, 1]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_speedByNetwork3, x='Network', y='Steps', hue='Uniform Weight', palette='dark', legend=False)
ax6 = sns.barplot(data=data_speedByNetwork3, x='Network', y='Steps', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Mean Nr of Steps (Inverse Speed)')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax6.containers:
    ax6.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the speed for the different
# types of network and combinations of source reach (50) and 
# uniform weight (0.1, 0.5, 0.9).
data_speedByNetworkBoxplot3 = pd.concat([data_experiment7,
                                           data_experiment1,
                                           data_experiment9,
                                           data_experiment53,
                                           data_experiment54,
                                           data_experiment55,
                                           data_experiment39,
                                           data_experiment40,
                                           data_experiment41,
                                           data_experiment17,
                                           data_experiment26,
                                           data_experiment27,
                                           data_experiment28])
steps_per_run_speedByNetworkBoxplot3 = data_speedByNetworkBoxplot3.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['[step]'].max().reset_index()
steps_per_run_speedByNetworkBoxplot3 = steps_per_run_speedByNetworkBoxplot3[(steps_per_run_speedByNetworkBoxplot3['uniform-weight'].isin([0.1, 0.5, 0.9])) & (steps_per_run_speedByNetworkBoxplot3['source-reach'].isin([50]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=steps_per_run_speedByNetworkBoxplot3,
            x='type-of-network',
            y='[step]',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.xlabel('Network')
plt.ylabel('Nr of Steps (Inverse Speed)')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()



######## Transmission Rate for Fully Connected ################################

# The following graph shows transmission rate as a function of uniform
# weight for the fully connected network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp33.index, mean_trans_rate_per_weight_exp33.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp33.index, mean_trans_rate_per_weight_exp34.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp33.index, mean_trans_rate_per_weight_exp35.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp33.index, mean_trans_rate_per_weight_exp36.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp33.index, mean_trans_rate_per_weight_exp37.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows transmission rate as a function of source reach
# for the fully connected network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp27.index, mean_trans_rate_per_reach_exp27.values, label='uniform weight = 0.1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp27.index, mean_trans_rate_per_reach_exp26.values, label='uniform weight = 0.5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp27.index, mean_trans_rate_per_reach_exp28.values, label='uniform weight = 0.9', marker='o', color='red', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()



######## Transmission Rate for Star ###########################################

# The following graph shows transmission rate as a function of uniform
# weight for the star network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp43.index, mean_trans_rate_per_weight_exp43.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp43.index, mean_trans_rate_per_weight_exp44.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp43.index, mean_trans_rate_per_weight_exp70.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp43.index, mean_trans_rate_per_weight_exp45.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp43.index, mean_trans_rate_per_weight_exp71.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows transmission rate as a function of source reach
# for the star network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp40.index, mean_trans_rate_per_reach_exp40.values, label='uniform weight = 0.1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp40.index, mean_trans_rate_per_reach_exp46.values, label='uniform weight = 0.3', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp40.index, mean_trans_rate_per_reach_exp39.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp40.index, mean_trans_rate_per_reach_exp47.values, label='uniform weight = 0.7', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp40.index, mean_trans_rate_per_reach_exp41.values, label='uniform weight = 0.9', marker='o', color='green', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows transmission rate as a function of source reach
# for the star network for given values of varied weight
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp48.index, mean_trans_rate_per_reach_exp48.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp48.index, mean_trans_rate_per_reach_exp49.values, label='weight = 0-1', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp48.index, mean_trans_rate_per_reach_exp52.values, label='weight = 0.3-0.6', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp48.index, mean_trans_rate_per_reach_exp51.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp48.index, mean_trans_rate_per_reach_exp50.values, label='weight = 0-0.5', marker='o', color='green', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate per Run')
plt.title('H.3: Transmission Rate as a Function of Source Reach for Given Varied Weight [Network: Star]')
plt.legend()
plt.grid(True)
plt.show()



######## Transmission Rate for Star ###########################################

# The following graph shows transmission rate as a function of uniform
# weight for the small world network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp65.index, mean_trans_rate_per_weight_exp65.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp65.index, mean_trans_rate_per_weight_exp66.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp65.index, mean_trans_rate_per_weight_exp68.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp65.index, mean_trans_rate_per_weight_exp67.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp65.index, mean_trans_rate_per_weight_exp69.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows transmission rate as a function of source reach
# for the small world network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp54.index, mean_trans_rate_per_reach_exp54.values, label='uniform weight = 0.1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp54.index, mean_trans_rate_per_reach_exp56.values, label='uniform weight = 0.3', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp54.index, mean_trans_rate_per_reach_exp53.values, label='uniform weight = 0.5', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp54.index, mean_trans_rate_per_reach_exp57.values, label='uniform weight = 0.7', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp54.index, mean_trans_rate_per_reach_exp55.values, label='uniform weight = 0.9', marker='o', color='green', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows transmission rate as a function of source reach
# for the small world network for given values of varied weight
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp58.index, mean_trans_rate_per_reach_exp58.values, label='weight = 0.2-0.8', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp58.index, mean_trans_rate_per_reach_exp62.values, label='weight = 0-1', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp58.index, mean_trans_rate_per_reach_exp61.values, label='weight = 0.3-0.6', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp58.index, mean_trans_rate_per_reach_exp60.values, label='weight = 0.5-1', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp58.index, mean_trans_rate_per_reach_exp59.values, label='weight = 0-0.5', marker='o', color='green', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()



######## Transmission Rate by Network Type ####################################

# The following bar chart shows the mean transmission rate for the different
# types of network and combinations of source reach (1) and 
# uniform weight (0.1, 0.5, 0.9).
data_rateByNetwork = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Rate' : [0.16, 0.826619, 1.34544,
                                  0.38, 2.78106, 9.84939,
                                  0.706667, 12.4777, 30.7707,
                                  6.10083, 20.1782, 45.5888,
                                  31.515, 49.5, 49.5]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_rateByNetwork, x='Network', y='Rate', hue='Uniform Weight', palette='dark', legend=False)
ax7 = sns.barplot(data=data_rateByNetwork, x='Network', y='Rate', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax7.containers:
    ax7.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the transmission rate for the different
# types of network and combinations of source reach (1) and 
# uniform weight (0.1, 0.5, 0.9).
data_rateByNetworkBoxplot = pd.concat([data_experiment12,
                                       data_experiment17,
                                       data_experiment65,
                                       data_experiment43,
                                       data_experiment33])
rateByNetworkBoxplot = data_rateByNetworkBoxplot.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()
rateByNetworkBoxplot = rateByNetworkBoxplot[(rateByNetworkBoxplot['uniform-weight'].isin([0.1, 0.5, 0.9])) & (rateByNetworkBoxplot['source-reach'].isin([1]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=rateByNetworkBoxplot,
            x='type-of-network',
            y='REPORT-AVERAGE-TRANSMISSION-RATE',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.title('J.1: Transmission Rate by Network for Source Reach = 1 and Uniform Weight = 0.1, 0.5, 0.9')
plt.xlabel('Network')
plt.ylabel('Mean Transmission Rate per Run')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()

# The following bar chart shows the transmission rate for the different
# types of network and combinations of source reach (30) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_rateByNetwork2 = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Rate' : [3.885, 7.9385, 10.225,
                                  5.38, 13.2798, 23.995,
                                  5.70083, 17.4893, 27.6133,
                                  6.10083, 20.1782, 45.5888,
                                  36.05, 70, 70]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_rateByNetwork2, x='Network', y='Rate', hue='Uniform Weight', palette='dark', legend=False)
ax8 = sns.barplot(data=data_rateByNetwork2, x='Network', y='Rate', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax8.containers:
    ax8.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following bar chart shows the transmission rate for the different
# types of network and combinations of source reach (50) and 
# uniform weight (0.1, 0.5, 0.9). Keep in mind that the royal family is 
# the only seed node in the royal family network.
data_rateByNetwork3 = pd.DataFrame({
                        'Network' : ['Circle', 'Circle', 'Circle', 
                                     'Small world', 'Small world', 'Small world',
                                     'Star', 'Star', 'Star',
                                     'Royal Family', 'Royal Family', 'Royal Family',
                                     'Fully Connected','Fully Connected', 'Fully Connected'],
                        'Uniform Weight' : [0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,
                                            0.1, 0.5, 0.9,],
                        'Rate' : [4.38, 9.69683, 12.7039,
                                   6.3625, 15.2897, 24.495,
                                   5.73417, 14.8475, 25.2908,
                                   6.10083, 20.1782, 45.5888,
                                   45.75, 50, 50]
                        })
plt.figure(figsize=(16, 10))
sns.barplot(data=data_rateByNetwork3, x='Network', y='Rate', hue='Uniform Weight', palette='dark', legend=False)
ax9 = sns.barplot(data=data_rateByNetwork3, x='Network', y='Rate', hue='Uniform Weight', palette='dark')
plt.xlabel('Network')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend(title='Uniform Weight')
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i in ax9.containers:
    ax9.bar_label(i, fmt='%.2f', padding=10, label_type='edge', fontsize=10)
plt.show()

# The following box plot shows the transmission rate for the different
# types of network and combinations of source reach (50) and 
# uniform weight (0.1, 0.5, 0.9).
data_rateByNetworkBoxplot3 = pd.concat([data_experiment73,
                                        data_experiment69,
                                        data_experiment17,
                                        data_experiment71,
                                        data_experiment37])
rateByNetworkBoxplot3 = data_rateByNetworkBoxplot3.groupby(['[run number]', 'uniform-weight', 'type-of-network', 'source-reach'])['REPORT-AVERAGE-TRANSMISSION-RATE'].last().reset_index()
rateByNetworkBoxplot3 = rateByNetworkBoxplot3[(rateByNetworkBoxplot3['uniform-weight'].isin([0.1, 0.5, 0.9])) & (rateByNetworkBoxplot3['source-reach'].isin([50]))]
plt.figure(figsize=(16, 10))
sns.boxplot(data=rateByNetworkBoxplot3,
            x='type-of-network',
            y='REPORT-AVERAGE-TRANSMISSION-RATE',
            hue='uniform-weight',
            palette='dark',
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black"})
plt.title('J.3: Transmission Rate by Network for Source Reach = 50 and Uniform Weight = 0.1, 0.5, 0.9')
plt.xlabel('Network')
plt.ylabel('Mean Transmission Rate per Run')
plt.grid(axis='y', 
         linestyle='--',
         alpha=0.7)
plt.show()



######## Relationship between Speed & Coverage ################################

# The following regression shows the relationship between speed & coverage for 
# the circle network for uniform weight = 0.1, 0.5, 0.9 and source reach varied
regression1 = pd.DataFrame(mean_max_per_reach_exp7)
regression1['steps'] = mean_nr_steps_per_reach_exp7
regression2 = pd.DataFrame(mean_max_per_reach_exp1)
regression2['steps'] = mean_nr_steps_per_reach_exp1
regression3 = pd.DataFrame(mean_max_per_reach_exp9)
regression3['steps'] = mean_nr_steps_per_reach_exp9

plt.figure(figsize=(16, 10))
sns.regplot(data=regression1, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "weight = 0.1"})
sns.regplot(data=regression2, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "weight = 0.5"})
sns.regplot(data=regression3, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "weight = 0.9"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the circle network for source reach = 1, 30, 50 and uniform weight varied
regression4 = pd.DataFrame(mean_max_per_weight_exp12)
regression4['steps'] = mean_nr_steps_per_weight_exp12
regression5 = pd.DataFrame(mean_max_per_weight_exp15)
regression5['steps'] = mean_nr_steps_per_weight_exp15
regression6 = pd.DataFrame(mean_max_per_weight_exp73)
regression6['steps'] = mean_nr_steps_per_weight_exp73

plt.figure(figsize=(16, 10))
sns.regplot(data=regression4, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "source reach = 1"})
sns.regplot(data=regression5, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "source reach = 30"})
sns.regplot(data=regression6, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "source reach = 50"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the star network for uniform weight = 0.1, 0.5, 0.9 and source reach varied
regression7 = pd.DataFrame(mean_max_per_reach_exp40)
regression7['steps'] = mean_nr_steps_per_reach_exp40
regression8 = pd.DataFrame(mean_max_per_reach_exp39)
regression8['steps'] = mean_nr_steps_per_reach_exp39
regression9 = pd.DataFrame(mean_max_per_reach_exp41)
regression9['steps'] = mean_nr_steps_per_reach_exp41

plt.figure(figsize=(16, 10))
sns.regplot(data=regression7, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "weight = 0.1"})
sns.regplot(data=regression8, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "weight = 0.5"})
sns.regplot(data=regression9, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "weight = 0.9"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the star network for source reach = 1, 30, 50 and uniform weight varied
regression10 = pd.DataFrame(mean_max_per_weight_exp43)
regression10['steps'] = mean_nr_steps_per_weight_exp43
regression11 = pd.DataFrame(mean_max_per_weight_exp45)
regression11['steps'] = mean_nr_steps_per_weight_exp45
regression12 = pd.DataFrame(mean_max_per_weight_exp71)
regression12['steps'] = mean_nr_steps_per_weight_exp71

plt.figure(figsize=(16, 10))
sns.regplot(data=regression10, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "source reach = 1"})
sns.regplot(data=regression11, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "source reach = 30"})
sns.regplot(data=regression12, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "source reach = 50"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the small world network for uniform weight = 0.1, 0.5, 0.9 and source reach varied
regression13 = pd.DataFrame(mean_max_per_reach_exp54)
regression13['steps'] = mean_nr_steps_per_reach_exp54
regression14 = pd.DataFrame(mean_max_per_reach_exp53)
regression14['steps'] = mean_nr_steps_per_reach_exp53
regression15 = pd.DataFrame(mean_max_per_reach_exp55)
regression15['steps'] = mean_nr_steps_per_reach_exp55

plt.figure(figsize=(16, 10))
sns.regplot(data=regression13, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "weight = 0.1"})
sns.regplot(data=regression14, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "weight = 0.5"})
sns.regplot(data=regression15, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "weight = 0.9"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the small world network for source reach = 1, 30, 50 and uniform weight varied
regression16 = pd.DataFrame(mean_max_per_weight_exp65)
regression16['steps'] = mean_nr_steps_per_weight_exp65
regression17 = pd.DataFrame(mean_max_per_weight_exp67)
regression17['steps'] = mean_nr_steps_per_weight_exp67
regression18 = pd.DataFrame(mean_max_per_weight_exp69)
regression18['steps'] = mean_nr_steps_per_weight_exp69

plt.figure(figsize=(16, 10))
sns.regplot(data=regression16, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "source reach = 1"})
sns.regplot(data=regression17, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "source reach = 30"})
sns.regplot(data=regression18, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "source reach = 50"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the royal family network for uniform weight varied
regression19 = pd.DataFrame(mean_max_per_weight_exp17)
regression19['steps'] = mean_nr_steps_per_weight_exp17

plt.figure(figsize=(16, 10))
sns.regplot(data=regression19, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "source reach =  central node"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the fully connected network for uniform weight = 0.1, 0.5, 0.9 and source reach varied
regression20 = pd.DataFrame(mean_max_per_reach_exp27)
regression20['steps'] = mean_nr_steps_per_reach_exp27
regression21 = pd.DataFrame(mean_max_per_reach_exp26)
regression21['steps'] = mean_nr_steps_per_reach_exp26
regression22 = pd.DataFrame(mean_max_per_reach_exp28)
regression22['steps'] = mean_nr_steps_per_reach_exp28

plt.figure(figsize=(16, 10))
sns.regplot(data=regression20, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "weight = 0.1"})
sns.regplot(data=regression21, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "weight = 0.5"})
sns.regplot(data=regression22, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "weight = 0.9"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()

# The following regression shows the relationship between speed & coverage for 
# the fully connected network for source reach = 1, 30, 50 and uniform weight varied
regression23 = pd.DataFrame(mean_max_per_weight_exp33)
regression23['steps'] = mean_nr_steps_per_weight_exp33
regression24 = pd.DataFrame(mean_max_per_weight_exp36)
regression24['steps'] = mean_nr_steps_per_weight_exp36
regression25 = pd.DataFrame(mean_max_per_weight_exp37)
regression25['steps'] = mean_nr_steps_per_weight_exp37

plt.figure(figsize=(16, 10))
sns.regplot(data=regression23, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "red", "label": "source reach = 1"})
sns.regplot(data=regression24, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "blue", "label": "source reach = 30"})
sns.regplot(data=regression25, x='REPORT-INFORMED-INDIVIDUALS', y='steps', ci=95, line_kws={"color": "black", "label": "source reach = 50"})
plt.legend()
plt.xlabel('Information Coverage')
plt.ylabel('Number of Steps (Inverse Speed)')
plt.show()



######## Transmission Rate for Fully Connected ################################

# The following graph shows transmission rate as a function of uniform
# weight for the circle network for given values of source reach
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_weight_exp12.index, mean_trans_rate_per_weight_exp12.values, label='source reach = 1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp12.index, mean_trans_rate_per_weight_exp13.values, label='source reach = 5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp12.index, mean_trans_rate_per_weight_exp14.values, label='source reach = 10', marker='o', color='red', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp12.index, mean_trans_rate_per_weight_exp15.values, label='source reach = 30', marker='o', color='blue', linestyle='-')
plt.plot(mean_trans_rate_per_weight_exp12.index, mean_trans_rate_per_weight_exp73.values, label='source reach = 50', marker='o', color='green', linestyle='-')
plt.xlabel('Uniform Weight')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()

# The following graph shows transmission rate as a function of source reach
# for the circle network for given values of uniform weight
plt.figure(figsize=(16, 10))
plt.plot(mean_trans_rate_per_reach_exp7.index, mean_trans_rate_per_reach_exp7.values, label='uniform weight = 0.1', marker='o', color='black', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp7.index, mean_trans_rate_per_reach_exp1.values, label='uniform weight = 0.5', marker='o', color='yellow', linestyle='-')
plt.plot(mean_trans_rate_per_reach_exp7.index, mean_trans_rate_per_reach_exp9.values, label='uniform weight = 0.9', marker='o', color='red', linestyle='-')
plt.xlabel('Source Reach')
plt.ylabel('Mean Transmission Rate per Run')
plt.legend()
plt.grid(True)
plt.show()



######## Clustering Coefficient of Small World Networks #######################

print(data_experiment53['FIND-CLUSTERING-COEFFICIENT'].min())
print(data_experiment53['FIND-CLUSTERING-COEFFICIENT'].max())
print(data_experiment53['FIND-AVERAGE-PATH-LENGTH'].min())
print(data_experiment53['FIND-AVERAGE-PATH-LENGTH'].max())

print(data_experiment54['FIND-CLUSTERING-COEFFICIENT'].min())
print(data_experiment54['FIND-CLUSTERING-COEFFICIENT'].max())
print(data_experiment54['FIND-AVERAGE-PATH-LENGTH'].min())
print(data_experiment54['FIND-AVERAGE-PATH-LENGTH'].max())

print(data_experiment55['FIND-CLUSTERING-COEFFICIENT'].min())
print(data_experiment55['FIND-CLUSTERING-COEFFICIENT'].max())
print(data_experiment55['FIND-AVERAGE-PATH-LENGTH'].min())
print(data_experiment55['FIND-AVERAGE-PATH-LENGTH'].max())

print(data_experiment56['FIND-CLUSTERING-COEFFICIENT'].min())
print(data_experiment56['FIND-CLUSTERING-COEFFICIENT'].max())
print(data_experiment56['FIND-AVERAGE-PATH-LENGTH'].min())
print(data_experiment56['FIND-AVERAGE-PATH-LENGTH'].max())

print(data_experiment57['FIND-CLUSTERING-COEFFICIENT'].min())
print(data_experiment57['FIND-CLUSTERING-COEFFICIENT'].max())
print(data_experiment57['FIND-AVERAGE-PATH-LENGTH'].min())
print(data_experiment57['FIND-AVERAGE-PATH-LENGTH'].max())
