import networkx as nx
import numpy as np
from bokeh.io import output_file, save
from bokeh.models import (BoxSelectTool, Circle, MultiLine, NodesAndLinkedEdges, TapTool,
                          ColorBar, LogColorMapper, LogTicker, OpenURL, Range1d)
from bokeh.models.tools import HoverTool, WheelZoomTool, PanTool
from bokeh.palettes import Spectral4
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.transform import log_cmap


async def networkx_nodes(df_forward_channels):  # Current channel graph tree
    df_forward_channels['sizes'] = np.log(
        df_forward_channels['channel_forward_members'].astype('float64') + 5)  # Sizes generation
    G = nx.Graph()
    for i, channel in enumerate(df_forward_channels['channel_forward_id']):
        try:
            G.add_node(
                channel, **df_forward_channels[df_forward_channels['channel_forward_id'] == channel].T.to_dict()[i]
            )
        except KeyError:
            continue
    for i, channel in enumerate(list(G.nodes())):
        if i != 0:
            G.add_edge(list(G.nodes())[0], channel)
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos)

    return G


def graph_export(G):
    for start_node, end_node, _ in G.edges(data=True):  # New size generator
        G.nodes[start_node]['sizes'] = np.log10(G.nodes[start_node]['channel_forward_members'] + 1000)

    output_file(filename="index.html", title="Telegram Network")
    tooltips = [
        ('Title', '@channel_forward_title'),
        ('Link', 't.me/' + '@channel_forward_link')
    ]
    plot = figure(
        # sizing_mode='scale_height',
        x_range=Range1d(-1.05, 1.05),
        y_range=Range1d(-1.05, 1.05),
        tools=[HoverTool(tooltips=tooltips)])
    plot.sizing_mode = 'scale_both'
    plot.grid.visible = True
    plot.xaxis.visible = False
    plot.yaxis.visible = False

    color_transformer = LogColorMapper(palette='Magma256', low=1, high=10 ** 7)
    color_bar = ColorBar(color_mapper=color_transformer,
                         orientation='vertical',
                         label_standoff=10,
                         width=8,
                         ticker=LogTicker()
                         )

    plot.title.text = "Telegram Network Map"
    plot.add_tools(
        TapTool(),
        BoxSelectTool(),
        WheelZoomTool(),
        PanTool(),
    )
    plot.toolbar.active_scroll = "auto"
    graph_renderer = from_networkx(G, nx.spring_layout, center=(0, 0))

    graph_renderer.node_renderer.glyph = Circle(
        size='sizes',
        fill_color=log_cmap('sizes', 'Magma256', 3, np.log(10 ** 7)),
        hit_dilation=1
    )
    graph_renderer.node_renderer.selection_glyph = Circle(
        size='sizes',
        fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(
        size='sizes',
        fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(
        line_join='miter',
        line_color="#CCCCCC",
        line_alpha=0.98,
        line_width=0.5, )
    graph_renderer.edge_renderer.selection_glyph = MultiLine(
        line_color=Spectral4[2],
        line_width=2)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(
        line_color=Spectral4[1],
        line_width=2)

    url = 'tg://resolve?domain=' + '@channel_forward_link'
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    graph_renderer.inspection_policy = NodesAndLinkedEdges()
    graph_renderer.selection_policy = NodesAndLinkedEdges()
    plot.add_layout(color_bar, 'right')
    plot.renderers.append(graph_renderer)

    save(plot)
    # show(plot)    # Script can open the map in browser after each channel

    return G
