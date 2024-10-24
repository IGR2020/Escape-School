import Game.game
import Game.school

if __name__ == "__main__":
    menu = Game.game.MainMenu((900, 500))
    command = menu.start()
    if command == "Quit":
        print("[Advice] At Least Play The Game")
    elif command == "Game":
        school = Game.school.School((900, 500), "Game/data/test2.pkl")
        school.start()
    elif command == "Editor":
        editor = Game.game.LevelEditor((900, 600), "Game/data/test2.pkl")
        editor.start()
    