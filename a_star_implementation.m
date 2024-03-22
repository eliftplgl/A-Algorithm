area_size = 5;
start = [1,1]; 
goal = [4,4];
astar(area_size,start,goal)
bold_sides = zeros(area_size + 1, area_size+1); % Initialize all sides to be regular
bold_sides(4, 4) = 1;% Make the side between (2, 3) and (2, 4) bold
grid_plot(area_size,bold_sides);


%----------------------Get List Value------------------------------------
function val = get_i(list, i) % get the values of the ith element
    val = [list((i - 1) * 2 + 1) list((i- 1) * 2 + 2)];
end
%------------------------------------------------------------------------


%----------------------Delete List Value---------------------------------
function list = del_i(list, i)
    list((i-1) * 2 + 1) = [];
    list((i-1) * 2 + 1) = []; % delete the ith element twice (priority queue)
end
%------------------------------------------------------------------------


%-----------------------Check Smt is in List-----------------------------
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
    g(start)=0;

    %f = zeros(size(area));
    %f(:,:) = inf;
    %f(start)=h(start,goal)+g(start);
    
    open_list = [];
    open_list = [open_list start];
    closed_list = [];

    parents = char(zeros(size(area)));

    while numel(open_list) > 0
        [current_node, open_list] = find_smallest_f(open_list, goal, g, h);   % we exclude the start node from the list
        if current_node == goal
            break 
        end

        
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
                child_cell = [current_node(1)+1,current_node(2)];
                [open_list, closed_list, g, parents] = child_sub_routine(child_cell, current_node, open_list, closed_list, g, 'S', parents);
                
            end
            if value.("S") == 1
                child_cell = [current_node(1)-1,current_node(2)];
                [open_list, closed_list, g, parents] = child_sub_routine(child_cell, current_node, open_list, closed_list, g, 'N', parents);
                
            end

        
        closed_list = [closed_list current_node];


        
    end
    path = parents;
end


function grid_map = grid_generate()
    keys = [11,12,13,14,15, ...
            21,22,23,24,25, ...
            31,32,33,34,35, ...
            41,42,43,44,45, ...
            51,52,53,54,55];
    
    % Define the directional values as a cell array of structures
    values = {struct('E',1,'W',0,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',0,'W',1,'N',1,'S',0), ...
              struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',1), ...
              struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',0,'S',1), struct('E',0,'W',0,'N',1,'S',1), ...
              struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',1), struct('E',1,'W',0,'N',1,'S',0), struct('E',0,'W',1,'N',1,'S',1), ...
              struct('E',1,'W',0,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',0,'W',1,'N',0,'S',1)};
    
    % Create the grid map as a cell array
    grid_map = containers.Map(keys, values);

end





function grid_plot(area_size, bold_sides)
    % Create a grid of size area_size x area_size
    
    % Plot the grid
    figure;
    hold on;
    xlim([0, area_size + 1]);
    ylim([0, area_size + 1]);
    grid on;
    axis equal;
    xlabel('Column');
    ylabel('Row');
    title(sprintf('%dx%d Grid', area_size, area_size));
    
    % Plot horizontal lines with bold sides
    for i = 1:area_size+1
        for j = 1:area_size
            if bold_sides(i, j) == 1
                plot([j-0.5, j+0.5], [i-0.5, i-0.5], 'k', 'LineWidth', 2); % Bold horizontal line
            else
                plot([j-0.5, j+0.5], [i-0.5, i-0.5], 'k'); % Regular horizontal line
            end
        end
    end
    
    % Plot vertical lines with bold sides
    for i = 1:area_size+1
        for j = 1:area_size
            if bold_sides(j, i) == 1
                plot([i-0.5, i-0.5], [j-0.5, j+0.5], 'k', 'LineWidth', 2); % Bold vertical line
            else
                plot([i-0.5, i-0.5], [j-0.5, j+0.5], 'k'); % Regular vertical line
            end
        end
    end
    plot([4.5, 4.5], [2.5, 3.5], 'k', 'LineWidth', 2); % Bold vertical line
end
