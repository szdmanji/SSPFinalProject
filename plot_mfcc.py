import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import numpy as np

sober_data_path = r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\mfcc_data_drunk.csv"
drunk_data_path = r"C:\Users\iannb\OneDrive\Documents\BC Senior Year_\Speech Sig\SSPFinalProject\mfcc_data_sober.csv"

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta



def t_plot():
    sober_df = pd.read_csv(sober_data_path)
    del sober_df['filename']
    del sober_df['label']

    drunk_df = pd.read_csv(drunk_data_path)
    del drunk_df['filename']
    del drunk_df['label']

    npdata_sober = sober_df.to_numpy()
    npdata_drunk = drunk_df.to_numpy()
    # drunk_df.drop(drunk_df.index[0])
    # drunk_df.drop(drunk_df.columns[1], axis=1)
    # print(drunk_df)
    # print(npdata)
    # del drunk_df['filename']



    # sober plot
    pd.DataFrame(npdata_sober).T.plot()
    plt.show()

    pd.DataFrame(npdata_drunk).T.plot()
    plt.show()

    # drunk plot
    # drunk_df.T.plot()
    # plt.show()

def rador_plot():
    headers = ['chroma_stft','rms','spectral_centroid','spectral_bandwidth','rolloff','zero_crossing_rate','onset_strength','mfcc1','mfcc2','mfcc3','mfcc4','mfcc5','mfcc6','mfcc7','mfcc8','mfcc9','mfcc10','mfcc11','mfcc12','mfcc13','mfcc14','mfcc15','mfcc16','mfcc17','mfcc18','mfcc19','mfcc20']
    N = len(headers)
    theta = radar_factory(N, frame='polygon')
    sober_df = pd.read_csv(sober_data_path)
    del sober_df['filename']
    del sober_df['label']

    drunk_df = pd.read_csv(drunk_data_path)
    del drunk_df['filename']
    del drunk_df['label']

    npdata_sober = sober_df.to_numpy()
    npdata_drunk = drunk_df.to_numpy()

    spoke_labels = headers

    fig, axes = plt.subplots(figsize=(9, 9), nrows=2, ncols=2,
                             subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    colors = ['b', 'r', 'g', 'm', 'y']


t_plot()
