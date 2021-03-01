from typing import Any
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from random import choice


class TextBasedAdventureGameTest(StageTest):
    username = "new_user"
    name = "john"
    species = "human"
    gender = "male"
    snack = "apple"
    weapon = "sword"
    tool = "rope"
    difficulty = "easy"
    lives = "5"
    picked_choice = ""

    def generate(self) -> [TestCase]:
        return [
            TestCase(stdin=[self.check_welcome]),
            TestCase(stdin=["1", self.check_start_load]),
            TestCase(stdin=["start", self.check_start_load]),
            TestCase(stdin=["StARt", self.check_start_load]),
            TestCase(stdin=["2", self.check_start_load]),
            TestCase(stdin=["load", self.check_start_load]),
            TestCase(stdin=["lOAd", self.check_start_load]),
            TestCase(stdin=["5", self.check_unknown]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, self.check_game_state, "3"]),
            TestCase(stdin=["1", "/b", self.check_go_back]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, (-1, self.check_level1)]),
            TestCase(stdin=[self.check_save]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, "/i", self.check_inventory]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, "/c", self.check_char]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, "/h", self.check_help]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, "/q", (2, self.check_quit)]),
            TestCase(stdin=["1", self.check_username, self.name, self.species, self.gender, self.snack, self.weapon,
                            self.tool, self.difficulty, "4", self.check_unknown]),
            TestCase(stdin=["2", self.username, (-1, self.check_level2)]),
            TestCase(stdin="3"),
            TestCase(stdin="quIt")
        ]

    def check_welcome(self, output):
        if "welcome to" not in output.lower() and "***" not in output:
            return CheckResult.wrong("You didn't output a correct welcome message!")
        return CheckResult.correct()

    def check_start_load(self, output):
        if "starting a new game" in output.lower() or "no save data found" in output.lower() or "type your username" in output.lower():
            return CheckResult.correct()
        return CheckResult.wrong("Your program didn't output correct message.")

    def check_unknown(self, output):
        if "unknown input! please enter a valid one" in output.lower():
            return CheckResult.correct()
        return CheckResult.wrong("Your program couldn't process unknown input.")

    def check_username(self, output):
        if "enter a username" not in output.lower() and "/b" not in output.lower():
            return CheckResult.wrong("You didn't ask for the username and didn't give the option to go back.")
        return self.username

    def check_game_state(self, output):
        states = [self.name, self.species, self.gender, self.snack, self.weapon, self.tool, self.difficulty]
        have_state = all([state in output.lower() for state in states])
        if "good luck on your journey" not in output.lower():
            return CheckResult.wrong("You didn't output the correct message.")
        elif not have_state:
            return CheckResult.wrong("You didn't output the correct game state.")
        return CheckResult.correct()

    def check_go_back(self, output):
        if "going back to menu" not in output.lower():
            CheckResult.wrong("You didn't output the correct message when going back to menu.")
        return "3"

    def check_level1(self, output):
        choices = ["1", "2", "3"]
        random_choice = choice(choices)
        if "level 2" in output.lower():
            return CheckResult.correct()
        elif "game over" in output.lower():
            return "1"
        elif "starting a new game" in output.lower():
            return self.username
        elif "1- name" in output.lower():
            return self.name
        elif "2- species" in output.lower():
            return self.species
        elif "3- gender" in output.lower():
            return self.gender
        elif "1- favourite snack" in output.lower():
            return self.snack
        elif "2- a weapon for the journey" in output.lower():
            return self.weapon
        elif "3- a traversal tool" in output.lower():
            return self.tool
        elif "choose your difficulty" in output.lower():
            return self.difficulty

        if "you died" in output.lower() and "level 1" not in output.lower():
            return CheckResult.wrong("Your program didn't start from the beginning of the level.")

        if "what will you do? type the number of the option or type '/h' to show help." not in output.lower():
            choices.pop(choices.index(self.picked_choice))
            self.picked_choice = choice(choices)
            return self.picked_choice

        else:
            self.picked_choice = random_choice
            return self.picked_choice

    def check_save(self, output):
        try:
            with open(f"saves/{self.username}.txt") as f:
                content = f.readlines()
                character = content[0].lower().strip().split(", ")
                inventory = content[1].lower().strip().split(", ")
                difficulty = content[2].lower().strip().split(" ")
                level = content[3].strip()

                if len(character) != 3 or self.name not in character or self.species not in character or self.gender not in character:
                    return CheckResult.wrong("Save file doesn't contain the correct character traits.")
                elif len(inventory) < 2 or self.weapon not in inventory or self.tool not in inventory:
                    return CheckResult.wrong("Save file doesn't contain the correct inventory.")
                elif len(difficulty) != 2 or self.difficulty not in difficulty:
                    return CheckResult.wrong("Save file doesn't contain the correct difficulty and life count.")
                elif level != "2":
                    return CheckResult.wrong("Save file doesn't contain the correct level count.")
                else:
                    return CheckResult.correct()

        except (TypeError, IndexError, FileNotFoundError):
            return CheckResult.wrong("Save file doesn't exist with the given player name.")

    def check_level2(self, output):
        choices = ["1", "2", "3"]
        random_choice = choice(choices)
        if "congratulations! you beat the game" in output.lower() or "game over" in output.lower():
            return CheckResult.correct()

        if "you died" in output.lower() and "level 2" not in output.lower():
            return CheckResult.wrong("Your program didn't start from the beginning of the level.")

        if "what will you do? type the number of the option or type '/h' to show help." not in output.lower():
            choices.pop(choices.index(self.picked_choice))
            self.picked_choice = choice(choices)
            return self.picked_choice

        else:
            self.picked_choice = random_choice
            return self.picked_choice

    def check_inventory(self, output):
        inventory = [self.snack, self.weapon, self.tool]
        in_inventory = all([item in output.lower() for item in inventory])

        if "inventory" not in output.lower() or not in_inventory:
            return CheckResult.wrong("Your program didn't output correct inventory content.")
        else:
            return CheckResult.correct()

    def check_char(self, output):
        char = [self.name, self.species, self.gender, self.lives]
        in_char = all([ch in output.lower() for ch in char])
        if "character" not in output.lower() or not in_char or "lives remaining" not in output.lower():
            return CheckResult.wrong("Your program didn't output correct character traits.")
        else:
            return CheckResult.correct()

    def check_help(self, output):
        message = "type the number of the option you want to choose.\n" + "commands you can use:\n/i => shows inventory.\n" \
                  + "/q => exits the game.\n" + "/c => shows the character traits.\n" + "/h => shows help."
        if message not in output.lower():
            return CheckResult.wrong("Your program didn't output the correct help message.")
        else:
            return CheckResult.correct()

    def check_quit(self, output):
        if "you sure you want to quit the game? y/n " in output.lower():
            return "y"
        elif "goodbye!" in output.lower():
            return CheckResult.correct()
        else:
            return CheckResult.wrong("You didn't ask to quit the game.")

    def check(self, reply: str, attach: Any) -> CheckResult:
        if "goodbye!" in reply.lower():
            return CheckResult.correct()
        return CheckResult.wrong("Your program didn't print a correct goodbye message.")


if __name__ == '__main__':
    TextBasedAdventureGameTest().run_tests()
