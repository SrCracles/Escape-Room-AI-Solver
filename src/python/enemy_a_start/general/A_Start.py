from .State import State
from itertools import count
import heapq


def a_start(initial_state, final_state):
  parent_map={}
  from_hash_to_object={}
  #It was necessary to add a third element to the priority queue, if two f's are the same, the second criteria is this counter,
  #otherwise, python tries to compare np.arrays
  counter=count()
  #PRIORITY QUEUE
  priority_queue = []
  #OPEN STATES
  open_set=set()
  #CLOSED STATES
  closed_set=set()



  initial_state_hash=initial_state.get_hash()
  final_state_hash=final_state.get_hash()
  # DICT TO SAVE COSTS
  g={}
  g[initial_state_hash]=0
  # Dicto to save g+h
  f={}
  # F
  f_val=0+initial_state.get_h(final_state)
  f[initial_state_hash]=f_val

  heapq.heappush(priority_queue, (f_val, next(counter),initial_state))
  open_set.add(initial_state_hash)



  while priority_queue:

    _,_,parent=heapq.heappop(priority_queue)
    parent_hash=parent.get_hash()
    closed_set.add(parent_hash)
    sucessors=parent.get_sucessors()
    parent_cost=g[parent_hash]
    from_hash_to_object[parent_hash]=parent
    
    if (parent.is_goal()):
      
      return build_path(initial_state_hash,parent_hash,from_hash_to_object,parent_map)
    for sucessor in sucessors:
      sucessor_hash=sucessor.get_hash()
      cost=parent_cost+1
      current_f=cost+sucessor.get_h(final_state)
      if( (sucessor_hash not in open_set) and (sucessor_hash not in closed_set )):

        open_set.add(sucessor_hash)
        heapq.heappush(priority_queue, (current_f,next(counter), sucessor))
        g[sucessor_hash]=cost
        f[sucessor_hash]=current_f
        parent_map[sucessor_hash]=parent_hash

      else:
        prev_g=g[sucessor_hash]
        prev_f=f[sucessor_hash]
        g[sucessor_hash]=min(prev_g,cost)
        if sucessor_hash in closed_set and current_f<f[sucessor_hash]:
          f[sucessor_hash]=current_f
          open_set.add(sucessor_hash)
          heapq.heappush(priority_queue, (current_f,next(counter), sucessor))
          parent_map[sucessor_hash]=parent_hash
  return False

def build_path(initial_state_hash, final_state_hash, from_hash_to_state, parent_map):
    current=final_state_hash
    path=[]
    while True:
        path.append(from_hash_to_state[current])
        if current==initial_state_hash:
            break
        current=parent_map[current]
    path.reverse()
    return path
