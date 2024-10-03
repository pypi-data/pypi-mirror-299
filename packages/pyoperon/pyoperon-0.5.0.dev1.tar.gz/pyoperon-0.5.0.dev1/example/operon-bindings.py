# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2019-2022 Heal Research

import random, time, sys, os, json
import numpy as np
import pandas as pd
from scipy import stats

import pyoperon as Operon


if __name__ == '__main__':
    D = pd.read_csv('./datasets/1027_ESL/1027_ESL.tsv.gz', sep='\t').to_numpy()
    X, y = D[:,:-1], D[:,-1]

    # initialize a dataset from a numpy array
    print(X.shape, y.shape)
    A = np.column_stack((X, y))
    ds             = Operon.Dataset(np.asfortranarray(A))

    # define the training and test ranges
    training_range = Operon.Range(0, ds.Rows // 2)
    test_range     = Operon.Range(ds.Rows // 2, ds.Rows)

    # define the regression target
    target         = ds.Variables[-1] # take the last column in the dataset as the target

    # take all other variables as inputs
    inputs         = [ h for h in ds.VariableHashes if h != target.Hash ]

    # initialize a rng
    rng            = Operon.RomuTrio(random.randint(1, 1000000))

    # initialize a problem object which encapsulates the data, input, target and training/test ranges
    problem        = Operon.Problem(ds)
    problem.TrainingRange = training_range
    problem.TestRange = test_range
    problem.Target = target
    problem.InputHashes = inputs

    # initialize an algorithm configuration
    config         = Operon.GeneticAlgorithmConfig(generations=1000, max_evaluations=1000000, local_iterations=1, population_size=1000, pool_size=1000, p_crossover=1.0, p_mutation=0.25, epsilon=1e-5, seed=1, max_time=86400)

    # use tournament selection with a group size of 5
    # we are doing single-objective optimization so the objective index is 0
    selector       = Operon.TournamentSelector(objective_index=0)
    selector.TournamentSize = 5

    # initialize the primitive set (add, sub, mul, div, exp, log, sin, cos), constants and variables are implicitly added
    problem.ConfigurePrimitiveSet(Operon.NodeType.Constant | Operon.NodeType.Variable | Operon.NodeType.Add | Operon.NodeType.Mul | Operon.NodeType.Div | Operon.NodeType.Exp | Operon.NodeType.Log | Operon.NodeType.Sin | Operon.NodeType.Cos)
    pset = problem.PrimitiveSet

    # define tree length and depth limits
    minL, maxL     = 1, 50
    maxD           = 10

    # define a tree creator (responsible for producing trees of given lengths)
    btc            = Operon.BalancedTreeCreator(pset, problem.InputHashes, bias=0.0)
    tree_initializer = Operon.UniformLengthTreeInitializer(btc)
    tree_initializer.ParameterizeDistribution(minL, maxL)
    tree_initializer.MaxDepth = maxD

    # define a coefficient initializer (this will initialize the coefficients in the tree)
    coeff_initializer = Operon.NormalCoefficientInitializer()
    coeff_initializer.ParameterizeDistribution(0, 1)

    # define several kinds of mutation
    mut_onepoint   = Operon.NormalOnePointMutation()
    mut_changeVar  = Operon.ChangeVariableMutation(inputs)
    mut_changeFunc = Operon.ChangeFunctionMutation(pset)
    mut_replace    = Operon.ReplaceSubtreeMutation(btc, coeff_initializer, maxD, maxL)

    # use a multi-mutation operator to apply them at random
    mutation       = Operon.MultiMutation()
    mutation.Add(mut_onepoint, 1)
    mutation.Add(mut_changeVar, 1)
    mutation.Add(mut_changeFunc, 1)
    mutation.Add(mut_replace, 1)

    # define crossover
    crossover_internal_probability = 0.9 # probability to pick an internal node as a cut point
    crossover      = Operon.SubtreeCrossover(crossover_internal_probability, maxD, maxL)

    # define fitness evaluation
    dtable         = Operon.DispatchTable()
    error_metric   = Operon.R2()          # use the coefficient of determination as fitness
    evaluator      = Operon.Evaluator(problem, dtable, error_metric, True) # initialize evaluator, use linear scaling = True
    evaluator.Budget = config.Evaluations # computational budget

    optimizer      = Operon.LMOptimizer(dtable, problem, max_iter=config.Iterations)
    local_search   = Operon.CoefficientOptimizer(optimizer)

    # define how new offspring are created
    generator      = Operon.BasicOffspringGenerator(evaluator, crossover, mutation, selector, selector, local_search)

    # define how the offspring are merged back into the population - here we replace the worst parents with the best offspring
    reinserter     = Operon.ReplaceWorstReinserter(objective_index=0)
    gp             = Operon.GeneticProgrammingAlgorithm(config, problem, tree_initializer, coeff_initializer, generator, reinserter)

    # report some progress
    gen = 0
    max_ticks = 50
    interval = 1 if config.Generations < max_ticks else int(np.round(config.Generations / max_ticks, 0))
    t0 = time.time()

    def report():
        global gen
        best = gp.BestModel
        bestfit = best.GetFitness(0)
        sys.stdout.write('\r')
        cursor = int(np.round(evaluator.TotalEvaluations/config.Evaluations * max_ticks))
        for i in range(cursor):
            sys.stdout.write('\u2588')
        sys.stdout.write(' ' * (max_ticks-cursor))
        sys.stdout.write(f'{100 * evaluator.TotalEvaluations/config.Evaluations:.1f}%, generation {gen}/{config.Generations}, train quality: {-bestfit:.6f}, elapsed: {time.time()-t0:.2f}s')
        sys.stdout.flush()
        gen += 1


    # run the algorithm
    gp.Run(rng, report, threads=16)

    # get the best solution and print it
    best = gp.BestModel
    model_string = Operon.InfixFormatter.Format(best.Genotype, ds, 6)
    fit = evaluator(rng, gp.BestModel)
    print('Time limit:', config.TimeLimit)
    print('gen=', gp.Generation, '\nfit=', fit)
    print(f'\n{model_string}')
