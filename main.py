import sys
import pytest


import project.database as database
import project.game as game
import project.objects as obj


def buyTruck():
    g = game.GameState()
    p = g.player
    if p.balance >= 1000:
        p.makePurchase(1000)
        g.trucks.addTruck(f"Truck {g.trucks.truckCount + 1}")
    else:
        print("Insufficient Balance")

def viewTrucks():
    print("TRUCKS:")
    print("     1. List Trucks")
    print("     2. Add Trucks")
    print("     3. Return to Menu")

    G = game.GameState()
    t = G.trucks

    while True:
        try:
            i = int(input("Enter command (1-3): "))
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")
            continue

        match i:
            case 1:
                t.printTrucks()
            case 2:
                buyTruck()
                print()
            case 3:
                break


def printCommands1():
    print("COMMANDS:")
    print("     1. View Orders")
    print("     2. View Trucks")

    print("     7. View Player")
    print("     8. Show Commands")
    print("     9. Exit Game")

    return 1


def Game():
    print("Start Game...\n")
    G = game.GameState()
    
    printCommands1()
    while True:
        
        G = game.GameState()
        

        try:
            i = int(input("MENU: Enter command (1-9): "))
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")
            continue

        match i:
            case 1:
                continue
            case 2:
                viewTrucks()
                print()
            case 7:
                p = G.player
                print(p)
                print()
            case 8:
                printCommands1()
                print()
            case 9:
                break


    return 1

def menuLoop():
    print("Logistics Company Game")
    print("1. Play")
    print("2. Exit")

    while True:
        try:
            i = int(input("Enter command (1-2): "))
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")
            continue

        match i:

            case 1:
                Game()
                break

            case 2:
                print("Exiting Game...\n")
                return 1
            
            case _:
                print("Invalid Command\n")


def main():

    DB = database.PostgresHandler()
    DB.connect()

    menuLoop()


    DB.close()

    return 0


if __name__ == "__main__":
    main()