function [x] = findAvg(A)
%goes through all points and it they are less than 6000 finds the average
count = 0;
tot = 0;
for i = 1:1320
    for j = 1:1440
        if A(i,j) < -6000
            count = count + 1;
            tot = tot + A(i,j);
        end
    end
end

x = tot/count;
end

