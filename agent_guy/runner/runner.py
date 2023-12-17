import logging

from agent_guy.executor import IExecutor
from agent_guy.model import IModel
from agent_guy.observer import IObserver
from agent_guy.visitor import IVisitor


class Runner:
    def __init__(
        self,
        model: IModel,
        observer: IObserver,
        executor: IExecutor,
        visitor: IVisitor,
        debug: bool = False,
    ) -> None:
        self.model = model
        self.observer = observer
        self.executor = executor
        self.visitor = visitor

        self.debug = debug

    def run(self) -> None:
        """run the simulation"""

        self._init_simulation()

        logging.info("Start Simulation")
        self._run_simulation()

        logging.info("Simulation finished")

    def _init_simulation(self) -> None:
        """initialize the simulation"""
        logging.info("Running the simulation")
        logging.info("Setup the model")
        self.model.setup_grid()
        self.model.setup_agents()

        # add executor to model
        self.model.add_executor(self.executor)

    def _run_simulation(self) -> None:
        """run the simulation"""
        for i_step in range(1, self.executor.max_step + 1):
            logging.info(f"Executing step {i_step}/{self.executor.max_step}")
            self.model.step()
