import tournament, menu
import os

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

for p in tour.wall:
    print(p)
