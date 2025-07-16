import time
from .Game_Constants import GameConstants
from .general.A_Start import a_start
from .Minimax import minimax

gameConstants=GameConstants()
def menu():
    lvl_1()
    lvl_2()
    lvl_3()

def lvl_1(): #OK!!
    print("LEVEL 1")
    initial_state=gameConstants.lvl_1_get_initial_state()
    final_state=gameConstants.lvl_1_get_final_state()
    handle_lvl(initial_state, final_state)
def lvl_2(): #OK
    print("LEVEL 2")
    initial_state=gameConstants.lvl_2_get_initial_state()
    final_state=gameConstants.lvl_2_get_final_state()
    handle_lvl(initial_state, final_state)

def lvl_3():
    print("LEVEL 3")
    initial_state=gameConstants.lvl_3_get_initial_state()
    final_state=gameConstants.lvl_3_get_final_state()
    handle_lvl(initial_state, final_state)

def handle_lvl(initial_state,final_state):
    current=initial_state
    while(current.has_won==False):
        print("Enter -1 to seek a small fragment of wisdom from the oracle.")
        print("Enter -2 to call your mother.")
        print("Enter -3 to to raise the white flag and omit this level")

        print(current)

        next_states=current.get_sucessors()
        
        for i in range (0,len(next_states)):
            print(f"{i} to {next_states[i].action}")
        
        try:
            action=int(input("Action:"))
        except Exception:
            print("Invalid option")
            continue
        

        if action==-1:
            handle_next_movement_request(current,final_state)
            continue
        
        if action == -2:
            handle_solution_request(current, final_state)
            continue
        if action == -3:
            break

        if not ( 0<=action<len(next_states)):
            print("Invalid option")
            continue

        current= next_states[action]    
    print(current)
    print("The end...")

def handle_next_movement_request(initial_state,final_state):
    start = time.time()
    path=a_start(initial_state,final_state)
    end = time.time()
    total_time=end-start
    old_man="""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡤⠶⠭⠥⣼⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠉⠓⢦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⡤⠞⢋⡟⣡⣤⠶⣶⡄⠀⠀⠀⢠⡶⠶⢦⣄⠙⣦⠤⢤⡀⠀⠀
⢀⡞⣡⢤⡾⠈⣵⠒⠶⢦⡀⢠⠖⠀⢠⡔⠒⠶⣮⠀⠘⣦⣤⡙⣆⠀
⢸⢿⡇⢰⠇⠀⠙⠒⠶⠋⢀⡏⠀⠀⠀⠙⠒⠚⠉⠀⠀⢹⠀⣹⠸⡆
⣾⠀⣉⢻⡄⠀⠀⠀⠀⣸⣼⣆⠀⣸⣤⡆⠀⠀⠀⠀⠀⢸⠞⠁⠀⢷
⠈⠉⠉⠛⢷⡀⠀⠀⠰⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⡼⠶⠚⠛⠋
⠀⠀⠀⠀⠀⠳⣄⠀⠀⠀⠀⠀⠉⠀⠈⠁⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠛⠦⣄⣀⠀⠀⠀⠀⣀⣠⡴⠚⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⢾⣈⠉⠉⢉⣉⣁⡿⢤⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡟⠀⠈⠉⠉⠉⠉⠁⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⠤⠶⠚⠁⠀⠦⠤⠤⠤⠤⠖⠂⠀⠈⠓⠦⢤⣀⠀⠀⠀
⠀⢀⡞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⠀
⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡆
⣸⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠀⠀⣷
⡏⠀⠀⠀⢸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⢸
⠃⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠁⠀⠀⠀⠘

"""
    print(old_man)
    time.sleep(2)
    print(f"The old man thought for about {total_time} seconds")
    print("The old man whispers...")
    time.sleep(2)
    try:
        print( f"{path[1].get_prev_action()}" )
    except Exception:
        print("not now homie")

    time.sleep(1)
    print()

def handle_solution_request(initial_state, final_state):
    start = time.time()
    path=a_start(initial_state,final_state)
    end = time.time()
    total_time=end-start
    image="""
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠶⠖⣒⣛⣛⠒⠲⠶⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡴⠛⠉⠀⣀⣴⠿⠛⠛⠛⠿⣷⣦⡀⠀⠉⠛⢦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⠔⠁⠀⠀⠀⢰⠃⠀⠀⠀⠀⠀⠀⢼⣿⣷⠀⠀⠀⠀⠈⠢⡀⠀⠀⠀
⠀⠀⡴⠋⠀⠀⠀⠀⠀⢸⣠⢤⣄⢀⣤⢤⣤⡤⠽⣟⡀⠀⠀⠀⠀⠀⠙⢦⠀⠀
⠀⡸⠁⠀⠀⠀⠀⠀⠀⠘⠛⠑⠽⠉⠚⠉⠩⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀
⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⢤⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆
⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠊⠁⠈⠁⠀⠀⠀⢀⣶⣄⠀⠀⠀⠀⠀⠀⠀⣷
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣬⠲⣦⡤⠔⠊⠀⣠⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿
⢿⠀⠀⠀⠀⠀⠤⠤⡀⢻⣿⣿⠃⢿⣯⡅⠀⣰⣿⣿⣿⡗⡎⡀⠀⠀⠀⠀⠀⡿
⠸⡇⠀⠀⠀⠀⠀⠀⠟⠀⣿⡏⢀⡾⡟⠀⣰⣿⣿⣿⣿⡿⢖⡈⡄⠀⠀⠀⢰⠇
⠀⢳⡀⠀⠀⠀⠀⠈⡤⢤⢬⡥⢺⣿⣷⣤⢯⠽⡛⡹⠛⡙⡢⠄⡄⠀⠀⢀⡞⠀
⠀⠀⠳⡄⠀⠰⣤⠏⠇⠫⠼⡇⣾⡃⢸⣿⠈⠨⣐⠹⠶⠕⣬⠜⠁⠀⢠⠞⠀⠀
⠀⠀⠀⠈⠢⡀⠀⠀⠀⠰⠦⣶⢾⡷⣾⡷⠲⣶⢶⣾⠀⠉⠀⠀⢀⡴⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠶⣄⡀⠀⢶⡿⢼⡇⣿⡇⠾⡿⢺⣿⠀⢀⣠⠖⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠒⠶⠬⣥⣬⣥⣤⠤⠶⠛⠊⠉⠀⠀⠀⠀
"""
    print(image)
    time.sleep(2)
    print(f"The woman thoght for about {total_time} seconds")
    print("The woman shouts... ")
    time.sleep(2)

    try:
        for i in range(1, len(path)):
            print(f" {path[i].action.upper()}!", end="")
    except Exception:
        print("I'm busy!!")


    time.sleep(2)
    
    print()
    print()
    print()
    
    



    
