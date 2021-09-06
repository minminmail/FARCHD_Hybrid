from DataRow import DataRow


class Convert:

    def __init__(self):
        pass

    def convert_to_data_row_array(self, train):
        for i in range(0, train.size()):

            class_value = train.get_output_as_integer_with_pos(i)
            example = train.get_example(i)
            example_feature_array = []
            example_feature_array.append(train.get_example(i))
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
