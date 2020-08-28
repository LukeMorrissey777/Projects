function [E] = findEigValues(V,A)
%finds all the eigenvalues
E = zeros(100,1);
av = A*V;
for i = 1:100
    E(i) = av(100,i)/V(100,i);
end
end

