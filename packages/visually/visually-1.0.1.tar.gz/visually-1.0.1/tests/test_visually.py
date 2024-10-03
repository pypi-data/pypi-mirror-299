import os
import unittest
import pandas as pd
import matplotlib.pyplot as plt
from visual.visually import MatplotlibVisualizer, PlotlyVisualizer

class TestMatplotlibVisualizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load the dataset and set up the Matplotlib visualizer."""
        # Path to the data.csv file
        cls.data_file = os.path.join('data', 'data.csv')
        cls.df = pd.read_csv(cls.data_file)
        cls.visualizer = MatplotlibVisualizer()
        cls.plotly_visualizer = PlotlyVisualizer()

        # Create output directory for saving the plots
        cls.output_dir = 'test_outputs'
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)

    def file_exists_with_substring(self, filename_contains):
        """Helper function to check if a file containing the substring exists in the output directory."""
        files = os.listdir(self.output_dir)
        return any(filename_contains in file for file in files)

    def test_histogram(self):
        """Test if a histogram is generated successfully."""
        filename = os.path.join(self.output_dir, 'histogram')
        self.visualizer.visualize(self.df, visualization_type='histogram', filename=filename)

        # Check if the file was created (filename contains 'histogram')
        print(filename)
        self.assertTrue(self.file_exists_with_substring('histogram'))

    def test_line_chart(self):
        """Test if a line chart is generated successfully."""
        filename = os.path.join(self.output_dir, 'line_chart')
        self.visualizer.visualize(self.df, visualization_type='line', class_variable='class', filename=filename)

        print(filename)
        # Check if the file was created (filename contains 'line_chart')
        self.assertTrue(self.file_exists_with_substring('line_chart'))

    def test_bar_chart(self):
        """Test if a bar chart is generated successfully."""
        filename = os.path.join(self.output_dir, 'bar_chart')
        self.visualizer.visualize(self.df, visualization_type='bar', filename=filename)

        print(filename)
        # Check if the file was created (filename contains 'bar_chart')
        self.assertTrue(self.file_exists_with_substring('bar_chart'))

    def test_plotly_histogram(self):
        """Test Plotly: if a histogram is generated successfully."""
        filename = os.path.join(self.output_dir, 'plotly_histogram')
        self.plotly_visualizer.visualize(self.df, filename=filename)

        # Check if the file was created (filename contains 'plotly_histogram')
        self.assertTrue(self.file_exists_with_substring('plotly_histogram'))

    def test_plotly_line_chart(self):
        """Test Plotly: if a line chart is generated successfully."""
        filename = os.path.join(self.output_dir, 'plotly_line_chart')
        self.plotly_visualizer.visualize(self.df, visualization_type='line', class_variable='class', filename=filename)

        # Check if the file was created (filename contains 'plotly_line_chart')
        self.assertTrue(self.file_exists_with_substring('plotly_line_chart'))

    def test_plotly_scatter_plot(self):
        """Test Plotly: if a scatter plot is generated successfully."""
        filename = os.path.join(self.output_dir, 'plotly_scatter_plot')
        self.plotly_visualizer.visualize(self.df, visualization_type='scatter', class_variable='class', filename=filename)

        # Check if the file was created (filename contains 'plotly_scatter_plot')
        self.assertTrue(self.file_exists_with_substring('plotly_scatter_plot'))

    @classmethod
    def tearDownClass(cls):
        """Close all Matplotlib figures after running tests."""
        plt.close('all')

if __name__ == '__main__':
    unittest.main()
