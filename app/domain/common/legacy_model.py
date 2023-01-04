
from sqlalchemy import BigInteger, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.sql import func

from app.database import Base
from app.internal.config import DATABASE_SCHEMA


class EntityModelBase(Base):
    __abstract__ = True
    __table_args__ = {"schema": DATABASE_SCHEMA}

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProdutoFinanceiro(EntityModelBase):
    __tablename__ = 'produto_financeiro'

    slug = Column(String(255))


class Cliente(EntityModelBase):
    __tablename__ = "cliente"

    cpf = Column(String(32), index=True, nullable=True)
    nome_completo = Column(String(128), index=True, nullable=True)


class TipoDeFinanciamento(EntityModelBase):
    __tablename__ = "tipo_de_financiamento"

    name = Column(String(32), unique=True, nullable=True)
    tipo = Column(String(8), unique=True, nullable=True)


class Bancarizadora(EntityModelBase):
    __tablename__ = "bancarizadora"

    name = Column(String(255), unique=True, nullable=True)


class Contrato(EntityModelBase):
    __tablename__ = "contrato"

    produto_financeiro_id = Column(Integer, ForeignKey('produto_financeiro.id'))
    estimativa_de_emprestimo_id = Column(Integer, ForeignKey('emprestimo.id'))


class Emprestimo(EntityModelBase):
    __tablename__ = "emprestimo"

    numero_ccb = Column(String(32), nullable=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    avalista_id = Column(Integer, ForeignKey('cliente.id'))


class Financiamento(EntityModelBase):
    __tablename__ = 'financiamento'

    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    avalista_id = Column(Integer, ForeignKey('cliente.id'))
    contrato_id = Column(Integer, ForeignKey('contrato.id'))
    emprestimo_id = Column(Integer, ForeignKey('emprestimo.id'))
    bancarizadora_id = Column(Integer, ForeignKey('bancarizadora.id'))
    tipo_de_financiamento_id = Column(Integer, ForeignKey('tipo_de_financiamento.id'))
