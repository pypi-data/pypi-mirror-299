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
This module defines the `MatplotlibVisualizer` class, which provides various
visualization methods using Matplotlib.

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

from visual.basevisualizer import BaseVisualizer
import matplotlib.pyplot as plt
import random
import numpy as np

class MatplotlibVisualizer(BaseVisualizer):
    """
    Matplotlib implementation of the visualizer.
    This class provides various visualization methods using Matplotlib to display data pictorially.
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
        Automatically visualize columns in the DataFrame using Matplotlib.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height). Default is (10, 10).
            ncols (int): Number of columns in the subplot layout. Default is 2.
            filename (str, optional): The file path to save the figure. Default is None.

        Returns:
            None
        """
        ncols = max(ncols, 1)
        nrows = (len(df.columns) + ncols - 1) // ncols  # Calculate number of rows
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = np.array(axes).flatten()  # Flatten in case of multi-dimensional axes

        for idx, column_name in enumerate(df.columns):
            column = df[column_name]
            col_type = self.type_detector.detect_column_type(column)
            ax = axes[idx]  # Assigning the subplot

            print(f"Visualizing {column_name} of type {col_type}")

            # Numeric columns
            if col_type == 'numeric':
                ax.hist(column.dropna(), bins=20, color=self.get_random_color(), alpha=0.7)
                ax.set_title(f'Histogram of {column_name}')
                ax.set_xlabel(column_name)
                ax.set_ylabel('Frequency')

            # Categorical columns
            elif col_type in ['string', 'category']:
                value_counts = column.value_counts()
                ax.barh(value_counts.index, value_counts.values, color=self.get_random_color())
                ax.set_title(f'Bar chart of {column_name}')
                ax.set_xlabel('Count')
                ax.set_ylabel(column_name)

        # Hide any unused subplots
        for i in range(len(df.columns), nrows * ncols):
            fig.delaxes(axes[i])

        plt.tight_layout()
        if filename:
            plt.savefig(filename)
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
            base_filename = filename

            if visualization_type == 'bar':
                self._bar_chart(df, figsize, base_filename)
            elif visualization_type == 'histogram':
                self._histogram(df, figsize, base_filename)
            elif visualization_type == 'scatter' and class_variable:
                self._scatter_plot(df, class_variable, figsize, base_filename)
            elif visualization_type == 'pairplot':
                self._pair_plot(df, figsize, base_filename)
            elif visualization_type == 'heatmap':
                self._heatmap(df, figsize, base_filename)
            elif visualization_type == 'pie':
                self._pie_chart(df, figsize, base_filename)
            elif visualization_type == 'line' and class_variable:
                self._line_chart(df, class_variable, figsize, base_filename)
            elif visualization_type == 'boxplot':
                self._box_plot(df, figsize, base_filename)
            elif visualization_type == 'violin':
                self._violin_plot(df, figsize, base_filename)
            elif visualization_type == 'dotplot':
                self._dot_plot(df, figsize, base_filename)
            elif visualization_type == 'errorbar':
                self._error_bar_plot(df, figsize, base_filename)
            else:
                print(f"Unsupported visualization type {visualization_type}")

    # Individual visualization methods for different types of charts

    def _bar_chart(self, df, figsize, base_filename):
        """
        Generate bar charts for string columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        string_columns = self.filter_columns_by_type(df, 'string')
        for i, col in enumerate(string_columns):
            value_counts = df[col].value_counts()
            fig, ax = plt.subplots(figsize=figsize)
            ax.barh(value_counts.index, value_counts.values, color=self.get_random_color())
            ax.set_title(f'Bar Chart of {col}')
            ax.set_xlabel('Count')
            ax.set_ylabel(col)
            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_bar_{i}.png")
            plt.show()

    def _histogram(self, df, figsize, base_filename):
        """
        Generate histograms for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        for i, col in enumerate(numeric_columns):
            fig, ax = plt.subplots(figsize=figsize)
            ax.hist(df[col].dropna(), bins=20, color=self.get_random_color(), alpha=0.7)
            ax.set_title(f'Histogram of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_histogram_{i}.png")
            plt.show()

    def _scatter_plot(self, df, class_variable, figsize, base_filename):
        """
        Generate scatter plots of numeric columns against a class variable.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str): The class variable to plot against.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        for i, col in enumerate(numeric_columns):
            if col == class_variable:
                continue  # Skip if the column is the class variable itself
            fig, ax = plt.subplots(figsize=figsize)
            ax.scatter(df[col], df[class_variable], color=self.get_random_color(), alpha=0.7)
            ax.set_title(f'Scatter Plot of {col} vs {class_variable}')
            ax.set_xlabel(col)
            ax.set_ylabel(class_variable)
            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_scatter_{i}.png")
            plt.show()

    def _pair_plot(self, df, figsize, base_filename):
        """
        Generate a pair plot for the numeric columns in the DataFrame using Matplotlib.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        num_cols = len(numeric_columns)

        if num_cols < 2:
            print("Not enough numeric columns for a pair plot.")
            return

        fig, axes = plt.subplots(nrows=num_cols, ncols=num_cols, figsize=figsize)
        for i in range(num_cols):
            for j in range(num_cols):
                x_col = numeric_columns[j]
                y_col = numeric_columns[i]
                ax = axes[i, j]

                if i == j:
                    ax.hist(df[x_col].dropna(), bins=20, color=self.get_random_color(), alpha=0.7)
                    ax.set_ylabel(y_col)
                else:
                    ax.scatter(df[x_col], df[y_col], color=self.get_random_color(), alpha=0.5)
                if i == num_cols - 1:
                    ax.set_xlabel(x_col)
                else:
                    ax.set_xticklabels([])
                if j > 0:
                    ax.set_yticklabels([])

        plt.tight_layout()
        if base_filename:
            plt.savefig(f"{base_filename}_pairplot.png")
        plt.show()

    def _heatmap(self, df, figsize, base_filename):
        """
        Generate a heatmap of correlations between numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        correlation_matrix = df[numeric_columns].corr()

        fig, ax = plt.subplots(figsize=figsize)
        cax = ax.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
        fig.colorbar(cax)
        ax.set_xticks(range(len(numeric_columns)))
        ax.set_yticks(range(len(numeric_columns)))
        ax.set_xticklabels(numeric_columns, rotation=90)
        ax.set_yticklabels(numeric_columns)
        ax.set_title('Heatmap of Correlations')
        plt.tight_layout()
        if base_filename:
            plt.savefig(f"{base_filename}_heatmap.png")
        plt.show()

    def _pie_chart(self, df, figsize, base_filename):
        """
        Generate pie charts for categorical columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        # Adjust filtering to check for both 'string' and 'category' types
        categorical_columns = self.filter_columns_by_type(df, 'string') + self.filter_columns_by_type(df, 'category')

        if not categorical_columns:
            print("No categorical columns found for pie chart generation.")
            return

        for i, col in enumerate(categorical_columns):
            value_counts = df[col].value_counts(dropna=False)  # Include NaN counts if necessary
            fig, ax = plt.subplots(figsize=figsize)
            colors = [self.get_random_color() for _ in range(len(value_counts))]

            # Plot the pie chart
            ax.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90, counterclock=False)

            ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
            ax.set_title(f'Pie Chart of {col}')

            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_pie_{i}.png")
            plt.show()

    def _line_chart(self, df, class_variable, figsize, base_filename):
        """
        Generate line charts for numeric columns in relation to a class variable.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            class_variable (str): The class variable to plot against.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        if class_variable not in df.columns:
            print(f"Class variable '{class_variable}' not found in DataFrame.")
            return

        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        for i, col in enumerate(numeric_columns):
            if col == class_variable:
                continue  # Skip if the column is the class variable itself
            fig, ax = plt.subplots(figsize=figsize)
            sorted_df = df.sort_values(by=class_variable)
            ax.plot(sorted_df[class_variable], sorted_df[col], marker='o', linestyle='-', color=self.get_random_color())
            ax.set_title(f'Line Chart of {col} vs {class_variable}')
            ax.set_xlabel(class_variable)
            ax.set_ylabel(col)
            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_line_{i}.png")
            plt.show()

    def _box_plot(self, df, figsize, base_filename):
        """
        Generate box plots for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        data = [df[col].dropna() for col in numeric_columns]
        fig, ax = plt.subplots(figsize=figsize)
        ax.boxplot(data, labels=numeric_columns)
        ax.set_title('Box Plots of Numeric Columns')
        ax.set_xlabel('Variables')
        ax.set_ylabel('Values')
        plt.xticks(rotation=45)
        plt.tight_layout()
        if base_filename:
            plt.savefig(f"{base_filename}_boxplot.png")
        plt.show()

    def _violin_plot(self, df, figsize, base_filename):
        """
        Generate violin plots for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        data = [df[col].dropna() for col in numeric_columns]
        positions = range(1, len(numeric_columns) + 1)
        fig, ax = plt.subplots(figsize=figsize)
        ax.violinplot(data, positions=positions, showmeans=True)
        ax.set_title('Violin Plots of Numeric Columns')
        ax.set_xlabel('Variables')
        ax.set_ylabel('Values')
        ax.set_xticks(positions)
        ax.set_xticklabels(numeric_columns, rotation=45)
        plt.tight_layout()
        if base_filename:
            plt.savefig(f"{base_filename}_violinplot.png")
        plt.show()

    def _dot_plot(self, df, figsize, base_filename):
        """
        Generate dot plots for categorical variables in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        categorical_columns = self.filter_columns_by_type(df, 'category')
        for i, col in enumerate(categorical_columns):
            value_counts = df[col].value_counts()
            fig, ax = plt.subplots(figsize=figsize)
            ax.plot(value_counts.index, value_counts.values, 'o', color=self.get_random_color())
            ax.set_title(f'Dot Plot of {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Count')
            plt.xticks(rotation=45)
            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_dot_{i}.png")
            plt.show()

    def _error_bar_plot(self, df, figsize, base_filename):
        """
        Generate error bar plots for numeric columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            figsize (tuple): The size of the figure (width, height).
            base_filename (str, optional): The base file path to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        x = np.arange(len(df))
        for i, col in enumerate(numeric_columns):
            y = df[col].dropna()
            yerr = y.std()
            fig, ax = plt.subplots(figsize=figsize)
            ax.errorbar(x[:len(y)], y, yerr=yerr, fmt='o', color=self.get_random_color())
            ax.set_title(f'Error Bar Plot of {col}')
            ax.set_xlabel('Index')
            ax.set_ylabel(col)
            plt.tight_layout()
            if base_filename:
                plt.savefig(f"{base_filename}_errorbar_{i}.png")
            plt.show()
