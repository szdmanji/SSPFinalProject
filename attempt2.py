import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_validate
from sklearn import metrics
import matplotlib.pyplot as plt


f = open("phoneme_data3.csv")

# Get the first line of the file, which is the headers indicated which
# information is contained in each column.
featureIDs = f.readline().rstrip().split(",")

# Close the file
f.close()

print("The features are:", featureIDs)
features_df = pd.read_csv("phoneme_data2.csv")
nptarget = features_df['test'].to_numpy()
del features_df['name']
del features_df['test']
del features_df['ENG']
features_df.fillna(0)
npdata = features_df.to_numpy()
print(features_df)
print(npdata)

print("You have ", npdata.shape[0], "training instances")
print("You have ", npdata.shape[1], "features")
print("You have ", nptarget.shape[0], "class labels")

gnb = GaussianNB()

# Select some scoring metrics
scoring_metrics = ['accuracy', 'precision', 'recall', 'f1']

# Train a Naive Bayes model with 5-fold cross validation for the duration feature.

scores = cross_validate(gnb, npdata, nptarget, cv=5, scoring=scoring_metrics)

# Print out each of the metrics for each of the 5 folds and their means.
for score_name, score_value in scores.items():
    print(score_name, score_value, np.mean(score_value))
