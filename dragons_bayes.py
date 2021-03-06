'''A critter classification script'''

import numpy
import pandas

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB


# retrieving the data from the spreadsheet TR
creatures_file = r'datasets\creatures_data_set.csv'
creatures_extract = pandas.read_csv(creatures_file)
creatures_df = pandas.DataFrame(creatures_extract)

# prep the test set TR
test_file = r'datasets\creatures_test_set.csv'
test_extract = pandas.read_csv(test_file)
test_df = pandas.DataFrame(test_extract)

# prep the second test set TR
test_file2 = r'datasets\creatures_test_set2.csv'
test_extract2 = pandas.read_csv(test_file2)
test_df2 = pandas.DataFrame(test_extract2)


# need to adjust final column to be numbers only TR
def adjust_data(my_dataframe):
    # delete unnecessary columns
    del my_dataframe['Number']

    # use label encoder to create numerical values for gender: Tr
    gender_encoder = preprocessing.LabelEncoder()

    # use custom encodings for other categorical data TR
    environment_mappings = {'air': 0, 'cave': 1, 'desert': 2, 'swamp': 3, 'volcanoes': 4, 'water': 5, 'woods': 6,
                            'mountain': 7}
    creature_mappings = {'Dragon': 0, 'Drake': 1, 'Flying Serpent': 2, 'Serpent': 3, 'Wyrm': 4, 'Wyvern': 5}

    my_dataframe.Gender = gender_encoder.fit_transform(my_dataframe.Gender)
    my_dataframe.Environment = my_dataframe.Environment.map(environment_mappings)
    my_dataframe.Classification = my_dataframe.Classification.map(creature_mappings)

    return my_dataframe


def classify_data(data_frame):
    # first create the training data for the model  TR
    X = data_frame.iloc[:, 0: -1]
    y = data_frame.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=33)

    # print(X_train, X_test, y_train, y_test)

    # create the classification model   TR
    the_model = GaussianNB().fit(X_train, y_train)

    # test out the model TR
    predicted = the_model.predict(X_test)

    # print(y_test)
    # print(predicted)
    print(numpy.mean(predicted == y_test))
    print("Total points: ", (X_test.shape[0], "Mislabelled: ", (y_test != predicted).sum()))

    return the_model


def test_data(data_frame, model):
    X = data_frame.iloc[:, 0: -1]
    y = data_frame.iloc[:, -1]
    predicted2 = model.predict(X)

    # print(numpy.mean(predicted2 == y))
    print("Total points: ", (X.shape[0], "Mislabelled: ", (y != predicted2).sum()))


# create initial model
creatures_fitted_df = adjust_data(creatures_df)
my_model = classify_data(creatures_fitted_df)

# test it out
adjusted_test_data = adjust_data(test_df)
test_data(adjusted_test_data, my_model)

# try another test
# test it out
adjusted_test_data2 = adjust_data(test_df2)
test_data(adjusted_test_data2, my_model)

# final results: 0.9908979089790898
# Total points:  (4065, 'Mislabelled: ', 37)
# Total points:  (50, 'Mislabelled: ', 1)
# Total points:  (35, 'Mislabelled: ', 1)
