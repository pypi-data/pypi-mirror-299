import pandas as pd
import altair as alt


def plot_time_series_by_doy(df: pd.DataFrame, 
                     columns_to_plot: list = None, 
                     plot_options: dict = None, 
                     title: str = 'Time Series Plot', 
                     width: int = 600, 
                     height: int = 400, 
                     interactive: bool = True,
                     substrings: list = None,
                     exclude_columns: list = None,
                     group_by: str = None,
                     facet: bool = False):
    """
    Plots a time series using Altair from a pandas DataFrame, focusing on the range of day_of_year
    where data exists, with optional plot customizations and general properties.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    columns_to_plot (list): List of column names to plot on the y-axis. 
                            If None, columns are selected based on `substrings`.
    plot_options (dict): Optional dictionary with customization for each column. The keys are the column names, 
                         and the values are dictionaries with Altair properties like:
                         - 'mark_type' (str): Mark type for the chart (e.g., 'line', 'point', 'bar').
                         - 'color' (str): Color of the line or points.
                         - 'axis' (str): Either 'left' or 'right' to specify which y-axis to use.
                         - 'size' (float): Size of the points (if using points).
                         - 'opacity' (float): Opacity level for the mark.
                         - 'strokeWidth' (float): Width of the line if using line marks.
    title (str): Title of the chart. Defaults to 'Time Series Plot'.
    width (int): Width of the chart. Defaults to 600.
    height (int): Height of the chart. Defaults to 400.
    interactive (bool): Whether the chart should be interactive (zoomable, scrollable). Defaults to True.
    substrings (list): List of substrings to select columns by matching names containing any of them. Defaults to None.
    exclude_columns (list): List of columns to exclude from the selected columns. Defaults to None.
    group_by (str): Optional column name to group the data by (e.g., 'year'). Defaults to None.
    facet (bool): Whether to create a faceted plot by 'group_by'. Defaults to False.

    Returns:
    alt.Chart: The Altair chart object.
    """
    
    # Ensure that 'day_of_year' is in the DataFrame
    if 'day_of_year' not in df.columns:
        raise ValueError("'day_of_year' column is required in the DataFrame")

    # Handle column selection based on substrings and exclusions
    if columns_to_plot is None and substrings:
        selected_columns = []
        
        # Iterate over the substrings and filter columns containing any of them
        for substring in substrings:
            selected_columns.extend([col for col in df.columns if substring in col]) 
        
        # Remove duplicates in case a column matches multiple substrings
        selected_columns = list(set(selected_columns))
        
        # If no columns were found, return the entire DataFrame columns excluding 'day_of_year'
        if not selected_columns:
            selected_columns = df.columns.tolist()
            selected_columns.remove('day_of_year')
            
        # Handle exclusion of columns
        if exclude_columns:
            selected_columns = [col for col in selected_columns if col not in exclude_columns]

        columns_to_plot = selected_columns
    
    # If no columns were specified and no substrings provided, raise an error
    if columns_to_plot is None:
        raise ValueError("No columns specified for plotting.")

    # Filter out rows where all selected columns are NaN
    df_filtered = df.dropna(subset=columns_to_plot, how='all')

    # Focus only on the range of day_of_year where data exists
    min_day = df_filtered['day_of_year'].min()
    max_day = df_filtered['day_of_year'].max()

    df_filtered = df_filtered[(df_filtered['day_of_year'] >= min_day) & (df_filtered['day_of_year'] <= max_day)]

    # Melt the dataframe to long format for Altair plotting
    id_vars = ['day_of_year']
    
    # If grouping by 'year' or another column, include it as an identifier
    if group_by and group_by in df.columns:
        id_vars.append(group_by)

	# Melt the DataFrame
    df_melted = df_filtered.melt(
        id_vars=id_vars,
        value_vars=columns_to_plot, 
        var_name='variable', value_name='value')
    
    ## Extract the ROI number and create a new column
    
    #df_melted['roi'] = df_melted['variable'].str.extract(r'L3_ROI_(\d+)_')
    ## Remove the ROI prefix from the column names
    #df_melted['variable'] = df_melted['roi_column'].str.replace(r'L3_ROI_\d+_', '', regex=True)
    
	## Drop the original column name and keep only necessary columns 
    #df_melted = df_melted[['roi', 'variable', 'value']]
	
 	# Optional: Rename columns for clarity
	# df_melted.rename(columns={'variable': 'metric'}, inplace=True)   
  
 	# Initialize the base char
    base = alt.Chart(df_melted).encode(
        x='day_of_year:Q'
    )

	# Container for layers
    layers = []

    # Add each column with custom options (if provided)
    for column in columns_to_plot:
        # Default options
        mark_type = 'line'  # Default to line
        color = 'variable:N'  # Default to Altair's color scheme
        y_axis = alt.Y('value:Q')  # Default to single y-axis
        size = None
        opacity = 1.0
        strokeWidth = 2.0  # Default line width for line marks

        # Apply custom options if available
        if plot_options and column in plot_options:
            # Set mark_type (e.g., line, point, bar)
            if 'mark_type' in plot_options[column]:
                mark_type = plot_options[column]['mark_type']

            # Set color
            if 'color' in plot_options[column]:
                color = alt.value(plot_options[column]['color'])
            
            # Set y-axis (left or right)
            if 'axis' in plot_options[column]:
                if plot_options[column]['axis'] == 'right':
                    y_axis = alt.Y('value:Q', axis=alt.Axis(title=column, orient='right'))
                else:
                    y_axis = alt.Y('value:Q', axis=alt.Axis(title=column, orient='left'))
            
            # Set size (for point marks)
            if 'size' in plot_options[column]:
                size = plot_options[column]['size']

            # Set opacity
            if 'opacity' in plot_options[column]:
                opacity = plot_options[column]['opacity']
            
            # Set stroke width (for line marks)
            if 'strokeWidth' in plot_options[column]:
                strokeWidth = plot_options[column]['strokeWidth']

        # Create the chart for the current column
        if mark_type == 'line':
            layer = base.mark_line(strokeWidth=strokeWidth, opacity=opacity).encode(
                y=y_axis,
                color=color
            ).transform_filter(
                alt.datum.variable == column
            )
        elif mark_type == 'point':
            layer = base.mark_point(size=size, opacity=opacity).encode(
                y=y_axis,
                color=color
            ).transform_filter(
                alt.datum.variable == column
            )
        else:  # Fallback for unsupported marks
            layer = base.mark_line().encode(
                y=y_axis,
                color=color
            ).transform_filter(
                alt.datum.variable == column
            )
        
        layers.append(layer)

    # Combine all layers into one chart
    chart = alt.layer(*layers).properties(
        width=width,
        height=height,
        title=title
    )

    # Add interactivity if specified
    if interactive:
        chart = chart.interactive()

    # Group by the 'group_by' column if specified
    if group_by and group_by in df.columns:
        if facet:
            # Create a faceted chart
            chart = chart.facet(
                facet=alt.Facet(f'{group_by}:N', columns=3),
                columns=3
            )
        else:
            # Overlay the lines and color by 'group_by'
            chart = chart.encode(
                color=f'{group_by}:N'
            )

    return chart
