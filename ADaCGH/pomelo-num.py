#!/usr/bin/python2.4

""" Compare output from Pomelo II with output from analyses done in R.
These tests carry out a fairly comprehensive set of tests of all the
functionality available in Pomelo II.
These tests differ from those of testPomelo.py in that they focus
only on the numerical aspect. We try to get to the output and results,
and thus we use funkload after hacking a little bit of it.

You can expect warnings from R for some of the p-value testing
(small cell counts for some proportion comparisons)."""



import sys
import os
import time

## sys.path = [] + sys.path

import flstandalone
import rpy

FILES_DIR = './DataSets_R_Analyses/'


class AsteriasAssertionError(AssertionError):
    """Comparison between reference and observed failed."""

## zz: define the right exception class here. AsteriasAssertExcept
##and then substitute all print "**###@@@@!!!!!   Test failed       !!!!!@@@@###**"
##with raise(AsteriasAssertExcept)

## zz: how do I use several distinct R sessions? Nope: just do an rm


def verify_Cox(data_name):
    ''' Launch Cox in PomeloII, get results, and verify against R.'''
    print '\n\n\n******* Verifying Cox results for data set ' + data_name + '\n'
    coxConnect = flstandalone.NumTesting()
    coxConnect.setUp('http://pomelo2.bioinfo.cnio.es')
    coxConnect.send_get_pomelo(FILES_DIR + data_name + '.covar.txt',
                              FILES_DIR + data_name + '.surv.txt',
                              FILES_DIR + data_name + '.event.txt',
                              'Cox', '2')
    r_read = data_name + 'Pomelo <- readPomeloOutput()'
    r_compare = 'comparePomelo(' + data_name + 'Pomelo, ' + \
                     data_name + '.results)'
    ## r_read and r_compare are so that we can
    ## send to R the following two types of instructions
    ## rpy.r('breastPomelo <- readPomeloOutput()')
    ## rpy.r('comparePomelo(breastPomelo, breast.results)')
    rpy.r(r_read)
    out_comparison = rpy.r(r_compare)
    if (out_comparison == 'ERROR: test failed'):
        raise AsteriasAssertionError
    

def verify_Permut(data_name, test, permuts = '200000'):
    '''Verify PomeloII permutation-based tests against R.
    @param test: the type of test, one of t, Anova, Regres. '''
    compare_p_values = 1 ## this is legacy stuff
    accepted_tests = ('t', 'Anova', 'Regres') 
    if test not in accepted_tests:
        print "Invalid test specificed which should be one of " + \
              accepted_tests
    print '\n\n\n******* Verifying test ' + test + ' for data set ' + \
          data_name + "\n"
    pConnect = flstandalone.NumTesting()
    pConnect.setUp('http://pomelo2.bioinfo.cnio.es')
    pConnect.send_get_pomelo(Covar = FILES_DIR + data_name + '.covar.txt'\
                             ,Class = FILES_DIR + data_name + '.class.txt'\
                             ,Status = FILES_DIR + 'empty.txt'\
                             ,Test_type = test, Num_permut = permuts)
    r_read = data_name + 'Pomelo <- readPomeloOutput()'
    r_compare = 'comparePermutPomelo(' + data_name + 'Pomelo, ' + \
                     data_name + '.' + test + \
                     ', compare.p.values = ' + str(compare_p_values) +')'
    rpy.r(r_read)
    out_comparison = rpy.r(r_compare)
    if (out_comparison == 'ERROR: test failed'):
        raise AsteriasAssertionError

def verify_Limma(data_name, test, other_covars = None, tol = 0.02):
    '''Verify PomeloII limma-based tests against R.
    @param test: the type of test
    '''
    compare_p_values = 1 ## legacy stuff again
    accepted_tests = ('Anova_limma', 't_limma', 't_limma_paired') 
    if test not in accepted_tests:
        print "Invalid test specificed which should be one of " + \
              accepted_tests
         
    print '\n\n\n******* Verifying test ' + test + ' for data set ' + \
          data_name + "\n"
    pConnect = flstandalone.NumTesting()
    pConnect.setUp('http://pomelo2.bioinfo.cnio.es')
    if (test == 't_limma'):
        pConnect.send_get_pomelo(FILES_DIR + data_name + '.covar.txt',
                                 FILES_DIR + data_name + '.class.txt',
                                 FILES_DIR + 'empty.txt',
                                 test, '2')
    elif (test == 't_limma_paired'):
        pConnect.send_get_pomelo(FILES_DIR + data_name + '.covar.txt',
                                 FILES_DIR + data_name + '.class.txt',
                                 FILES_DIR + 'empty.txt',
                                 test, '2',
                                 paired_indicator = FILES_DIR + data_name + \
                                 '.pairs.txt')
    elif (test == 'Anova_limma'):
        if other_covars:
            other_covars = FILES_DIR + other_covars
        else:
            other_covars = None
        pConnect.send_get_pomelo(FILES_DIR + data_name + '.covar.txt',
                                 FILES_DIR + data_name + '.class.txt',
                                 FILES_DIR + 'empty.txt',
                                 test, '2',
                                 paired_indicator = None,
                                 other_covars = other_covars)    
    if not (test == 'Anova_limma'):
        r_read = data_name + 'Pomelo <- readPomeloOutput()'
        r_compare = 'comparePomeloLimma(' + data_name + 'Pomelo, ' + \
                    data_name + '.' + test + ', tol = ' + str(tol) + ')'
        rpy.r(r_read)
        out_comparison = rpy.r(r_compare)
        if (out_comparison == 'ERROR: test failed'):
            raise AsteriasAssertionError
      
    else: ## anovas; compare coefs; FIXME: parameterize
        r_read = 'cl0cl1 <- readPomeloOutput("./tmp-files/class0-class1.txt"); \
        cl0cl2 <- readPomeloOutput("./tmp-files/class0-class2.txt");\
        cl1cl2 <- readPomeloOutput("./tmp-files/class1-class2.txt")'
        garbage = rpy.r(r_read)
        ## FIXME: the contrasts names should be passed
        ## and we might need to change their names in the DataSets_R_Analyses
    
        if other_covars:
            print '\n\n\n\n---- Contrasts comparisons: cl0 vs cl1'
            out_comparison = rpy.r('comparePomeloLimma(cl0cl1, t1.breast.cov)')
            if (out_comparison == 'ERROR: test failed'):
                raise AsteriasAssertionError
            print '\n\n\n\n---- Contrasts comparisons: cl0 vs cl2'
            out_comparison = rpy.r('comparePomeloLimma(cl0cl2, t2.breast.cov)')
            if (out_comparison == 'ERROR: test failed'):
                raise AsteriasAssertionError
            print '\n\n\n\n---- Contrasts comparisons: cl1 vs cl2'
            out_comparison = rpy.r('comparePomeloLimma(cl1cl2, t3.breast.cov)')
            if (out_comparison == 'ERROR: test failed'):
                raise AsteriasAssertionError
        else:
            print '\n\n\n\n---- Contrasts comparisons: cl0 vs cl1'
            out_comparison = rpy.r('comparePomeloLimma(cl0cl1, t1.breast)')
            if (out_comparison == 'ERROR: test failed'):
                raise AsteriasAssertionError
            print '\n\n\n\n---- Contrasts comparisons: cl0 vs cl2'
            out_comparison = rpy.r('comparePomeloLimma(cl0cl2, t2.breast)')
            if (out_comparison == 'ERROR: test failed'):
                raise AsteriasAssertionError
            print '\n\n\n\n---- Contrasts comparisons: cl1 vs cl2'
            out_comparison = rpy.r('comparePomeloLimma(cl1cl2, t3.breast)')
            if (out_comparison == 'ERROR: test failed'):
                raise AsteriasAssertionError


