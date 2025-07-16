
from python.astar import escape_room_game_astar
from python.enemy_a_start.Enemy_Menu import menu
from python.escape_room import EscapeRoomGame


if __name__ == "__main__":
    option=0
    while True:
        print("1. Escape Room Clásico (Prolog)")
        print("2. Escape Room A*")
        print("3. Enemy A*")
        print("Enter -1 to exit")
        try:
            option=int(input("Enter game version:(1,2 or 3) "))
        except Exception:
            print("Invalid option")

        if option ==1:
            print("\nIniciando Escape Room Clásico...")
            game = EscapeRoomGame()  # Crea una instancia de tu juego
            game.main_menu() 
        elif option ==2:
            escape_room_game_astar.run_game()
        elif option ==3:
            menu()
            
        elif option ==-1:
            break

        
