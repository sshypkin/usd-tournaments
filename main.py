import tournament
import menu
import os
import pickle

tour = None

data_files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.dat')]
if data_files:
    print("Data files were found in the directory:")
    for file in data_files:
        print(f"{data_files.index(file) + 1}. {file}")
    print('-' * 5)
    choice = int(input("Please enter a file number to open or '0' for a new tournament: "))

    if choice:
        if choice <= len(data_files):
            data_file = data_files[choice - 1]
            with open(data_file, 'rb') as file:
                tour = pickle.load(file)
                print(f"Load tournament from file {data_file}")
        else:
            print(f"Wrong file number '{choice}'")

if not tour:
    print("Create a new tournament")
    tour = tournament.Tournament()


while True:
    os.system('clear')
    action = input(menu.main)
    if action == '0':
        break
    elif action == '1':
        menu.tournament(tour)
    elif action == '2':
        menu.players(tour)

data_file = f"tournament.dat"
with open(data_file, 'wb') as file:
    pickle.dump(tour, file)
    print(f"Saved the tournament data to {data_file}")
