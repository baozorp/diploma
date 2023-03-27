import random
import pandas as pd


def start_generators():
    _content_based_generation()
    _collobarative_generation()
    _distances_generation()


def _content_based_generation():
    exhibits = []

    # List of possible values for each field
    types_of_exhibits = ['Wine', 'Barrel', 'Cork', 'Opener', 'Grape Press', 'Fermentation Tank', 'Bottle', 'Vine', 'Wine Glass', 'Wine Bottle Holder']
    types_of_wine = ['Red', 'White', 'Rose', 'Sparkling', 'Dessert', 'Fortified']
    grapes = ['Cabernet Sauvignon', 'Chardonnay', 'Grenache', 'Muscat', 'Tinta Roriz', 'Tempranillo', 'Sauvignon Blanc', 'Riesling', 'Touriga Nacional']
    countries = {
        'France': ['Bordeaux', 'Provence', 'Loire Valley'],
        'United States': ['California'],
        'Greece': ['Samos'],
        'Portugal': ['Douro'],
        'Spain': ['Rioja', 'Rioja'],
        'Germany': ['Mosel']
    }
    years = [str(year) for year in range(1990, 2021)]
    sweets = ['Dry', 'Medium', 'Medium Sweet', 'Sweet', 'Very Sweet']
    materials = ['Oak', 'Cedar', 'Mahogany', 'Natural', 'Synthetic', 'Stainless Steel', 'Aluminum', 'Plastic']
    sizes = ['Small', 'Medium', 'Large']
    types_of_openers = ['Waiter\'s Corkscrew', 'Lever Corkscrew', 'Wing Corkscrew', 'Electric Corkscrew']
    types_of_bottles = ['Bordeaux', 'Burgundy', 'Champagne', 'Sauternes', 'Port']
    types_of_vines = ['Cabernet Franc', 'Cabernet Sauvignon', 'Chardonnay', 'Gewürztraminer', 'Malbec', 'Merlot', 'Pinot Noir', 'Riesling', 'Sangiovese', 'Sauvignon Blanc', 'Syrah', 'Tempranillo']
    types_of_glasses = ['Red Wine Glass', 'White Wine Glass', 'Champagne Flute', 'Stemless Wine Glass']
    types_of_bottle_holders = ['Metal Wine Rack', 'Wooden Wine Rack', 'Wall Mounted Wine Rack']

    # Generate a dictionary for each exhibit
    for i in range(2200):
        exhibit = {}
        exhibit['ID'] = i
        exhibit['Type'] = random.choice(types_of_exhibits)
        exhibit['Country'] = random.choice(list(countries.keys()))
        if exhibit['Type'] == 'Wine':
            exhibit['Wine Type'] = random.choice(types_of_wine)
            exhibit['Grape'] = random.choice(grapes)
            exhibit['Region'] = random.choice(countries[exhibit['Country']])
            exhibit['Sweetness'] = random.choice(sweets)
        elif exhibit['Type'] == 'Barrel':
            exhibit['Material'] = random.choice(materials[:3])
            exhibit['Size'] = random.choice(sizes)
        elif exhibit['Type'] == 'Cork':
            exhibit['Material'] = random.choice(materials[3:5])
            exhibit['Size'] = random.choice(sizes)
        elif exhibit['Type'] == 'Opener':
            exhibit['Material'] = random.choice(materials[5:])
            exhibit['Type of Opener'] = random.choice(types_of_openers)
        elif exhibit['Type'] == 'Grape Press':
            exhibit['Material'] = random.choice(materials[:3])
            exhibit['Size'] = random.choice(sizes)
        elif exhibit['Type'] == 'Fermentation Tank':
            exhibit['Material'] = random.choice(materials[:3])
            exhibit['Size'] = random.choice(sizes)
        elif exhibit['Type'] == 'Bottle':
            exhibit['Type of Bottle'] = random.choice(types_of_bottles)
            exhibit['Country'] = random.choice(list(countries.keys()))
            exhibit['Year'] = random.choice(years)
        elif exhibit['Type'] == 'Vine':
            exhibit['Type of Vine'] = random.choice(types_of_vines)
            exhibit['Country'] = random.choice(list(countries.keys()))
            exhibit['Year'] = random.choice(years)
        elif exhibit['Type'] == 'Wine Glass':
            exhibit['Type of Glass'] = random.choice(types_of_glasses)
            exhibit['Material'] = random.choice(materials[5:])
        elif exhibit['Type'] == 'Wine Bottle Holder':
            exhibit['Type of Bottle Holder'] = random.choice(types_of_bottle_holders)
            exhibit['Material'] = random.choice(materials[:3])
        exhibits.append(exhibit)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(exhibits)

    # Export the DataFrame to a CSV file
    df.to_csv('sources/wine_museum_exhibits.csv', index=False)


# Генерация координат и принадлежности экспонатов
def generate_objects(num_objects, x_range=(0, 25), y_range=(0, 10), room_ids=[]):
    for i in range(num_objects):
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        room_id = random.choice(room_ids) if room_ids else 0
        yield {'name': i, 'x': x, 'y': y, 'room_id': room_id}


def _generate_room_distance_matrix(room_ids):
    matrix = {}
    for i in room_ids:
        matrix[i] = {}
        for j in room_ids:
            distance = abs(i - j)
            matrix[i][j] = distance
    return matrix


def _distances_generation():
    objects = list(generate_objects(2200, room_ids=list(range(1, 10))))
    room_distance_matrix = _generate_room_distance_matrix(list(range(1, 10)))
    # Convert objects list to DataFrame
    objects_df = pd.DataFrame(objects)

    # Save objects to CSV
    objects_df.to_csv('sources/coordinates.csv', index=False)

    # Convert room distance matrix to DataFrame
    room_distance_matrix_df = pd.DataFrame(room_distance_matrix)

    # Save room distance matrix to CSV
    room_distance_matrix_df.to_csv('sources/room_distance_matrix.csv', index=True)


# Генерация пользователей
def _collobarative_generation():
    # Generate sample data
    user_ids = [i for i in range(0, 1001)]
    object_ids = [i for i in range(1, 2200)]
    time_spent = []
    user_id = []
    object_id = []

    # Create a sample dataframe
    for user in user_ids:
        # get unique object for each user
        user_objects = random.sample(object_ids, k=random.randint(1, len(object_ids)))
        for obj in user_objects:
            time_spent.append(random.randint(60, 100))
            user_id.append(user)
            object_id.append(obj)

    data = {'user_id': user_id, 'object_id': object_id, 'time_spent': time_spent}
    df = pd.DataFrame(data)

    # Sort the dataframe by user_id in ascending order
    df = df.sort_values(by=['user_id', 'object_id'])

    # Write data for user 0 to separate csv file
    df_user0 = df[df['user_id'] == 0]
    df_user0.to_csv("sources/current_user.csv", index=False)

    # Write the dataframe to a csv file
    df = df[df['user_id'] != 0]
    df.to_csv("sources/exhibit_data.csv", index=False)
