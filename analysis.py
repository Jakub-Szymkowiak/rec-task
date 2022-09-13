from src.components import *
from src.utils import *

from functools import cmp_to_key

import plotly.graph_objects as go
import plotly.express as px
import numpy as np

group_colors = [
        Color(0,   0,   0  ),
        Color(255, 0,   0  ),
        Color(0,   255, 0  ),
        Color(0,   0,   255),
        Color(255, 255, 0  ),
        Color(0,   255, 255),
        Color(255, 0,   255),
        Color(255, 255, 255)
    ]

class ColorGrouping:
    group_colors = group_colors
    group_colors_str = [c.to_str() for c in group_colors]
    
    def __agent_comp(A: Agent, B: Agent):
        return ColorUtils.single_color_comp(A.color, B.color)

    def __agent_to_group_idx(A: Agent):
        distances = [ColorUtils.normalized_sRGB(A.color, c) for c in ColorGrouping.group_colors]

        return np.argmin(distances)

    def print_group_colors():
        for c in ColorGrouping.group_colors_str:
            print(c)

    def group_colors_plot(group_counts: list=np.ones(8), demo: bool=False, title: str=None):
        max_grp_size = np.max(group_counts)
        size = np.log1p(group_counts) / np.log1p(max_grp_size) * 75
        
        x = [0, 1, 2, 3, 0, 1, 2, 3]
        y = [0, 0, 0, 0, 2, 2, 2, 2]

        marker = dict(
            color=ColorGrouping.group_colors_str,
            size=list(size)
        )

        if demo:
            text = list(ColorGrouping.group_colors_str)
        else:
            text = list(group_counts)

        fig = go.Figure(
            go.Scatter(
                x=x, 
                y=y, 
                mode="markers+text",
                marker=marker,
                text=text,
                textposition="bottom center"
            )
        )

        fig.update_layout(title=title)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

        return fig

    def population_to_group_counts(population: list):
        grp_indeces = [ColorGrouping.__agent_to_group_idx(A) for A in population]

        values, counts = np.unique(grp_indeces, return_counts=True)

        group_counts = np.zeros(8)
        for i, v in enumerate(values):
            group_counts[v] = counts[i]
        
        return group_counts

    def sort_agents_by_color(agents: list):
        order = cmp_to_key(ColorGrouping.__agent_comp)
        return sorted(agents, key=order)

class Plots:
    def heatmap(data: np.ndarray, x: np.ndarray, y: np.ndarray, labels: dict):
        title = "Wpływ parametrów symulacji na wielkość populacji po zakończeniu eksperymentu"

        fig = px.imshow(data, labels=labels, x=x, y=y, text_auto=True, aspect="auto")
        fig.update_layout(title=title)
        return fig
    
    def line(data: np.ndarray, x: np.ndarray, lvl: np.ndarray, lvl_name: str, swap: bool, labels: dict, log: bool=True):
        title = "Wpływ parametrów symulacji na wielkość populacji po zakończeniu eksperymentu"

        fig = go.Figure()

        if swap:
            data = np.swapaxes(data, 0, 1)            

        for i in range(len(lvl)):
            lvl_value = np.around(lvl[i], 2)

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=np.log1p(data[i]) if log else data[i],
                    name=f"{lvl_name}={lvl_value}"
                )
            )
        
        fig.update_layout(
            title=title,
            xaxis_title=labels["x"],
            yaxis_title=labels["y"]
        )

        return fig

    def single_line(x: np.ndarray, y: np.ndarray, labels: dict):

        fig = go.Figure()           

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y
            )
        )           
        
        fig.update_layout(
            title=labels["title"],
            xaxis_title=labels["x"],
            yaxis_title=labels["y"]
        )

        return fig

class MutantAnalysis:
    def get_mutants(population):
        return [A for A in population if A.is_mutant == True]

    def get_mutant_share(population):
        mutants = MutantAnalysis.get_mutants(population)
        return len(mutants) / len(population)