from DataRow import DataRow
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


class Convert:
    n_variables = 2
    data_base = None
    data_row_array = None
    data_file = ''

    train_data_set = None
    test_data_set = None

    def __init__(self, data_base_pass):
        self.data_base = data_base_pass
        self.data_row_array = []

    def convert_to_data_row_array(self, train):
        for i in range(0, train.size()):

            class_value = train.get_output_as_integer_with_pos(i)
            example_feature_array = []

            example = train.get_example(i)
            example_feature_array = np.array(example)
            """
              example = example.replace('[', '')
              example = example.replace(']', '')
              example_feature_array = example.split(", ")
            """

            print("convert_to_data_row_array,example" + str(example_feature_array))

            """
            for f_variable in range(0, self.n_variables):
                # print("The f_variable is :"+str(f_variable))
                # print("The example is :" + str(example))
                example_feature_array.append(train.get_example(f_variable))
            """

            label_array = []
            for m in range(0, self.n_variables):
                max_value = 0.0
                etq = -1
                per = None
                self.n_labels = self.data_base.num_labels(m)
                # print("n_labels: " + str(self.n_labels))
                for n in range(0, self.n_labels):
                    # print("Inside the second loop of searchForBestAntecedent......")
                    # print("example[" + str(m) + ")]: " + str(example[m]))
                    per = self.data_base.membership_function(m, n, example[m])
                    # print("per: " + str(per))
                    if per > max_value:
                        max_value = per
                        etq = n
                if max_value == 0.0:
                    # print("There was an Error while searching for the antecedent of the rule")
                    # print("Example: ")
                    for n in range(0, self.n_variables):
                        # print(str(example[n]) + "\t")
                        pass

                    # print("Variable " + str(m))
                    exit(1)
                # print(" The max_value is : " + str(max_value))
                # print(" ,the j value is : " + str(j))

                label_array.append(etq)

            data_row_temp = DataRow(class_value, example_feature_array, label_array)
            self.data_row_array.append(data_row_temp)

        return self.data_row_array

    @staticmethod
    def convert_to_file(data_row_array, file_path):
        file_string = 'feature1,feature2,class'+ '\n'
        for i in range(0, len(data_row_array)):
            feature_array = data_row_array[i].feature_values
            for each_feature in feature_array:
                file_string = file_string + str(each_feature) + ','
            if data_row_array[i].class_value == 0:
                class_value = 'green'
            else:
                class_value = 'red'

            file_string = file_string + class_value + '\n'
        file = open(file_path, "w")
        file.write(file_string)
        return file_path

    @staticmethod
    def separate_train_test_files(dataset_name, file_path, train_file_path, test_file_path):
        df = pd.read_csv(file_path)
        training_data, testing_data = train_test_split(df, test_size=0.2, random_state=25)
        training_data.to_csv(train_file_path, index=False, header=False)
        testing_data.to_csv(test_file_path, index=False, header=False)
        train_header = Convert.add_headers_to_train_test_files(dataset_name, train_file_path)
        test_header = Convert.add_headers_to_train_test_files(dataset_name, test_file_path)
        with open(train_file_path, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(train_header + '\n' + content)

        with open(test_file_path, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(test_header + '\n' + content)

    @staticmethod
    def add_headers_to_train_test_files(dataset_name, file_path):

        feature_1 = 0
        feature_2 = 1
        feature_1_min = Convert.get_feature_min(file_path, feature_1)
        feature_1_max = Convert.get_feature_max(file_path, feature_1)
        feature_2_min = Convert.get_feature_min(file_path, feature_2)
        feature_2_max = Convert.get_feature_max(file_path, feature_2)

        data_file_header = "@relation" + dataset_name + '\n'
        data_file_header = data_file_header + "feature1 " + "real [" + str(feature_1_min) + "," + str(
            feature_1_max) + "]" + '\n'
        data_file_header = data_file_header + "feature2 " + "real [" + str(feature_2_min) + "," + str(
            feature_2_max) + "]" + '\n'
        data_file_header = data_file_header + "class " + "{red, green}" + '\n'
        data_file_header = data_file_header + "@inputs  " + "feature1, feature2" + '\n'
        data_file_header = data_file_header + "@outputs  " + "class" + '\n'
        data_file_header = data_file_header + "@data"

        return data_file_header

    @staticmethod
    def get_feature_min(file_path, column_number):
        feature_min = -1
        df = pd.read_csv(file_path)
        feature_min = df.iloc[column_number].min()

        return feature_min

    @staticmethod
    def get_feature_max(file_path, column_number):
        feature_max = -1
        df = pd.read_csv(file_path)
        feature_max = df.iloc[column_number].max()

        return feature_max
