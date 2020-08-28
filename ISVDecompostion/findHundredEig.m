function [V] = findHundredEig(A)
%finds first 100 eigenvectors
V = zeros(1440,100);
for i = 1:100
    uold = rand(1440,1);
    uold = uold/norm(uold);
    unew = A*uold;
    unew = unew/norm(unew);
    while norm(uold-unew) > 1e-3
        uold = unew;
        unew = A*uold;
        for j = 1:(i-1)
            unew = unew - (unew'*V(:,j))*V(:,j);
        end
        unew = unew/norm(unew);
    end
    V(:,i) = unew;
end
end

