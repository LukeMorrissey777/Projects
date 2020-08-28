function [O] = ISVD(x,V,eigValues,A)
%Does all the ISVD stuff
sigma = eye(x);
for i = 1:x
    sigma(i,i) = eigValues(i)^(1/2);
end
Vnew = V(:,1:x);
U = A*Vnew;
for i = 1:x
    U(:,i) = U(:,i)/sigma(i,i);
end
O = U*sigma*Vnew';

end

