# coding=utf-8
import numpy as np

import PIL.Image

import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.axes_grid1 import ImageGrid

import scipy.interpolate


def load_image_grayscale(path):
    "Load a grayscale image by path"
    return np.asarray(PIL.Image.open(path).convert('L'))


def image_grid(images, nrows=1, ncols=None, separate_colorbars=False, share_all=False, imshow_opts={}):
    """Plot a grid of images from list or dict
    
    Examples:
        
        image_grid([im1, im2, im3], nrows=2)
        
        image_grid({'A': image_a, 'B': image_b})
    
    Parameters
    --------------
    images : list or dict
            Images to plot. If a dict, the format is {'name1': im1, 'name2': im2}
    
    nrows : int
            Number of grid rows
    
    ncols : int
            Number of grid columns. If None, a suitable number is calculated.            
    
    separate_colorbars : bool
            If True, each image gets its own colorbar and colors are NOT normalized.
            If False, a shared colorbar is created, and the image colors are normalized.
            
    share_all: bool
            If true, the subaxes will share coordinate system, and zoom/move together.
            
    imshow_opts: dict
            Keyword arguments passed to plt.imshow(). e.g {'cmap': 'gray', 'interpolation': 'nearest'}
            
    Returns
    ---------------
    axes : list of Axes objects
        The Axes objects
            
    """
    try:
        names, images = images.keys(), images.values()
    except AttributeError:
        names = [None] * len(images)
    
    if not ncols:
        ncols = int(np.ceil(len(images) / nrows))
    
    if separate_colorbars:
        norm = None
    else:
        vmin = min(np.min(im) for im in images)
        vmax = max(np.max(im) for im in images)
        norm = matplotlib.colors.Normalize(vmax=vmax, vmin=vmin)
    
    fig = plt.figure()
    cbar_mode = 'each' if separate_colorbars else 'single'
    grid = ImageGrid(fig, 111, (nrows, ncols), cbar_mode=cbar_mode, share_all=share_all)
    
    axes = []
    for ax, name, im in zip(grid, names, images):
        handle = ax.imshow(im, norm=norm, **imshow_opts)
        if name:
            ax.set_title(name)    
        ax.cax.colorbar(handle)
        ax.cax.toggle_label(True)
        axes.append(ax)
        
    return axes

def gopimage(V, scale=1, ax=None):
    """Display color representation of motion field
    
    Parameters
    ----------------
    V : array of shape (R, C, 2), or complex array of shape (R, C)
        The motion field in (x, y) order
    
    scale: float
        Scale the magnitude
        
    ax : Axes
        Axes object to plot to, or None to create a new figure        
    
    Original MATLAB implementation by Gunnar Farnebäck, CVL, Linköping University
    Python re-implementation by Hannes Ovrén, CVL, Linköping University, 2018
    """
    
    if V.ndim == 2 and V.dtype == np.complex:
        W = V
    elif V.ndim == 3 and V.shape[2] == 2:
        Vx = V[..., 0]
        Vy = V[..., 1]
        
        # Complex representation
        W = Vx + 1j * Vy
    else:
        raise ValueError("Input must be real MxNx2 array, or complex MxN array")
        
        
    max_mag = np.max(np.abs(W))
    
    #Normalize magnitude
    if not max_mag == 0:
        W /= max_mag

    # Setu colortable with 257 entries. Last is to make it cyclic (2pi equivalent with 0)
    gtab = np.vstack((GOPTABLE, GOPTABLE[0]))
    gtab_angles = 2 * np.pi * np.arange(256 + 1) / 256;
    cmap_table = scipy.interpolate.interp1d(gtab_angles, gtab, axis=0)

        
    abs_w = np.minimum(1, scale * np.abs(W))
    angle_w = np.clip(np.pi + np.angle(-W), 0, 2*np.pi)
    rows, cols = V.shape[:2]
    angle_im = cmap_table(angle_w.flat).reshape(rows, cols, 3)
    
    gopim = np.atleast_3d(abs_w) * angle_im
    
    if ax is None:
        _, ax = plt.subplots()
    
    imh = ax.imshow(gopim)
    
    
