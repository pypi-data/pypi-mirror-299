# visualization.py

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import warnings
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from pandas.plotting import parallel_coordinates
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import matplotlib.patches as mpatches
from itertools import combinations

import plotly.graph_objects as go
from scipy.interpolate import griddata

# Suppress all warnings
warnings.filterwarnings("ignore")

# Set default Matplotlib style with a dark background
plt.style.use('dark_background')

# Default color palette with at least 20 colors
DEFAULT_PALETTE = sns.color_palette("tab20", 20)

# Function to dynamically select a palette based on the number of columns
def get_dynamic_palette(palette, num_cols):
    if num_cols <= len(palette):
        return palette[:num_cols]
    else:
        # If more colors are needed, extend the palette by repeating it
        repeat_factor = math.ceil(num_cols / len(palette))
        extended_palette = palette * repeat_factor
        return extended_palette[:num_cols]

# Helper function to create grid layout
def create_grid(num_plots, cols=3, per_subplot_size=(5, 5)):
    rows = math.ceil(num_plots / cols)
    total_fig_width = cols * per_subplot_size[0]
    total_fig_height = rows * per_subplot_size[1]
    fig, axes = plt.subplots(rows, cols, figsize=(total_fig_width, total_fig_height), subplot_kw={})
    if rows == 1 and cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    return fig, axes

