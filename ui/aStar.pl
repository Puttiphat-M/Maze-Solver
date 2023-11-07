h((X1, Y1), (X2, Y2), H) :-
    H is abs(X1 - X2) + abs(Y1 - Y2).

has_wall(X, Y, D) :-
    wall(X, Y, D, 0).

% Define the A* algorithm using a heap for open nodes and a list for synchronization
a_star(Start, End, Path, Cost) :-
    % Create an empty heap for open nodes
    empty_heap(OpenHeap),
    % Create an empty list for open nodes (used for synchronization)
    OpenList = [],
    % Create the initial node with the start state
    InitialNode = a_star_node(Start, 0, [Start]),
    % Add the initial node to both the heap and list
    add_to_heap(OpenHeap, 0, InitialNode, OpenHeapWithNode),
    append(OpenList, [InitialNode], OpenListWithNode),
    % Initialize the closed list as an empty list
    ClosedList = [],
    % Call the A* search
    a_star(OpenHeapWithNode, OpenListWithNode, End, ClosedList, Path, Cost).



% Recursive case: Continue searching
a_star(OpenHeap, OpenList, End, ClosedList, Path, Cost) :-
    % Get the node with the lowest cost from the open heap
    get_from_heap(OpenHeap, _, CurrentNode, RestOpenHeap),
    % Extract information from the current node
    a_star_node(CurrentState, CurrentCost, CurrentPath) = CurrentNode,
    % Check if the current state is the goal
    (CurrentState = End ->
        Path = CurrentPath,
        Cost is CurrentCost
    ;   % Continue searching
        % Find valid neighbors, considering walls
        findall(Neighbor, valid_neighbor(CurrentState, Neighbor, ClosedList), Neighbors),
        % Update the closed list with the current state
        NewClosedList = [CurrentState | ClosedList],
        list_to_set(Neighbors, UniqueNeighbors),
        % Process neighbors and update open heap
        process_neighbors(UniqueNeighbors, CurrentState, CurrentCost, CurrentPath, End, RestOpenHeap, OpenList, NewOpenHeap),
        % Recursively search for the goal
        a_star(NewOpenHeap, OpenList, End, NewClosedList, Path, Cost)
    ).


% Process neighbors and update open heap
process_neighbors([], _, _, _, _, OpenHeap, _, OpenHeap).
process_neighbors([Neighbor | RestNeighbors], CurrentState, CurrentCost, CurrentPath, End, OpenHeap, ClosedList, NewOpenHeap) :-
    % Calculate the cost to reach the neighbor from the current node
    NewCost is CurrentCost + 1,
    % Calculate the heuristic value (e.g., Manhattan distance) for the neighbor
    h(Neighbor, End, H),
    % Calculate the total estimated cost
    F is NewCost + H,
    % Create a new node for the neighbor
    NewNode = a_star_node(Neighbor, NewCost, [Neighbor | CurrentPath]),
    % Check if the neighbor is in the closed list
    (   member(Neighbor, ClosedList)
    ->  % Neighbor is in the closed list, skip it
        process_neighbors(RestNeighbors, CurrentState, CurrentCost, CurrentPath, End, OpenHeap, ClosedList, NewOpenHeap)
    ;   % Neighbor is not in the closed list, insert it into the open heap
        add_to_heap(OpenHeap, F, NewNode, UpdatedOpenHeap),
        process_neighbors(RestNeighbors, CurrentState, CurrentCost, CurrentPath, End, UpdatedOpenHeap, ClosedList, NewOpenHeap)
    ).

% Define the predicate to check for valid neighbors, considering walls
valid_neighbor(CurrentState, Neighbor, ClosedList) :-
    neighbor(CurrentState, Neighbor),
    has_wall_between(CurrentState, Neighbor),
    \+ member(Neighbor, ClosedList).

neighbor((X, Y), (X, Y1)) :- Y1 is Y + 1, cell(_, Y1).
neighbor((X, Y), (X, Y1)) :- Y1 is Y - 1, cell(_, Y1).
neighbor((X, Y), (X1, Y)) :- X1 is X + 1, cell(X1, _).
neighbor((X, Y), (X1, Y)) :- X1 is X - 1, cell(X1, _).

% Define the predicate to check for the presence of walls between cells
has_wall_between((X, Y), (X, Y1)) :-
    Y < Y1,
    has_wall(X, Y, s),
    has_wall(X, Y1, n).

has_wall_between((X, Y), (X, Y1)) :-
    Y > Y1,
    has_wall(X, Y, n),
    has_wall(X, Y1, s).

has_wall_between((X, Y), (X1, Y)) :-
    X < X1,
    has_wall(X, Y, e),
    has_wall(X1, Y, w).

has_wall_between((X, Y), (X1, Y)) :-
    X > X1,
    has_wall(X, Y, w),
    has_wall(X1, Y, e).