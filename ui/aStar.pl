a_star(Grid, Start, Goal, Walls, Path) :-
    % Initialize the open and closed lists.
    Open = [[0, Start]],
    Closed = [].

    % Loop until the goal node is found or the open list is empty.
    loop(Open, Closed, Walls, Goal, Path).

loop([Cost, Current | Open], Closed, Walls, Goal, Path) :-
    % Check if the current node is the goal node.
    if (Current = Goal) then
        % Path found!
        get_path(Path, Current, Start).
    else
        % Expand the current node.
        expand(Current, Walls, Grid, Successors).

        % Add the successors to the open list if they are not already in the open or closed lists.
        for (Successor in Successors) do
            if (not member(Successor, Open) and not member(Successor, Closed)) then
                insert(Open, [Cost + 1, Successor]).
            end.
        end.

        % Move the current node to the closed list.
        remove(Open, Current, Open1).
        append(Closed, [Current], Closed1).

        % Recursively loop until the goal node is found or the open list is empty.
        loop(Open1, Closed1, Walls, Goal, Path).

expand(Node, Walls, Grid, Successors) :-
    % Get the coordinates of the current node.
    (X, Y) = Node.

    % Generate the possible successor nodes.
    for (Direction in ['E', 'W', 'N', 'S']) do
        % Check if the successor node is within the bounds of the grid.
        if ((X + 1 <= 6 and Direction = 'E') or
            (X - 1 >= 0 and Direction = 'W') or
            (Y + 1 <= 6 and Direction = 'N') or
            (Y - 1 >= 0 and Direction = 'S')) then
            % Check if the successor node is a wall.
            if (Walls[Node][Direction] = 0 or Grid[Node][Direction] = 0) then
                % The successor node is either a wall or an invalid space, so do not add it to the list of successors.
            else
                % The successor node is not a wall and is a valid space, so add it to the list of successors.
                append(Successors, [X + dx(Direction), Y + dy(Direction)]).
            end.
        end.
    end.

dx(Direction) :-
    if (Direction = 'E') then
        1.
    else if (Direction = 'W') then
        -1.
    else
        0.

dy(Direction) :-
    if (Direction = 'N') then
        1.
    else if (Direction = 'S') then
        -1.
    else
        0.

get_path(Path, Goal, Start) :-
    if (Goal = Start) then
        Path = [Goal].
    else
        % Find the parent of the goal node.
        (Parent, _) = member(Goal, Open),
        remove(Open, Parent, Open1),

        % Recursively get the path from the parent to the start node.
        append([Parent], Path, NewPath),
        get_path(NewPath, Parent, Start).
