"""
Visualization Module

Provides utilities for visualizing routes, convergence, and comparative
results for the VRP optimization.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def plot_routes(
    routes,
    locations,
    title="Vehicle Routes",
    save_path=None
):
    """
    Plot vehicle routes on a 2D map.
    
    Parameters
    ----------
    routes : list
        List of routes, where each route is a list of node indices
    locations : np.ndarray
        Array of (x, y) coordinates for each node
    title : str
        Title for the plot
    save_path : str, optional
        Path to save the figure
    """
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot depot
    ax.scatter(
        locations[0, 0],
        locations[0, 1],
        c='red',
        s=200,
        marker='*',
        label='Depot',
        zorder=5
    )
    
    # Plot customers
    if len(locations) > 1:
        ax.scatter(
            locations[1:, 0],
            locations[1:, 1],
            c='blue',
            s=100,
            marker='o',
            label='Customers',
            zorder=4
        )
    
    # Plot routes
    colors = plt.cm.tab10(np.linspace(0, 1, len(routes)))
    
    for vehicle, route in enumerate(routes):
        route_with_depot = [0] + route + [0]
        route_coords = locations[route_with_depot]
        
        ax.plot(
            route_coords[:, 0],
            route_coords[:, 1],
            color=colors[vehicle],
            linewidth=2,
            label=f'Vehicle {vehicle + 1}',
            zorder=3
        )
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def plot_convergence(
    iterations,
    values,
    label="Objective Value",
    title="Convergence Plot",
    save_path=None
):
    """
    Plot convergence of optimization algorithm.
    
    Parameters
    ----------
    iterations : list
        List of iteration numbers
    values : list
        List of objective values
    label : str
        Label for the y-axis
    title : str
        Title for the plot
    save_path : str, optional
        Path to save the figure
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(iterations, values, 'b-o', linewidth=2, markersize=6)
    ax.set_xlabel('Iteration')
    ax.set_ylabel(label)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def plot_comparison(
    methods,
    results,
    title="Algorithm Comparison",
    save_path=None
):
    """
    Compare results across multiple solution methods.
    
    Parameters
    ----------
    methods : list
        List of method names
    results : list
        List of objective values
    title : str
        Title for the plot
    save_path : str, optional
        Path to save the figure
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(methods)))
    bars = ax.bar(methods, results, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Objective Value (Route Cost)')
    ax.set_title(title)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{height:.2f}',
            ha='center',
            va='bottom'
        )
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()


def plot_noise_robustness(
    error_rates,
    probabilities,
    title="Noise Robustness (Depolarizing Error)",
    save_path=None
):
    """
    Plot the probability of finding the optimal route under different error rates.
    
    Parameters
    ----------
    error_rates : list
        List of error rates tested
    probabilities : list
        List of probabilities of measuring the optimal solution
    title : str
        Title for the plot
    save_path : str, optional
        Path to save the figure
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(error_rates, probabilities, 'r-s', linewidth=2, markersize=8)
    ax.set_xlabel('Depolarizing Error Rate')
    ax.set_ylabel('Probability of Optimal Solution')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(probabilities) * 1.1 if probabilities else 1.0)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.close()
