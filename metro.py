from geopy.distance import vincenty


class Metro:
    stations = [
        # Orange line
        [45.5561, -73.6673, 'Henri-Bourassa', 70],
        [45.5506, -73.6560, 'Sauve', 80],
        [45.5457, -73.6381, 'Cremazie', 70],
        [45.5432, -73.6284, 'Jarry', 70],
        [45.5396, -73.6136, 'Jean-Talon', 70],
        [45.5355, -73.6045, 'Beaubien', 70],
        [45.5312, -73.5978, 'Rosemont', 90],
        [45.5278, -73.5890, 'Laurier', 100],
        [45.5245, -73.5817, 'Mont-Royal', 100],
        [45.5182, -73.5683, 'Sherbrooke', 100],
        [45.5155, -73.5604, 'Berri-UQAM', 100],
        [45.5102, -73.5566, 'Champ-de-Mars', 90],
        [45.50509, -73.55972, 'Place-d\'Armes', 80],
        [45.50194, -73.56306, 'Square-Victoria–OACI', 80],
        [45.4980, -73.5668, 'Bonaventure', 70],
        [45.4950, -73.5709, 'Lucien L\'Allier', 80],
        [45.4889, -73.5765, 'Georges-Vanier', 90],
        [45.4771, -73.5865, 'Place Saint-Henri', 100],
        [45.473889, -73.603889, 'Vendome', 100],
        [45.4796, -73.6198, 'Villa-Maria', 80],
        [45.4855, -73.6280, 'Snowdon', 50],
        [45.4924, -73.6327, 'Cote-Sainte-Catherine', 50],
        [45.4943, -73.6380, 'Plamondon', 50],
        [45.4950, -73.6530, 'Metro Namur', 40],
        [45.5003, -73.6615, 'De la Savaine', 40],
        [45.5094, -73.6747, 'Du College', 40],
        [45.5142, -73.6832, 'Cote-Vertu', 30],
        # Blue line
        [45.4963, -73.6226, 'Cote-des-Neiges', 30],
        [45.5027, -73.6183, 'Station Universite-de-Montreal', 50],
        [45.5101, -73.6125, 'Edouard-Montpetit', 70],
        [45.520278, -73.615, 'Outremont', 80],
        # [Parc extension],  #
        [45.5465, -73.6081, 'Fabre', 60],
        [45.5538, -73.6021, 'D\'Iberville', 40],
        # [45.55972, -73.60000, 'St-Michel', 60],
        # Green line
        # [45.4462, -73.6037, 'Terminus Angrignon', 20],
        # [45.4509, -73.5934, 'Monk', 30],
        # [45.4568, -73.5820, 'Jolicoeur', 40],
        # [45.4592, -73.5715, 'Verdun', 40],
        # [45.4618, -73.5665, 'De l\'Eglise', 40],
        [45.4708, -73.5661, 'Station Lasalle', 40],
        [45.4782, -73.5693, 'Charlevoix', 80],
        [45.4828, -73.5797, 'Lionel Groulx', 100],
        [45.4893, -73.5841, 'Atwater', 100],
        [45.4945, -73.5808, 'Guy-Concordia', 100],
        [45.5009, -73.5747, 'Peel', 90],
        [45.5039, -73.5714, 'McGill ', 80],
        [45.5108, -73.5648, 'Saint-Laurent', 90],
        # [Berri UQAM],  #
        [45.5190, -73.5559, 'Beaudry', 70],
        [45.5237, -73.5521, 'Papineau', 30],
        # [45.5335, -73.5522, 'Frontenac', 60],
        # [45.5415, -73.5543, 'Prefontaine', 50],
        # [45.5470, -73.5515, 'Station Joliette', 10],
        # [45.5540, -73.5519, 'Pie-IX'],
        # [45.5612, -73.5472, 'Viau'],
        # [],  # Station Assomption
        # [],  # Cadillac
        # [],  # Langelier
        # [],  # Radisson
        # [],  # Station Honoré-Beaugrand
    ]

    @staticmethod
    def get_distance(metro_index: int, point):
        metro = Metro.stations[metro_index]
        return vincenty((metro[0], metro[1]), point).meters
