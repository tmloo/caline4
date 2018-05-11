
# coding: utf-8

# In[2]:


#setting environment and reading in data
# /Users/reinarau/Desktop/links.csv
# /Users/reinarau/Desktop/receptors.csv

#import packages
import pandas as pd

def valid_input(question_string, possible_answers):
    while True:
        response = input(question_string)
        if response in possible_answers:
            return response
        else:
            print('Invalid response, try again.')

#import link csv
link = input("Please type in the path to your link source file: ")
file = open(link, 'r')
link_data = pd.read_csv(link)

#import receptor csv
receptor = input("Please type in the path to your receptor source file: ")
file = open(receptor, 'r')
receptor_data = pd.read_csv(receptor)


# In[3]:


# merge duplicate link data 
merge1 = link_data.groupby('Name').nth(0).reset_index()
merge2 = link_data.groupby('Name').nth(1).reset_index()

merge3 = pd.concat([merge1, merge2.drop('Name', 1)], axis = 1)
merge3.columns = ['Name','EMFAC1', 'Traffic Volume1','X1', 'Y1','EMFAC2','Traffic Volume2','X2', 'Y2']


# In[4]:


# name of run
name = input('Enter run name: ')

run = valid_input("Select the type of pollutant to model ('CO', 'NO2', 'PM'): ", ['CO', 'NO2', 'PM'])

mol_weight = run
if mol_weight == "PM":
    mol_weight = 0
elif run_answer == "CO":
    mol_weight = 28
elif run_answer == "NO2":
    mol_weight = 46
else:
    mol_weight = 'invalid pollutant type'

# run units
unit_set = 1 #1 for meters, 0 for feet


# In[5]:


# receptor information 
receptor_num = input('Enter number of receptors as an integer: ')
altitude_receptor = input('Enter height of receptor in meters as an integer without any units: ')
altitude_sea = input('Enter altitude above sea level in meters as an integer without any units: ')

# link information
link_num = input('Enter number of links as an integer: ')
link_type = valid_input("Select the link type ('at_grade', 'depressed', 'fill', 'bridge', 'parking_lot'): ", ['at_grade', 'depressed', 'fill', 'bridge', 'parking_lot'])
link_height = input("Enter the average link height in meters as an integer with no units: ")
mixing_zone_width = input("Enter the average width of traffic lanes plus 3 meters on each side, as an integer with no units. Min allowable value = 10m: ")

# recode link type 
link_type_answer = link_type
if link_type == "at_grade":
    link_type_answer = 1
elif link_type == "depressed":
    link_type_answer = 2
elif link_type == "fill":
    link_type_answer = 3
elif link_type == "bridge":
    link_type_answer = 4
elif link_type == "parking_lot":
    link_type_answer = 5


# In[6]:


z0 = input('Enter the aerodynamic roughness coefficient as an integer without any units. Rural = 10cm, Suburban = 100cm, Urban = 400cm: ')
settling_v = input('Enter settling velocity as an integer without any units: ')
deposition_v = input('Enter deposition velocity as an integer without any units: ')
parameter_8 = 1 #figure what this is
parameter_9 = 1 #figure what this is


# In[7]:


wind_dir = input('Enter wind direction without units 0 - 360: ')
wind_speed = input('Enter wind speed in m/s without units: ')
atm_class = input('Enter atmospheric stability class 1-7: ')
mixing_height = input('Enter mixing height in meters without units: ')
wind_dir_sd = input('Enter wind direction standard deviation, SD 5-60 degrees: ')
ambient_conc = input('Enter the ambient pollution concentration ug/m3 without units: ')
ambient_temp = input('Enter the ambient temperature in Celcius, without units: ')


# In[8]:


# create new text file
output_file_name = 'caline_output.txt'
out = open(output_file_name, 'w+')

# write name of run
out.write(name)
out.write('\r\n')

# write chosen pollutant model
run_answer = run
if run_answer == "PM":
    out.write("4Particulates\r\n")
elif run_answer == "CO":
    out.write("1CO\r\n")
elif run_answer == "NO2":
    out.write("2Nitrogen Dioxide\r\n")
else:
    out.write("Invalid pollutant.\r\n")
    
# write general parameters
gen_parameters = [z0, mol_weight, settling_v, deposition_v, receptor_num, link_num, unit_set, parameter_8, parameter_9, altitude_sea]
for x in gen_parameters: 
    out.write(str(x) + ' ')
out.write('\r\n')

# write receptor name
for index, row in receptor_data.iterrows(): 
    out.write(row['Name'] + '\r\n')
    
# write receptor geometry and height
receptor_data['height'] = altitude_receptor
for index, row in receptor_data.iterrows():
    out.write(str(row['X']) + ' ')
    out.write(str(row['Y']) + ' ')
    out.write(str(row['height'])+ ' ')
    out.write('\r\n')


# write link names 
for index, row in merge3.iterrows():
    out.write(row['Name'])
    out.write('\r\n')

#link parameters
merge3['link_type'] = link_type_answer  #only works as a bulk function. what if a link types are dif for each link?
merge3['link_height'] = link_height #as written, is an average
merge3['mixing_zone_width'] = mixing_zone_width  #as written, is an average
merge3['c_b_left'] = 0 #as written, disables canyon/bluff interaction
merge3['c_b_right'] = 0 #as written, disables canyon/bluff interaction
merge3['unknown_parameter'] = 0 #as written, assumes all links are at 0

for index, row in merge3.iterrows():
    out.write(str(row['link_type'])+' ')
    out.write(str(row['X1'])+' ')
    out.write(str(row['Y1'])+ ' ')
    out.write(str(row['X2'])+' ')
    out.write(str(row['Y2'])+' ')
    out.write(str(row['link_height'])+' ')
    out.write(str(row['mixing_zone_width'])+' ')
    out.write(str(row['c_b_left'])+' ')
    out.write(str(row['c_b_right'])+' ')
    out.write(str(row['unknown_parameter'])+' ')
    out.write('\r\n')

out.write("31101Hour1\r\n")

# write traffic volume at each link
traffic_volume_list = merge3['Traffic Volume2'].values.tolist()

for traffic_volume in traffic_volume_list:
    out.write(str(traffic_volume)+' ')
out.write('\r\n') 


# write emissions factor at each link
emfac_list = merge3['EMFAC1'].values.tolist()

for emfac in emfac_list:
    out.write(str(emfac)+' ')
out.write('\r\n')
    
    
# write meteorological parameters
met_parameters = [wind_dir, wind_speed, atm_class, mixing_height, wind_dir_sd, ambient_conc, ambient_temp]
for x in met_parameters: 
    out.write(str(x)+ ' ')

out.close()

print("Successfully created input .txt file for CALINE4 -- " + output_file_name)

