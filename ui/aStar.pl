
h(cell(X1, Y1), cell(X2, Y2), H) :-
    H is abs(X1 - X2) + abs(Y1 - Y2).


a_star(Grid, Start, End, Walls, Path) :-

    initialize_scores(Grid, Start, GScore, FScore),

    open_set_priority_queue([fscore(Start, FScore)], OpenSet),
    a_star_helper(Grid, Start, End, Walls, GScore, FScore, OpenSet, [], Path).


a_star_helper(_, End, End, _, _, _, Acc, Acc).


a_star_helper(Grid, CurrCell, End, Walls, GScore, FScore, OpenSet, Acc, Path) :-

    find_neighbors(Grid, CurrCell, Walls, Neighbors),

    update_scores(CurrCell, End, Neighbors, GScore, FScore, OpenSet, NewOpenSet),

    select(fscore(NextCell, _), NewOpenSet, UpdatedOpenSet),

    a_star_helper(Grid, NextCell, End, Walls, GScore, FScore, UpdatedOpenSet, [NextCell|Acc], Path).


initialize_scores(Grid, Start, GScore, FScore) :-
    findall(cell(X, Y), member(row(X, Y, _), Grid), Cells),
    maplist(init_score(GScore), Cells, [inf|_]),
    h(Start, End, H),
    maplist(init_score(FScore, H), Cells, [inf|_]).

init_score(Dict, Key, Value) :- Dict =.. [Name, Key, Value], call(Name).


find_neighbors(Grid, cell(X, Y), Walls, Neighbors) :-
    findall(NextCell, (
        member(d(Direction, NextCell), [n(cell(X, Y), N), e(cell(X, Y), E), s(cell(X, Y), S), w(cell(X, Y), W)]),
        \+ member(row(N, E, S, W), Grid),
        \+ member(d(Direction, NextCell), Walls)
    ), Neighbors).


update_scores(CurrCell, End, Neighbors, GScore, FScore, OpenSet, UpdatedOpenSet) :-
    maplist(update_score(CurrCell, End, GScore, FScore, OpenSet), Neighbors, UpdatedOpenSet).


update_score(CurrCell, End, GScore, FScore, OpenSet, NextCell, fscore(NextCell, NewFScore)) :-
    g_score(CurrCell, NextCell, G),
    NewG is G + g_score(CurrCell),
    get_f_score(NextCell, FScore, OldFScore),
    NewFScore is NewG + h(NextCell, End),
    (member(fscore(NextCell, _), OpenSet) ->
        replace(open_set_priority_queue, fscore(NextCell, OldFScore), fscore(NextCell, NewFScore), OpenSet)
    ;   append([fscore(NextCell, NewFScore)], OpenSet, UpdatedOpenSet)
    ).


g_score(CurrCell, NextCell, G) :-
    h(CurrCell, NextCell, H),
    G is 1 + H.


get_f_score(Cell, FScore, Value) :-
    FScore =.. [fscore, Cell, Value].


reconstruct_path(Start, Acc, Path) :-
    reverse([Start|Acc], Path).


print_path([]).
print_path([cell(X,Y)|T]) :-
    format("path(~w,~w) ", [X, Y]),
    print_path(T).
