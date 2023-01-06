from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
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
    __tablename__ = "produto_financeiro"

    slug = Column(String(255))


class Cliente(EntityModelBase):
    __tablename__ = "cliente"

    cpf = Column(String(32))
    nome_completo = Column(String(128))


class Empresa(EntityModelBase):
    __tablename__ = "empresa"

    cnpj = Column(String(32))
    nome_fantasia = Column(String(128))


class TipoDeFinanciamento(EntityModelBase):
    __tablename__ = "tipo_de_financiamento"

    nome = Column(String(32))
    tipo = Column(String(8))


class Bancarizadora(EntityModelBase):
    __tablename__ = "bancarizadora"

    nome = Column(String(255))


class Contrato(EntityModelBase):
    __tablename__ = "contrato"

    produto_financeiro_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.produto_financeiro.id"))
    estimativa_de_emprestimo_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.emprestimo.id"))


class Emprestimo(EntityModelBase):
    __tablename__ = "emprestimo"

    numero_ccb = Column(String(32))
    cliente_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cliente.id"))
    avalista_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cliente.id"))


class Financiamento(EntityModelBase):
    __tablename__ = "financiamento"

    cliente_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cliente.id"))
    empresa_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.empresa.id"))
    contrato_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.contrato.id"))
    emprestimo_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.emprestimo.id"))
    bancarizadora_id = Column(BigInteger, ForeignKey(f"{DATABASE_SCHEMA}.bancarizadora.id"))
    tipo_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.tipo_de_financiamento.id"))


class Formalizacao(EntityModelBase):
    __tablename__ = "formalizacao"

    financiamento_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.financiamento.id"))


class Cessao(EntityModelBase):
    __tablename__ = "cessao"

    produto_financeiro_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.produto_financeiro.id"))


class CessaoFormalizacao(EntityModelBase):
    __tablename__ = "cessao_formalizacao"

    cessao_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cessao.id"))
    formalizacao_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.formalizacao.id"))