### gopimage colormap table
GOPTABLE = np.array([[0.28125   , 0.90234375, 0.140625  ],
       [0.26953125, 0.91015625, 0.1484375 ],
       [0.2578125 , 0.9140625 , 0.16015625],
       [0.24609375, 0.921875  , 0.16796875],
       [0.234375  , 0.9296875 , 0.1796875 ],
       [0.22265625, 0.93359375, 0.19140625],
       [0.2109375 , 0.94140625, 0.203125  ],
       [0.203125  , 0.94921875, 0.21484375],
       [0.1953125 , 0.953125  , 0.23046875],
       [0.18359375, 0.95703125, 0.2421875 ],
       [0.17578125, 0.96484375, 0.25390625],
       [0.16796875, 0.96875   , 0.26953125],
       [0.1640625 , 0.97265625, 0.28515625],
       [0.15625   , 0.9765625 , 0.296875  ],
       [0.1484375 , 0.98046875, 0.3125    ],
       [0.14453125, 0.984375  , 0.328125  ],
       [0.140625  , 0.98828125, 0.34375   ],
       [0.13671875, 0.9921875 , 0.359375  ],
       [0.1328125 , 0.9921875 , 0.375     ],
       [0.1328125 , 0.9921875 , 0.39453125],
       [0.12890625, 0.99609375, 0.41015625],
       [0.12890625, 0.99609375, 0.4296875 ],
       [0.12890625, 0.99609375, 0.4453125 ],
       [0.12890625, 0.99609375, 0.46484375],
       [0.12890625, 0.99609375, 0.48046875],
       [0.1328125 , 0.9921875 , 0.5       ],
       [0.1328125 , 0.9921875 , 0.51953125],
       [0.13671875, 0.98828125, 0.53515625],
       [0.140625  , 0.984375  , 0.5546875 ],
       [0.14453125, 0.98046875, 0.57421875],
       [0.15234375, 0.9765625 , 0.58984375],
       [0.15625   , 0.97265625, 0.609375  ],
       [0.1640625 , 0.96484375, 0.62890625],
       [0.171875  , 0.9609375 , 0.6484375 ],
       [0.1796875 , 0.953125  , 0.6640625 ],
       [0.19140625, 0.9453125 , 0.68359375],
       [0.19921875, 0.9375    , 0.703125  ],
       [0.2109375 , 0.9296875 , 0.71875   ],
       [0.21875   , 0.921875  , 0.73828125],
       [0.23046875, 0.91015625, 0.75390625],
       [0.2421875 , 0.8984375 , 0.76953125],
       [0.2578125 , 0.890625  , 0.7890625 ],
       [0.26953125, 0.87890625, 0.8046875 ],
       [0.28515625, 0.8671875 , 0.8203125 ],
       [0.296875  , 0.8515625 , 0.83203125],
       [0.3125    , 0.83984375, 0.84765625],
       [0.328125  , 0.828125  , 0.86328125],
       [0.34375   , 0.8125    , 0.875     ],
       [0.359375  , 0.796875  , 0.890625  ],
       [0.375     , 0.78515625, 0.90234375],
       [0.390625  , 0.76953125, 0.9140625 ],
       [0.41015625, 0.75390625, 0.92578125],
       [0.42578125, 0.73828125, 0.93359375],
       [0.44140625, 0.72265625, 0.9453125 ],
       [0.4609375 , 0.70703125, 0.953125  ],
       [0.4765625 , 0.6875    , 0.9609375 ],
       [0.49609375, 0.671875  , 0.96875   ],
       [0.51171875, 0.65625   , 0.9765625 ],
       [0.53125   , 0.63671875, 0.98046875],
       [0.546875  , 0.62109375, 0.984375  ],
       [0.5625    , 0.6015625 , 0.98828125],
       [0.58203125, 0.5859375 , 0.9921875 ],
       [0.59765625, 0.56640625, 0.99609375],
       [0.61328125, 0.55078125, 0.99609375],
       [0.62890625, 0.53125   , 0.99609375],
       [0.64453125, 0.515625  , 0.99609375],
       [0.66015625, 0.49609375, 0.99609375],
       [0.67578125, 0.48046875, 0.9921875 ],
       [0.69140625, 0.46484375, 0.98828125],
       [0.70703125, 0.4453125 , 0.984375  ],
       [0.71875   , 0.4296875 , 0.98046875],
       [0.73046875, 0.4140625 , 0.9765625 ],
       [0.74609375, 0.39453125, 0.96875   ],
       [0.7578125 , 0.37890625, 0.9609375 ],
       [0.76953125, 0.36328125, 0.953125  ],
       [0.78125   , 0.34765625, 0.9453125 ],
       [0.7890625 , 0.33203125, 0.93359375],
       [0.80078125, 0.31640625, 0.92578125],
       [0.80859375, 0.30078125, 0.9140625 ],
       [0.81640625, 0.2890625 , 0.90234375],
       [0.82421875, 0.2734375 , 0.890625  ],
       [0.83203125, 0.2578125 , 0.875     ],
       [0.8359375 , 0.24609375, 0.86328125],
       [0.84375   , 0.234375  , 0.84765625],
       [0.84765625, 0.21875   , 0.83203125],
       [0.8515625 , 0.20703125, 0.8203125 ],
       [0.85546875, 0.1953125 , 0.8046875 ],
       [0.859375  , 0.18359375, 0.7890625 ],
       [0.86328125, 0.17578125, 0.76953125],
       [0.8671875 , 0.1640625 , 0.75390625],
       [0.8671875 , 0.15234375, 0.73828125],
       [0.87109375, 0.14453125, 0.71875   ],
       [0.87109375, 0.1328125 , 0.703125  ],
       [0.87109375, 0.125     , 0.68359375],
       [0.87109375, 0.1171875 , 0.6640625 ],
       [0.87109375, 0.109375  , 0.6484375 ],
       [0.87109375, 0.1015625 , 0.62890625],
       [0.87109375, 0.09375   , 0.609375  ],
       [0.8671875 , 0.0859375 , 0.58984375],
       [0.8671875 , 0.078125  , 0.57421875],
       [0.8671875 , 0.07421875, 0.5546875 ],
       [0.86328125, 0.06640625, 0.53515625],
       [0.86328125, 0.0625    , 0.51953125],
       [0.86328125, 0.05859375, 0.5       ],
       [0.859375  , 0.05078125, 0.48046875],
       [0.859375  , 0.046875  , 0.46484375],
       [0.859375  , 0.04296875, 0.4453125 ],
       [0.85546875, 0.0390625 , 0.4296875 ],
       [0.85546875, 0.03515625, 0.41015625],
       [0.85546875, 0.03515625, 0.39453125],
       [0.8515625 , 0.03125   , 0.375     ],
       [0.8515625 , 0.02734375, 0.359375  ],
       [0.8515625 , 0.0234375 , 0.34375   ],
       [0.8515625 , 0.0234375 , 0.328125  ],
       [0.8515625 , 0.01953125, 0.3125    ],
       [0.8515625 , 0.01953125, 0.296875  ],
       [0.8515625 , 0.01953125, 0.28515625],
       [0.8515625 , 0.015625  , 0.26953125],
       [0.85546875, 0.015625  , 0.25390625],
       [0.85546875, 0.015625  , 0.2421875 ],
       [0.85546875, 0.015625  , 0.23046875],
       [0.859375  , 0.015625  , 0.21484375],
       [0.86328125, 0.015625  , 0.203125  ],
       [0.86328125, 0.015625  , 0.19140625],
       [0.8671875 , 0.015625  , 0.1796875 ],
       [0.87109375, 0.015625  , 0.16796875],
       [0.875     , 0.015625  , 0.16015625],
       [0.87890625, 0.015625  , 0.1484375 ],
       [0.8828125 , 0.01953125, 0.140625  ],
       [0.88671875, 0.01953125, 0.12890625],
       [0.890625  , 0.01953125, 0.12109375],
       [0.89453125, 0.0234375 , 0.11328125],
       [0.8984375 , 0.0234375 , 0.10546875],
       [0.90234375, 0.02734375, 0.09765625],
       [0.91015625, 0.02734375, 0.08984375],
       [0.9140625 , 0.03125   , 0.0859375 ],
       [0.91796875, 0.03515625, 0.078125  ],
       [0.921875  , 0.0390625 , 0.0703125 ],
       [0.9296875 , 0.04296875, 0.06640625],
       [0.93359375, 0.04296875, 0.0625    ],
       [0.9375    , 0.046875  , 0.0546875 ],
       [0.94140625, 0.05078125, 0.05078125],
       [0.94921875, 0.05859375, 0.046875  ],
       [0.953125  , 0.0625    , 0.04296875],
       [0.95703125, 0.06640625, 0.0390625 ],
       [0.9609375 , 0.0703125 , 0.03515625],
       [0.96484375, 0.078125  , 0.03125   ],
       [0.96875   , 0.08203125, 0.02734375],
       [0.97265625, 0.08984375, 0.02734375],
       [0.9765625 , 0.09375   , 0.0234375 ],
       [0.98046875, 0.1015625 , 0.01953125],
       [0.98046875, 0.109375  , 0.01953125],
       [0.984375  , 0.11328125, 0.015625  ],
       [0.98828125, 0.12109375, 0.015625  ],
       [0.98828125, 0.12890625, 0.01171875],
       [0.9921875 , 0.13671875, 0.01171875],
       [0.9921875 , 0.14453125, 0.01171875],
       [0.9921875 , 0.15234375, 0.0078125 ],
       [0.99609375, 0.16015625, 0.0078125 ],
       [0.99609375, 0.171875  , 0.0078125 ],
       [0.99609375, 0.1796875 , 0.0078125 ],
       [0.99609375, 0.1875    , 0.00390625],
       [0.99609375, 0.19921875, 0.00390625],
       [0.99609375, 0.20703125, 0.00390625],
       [0.99609375, 0.21875   , 0.00390625],
       [0.99609375, 0.2265625 , 0.00390625],
       [0.9921875 , 0.23828125, 0.00390625],
       [0.9921875 , 0.24609375, 0.00390625],
       [0.9921875 , 0.2578125 , 0.        ],
       [0.98828125, 0.26953125, 0.        ],
       [0.98828125, 0.28125   , 0.        ],
       [0.984375  , 0.2890625 , 0.        ],
       [0.984375  , 0.30078125, 0.        ],
       [0.98046875, 0.3125    , 0.        ],
       [0.98046875, 0.32421875, 0.        ],
       [0.9765625 , 0.33203125, 0.        ],
       [0.9765625 , 0.34375   , 0.        ],
       [0.97265625, 0.35546875, 0.        ],
       [0.97265625, 0.3671875 , 0.        ],
       [0.96875   , 0.37890625, 0.        ],
       [0.96484375, 0.390625  , 0.        ],
       [0.96484375, 0.3984375 , 0.        ],
       [0.9609375 , 0.41015625, 0.        ],
       [0.95703125, 0.421875  , 0.        ],
       [0.95703125, 0.43359375, 0.        ],
       [0.953125  , 0.44140625, 0.        ],
       [0.94921875, 0.453125  , 0.        ],
       [0.94921875, 0.46484375, 0.        ],
       [0.9453125 , 0.47265625, 0.        ],
       [0.94140625, 0.484375  , 0.        ],
       [0.94140625, 0.4921875 , 0.        ],
       [0.9375    , 0.50390625, 0.        ],
       [0.93359375, 0.51171875, 0.        ],
       [0.9296875 , 0.51953125, 0.        ],
       [0.9296875 , 0.53125   , 0.        ],
       [0.92578125, 0.5390625 , 0.        ],
       [0.921875  , 0.546875  , 0.        ],
       [0.91796875, 0.5546875 , 0.        ],
       [0.9140625 , 0.5625    , 0.        ],
       [0.91015625, 0.5703125 , 0.        ],
       [0.91015625, 0.578125  , 0.        ],
       [0.90625   , 0.5859375 , 0.        ],
       [0.90234375, 0.59375   , 0.        ],
       [0.89453125, 0.6015625 , 0.        ],
       [0.890625  , 0.609375  , 0.        ],
       [0.88671875, 0.61328125, 0.        ],
       [0.8828125 , 0.62109375, 0.        ],
       [0.875     , 0.625     , 0.        ],
       [0.87109375, 0.6328125 , 0.        ],
       [0.86328125, 0.63671875, 0.        ],
       [0.859375  , 0.64453125, 0.        ],
       [0.8515625 , 0.6484375 , 0.        ],
       [0.84375   , 0.65625   , 0.        ],
       [0.83984375, 0.66015625, 0.        ],
       [0.83203125, 0.6640625 , 0.        ],
       [0.82421875, 0.671875  , 0.        ],
       [0.8125    , 0.67578125, 0.        ],
       [0.8046875 , 0.6796875 , 0.00390625],
       [0.796875  , 0.68359375, 0.00390625],
       [0.78515625, 0.6875    , 0.00390625],
       [0.77734375, 0.6953125 , 0.00390625],
       [0.765625  , 0.69921875, 0.00390625],
       [0.7578125 , 0.703125  , 0.00390625],
       [0.74609375, 0.70703125, 0.00390625],
       [0.734375  , 0.7109375 , 0.0078125 ],
       [0.72265625, 0.71484375, 0.0078125 ],
       [0.7109375 , 0.72265625, 0.0078125 ],
       [0.69921875, 0.7265625 , 0.0078125 ],
       [0.68359375, 0.73046875, 0.01171875],
       [0.671875  , 0.734375  , 0.01171875],
       [0.66015625, 0.73828125, 0.01171875],
       [0.64453125, 0.74609375, 0.015625  ],
       [0.62890625, 0.75      , 0.015625  ],
       [0.6171875 , 0.75390625, 0.01953125],
       [0.6015625 , 0.76171875, 0.01953125],
       [0.5859375 , 0.765625  , 0.0234375 ],
       [0.57421875, 0.76953125, 0.02734375],
       [0.55859375, 0.77734375, 0.02734375],
       [0.54296875, 0.78125   , 0.03125   ],
       [0.52734375, 0.7890625 , 0.03515625],
       [0.51171875, 0.79296875, 0.0390625 ],
       [0.49609375, 0.80078125, 0.04296875],
       [0.48046875, 0.80859375, 0.046875  ],
       [0.46875   , 0.8125    , 0.05078125],
       [0.453125  , 0.8203125 , 0.0546875 ],
       [0.4375    , 0.828125  , 0.0625    ],
       [0.421875  , 0.83203125, 0.06640625],
       [0.40625   , 0.83984375, 0.0703125 ],
       [0.390625  , 0.84765625, 0.078125  ],
       [0.37890625, 0.85546875, 0.0859375 ],
       [0.36328125, 0.859375  , 0.08984375],
       [0.34765625, 0.8671875 , 0.09765625],
       [0.3359375 , 0.875     , 0.10546875],
       [0.3203125 , 0.8828125 , 0.11328125],
       [0.30859375, 0.88671875, 0.12109375],
       [0.29296875, 0.89453125, 0.12890625]])        
