%load('data/SOC_0%-60%_HalfC/PL03.mat')

dataset = zeros(50*25,8);

%rows: day[1] charge_rate[2] discharge_rate[3] lowSOC[4] highSOC[5] cyclenum[6] Cap%[7]
%days = [1 21 36 55 90 104

%
tic
idx0 = 1;
idx1 = 1;
cycle = 1;
for jj = [3:15 19:25]
    
    data2 = PL03{jj,3};
    idxs = find(data2{2:end,4} - data2{1:end-1,4} == 1);
    cap = zeros(size(idxs));
    for ii = 1:length(idxs)
        cap(ii) = data2{idxs(ii),8};
        
    end
    cap2 = diff(cap);
    dataset(idx1:idx1+length(cap2)-1,1) = day(datetime(PL03{jj,2}) - datetime(PL03{2,2})); %fix year thing
    dataset(idx1:idx1+length(cap2)-1,2) = 0.5; %always
    dataset(idx1:idx1+length(cap2)-1,3) = 0.5;
    dataset(idx1:idx1+length(cap2)-1,4) = 0;
    dataset(idx1:idx1+length(cap2)-1,5) = 60;
    dataset(idx1:idx1+length(cap2)-1,6) = cycle:cycle+length(cap2)-1;
    dataset(idx1:idx1+length(cap2)-1,7) = cap2/cap2(idx0);
    idx1 = idx1 + length(cap2)-1;
    cycle = cycle + length(cap2)-1;
    %delete outliers
    
    %days = day(datetime(PL03{jj,2}) - datetime(PL03{2,2}));
end  
toc

data2 = PL03{3,3};