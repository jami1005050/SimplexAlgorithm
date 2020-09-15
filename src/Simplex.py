#Date: 12/08/2019
#Class: CS5310
#Assignment: Simplex Algorithm
#Author(s): Mohammad Jaminur Islam


import math
import sys
class Simplex(object):
    def __init__(self, constraintMatrix, right_side_constant, co_efficient,numberOfRow,numberOfColumn):
        self.constraintMatrix = constraintMatrix  #m*n matrix for coefficient matrix
        self.right_side_constant = right_side_constant # right side constrants list
        self.co_efficient = co_efficient # coefficient list
        self.basic = []
        self.non_basic = []
        self.numberOfRow = numberOfRow #number of basic variable
        self.numberOfColumn = numberOfColumn #number of non basic variable
        self.objectiveValue = 0 #initial objective value setting all non basic to zero

    def simplex_init(self):
        min = sys.maxsize  # define int max as the min value
        minIndex = -1  # initialize
        for i in range(len(self.right_side_constant)):  # for each item of b
            if (self.right_side_constant[i] < min):  # check if it is the minimum
                min = self.right_side_constant[i]
                minIndex = i
        # print("Min :",min)
        if(min>=0): #basic feasible solution
            for j in range(self.numberOfColumn):#number of non basic variable
                self.non_basic.insert(j, j)
            for i in range(self.numberOfRow): #number of constraint or basic variable
                self.basic.insert(i,self.numberOfColumn + i)
            # print("basic: ",self.basic," non basic: ",self.non_basic)
            return 0
        #auxiliary slack

        self.numberOfColumn = self.numberOfColumn +1
        # print("Number of cols: ",self.numberOfColumn )
        for j in range(self.numberOfColumn):
            self.non_basic.insert(j, j)
        for i in range(self.numberOfRow):
            self.basic.insert(i, self.numberOfColumn + i)
        # store the objective function double
        print("Non Basic: ",self.non_basic," Basic:",self.basic)
        co_efficient_old = []
        for j in range(self.numberOfColumn-1):
            # print("self.co_efficient[j]: ",self.co_efficient[j])
            co_efficient_old.insert(j, self.co_efficient[j])
        objectiveValue_old = self.objectiveValue
        print("coefficient old ",co_efficient_old," Objective Value:",self.objectiveValue) #mathced output till now

        # aux.objective function
        self.co_efficient.insert(self.numberOfColumn - 1, -1)
        # print("self.co_efficient[j]: ", self.co_efficient)
        for j in range(self.numberOfColumn-1):
            self.co_efficient[j] = 0
        self.objectiveValue = 0
        print("self.co_efficient[j]: ", self.co_efficient)  #mathced output till now

        #aux.coefficients
        # print("self.constraintMatrix: ",self.constraintMatrix)
        for i in range(self.numberOfRow):
            # print("self.constantMatrix[i]: ",self.constraintMatrix[i])
            self.constraintMatrix[i].insert(self.numberOfColumn - 1,1)
            # self.constraintMatrix[i][self.numberOfColumn - 1] = 1
        print("self.constraintMatrix: ",self.constraintMatrix)

        self.simplex_pivot(minIndex,self.numberOfColumn-1)
        optimal = self.iterate_simplex()
        while (optimal == 0):
            optimal = self.iterate_simplex()
        print("is optimal: ",optimal)
        if (self.objectiveValue != 0) :
            return -1 # infeasible!

        z_basic = -1 ##mathced output till now
        for i in range(self.numberOfRow):
            if (self.basic[i] == self.numberOfColumn - 1):
                z_basic = i
                break

        # if x_n basic, perform one degenerate pivot to make it nonbasic
        if (z_basic != -1):
            self.simplex_pivot(z_basic, self.numberOfColumn - 1)
        z_nonbasic = -1
        for j in range(self.numberOfColumn):
            if (self.non_basic[j] == self.numberOfColumn - 1):
                z_nonbasic = j
                break

        for i in range(self.numberOfRow):
            self.constraintMatrix[i][z_nonbasic] = self.constraintMatrix[i][self.numberOfColumn-1]

        # swap(self.non_basic[z_nonbasic], self.non_basic[self.numberOfColumnn - 1])
        temp = self.non_basic[z_nonbasic]
        self.non_basic[z_nonbasic] = self.non_basic[self.numberOfColumn - 1]
        self.non_basic[self.numberOfColumn - 1] =  temp
        self.numberOfColumn = self.numberOfColumn -1 #mathed
        for j in range(self.numberOfColumn):
            if (self.non_basic[j] > self.numberOfColumn):
                self.non_basic[j] = self.non_basic[j] -1
        for i in range(self.numberOfRow):
            if (self.basic[i] > self.numberOfColumn):
                self.basic[i] = self.basic[i] -1  #mathed


        for j in range(self.numberOfColumn):
            self.co_efficient[j] = 0
        self.objectiveValue = objectiveValue_old
        for j in range(self.numberOfColumn):
            ok = False
            for jj in range(self.numberOfColumn):
                if (j == self.non_basic[jj]):
                    self.co_efficient[jj] = self.co_efficient[jj] + co_efficient_old[j]
                    ok = True
                    break
            if (ok):
                continue
            for  i in range(self.numberOfRow):
                if (j == self.basic[i]):
                    for jj in range(self.numberOfColumn):
                        self.co_efficient[jj] += co_efficient_old[j] * self.constraintMatrix[i][jj]
                    self.objectiveValue += co_efficient_old[j] * self.right_side_constant[i]
                    break

        return 0

    def simplex_pivot(self, x, y):
        #first rearrange  the x - th row
        print("Performing pivoting with x: ",x," y:",y)
        for j in range(self.numberOfColumn):
            if (j != y):
                self.constraintMatrix[x][j] /= -self.constraintMatrix[x][y]
        self.right_side_constant[x] /= -self.constraintMatrix[x][y]
        self.constraintMatrix[x][y] = 1.0 / self.constraintMatrix[x][y]
        # now rearrange the other rows
        for i in range(self.numberOfRow):
            if (i != x):
                for j in range(self.numberOfColumn):
                    if (j != y):
                        self.constraintMatrix[i][j] += self.constraintMatrix[i][y] * self.constraintMatrix[x][j]
                self.right_side_constant[i] += self.constraintMatrix[i][y] * self.right_side_constant[x]
                self.constraintMatrix[i][y] *= self.constraintMatrix[x][y]
        # print("constraint matrix:" ,self.constraintMatrix," right side constant: ",self.right_side_constant)

        #now rearrange the objective function
        for j in range(self.numberOfColumn):
            if (j != y):
                self.co_efficient[j] += self.co_efficient[y] * self.constraintMatrix[x][j]
        self.objectiveValue += self.co_efficient[y] * self.right_side_constant[x]
        self.co_efficient[y] *= self.constraintMatrix[x][y]
            #finally, swap the basic & nonbasic variable
        #swap(self.basic[x], self.non_basic[y]);
        # print("co-efficient length: ",len(self.co_efficient))
        print("constraint matrix:", self.constraintMatrix, " right side constant: ", self.right_side_constant)
        print("coefficient: ",self.co_efficient)
        print("Objective value: ",self.objectiveValue)
        temp = self.basic[x]
        self.basic[x] = self.non_basic[y]
        self.non_basic[y] = temp
        print("After swap Non basic: ",self.non_basic," basic: ",self.basic) #now it is done correctly

    def iterate_simplex(self):
        print("--------------------")
        print("State:\n")
        print("Maximise: ",end=" ")
        for j in range(self.numberOfColumn):
            print(self.co_efficient[j],"x_", self.non_basic[j]," + ", end=" ")
        print(self.objectiveValue,end=" ")
        print("Subject to:")
        for i in range(self.numberOfRow):
            for j in range (self.numberOfColumn):
                print(self.constraintMatrix[i][j], "x_", self.non_basic[j], " + ",end=" ")
            print( self.right_side_constant[i],"= x_", self.basic[i])
        ind = -1
        best_var = -1
        for j in range(self.numberOfColumn):
            if (self.co_efficient[j] > 0):
                if (best_var == -1 or self.non_basic[j] < ind):
                    ind = self.non_basic[j]
                    best_var = j
        print("best_var: ",best_var," ind: ",ind)
        if (ind == -1):
            return 1
        max_constr = math.inf
        best_constr = -1
        for i in range(self.numberOfRow):
            # print("self.constraintMatrix[i][best_var]: ",self.constraintMatrix[i][best_var])
            if (self.constraintMatrix[i][best_var] < 0):
                curr_constr = -self.right_side_constant[i] / self.constraintMatrix[i][best_var]
                # print("curr_constr: ",curr_constr)
                if (curr_constr < max_constr):
                    max_constr = curr_constr
                    best_constr = i
        # print("max_constr:" ,max_constr," best_constr: ",best_constr)

        if (math.isinf(max_constr)):
            return -1
        else:
            self.simplex_pivot(best_constr, best_var)
        return 0

    def simplex_main(self):
        feasible = self.simplex_init()
        if (feasible == -1):
            return -1
        code = self.iterate_simplex()
        while (code == 0):
            code = self.iterate_simplex()

        if (code == -1):
            return -1
        result = []
        for j in range(self.numberOfColumn):
            result.insert(self.non_basic[j], 0)
        for i in range(self.numberOfRow):
            result.insert(self.basic[i], self.right_side_constant[i])

        print("result: ",result," objective value: ",self.objectiveValue)
        return 1

