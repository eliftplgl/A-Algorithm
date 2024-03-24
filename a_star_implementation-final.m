area_size = 5;
start = [3,1]; 
goal = [4,4];
path = astar(area_size,start,goal);
route_array = route(goal,path);
grid_plot(route_array,goal,start);
route_array
path



%----------------------Get List Value------------------------------------
function val = get_i(list, i) % get the values of the ith element
    val = [list((i - 1) * 2 + 1) list((i- 1) * 2 + 2)];
end
%------------------------------------------------------------------------


%----------------------Delete List Value---------------------------------
function list = del_i(list, i)
    list((i-1) * 2 + 1) = [];
    list((i-1) * 2 + 1) = []; 
    % delete the ith element twice (priority queue)
end
%------------------------------------------------------------------------


%-----------------------Check Element is in List--------------------------
function res = is_in_list(list, el)
    for i = 1 : numel(list) / 2
        getted = get_i(list, i);
        if el(1) == getted(1) && el(2) ==getted(2)
            res = i;
            return;
        end
    end
    res = 0;
end
%------------------------------------------------------------------------


%-----------------------Find Smallest f in List--------------------------
function [smallest, open_list] = find_smallest_f(open_list, goal, g, h)
    smallest_node = get_i(open_list, 1);
    smallest_i = 1;
    smallest_f = g(smallest_node(1),smallest_node(2)) + h(smallest_node, goal);

    for i = 1:numel(open_list) / 2
        node = get_i(open_list, i);
        f = g(node(1),node(2)) + h(node, goal);
        if f < smallest_f
            smallest_node = node;
            smallest_f = f;
            smallest_i = i;
        end
    end
    open_list = del_i(open_list, smallest_i);
    smallest = smallest_node;
end
%------------------------------------------------------------------------


%----------------------Child Sub Routine---------------------------------
function [open_list, closed_list, g, parents] = child_sub_routine(child, parent, open_list, closed_list, g, from, parents) % create an open list
    if child(1) <= 0 || child(2) <= 0
        return;
    end
    new_g = 1 + g(parent(1), parent(2));
    
    open_ind = is_in_list(open_list, child);
    if open_ind ~=0
        if g(child(1),child(2)) <= new_g
            return
        end
        parents(child(1), child(2)) = from;
        g(child(1),child(2)) = new_g;
        return;
    end

    closed_ind = is_in_list(closed_list, child);
    if closed_ind ~= 0
        if g(child(1),child(2)) <= new_g
            return
        end
        % closed listten silip open liste ekle

        g(child(1),child(2)) = new_g;
        parents(child(1), child(2)) = from;
        closed_list = del_i(closed_list,closed_ind);
        open_list = [open_list child];
        return;
    end
    if g(child(1), child(2)) <= new_g
        return
    end
    parents(child(1), child(2)) = from;
    g(child(1),child(2)) = g(parent(1),parent(2)) + 1;
    open_list = [open_list child];

end
%------------------------------------------------------------------------


%------------------------A* Algorithm-----------------------------------
function path = astar(area_size,start,goal)
    
    area = zeros(area_size,area_size);
    
    % Heuristic distance calculation considering manhattan distance
    h = @(node,goal) abs(node(1)-goal(1))+abs(node(2)-goal(2));
    
    % Generate grid
    grid_map = grid_generate();

    g = zeros(size(area));
    g(:,:) = inf;
    g(start(1),start(2))=0;

    %f = zeros(size(area));
    %f(:,:) = inf;
    %f(start)=h(start,goal)+g(start);
    
    open_list = [];
    open_list = [open_list start];
    closed_list = [];

    parents = char(zeros(size(area))); % create 5x5 character array

    while numel(open_list) > 0
        [current_node, open_list] = find_smallest_f(open_list, goal, g, h);   % we exclude the start node from the list
        if current_node == goal
            break 
        end
    a = current_node(1) * 10 + current_node(2)
        value = grid_map(current_node(1) * 10 + current_node(2));
        if value.("E") == 1
            child_cell = [current_node(1),current_node(2)+1];
            [open_list, closed_list, g, parents] = child_sub_routine(child_cell, current_node, open_list, closed_list, g, 'W', parents);
            
        end
        if value.("W") == 1
            child_cell = [current_node(1),current_node(2)-1];
            [open_list, closed_list, g, parents] = child_sub_routine(child_cell, current_node, open_list, closed_list, g,'E', parents);
            
        end
        if value.("N") == 1
            child_cell = [current_node(1)-1,current_node(2)];
            [open_list, closed_list, g, parents] = child_sub_routine(child_cell, current_node, open_list, closed_list, g, 'S', parents);
            
        end
        if value.("S") == 1
            child_cell = [current_node(1)+1,current_node(2)];
            [open_list, closed_list, g, parents] = child_sub_routine(child_cell, current_node, open_list, closed_list, g, 'N', parents);
            
        end

        closed_list = [closed_list current_node];

    end
    path = parents;
end
%------------------------------------------------------------------------


%-------------------------Generate Grid-----------------------------------
function grid_map = grid_generate()
    keys = [11,12,13,14,15, ...
            21,22,23,24,25, ...
            31,32,33,34,35, ...
            41,42,43,44,45, ...
            51,52,53,54,55];
    
    % Define the directional values as a cell array of structures
    values = {struct('E',1,'W',0,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',0,'W',1,'N',0,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',0), struct('E',0,'W',0,'N',1,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',1), struct('E',1,'W',0,'N',0,'S',1), struct('E',0,'W',1,'N',1,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',0,'W',1,'N',1,'S',0)};

    % Create the grid map as a cell array
    grid_map = containers.Map(keys, values);

end
%------------------------------------------------------------------------


%--------------------------------Route-----------------------------------

function route_array = route(goal,parents)

target = parents(goal(1),goal(2));
node = goal;
route = goal;
while target ~=0
    if target == "W"
        node = [node(1),node(2)-1];
        target = parents(node(1),node(2));
        route = [route;node];
    end
    if target == "E"
        node = [node(1),node(2)+1];
        target = parents(node(1),node(2));
        route = [route;node];
    end
    if target == "N"
        node = [node(1)-1,node(2)];
        target = parents(node(1),node(2));
        route = [route;node];
    end
    if target == "S"
        node = [node(1)+1,node(2)];
        target = parents(node(1),node(2));
        route = [route;node];
    end 
end
route_array = route;
end
%------------------------------------------------------------------------

