
import numpy as np
import plotly.graph_objects as go

def generate_unit_sphere_grid(num_points=100):
    theta, phi = np.linspace(0, 2 * np.pi, num_points), np.linspace(0, np.pi, num_points)
    theta, phi = np.meshgrid(theta, phi)
    
    zx_surface = np.cos(theta) * np.sin(phi)
    zy_surface = np.sin(theta) * np.sin(phi)
    zz_surface = np.cos(phi)
    
    return zx_surface, zy_surface, zz_surface

def compute_interpolated_values(xx, xy, xz, v, num_points=100):
    zx_surface, zy_surface, zz_surface = generate_unit_sphere_grid(num_points)
    n1, n2 = zx_surface.shape

    electrode_positions = np.vstack([xx, xy, xz]).T 
    grid_positions = np.dstack([zx_surface, zy_surface, zz_surface]).reshape(-1, 3)

    dot_products = np.dot(grid_positions, electrode_positions.T)
    distances = np.arccos(np.clip(dot_products, -1.0, 1.0))

    weights = np.exp(-distances)
    weighted_values = np.dot(weights, v) / np.sum(weights, axis=1)
    
    interpolated_values = weighted_values.reshape(n1, n2)
    
    return zx_surface, zy_surface, zz_surface, interpolated_values

def smoothed_sphere_plot(electrode_positions, values, num_points=100, marker_size=10, scale_factor=1.2):
    xx, xy, xz = electrode_positions[:, 0], electrode_positions[:, 1], electrode_positions[:, 2]
    
    assert np.allclose(np.sum(electrode_positions**2, axis=1), 1), "All points must lie on the unit sphere."
    
    zx_surface, zy_surface, zz_surface, ivals = compute_interpolated_values(xx, xy, xz, values, num_points)

    xx_scaled, xy_scaled, xz_scaled = xx * scale_factor, xy * scale_factor, xz * scale_factor

    fig = go.Figure(data=[
        go.Surface(x=zx_surface, y=zy_surface, z=zz_surface, surfacecolor=ivals, cmin=0, cmax=1),
        go.Scatter3d(x=xx_scaled, y=xy_scaled, z=xz_scaled, mode='markers', marker=dict(size=marker_size, color='black'))
    ])
    
    fig.update_layout(scene=dict(
        xaxis=dict(showbackground=False, showticklabels=False, title=''),
        yaxis=dict(showbackground=False, showticklabels=False, title=''),
        zaxis=dict(showbackground=False, showticklabels=False, title='')
    ), width=800, height=800)
    
    return fig

def plot_smoothed_sphere(electrode_positions, values):
    values = values.astype(float)
    values /= np.linalg.norm(values)

    fig = smoothed_sphere_plot(electrode_positions, values, num_points=200, marker_size=8)
    fig.show()
    