# 1. Histogram - Continuous data
def histogram_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(continuous_cols))

    for i, column in enumerate(continuous_cols):
        sns.histplot(data=data, x=column, hue=target, fill=True, palette=[dynamic_palette[i]], ax=axes[i])
        axes[i].set_title(f'Histogram - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    # Hide any unused subplots
    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 2. Bar Plot - Categorical data
def plot_bar_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(categorical_cols))

    for i, column in enumerate(categorical_cols):
        sns.countplot(data=data, x=column, hue=target, palette=[dynamic_palette[i]], ax=axes[i])
        axes[i].set_title(f'Bar Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 3. Box Plot - Continuous data
def plot_box_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(continuous_cols))

    for i, column in enumerate(continuous_cols):
        sns.boxplot(data=data, x=target, y=column, palette=[dynamic_palette[i]], ax=axes[i])
        axes[i].set_title(f'Box Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 4. [Add any additional plotting functions here, following the same pattern]

# 5. Violin Plot - Continuous data
def plot_violin_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(continuous_cols))

    for i, column in enumerate(continuous_cols):
        sns.violinplot(data=data, x=target, y=column, palette=[dynamic_palette[i]], ax=axes[i], legend=False)
        axes[i].set_title(f'Violin Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 6. Pie Chart - Categorical data
def plot_pie_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, column in enumerate(categorical_cols):
        counts = data[column].value_counts()
        axes[i].pie(counts, labels=counts.index, colors=get_dynamic_palette(palette, len(counts)),
                   autopct='%1.1f%%', startangle=140)
        axes[i].set_title(f'Pie Chart - {column}', color='white')
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 7. Scatter Plot - Continuous data
def plot_scatter_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    if len(numerical_columns) < 2:
        raise ValueError("Not enough continuous columns for scatter plot.")

    # Plot scatter for every pair of continuous columns
    num_pairs = len(numerical_columns) * (len(numerical_columns) - 1) // 2
    fig, axes = create_grid(num_pairs, cols, per_subplot_size=(5, 5))
    plot_idx = 0

    for i in range(len(numerical_columns)):
        for j in range(i+1, len(numerical_columns)):
            if plot_idx >= len(axes):
                break
            sns.scatterplot(data=data, x=numerical_columns[i], y=numerical_columns[j], hue=target, palette=palette, ax=axes[plot_idx])
            axes[plot_idx].set_title(f'Scatter Plot - {numerical_columns[i]} vs {numerical_columns[j]}', color='white')
            axes[plot_idx].tick_params(colors='white')
            plot_idx += 1

    for ax in axes[plot_idx:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 8. Line Plot - Continuous data
def plot_line_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)
    for column in continuous_cols:
        sns.lineplot(data=data, x=data.index, y=column, label=column)
    plt.title('Line Plot - Continuous Variables', color='white')
    plt.legend()
    plt.show()

# 9. Heatmap - Correlation Matrix
def plot_correlation_matrix(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    plt.figure(figsize=figsize)
    corr = data[numerical_columns].corr()

    # Using cubehelix_palette for color mapping
    cubehelix_palette = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)

    sns.heatmap(corr, annot=True, cmap=cubehelix_palette, linewidths=0.5)
    plt.title("Correlation Matrix", color='white')
    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    plt.show()

# 10. Pair Plot - Continuous data
def plot_pair_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    sns.pairplot(data[numerical_columns + [target]], hue=target, palette=palette)
    plt.suptitle("Pair Plot", y=1.02, color='white')
    plt.show()

# 11. Swarm Plot - Categorical data
def plot_swarm_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for Swarm Plot.")
    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(categorical_cols))

    for i, column in enumerate(categorical_cols):
        sns.swarmplot(data=data, x=column, y=continuous_cols[0], hue=target, palette=[dynamic_palette[i]], ax=axes[i])
        axes[i].set_title(f'Swarm Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 12. Strip Plot - Categorical data
def plot_strip_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for Strip Plot.")
    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(categorical_cols))

    for i, column in enumerate(categorical_cols):
        sns.stripplot(data=data, x=column, y=continuous_cols[0], hue=target, palette=[dynamic_palette[i]], ax=axes[i], jitter=True)
        axes[i].set_title(f'Strip Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 13. KDE Plot - Continuous data 
def plot_kde_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(continuous_cols))

    for i, column in enumerate(continuous_cols):
        sns.kdeplot(data=data, x=column, hue=target, fill=True, common_norm=False, alpha=0.5, palette=[dynamic_palette[i]], ax=axes[i])
        axes[i].set_title(f'KDE Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 14. Ridge Plot - Continuous data
def plot_ridge_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for Ridge Plot.")

    num_plots = len(continuous_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    unique_targets = data[target].unique()
    n_targets = len(unique_targets)
    dynamic_palette = get_dynamic_palette(palette, n_targets)

    for i, column in enumerate(continuous_cols):
        sns.kdeplot(data=data, x=column, hue=target, fill=True, common_norm=False, alpha=0.5, palette=dynamic_palette, ax=axes[i])
        axes[i].set_title(f'Ridge Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 15. Density Plot - Continuous data
def plot_density_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)

    for column in continuous_cols:
        sns.kdeplot(data=data, x=column, hue=target, fill=True, palette=palette, label=column)

    plt.title("Density Plot", color='white')
    plt.legend()
    plt.show()

# 16. Joint Plot - Continuous data
def plot_joint_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    if len(numerical_columns) < 2:
        raise ValueError("Not enough continuous columns for joint plot.")

    # Plot jointplot for every pair of continuous columns
    num_pairs = len(numerical_columns) * (len(numerical_columns) - 1) // 2
    fig, axes = create_grid(num_pairs, cols, per_subplot_size=(5, 5))
    plot_idx = 0

    for i in range(len(numerical_columns)):
        for j in range(i+1, len(numerical_columns)):
            if plot_idx >= len(axes):
                break
            g = sns.jointplot(data=data, x=numerical_columns[i], y=numerical_columns[j], hue=target, palette=palette, kind='scatter')
            g.fig.suptitle(f'Joint Plot - {numerical_columns[i]} vs {numerical_columns[j]}', y=1.02, color='white')
            g.fig.tight_layout()
            g.fig.subplots_adjust(top=0.95)
            plot_idx += 1

    for ax in axes[num_pairs:]:
        ax.set_visible(False)

    plt.show()

# 17. Facet Grid - Categorical data
def plot_facet_grid_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    if len(categorical_columns) == 0 or len(numerical_columns) == 0:
        raise ValueError("Insufficient categorical or continuous columns for Facet Grid.")

    for column in categorical_columns:
        g = sns.FacetGrid(data, col=column, hue=target, palette=palette, height=5, aspect=1)
        g.map(sns.histplot, numerical_columns[0], kde=True)
        g.add_legend()
        plt.subplots_adjust(top=0.9)
        g.fig.suptitle(f'Facet Grid - {column}', color='white')
        plt.show()

# 18. Regression Plot - Continuous data
def plot_regression_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    if len(numerical_columns) < 2:
        raise ValueError("Not enough continuous columns for regression plot.")

    # Plot regression for every pair of continuous columns
    num_pairs = len(numerical_columns) * (len(numerical_columns) - 1) // 2
    fig, axes = create_grid(num_pairs, cols, per_subplot_size=(5, 5))
    plot_idx = 0

    for i in range(len(numerical_columns)):
        for j in range(i+1, len(numerical_columns)):
            if plot_idx >= len(axes):
                break
            sns.regplot(data=data, x=numerical_columns[i], y=numerical_columns[j], scatter_kws={'alpha':0.5}, line_kws={'color': 'red'}, ax=axes[plot_idx])
            axes[plot_idx].set_title(f'Regression Plot - {numerical_columns[i]} vs {numerical_columns[j]}', color='white')
            axes[plot_idx].tick_params(colors='white')
            plot_idx += 1

    for ax in axes[plot_idx:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 19. Dendrogram - Categorical data
def plot_dendrogram_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for dendrogram.")

    # Encode categorical variables
    encoded_data = pd.get_dummies(data[categorical_cols])
    linked = linkage(encoded_data, 'single')

    plt.figure(figsize=figsize)
    dendrogram(linked, labels=data[target].values, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Dendrogram', color='white')
    plt.xticks(color='white')
    plt.yticks(color='white')
    plt.show()

# 20. Donut Chart - Categorical data
def plot_donut_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, column in enumerate(categorical_cols):
        counts = data[column].value_counts()
        wedges, texts, autotexts = axes[i].pie(counts, labels=counts.index, colors=get_dynamic_palette(palette, len(counts)),
                                               autopct='%1.1f%%', startangle=140, pctdistance=0.85)
        # Draw circle
        centre_circle = plt.Circle((0,0),0.70,fc='black')
        axes[i].add_artist(centre_circle)
        axes[i].set_title(f'Donut Chart - {column}', color='white')
        axes[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 21. Bubble Plot - Continuous data
def plot_bubble_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 3:
        raise ValueError("Need at least three continuous columns for bubble plot.")

    # Plot bubble plot for every triplet of continuous columns
    triplets = list(combinations(continuous_cols, 3))
    num_plots = len(triplets)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, (x_col, y_col, size_col) in enumerate(triplets):
        if i >= len(axes):
            break
        sns.scatterplot(data=data, x=x_col, y=y_col, size=size_col, hue=target, palette=palette, sizes=(20, 200), alpha=0.6, ax=axes[i])
        axes[i].set_title(f'Bubble Plot - {x_col} vs {y_col} sized by {size_col}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 22. Sunburst Chart - Categorical data
def plot_sunburst_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    try:
        import plotly.express as px
    except ImportError:
        raise ImportError("Plotly is required for Sunburst Chart. Please install it using pip install plotly.")

    categorical_cols = categorical_columns
    if len(categorical_cols) < 2:
        raise ValueError("Need at least two categorical columns for Sunburst Chart.")

    # Create combinations for sunburst paths
    paths = list(combinations(categorical_cols, 2))

    for path in paths:
        fig = px.sunburst(data, path=path, color=target, color_discrete_sequence=palette,
                          title=f'Sunburst Chart - {" & ".join(path)}')
        fig.update_layout(title_font_color='white')
        fig.show()

# 23. Interactive 3D Scatter Plot - Continuous data using Plotly
def plot_3d_scatter_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 3:
        raise ValueError("Need at least three continuous columns for 3D scatter plot.")

    # Plot 3D scatter for every triplet of continuous columns
    triplets = list(combinations(continuous_cols, 3))

    for (x_col, y_col, z_col) in triplets:
        fig = px.scatter_3d(
            data_frame=data,
            x=x_col,
            y=y_col,
            z=z_col,
            color=target,
            color_discrete_sequence=palette,
            title=f'3D Scatter Plot - {x_col} vs {y_col} vs {z_col}',
            labels={
                x_col: x_col,
                y_col: y_col,
                z_col: z_col,
                target: target
            },
            opacity=0.7
        )
        fig.update_layout(
            title=dict(
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        fig.show()

# 24. Parallel Coordinates - Continuous data
def plot_parallel_coordinates_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    if target not in continuous_cols:
        pass  # Assuming target is categorical or already included
    plt.figure(figsize=figsize)
    parallel_coordinates(data[numerical_columns + [target]], target, color=get_dynamic_palette(palette, len(data[target].unique())))
    plt.title('Parallel Coordinates Plot', color='white')
    plt.show()

# 25. Radar Chart - Categorical data
def plot_radar_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    import matplotlib.colors as mcolors
    from matplotlib import cm
    import numpy as np

    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Radar Chart.")

    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(categorical_cols))

    for i, column in enumerate(categorical_cols):
        counts = data[column].value_counts()
        categories = list(counts.index)
        values = counts.values
        N = len(categories)

        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values = np.concatenate((values, [values[0]]))
        angles += angles[:1]

        ax = axes[i]
        ax.plot(angles, values, color=dynamic_palette[i], linewidth=2)
        ax.fill(angles, values, color=dynamic_palette[i], alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), categories)
        ax.set_title(f'Radar Chart - {column}', color='white')
        ax.tick_params(colors='white')
        ax.grid(color='white')

    # Hide any unused subplots
    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 26. Waterfall Chart - Categorical data
def plot_waterfall_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Waterfall Chart.")

    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, column in enumerate(categorical_cols):
        counts = data[column].value_counts().sort_index()
        cumulative = counts.cumsum()
        axes[i].bar(counts.index, counts.values, color=get_dynamic_palette(palette, len(counts)))
        axes[i].plot(cumulative, color='cyan', marker='o')
        axes[i].set_title(f'Waterfall Chart - {column}', color='white')
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('Count')
        axes[i].tick_params(colors='white')
        axes[i].tick_params(axis='x', colors='white')
        axes[i].tick_params(axis='y', colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# 27. Area Plot - Continuous data
def plot_area_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)

    for column in continuous_cols:
        sns.kdeplot(data=data, x=column, fill=True, label=column, alpha=0.5)

    plt.title('Area Plot - Continuous Variables', color='white')
    plt.legend()
    plt.show()

# 28. Step Plot - Continuous data
def plot_step_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    plt.figure(figsize=figsize)

    for column in continuous_cols:
        sns.lineplot(data=data, x=data.index, y=column, drawstyle='steps', label=column)

    plt.title('Step Plot - Continuous Variables', color='white')
    plt.legend()
    plt.show()

# 29. Trellis Plot - Categorical data
def plot_trellis_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    continuous_cols = numerical_columns
    if len(categorical_cols) == 0 or len(continuous_cols) == 0:
        raise ValueError("Insufficient categorical or continuous columns for Trellis Plot.")

    for column in categorical_cols:
        g = sns.FacetGrid(data, col=column, hue=target, palette=palette, height=5, aspect=1)
        g.map(sns.histplot, continuous_cols[0], kde=True)
        g.add_legend()
        plt.subplots_adjust(top=0.9)
        g.fig.suptitle(f'Trellis Plot - {column}', color='white')
        plt.show()

# 30. Lollipop Chart - Categorical data
def plot_lollipop_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Lollipop Chart.")

    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, column in enumerate(categorical_cols):
        counts = data[column].value_counts()
        axes[i].stem(counts.index, counts.values, linefmt='C0-', markerfmt='C0o', basefmt=" ", use_line_collection=True)
        axes[i].set_title(f'Lollipop Chart - {column}', color='white')
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('Count')
        axes[i].tick_params(colors='white')
        axes[i].tick_params(axis='x', colors='white')
        axes[i].tick_params(axis='y', colors='white')

    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 31. PCA Visualization - Continuous data
def plot_pca_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE, n_components=2):
    continuous_cols = numerical_columns
    if len(continuous_cols) < n_components:
        raise ValueError(f"Need at least {n_components} continuous columns for PCA.")

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(data[continuous_cols])
    pca_df = pd.DataFrame(data=components, columns=[f'PC{i+1}' for i in range(n_components)])
    pca_df[target] = data[target]

    plt.figure(figsize=figsize)
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue=target, palette=palette)
    plt.title('PCA Visualization', color='white')
    plt.legend()
    plt.show()

# 32. TSNE Visualization - Continuous data
def plot_tsne_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 10), palette=DEFAULT_PALETTE, n_components=2):
    continuous_cols = numerical_columns
    if len(continuous_cols) == 0:
        raise ValueError("No continuous columns available for t-SNE.")

    tsne = TSNE(n_components=n_components, random_state=42)
    components = tsne.fit_transform(data[continuous_cols])
    tsne_df = pd.DataFrame(data=components, columns=[f'Dim{i+1}' for i in range(n_components)])
    tsne_df[target] = data[target]

    plt.figure(figsize=figsize)
    sns.scatterplot(data=tsne_df, x='Dim1', y='Dim2', hue=target, palette=palette)
    plt.title('t-SNE Visualization', color='white')
    plt.legend()
    plt.show()

# 33. Mosaic Plot - Categorical data
def plot_mosaic_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    try:
        from statsmodels.graphics.mosaicplot import mosaic
    except ImportError:
        raise ImportError("Statsmodels is required for Mosaic Plot. Please install it using pip install statsmodels.")

    categorical_cols = categorical_columns
    if len(categorical_cols) < 2:
        raise ValueError("Need at least two categorical columns for Mosaic Plot.")

    num_plots = len(categorical_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, column in enumerate(categorical_cols):
        if i >= len(axes):
            break
        plt.sca(axes[i])
        mosaic(data, [column, target], title=f'Mosaic Plot - {column} vs {target}', facecolor=lambda x: palette[x[1] % len(palette)])
        plt.title(f'Mosaic Plot - {column} vs {target}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 34. Boxen Plot - Continuous data 
def plot_boxen_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    num_plots = len(continuous_cols)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    dynamic_palette = get_dynamic_palette(palette, len(continuous_cols))

    for i, column in enumerate(continuous_cols):
        sns.boxenplot(data=data, x=target, y=column, palette=[dynamic_palette[i]], ax=axes[i])
        axes[i].set_title(f'Boxen Plot - {column}', color='white')
        axes[i].tick_params(colors='white')
    
    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 35. Stacked Bar Plot - Categorical data
def plot_stacked_bar_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    categorical_cols = categorical_columns
    for column in categorical_cols:
        counts = pd.crosstab(data[column], data[target])
        counts.plot(kind='bar', stacked=True, color=get_dynamic_palette(palette, counts.shape[1]))
        plt.title(f'Stacked Bar Plot - {column}', color='white')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.legend(title=target)
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.show()

# 36. Funnel Chart - Categorical data
def plot_funnel_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    try:
        import plotly.express as px
    except ImportError:
        raise ImportError("Plotly is required for Funnel Chart. Please install it using pip install plotly.")

    categorical_cols = categorical_columns
    if len(categorical_cols) == 0:
        raise ValueError("No categorical columns for Funnel Chart.")

    for column in categorical_cols:
        counts = data[column].value_counts().reset_index()
        counts.columns = [column, 'count']
        fig = px.funnel(counts, x='count', y=column, title=f'Funnel Chart - {column}', color_discrete_sequence=palette)
        fig.show()

# 37. Hexbin Plot - Continuous data
def plot_hexbin_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 2:
        raise ValueError("Need at least two continuous columns for Hexbin Plot.")

    # Plot hexbin for every pair of continuous columns
    pairs = list(combinations(continuous_cols, 2))
    num_plots = len(pairs)
    fig, axes = create_grid(num_plots, cols, per_subplot_size=(5, 5))

    for i, (x_col, y_col) in enumerate(pairs):
        if i >= len(axes):
            break
        hb = axes[i].hexbin(data[x_col], data[y_col], gridsize=30, cmap='viridis')
        axes[i].set_xlabel(x_col)
        axes[i].set_ylabel(y_col)
        axes[i].set_title(f'Hexbin Plot - {x_col} vs {y_col}', color='white')
        axes[i].tick_params(colors='white')
        fig.colorbar(hb, ax=axes[i], label='count in bin')

    for ax in axes[num_plots:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()

# 38. Gantt Chart - Categorical data
def plot_gantt_categorical(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    try:
        import plotly.express as px
    except ImportError:
        raise ImportError("Plotly is required for Gantt Chart. Please install it using pip install plotly.")

    # Assuming data has 'Task', 'Start', 'Finish' columns
    required_cols = ['Task', 'Start', 'Finish']
    if not all(col in data.columns for col in required_cols):
        raise ValueError("Data must contain 'Task', 'Start', and 'Finish' columns for Gantt Chart.")

    fig = px.timeline(data, x_start="Start", x_end="Finish", y="Task", color=target, color_discrete_sequence=palette, title='Gantt Chart')
    fig.update_yaxes(autorange="reversed")  # To display tasks top-down
    fig.update_layout(title_font_color='white')
    fig.show()

# 39. Interactive 3D Surface Plot - Continuous data using Plotly
def plot_3d_surface_continuous(data, target, numerical_columns, categorical_columns, cols=3, figsize=(15, 15), palette=DEFAULT_PALETTE):
    continuous_cols = numerical_columns
    if len(continuous_cols) < 3:
        raise ValueError("Need at least three continuous columns for 3D surface plot.")

    # Plot 3D surface for every triplet of continuous columns
    triplets = list(combinations(continuous_cols, 3))

    for (x_col, y_col, z_col) in triplets:
        x = data[x_col]
        y = data[y_col]
        z = data[z_col]

        # Create grid values first.
        xi = np.linspace(x.min(), x.max(), 100)
        yi = np.linspace(y.min(), y.max(), 100)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate
        zi = griddata((x, y), z, (xi, yi), method='linear')

        # Create the surface plot
        fig = go.Figure(data=[go.Surface(x=xi, y=yi, z=zi, colorscale='Viridis')])

        fig.update_layout(
            title=f'3D Surface Plot - {x_col} vs {y_col} vs {z_col}',
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                xaxis=dict(color='white'),
                yaxis=dict(color='white'),
                zaxis=dict(color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        fig.show()

# 40. Additional Plots can be added here following the same pattern

# General visualize function


def visualize(
    data,
    graphics='kde',
    cols=3,
    figsize=(15, 15),
    palette=DEFAULT_PALETTE
):
    """
    Visualizes the data using the specified plot type.

    Args:
        data (pandas.DataFrame or array-like): Data to visualize.
        plot_type (str, optional): The type of plot to generate (e.g., 'scatter', 'bar', 'heatmap', 'corr'). Defaults to 'scatter'.
        **plot_params: Additional parameters for the plot (e.g., title, labels, color).

    Returns:
        None: Displays the plot.

    Usage:
        >>> from mkyz import visualization as viz
        >>> viz.visualize(data=data, plot_type='corr')
    """
    
    if data is None:
        raise ValueError("Data must be provided.")
    
    # Beklenen tuple yapısı: (df, target_column, numerical_columns, categorical_columns)
    if isinstance(data, tuple):
        if len(data) != 4:
            raise ValueError("Tuple must contain exactly four elements: (df, target_column, numerical_columns, categorical_columns).")
        df, target_column, numerical_columns, categorical_columns = data
    else:
        raise ValueError("Data must be a tuple containing (df, target_column, numerical_columns, categorical_columns).")
    
    graphics = graphics.lower()

    # Grafik fonksiyonlarını tanımlayın veya ithal edin
    graphics_dict = {
        'corr': plot_correlation_matrix,

        # Sürekli görselleştirmeler
        'histogram': histogram_continuous,
        'box': plot_box_continuous,
        'scatter': plot_scatter_continuous,
        'line': plot_line_continuous,
        'kde': plot_kde_continuous,
        'pair': plot_pair_continuous,
        'violin': plot_violin_continuous,
        'ridge': plot_ridge_continuous,
        'area': plot_area_continuous,
        'step': plot_step_continuous,
        'density': plot_density_continuous,
        'bubble': plot_bubble_continuous,
        '3dscatter': plot_3d_scatter_continuous,
        'parallel': plot_parallel_coordinates_continuous,
        'hexbin': plot_hexbin_continuous,
        'boxen': plot_boxen_continuous,
        '3dsurface': plot_3d_surface_continuous,
        'pca': plot_pca_continuous,
        'tsne': plot_tsne_continuous,
        'regression': plot_regression_continuous,
        'joint': plot_joint_continuous,

        # Kategorik görselleştirmeler
        'bar': plot_bar_categorical,
        'pie': plot_pie_categorical,
        'swarm': plot_swarm_categorical,
        'strip': plot_strip_categorical,
        'trellis': plot_trellis_categorical,
        'lollipop': plot_lollipop_categorical,
        'mosaic': plot_mosaic_categorical,
        'donut': plot_donut_categorical,
        'sunburst': plot_sunburst_categorical,
        'radar': plot_radar_categorical,
        'waterfall': plot_waterfall_categorical,
        'gantt': plot_gantt_categorical,
        'funnel': plot_funnel_categorical,
        'stackedbar': plot_stacked_bar_categorical,
        'dendrogram': plot_dendrogram_categorical,
        'facetgrid': plot_facet_grid_categorical,
    }

    if graphics not in graphics_dict:
        raise ValueError(f"Invalid graphics type. Choose from: {', '.join(graphics_dict.keys())}")
    
    graphics_func = graphics_dict[graphics]
    
    # Grafik fonksiyonunu çağırın
    graphics_func(df, target_column, numerical_columns, categorical_columns, cols, figsize, palette)
