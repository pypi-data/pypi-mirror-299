# MIT License
#
# Copyright (c) [2024] [Sariya Ansari]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# 1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# 2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
This module defines the `Visually` class, which serves as the main interface
for visualizing data using different backends, including Matplotlib, Seaborn,
and Plotly.

The class provides methods to:
- Set the visualization backend style.
- Load data from local files or URLs.
- Invoke the appropriate visualization methods based on the specified backend and options.
"""

import pandas as pd

from visual.matplotlibvisualizer import MatplotlibVisualizer
from visual.plotlyvisualizer import PlotlyVisualizer
from visual.seabornvisualizer import SeabornVisualizer


class Visually:
    """
    Main interface class for data visualization.

    This class provides an interface to visualize data using different
    backends, such as Matplotlib, Seaborn, and Plotly. It allows setting
    the visualization style and loading data from various sources.
    """

    def __init__(self, style='matplot'):
        """
        Initialize the Visually instance with the specified visualization style.

        Args:
            style (str, optional): The visualization style to use ('matplot', 'seaborn', 'plotly').
                                   Default is 'matplot'.
        """
        self.visualizer = None
        self.set_style(style)

    def set_style(self, style):
        """
        Set the backend visualization style.

        Args:
            style (str): The visualization style to set ('matplot', 'seaborn', or 'plotly').

        Raises:
            ValueError: If the specified style is unsupported.
        """
        if style == 'matplot':
            self.visualizer = MatplotlibVisualizer()
        elif style == 'seaborn':
            self.visualizer = SeabornVisualizer()
        elif style == 'plotly':
            self.visualizer = PlotlyVisualizer()
        else:
            raise ValueError(f"Unsupported style: {style}")

    def visualize(self, data, visualization_type=None, class_variable=None,
                  figsize=(10, 5), ncols=2, filename=None, header=True, url=False):
        """
        Load data and call the appropriate visualizer methods based on the specified backend.

        This method handles loading data from either a URL or a local path. It then
        invokes the corresponding visualization method based on the set backend
        (Matplotlib, Seaborn, or Plotly).

        Args:
            data (str or pd.DataFrame): The data source, either a URL string or a DataFrame.
            visualization_type (str, optional): The type of visualization to create (e.g., 'bar', 'histogram').
            class_variable (str, optional): The name of the class variable for color-based grouping.
            figsize (tuple, optional): The size of the figure (width, height). Default is (10, 5).
            ncols (int, optional): The number of columns for subplots. Default is 2.
            filename (str, optional): The filename to save the figure as an image.
            header (bool, optional): Whether the input data has a header row. Default is True.
            url (bool, optional): Whether to interpret the `data` parameter as a URL. Default is False.

        Raises:
            ValueError: If the data is not in an acceptable format (e.g., unsupported file type or invalid input).
        """

        valid_types = [None, 'line', 'bar', 'scatter', 'histogram', 'pairplot', 'heatmap', 'boxplot', 'violin', 'dotplot', 'errorbar', 'pie']
        if visualization_type not in valid_types:
            raise ValueError(f"Unsupported visualization type {visualization_type}")

        if url:
            # Load data from a URL
            if isinstance(data, str):
                # Determine file type from the URL
                if data.endswith('.csv'):
                    df = pd.read_csv(data, header=None if not header else 'infer')
                elif data.endswith('.pkl'):
                    df = pd.read_pickle(data)
                else:
                    raise ValueError("Unsupported file type. Please provide a .csv or .pkl file.")
            else:
                raise ValueError("Data must be a URL string.")
        else:
            # Load data from a local path or DataFrame
            if isinstance(data, str):
                df = pd.read_csv(data, header=None if not header else 'infer')
            elif isinstance(data, pd.DataFrame):
                df = data
            else:
                raise ValueError("Data must be a file path or a DataFrame.")

        # If no header is present, generate dummy headers
        if not header:
            df.columns = [f"Column_{i+1}" for i in range(df.shape[1])]

        # Call the visualizer to render the specified visualization
        self.visualizer.visualize(df, visualization_type, class_variable, figsize, ncols, filename)
