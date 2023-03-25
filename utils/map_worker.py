import osmnx as ox
import networkx as nx
import folium


class MapWorker:
    def __init__(self, start_location, end_location, region):
        ox.config(log_console=True, use_cache=True)
        self.start_location = start_location
        self.end_location = end_location
        self.region = region
        self.mode = 'walk'  # 'drive', 'bike', 'walk'
        self.optimizer = 'time'  # 'length', 'time'
        self.graph = None

    def set_start_location(self, new_location):
        self.start_location = new_location

    def set_end_location(self, new_location):
        self.end_location = new_location

    def set_mode(self, new_mode):
        self.mode = new_mode

    def set_optimizer(self, new_optimizer):
        self.optimizer = new_optimizer

    def set_region(self, new_region):
        self.region = new_region

    def calculate_graph(self):
        self.graph = ox.graph_from_place(self.region, network_type=self.mode)

    def find_nearest_node(self):
        if self.graph is None:
            self.calculate_graph()
        return ox.nearest_nodes(self.graph, *self.start_location[::-1])

    def find_destination_node(self):
        if self.graph is None:
            self.calculate_graph()
        return ox.nearest_nodes(self.graph, *self.end_location[::-1])

    def calculate_shortest_route(self):
        if self.graph is None:
            self.calculate_graph()
        original_node = self.find_nearest_node()
        destination_node = self.find_destination_node()
        print(original_node, destination_node)

        # method: dijkstra, bellman-ford
        return nx.shortest_path(self.graph, original_node, destination_node, weight=self.optimizer)

    def get_plot(self):
        shortest_route = self.calculate_shortest_route()
        shortest_route_map = ox.plot_route_folium(self.graph, shortest_route, tiles='openstreetmap')

        folium.TileLayer('openstreetmap').add_to(shortest_route_map)
        folium.TileLayer('Stamen Terrain').add_to(shortest_route_map)
        folium.TileLayer('Stamen Toner').add_to(shortest_route_map)
        folium.TileLayer('Stamen Water Color').add_to(shortest_route_map)
        folium.TileLayer('cartodbpositron').add_to(shortest_route_map)
        folium.TileLayer('cartodbdark_matter').add_to(shortest_route_map)
        folium.LayerControl().add_to(shortest_route_map)
        return shortest_route_map


if __name__ == '__main__':
    start_location = (56.848114, 60.600726)
    end_location = (57.001182, 60.520375)
    region = 'Екатеринбург'
    mw = MapWorker(start_location, end_location, region)
    plot = mw.get_plot()
    plot.save('map.html')
    plot.show_in_browser()
