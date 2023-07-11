# coding: utf-8
"""
Created on 5/23/2023 4:32 PM
@author: zn
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

'''
Radial plot of the universe
Civ starts as dot
Wars as arrows

'''


def main():
    # Create the figure and subplots
    fig = make_subplots(rows=1, cols=1, subplot_titles=("Animated Scatter Plot in Polar Coordinates"))

    # Set the layout for the polar subplot
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        )
    )

    # Create the scatter trace
    scatter = go.Scatterpolar(
        r=[],  # Empty list to store data for each frame
        theta=[],  # Empty list to store data for each frame
        mode='markers',
        marker=dict(
            symbol='circle',
            size=5,
            color='blue'
        )
    )

    # Add the scatter trace to the figure
    fig.add_trace(scatter)

    # Define the animation frames
    frames = []

    radius = []
    theta = []

    # Create the animation frames
    for frame in range(100):
        # theta, radius = generate_data()
        radius.append(np.random.rand())
        theta.append(np.random.rand() * 360)

        frame_data = go.Frame(
            data=[go.Scatterpolar(
                r=radius,
                theta=theta,
                mode='markers',
                marker=dict(
                    symbol='circle',
                    size=5,
                    color='blue'
                )
            )],
            name=f'frame_{frame}'
        )

        frames.append(frame_data)

    fig.frames = frames

    # Set animation options
    animation_opts = dict(frame=dict(duration=200, redraw=True), fromcurrent=True)

    # Update layout to include animation options
    fig.update_layout(
        updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None, animation_opts])])])

    # Show the figure
    fig.show()

    return


if __name__ == '__main__':
    main()
    print('All Done.')
