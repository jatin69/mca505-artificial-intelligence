class GeneticNQueen:

    def __init__(self,n):
        """
        Constructor : initialises all the required member functions
        """

        # size of board
        self.boardSize = n

        # a chess board of size NxN
        self.board = [[0 for j in range(n)] for i in range(n)]
        
        # population for genetic algo
        self.population = []
        
        # a solution for N queens
        self.solutionChromosome = []

        # maximum generations allowed
        self.MAX_GENERATIONS_ALLOWED = 100

        # what percentage of chromosomes should be mutated
        self.MUTATION_RATE_FOR_POPULATION = 1
        self.MUTATION_RATE_FOR_CHROMOSOME = 0.2     # more or less unused for now
        self.fittestYet = 1000

        # for now
        self.NO_OF_WINNERS = self.boardSize

    def initializePopulation(self):
        """
        initialises population
        """
        def factorial(n):
            fact = 1
            for i in range(2, self.boardSize+1):
                fact *= i
            return fact

        populationSize = 0
        if self.boardSize < 6:
            # populationSize = factorial(self.boardSize)
            populationSize = 100
        else:
            populationSize = 500

        def generateChromosome():
            from random import shuffle
            chromosome = list(range(self.boardSize))
            shuffle(chromosome)
            while chromosome in self.population:
                shuffle(chromosome)
            return chromosome

        for _ in range(populationSize):
            self.population.append(generateChromosome())


    def crossOver(self):
        """
        perform cross over in this generation
        """

        def isNotMutuallySafe(queenA, queenB):
            """
            Two queens will never be mutually safe, 
            when they are less than 2 distance apart.
            """
            return abs(queenA-queenB) < 2


        def crossOverGenes(A, B):
            for i in range(1, len(A)):
                if isNotMutuallySafe(A[i], A[i-1]):
                    A[i], B[i] = B[i], A[i]
                
                if isNotMutuallySafe(B[i], B[i-1]):
                    A[i], B[i] = B[i], A[i]


        for i in range(1, len(self.population), 2):
            chromosomeA = self.population[i-1][:]
            chromosomeB = self.population[i][:]
            crossOverGenes(chromosomeA, chromosomeB)

    def mutate(self):
        """
        performs mutation in this generation
        """

        def mutateChromosome(chromosome):
            mutatedChromosome = []
            
            for gene in chromosome:
                if gene not in mutatedChromosome:
                    mutatedChromosome.append(gene)

            for i in range(self.boardSize):
                if i not in mutatedChromosome:
                    mutatedChromosome.append(i)
            
            return mutatedChromosome
        
        from math import floor
        mutationCount = floor(len(self.population) * self.MUTATION_RATE_FOR_POPULATION)
        
        for i in range(mutationCount):
            self.population.append(mutateChromosome(self.population[i]))

    def utilityFunction(self, chromosome):
        """
        kind of inverse fitness function
        """
        board = [[0 for j in range(n)] for i in range(n)]
        for i in range(len(chromosome)):
            board[chromosome[i]][i] = 1
        
        collisions = 0
        col = 1

        for gene in chromosome:
            try:
                for i in range(col-1, -1, -1):
                    if board[gene][i] == 1:
                        collisions += 1
            except IndexError:
                print(chromosome)
                quit(-1)
            
            for i, j in zip(range(gene-1, -1, -1), range(col-1, -1, -1)):
                if board[i][j] == 1:
                    collisions += 1

            for i, j in zip(range(gene+1, self.boardSize, 1), range(col-1, -1, -1)):
                if board[i][j] == 1:
                    collisions += 1

        return collisions

    def selectFittest(self):
        """
        performs selection of the fittest in this generation
        """

        utilityOfCurrentPopulation = []
        for chromosome in self.population:
            utilityOfCurrentPopulation.append(self.utilityFunction(chromosome))

        if min(utilityOfCurrentPopulation) == 0:
            self.solutionChromosome = self.population[utilityOfCurrentPopulation.index(min(utilityOfCurrentPopulation))]
            return

        newPopulation = []
        while len(newPopulation) < self.NO_OF_WINNERS:
           
            minUtility = min(utilityOfCurrentPopulation)
            indexOfMinUtility = utilityOfCurrentPopulation.index(minUtility)
            
            if minUtility < self.fittestYet:
                self.fittestYet = minUtility
            newPopulation.append(self.population[indexOfMinUtility])

            self.population.remove(self.population[indexOfMinUtility])
            utilityOfCurrentPopulation.remove(minUtility)
            
        # self.population = newPopulation
        pass
            
    def isGoal(self, chromosome):
        return self.utilityFunction(chromosome) == 0

    def solve(self):
        """
        solves the N queen with genetic algorithm
        """
        
        # create a population
        self.initializePopulation()
        generationNumber = 0

        # does this population have goal chromosome
        for chromosome in self.population:
            if self.isGoal(chromosome):
                return chromosome
        
        while generationNumber < self.MAX_GENERATIONS_ALLOWED:
            self.crossOver()
            self.mutate()
            self.selectFittest()
            generationNumber += 1

            if self.solutionChromosome != []:
                return self.solutionChromosome
            else:
                print("Generation is : {0} and fittest yet is : {1}".format(generationNumber, self.fittestYet))
                continue


def displayBoard(chromosome):
    """
    create the board from chromosome
    """
    size = len(chromosome)
    board = [[0 for j in range(n)] for i in range(n)]
    for i in range(size):
        board[chromosome[i]][i] = 1


    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                print("#", end="")
            else:
                print("Q", end="")
        print("")

if __name__ == "__main__": 

    # n = int(input("Enter board dimension: "))
    n = 5
    chessBoard = GeneticNQueen(n)

    from time import time
    start = time()
    solutionChromosome = chessBoard.solve()
    end = time()

    print("Solution chromosome:")
    print(solutionChromosome)

    print("Time taken : ")
    print(end - start)

    print("\nBoard status : ")
    displayBoard(solutionChromosome)

