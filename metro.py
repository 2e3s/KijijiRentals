from typing import Tuple, List
from geopy.distance import geodesic


NO_ELEVATOR = 0
PARTIAL_ELEVATOR = 1
FULL_ELEVATOR = 2


class Metro:
    _stations: List[Tuple[float, float, str, int, int]] = [
        # Orange line
        (45.5561, -73.6673, 'Henri-Bourassa', 6, FULL_ELEVATOR),
        (45.5506, -73.6560, 'Sauve', 7, NO_ELEVATOR),
        (45.5457, -73.6381, 'Cremazie', 7, NO_ELEVATOR),
        (45.5432, -73.6284, 'Jarry', 10, NO_ELEVATOR),
        (45.5396, -73.6136, 'Jean-Talon', 10, FULL_ELEVATOR),
        (45.5355, -73.6045, 'Beaubien', 10, NO_ELEVATOR),
        (45.5312, -73.5978, 'Rosemont', 10, FULL_ELEVATOR),
        (45.5278, -73.5890, 'Laurier', 10, NO_ELEVATOR),
        (45.5245, -73.5817, 'Mont-Royal', 10, PARTIAL_ELEVATOR),
        (45.5182, -73.5683, 'Sherbrooke', 10, NO_ELEVATOR),
        (45.5155, -73.5604, 'Berri-UQAM', 10, FULL_ELEVATOR),
        (45.5102, -73.5566, 'Champ-de-Mars', 8, FULL_ELEVATOR),
        (45.50509, -73.55972, 'Place-d\'Armes', 8, FULL_ELEVATOR),
        (45.50194, -73.56306, 'Square-Victoria–OACI', 7, NO_ELEVATOR),
        (45.4980, -73.5668, 'Bonaventure', 7, FULL_ELEVATOR),
        (45.4950, -73.5709, 'Lucien L\'Allier', 8, NO_ELEVATOR),
        (45.4889, -73.5765, 'Georges-Vanier', 9, NO_ELEVATOR),
        (45.4771, -73.5865, 'Place Saint-Henri', 10, PARTIAL_ELEVATOR),
        (45.473889, -73.603889, 'Vendome', 10, FULL_ELEVATOR),
        (45.4796, -73.6198, 'Villa-Maria', 10, PARTIAL_ELEVATOR),
        (45.4855, -73.6280, 'Snowdon', 3, FULL_ELEVATOR),
        (45.4924, -73.6327, 'Cote-Sainte-Catherine', 2, NO_ELEVATOR),
        (45.4943, -73.6380, 'Plamondon', 1, NO_ELEVATOR),
        (45.4950, -73.6530, 'Metro Namur', 0, NO_ELEVATOR),
        (45.5003, -73.6615, 'De la Savaine', 0, NO_ELEVATOR),
        (45.5094, -73.6747, 'Du College', 0, FULL_ELEVATOR),
        (45.5142, -73.6832, 'Cote-Vertu', 1, FULL_ELEVATOR),
        # Blue line
        (45.4963, -73.6226, 'Cote-des-Neiges', 3, NO_ELEVATOR),
        (45.5027, -73.6183, 'Station Universite-de-Montreal', 4, NO_ELEVATOR),
        (45.5101, -73.6125, 'Edouard-Montpetit', 4, PARTIAL_ELEVATOR),
        (45.5203, -73.615, 'Outremont', 10, PARTIAL_ELEVATOR),
        (45.5303, -73.624, 'Parc extension', 0, NO_ELEVATOR),
        (45.5353, -73.620, 'De Castelnau', 3, NO_ELEVATOR),
        (45.5465, -73.6081, 'Fabre', 5, NO_ELEVATOR),
        (45.5538, -73.6021, 'D\'Iberville', 3, PARTIAL_ELEVATOR),
        (45.55972, -73.60000, 'St-Michel', 2, NO_ELEVATOR),
        # Green line
        (45.4462, -73.6037, 'Terminus Angrignon', 8, PARTIAL_ELEVATOR),
        (45.4509, -73.5934, 'Monk', 9, NO_ELEVATOR),
        (45.4568, -73.5820, 'Jolicoeur', 9, PARTIAL_ELEVATOR),
        (45.4592, -73.5715, 'Verdun', 9, NO_ELEVATOR),
        (45.4618, -73.5665, 'De l\'Eglise', 9, NO_ELEVATOR),
        (45.4708, -73.5661, 'Station Lasalle', 8, NO_ELEVATOR),
        (45.4782, -73.5693, 'Charlevoix', 7, NO_ELEVATOR),
        (45.4828, -73.5797, 'Lionel Groulx', 10, FULL_ELEVATOR),
        (45.4893, -73.5841, 'Atwater', 7, PARTIAL_ELEVATOR),
        (45.4945, -73.5808, 'Guy-Concordia', 6, NO_ELEVATOR),
        (45.5009, -73.5747, 'Peel', 6, NO_ELEVATOR),
        (45.5039, -73.5714, 'McGill ', 6, PARTIAL_ELEVATOR),
        (45.5081, -73.5686, 'Place-des-Arts', 6, PARTIAL_ELEVATOR),
        (45.5108, -73.5648, 'Saint-Laurent', 6, NO_ELEVATOR),
        (45.5190, -73.5559, 'Beaudry', 9, NO_ELEVATOR),
        (45.5237, -73.5521, 'Papineau', 10, NO_ELEVATOR),
        (45.5335, -73.5522, 'Frontenac', 10, NO_ELEVATOR),
        (45.5415, -73.5543, 'Prefontaine', 10, PARTIAL_ELEVATOR),
        (45.5470, -73.5515, 'Station Joliette', 10, NO_ELEVATOR),
        (45.5540, -73.5519, 'Pie-IX', 9, PARTIAL_ELEVATOR),
        (45.5612, -73.5472, 'Viau', 8, FULL_ELEVATOR),
        (45.5692, -73.5469, 'Assomption', 7, NO_ELEVATOR),
        (45.5769, -73.5467, 'Cadillac', 5, NO_ELEVATOR),
        (45.5828, -73.5431, 'Langelier', 3, NO_ELEVATOR),
        (45.5889, -73.5394, 'Radisson', 2, NO_ELEVATOR),
        (45.5967, -73.5356, 'Honoré-Beaugrand', 1, FULL_ELEVATOR),
        # Yellow
        (45.5253, -73.5219, 'Longueuil', 6, NO_ELEVATOR),
    ]

    def __init__(self, index: int, original_point: Tuple[float, float]) -> None:
        self.original_point = original_point
        station = Metro._stations[index]

        self.point = (station[0], station[1])
        self.name = station[2]
        multiplier = 1.0
        if station[4] == NO_ELEVATOR:
            multiplier = 0.8
        elif station[4] == PARTIAL_ELEVATOR:
            multiplier = 0.95

        self.score = int(station[3] * multiplier * 10)
        self.index = index

    def distance_to(self, point: Tuple[float, float]) -> int:
        return int(geodesic(self.point, point).meters)

    def distance(self) -> int:
        return int(geodesic(self.point, self.original_point).meters)

    @staticmethod
    def get_closest(point: Tuple[float, float]) -> 'Metro':
        min_distance = 0xFFFFFFFF
        min_index = 0
        for i in range(len(Metro._stations)):
            (latitude, longitude, _, _, _) = Metro._stations[i]
            distance = geodesic((latitude, longitude), point).meters
            if distance < min_distance:
                min_index = i
                min_distance = distance

        return Metro(min_index, point)
