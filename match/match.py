import os
import entities
import algorithims

from concurrent import futures

class Match(object):
    def __init__(self, game, team_color, num_robots=3):
        super().__init__()
        self.game = game
        self.n_robots = num_robots
        self.team_color = os.environ.get('TEAM_COLOR', team_color)

        self.opposite_team_color = 'yellow' if self.team_color == 'blue' else 'blue'
    
    def start(self):
        self.ball = entities.Ball(self.game)

        self.opposites = [
            entities.Robot(self.game, i, self.opposite_team_color) for i in range(self.n_robots)
        ]

        self.robots = [
            entities.Robot(self.game, i, self.team_color) for i in range(self.n_robots)
        ]

        self.coach = entities.Coach(self)
        self.coach.decide()

        for robot in self.robots:
            robot.start()

    def update(self, frame):
        self.ball.update(frame)

        for entity in self.opposites:
            entity.update(frame)
        
        for entity in self.robots:
            entity.update(frame)

        
    def decide(self):
        commands = []
        '''
        https://docs.python.org/3/library/concurrent.futures.html
        '''

        self.coach.decide()

        with futures.ThreadPoolExecutor(max_workers=self.n_robots) as executor:
            commands = [
                executor.submit(robot.decide).result() for robot in self.robots
            ]
        
        return commands