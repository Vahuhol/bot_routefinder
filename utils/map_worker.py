import osmnx as ox
import networkx as nx
import folium

from osmnx import settings

from geopy.geocoders import Nominatim

import io
from PIL import Image


class MapWorker:
    def __init__(self, start_location: dict, end_location: str, region: str = 'Екатеринбург'):
        settings.log_console = True
        settings.use_cache = True
        self.region = region
        self.locator = Nominatim(user_agent='lol')
        self.start_location = start_location['latitude'], start_location['longitude']
        self.end_location = self.calculate_location(end_location)
        self.mode = 'walk'  # 'drive', 'bike', 'walk'
        self.optimizer = 'time'  # 'length', 'time'
        self.graph = self.calculate_graph()

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
        location_coordinates = self.locator.geocode(f'{self.region} {location}')
        return location_coordinates.latitude, location_coordinates.longitude

    @staticmethod
    def save_plot_as_image(plot: folium.Map, path: str = 'res') -> Image:
        img_data = plot._to_png(5)
        img = Image.open(io.BytesIO(img_data))
        img.save(f'{path}/map.png')
        return img


if __name__ == '__main__':
    start_location = {"latitude": 56.894878, "longitude": 60.587989}
    region = 'Екатеринбург'
    end_location = f'{region} 40-летия Октября, 75'
    mw = MapWorker(start_location, end_location, region)
    print(mw.calculate_location(end_location))
    plot = mw.get_plot()
    mw.save_plot_as_image(plot, path='')
    plot.show_in_browser()
