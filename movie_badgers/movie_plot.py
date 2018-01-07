import pandas as pd
import numpy as np
from datetime import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d
from bokeh.palettes import Spectral11


def scatter_plot(path, x, y):
    '''Draw a scatter plot for two continuous variables in the movie data'''
    df = pd.read_csv(path + "/data_for_lr.csv")
    output_file("scatter_%s_%s.html" % (y, x))
    xx = df[y]
    yy = df[x]
    # Adjust y range to have a more elegant layout
    y_max = max(yy)
    x_max = max(xx)
    p = figure(title="%s against %s" % (y, x),
               x_range=Range1d(0, x_max * 1.5),
               y_range=Range1d(0, y_max * 1.5))
    p.yaxis.axis_label = y
    p.xaxis.axis_label = x
    p.scatter(xx, yy)
    show(p)


def box_plot(path, x):
    '''Draw a boxplot plot revenue versus categorical in the movie data'''
    df = pd.read_csv(path + "/data_for_lr.csv")
    # find the quartiles and IQR for each category
    groups = df.groupby(x)
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr
    xx = df[x]
    # find the outliers for each category

    def outliers(group):
        cat = group.name
        return group[(group.revenue > upper.loc[cat]['revenue']) |
                     (group.revenue < lower.loc[cat]['revenue'])]['revenue']
    out = groups.apply(outliers).dropna()
    # prepare outlier data for plotting, we need coordinates for every outlier.
    cats = df[x].unique()
    if not out.empty:
        outx = []
        outy = []
        for cat in cats:
            # only add outliers if they exist
            if not out.loc[cat].empty:
                for value in out[cat]:
                    outx.append(cat)
                    outy.append(value)
    cats1 = [-1, 2]
    p = figure(tools="save", background_fill_color="#EFE8E2", title="",
               x_range=cats1)

    # if no outliers, shrink lengths of stems to be no longer than the minimums
    # or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.revenue = [min([x, y]) for (x, y) in
                     zip(list(qmax.loc[:, 'revenue']), upper.revenue)]
    lower.revenue = [max([x, y]) for (x, y) in
                     zip(list(qmin.loc[:, 'revenue']), lower.revenue)]

    # stems
    p.segment(cats, upper.revenue, cats, q3.revenue, line_color="black")
    p.segment(cats, lower.revenue, cats, q1.revenue, line_color="black")

    # boxes
    p.vbar(cats, 0.7, q2.revenue, q3.revenue, fill_color="#E08E79",
           line_color="black")
    p.vbar(cats, 0.7, q1.revenue, q2.revenue, fill_color="#3B8686",
           line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    p.rect(cats, lower.revenue, 0.2, 0.01, line_color="black")
    p.rect(cats, upper.revenue, 0.2, 0.01, line_color="black")

    # outliers
    if not out.empty:
        p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size = "12pt"

    output_file("boxplot_revenue_%s.html" % x,
                title="Boxplot of Revenue by %s" % x)

    show(p)
