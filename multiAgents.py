# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        ghostPostions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        distance = 0.0
        gameScore = successorGameState.getScore()
        newFoodPostion = newFood.asList()       


        # use reciprocal of distance between pacman and ghost
        distanceBetweenPacmanAndGhost = [util.manhattanDistance(newPos, i) for i in ghostPostions]
        if len(distanceBetweenPacmanAndGhost) and max(distanceBetweenPacmanAndGhost) != 0.0:
          distance -= 10.0/ max(distanceBetweenPacmanAndGhost)

        # use reciprocal of distance between pacman and food
        distanceBetweenPacmanAndFood = [util.manhattanDistance(newPos, i) for i in newFoodPostion]
        if len(distanceBetweenPacmanAndFood) and min(distanceBetweenPacmanAndFood) != 0.0:
          distance += 9.0/ min(distanceBetweenPacmanAndFood)

        # use reciprocal of min scared time
        if min(newScaredTimes) != 0.0:
          distance += 1.0/ min(newScaredTimes)

        # force pacman to continue
        if action == 'STOP':
          distance -= 100000.0


        return distance + gameScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"



        # only one pacman so only one layer
        def maxValue(state, depth):
          # terminal test
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          # set value to minus infinite
          value = float("-inf")
          # get legal actions from pacman
          legalActions = state.getLegalActions(0)
          legalStates = [state.generateSuccessor(0,i) for i in legalActions]
          for i in legalStates:
            value = max(value, minValue(i, depth, 1))

          return value

        # depth: how many (max+mins)
        def minValue(state, depth, index):
          # terminal test
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          # set value to infinite
          value = float("inf")
          legalActions = state.getLegalActions(index)
          legalStates = [state.generateSuccessor(index, i) for i in legalActions]
          for i in legalStates:
            if (index == state.getNumAgents()-1):
              # turn into pacman
              value =  min(value, maxValue(i, depth + 1))             
            else:                         
              # Go to another layer 
              value = min(value, minValue(i, depth, index + 1))
          return value


        # pacman move first then ghosts move
        # i.e. call minValue at leaves of the tree
        def minimaxDecision(state):
          legalActionsPacman = state.getLegalActions(0)
          # initialize action
          action = None
          value = float("-inf")
          for i in legalActionsPacman:
            # get the corresponding position of the action
            # should not need this generateSuccessor function
            legelState = gameState.generateSuccessor(0,i)
            temp = max(value, minValue(legelState, 0, 1))
            if temp > value:
              value = temp
              action = i
          return action
        
        return minimaxDecision(gameState)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # only one pacman so only one layer
        def maxValue(state, depth, alpha, beta):
          # terminal test
          if state.isLose() or state.isWin() or depth == self.depth:
            return (self.evaluationFunction(state), None)
          # set value to minus infinite
          valueI = float("-inf")
          action = None
          # get legal actions from pacman
          legalActions = state.getLegalActions(0)
          for i in legalActions:
            nextState = state.generateSuccessor(0,i)
            value =  minValue(nextState, depth, 1, alpha, beta)[0]
            if (value > valueI):
              action = i
              valueI = value
            if value > beta:
              return (valueI, action)
            alpha = max(valueI, alpha)

          return (valueI, action)

        # depth: how many (max+mins)
        def minValue(state, depth, index, alpha, beta):
          # terminal test
          if state.isLose() or state.isWin() or depth == self.depth:
            return (self.evaluationFunction(state), None)
          # set value to infinite
          valueI = float("inf")
          legalActions = state.getLegalActions(index)
          for i in legalActions:
            nextState = state.generateSuccessor(index, i)
            if (index == state.getNumAgents()-1):
              # turn into pacman
              value = maxValue(nextState, depth + 1, alpha, beta)[0]      
            else:                         
              # Go to another layer 
              value = minValue(nextState, depth, index + 1, alpha, beta)[0]

            if value < valueI:
              valueI = value
              action = i

            if value < alpha:
              return (valueI, action)
            beta = min(valueI, beta)

          return (valueI, action)
        

        return maxValue(gameState, 0, float("-inf"), float("inf"))[1]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def maxValue(state, depth):
          # terminal test
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          # set value to minus infinite
          value = float("-inf")
          # get legal actions from pacman
          legalActions = state.getLegalActions(0)
          legalStates = [state.generateSuccessor(0,i) for i in legalActions]
          for i in legalStates:
            value = max(value, expMinValue(i, depth, 1))

          return value

        # depth: how many (max+mins)
        def expMinValue(state, depth, index):
          # terminal test
          if state.isLose() or state.isWin() or depth == self.depth:
            return self.evaluationFunction(state)
          # set value to infinite
          value = 0
          legalActions = state.getLegalActions(index)
          legalStates = [state.generateSuccessor(index, i) for i in legalActions]

          # number of children
          length = len(legalStates)


          # sum up all child's values 
          for i in legalStates:
            if (index == state.getNumAgents()-1):
              # turn into pacman
              value += maxValue(i, depth + 1)            
            else:                         
              # Go to another layer 
              value += expMinValue(i, depth, index + 1)

          # children's values are equally-weighted
          # average of all child's values
          return float(value)/ length


        # pacman move first then ghosts move
        # i.e. call minValue at leaves of the tree
        def expectiMax(state):
          legalActionsPacman = state.getLegalActions(0)
          # initialize action
          action = None
          value = float("-inf")
          for i in legalActionsPacman:
            # get the corresponding position of the action
            # should not need this generateSuccessor function
            legelState = gameState.generateSuccessor(0,i)
            temp = max(value, expMinValue(legelState, 0, 1))
            if temp > value:
              value = temp
              action = i
          return action
        
        return expectiMax(gameState)

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      The value should return a linear combination of distances between food and pacman,
      distances between ghosts and pacman.
      Since we want to keep the pacman alive while eating all the food
      the weight on distances between ghosts and pacman should be more than
      the weight on distances between food and pacman

    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    ghostPostions = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


    distance = 0.0
    gameScore = currentGameState.getScore()
    newFoodPostion = newFood.asList()       


    # use reciprocal of distance between pacman and ghost
    distanceBetweenPacmanAndGhost = [util.manhattanDistance(newPos, i) for i in ghostPostions]
    if len(distanceBetweenPacmanAndGhost) and max(distanceBetweenPacmanAndGhost) != 0.0:
      distance += 2.0/ max(distanceBetweenPacmanAndGhost)

    # use reciprocal of distance between pacman and food
    distanceBetweenPacmanAndFood = [util.manhattanDistance(newPos, i) for i in newFoodPostion]
    if len(distanceBetweenPacmanAndFood) and min(distanceBetweenPacmanAndFood) != 0.0:
      distance += 5.0/ min(distanceBetweenPacmanAndFood)

    # use reciprocal of min scared time
    if min(newScaredTimes) != 0.0:
      distance += 10.0/ min(newScaredTimes)


    return distance + gameScore

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

