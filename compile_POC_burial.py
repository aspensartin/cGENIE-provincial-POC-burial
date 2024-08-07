import pandas as pd
import matplotlib.pyplot as plt

sim_ages = [0, 2.5, 4.5, 7.5, 10, 12.5, 15]
data = [0, 0, 0, 0, 0, 0, 0]

for i in range(len(sim_ages)):
    data[i] = pd.read_excel('cgenie_provs_{0}.xlsx'.format(sim_ages[i]), usecols=[0, 3])

poc_export = pd.DataFrame({'province': data[0]['province']})
for j in range(len(sim_ages)):
    poc_export = poc_export.join(data[j]['POC_export_rate'], rsuffix=sim_ages[j])

poc_export = poc_export.fillna(0)

poc_export.to_excel('poc_export.xlsx')