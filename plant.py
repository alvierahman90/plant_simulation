# Skeleton Program for the AQA A1 Summer 2017 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS1 Programmer Team
# developed in a Python 3 environment

from random import randint, shuffle
import pathlib

SOIL = '.'
SEED = 'S'
PLANT = 'P'
ROCK = 'X'

FIELDLENGTH = 20
FIELDWIDTH = 35

# supports max field width of 52
COLUMN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def GetHowLongToRun():
    print('Welcome to the Plant Growing Simulation')
    print()
    print('You can step through the simulation a year at a time')
    print('or run the simulation for 0 to 5 years')
    print('How many years do you want the simulation to run?')

    while True:
        user_input = input('Enter a number between 0 and 5, or -1 for stepping mode: ')
        for index, char in enumerate(user_input):
            if index == 0 and char == '-':
                continue
            if not char.isdigit():
                break
        else:
            user_input = int(user_input)
            if user_input == -1 or (6 > user_input > 0):
                return user_input

def CreateNewField():
    Field = [[SOIL for Column in range(FIELDWIDTH)] for Row in range(FIELDLENGTH)]
    Row = FIELDLENGTH // 2
    Column = FIELDWIDTH // 2
    Field[Row][Column] = SEED

    rocks_per_mille = ' '
    while True:
        rocks_per_mille = input('How many rocks do you want to add? (per thousand soils) ')
        for char in rocks_per_mille:
            if not char.isdigit():
                break
        else:
            rocks_per_mille = int(rocks_per_mille)
            if 1000 >= rocks_per_mille >= 0:
                break

    soils = []
    for Row in range(FIELDLENGTH):
        for Column in range(FIELDWIDTH):
            if Field[Row][Column] == SOIL:
                soils.append((Row, Column))

    shuffle(soils)
    for row, column in soils:
        if randint(1,1000) <= rocks_per_mille:
            Field[row][column] = ROCK


    return Field

def ReadFile():
    while True:
        FileName = input('Enter file name (without .txt extention): ')
        Field = [[SOIL for Column in range(FIELDWIDTH)] for Row in range(FIELDLENGTH)]
        try:
            FileHandle = open(FileName + '.txt' , 'r')
            for Row in range(FIELDLENGTH):
                FieldRow = FileHandle.readline()
                for Column in range(FIELDWIDTH):
                    Field[Row][Column] = FieldRow[Column]
            FileHandle.close()
            return Field
        except FileNotFoundError:
            continue

def InitialiseField():
    Response = input('Do you want to load a file with seed positions? (Y/N): ')
    if Response == 'Y':
        Field = ReadFile()
    else:
        Field = CreateNewField()
    return Field

def Display(Field, Season, Year):
    print('Season: ', Season, '    Year number: ', Year)
    print(COLUMN_LETTERS[:FIELDWIDTH])
    for Row in range(FIELDLENGTH):
        for Column in range(FIELDWIDTH):
            print(Field[Row][Column], end='')
        print('|{0:>3}'.format(Row))
    print()

def CountPlants(Field):
    NumberOfPlants = 0
    for Row in range(FIELDLENGTH):
        for Column in range(FIELDWIDTH):
            if Field[Row][Column] == PLANT:
                NumberOfPlants += 1
    if NumberOfPlants == 1:
        print('There is 1 plant growing')
    else:
        print('There are', NumberOfPlants, 'plants growing')

def SimulateSpring(Field):
    for Row in range(FIELDLENGTH):
        for Column in range(FIELDWIDTH):
            if Field[Row][Column] == SEED:
                Field[Row][Column] = PLANT
    CountPlants(Field)
    if randint(0, 1) == 1:
        Frost = True
    else:
        Frost = False
    if Frost:
        PlantCount = 0
        for Row in range(FIELDLENGTH):
            for Column in range(FIELDWIDTH):
                if Field[Row][Column] == PLANT:
                    PlantCount += 1
                    if PlantCount % 3 == 0:
                        Field[Row][Column] = SOIL
        print('There has been a frost')
        CountPlants(Field)
    return Field

