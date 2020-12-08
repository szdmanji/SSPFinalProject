import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_validate
from sklearn import metrics
import matplotlib.pyplot as plt

drunk_mfcc_data_path = r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\mfcc_data_drunk.csv"
sober_mfcc_data_path = r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\mfcc_data_sober.csv"
drunk_f0_data_path =  r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\f0_data_drunk.csv"
drunk_f0_data_path =  r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\f0_data_sober.csv"

sober_mfcc_df = pd.read_csv(sober_mfcc_data_path)
drunk_mfcc_df = pd.read_csv(drunk_mfcc_data_path)
drunk_f0_df = pd.read_csv(drunk_f0_data_path)
sober_f0_df = pd.read_csv(drunk_f0_data_path)
all_f0_data = pd.concat([sober_f0_df, drunk_f0_df], ignore_index=True)
print(len(sober_mfcc_df['label']))
print(len(drunk_mfcc_df['label']))

drunk_mfcc_df['label'] = 1
print(drunk_mfcc_df)

new_names = []
for name in drunk_mfcc_df['filename']:
    dex = name.rindex("\\")
    # print(name[dex+1:])
    new_names.append(name[dex+1:])

drunk_mfcc_df['filename'] = new_names
print(drunk_mfcc_df)

new_names = []
for name in sober_mfcc_df['filename']:
    dex = name.rindex("\\")
    # print(name[dex+1:])
    new_names.append(name[dex+1:])

sober_mfcc_df['filename'] = new_names
print(sober_mfcc_df)

new_names = []
for name in all_f0_data['filename']:
    dex = name.rindex("/")
    # print(name[dex+1:])
    new_names.append(name[dex+1:])

all_f0_data['filename'] = new_names
print(all_f0_data)


new_df = pd.concat([sober_mfcc_df, drunk_mfcc_df], ignore_index=True)
print(new_df)
new_df.to_csv('testing_data_initial.csv', index = False)

# for name in new_df['filename']:
#     print(short_name)
#     for temp_name in all_f0_data['filname']

# final_data = pd.merge(all_f0_data, new_df)
# print(final_data)

# final_data.to_csv('final_data.csv', index = False)




# del sober_df['filename']
# del sober_df['label']
#
# # drunk_df = pd.read_csv(drunk_data_path)
# del drunk_df['filename']
# del drunk_df['label']

npdata_sober = sober_mfcc_df.to_numpy()
npdata_drunk = drunk_mfcc_df.to_numpy()
