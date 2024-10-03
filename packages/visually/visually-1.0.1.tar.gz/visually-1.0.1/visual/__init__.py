"""
# Visually

The `Visually` class serves as a unified interface for visualizing data using different backends, such as Matplotlib, Seaborn, and Plotly. This document provides a comprehensive guide on how to initialize the class, set the visualization style, and create various types of graphs.

## Table of Contents
- Installation
- Usage
  - Class Initialization
  - Setting Visualization Style
  - Visualizing Data
- Parameters
- Example Combinations and Their Purpose
- Summary
- Important Note

## Installation

Before using the `Visually`, ensure you have the necessary libraries installed:

```
pip install pandas matplotlib seaborn plotly kaleido
```

To install `Visually`, execute the following command:

```
pip install visually
```

## Usage

### Class Initialization

To use the `Visually` class, first initialize an instance of it, specifying the desired visualization style:

```python
visualizer = Visually()  # Defaults to 'matplot'
# OR
visualizer = Visually(style='seaborn')  # Options: 'matplot', 'seaborn', 'plotly'
```

### Setting Visualization Style

You can set the visualization style during initialization or change it later using the `set_style` method if the instance is already created:

```python
visualizer.set_style('seaborn')  # Changes the visualizer to use Seaborn
```

### Visualizing Data

The main method for creating visualizations is `visualize`. This method can load data from a URL or a local file path and can visualize it according to the specified parameters.

Here’s the method signature for `visualize`:

```python
def visualize(self, data, visualization_type=None, class_variable=None, figsize=(10, 10), ncols=2, filename=None, header=True, url=False):
```

## Parameters

- **data**: (`str` or `pd.DataFrame`)  
  The data source. This can be either a URL pointing to a CSV or pickle file or a Pandas DataFrame.

- **visualization_type**: (`str`, optional)  
  Specifies the type of visualization to create. Common options might include:
  - `'line'`: Create a line plot.
  - `'bar'`: Create a bar chart.
  - `'scatter'`: Create a scatter plot.
  - `'box'`: Create a box plot.
  - `'hist'`: Create a histogram.
  - `'pairplot'`: Create a pair plot.
  - `'pie'`: Create a pie chart.
  - `'box'`: Create a box plot.
  - `'violin'`: Create a violin plot.
  - `'dot'`: Create a dot plot.
  - `'error'`: Create an error bar plot.

- **class_variable**: (`str`, optional)  
  The name of the column to use for grouping or coloring data points in the visualization.

- **figsize**: (`tuple`, optional)  
  A tuple specifying the width and height of the figure (e.g., `(10, 5)`).

- **ncols**: (`int`, optional)  
  The number of columns for subplot layouts.

- **filename**: (`str`, optional)  
  The name of the file to save the visualization (with appropriate file extension based on the style).

- **header**: (`bool`, optional)  
  Indicates whether the data source has a header row (default is `True`).

- **url**: (`bool`, optional)  
  If `True`, treats `data` as a URL. If `False`, treats `data` as a file path or DataFrame.

## Example Combinations and Their Purpose

Here’s a breakdown of various combinations you can use with the `visualize` method:

### 1. Basic Line Plot

```python
visualizer = Visually()

# Auto visualize
visualizer.visualize(data='test.csv')

# Visualize line chart where class variable is category, store result with (prefix) filename line_plot
visualizer.visualize(data='data.csv', visualization_type='line', class_variable='Category', filename='line_plot')
```

- **Purpose**:
Create an object of `Visually` and pass the data from the file `"test.csv"` to the `visualize` method.
The class will automatically predict the appropriate visualization based on the data type.
In another example, specifying the type of chart to generate and the filename to save the resulting visualization.

### 2. Bar Chart with Grouping

```python
visualizer.visualize(data=df, visualization_type='bar', class_variable='Category', figsize=(12, 6))
```

- **Purpose**: Create a bar chart, grouping data by the 'Category' column, with a custom figure size.

### 3. Scatter Plot with Color Coding

```python
visualizer.visualize(data='data.csv', visualization_type='scatter', class_variable='Class', ncols=2, header=True)
```

- **Purpose**: Create a scatter plot, using the 'Class' variable to color the points, with a layout of 2 columns.

### 4. Box Plot for Distribution Analysis

```python
visualizer.visualize(data=df, visualization_type='box', filename='box_plot', header=False)
```

- **Purpose**: Create a box plot to analyze the distribution of values in the DataFrame without headers.

### 5. Histogram for Frequency Distribution

```python
visualizer.visualize(data='data.pkl', visualization_type='hist', class_variable=None, figsize=(10, 5), url=False)
```

- **Purpose**: Create a histogram from a pickle file, displaying the frequency distribution of the entire dataset.

### 6. Usage with Different Styles
```python
# For Matplotlib
visualizer = Visually(style='matplot')
visualizer.visualize(data='data.csv', visualization_type='bar', filename='matplotlib_bar_plot')

# For Seaborn
visualizer.set_style('seaborn')
visualizer.visualize(data='data.csv', visualization_type='scatter', class_variable='Category')

# For Plotly
visualizer.set_style('plotly')
visualizer.visualize(data='data.csv', visualization_type='line', class_variable='target', filename='plotly_line_plot')

# Matplotlib
visualizer = Visually('matplot')
visualizer.visualize(data='data.csv', visualization_type='line', class_variable='target', figsize=(10, 5), filename='file1')

# Changing instance backend to plotly type
visualizer.set_style('plotly')
visualizer.visualize('data.csv', visualization_type='heatmap')

# Change backend and plot all graph one by one
visualizer.set_style('seaborn')
df = pd.read_csv('/content/testdata.csv')
visualizer.visualize(df, figsize=(10, 15)) #Auto Visualize case
visualizer.visualize(df, visualization_type='bar', figsize=(10, 10))
visualizer.visualize(df, visualization_type='histogram', figsize=(10, 10))
visualizer.visualize(df, visualization_type='line', class_variable='class', figsize=(10, 10))
visualizer.visualize(df, visualization_type='scatter', class_variable='class', figsize=(10, 10))
visualizer.visualize(df, visualization_type='pie', figsize=(10, 10))
visualizer.visualize(df, visualization_type='heatmap', figsize=(10, 10))
visualizer.visualize(df, visualization_type='pairplot', figsize=(10, 10))
visualizer.visualize(df, visualization_type='boxplot', figsize=(30, 10))
visualizer.visualize(df, visualization_type='violin', figsize=(30, 10))
visualizer.visualize(df, visualization_type='dotplot', figsize=(10, 10))
visualizer.visualize(df, visualization_type='errorbar', figsize=(10, 10))

# Fetch data from public URL and visualize
visualizer.set_style('seaborn')
visualizer.visualize(data='https://example.com/data.csv', url=True)
```

- **Purpose**: Demonstrates how to create multiple visualizations with different styles (Matplotlib, Seaborn, Plotly) using the same dataset.

## Summary

The `Visually` class provides a flexible and powerful interface for creating various types of visualizations with minimal setup. By combining different parameters and styles, users can tailor their visualizations to fit their specific needs and data characteristics. Whether you're creating simple plots or more complex visualizations with grouping, the `Visually` class simplifies the process of data visualization in Python.


## Important Note
1. To save the snapshot of chart filename need not to have extension.
2. It supports .png or .html file format automatically.
3. There is a possibility that your environment is failing on kaleido lib in this case chart will be save in html format.
4. Kaleido is a dependency for plotly based charts.
5. Data folder may be empty but you can copy your csv file to execute unit test or main method to play with code.
6. Snapshot or images created using unit test will be stored in test_outputs folder created dynamically.
7. visualize API supports ONLY PUBLIC URL to fetch the data, therefore no API key parameter is provided in it.
8. To execute unit test you need to execute below command.
```python
python -m unittest discover -s tests
```
"""
from .visually import Visually
from .matplotlibvisualizer import MatplotlibVisualizer
from .seabornvisualizer import SeabornVisualizer
from .plotlyvisualizer import PlotlyVisualizer