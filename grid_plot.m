function grid_plot(route,targetPoint,startPoint)

% Define the values
    values = {struct('E',1,'W',0,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',1,'W',1,'N',0,'S',1), struct('E',0,'W',1,'N',0,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',0), struct('E',0,'W',0,'N',1,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',1), struct('E',1,'W',1,'N',1,'S',1), struct('E',0,'W',1,'N',1,'S',1), struct('E',1,'W',0,'N',0,'S',1), struct('E',0,'W',1,'N',1,'S',1), ...
            struct('E',1,'W',0,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',1,'W',1,'N',1,'S',0), struct('E',0,'W',1,'N',1,'S',0)};
    
% Plot the grid
figure;
hold on;
for i = 1:5
    for j = 1:5
        % Extract the value for the current square
        square = values{(i - 1) * 5 + j};
        
        % Calculate the coordinates of the square's corners
        x = [j-0.5, j+0.5, j+0.5, j-0.5, j-0.5];
        y = [(6-i)+0.5, (6-i)+0.5, (6-i)-0.5, (6-i)-0.5, (6-i)+0.5];
        
        %Draw impassable sides as bold
        if ~square.E
            plot([j+0.5, j+0.5], [(6-i)-0.5, (6-i)+0.5], 'k', 'LineWidth', 3);
        end
        if ~square.W
            plot([j-0.5, j-0.5], [(6-i)-0.5, (6-i)+0.5], 'k', 'LineWidth', 3);
        end
        if ~square.N
            plot([j-0.5, j+0.5], [(6-i)+0.5, (6-i)+0.5], 'k', 'LineWidth', 3);
        end
        if ~square.S
            plot([j-0.5, j+0.5], [(6-i)-0.5,(6-i)-0.5], 'k', 'LineWidth', 3);
        end
        
        plot( route(:, 2),(6-route(:, 1)), 'ro', 'MarkerSize', 10);
        
        % Fill the square with appropriate color
        if isequal(startPoint, [i, j])
            fill(x, y, 'r','FaceAlpha',0.2);
        elseif isequal(targetPoint, [i,j])
            fill(x, y, 'g','FaceAlpha',0.2);
        else
            fill(x, y, 'w');
        end
    end
end

% Set axis limits and labels, and aspect ratio
axis([0, 6, 0, 6]);
yticklabels({'6','5','4','3','2','1','0'});
xlabel('S');
ylabel('W');
title('A* Algorithm');
axis equal;  % Set aspect ratio to equal

hold off;
end