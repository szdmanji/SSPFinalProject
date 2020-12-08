import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_validate
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
# import matplotlib.pyplot as plt

f = open("//Users/eandrade/Boston College/2020-2021/CSCI3398/SSPFinalProject/testing_data_initial.csv")

# Get the first line of the file, which is the headers indicated which
# information is contained in each column.
featureIDs = f.readline().rstrip().split(",")
print("The features are:", featureIDs)
# Close the file
f.close()


features = pd.read_csv("/Users/eandrade/Boston College/2020-2021/CSCI3398/SSPFinalProject/testing_data_initial.csv")
nptarget = features['label'].to_numpy()
del features['filename']
del features['label']
# print(features)
npdata = features.to_numpy()

print("You have ", npdata.shape[0], "training instances")
print("You have ", npdata.shape[1], "features")
print("You have ", nptarget.shape[0], "class labels")

count_sober = 0
count_drunk = 0
# sober  - label 0 | drunk - label 1
for x in nptarget:
    if x == 0: count_sober = count_sober + 1
    else: count_drunk = count_drunk + 1

print('')
print("The number of sober samples is: " + str(count_sober))
print("The number of drunk samples is: " + str(count_drunk))

maj_baseline = round(count_drunk/(count_drunk+count_sober), 2)
print("The majority baseline is:", maj_baseline)

out_val = float(input("Hold out %: "))
iter = int(input("Iterations: "))

held_out = int(out_val * (count_sober + count_drunk))
print("Held out samples -", out_val,"% of total:", held_out)
# testid = [1, 1]
# track = 0
# # while len(testid) != len(set(testid)):
# #     testid = np.random.randint(0, npdata.shape[0], held_out)
# #     track += 1
# #     if track % 10 == 0:
# #         print(track)

GNB = GaussianNB()
DT = DecisionTreeClassifier()
RF = RandomForestClassifier()

methods = [GNB, DT, RF]
for method in methods:
    print(str(method), end="...")
    count = 0
    sim_average_0 = []
    sim_average_1 = []
    while count < iter:
        # held out data
        testid = [1, 1]
        while len(testid) != len(set(testid)):
            testid = np.random.randint(0, npdata.shape[0], held_out)
        # Get testing and training  data
        testset = npdata[testid, :]
        testtarget = nptarget[testid]
        trainset = np.delete(npdata, testid, 0)
        traintarget = np.delete(nptarget, testid, 0)

        # Build model and apply GNB model
        model = method
        model.fit(trainset, traintarget)
        expected = testtarget
        predicted = model.predict(testset)

        # classification report
        report = metrics.classification_report(expected, predicted, output_dict=True)
        # append to the simulation average
        sim_average_0.append(report['0'])
        sim_average_1.append(report['1'])
        count += 1
        if count % 10 == 0:
            print(count, end="...")
    # print(sim_average_0)

    sum_p_0, sum_r_0, sum_f1_0 = 0, 0, 0
    for run in sim_average_0:
        sum_p_0 += run['precision']
        sum_r_0 += run['recall']
        sum_f1_0 += run['f1-score']
    avg_p_0 = sum_p_0 / len(sim_average_0)
    avg_r_0 = sum_r_0 / len(sim_average_0)
    avg_f1_0 = sum_f1_0 / len(sim_average_0)

    sum_p_1, sum_r_1, sum_f1_1 = 0, 0, 0
    for run in sim_average_1:
        sum_p_1 += run['precision']
        sum_r_1 += run['recall']
        sum_f1_1 += run['f1-score']
    avg_p_1 = sum_p_1 / len(sim_average_1)
    avg_r_1 = sum_r_1 / len(sim_average_1)
    avg_f1_1 = sum_f1_1 / len(sim_average_1)

    print("\nAverage Metrics: Precision | Recall | F1-Score ")
    print(round(avg_p_0, 4), round(avg_r_0, 4), round(avg_f1_0, 4))
    print(round(avg_p_1, 4), round(avg_r_1, 4), round(avg_f1_1, 4))
