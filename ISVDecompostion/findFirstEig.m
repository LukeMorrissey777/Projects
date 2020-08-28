function [E] = findFirstEig(A)
%finds first eigenvector
tol = 1e-10;
uold = rand(1440,1);
uold = uold/norm(uold);
unew = A'*A*uold;
while norm(unew-uold) > tol
    uold = unew;
    unew = A'*A*unew/norm(A'*A*unew);
end
E = unew;
end

