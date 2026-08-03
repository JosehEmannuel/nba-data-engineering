from abc import ABC, abstractmethod

from src.uow.unit_of_work import UnitOfWork
from src.utils.logger import Logger


class BasePipeline(ABC):

    def __init__(self):

        self.logger = Logger.get_logger(self.__class__.__name__)

    @abstractmethod
    def execute(self, uow):

        pass

    def run(self):

        self.logger.info(
            f"Iniciando {self.__class__.__name__}"
        )

        try:

            with UnitOfWork() as uow:

                self.execute(uow)

            self.logger.info(
                f"{self.__class__.__name__} finalizado."
            )

        except Exception as erro:

            self.logger.exception(erro)

            raise