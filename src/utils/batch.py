from collections.abc import Generator, Iterable
from typing import TypeVar


T = TypeVar("T")


class BatchProcessor:
    """
    Responsável por dividir iteráveis em lotes (batches).

    Exemplo:

        generator = service.fetch_players()

        for batch in BatchProcessor.chunk(generator, 100):
            ...

    """

    @staticmethod
    def chunk(
        iterable: Iterable[T],
        batch_size: int = 100
    ) -> Generator[list[T], None, None]:
        """
        Divide qualquer iterável em lotes.

        Parameters
        ----------
        iterable : Iterable
            Sequência de objetos.

        batch_size : int
            Quantidade máxima de objetos por lote.

        Returns
        -------
        Generator[list[T]]
        """

        if batch_size <= 0:
            raise ValueError("batch_size deve ser maior que zero.")

        batch: list[T] = []

        for item in iterable:

            batch.append(item)

            if len(batch) >= batch_size:

                yield batch

                batch = []

        if batch:

            yield batch

    @staticmethod
    def count_batches(
        total_items: int,
        batch_size: int
    ) -> int:
        """
        Retorna quantos batches serão necessários.

        Exemplo:

            5300 registros

            batch_size=100

            retorno = 53
        """

        if batch_size <= 0:
            raise ValueError("batch_size deve ser maior que zero.")

        return (total_items + batch_size - 1) // batch_size

    @staticmethod
    def batch_info(
        current_batch: int,
        total_batches: int,
        current_items: int,
        total_items: int
    ) -> str:
        """
        Gera uma mensagem padronizada para logs.

        Exemplo:

        Batch 3/25 | 300/2500 registros
        """

        return (
            f"Batch {current_batch}/{total_batches} | "
            f"{current_items}/{total_items} registros"
        )