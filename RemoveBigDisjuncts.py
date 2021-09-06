class RemoveBigDisjuncts:
    rule_set = None
    data_row_new_array = None
    data_row_array_pass = None
    data_row_correct_clas_array = None
    data_row_wrong_clas_array = None

    data_row_small_disjunct_array = None
    data_row_big_disjunct_array = None

    small_disjunct_class = None

    def __init__(self, rule_set, data_row_array_pass, feature_number, small_disjunct_class,big_disjunct_class):
        self.rule_set = rule_set
        self.feature_number = feature_number
        self.data_row_array_pass = data_row_array_pass
        self.small_disjunct_class = small_disjunct_class
        self.big_disjunct_class = big_disjunct_class

    def remove(self):
        data_row_array = None
        for i in range(0, len(self.rule_set)):
            rule = self.rule_set[i]
            small_disjunct_correct_rate = 0
            big_disjunct_correct_rate = 0
            small_disjunct_correct_classify_number =0
            big_disjunct_correct_classify_number =0

            for j in range(0, len(self.data_row_array_pass)):
                meet_rule_number = 0
                rule_antecedent_number = 0

                data_row_pass = self.data_row_array_pass[j]
                if self.data_row_array_pass[j] == self.small_disjunct_class:
                    self.data_row_small_disjunct_array.append(data_row_pass)
                else:
                    self.data_row_big_disjunct_array.append(data_row_pass)

                for k in range(0, len(rule.antecedent[k])):

                    if rule.antecedent[k] != -1:
                        rule_antecedent_number = rule_antecedent_number + 1

                    if rule.antecedent[k] == data_row_pass.feature_values[k]:
                        meet_rule_number = meet_rule_number + 1

                if meet_rule_number == rule_antecedent_number:
                    if rule.class_value == data_row_pass.class_value:
                        self.data_row_correct_clas_array.append(data_row_pass)
                        if rule.class_value == self.small_disjunct_class:
                            small_disjunct_correct_classify_number =small_disjunct_correct_classify_number + 1
                        elif rule.class_value == self.big_disjunct_class:
                            big_disjunct_correct_classify_number = big_disjunct_correct_classify_number + 1

                    else:
                        self.data_row_wrong_clas_array.append(data_row_pass)

            small_disjunct_correct_rate = small_disjunct_correct_classify_number /len(self.data_row_small_disjunct_array)
            big_disjunct_correct_rate = big_disjunct_correct_classify_number /len(self.data_row_big_disjunct_array)

            if big_disjunct_correct_rate == 1:
                self.remove_big_disjunct()

    def remove_big_disjunct(self):
        for each_row in self.data_row_big_disjunct_array:
            self.data_row_array_pass.remove(each_row)
        return self.data_row_array_pass
