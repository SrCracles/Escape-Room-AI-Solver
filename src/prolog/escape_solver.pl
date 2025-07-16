:- module(escape_solver, [best_next_move/6, full_solution/1]).

:- dynamic room_data/3.
:- dynamic visited/4.  % (X, Y, Room, HasKey)

move(Room, X, Y, X1, Y) :- X1 is X + 1, X1 < 5. % Right
move(Room, X, Y, X1, Y) :- X1 is X - 1, X1 >= 0. % Left
move(Room, X, Y, X, Y1) :- Y1 is Y + 1, Y1 < 5. % Down
move(Room, X, Y, X, Y1) :- Y1 is Y - 1, Y1 >= 0. % Up

% Room configuration (number, door, puzzle, item)
room_data(1, door(2,2), puzzle(3,3), item(4,4)).
room_data(2, door(3,3), puzzle(1,1), item(4,4)).
room_data(3, door(4,0), puzzle(2,2), item(0,4)). % Removed room 4

% best_next_move
best_next_move(X, Y, Room, DX, DY, Action) :-
    room_data(Room, _, puzzle(PX, PY), item(IX, IY)),
    (   (X =:= IX, Y =:= IY) -> Action = 'get item'
    ;   (X =:= PX, Y =:= PY) -> Action = 'solve puzzle'
    ;   (X =:= DX, Y =:= DY) -> Action = 'go to next room'
    ;   DY < Y, can_move(Room, X, Y, X, NY), NY is Y - 1 -> Action = 'up'
    ;   DY > Y, can_move(Room, X, Y, X, NY), NY is Y + 1 -> Action = 'down'
    ;   DX < X, can_move(Room, X, Y, NX, Y), NX is X - 1 -> Action = 'left'
    ;   DX > X, can_move(Room, X, Y, NX, Y), NX is X + 1 -> Action = 'right'
    ;   Action = 'wait'
    ).

can_move(Room, X, Y, NX, NY) :-
    move(Room, X, Y, NX, NY),
    \+ obstacle(Room, NX, NY).

obstacle(_, X, Y) :- X < 0 ; Y < 0 ; X >= 5 ; Y >= 5.

full_solution(Path) :-
    initial_state(1, 0, 0, false, false, State),
    find_escape_path(State, Path).

% Game states: state(Room, X, Y, HasKey, HasItem)
initial_state(Room, X, Y, HasKey, HasItem, state(Room, X, Y, HasKey, HasItem)).

find_escape_path(state(3, X, Y, _, _), []) :-
    room_data(3, door(X, Y), _, _), !.

find_escape_path(State, [Action|Actions]) :-
    next_action(State, Action, NextState),
    find_escape_path(NextState, Actions).

next_action(state(Room, X, Y, HasKey, HasItem), Action, NextState) :-
    room_data(Room, door(DX, DY), puzzle(PX, PY), item(IX, IY)),
    (   % Get item if we're at its position and don't have it
        X =:= IX, Y =:= IY, \+ HasItem ->
        Action = 'get item',
        NextState = state(Room, X, Y, HasKey, true)
    ;   % Solve puzzle if we have the item and are at its position
        X =:= PX, Y =:= PY, HasItem, \+ HasKey ->
        Action = 'solve puzzle',
        NextState = state(Room, X, Y, true, false)
    ;   % Go to next room if we have the key and are at the door
        X =:= DX, Y =:= DY, HasKey, Room < 3 -> % Changed from 4 to 3
        Action = 'go to next room',
        NextRoom is Room + 1,
        NextState = state(NextRoom, 0, 0, false, false)
    ;   % Movement toward door, puzzle or item
        best_move_towards_target(Room, X, Y, HasKey, HasItem, Action),
        update_position(Action, Room, X, Y, NX, NY),
        NextState = state(Room, NX, NY, HasKey, HasItem)
    ).

best_move_towards_target(Room, X, Y, HasKey, HasItem, Action) :-
    room_data(Room, door(DX, DY), puzzle(PX, PY), item(IX, IY)),
    (   \+ HasItem -> TargetX = IX, TargetY = IY
    ;   \+ HasKey -> TargetX = PX, TargetY = PY
    ;   TargetX = DX, TargetY = DY
    ),
    (   TargetY < Y, can_move(Room, X, Y, X, NY), NY is Y - 1 -> Action = 'up'
    ;   TargetY > Y, can_move(Room, X, Y, X, NY), NY is Y + 1 -> Action = 'down'
    ;   TargetX < X, can_move(Room, X, Y, NX, Y), NX is X - 1 -> Action = 'left'
    ;   TargetX > X, can_move(Room, X, Y, NX, Y), NX is X + 1 -> Action = 'right'
    ;   Action = 'wait'
    ).

update_position('up', Room, X, Y, X, NY) :- NY is Y - 1.
update_position('down', Room, X, Y, X, NY) :- NY is Y + 1.
update_position('left', Room, X, Y, NX, Y) :- NX is X - 1.
update_position('right', Room, X, Y, NX, Y) :- NX is X + 1.
update_position(Action, Room, X, Y, X, Y) :- 
    member(Action, ['get item', 'solve puzzle', 'go to next room']).

:- initialization((
    writeln('Escape Room solution system loaded successfully'),
    retractall(visited(_, _, _, _))
)).