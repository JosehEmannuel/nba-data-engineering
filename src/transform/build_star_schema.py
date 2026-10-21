from src.ingestion.base_pipeline import BasePipeline


class BuildStarSchemaPipeline(BasePipeline):
    """Atualiza as dimensões e fatos consumidos pelo Power BI."""

    def execute(self, uow):
        self.logger.info("Atualizando dimensões e fatos analíticos.")
        uow.analytics.refresh_star_schema()
        uow.commit()


if __name__ == "__main__":
    BuildStarSchemaPipeline().run()
