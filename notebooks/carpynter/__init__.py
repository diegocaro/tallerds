from matplotlib.collections import PatchCollection
from matplotlib.colors import from_levels_and_colors
from matplotlib.patches import Polygon, Patch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from .smopy import Map as SmopyMap

def feature_to_patch(s, smopy_map):
    s_arr = np.array(s.exterior.xy).T
    s_pos = np.array(smopy_map.to_pixels(s_arr[:,1], s_arr[:,0])).T
    return Polygon(s_pos, closed=False)

def choropleth(geodf, figsize=12, column=None, scheme='fisher_jenks', 
                   n_colors=5, palette='viridis', alpha=0.75, cbar_orientation='vertical'):
        
    bounds = geodf.total_bounds
    bbox = (bounds[1], bounds[0], bounds[3], bounds[2])
    smopy_map = SmopyMap(bbox, z=12, margin=0)

    fig_shape = smopy_map.to_numpy().shape
    aspect = fig_shape[0] / fig_shape[1]

    fig = plt.figure(figsize=(figsize, figsize / aspect))
    plt.imshow(smopy_map.img)
    ax = plt.gca()
    plt.axis('off')
    
    choro = []
    patch_values = []
    
    if scheme != 'categorical':
        
        for idx, row in geodf.iterrows():
            feature = row.geometry
            value = row[column]
            
            if feature.geom_type == 'Polygon':
                choro.append(feature_to_patch(feature, smopy_map))
                patch_values.append(value)
            elif feature.geom_type == 'MultiPolygon':
                for subfeature in feature:
                    choro.append(feature_to_patch(subfeature, smopy_map))
                    patch_values.append(value)
            else:
                continue
        
        binning = gpd.plotting.__pysal_choro(geodf[column], scheme='fisher_jenks', k=n_colors)
        bins = np.insert(binning.bins, 0, geodf[column].min())
        palette_values = sns.color_palette(palette, n_colors=n_colors)
        cmap, norm = from_levels_and_colors(bins, palette_values, extend='neither')
        cmap.set_over(palette_values[-1], alpha=alpha)

        collection = PatchCollection(choro, alpha=alpha, cmap=cmap, norm=norm)    
        collection.set_array(np.array(patch_values))

        
        
        if cbar_orientation is not None:
            plt.colorbar(collection, shrink=0.5, orientation='vertical', label=column, 
                     fraction=0.05, pad=0.01)
    else:
        category_values = sorted(geodf[column].unique())
        n_colors = len(category_values)
        palette = sns.color_palette(palette, n_colors=n_colors)
        color_dict = dict(zip(category_values, palette))
        
        
        for idx, row in geodf.iterrows():
            feature = row.geometry
            value = row[column]
            
            if feature.geom_type == 'Polygon':
                choro.append(feature_to_patch(feature, smopy_map))
                patch_values.append(color_dict[value])
            elif feature.geom_type == 'MultiPolygon':
                for subfeature in feature:
                    choro.append(feature_to_patch(subfeature, smopy_map))
                    patch_values.append(color_dict[value])
            else:
                continue

        collection = PatchCollection(choro, alpha=alpha, color=patch_values)   
        
        bbox_to_anchor = None#(0.99, 0.75)
        legend_parts = [Patch(color=color, label=label) for label, color in zip(category_values, palette)]
        plt.legend(legend_parts, [p.get_label() for p in legend_parts], bbox_to_anchor=bbox_to_anchor)
        
    ax.add_collection(collection)
    plt.tight_layout()
    
    return ax
    

