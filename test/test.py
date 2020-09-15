#Date: 12/08/2019
#Class: CS5310
#Assignment: Simplex Algorithm
#Author(s): Mohammad Jaminur Islam


import unittest

from src.Simplex import Simplex


class MyTestCase(unittest.TestCase):
    def test_simplex_feasible_solution(self):
        # Basic solution  feasible:
        numberOfCols = 2  #number of intial variables
        numberOfRows = 2 # number of constraints
        constantMatrix = [[0 for i in range(numberOfCols)] for j in range(numberOfRows)] #initialization

        constantMatrix[0][0] = -1  #coefficients from the constraints
        constantMatrix[0][1] = 1
        constantMatrix[1][0] = -2
        constantMatrix[1][1] = -1
        right_side_constants = [0 for i in range(numberOfRows)]
        right_side_constants[0] = 1 #right side values
        right_side_constants[1] = 2
        co_efficient = [0 for i in range(numberOfCols)]
        co_efficient[0] = 5 #coefficients for the objective function
        co_efficient[1] = -3
        simplex = Simplex(constantMatrix, right_side_constants, co_efficient, numberOfRows, numberOfCols) #initialize simplex
        assert isinstance(simplex,Simplex)
        ret = simplex.simplex_main()  #simplex check


    def test_simplex_infeasible_solution(self):
        # Basic solution infeasible
        numberOfCols = 2  #number of initial variables
        numberOfRows = 3
        constantMatrix = [[0 for i in range(numberOfCols)] for j in range(numberOfRows)] #constraint matrix initalization

        constantMatrix[0][0] = -1 #set values for contraint matrix
        constantMatrix[0][1] = 1
        constantMatrix[1][0] = 1
        constantMatrix[1][1] = 1
        constantMatrix[2][0] = 1
        constantMatrix[2][1] = -4
        right_side_constants = [0 for i in range(numberOfRows)] #right side constants
        right_side_constants[0] = 8
        right_side_constants[1] = -3
        right_side_constants[2] = 2

        co_efficient = [0 for i in range(numberOfCols)] #coefficient for objective function
        co_efficient[0] = 1
        co_efficient[1] = 3
        simplex = Simplex(constantMatrix, right_side_constants, co_efficient, numberOfRows, numberOfCols) #simplex initialization
        assert isinstance(simplex, Simplex)
        ret = simplex.simplex_main() #simplex return

if __name__ == '__main__':
    unittest.main()
