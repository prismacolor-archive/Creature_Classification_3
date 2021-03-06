import matplotlib.pyplot as plt
import numpy
import os
import pandas

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

base_path = os.getcwd()
data_path = base_path + '\\datasets\\'

creatures_file = r'datasets\creatures_data_set.csv'
creatures_extract = pandas.read_csv(creatures_file)
# you can also read from json and excel files
creatures_df = pandas.DataFrame(creatures_extract)

creatures_test_file = r'datasets\creatures_test_set.csv'
creatures_test_extract = pandas.read_csv(creatures_test_file)
creatures_test_df = pandas.DataFrame(creatures_test_extract)

creatures_test_file2 = r'datasets\creatures_test_set2.csv'
creatures_test_extract2 = pandas.read_csv(creatures_test_file2)
creatures_test_df2 = pandas.DataFrame(creatures_test_extract2)


def clean_data(some_dataframe):
    # print(some_dataframe.head())
    # get a snapshot of the data to see what you need and don't need
    del some_dataframe['Number']

    # you need all numerical data for this classification model
    environment_mappings = {'air': 0, 'cave': 1, 'desert': 2, 'swamp': 3, 'volcanoes': 4,
                            'water': 5, 'woods': 6, 'mountain': 7}
    creature_mappings = {'Dragon': 0, 'Drake': 1, 'Flying Serpent': 2, 'Serpent': 3, 'Wyrm': 4, 'Wyvern': 5}
    gender_encoder = preprocessing.LabelEncoder()

    some_dataframe.Gender = gender_encoder.fit_transform(some_dataframe.Gender)
    some_dataframe.Environment = some_dataframe.Environment.map(environment_mappings)
    some_dataframe.Classification = some_dataframe.Classification.map(creature_mappings)

    return some_dataframe


def make_tree_model(some_dataframe):
    X = some_dataframe.iloc[:, 0: -1]
    y = some_dataframe.iloc[:, -1]
    X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    creatures_model = tree.DecisionTreeClassifier().fit(X_train, y_train)

    plt.figure()
    tree.plot_tree(creatures_model)
    plt.show()

    y_pred = creatures_model.predict(x_test)

    creatures_model.predict(x_test)
    creatures_score = creatures_model.score(x_test, y_test)

    # print(confusion_matrix(y_test, y_pred))
    # print(classification_report(y_test, y_pred))
    print(creatures_score)

    return creatures_model


def make_random_forest(some_dataframe):
    X = some_dataframe.iloc[:, 0: -1]
    y = some_dataframe.iloc[:, -1]
    X_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    forest_model = RandomForestClassifier(n_estimators=100, random_state=33)
    forest_model.fit(X_train, y_train)

    forest_model.predict(x_test)
    forest_score = forest_model.score(x_test, y_test)

    print(forest_score)

    return forest_model


def test_model(model, dataframe):
    X = dataframe.iloc[:, 0: -1]
    y = dataframe.iloc[:, -1]

    pred_y = model.predict(X)

    # print(classification_report(y, pred_y))
    print(accuracy_score(y, pred_y))


cleaned_dataframe = clean_data(creatures_df)
tree_model_1 = make_tree_model(cleaned_dataframe)
forest_model_1 = make_random_forest(cleaned_dataframe)

cleaned_dataframe2 = clean_data(creatures_test_df)
test_model(tree_model_1, cleaned_dataframe2)
test_model(forest_model_1, cleaned_dataframe2)

cleaned_dataframe3 = clean_data(creatures_test_df2)
test_model(tree_model_1, cleaned_dataframe3)
test_model(forest_model_1, cleaned_dataframe3)

# Last run 5/20/20: Test set accuracy with decision tree = 99.87%, accuracy with random forest = 99.92%
# training set was 98%
# 2nd test set was 97%
