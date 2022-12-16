from game import Game
from client_setup import WIDTH, HEIGHT

if __name__ == "__main__":
    my_nickname = input("Ingrese su nickname: ")
    game = Game(WIDTH, HEIGHT, my_nickname)
    game.run()