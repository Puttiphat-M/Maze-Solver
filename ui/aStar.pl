% Define the heuristic function (Manhattan distance)
h((X1, Y1), (X2, Y2), H) :-
    write('Calculating heuristic for '), write((X1, Y1)), write(' and '), write((X2, Y2)), nl,
    H is abs(X1 - X2) + abs(Y1 - Y2),
    write('Heuristic is '), write(H), nl.

has_wall(X, Y, D) :-
    wall(X, Y, D, 0).

% Define the A* algorithm
a_star(Start, End, Path, Cost) :-
    g_score(Start, 0, Start, End, [], Path, Cost).

g_score(Current, G, _, _, Visited, Path, Cost) :-
    member(Current, Visited),
    !,
    Path = [],
    Cost = G, %0
    write('Already visited '), write(Current), nl.

g_score(Current, G, _, Current, _, [Current], G) :-
    !,
    write('Reached goal at '), write(Current), nl.

g_score(Current, G, Start, End, Visited, Path, Cost) :-
    findall(Neighbor, valid_neighbor(Current, Neighbor, Visited), Neighbors),
    list_to_set(Neighbors, UniqueNeighbors),
    write('Neighbors: '), write(UniqueNeighbors), nl,
    best_neighbor(UniqueNeighbors, Start, End, G, BestNeighbor, BestNeighborCost),
    write('Best neighbor: '), write(BestNeighbor), write(' with cost '), write(BestNeighborCost), nl,
    NewG is G + 1,
    g_score(BestNeighbor, NewG, Start, End, [Current|Visited], RestOfPath, RestOfCost),
    append([Current], RestOfPath, Path),
    Cost is BestNeighborCost + RestOfCost.

valid_neighbor(Current, Neighbor, Visited) :-
    neighbor(Current, Neighbor),
    wall_between(Current, Neighbor),
    \+ member(Neighbor, Visited).

neighbor((X, Y), (X, Y1)) :- Y1 is Y + 1, cell(_, Y1).
neighbor((X, Y), (X, Y1)) :- Y1 is Y - 1, cell(_, Y1).
neighbor((X, Y), (X1, Y)) :- X1 is X + 1, cell(X1, _).
neighbor((X, Y), (X1, Y)) :- X1 is X - 1, cell(X1, _).

wall_between((X, Y), (X, Y1)) :-
    Y < Y1,
    has_wall(X, Y, s),
    has_wall(X, Y1, n).

wall_between((X, Y), (X, Y1)) :-
    Y > Y1,
    has_wall(X, Y, n),
    has_wall(X, Y1, s).

wall_between((X, Y), (X1, Y)) :-
    X < X1,
    has_wall(X, Y, e),
    has_wall(X1, Y, w).

wall_between((X, Y), (X1, Y)) :-
    X > X1,
    has_wall(X, Y, w),
    has_wall(X1, Y, e).


best_neighbor([Neighbor], _, _, G, Neighbor, G).
best_neighbor([Neighbor1, Neighbor2|Rest], Start, End, G, BestNeighbor, BestNeighborCost) :-
    write('Best neighbor: '), write(Neighbor1), write(' or '), write(Neighbor2), nl,
    write('End: '), write(End), nl,
    h(Neighbor1, End, H1),
    h(Neighbor2, End, H2),
    F1 is G + H1,
    F2 is G + H2,
    (F1 < F2 -> best_neighbor([Neighbor1|Rest], Start, End, G, BestNeighbor, BestNeighborCost);
               best_neighbor([Neighbor2|Rest], Start, End, G, BestNeighbor, BestNeighborCost)).
