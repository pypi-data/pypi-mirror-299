# MIT License
#
# Copyright (c) [2024] [Sariya Ansari]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# 1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# 2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from abc import ABC, abstractmethod
from visual.columntypedetector import ColumnTypeDetector

class BaseVisualizer(ABC):
    """
    Abstract base class for all visualizer backends.

    This class serves as a blueprint for creating various visualization backends,
    ensuring that essential methods for visualizing data are implemented.
    """

    def __init__(self):
        """ Initialize the BaseVisualizer with a ColumnTypeDetector instance. """
        self.type_detector = ColumnTypeDetector()

    @abstractmethod
    def auto_visualize(self, df, figsize=(10, 10), ncols=2, filename=None):
        """
        Automatically visualize the given DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            figsize (tuple, optional): The size of the figure (width, height).
            ncols (int, optional): The number of columns for subplots.
            filename (str, optional): The filename to save the figure as an image.

        Returns:
            None
        """
        pass

    @abstractmethod
    def visualize(self, df, visualization_type=None, class_variable=None, figsize=(10, 10), ncols=2, filename=None):
        """
        Visualize the data using the specified visualization type.

        This method can handle both DataFrames and URLs. If a URL is provided,
        it will be loaded into a DataFrame before visualization.

        Args:
            df (str or pd.DataFrame): The data source, either a URL string pointing to a dataset
                                      or a Pandas DataFrame containing the data to visualize.
            visualization_type (str, optional): The type of visualization to create (e.g., bar, line).
            class_variable (str, optional): The name of the class variable to use for coloring points.
            figsize (tuple, optional): The size of the figure (width, height).
            ncols (int, optional): The number of columns for subplots.
            filename (str, optional): The filename to save the figure as an image.

        Returns:
            None
        """
        pass

    @abstractmethod
    def filter_columns_by_type(self, df, expected_type):
        """
        Filter columns of the DataFrame based on their detected type.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            expected_type (str): The expected column type to filter.

        Returns:
            list: A list of column names matching the expected type.
        """
        pass

    @abstractmethod
    def get_random_color(self):
        """
        Generate a random color for visualizations.

        Returns:
            str: A string representing a random RGBA color value.
        """
        pass