function findDuplicatedRxns(model)
% findDuplicatedRxns
%   Find and print reactions that have the same stoichiometry (forwards or
%   backwards).
%
%   Input:
%   model   genome-scale model
%
%   Usage: findDuplicatedRxns(model)
%

for i = 1:length(model.rxns)-1
    for j = i+1:length(model.rxns)
        if isequal(model.S(:,i),model.S(:,j)) || isequal(model.S(:,i),-model.S(:,j))
            constructEquations(model,model.rxns(i));
            disp(['Name: ' model.rxnNames{i} ' - GPR: ' model.grRules{i} ' - LB=' num2str(model.lb(i)) ' - UB=' num2str(model.ub(i))])
            constructEquations(model,model.rxns(j));
            disp(['Name: ' model.rxnNames{j} ' - GPR: ' model.grRules{j} ' - LB=' num2str(model.lb(j)) ' - UB=' num2str(model.ub(j))])
            disp(" ")
        end
    end
end
end
