"""Second stage implementation of adventure game.
Implementation of the game story, choices and outcomes"""

from sys import exit
from os import listdir


def main_menu():
    print("***Welcome to the Journey to Mount Qaf***\n",
          "1- Press key '1' or type 'start' to start a new game",
          "2- Press key '2' or type 'load' to load your progress",
          "3- Press key '3' or type 'quit' to quit the game", sep='\n')


class Game:
    def __init__(self):
        self.input_list = ['1', '2', '3', 'start', 'load', 'quit']
        self.character = []
        self.inventory = []
        self.difficulty = ''
        self.user_name = ''
        self.lives = 5
        self.level = 1
        self.progress = 0
        with open('story/story.txt') as s, open('story/choices.txt') as c, open('story/outcomes.txt') as o:
            self.story = [i.strip() for i in s.read().split('+')]
            self.choices = c.read().split('\n')
            self.outcomes = [i.strip() for i in o.read().split('*')]

    def menu_input(self):
        """Taking input from user and checking if it valid or not,
        Then checking user's choice and moving to next step accordingly"""
        main_menu()
        user_input = input("> ").lower()
        if user_input in self.input_list:
            if user_input == '1' or user_input == 'start':
                print("Starting a new game...")
                self.creating_new_character()
            elif user_input == '2' or user_input == 'load':
                for f in listdir('saves'):
                    print(f[:-4])
                self.user_name = input()
                with open(f"saves/{self.user_name}.txt") as g:
                    game = g.readlines()
                    print(game)
                    for i in range(4):
                        print(game[i].strip())
                    self.character = game[0]
                    self.inventory = game[1]
                    self.difficulty = game[2].split()[0]
                    self.level = game[3]
                    self.progress = int(game[4])
                self.game_loop()
            elif user_input == '3' or user_input == 'quit':
                print("Goodbye!")
                exit()
        else:
            print("Unknown input! Please enter a valid one.\n")
            self.menu_input()

    def creating_new_character(self):
        self.user_name = input("Enter a user name to save your progress or type '/b' to go back\n> ")
        if self.user_name == '/b':
            print("Going back to menu...")
            self.menu_input()

        character = ["Name", "Species", "Gender"]
        print("Create your character:")
        for i, e in enumerate(character, start=1):
            self.character.append(input(f"{i}- {e} ").lower().capitalize())

        inventory = ["Favourite Snack", "A weapon for the journey", "A traversal tool"]
        print("Pack your bag for the journey:")
        for i, e in enumerate(inventory, start=1):
            self.inventory.append(input(f"{i}- {e} ").lower().capitalize())

        difficulty_level = ["Easy", "Medium", "Hard"]
        print("Choose your difficulty:")
        for i, e in enumerate(difficulty_level, start=1):
            print(f"{i}- {e}")
        difficulty_choice = input()
        try:
            self.difficulty = difficulty_level[int(difficulty_choice) - 1]
        except ValueError:
            self.difficulty = difficulty_choice.lower().capitalize()

        print("Good luck on your journey!",
              f"Your character: {self.character}",
              f"Your inventory: {self.inventory}",
              f"Difficulty: {self.difficulty}", sep='\n')
        self.game_loop()

    def game_loop(self):
        while self.progress != 'break':
            if self.story[self.progress] == "Level 2":
                self.level = 2
                print("You've found a safe spot to rest. Saving your progress...")
                with open(f'saves/{self.user_name}.txt', 'w') as save:
                    print(self.character, self.inventory,
                          (self.difficulty + ' ' + str(self.lives) + '\n'),
                          (str(self.level) + '\n'), self.progress, file=save)
            print(self.story[self.progress])
            print(self.choices[self.progress])
            print(self.outcomes[self.progress])
            move = input()
            if move == '/q':
                print("Goodbye!")
                exit()
                """print("You sure you want to quit the game? y/n\n> ")
                inp = input()
                if inp == 'y':
                    print("Goodbye!")
                    exit()"""
            elif move == '/i':
                print(f"Inventory: {self.inventory}")
            elif move == '/c':
                print(f"Your character: {self.character}.\n"
                      f"Lives remaining: {self.lives}")
            elif move == '/h':
                print("Type the number of the option you want to choose.",
                      "Commands you can use:",
                      "/i => Shows inventory.",
                      "/q => Exits the game.",
                      "/c => Shows the character traits.",
                      "/h => Shows help.", sep='\n')
            else:
                print("Unknown input! Please enter a valid one")
                pass
            self.progress += 1


game_start = Game()
game_start.menu_input()
