import osmnx as ox
import networkx as nx
import folium

from osmnx import settings

from geopy.geocoders import Nominatim


class MapWorker:
    def __init__(self, start_location, end_location, region):
        settings.log_console = True
        settings.use_cache = True

        self.locator = Nominatim(user_agent='lol')
        self.start_location = self.calculate_location(start_location)
        self.end_location = self.calculate_location(end_location)
        self.region = region
        self.mode = 'walk'  # 'drive', 'bike', 'walk'
        self.optimizer = 'time'  # 'length', 'time'
        self.graph = self.calculate_graph()

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
        return ox.graph_from_place(self.region, network_type=self.mode)

    def find_nearest_node(self):
        return ox.nearest_nodes(self.graph, *self.start_location[::-1])

    def find_destination_node(self):
        return ox.nearest_nodes(self.graph, *self.end_location[::-1])

    def calculate_shortest_route(self):
        original_node = self.find_nearest_node()
        destination_node = self.find_destination_node()
        # approach: dijkstra, bellman-ford
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

        start_marker = folium.Marker(
            location=self.start_location,
            popup=self.start_location,
            icon=folium.Icon(color='green')
        )
        end_marker = folium.Marker(
            location=self.end_location,
            popup=self.end_location,
            icon=folium.Icon(color='red')
        )
        start_marker.add_to(shortest_route_map)
        end_marker.add_to(shortest_route_map)

        return shortest_route_map

    def calculate_location(self, location):
        location_coordinates = self.locator.geocode(location)
        return location_coordinates.latitude, location_coordinates.longitude


if __name__ == '__main__':
    start_location = 'площадь 1905 года'
    region = 'Екатеринбург'
    end_location = 'Екатеринбургский государственный академический театр оперы и балета'
    mw = MapWorker(start_location, end_location, region)
    plot = mw.get_plot()
    plot.save('map.html')
    plot.show_in_browser()
