import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
import opendp.prelude as dp

dp.enable_features("contrib", "floating-point", "honest-but-curious")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from DP_epidemiology.hotspot_analyzer import hotspot_analyzer 
from DP_epidemiology.mobility_analyzer import mobility_analyzer
from DP_epidemiology.pandemic_stage_analyzer import pandemic_stage_analyzer
from DP_epidemiology.contact_matrix import get_age_group_count_map, get_contact_matrix, get_pearson_similarity

path = "C:\\Users\kshub\\OneDrive\\Documents\\PET_phase_2\\Technical_Phase_Data\\technical_phase_data.csv"
df = pd.read_csv(path)

start_date, end_date = datetime(2020, 9, 1), datetime(2021, 3, 31)
print("hotspot_analyzer")
print(hotspot_analyzer(df,start_date,end_date,"Medellin",10))
print("mobility_analyzer")
print(mobility_analyzer(df,start_date,end_date,"Medellin",10))
print("pandemic_stage_analyzer")
print(pandemic_stage_analyzer(df,start_date,end_date,"Medellin",essential_or_luxury="luxury",epsilon=10))

print("contact_matrix")
start_date, end_date = datetime(2022,12,27), datetime(2022,12,27)
city = "Bogota"
age_group_count_map = get_age_group_count_map(df, start_date, end_date, city, epsilon=1.0)
age_group_sample_size = list(age_group_count_map.values())
age_group_population_distribution =  [8231200, 7334319, 6100177]
contact_matrix = get_contact_matrix(age_group_sample_size, age_group_population_distribution)
print(contact_matrix)
print("pearson_similarity of the estimated contact matrix with the ground truth contact matrix obtained from 'contactdata' R package:"+ str(get_pearson_similarity(contact_matrix)))
