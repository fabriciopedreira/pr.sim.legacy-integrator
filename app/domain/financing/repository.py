import uuid
from typing import Any, Dict, Optional

from sqlalchemy import insert, update

from app.domain.common.legacy_model import (ClickSign, ConfiguracaoEletrica,
                                            Cotacao, Financiamento, Inversor,
                                            Parcela, SmartMeter,
                                            SmartMeterInversor)
from app.domain.common.repository_base import RepositoryBase
from app.domain.financing.schemas import FinancingCotationDTO, InstallmentData


class FinancingRepository(RepositoryBase):
    async def save(self, model) -> Any:
        self.session_db.add(model)
        self.session_db.commit()
        self.session_db.refresh(model)
        return model

    async def remove(self, model: Any, model_id: int, commit: Optional[bool] = True) -> tuple[Any] | None:

        result = self.session_db.query(model).filter_by(id=model_id).one_or_none()

        if result:
            self.session_db.delete(result)

            if commit:
                self.session_db.commit()
            return model_id

        return None

    async def update(
        self, model: Any, model_id: int, values: Dict[str, Any], commit: Optional[bool] = True
    ) -> tuple[Any] | None:
        """Update BaseModel in database
        :param model: Model
        :param model_id: ID of the model
        :param values: Dictionary values of the model to be updated
        :param commit: Optional commit in database

        :return: mode_id or None
        """

        stmt = update(model).where(model.id == model_id).values(values)
        self.session_db.execute(stmt)

        if commit:
            self.session_db.commit()
            return model_id

        return None

    async def get(self, model: Any, model_id: int) -> Any | None:
        result = self.session_db.query(model).filter_by(id=model_id).one_or_none()

        return result
    
    def get_smart_meter_by_financing_id(self, financing_id: int) -> Any | None:
        result = (self.session_db.query(SmartMeter)
            .join(ConfiguracaoEletrica, SmartMeter.configuracao_eletrica_id == ConfiguracaoEletrica.id)
            .join(Financiamento, Financiamento.configuracao_eletrica_id == ConfiguracaoEletrica.id)
            .filter_by(id=financing_id)
            .one_or_none()
        )
        return result
    
    def delete_smart_meter(self, smart_meter_id: int) -> Any | None:
        inversors = self.session_db.query(SmartMeterInversor).filter_by(smart_meter_id=smart_meter_id).all()
        for inversor in inversors:
            self.session_db.delete(inversor)
        
        result = self.session_db.query(SmartMeter).filter_by(id=smart_meter_id).one_or_none()
        self.session_db.delete(result)

        self.session_db.commit()

        return True
    
    def create_smart_meter(self, financing_id: int) -> Any | None:
        inversors = (self.session_db.query(Inversor)
                     .join(ConfiguracaoEletrica, Inversor.configuracao_eletrica_id == ConfiguracaoEletrica.id)
                     .join(Financiamento, Financiamento.configuracao_eletrica_id == ConfiguracaoEletrica.id)
                     .filter_by(id=financing_id)
                     .all())
        configuracao_eletrica_id = (self.session_db.query(Financiamento.configuracao_eletrica_id)
                                    .filter_by(id=financing_id)
                                    .scalar())
        smart_meter = SmartMeter(configuracao_eletrica_id=configuracao_eletrica_id)
        self.session_db.add(smart_meter)
        self.session_db.commit()
        self.session_db.refresh(smart_meter)
        for inversor in inversors:
            smart_meter_inversor = SmartMeterInversor(smart_meter_id=smart_meter.id, inversor_id=inversor.id)
            self.session_db.add(smart_meter_inversor)
        
        self.session_db.commit()

        return True
     
    async def get_financing_by_project_id(self, project_id: uuid.UUID) -> Any | None:

        result = (
            self.session_db.query(Financiamento.etapa, Financiamento.id)
            .join(Cotacao, Financiamento.cotacao_id == Cotacao.id)
            .filter(Cotacao.external_simulation_id == str(project_id))
            .one_or_none()
        )

        return result

    async def is_contract_clicksign_by_financing_id(self, financing_id: uuid.UUID) -> bool | None:

        result = (
            self.session_db.query(ClickSign)
            .join(Financiamento, ClickSign.financiamento_id == Financiamento.id)
            .filter(Financiamento.id == str(financing_id), ClickSign.tipo_documento == "contrato")
            .count()
        )

        return result == 0

    async def get_contract_by_financing_id(self, financing_id: uuid.UUID) -> Any | None:

        result = (
            self.session_db.query(ClickSign)
            .join(Financiamento, ClickSign.financiamento_id == Financiamento.id)
            .filter(Financiamento.id == str(financing_id), ClickSign.tipo_documento == "contrato")
            .one_or_none()
        )

        return result

    async def get_parcela_by_quotation_id(self, quotation_id: uuid.UUID) -> Any | None:

        result = (
            self.session_db.query(Parcela)
            .filter(Parcela.cotacao_id == str(quotation_id), Parcela.numero_de_parcelas != 144)
            .one_or_none()
        )

        if result is None:
            result = self.get_parcela144x_by_quotation_id(quotation_id=quotation_id)

        return result

    async def get_parcela144x_by_quotation_id(self, quotation_id: uuid.UUID) -> Any | None:

        result = (
            self.session_db.query(Parcela)
            .filter(Parcela.cotacao_id == str(quotation_id), Parcela.numero_de_parcelas == 144)
            .one_or_none()
        )
        return result

    async def get_financing_and_quotation_by_project_id(self, project_id: uuid.UUID) -> FinancingCotationDTO | None:
        """Get information of financing end quotation by project_id
        :param: project_id: UUID of the project

        :return: FinancingCotationDTO or None
        """

        result = (
            self.session_db.query(
                Cotacao.comissao_id,
                Financiamento.id,
                Financiamento.cotacao_id,
                Financiamento.combo_facil,
            )
            .filter_by(external_simulation_id=str(project_id))
            .join(Financiamento, Financiamento.cotacao_id == Cotacao.id)
            .one_or_none()
        )

        if result:
            result = FinancingCotationDTO(
                commission_id=result[0],
                financing_id=result[1],
                quotation_id=result[2],
                has_combo_facil=result[3],
            )
        return result

    async def create_or_update_installments(self, installment_data: InstallmentData) -> None:

        stmt = (
            update(Parcela)
            .where(Parcela.cet == installment_data.cet)
            .where(Parcela.numero_de_parcelas == installment_data.numero_de_parcelas)
            .where(Parcela.cotacao_id == installment_data.cotacao_id)
            .values(installment_data.dict())
        )

        result = self.session_db.execute(stmt)

        if not result.rowcount:
            insertion_stmt = insert(Parcela).values(installment_data.dict())

            self.session_db.execute(insertion_stmt)

        self.session_db.commit()