if __name__ == '__main__':
    # Basic solution  feasible:
    # numberOfCols = 2
    # numberOfRows = 2
    # constantMatrix = [[0 for i in range(2)] for j in range(2)]
    #
    # constantMatrix[0][0] = -1
    # constantMatrix[0][1] = 1
    # constantMatrix[1][0] = -2
    # constantMatrix[1][1] = -1
    # right_side_constants = [0 for i in range(2)]
    # right_side_constants[0] = 1
    # right_side_constants[1] = 2
    # co_efficient = [0 for i in range(2)]
    # co_efficient[0] = 5
    # co_efficient[1] = -3

    #Basic solution infeasible
    numberOfCols = 2
    numberOfRows = 3
    constantMatrix = [[0 for i in range(2)] for j in range(3)]

    constantMatrix[0][0] = -1
    constantMatrix[0][1] = 1
    constantMatrix[1][0] = 1
    constantMatrix[1][1] = 1
    constantMatrix[2][0] = 1
    constantMatrix[2][1] = -4
    right_side_constants = [0 for i in range(3)]
    right_side_constants[0] = 8
    right_side_constants[1] = -3
    right_side_constants[2] = 2

    co_efficient = [0 for i in range(2)]
    co_efficient[0] = 1
    co_efficient[1] = 3
    simplex = Simplex(constantMatrix,right_side_constants,co_efficient,numberOfRows,numberOfCols)
    ret = simplex.simplex_main()
    print("it is working and returned: ",ret)
