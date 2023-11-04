# Author B. Ivasic
# Generates a scatter plot as shooting stars from the centroid to facilitate visual analysis (and because it looks cool :-) )
    # df:            dataframe to plot
    # x_axis_col:    column name of the x axis
    # x_axis_label:  label for the x axis
    # y_axis_col:    column name of the y axis
    # y_axis_label:  label for the y axis
    # cluster_col:   column name of the cluster group
    # hover_col:     column name / list of names to include as hover data
    # colours:      list of colour names

import pandas as pd
import hvplot.pandas


def shooting_stars_plot( df, x_axis_column_name, x_axis_label, y_axis_column_name, y_axis_label, cluster_col, hover_cols, colours=None ):
# Create a new data frame which contains the cluster "point" values followed by the centroid values so that
# when plotting the lines from the centroid to the dot we don't get scattered lines going from the centroid to the dot and then to the next dot.
# Visual concept inspired by https://towardsdatascience.com/visualizing-clusters-with-pythons-matplolib-35ae03d87489

# Use the mean (average) to determine the centroids of each cluster
    centroids = df.groupby(cluster_col).mean() # Group by cluster and then apply the mean to get the "centre" of the cluster for each column


    # Now create a new dataframe inserting the centroid in between each of the original data's row
    centroids_to_points = [] # Create an empty list which we will append the data to and later turn into a dataframe which will look like this:
    #  df[0]
    #  centroid
    #  df[1]
    #  centroid
    # etc

    for index, row in df.iterrows():  # Run through the original data frame.
        # Append a row from market_data_predictions_df
        rcd = [ int(row[cluster_col]), row[x_axis_column_name], row[y_axis_column_name] ]   # Transfer the cluster data from the original data frame
        centroids_to_points.append( rcd )                                                   # Append the row's cluster data to the list

        # Append the related centroid of the cluster as a new data point to the same cluster that the row data relates to
        rcc = [ int(row[cluster_col]),
                centroids.iloc[int(row[cluster_col]),df.columns.get_loc(x_axis_column_name)],
                centroids.iloc[int(row[cluster_col]),df.columns.get_loc(y_axis_column_name)] ]  # Create a new cluster record using the centroid's values
        centroids_to_points.append(rcc)                                                         # Append the centroid values to the list


    # Create a dataframe from the centroids_to_points list, setting the column names as required
    centroids_to_points_df = pd.DataFrame( centroids_to_points, columns = [cluster_col, x_axis_column_name, y_axis_column_name ] )

    # Now generate a plot of lines from the centroid to the cluster points in the 
    # designated colours. Effectively, the line goes from the first cluster point to the centroid, then to the next cluster point and then back to the centroid, and so on.

    df_plot = df.hvplot.scatter(
        x=x_axis_column_name,                                       # Set x axis data
        xlabel=x_axis_label,                                        # Set x axis label
        y=y_axis_column_name,                                       # Set y axis data
        ylabel=y_axis_label,                                        # Set y axis label
        by=cluster_col,                                             # Group by the cluster
        title="Resulting Clusters - " + x_axis_label + " vs " + y_axis_label, # Set the title
        hover_cols=hover_cols,                                      # Add the column name(s) for hover labels
        grid=True,                                                  # Show the grid
        color=colours,                                              # Specify the colour scheme so we can ensure the shooting star colours match for corresponding cluster
        line_width=1,                                               # Set the width of the dot
        alpha=1.0                                                   # Set the alpha to minimum opacity for the dots for maximum visual effect
    ).opts(xformatter="%.1f", yformatter="%.1f")                    # Format the x and y numeric labels
    
    
    centroid_stars_plot = centroids_to_points_df.hvplot.line(
        x=x_axis_column_name,                              # Set x axis data
        y=y_axis_column_name,                              # Set y axis data
        by=cluster_col,                                    # Group by the cluster so the points in the same cluster get the same colours
        line_width=3,                                      # Set the line width so it is almost as thick as the dots
        color=colours,                                     # Use the specified colors for the line to ensure consistency with the dots
        hover=False,                                       # Turn off hover on the line as it causes confusion
        alpha=0.4                                          # Give the line opacity incase it goes over any cluster points
    )
    
    return df_plot * centroid_stars_plot  # Join the two plots and return the combined plot handle
