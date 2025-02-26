# Mapping of CCTV number to its location in the mall
cctv_locations = {
    "1": "Level 1 (East Wing): Main east entrance, adjacent to 'Urban Fashions' and the glass atrium",
    "2": "Level 1 (West Wing): Main west entrance, next to 'Home Essentials' department store",
    "3": "Level 1 (East Wing): Central corridor area with 'Tech World' on one side",
    "4": "Level 1 (West Wing): Central corridor area, beside the 'Grand Bookstore' and directory board",
    "5": "Level 1 (East Wing): Near the escalator to Level 2, by 'Coffee Bean' cafe and 'Cosmetics Corner'",
    "6": "Level 1 (West Wing): Near the escalator to Level 2, by 'Sporting Goods Outlet'",
    "7": "Level 2 (East Wing): East wing atrium between 'Boutique Jewelers' and 'Fashion Forward'",
    "8": "Level 2 (West Wing): West wing atrium, adjacent to 'Luxury Watches'",
    "9": "Level 2 (East Wing): North corridor with 'Gourmet Delights' restaurant",
    "10": "Level 2 (West Wing): South corridor near 'Cosmetic Emporium' and 'Accessory Hub'",
    "11": "Level 2 (East Wing): Secondary corridor area near the 'Modern Furniture' showroom",
    "12": "Level 2 (West Wing): Secondary corridor area, adjacent to 'Electronic Superstore'",
    "13": "Level 3 (East Wing): East wing lounge near the 'Artisan Crafts' gallery",
    "14": "Level 3 (West Wing): West wing seating area beside the 'Vintage Record' store",
    "15": "Level 3 (East Wing): Eastern end of the east wing, near the 'Specialty Bookstore' and 'Café Literati'",
    "16": "Level 3 (West Wing): Western end of the west wing, close to 'Designer Home Decor'",
    "17": "Level 3 (East Wing): Central staircase area, adjacent to the 'Fine Jewelry' outlet",
    "18": "Level 3 (West Wing): Central staircase area, with 'Electronics Gallery' nearby",
    "19": "Level 3 (East Wing): Along the east wing passage near 'Boutique Shoes'",
    "20": "Level 3 (West Wing): Along the west wing passage near 'Watch Gallery' and 'Accessory Loft'"
}


manpower_available = """
    There are 5 security guards and 1 security manager on duty today.
    Ther 5 security guards are John Tan, Mary Lim, Ali Hassan, Sarah Lee, and Peter Wong.
    The security manager is Rajesh Kumar.
    The 5 security guards are all trained in fire safety and evacuation procedures.
    John Tan is stationed at the east entrance on the first floor.
    Mary Lim is stationed at the west entrance on the first floor.
    Ali Hassan is patrolling the east wing on the second floor.
    Sarah Lee is patrolling the west wing on the second floor.
    Peter Wong is patrolling the third floor.
    Rajesh Kumar is stationed at the security office on the third floor.
"""

layout_of_mall = "The mall has 3 levels, split into the east and west wings, with only 2 entrances on the first floor."


fire_alarm_stations = """
    Here are the locations of the fire alarm stations:
    1: Level 1 (East Wing): Near the main east entrance, adjacent to 'Urban Fashions'
    2: Level 1 (West Wing): Near the main west entrance, next to 'Home Essentials'
    3: Level 2 (East Wing): In the central atrium between 'Boutique Jewelers' and 'Fashion Forward'
    4: Level 2 (West Wing): In the central atrium, adjacent to 'Luxury Watches'
    5: Level 2 (East Wing): Along the north corridor near 'Gourmet Delights'
    6: Level 2 (West Wing): Along the south corridor close to 'Cosmetic Emporium'
    7: Level 3 (East Wing): On the east wing passage near 'Specialty Bookstore' and 'Café Literati'
    8: Level 3 (West Wing): On the west wing passage adjacent to 'Designer Home Decor'
"""

with open("fire_management_SOP.txt", "r", encoding="utf-8") as f:
    fire_management_SOP = f.read()