def verify_FishersExact(data_name):
    """ Verify output from Fishers' Exact test for IxJ contingency tables."""
    print "\n\n\n******* Verifying Fisher's test results \n"
    rpy.r('load("' + FILES_DIR + 'fisher.verified.RData")')
    fisherConnect = flstandalone.NumTesting()
    fisherConnect.setUp('http://pomelo2.bioinfo.cnio.es')
    fisherConnect.send_get_pomelo(FILES_DIR + data_name + '.data.txt',
                                  FILES_DIR + data_name + '.labels.txt',
                                  FILES_DIR + 'empty.txt',
                                  'FisherIxJ', '2')
    ## time.sleep(50)
    r_read = 'fisherPomelo <- readPomeloOutput()'
    r_compare = 'comparePomelo(fisherPomelo, fisher.pv, fisher = TRUE)'
    rpy.r(r_read)
    out_comparison = rpy.r(r_compare)
    if (out_comparison == 'ERROR: test failed'):
        raise AsteriasAssertionError

    
def verify_Pomelo(test, data = None, **keypar):
    """ Generic wrapper to test numerical output of Pomelo II."""
    ## Try to get a clean R
    rpy.r('rm(list = ls())')
    rpy.r.source('pomelo_testing_util.R')

    if test == 'Fisher':
        rpy.r('load("' + FILES_DIR + 'fisher.verified.RData")')
        verify_FishersExact('fisher')
    elif test == 'Cox':
        rpy.r('load("' + FILES_DIR + 'cox.verified.RData")')
        data_sets = ('aml', 'dlbcl', 'breast')
        for data_set in data_sets:
            verify_Cox(data_name = data_set)
    elif test in ('t', 'Anova', 'Regres'):
        rpy.r('load("' + FILES_DIR + 'permutations.verified.RData")')
        verify_Permut(data_name = data, test = test,
                      **keypar)
    elif test in ('t_limma', 't_limma_paired', 'Anova_limma'):
        rpy.r('load("' + FILES_DIR + 'Limma.verified.RData")')
        verify_Limma(data_name = data, test = test,
                      **keypar)
    else:
        raise Exception, 'This test not implemented'
    



# def verify_Pomelo_nr(test, data = None, numtries = 3, **keypar):
#     """A wrapper to verify_Pomelo that keeps trying when there are network
#     problems. No longer used."""
#     tried = 0
#     network_problem = True
#     while network_problem and (tried < numtries):
#         try:
#             verify_Pomelo(test, data = data, **keypar)
# #         except socket.error:
# #             print 'Caught a socket.error'
# #             tried += 1
#         except AssertionError:
#             print 'Caught a AssertionError, hopefully just a Proxy Error'
#             tried += 1
#         except IOError:
#             print 'Caught an IOError, hopefully just a connection time out'
#             tried += 1
#         else:
#             network_problem = False
#             break
        
        

################################################################

####           Start execution   


verify_Pomelo('Fisher')
verify_Pomelo('Cox')

## Permutation-based tests
verify_Pomelo('t', 'leukemia')
verify_Pomelo('t', 'colon')
verify_Pomelo('Anova', 'breast.3.class')
verify_Pomelo('Anova', 'srbct')
verify_Pomelo('Anova', 'brain')

## We use only a few permutations, because the R version is very slow,
## and we have used only 1000 permuts there.
verify_Pomelo('Regres', 'aml.small', permuts = '2100')


## limma
verify_Pomelo('t_limma', 'leukemia')
verify_Pomelo('t_limma_paired', 'leukemia.paired')
verify_Pomelo('Anova_limma', 'breast.3.class')
verify_Pomelo('Anova_limma', 'breast.3.class',
             other_covars = 'covs.breast.txt')





