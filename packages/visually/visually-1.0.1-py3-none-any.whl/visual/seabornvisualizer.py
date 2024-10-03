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
This module defines the `SeabornVisualizer` class, which provides various
visualization methods using the Seaborn and Matplotlib library.

The class offers functionalities for generating different types of charts, such as:
- Histograms for numeric data
- Bar charts for categorical data
- Scatter plots for comparing variables
- Pair plots for visualizing relationships between multiple variables
- Heatmaps for displaying correlations
- Pie charts for categorical distribution
- Line charts, Box plots, Violin plots, Dot plots, and Error bar plots

Each visualization method can handle a DataFrame and produce a corresponding chart.
"""

import seaborn as sns
import pandas as pd
import random
from matplotlib import pyplot as plt
from visual.basevisualizer import BaseVisualizer

class SeabornVisualizer(BaseVisualizer):
    """
    Seaborn implementation of the visualizer.
    This class provides various visualization methods using Seaborn and Matplotlib
    to display data from a DataFrame.
    """

    def get_random_color(self):
        """
        Return a random hex color string for charts.

        Returns:
            str: A random color in hex format.
        """
        return "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

    def filter_columns_by_type(self, df, expected_type):
        """
        Filter columns by their detected type.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            expected_type (str): The expected type of columns to filter (e.g., 'numeric', 'string', 'category').

        Returns:
            list: A list of column names that match the expected type.
        """
        return [col for col in df.columns if self.type_detector.detect_column_type(df[col]) == expected_type]

    def auto_visualize(self, df, figsize=(10, 10), ncols=2, filename=None):
        """
        Automatically visualize columns in the DataFrame using Seaborn.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height). Default is (10, 10).
            ncols (int): Number of columns in the subplot layout. Default is 2.
            filename (str, optional): The file path to save the figure. Default is None.

        Returns:
            None
        """
        sns.set_theme(style="whitegrid")
        nrows = (len(df.columns) + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = axes.flatten()

        for idx, column_name in enumerate(df.columns):
            column = df[column_name]
            col_type = self.type_detector.detect_column_type(column)
            ax = axes[idx]

            if col_type == 'numeric':
                sns.histplot(column, kde=True, ax=ax, color=self.get_random_color())
                ax.set_title(f'Histogram of {column_name}')
            elif col_type in ['string', 'category']:
                sns.countplot(y=column, hue=column, ax=ax, palette='muted', legend=False)  # Fix for the palette warning
                ax.set_title(f'Bar chart of {column_name}')

        fig.tight_layout()
        if filename:
            fig.savefig(filename)
        plt.show()

    def visualize(self, df, visualization_type=None, class_variable=None, figsize=(10, 10), ncols=2, filename=None):
        """
        Handle specific visualization types or fallback to auto-visualization.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            visualization_type (str, optional): The type of visualization to generate (e.g., 'bar', 'histogram'). Default is None.
            class_variable (str, optional): The class variable for scatter plots and other visualizations. Default is None.
            figsize (tuple): The size of the figure (width, height). Default is (10, 10).
            ncols (int): Number of columns in the subplot layout for auto-visualization. Default is 2.
            filename (str, optional): The file path to save the figure. Default is None.

        Returns:
            None
        """
        if visualization_type is None:
            self.auto_visualize(df, figsize=figsize, ncols=ncols, filename=filename)
        else:
            if hasattr(self, f'_{visualization_type}_chart'):
                getattr(self, f'_{visualization_type}_chart')(df, class_variable, filename)
            else:
                print(f"Unsupported visualization type {visualization_type}")

    def _bar_chart(self, df, class_variable, filename):
        """
        Generate bar charts for string columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping. Default is None.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        string_columns = self.filter_columns_by_type(df, 'string')
        for i, col in enumerate(string_columns):
            ax = sns.countplot(y=df[col], hue=df[col], palette='muted', legend=False)
            ax.set_title(f'Bar chart of {col}')
            if filename:
                ax.figure.savefig(f"{filename}_bar_{i}.png")
            plt.show()

    def _histogram_chart(self, df, class_variable, filename):
        """
        Generate histograms for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping. Default is None.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        for i, col in enumerate(numeric_columns):
            ax = sns.histplot(df[col], kde=True, color=self.get_random_color())
            ax.set_title(f'Histogram of {col}')
            if filename:
                ax.figure.savefig(f"{filename}_histogram_{i}.png")
            plt.show()

    def _scatter_chart(self, df, class_variable, filename):
        """
        Generate scatter plots of numeric columns against a class variable.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str): The class variable to plot against.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        for i, col in enumerate(numeric_columns):
            ax = sns.scatterplot(data=df, x=col, y=class_variable, hue=class_variable, palette='Set1')
            ax.set_title(f'Scatter plot of {col} vs {class_variable}')
            if filename:
                ax.figure.savefig(f"{filename}_scatter_{i}.png")
            plt.show()

    def _heatmap_chart(self, df, class_variable, filename):
        """
        Generate a heatmap of correlations between numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping. Default is None.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = df.select_dtypes(include=['float64', 'int64'])
        if len(numeric_columns.columns) > 1:
            ax = sns.heatmap(numeric_columns.corr(), annot=True, cmap='coolwarm')
            ax.set_title('Heatmap of correlations')
            if filename:
                ax.figure.savefig(f"{filename}_heatmap.png")
            plt.show()

    def _pairplot_chart(self, df, class_variable, filename):
        """
        Generate a pairplot for relationships between numeric variables in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping. Default is None.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = df.select_dtypes(include=['float64', 'int64'])

        # Check if class_variable exists in the DataFrame and convert it to a categorical variable if needed
        if class_variable and class_variable in df.columns:
            if not pd.api.types.is_categorical_dtype(df[class_variable]):
                df[class_variable] = pd.Categorical(df[class_variable])

            g = sns.pairplot(df, hue=class_variable, palette='coolwarm')
        else:
            g = sns.pairplot(df)

        if filename:
            g.savefig(f"{filename}_pairplot.png")
        plt.show()

    def _line_chart(self, df, class_variable, filename):
        """
        Generate line charts for numeric columns against a class variable.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str): The class variable for grouping.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        for i, col in enumerate(numeric_columns):
            ax = sns.lineplot(data=df, x=df.index, y=col, hue=class_variable)
            ax.set_title(f'Line chart of {col} vs {class_variable}')
            if filename:
                ax.figure.savefig(f"{filename}_line_{i}.png")
            plt.show()

    def _boxplot_chart(self, df, class_variable, filename):
        """
        Generate box plots for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        ax = sns.boxplot(data=df[numeric_columns])
        ax.set_title('Box Plot of Numeric Columns')
        if filename:
            ax.figure.savefig(f"{filename}_boxplot.png")
        plt.show()

    def _violin_chart(self, df, class_variable, filename):
        """
        Generate violin plots for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        ax = sns.violinplot(data=df[numeric_columns], palette='Set2')
        ax.set_title('Violin Plot of Numeric Columns')
        if filename:
            ax.figure.savefig(f"{filename}_violin.png")
        plt.show()

    def _dotplot_chart(self, df, class_variable, filename):
        """
        Generate dot plots (strip plots) for categorical variables.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping.
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        string_columns = self.filter_columns_by_type(df, 'string')
        for i, col in enumerate(string_columns):
            ax = sns.stripplot(y=df[col], jitter=True, color=self.get_random_color())
            ax.set_title(f'Dot Plot of {col}')
            if filename:
                ax.figure.savefig(f"{filename}_dotplot_{i}.png")
            plt.show()

    def _errorbar_chart(self, df, class_variable, filename, sample_size=100):
        """
        Generate error bar plots for numeric columns, with data sampling for optimization.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str): The class variable for grouping (optional).
            filename (str): File name for saving the figure (optional).
            sample_size (int): Number of points to sample for error bar plotting.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')

        # Sample data for faster plotting
        if len(df) > sample_size:
            df = df.sample(n=sample_size)

        for col in numeric_columns:
            if class_variable and class_variable in df.columns:
                grouped_df = df.groupby(class_variable)[col].agg(['mean', 'std']).reset_index()
                ax = sns.pointplot(x=class_variable, y='mean', data=grouped_df, capsize=0.2,
                                   errorbar='sd', linestyle='none', err_style='bars')
            else:
                ax = sns.pointplot(x=range(len(df)), y=df[col], capsize=0.2, errorbar='sd',
                                   linestyle='none')

            ax.set_title(f'Error Bar Plot of {col}')
            if filename:
                ax.figure.savefig(f"{filename}_errorbar_{col}.png")
            plt.show()

    def _pie_chart(self, df, class_variable, filename):
        """
        Generate pie charts for categorical columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str, optional): The class variable for grouping (optional).
            filename (str, optional): The file path to save the figure.

        Returns:
            None
        """
        categorical_columns = self.filter_columns_by_type(df, 'string') + self.filter_columns_by_type(df, 'category')

        for i, col in enumerate(categorical_columns):
            counts = df[col].value_counts()
            colors = [self.get_random_color() for _ in range(len(counts))]

            plt.figure(figsize=(8, 8))
            plt.pie(counts, labels=counts.index, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.title(f'Pie Chart of {col}')

            if filename:
                plt.savefig(f"{filename}_pie_{i}.png")
            plt.show()
