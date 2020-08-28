%Imports the Data
A = importdata('mariana_depth.csv');
lon = importdata('mariana_longitude.csv');
lat = importdata('mariana_latitude.csv');

%Makes new matrices that are the same size as A with lat and lon
latTot = zeros(1320,1440);
lonTot = zeros(1320,1440);

for i = 1:1320
    latTot(i,:) = lat';
end
for i = 1:1440
    lonTot(:,i) = lon;
end


%Makes first figure
f1 = figure(1);  
contour(latTot,lonTot,A);
colorbar;
title('Depth of the Mariana Trench in Meters');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f1,'211.png');



%finds deepest and average depth
deep = findDeep(lon,lat,A)
avg = findAvg(A)


%finds first eigenvector
eig = findFirstEig(A);

%makes A'A and multiplies it by the eigenvector
AtA = A'*A;
AtE = AtA*eig; 

%Finds eigenvalue by definition of eigen value
a = AtE(879,1)/eig(879,1)

b = AtE(538,1)/eig(538,1)


%plots first eigenvector
N = 1:1440;
N = N';
f2 = figure(2);
plot(N,eig);
title('$\vec{V}_1$','Interpreter','latex');
xlabel('Element');
ylabel('Element Value');
saveas(f2,'221.png');



%finds first 50 eigenvectors and stores them in matrix V
V = findHundredEig(AtA);
%finds eigenvalue of each eigenvector and stores it in vector eigValues
eigValues = findEigValues(V,AtA);

%Plots the first 50 eigen values on semilog plot
count = 1:50;
count = count';
f3 = figure(3);
semilogy(count,eigValues(1:50));
title('First 50 Eigenvalues');
xlabel('Eigenvector');
ylabel('Eigenvalue');
saveas(f3,'222.png');


%finds the total for A and the total for USV
totalA = 1320*1440
totalUSV = 1320*50 + 50 +1440*50

%computes USV'
USV50 = ISVD(50,V,eigValues,A);

%Plots USV'
f4 = figure(4);
contour(latTot,lonTot,USV50);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=50)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f4,'233.png');


%same as above but uses k=40
USV40 = ISVD(40,V,eigValues,A);
f5 = figure(5);
contour(latTot,lonTot,USV40);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=40)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f5,'ISVD40.png');

%same as above but k=30
USV30 = ISVD(30,V,eigValues,A);
f6 = figure(6);
contour(latTot,lonTot,USV30);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=30)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f6,'ISVD30.png');

%same as above but k = 20
USV20 = ISVD(20,V,eigValues,A);
f7 = figure(7);
contour(latTot,lonTot,USV20);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=20)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f7,'ISVD20.png');

%same as above but k = 10
USV10 = ISVD(10,V,eigValues,A);
f8 = figure(8);
contour(latTot,lonTot,USV10);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=10)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f8,'ISVD10.png');

%same as above but k = 5
USV5 = ISVD(5,V,eigValues,A);
f10 = figure(10);
contour(latTot,lonTot,USV5);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=5)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f10,'ISVD10.png');

%same as above but k=100
USV100 = ISVD(100,V,eigValues,A);
f9 = figure(9);
contour(latTot,lonTot,USV100);
colorbar;
title('Depth of the Mariana Trench in Meters Using ISVD(k=100)');
xlabel('Latitude ({\circ}N)');
ylabel('Longitude ({\circ}E)');
saveas(f9,'ISVD100.png');




















