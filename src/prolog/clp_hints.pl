:- use_module(library(clpfd)).

:- dynamic room_puzzle/4.

get_puzzle_info(RoomNumber, Hint, ExpectedCode) :-
    room_puzzle(RoomNumber, Vars, Constraints, Codes),
    call(Constraints),
    label(Vars),
    generate_hint(RoomNumber, Vars, Hint),
    extract_code(RoomNumber, Codes, ExpectedCode).

extract_code(1, [_, _, _, _, Code1, Code2, Code3], CodeStr) :-
    format(atom(CodeStr), '~w~w~w', [Code1, Code2, Code3]).
extract_code(2, [_, _, _, _, Code], CodeStr) :-
    format(atom(CodeStr), '~w', [Code]).
extract_code(3, [_, _, _, _, Code], CodeStr) :-
    format(atom(CodeStr), '~w', [Code]).

room_puzzle(1, 
    [Red, Green, Blue, Yellow, Code1, Code2, Code3],
    (
        [Red, Green, Blue, Yellow] ins 1..4,
        all_different([Red, Green, Blue, Yellow]),
        Red #= 1,
        Green #\= 3,
        Blue #\= Red,
        Blue #\= Green,
        Yellow #= Blue + 1,
        Code1 #= Red,
        Code2 #= Green,
        Code3 #= Blue
    ),
    [1, 2, 3, 4, 1, 2, 3]).

room_puzzle(2,
    [North, South, East, West, Code],
    (
        [North, South, East, West] ins 1..4,
        all_different([North, South, East, West]),
        North #= 2,
        West #> South,
        East #= North + 1,
        Code #= West
    ),
    [2, 1, 3, 4, 4]).

room_puzzle(3,
    [Symbol1, Symbol2, Symbol3, Symbol4, FinalCode],
    (
        [Symbol1, Symbol2, Symbol3, Symbol4] ins 1..5,
        all_different([Symbol1, Symbol2, Symbol3, Symbol4]),
        Symbol1 #= 3,
        Symbol2 #\= 1,
        Symbol3 #= Symbol1 + 1,
        Symbol4 #= 2 #\/ Symbol4 #= 5,
        FinalCode #= Symbol2
    ),
    [3, 2, 4, 5, 2]).

generate_hint(1, [Red, Green, Blue|_], Hint) :-
    format(atom(Hint), 'Color code hint: Red is ~w, Green is ~w, Blue is ~w', [Red, Green, Blue]).
generate_hint(2, [_, _, _, West, _], Hint) :-
    format(atom(Hint), 'Direction lock hint: West is ~w', [West]).
generate_hint(3, [_, Symbol2|_], Hint) :-
    format(atom(Hint), 'Final puzzle hint: Second symbol is ~w', [Symbol2]).