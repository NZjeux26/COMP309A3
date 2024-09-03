import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

def create_3d_scatter_plot(csv_path, x_var, y_var, z_var, target_var):
    # Load the CSV data
    df = pd.read_csv(csv_path)
    
    # Ensure the selected variables exist in the dataframe
    for var in [x_var, y_var, z_var, target_var]:
        if var not in df.columns:
            raise ValueError(f"Column '{var}' not found in the CSV file.")

    # Create the 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Get the unique categories in the target variable
    categories = df[target_var].unique()
    
    # Assign a color to each category
    colors = plt.cm.get_cmap('tab10', len(categories))
    
    # Plot each category with a different color
    for i, category in enumerate(categories):
        subset = df[df[target_var] == category]
        ax.scatter(subset[x_var], subset[y_var], subset[z_var], color=colors(i), label=category)
    
    # Label the axes
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_zlabel(z_var)
    
    # Add a legend
    ax.legend(title=target_var)
    
    # Show the plot
    plt.show()

def create_3d_surface_plot(csv_path, x_var, y_var, z_var):
    # Load the CSV data
    df = pd.read_csv(csv_path)
    
    # Ensure the selected variables exist in the dataframe
    for var in [x_var, y_var, z_var]:
        if var not in df.columns:
            raise ValueError(f"Column '{var}' not found in the CSV file.")

    # Create the 3D surface plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Generate grid data for the surface plot
    x = df[x_var].values
    y = df[y_var].values
    z = df[z_var].values

    # Create a grid of x and y values
    x_grid, y_grid = np.meshgrid(np.linspace(x.min(), x.max(), 100),
                                 np.linspace(y.min(), y.max(), 100))

    # Interpolate z values on the grid
    z_grid = griddata((x, y), z, (x_grid, y_grid), method='cubic')

    # Plot the surface
    ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis', alpha=0.7)
    
    # Label the axes
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_zlabel(z_var)
    
    # Show the plot
    plt.show()
def create_3d_contour_plot(csv_path, x_var, y_var, z_var, target_var):
  # Load the CSV data
    df = pd.read_csv(csv_path)
    
    # Ensure the selected variables exist in the dataframe
    for var in [x_var, y_var, z_var, target_var]:
        if var not in df.columns:
            raise ValueError(f"Column '{var}' not found in the CSV file.")

    # Create the 3D contour plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Get the unique categories in the target variable
    categories = df[target_var].unique()

    # Assign a color to each category
    colors = plt.colormaps['tab10']

    # Plot each category with a different color
    for i, category in enumerate(categories):
        subset = df[df[target_var] == category]
        x = subset[x_var].values
        y = subset[y_var].values
        z = subset[z_var].values

        # Create a grid of x and y values
        x_grid, y_grid = np.meshgrid(np.linspace(x.min(), x.max(), 50),
                                     np.linspace(y.min(), y.max(), 50))

        # Interpolate z values on the grid
        z_grid = griddata((x, y), z, (x_grid, y_grid), method='cubic')

        # Plot the contours for this category with the specific color
        ax.contour3D(x_grid, y_grid, z_grid, 50, colors=[colors(i)])
    
    # Label the axes
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_zlabel(z_var)
    
    # Add a legend
    ax.legend(title=target_var)
    
    # Show the plot
    plt.show()
def create_3d_wireframe_plot_with_target(csv_path, x_var, y_var, z_var, target_var):
    # Load the CSV data
    df = pd.read_csv(csv_path)
    
    # Ensure the selected variables exist in the dataframe
    for var in [x_var, y_var, z_var, target_var]:
        if var not in df.columns:
            raise ValueError(f"Column '{var}' not found in the CSV file.")
    
    # Create the 3D wireframe plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Get the unique categories in the target variable
    categories = df[target_var].unique()

    # Assign a color to each category
    colors = plt.colormaps['tab10']

    # Plot each category with a different color
    for i, category in enumerate(categories):
        subset = df[df[target_var] == category]
        x = subset[x_var].values
        y = subset[y_var].values
        z = subset[z_var].values

        # Create a grid of x and y values
        x_grid, y_grid = np.meshgrid(np.linspace(x.min(), x.max(), 50),
                                     np.linspace(y.min(), y.max(), 50))

        # Interpolate z values on the grid
        z_grid = griddata((x, y), z, (x_grid, y_grid), method='cubic')

        # Plot the wireframe for this category
        ax.plot_wireframe(x_grid, y_grid, z_grid, color=colors(i), label=category)
    
    # Label the axes
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    ax.set_zlabel(z_var)
    
    # Add a legend
    ax.legend(title=target_var)
    
    # Show the plot
    plt.show()
# Example usage (comment out to prevent execution):
# create_3d_scatter_plot('data.csv', 'var1', 'var2', 'var3', 'target')
var1 = 'acousticness'
var2 = 'energy'
var3 = 'loudness'
target = 'genre'
data = '../data/mega_full_processedNorm.csv'
create_3d_scatter_plot(data, var1, var2,var3, target)
#create_3d_surface_plot(data,var1,var2,var3)
#create_3d_contour_plot(data,var1,var2,var3,target)