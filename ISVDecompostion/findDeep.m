function [P] = findDeep(long,lat,A)
%goes through all points and finds min
o = 0;
a = 0;
min = 0;
for i = 1:1320
    for j = 1:1440
        if A(i,j) < min
            min = A(i,j);
            o = i;
            a = j;
        end
    end
end
P = [long(o),lat(a),min];

end

