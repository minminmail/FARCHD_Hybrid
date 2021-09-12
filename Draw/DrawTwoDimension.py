# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path


class DrawTwoDimension:
    big_disjunct_file = ""
    small_disjunct_file = ""
    train_data_row_array = []
    dataset_folder = ""
    after_remove = False

    def __init__(self, train_data_row_array_pass, dataset_folder='data3',after_remove=False):
        self.train_data_row_array = train_data_row_array_pass
        self.dataset_folder = dataset_folder
        self.after_remove = after_remove

    def generate_files(self, small_disjunct_class):

        data_folder = 'dataset'
        cwd = Path.cwd()
        dataset_folder = self.dataset_folder
        if self.after_remove:
            self.small_disjunct_file = cwd / dataset_folder / data_folder / 'data_small_2.dat'
            self.big_disjunct_file = cwd / dataset_folder / data_folder / 'data_big_2.dat'
            open(self.small_disjunct_file, "x")

        else:
            self.small_disjunct_file = cwd / dataset_folder / data_folder / 'data_small.dat'
            self.big_disjunct_file = cwd / dataset_folder / data_folder / 'data_big.dat'
            open(self.big_disjunct_file, "x")

        small_disjunct_data_string = ''
        big_disjunct_data_string = ''
        for each_row in self.train_data_row_array:
            if each_row.class_value == small_disjunct_class:
                small_disjunct_data_string = small_disjunct_data_string + self.get_data_row_string(each_row)
            else:
                big_disjunct_data_string = big_disjunct_data_string + self.get_data_row_string(each_row)

        small_disjunct_file = open(self.small_disjunct_file, "w")
        small_disjunct_file.write(small_disjunct_data_string)
        small_disjunct_file.close()

        big_disjunct_file = open(self.big_disjunct_file, "w")
        big_disjunct_file.write(small_disjunct_data_string)
        big_disjunct_file.close()

    @staticmethod
    def get_data_row_string(data_row):
        data_row_string = ''
        for each_feature in data_row.feature_values:
            data_row_string = data_row_string + str(each_feature) + ' '
        data_row_string = data_row_string + str(data_row.class_value) + '/n '
        return data_row_string

    def paint(self):
        print("begin to paint")

        file_path1 = self.big_disjunct_file

        df = pd.read_csv(file_path1, names=["x", "y", "class"])
        plt.rcParams['figure.figsize'] = (6, 4)
        plt.rcParams['figure.dpi'] = 150

        columnx = df['x']
        columny = df['y']

        fig, ax = plt.subplots()
        ax.scatter(columnx, columny, marker='o', color='g', s=50)

        file_path2 = self.small_disjunct_file
        df = pd.read_csv(file_path2, names=["x", "y", "class"])
        columnx = df['x']
        columny = df['y']

        ax.scatter(columnx, columny, marker='^', color='r', s=50)

        line_y1 = 4
        line_y2 = 8
        line_y3 = 12
        x1_values = [0, 16]
        y1_values = [line_y1, line_y1]

        plt.plot(x1_values, y1_values, 'b')

        x2_values = [0, 16]
        y2_values = [line_y2, line_y2]

        plt.plot(x2_values, y2_values, 'b')

        x3_values = [0, 16]
        y3_values = [line_y3, line_y3]

        plt.plot(x3_values, y3_values, 'b')

        x1_v_values = [4, 4]
        y1_v_values = [0, 16]

        plt.plot(x1_v_values, y1_v_values, 'b')

        x2_v_values = [8, 8]
        y2_v_values = [0, 16]

        plt.plot(x2_v_values, y2_v_values, 'b')

        x3_v_values = [12, 12]
        y3_v_values = [0, 16]

        plt.plot(x3_v_values, y3_v_values, 'b')

        plt.show()
        print("Finished to paint")

    def paint_with_arrays(self, fig, ax, columnx, columny, paint_shape, paint_color):
        print("begin to paint with arrays parameters")

        ax.scatter(columnx, columny, marker=paint_shape, color=paint_color, s=50)
        plt.show()
        print("Finished to paint_with_arrays")

    def paint_grid(self, fig, ax):
        print("begin to paint_grid ")

        line_y1 = 4
        line_y2 = 8
        line_y3 = 12
        x1_values = [0, 16]
        y1_values = [line_y1, line_y1]

        plt.plot(x1_values, y1_values, 'b')

        x2_values = [0, 16]
        y2_values = [line_y2, line_y2]

        plt.plot(x2_values, y2_values, 'b')

        x3_values = [0, 16]
        y3_values = [line_y3, line_y3]

        plt.plot(x3_values, y3_values, 'b')

        x1_v_values = [4, 4]
        y1_v_values = [0, 12]

        plt.plot(x1_v_values, y1_v_values, 'b')

        x2_v_values = [8, 8]
        y2_v_values = [0, 12]

        plt.plot(x2_v_values, y2_v_values, 'b')

        x3_v_values = [12, 12]
        y3_v_values = [0, 12]

        plt.plot(x3_v_values, y3_v_values, 'b')

        plt.show()
        print("Finished to paint_grid")
