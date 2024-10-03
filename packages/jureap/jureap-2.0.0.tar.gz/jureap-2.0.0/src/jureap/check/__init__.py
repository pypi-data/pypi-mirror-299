# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import csv
import os

column_array = ["system", "version", "queue","variant",
                "jobid", "nodes", "taskspernode", "threadspertask", "runtime", "success"]

def check(input_filename):
    print("Checking csv files: " + input_filename)
    matrix = []
    with open(input_filename, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            matrix.append(row)


    try:
        title_row = matrix[0]
        for column in column_array:
            if column not in title_row:
                raise ValueError("Column " + column + " not found in the input file.")

        for row in matrix[1:]:
            for index, value in enumerate(row):
                if value == "":
                    raise ValueError("Empty value for column " + column_array[index] + " in the input file.")


    except ValueError as e:
        error_string = "Error in input csv file " + input_filename + str("\n")
        error_string = error_string + str(e)
        raise ValueError(error_string)












