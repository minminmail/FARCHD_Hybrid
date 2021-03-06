# -*- coding: utf-8 -*-
"""
This is a module to be used as a reference for building other modules
"""

from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels

from Apriori import Apriori
from DataBase import DataBase
from MyDataSet import MyDataSet
import datetime
import random
import os
import time

from Populate import Populate
from RuleBase import RuleBase
import numpy as np
from Logger import Logger
from sklearn.metrics import accuracy_score
from Convert import Convert


class FarcHDSmallDisjunctClassifier:
    """ A template estimator to be used as a reference implementation.

    For more information regarding how to build your own estimator, read more
    in the :ref:`User Guide <user_guide>`.

    Parameters
    ----------
    number_of_labels : int, how many classes need to classification
    combination_type : int，1 (PRODUCT),0 (MINIMUM)  T-norm for the Computation of the Compatibility Degree
    rule_weight : int,1 (PCF_IV	，Penalized_Certainty_Factor),0(CF，Certainty_Factor),
                      3(PCF_II，Average_Penalized_Certainty_Factor),3(NO_RW，No_Weights)
    inference_type : 0 ( WINNING_RULE, WINNING_RULEWinning_Rule), 1(ADDITIVE_COMBINATION,Additive_Combination)
          Fuzzy Reasoning Method
    ranges : [[0.0 for y in range (2)] for x in range nVars], nVars=self.__nInputs + Attributes.getOutputNumAttributes(Attributes)


    example :
        Number of Labels = 3
        T-norm for the Computation of the Compatibility Degree = Product
        Rule Weight = Penalized_Certainty_Factor
        Fuzzy Reasoning Method = Winning_Rule
        ranges = [[0.0 for y in range (2)] for x in range 4]
                 [4,3         7.9
                  2.0         4.4
                  1.0         6.9
                  0.1         2.5]


    """

    # algorithm parameters
    # int
    number_of_labels = 0
    population_size = 0
    depth = 0
    k_parameter = 0
    max_trials = 0
    type_inference = 0
    bits_gen = 0

    minsup = 0.0
    minconf = 0.0
    alpha = 0.0
    something_wrong = False

    train_mydataset = None
    val_mydataset = None
    test_mydataset = None

    output_tr = ""
    output_tst = ""

    file_db = ""
    file_rb = ""
    file_time = ""
    file_hora = ""
    data_string = ""
    file_rules = ""
    evolution = ""

    rules_stage1 = 0
    rules_stage2 = 0
    rules_stage3 = 0

    data_base = None
    rule_base = None

    apriori = None

    pop = None
    start_time = 0
    total_time = 0

    # algorithm parameters
    # int
    nlabels = 0
    negative_confident_value = 0
    negative_rule_number = None
    zone_confident = 0.2
    seed_int = None
    granularity_rule_Base_array = []
    normal_rule_degree = None
    max_granularity_degree = None
    logger = None
    big_disjunct_class = None
    small_disjunct_class = None
    big_disjunct_class_accuracy = 0
    small_disjunct_class_accuracy = 0
    big_disjunct_instance_number = 0
    small_disjunct_instance_number = 0
    big_disjunct_predict_correct_number = 0
    small_disjunct_predict_correct_number = 0
    imbalance_rate = 0
    small_disjunct_imbalance_rate_accuracy = 0
    big_disjunct_imbalance_rate_accuracy = 0
    whole_imbalance_rate_accuracy = 0

    def __init__(self, prepare_parameter, big_disjunct_class='green', small_disjunct_class='red'):
        print("__init__ of Fuzzy_Chi begin...")
        self.logger = Logger.set_logger()
        self.start_time = datetime.datetime.now()

        self.train_mydataset = MyDataSet()
        self.val_mydataset = MyDataSet()
        self.test_mydataset = MyDataSet()
        self.big_disjunct_class = big_disjunct_class
        self.small_disjunct_class = small_disjunct_class

        try:

            input_training_file = prepare_parameter.get_input_training_files()
            print("Reading the training set: " + input_training_file)

            self.train_mydataset.read_classification_set(input_training_file, True,prepare_parameter.data_main_folder ,prepare_parameter.dataset_folder_name)
            print("Reading the validation set: ")
            input_validation_file = prepare_parameter.get_validation_input_file()
            self.val_mydataset.read_classification_set(input_validation_file, True,prepare_parameter.data_main_folder , prepare_parameter.dataset_folder_name)
            print("Reading the test set: ")
            self.test_mydataset.read_classification_set(prepare_parameter.get_input_test_files(), False, prepare_parameter.data_main_folder,prepare_parameter.dataset_folder_name)
            print(" ********* test_mydataset.myDataSet read_classification_set finished !!!!!! *********")

        except IOError as ioError:
            print("I/O error: " + str(ioError))
            self.something_wrong = True
        except Exception as e:
            print("Unexpected error:" + str(e))
            self.something_wrong = True

        self.something_wrong = self.something_wrong or self.train_mydataset.has_missing_attributes()
        file_output_tr = prepare_parameter.get_training_output_file()
        file_output_tst = prepare_parameter.get_test_output_file()

        output_file_folder = "smalldijunctsresults"

        file_db_name = prepare_parameter.get_output_file(0)
        file_rb_name = prepare_parameter.get_output_file(1)

        self.file_db = os.path.join(prepare_parameter.result_path, output_file_folder + "\\" + file_db_name)

        self.file_rb = os.path.join(prepare_parameter.result_path, output_file_folder + "\\" + file_rb_name)

        self.output_tr = os.path.join(prepare_parameter.result_path, output_file_folder + "\\" + file_output_tr)
        self.output_tst = os.path.join(prepare_parameter.result_path, output_file_folder + "\\" + file_output_tst)

        self.file_db = os.getcwd() + "\\" + self.file_db
        self.file_rb = os.getcwd() + "\\" + self.file_rb

        self.output_tr = os.getcwd() + "\\" + self.output_tr

        self.output_tst = os.getcwd() + "\\" + self.output_tst

        self.data_string = prepare_parameter.get_input_training_files()

        output_file = prepare_parameter.get_output_file(1)
        # print("output_file is : " + output_file)

        self.file_time = os.getcwd() + "\\" + prepare_parameter.result_path + "\\" + output_file_folder + "\\" + "time.txt"
        self.file_hora = os.getcwd() + "\\" + prepare_parameter.result_path + "\\" + output_file_folder + "\\" + "hora.txt"
        self.file_rules = os.getcwd() + "\\" + prepare_parameter.result_path + "\\" + output_file_folder + "\\" + "rules.txt"
        # Now we parse the parameters long
        self.seed_int = int(float(prepare_parameter.get_parameter(0)))

        self.nlabels = int(prepare_parameter.get_parameter(1))
        self.minsup = float(prepare_parameter.get_parameter(2))
        self.minconf = float(prepare_parameter.get_parameter(3))
        self.depth = int(prepare_parameter.get_parameter(4))
        self.k_parameter = int(prepare_parameter.get_parameter(5))
        self.max_trials = int(prepare_parameter.get_parameter(6))
        self.population_size = int(prepare_parameter.get_parameter(7))
        if self.population_size % 2 > 0:
            self.population_size = self.population_size + 1
        self.alpha = float(prepare_parameter.get_parameter(8))
        self.bits_gen = int(prepare_parameter.get_parameter(9))
        self.type_inference = int(prepare_parameter.get_parameter(10))
        # javarandom.Random(self.seed_int)
        self.output = None
        random.seed(self.seed_int)

    def fit(self, X, y):
        """A reference implementation of a fitting function.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.
        y : array-like, shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels in classification, real numbers in
            regression).
        In fit function it will generate the rules and store it
        Returns
        -------
        self : object
            Returns self.
        """
        print(X.shape)
        print(y.shape)
        # y = y.reshape(-1,1)
        # print(y.shape)
        X, y = check_X_y(X, y, accept_sparse=True, ensure_2d=False)
        self.is_fitted_ = True

        # Store the classes seen during fit
        self.classes_ = unique_labels(y)

        self.X_ = X
        self.y_ = y

        if self.something_wrong:  # We do not execute the program
            print("An error was found, the data-set have missing values")
            print("Please remove the examples with missing data or apply a MV preprocessing.")
            print("Aborting the program")
        # We should not use the statement: System.exit(-1);
        else:
            print("No errors, Execute in FarcHD execute :")
            self.data_base = DataBase()
            self.data_base.init_with_three_parameters(self.nlabels, self.train_mydataset)
            self.rule_base = RuleBase(self.data_base, self.train_mydataset, self.k_parameter, self.type_inference)
            self.apriori = Apriori()
            self.apriori.multiple_init(self.rule_base, self.data_base, self.train_mydataset, self.minsup, self.minconf,
                                       self.depth)
            self.apriori.generate_rb()
            self.rules_stage1 = self.apriori.get_rules_stage1()
            self.rules_stage2 = self.rule_base.get_size()
            print("self.rules_stage1")
            print(self.rules_stage1)
            print("self.rules_stage2")
            print(self.rules_stage2)

            self.pop = Populate()

            self.pop.init_with_multiple_parameters(self.seed_int, self.train_mydataset, self.data_base, self.rule_base,
                                                   self.population_size, self.bits_gen, self.max_trials, self.alpha)
            self.pop.generation()

            print("Building classifier")
            self.rule_base = self.pop.get_best_RB()

            # calculate the rule suppx,suppxy,for check small disjuncts
            self.rule_base.prepare_data_rows(self.train_mydataset)
            self.rule_base.calculate_confident_support_rulebase(self.train_mydataset)
            self.rule_base.reduce_low_accurate_rules(2)

            rule_log = ""
            for i in range(0, len(self.rule_base.rule_base_array)):
                rule_log = rule_log + self.rule_base.rule_base_array[i].print_rule_information(
                    self.rule_base.n_variables, self.train_mydataset)

            self.logger.debug("Rule information log is  :" + " /n " + rule_log)

            self.rules_stage3 = int(self.rule_base.get_size())

            self.rule_base.generate_negative_rules_by_rule_cover_number(self.train_mydataset,
                                                                        self.negative_confident_value,
                                                                        self.zone_confident)

            self.negative_rule_number = len(self.rule_base.negative_rule_base_array)

            print("Begin the  negative rule generation ")
            print("self.file_db is :" + self.file_db)
            self.data_base.save_file(self.file_db)
            self.rule_base.save_file(self.file_rb, False)

            print("Begin the  granularity rule generation ")
            print("self.nlabels " + str(self.nlabels))

            """    

            granularity_rule = GranularityRule(self.train_mydataset, self.nlabels,
                                               self.file_db, self.file_rb, self.val_mydataset,
                                               self.output_tr, self.output_tst, self.rule_base, self.k_parameter,
                                               self.data_base, self.test_mydataset,
                                               self.val_mydataset, self.type_inference, self.minsup, self.minconf,
                                               self.depth, self.seed_int, self.population_size, self.bits_gen,
                                               self.alpha, self.max_trials)

            self.granularity_rule_Base_array = granularity_rule.get_granularity_rules(self.negative_rule_number)

            """

            #  Finally we should fill the training and test  output files
            self.do_output(self.val_mydataset, self.output_tr)
            self.do_output(self.test_mydataset, self.output_tst)

            current_millis = int(round(time.time() * 1000))

            # int(datetime.datetime.utcnow().timestamp())

            self.total_time = current_millis - int(self.start_time.utcnow().timestamp())
            print("Algorithm self.total_time is :" + str(self.total_time))
            self.write_time()
            self.write_rules()

            print("Algorithm Finished")

            # Return the classifier
            return self

    def write_rules(self):

        string_out = "" + str(self.rules_stage1) + " " + str(self.rules_stage2) + " " + str(self.rules_stage3) + "\n"

        file = open(self.file_rules, "a+")
        file.write(string_out)

    # """
    #    * It generates the output file from a given dataset and stores it in a file
    #    * @param dataset myDataset input dataset
    #    * @param filename String the name of the file
    #    *
    #    * @return The classification accuracy
    # """

    def write_time(self):
        aux = None  # int
        seg = None  # int
        min_value = None  # int
        hor = None  # int

        string_out = "" + str(self.total_time / 1000) + "  " + self.data_string + "\n"
        file = open(self.file_time, "a+")
        file.write(string_out)
        self.total_time /= 1000
        seg = self.total_time % 60
        self.total_time = self.total_time / 60
        min_value = self.total_time % 60
        hor = self.total_time / 60
        string_out = ""

        if hor < 10:
            string_out = string_out + "0" + str(hor) + ":"
        else:
            string_out = string_out + str(hor) + ":"

        if min_value < 10:
            string_out = string_out + "0" + str(min_value) + ":"
        else:
            string_out = string_out + str(min_value) + ":"

        if seg < 10:
            string_out = string_out + "0" + str(seg)
        else:
            string_out = string_out + str(seg)

        string_out = string_out + "  " + self.data_string + "\n"

        file = open(self.file_hora, "a+")
        file.write(string_out)

    def do_output(self, mydataset, filename):

        self.big_disjunct_class_accuracy = 0
        self.small_disjunct_class_accuracy = 0
        self.big_disjunct_instance_number = 0
        self.small_disjunct_instance_number = 0
        self.big_disjunct_predict_correct_number = 0
        self.small_disjunct_predict_correct_number = 0

        output = mydataset.copy_header()  # we insert the header in the output file
        # We write the output for each example
        for i in range(0, mydataset.get_ndata()):
            # for classification:
            original_class = mydataset.get_output_as_string_with_pos(i)
            predict_class = self.classification_output_string(mydataset.get_example(i))

            output = output + original_class + " " + predict_class + "\n"
            if original_class == self.big_disjunct_class:
                self.big_disjunct_instance_number = self.big_disjunct_instance_number + 1
                if predict_class == original_class:
                    self.big_disjunct_predict_correct_number = self.big_disjunct_predict_correct_number + 1
            elif original_class == self.small_disjunct_class:
                self.small_disjunct_instance_number = self.small_disjunct_instance_number + 1
                if predict_class == original_class:
                    self.small_disjunct_predict_correct_number = self.small_disjunct_predict_correct_number + 1

        if os.path.isfile(filename):
            # print("File exist")
            output_file = open(filename, "a+")
        else:
            # print("File not exist")
            output_file = open(filename, "w+")
        if self.big_disjunct_instance_number==0:
            self.big_disjunct_class_accuracy = -1
        else:
            self.big_disjunct_class_accuracy = self.big_disjunct_predict_correct_number / self.big_disjunct_instance_number
        if self.small_disjunct_instance_number ==0:
            self.small_disjunct_class_accuracy=-1
        else:
            self.small_disjunct_class_accuracy = self.small_disjunct_predict_correct_number / self.small_disjunct_instance_number

        if self.small_disjunct_instance_number ==0:
            self.imbalance_rate = -1
        else:
            self.imbalance_rate = self.big_disjunct_instance_number / self.small_disjunct_instance_number

        percentage_ir = self.big_disjunct_instance_number / (
                self.big_disjunct_instance_number + self.small_disjunct_instance_number)

        self.small_disjunct_imbalance_rate_accuracy = self.small_disjunct_class_accuracy * percentage_ir
        self.big_disjunct_imbalance_rate_accuracy = self.big_disjunct_class_accuracy * (1 - percentage_ir)
        self.whole_imbalance_rate_accuracy = self.small_disjunct_imbalance_rate_accuracy + self.big_disjunct_imbalance_rate_accuracy
        output = output + "The big disjunct accuracy is :" + str(self.big_disjunct_class_accuracy) + "\n"
        output = output + "The small disjunct accuracy is :" + str(self.small_disjunct_class_accuracy) + "\n"
        output = output + "The whole_imbalance_rate_accuracy accuracy is :" + str(
            self.whole_imbalance_rate_accuracy) + "\n"
        output_file.write(output)

    # * It returns the algorithm classification output given an input example
    # * @param example double[] The input example
    # * @return String the output generated by the algorithm

    def classification_output(self, example, row_index):
        output = "?"
        # Here we should include the algorithm directives to generate the
        # classification output from the input example

        class_out = self.rule_base.FRM(example, row_index)
        """ 
        if class_out >= 0:
            output = self.train_mydataset.get_output_value(class_out)
        """
        self.normal_rule_degree = self.rule_base.frm_ac_max_degree_value

        return class_out

    def classification_output_string(self, example, row_index=999):
        output = "?"
        # Here we should include the algorithm directives to generate the
        # classification output from the input example

        class_out = self.rule_base.FRM(example, row_index)

        if class_out >= 0:
            output = self.train_mydataset.get_output_value(class_out)

        self.normal_rule_degree = self.rule_base.frm_ac_max_degree_value

        return output

    """ 
     * Add all the rules generated by the classifier to fileRules file.
     """

    def write_score(self, score_string):
        file = open(self.file_rules, "a+")
        file.write(score_string)

    def predict(self, X):
        """ A reference implementation of a predicting function.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The label for each sample is the label of the closest sample
            seen udring fit.
        """

        # Input validation
        X = check_array(X, accept_sparse=True)

        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'], 'is_fitted_')

        row_num = X.shape[0]
        predict_y = np.empty([row_num, 1], dtype=str)  # dtype=np.int32

        for i in range(0, row_num):
            predict_y[i] = self.classification_output(X[i], i)
        print("normal rule ,predict_y is :")
        print(predict_y)

        self.rule_base.save_file(self.file_rb, True)

        return predict_y

    def predict_granularity(self, X):
        """ A reference implementation of a predicting function.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The label for each sample is the label of the closest sample
            seen udring fit.
        """

        # Input validation
        X = check_array(X, accept_sparse=True)

        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'], 'is_fitted_')

        row_num = X.shape[0]
        print("row_num is :" + str(row_num))
        predict_y = np.empty([row_num, 1], dtype=np.int32)
        selected_array = None

        count_granularity_result = 0
        count_normalrule_result = 0

        for i in range(0, row_num):

            class_out_here = None

            max_granularity_count = 0  # save the max degree of granularity rule result
            get_granularity_rule_result = False

            print("row = " + str(i) + "began predict")

            for j in range(0, self.negative_rule_number):
                print("before classification_Output_granularity")

                classOut = self.classification_Output_granularity(X[i], j)
                degree_new = self.max_granularity_degree

                print("after classification_Output_granularity")
                # classOut = self.classification_Output_pruned_granularity(dataset.getExample(i), j)
                if classOut is not "?" and classOut is not None:

                    if degree_new is not None and degree_new > max_granularity_count:
                        print(str(i) + " negative rule ,degree new is " + str(degree_new))
                        get_granularity_rule_result = True
                        class_out_here = classOut
                        print(" class_out_here is " + str(class_out_here))

                        max_granularity_degree = degree_new
                        print(" max_granularity_count is " + str(max_granularity_count))

            if get_granularity_rule_result and max_granularity_degree > 3:  #

                count_granularity_result = count_granularity_result + 1
                print("count_granularity_result is: " + str(
                    count_granularity_result) + " ,max_granularity_degree is :" + str(
                    max_granularity_degree))
            else:
                count_normalrule_result = count_normalrule_result + 1
                print("In predict_granularity count_normalrule_result is " + str(count_normalrule_result))
                class_out_here = self.classification_output(X[i])
                normal_rule_degree = self.normal_rule_degree
                print(" normal_rule_degree is " + str(normal_rule_degree))

            predict_y[i, 0] = class_out_here
            print(" finally the predict y  is " + str(predict_y[i, 0]))

        granularity_score_string = "\n\n" + "count_granularity_result score is: " + str(count_granularity_result)
        print(granularity_score_string)
        self.write_score(granularity_score_string)
        normal_score_string = "\n\n" + "count_normal_result score is: " + str(count_normalrule_result)
        print(normal_score_string)
        self.write_score(normal_score_string)
        return predict_y

    def classification_Output_granularity(self, example, zone_area_number):
        self.output = "?"

        # Here we should include the algorithm directives to generate the
        # classification output from the input example
        print("before FRM_Granularity")
        selected_array = None
        self.output = self.granularity_rule_Base_array[zone_area_number].frm_ac_with_two_parameters(example,
                                                                                                    selected_array)

        self.max_granularity_degree = self.granularity_rule_Base_array[zone_area_number].frm_ac_max_degree_value
        print("in classification_Output_granularity  max_granularity_degree is " + str(self.max_granularity_degree))

        return self.output

    def score(self, y_true, y_pred, if_granularity, if_train):
        """ A reference implementation of score function.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            The test input samples.

        Returns
        -------
        y : ndarray, shape (n_samples,)
            The label for each test sample is the label of the closest test sample
            seen udring fit.
        """

        """
        # Input validation
        real_X = check_array(real_X, accept_sparse=True)

        # Check is fit had been called
        check_is_fitted(self, ['X_', 'y_'], 'is_fitted_')

        row_num = real_X.shape[0]
        print("row_num in score is :" + str(row_num))
        
   """

        if if_granularity:
            if if_train:
                score_string = " \n\n " + "with granularity rules ,the train's   accuracy_score is :"
                print("accuracy_score with granularity rules ,the  score is :")
            else:

                score_string = " \n\n " + "with granularity rules ,the test's accuracy_score is :"
                print("accuracy_score with granularity rules ,the  score is :")
        else:
            if if_train:
                score_string = " \n\n " + "with normal rules ,the train's accuracy_score is :"
                print("accuracy_score with normal rules ,the  score is :")
            else:

                score_string = "\n\n" + "with normal rules ,the test's accuracy_score is :"
                print("accuracy_score with normal rules ,the score is :")
        # score = 1.0 * hits / row_num
        y_pred_int = []
        for i in range(0, len(y_pred)):
            y_pred_int.append(int(y_pred[i]))

        score = accuracy_score(y_true, y_pred_int)
        score_string = score_string + str(score)
        self.write_score(score_string)
        self.calculate_rule_accurate(y_true, y_pred_int)
        print(score)

        return score

    def get_X(self):

        self.X = self.train_mydataset.get_X()
        # change into ndarray type
        self.X = np.array(self.X)
        print(self.X)

        return self.X

    def get_y(self):

        self.y = self.train_mydataset.get_y()
        self.y = np.array(self.y)
        print(self.y)

        return self.y

    def get_test_x(self):

        self.X = self.test_mydataset.get_X()
        # change into ndarray type
        self.X = np.array(self.X)
        print(self.X)

        return self.X

    def get_test_y(self):

        self.y = self.test_mydataset.get_y()
        self.y = np.array(self.y)
        print(self.y)

        return self.y

    def calculate_rule_accurate(self, y_true, y_pred_int):
        row_num = len(y_true)
        rule_num = len(self.rule_base.rule_base_array)
        rule_sum_error_arr = [0] * rule_num
        error_rate_string = ""
        for i in range(0, row_num):

            if not (y_true[i] == y_pred_int[i]):
                sum_degree = 0
                rule_accurate_array = [0] * rule_num
                rule_degree = [0] * rule_num
                for rule_index, degree in self.rule_base.data_row_array[i].rule_degree_dic.items():
                    sum_degree = sum_degree + degree
                    rule_degree[rule_index] = degree

                for rule_index, degree in self.rule_base.data_row_array[i].rule_degree_dic.items():
                    rule_accurate_array[rule_index] = rule_degree[rule_index] / sum_degree
                    rule_sum_error_arr[rule_index] = rule_sum_error_arr[rule_index] + rule_accurate_array[rule_index]
        for k in range(0, rule_num):
            print("rule index number :" + str(k) + " ,  and the error rate :" + str(rule_sum_error_arr[k]))
            error_rate_string = error_rate_string + "rule index number :" + str(k) + " ,  and the error rate :" + str(
                rule_sum_error_arr[k])

        file = open(self.file_rules, "a+")
        file.write(error_rate_string)

    @staticmethod
    def data_row_to_train_test_files(data_set_folder, data_row_array_new, file_path, train_file_path, test_file_path):
        data_file = Convert.convert_to_file(data_row_array_new, file_path)
        Convert.separate_train_test_files(data_set_folder, data_file, train_file_path, test_file_path)
