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
This module defines the `PlotlyVisualizer` class, which provides various
visualization methods using the Plotly library.

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
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import random
import kaleido #Required for image
import os

import plotly.io as pio


class PlotlyVisualizer(BaseVisualizer):
    """
    Plotly implementation of the visualizer.
    This class uses Plotly for visualizing data from a DataFrame. It supports
    various types of visualizations such as histograms, bar charts, and scatter plots.
    """

    def get_random_color(self):
        """
        Return a random color for charts.

        Returns:
            str: A string representing a random RGBA color value.
        """
        return f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)'

    def filter_columns_by_type(self, df, expected_type):
        """
        Filter columns by their detected type.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            expected_type (str): The expected column type to filter.

        Returns:
            list: A list of column names matching the expected type.
        """
        return [col for col in df.columns if self.type_detector.detect_column_type(df[col]) == expected_type]

    def auto_visualize(self, df, figsize=(10, 10), ncols=2, filename=None):
        """
        Automatically visualize columns using Plotly.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            figsize (tuple, optional): The size of the figure (width, height). Default is (10, 10).
            ncols (int, optional): The number of columns for subplots. Default is 2.
            filename (str, optional): The filename to save the figure as an image.

        Returns:
            None
        """
        width = figsize[0] * 100  # Convert figsize width to pixels
        height = figsize[1] * 100  # Convert figsize height to pixels
        nrows = (len(df.columns) + ncols - 1) // ncols  # Calculate the required number of rows
        fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=df.columns.tolist())

        # Define a color scale for different plots
        color_palette = px.colors.qualitative.Set1

        for idx, column_name in enumerate(df.columns):
            column = df[column_name]
            col_type = self.type_detector.detect_column_type(column)

            print(f"Visualizing {column_name} of type {col_type}")

            # Calculate correct row and column indices
            row = (idx // ncols) + 1  # Determine the row index based on position
            col = (idx % ncols) + 1  # Determine the column index based on position

            # Generate the appropriate plot for each column type
            if col_type == 'numeric':
                trace = px.histogram(df, x=column_name, nbins=30,
                                     color_discrete_sequence=[color_palette[idx % len(color_palette)]])
                trace.update_layout(title=f'Histogram of {column_name}', xaxis_title=column_name, yaxis_title='Count')
                for data in trace.data:
                    fig.add_trace(data, row=row, col=col)

            elif col_type in ['string', 'category']:
                value_counts = df[column_name].value_counts()
                trace = px.bar(value_counts, x=value_counts.index, y=value_counts.values,
                               color_discrete_sequence=[color_palette[idx % len(color_palette)]])
                trace.update_layout(title=f'Bar chart of {column_name}', xaxis_title=column_name, yaxis_title='Count')
                for data in trace.data:
                    fig.add_trace(data, row=row, col=col)

            elif col_type == 'date':
                trace = px.line(df, x=column_name, y=df.index,
                                color_discrete_sequence=[color_palette[idx % len(color_palette)]])
                trace.update_layout(title=f'Line plot of {column_name}', xaxis_title=column_name, yaxis_title='Value')
                for data in trace.data:
                    fig.add_trace(data, row=row, col=col)

            else:
                print(f"Skipping {column_name} of unsupported type: {col_type}")

        # Adjust layout to reflect the specified figure size
        fig.update_layout(height=nrows * height, width=ncols * width)
        fig.update_layout(title_text="Auto Visualization", title_x=0.5)

        if filename:
            try:
                # Check if the filename has an extension, if not add '.png'
                if not os.path.splitext(filename)[1]:
                    filename += '.png'

                # Try saving the figure as an image (PNG)
                fig.write_image(filename)  # Save using Kaleido
                print(f"Plot saved successfully as image: {filename}")
            except Exception as png_error:
                print(f"Failed to save the plot as image: {png_error}")
                try:
                    # If saving as PNG fails, fallback to saving as HTML
                    if not os.path.splitext(filename)[1]:
                        filename += '.html'  # Add .html extension if no extension provided
                    fig.write_html(filename)
                    print(f"Plot saved successfully as HTML: {filename}")
                except Exception as html_error:
                    print(f"Failed to save the plot as HTML: {html_error}")
        else:
            print("No filename provided, skipping file save.")

        fig.show()

    def visualize(self, df, visualization_type=None, class_variable=None, figsize=(10, 10), ncols=2, filename=None):
        """
        Handle specific visualization types or fallback to auto-visualization.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            visualization_type (str, optional): The type of visualization to create.
            class_variable (str, optional): The name of the class variable to use for coloring points.
            figsize (tuple, optional): The size of the figure (width, height). Default is (10, 10).
            ncols (int, optional): The number of columns for subplots. Default is 2.
            filename (str, optional): The filename to save the figure as an image.

        Returns:
            None
        """
        if visualization_type is None:
            self.auto_visualize(df, figsize=figsize, ncols=ncols, filename=filename)
        else:
            base_filename = filename

            if visualization_type == 'boxplot':
                self._box_plot(df, base_filename)
            elif visualization_type == 'violin':
                self._violin_plot(df, base_filename)
            elif visualization_type == 'dotplot':
                self._dot_plot(df, base_filename)
            elif visualization_type == 'errorbar':
                self._error_bar_plot(df, base_filename)
            elif visualization_type == 'bar':
                self._bar_chart(df, base_filename)
            elif visualization_type == 'pie':
                self._pie_chart(df, base_filename)
            elif visualization_type == 'scatter':
                self._scatter_plot(df, base_filename)
            elif visualization_type == 'histogram':
                self._histogram(df, base_filename)
            elif visualization_type == 'heatmap':
                self._heatmap(df, base_filename)
            elif visualization_type == 'line':
                self._line_chart(df, base_filename)
            elif visualization_type == 'pairplot':
                self._pair_plot(df, base_filename)
            else:
                print(f"Unsupported visualization type {visualization_type}")

    def _box_plot(self, df, base_filename):
        """
        Create box plot for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if numeric_columns:
            fig = px.box(df, y=numeric_columns, title='Box Plot of Numeric Columns',
                         color_discrete_sequence=[self.get_random_color() for _ in numeric_columns])
            fig.show()
            if base_filename:
                try:
                    # Check if the base_filename has an extension, if not add '.png'
                    if not os.path.splitext(base_filename)[1]:
                        base_filename += '.png'

                    # Try saving the figure as an image (PNG)
                    fig.write_image(f"{base_filename}_boxplot.png")
                    print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                except Exception as png_error:
                    print(f"Failed to save the box plot as image: {png_error}")
                    try:
                        # If saving as PNG fails, fallback to saving as HTML
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.html'  # Add .html extension if no extension provided
                        fig.write_html(f"{base_filename}_boxplot.html")
                        print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                    except Exception as html_error:
                        print(f"Failed to save the box plot as HTML: {html_error}")
            else:
                print("No filename provided, skipping file save.")
        else:
            print("No numeric columns found for Box Plot.")

    def _violin_plot(self, df, base_filename):
        """
        Create violin plot for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if numeric_columns:
            fig = px.violin(df, y=numeric_columns, title='Violin Plot of Numeric Columns',
                            color_discrete_sequence=[self.get_random_color() for _ in numeric_columns])
            fig.show()
            if base_filename:
                try:
                    # Check if the base_filename has an extension, if not add '.png'
                    if not os.path.splitext(base_filename)[1]:
                        base_filename += '.png'

                    # Try saving the figure as an image (PNG)
                    fig.write_image(f"{base_filename}_violinplot.png")
                    print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                except Exception as png_error:
                    print(f"Failed to save the box plot as image: {png_error}")
                    try:
                        # If saving as PNG fails, fallback to saving as HTML
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.html'  # Add .html extension if no extension provided
                        fig.write_html(f"{base_filename}_violinplot.html")
                        print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                    except Exception as html_error:
                        print(f"Failed to save the box plot as HTML: {html_error}")
            else:
                print("No filename provided, skipping file save.")
        else:
            print("No numeric columns found for Violin Plot.")

    def _dot_plot(self, df, base_filename):
        """
        Create dot plot for string columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        string_columns = self.filter_columns_by_type(df, 'string')
        if string_columns:
            for i, col in enumerate(string_columns):
                fig = px.strip(df, y=col, title=f'Dot Plot of {col}', color_discrete_sequence=[self.get_random_color()])
                fig.show()
                if base_filename:
                    try:
                        # Check if the base_filename has an extension, if not add '.png'
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.png'

                        # Try saving the figure as an image (PNG)
                        fig.write_image(f"{base_filename}_dotplot_{i}.png")
                        print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                    except Exception as png_error:
                        print(f"Failed to save the box plot as image: {png_error}")
                        try:
                            # If saving as PNG fails, fallback to saving as HTML
                            if not os.path.splitext(base_filename)[1]:
                                base_filename += '.html'  # Add .html extension if no extension provided
                            fig.write_html(f"{base_filename}_dotplot_{i}.html")
                            print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                        except Exception as html_error:
                            print(f"Failed to save the box plot as HTML: {html_error}")
                else:
                    print("No filename provided, skipping file save.")
        else:
            print("No categorical/string columns found for Dot Plot.")

    def _error_bar_plot(self, df, base_filename):
        """
        Create error bar plot for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if numeric_columns:
            for col in numeric_columns:
                mean = df[col].mean()
                std = df[col].std()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='markers', name='Data Points'))
                fig.add_trace(go.Scatter(x=df.index, y=[mean] * len(df), mode='lines', name='Mean'))
                fig.add_trace(go.Scatter(x=df.index, y=[mean + std] * len(df), mode='lines', name='Upper Error'))
                fig.add_trace(go.Scatter(x=df.index, y=[mean - std] * len(df), mode='lines', name='Lower Error'))
                fig.update_layout(title=f'Error Bar Plot of {col}')
                fig.show()
                if base_filename:
                    try:
                        # Check if the base_filename has an extension, if not add '.png'
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.png'

                        # Try saving the figure as an image (PNG)
                        fig.write_image(f"{base_filename}_errorbar_{col}.png")
                        print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                    except Exception as png_error:
                        print(f"Failed to save the box plot as image: {png_error}")
                        try:
                            # If saving as PNG fails, fallback to saving as HTML
                            if not os.path.splitext(base_filename)[1]:
                                base_filename += '.html'  # Add .html extension if no extension provided
                            fig.write_html(f"{base_filename}_errorbar_{col}.html")
                            print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                        except Exception as html_error:
                            print(f"Failed to save the box plot as HTML: {html_error}")
                else:
                    print("No filename provided, skipping file save.")
        else:
            print("No numeric columns found for Error Bar Plot.")

    def _bar_chart(self, df, base_filename):
        """
        Create bar chart for string columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        string_columns = self.filter_columns_by_type(df, 'string')
        if string_columns:
            for i, col in enumerate(string_columns):
                value_counts = df[col].value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values, title=f'Bar Chart of {col}',
                             color_discrete_sequence=[self.get_random_color()])
                fig.show()
                if base_filename:
                    try:
                        # Check if the base_filename has an extension, if not add '.png'
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.png'

                        # Try saving the figure as an image (PNG)
                        fig.write_image(f"{base_filename}_barchart_{i}.png")
                        print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                    except Exception as png_error:
                        print(f"Failed to save the box plot as image: {png_error}")
                        try:
                            # If saving as PNG fails, fallback to saving as HTML
                            if not os.path.splitext(base_filename)[1]:
                                base_filename += '.html'  # Add .html extension if no extension provided
                            fig.write_html(f"{base_filename}_barchart_{i}.html")
                            print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                        except Exception as html_error:
                            print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("No categorical/string columns found for Bar Chart.")

    def _pie_chart(self, df, base_filename):
        """
        Create pie chart for string columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        string_columns = self.filter_columns_by_type(df, 'string')
        if string_columns:
            for i, col in enumerate(string_columns):
                value_counts = df[col].value_counts()
                fig = px.pie(values=value_counts.values, names=value_counts.index, title=f'Pie Chart of {col}')
                fig.show()
                if base_filename:
                    try:
                        # Check if the base_filename has an extension, if not add '.png'
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.png'

                        # Try saving the figure as an image (PNG)
                        fig.write_image(f"{base_filename}_piechart_{i}.png")
                        print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                    except Exception as png_error:
                        print(f"Failed to save the box plot as image: {png_error}")
                        try:
                            # If saving as PNG fails, fallback to saving as HTML
                            if not os.path.splitext(base_filename)[1]:
                                base_filename += '.html'  # Add .html extension if no extension provided
                            fig.write_html(f"{base_filename}_piechart_{i}.html")
                            print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                        except Exception as html_error:
                            print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("No categorical/string columns found for Pie Chart.")

    def _scatter_plot(self, df, base_filename):
        """
        Create scatter plot for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if len(numeric_columns) >= 2:
            fig = px.scatter(df, x=numeric_columns[0], y=numeric_columns[1], title='Scatter Plot')
            fig.show()
            if base_filename:
                try:
                    # Check if the base_filename has an extension, if not add '.png'
                    if not os.path.splitext(base_filename)[1]:
                        base_filename += '.png'

                    # Try saving the figure as an image (PNG)
                    fig.write_image(f"{base_filename}_scatterplot.png")
                    print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                except Exception as png_error:
                    print(f"Failed to save the box plot as image: {png_error}")
                    try:
                        # If saving as PNG fails, fallback to saving as HTML
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.html'  # Add .html extension if no extension provided
                        fig.write_html(f"{base_filename}_scatterplot.html")
                        print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                    except Exception as html_error:
                        print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("Not enough numeric columns found for Scatter Plot.")

    def _histogram(self, df, base_filename):
        """
        Create histogram for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if numeric_columns:
            for i, col in enumerate(numeric_columns):
                fig = px.histogram(df, x=col, title=f'Histogram of {col}', nbins=30,
                                   color_discrete_sequence=[self.get_random_color()])
                fig.show()
                if base_filename:
                    try:
                        # Check if the base_filename has an extension, if not add '.png'
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.png'

                        # Try saving the figure as an image (PNG)
                        fig.write_image(f"{base_filename}_histogram_{i}.png")
                        print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                    except Exception as png_error:
                        print(f"Failed to save the box plot as image: {png_error}")
                        try:
                            # If saving as PNG fails, fallback to saving as HTML
                            if not os.path.splitext(base_filename)[1]:
                                base_filename += '.html'  # Add .html extension if no extension provided
                            fig.write_html(f"{base_filename}_histogram_{i}.html")
                            print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                        except Exception as html_error:
                            print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("No numeric columns found for Histogram.")

    def _heatmap(self, df, base_filename):
        """
        Create heatmap for correlation of numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if len(numeric_columns) > 1:
            corr = df[numeric_columns].corr()
            fig = px.imshow(corr, text_auto=True, title='Heatmap of Correlation')
            fig.show()
            if base_filename:
                try:
                    # Check if the base_filename has an extension, if not add '.png'
                    if not os.path.splitext(base_filename)[1]:
                        base_filename += '.png'

                    # Try saving the figure as an image (PNG)
                    fig.write_image(f"{base_filename}_heatmap.png")
                    print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                except Exception as png_error:
                    print(f"Failed to save the box plot as image: {png_error}")
                    try:
                        # If saving as PNG fails, fallback to saving as HTML
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.html'  # Add .html extension if no extension provided
                        fig.write_html(f"{base_filename}_heatmap.html")
                        print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                    except Exception as html_error:
                        print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("Not enough numeric columns found for Heatmap.")

    def _line_chart(self, df, base_filename):
        """
        Create line chart for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if numeric_columns:
            fig = px.line(df, y=numeric_columns, title='Line Chart of Numeric Columns')
            fig.show()
            if base_filename:
                try:
                    # Check if the base_filename has an extension, if not add '.png'
                    if not os.path.splitext(base_filename)[1]:
                        base_filename += '.png'

                    # Try saving the figure as an image (PNG)
                    fig.write_image(f"{base_filename}_linechart.png")
                    print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                except Exception as png_error:
                    print(f"Failed to save the box plot as image: {png_error}")
                    try:
                        # If saving as PNG fails, fallback to saving as HTML
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.html'  # Add .html extension if no extension provided
                        fig.write_html(f"{base_filename}_linechart.html")
                        print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                    except Exception as html_error:
                        print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("No numeric columns found for Line Chart.")

    def _pair_plot(self, df, base_filename):
        """
        Create pair plot for numeric columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to visualize.
            base_filename (str, optional): The base filename to save the figure.

        Returns:
            None
        """
        numeric_columns = self.filter_columns_by_type(df, 'numeric')
        if len(numeric_columns) > 1:
            fig = px.scatter_matrix(df[numeric_columns], title='Pair Plot of Numeric Columns')
            fig.show()
            if base_filename:
                try:
                    # Check if the base_filename has an extension, if not add '.png'
                    if not os.path.splitext(base_filename)[1]:
                        base_filename += '.png'

                    # Try saving the figure as an image (PNG)
                    fig.write_image(f"{base_filename}_pairplot.png")
                    print(f"Box plot saved successfully as image: {base_filename}_boxplot.png")
                except Exception as png_error:
                    print(f"Failed to save the box plot as image: {png_error}")
                    try:
                        # If saving as PNG fails, fallback to saving as HTML
                        if not os.path.splitext(base_filename)[1]:
                            base_filename += '.html'  # Add .html extension if no extension provided
                        fig.write_html(f"{base_filename}_pairplot.html")
                        print(f"Box plot saved successfully as HTML: {base_filename}_boxplot.html")
                    except Exception as html_error:
                        print(f"Failed to save the box plot as HTML: {html_error}")
        else:
            print("Not enough numeric columns found for Pair Plot.")
