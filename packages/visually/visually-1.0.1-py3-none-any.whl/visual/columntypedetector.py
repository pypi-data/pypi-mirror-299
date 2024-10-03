# MIT License
#
# Copyright (c) [2024] [Sariya Ansari]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# 1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# 2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pandas as pd

class ColumnTypeDetector:
    """
    Utility class for detecting the types of DataFrame columns.

    This class provides a method to identify the data type of each column in
    a DataFrame, categorizing them into numeric, string, date, categorical, or other types.
    """

    def __init__(self):
        """ Initialize the ColumnTypeDetector. """
        pass

    @staticmethod
    def detect_column_type(column):
        """
        Detect the type of a given column.

        Args:
            column (pd.Series): The column to analyze.

        Returns:
            str: A string representing the detected column type ('numeric', 'string', 'date', 'category', or 'other').
        """
        if pd.api.types.is_numeric_dtype(column):
            return 'numeric'
        elif pd.api.types.is_string_dtype(column):
            return 'string'
        elif pd.api.types.is_datetime64_any_dtype(column):
            return 'date'
        elif pd.api.types.is_categorical_dtype(column):
            return 'category'
        else:
            return 'other'