def SimulateSummer(Field):
    RainFall = randint(0, 2)
    if RainFall == 0:
        PlantCount = 0
        for Row in range(FIELDLENGTH):
            for Column in range(FIELDWIDTH):
                if Field[Row][Column] == PLANT:
                    PlantCount += 1
                    if PlantCount % 2 == 0:
                        Field[Row][Column] = SOIL
        print('There has been a severe drought')
        CountPlants(Field)

    virus = randint(0, 9)
    virus_severity = randint(1, 100)
    plants = []

    if virus == 0:
        PlantCount = 0
        for Row in range(FIELDLENGTH):
            for Column in range(FIELDWIDTH):
                if Field[Row][Column] == PLANT:
                    plants.append((Row, Column))

        shuffle(plants)
        for plant in plants:
            if randint(0, 100) <= virus_severity:
                Field[plant[0]][plant[1]] = SOIL

        print(f'There has been a virus which destroyed {virus_severity}% of your crops')
        CountPlants(Field)


    return Field

def SeedLands(Field, Row, Column):
    """Plants a seed"""

    # No need to verify if seed would land in field, since in real life if the
    # wind blew it out of the field it wouldn't be on the field anyways
    wind = randint(0, 4)
    if wind == 0:   # North
        Row += 1
    elif wind == 1: # East
        Column += 1
    elif wind == 2: # South
        Row -= 1
    elif wind == 3: # West
        Column -= 1

    if Row >= 0 and Row < FIELDLENGTH and Column >= 0 and Column < FIELDWIDTH:
        if Field[Row][Column] == SOIL:
            Field[Row][Column] = SEED
    return Field

def SimulateAutumn(Field):
    for Row in range(FIELDLENGTH):
        for Column in range(FIELDWIDTH):
            if Field[Row][Column] == PLANT:
                Field = SeedLands(Field, Row - 1, Column - 1)
                Field = SeedLands(Field, Row - 1, Column)
                Field = SeedLands(Field, Row - 1, Column + 1)
                Field = SeedLands(Field, Row, Column - 1)
                Field = SeedLands(Field, Row, Column + 1)
                Field = SeedLands(Field, Row + 1, Column - 1)
                Field = SeedLands(Field, Row + 1, Column)
                Field = SeedLands(Field, Row + 1, Column + 1)
    return Field

def SimulateWinter(Field):
    for Row in range(FIELDLENGTH):
        for Column in range(FIELDWIDTH):
            if Field[Row][Column] == PLANT:
                Field[Row][Column] = SOIL
    return Field

def SimulateOneYear(Field, Year):
    Field = SimulateSpring(Field)
    Display(Field, 'spring', Year)
    Field = SimulateSummer(Field)
    Display(Field, 'summer', Year)
    Field = SimulateAutumn(Field)
    Display(Field, 'autumn', Year)
    Field = SimulateWinter(Field)
    Display(Field, 'winter', Year)

def Simulation():
    YearsToRun = GetHowLongToRun()

    if YearsToRun != 0:
        Field = InitialiseField()
        if YearsToRun >= 1:
            for Year in range(1, YearsToRun + 1):
                SimulateOneYear(Field, Year)
        else:
            Continuing = True
            Year = 0
            while Continuing:
                Year += 1
                SimulateOneYear(Field, Year)
                Response = input('Press Enter to run simulation for another Year, Input X to stop: ')
                if Response == 'x' or Response == 'X':
                    Continuing = False
        print('End of Simulation')

    save_field = get_yes_no_answer('Save output field?')

    if save_field:
        filepath = pathlib.Path('/')
        while filepath.exists():
            filename = input('Enter file name to save to: ')
            filepath = pathlib.Path(filename)
        with open(filename, 'a') as f:
            write_field_to_file(Field, f)

def get_yes_no_answer(prompt):
    answer = 'ahhhhhhhhhh'
    while answer not in [True, False]:
        answer = input(prompt + '(y/n) ').lower()
        if answer in ['y', 'yes', 'yeet']:
            answer = True
        elif answer in ['n', 'no', 'nah bruv']:
            answer = False

    return answer

def write_field_to_file(field, file):
    for row in range(FIELDLENGTH):
        for column in range(FIELDWIDTH):
            f.write(field[row][column])


if __name__ == "__main__":
    Simulation()
