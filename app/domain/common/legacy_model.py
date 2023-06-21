from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.internal.config import DATABASE_SCHEMA


class EntityModelBase(Base):
    __abstract__ = True
    __table_args__ = {"schema": DATABASE_SCHEMA}

    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class ProdutoFinanceiro(EntityModelBase):
    __tablename__ = "produto_financeiro"

    slug = Column(String(255))


class Cliente(EntityModelBase):
    __tablename__ = "cliente"

    cpf = Column(String(32))
    nome_completo = Column(String(128))

    financiamento = relationship("Financiamento", back_populates="cliente")


class Empresa(EntityModelBase):
    __tablename__ = "empresa"

    cnpj = Column(String(32))
    nome_fantasia = Column(String(128))

    financiamento = relationship("Financiamento", back_populates="empresa")


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
    upload_drive_data = Column(DateTime(timezone=True))


class Emprestimo(EntityModelBase):
    __tablename__ = "emprestimo"

    numero_ccb = Column(String(32))
    cliente_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cliente.id"))
    avalista_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cliente.id"))


class Financiamento(EntityModelBase):
    __tablename__ = "financiamento"

    etapa = Column(String(64))
    status = Column(String(16))
    deletado = Column(Boolean, default=False)
    inativo = Column(Boolean, default=False)
    combo_facil = Column(Boolean, default=False)

    cliente_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cliente.id"))
    empresa_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.empresa.id"))
    contrato_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.contrato.id"))
    emprestimo_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.emprestimo.id"))
    bancarizadora_id = Column(BigInteger, ForeignKey(f"{DATABASE_SCHEMA}.bancarizadora.id"))
    tipo_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.tipo_de_financiamento.id"))
    cotacao_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cotacao.id"))
    parceiro_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.parceiro.id"))
    user_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.users.id"))

    cliente = relationship("Cliente", back_populates="financiamento")
    empresa = relationship("Empresa", back_populates="financiamento")
    cotacao = relationship("Cotacao", back_populates="financiamento")
    parceiro = relationship("Parceiro", back_populates="financiamento")
    users = relationship("Users", back_populates="financiamento")


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


class Parcela(EntityModelBase):
    __tablename__ = "parcela"

    numero_de_parcelas = Column(Integer, nullable=True)
    iof = Column(Float, nullable=True)
    cet = Column(String(16), nullable=True)
    valor_da_parcela = Column(Float, nullable=True)
    taxa_de_juros = Column(Float, nullable=True)
    taxa_de_cadastro = Column(Float, nullable=True)
    valor_da_comissao = Column(Float, nullable=True)
    aliquota_iof = Column(Float, nullable=True)

    cotacao_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cotacao.id"), nullable=True)

    cotacao = relationship("Cotacao", back_populates="parcelas")


class Comissao(EntityModelBase):
    __tablename__ = "comissao"

    valor = Column(Float, nullable=True)
    tipo = Column(String(16), nullable=True, default="comissao")
    pagamento_realizado = Column(Boolean, default=False)
    cotacao = relationship("Cotacao", back_populates="comissao")


class Cotacao(EntityModelBase):
    __tablename__ = "cotacao"

    valor_do_projeto = Column(Float)
    nome_do_projeto = Column(String(128))
    entrada = Column(Float)
    carencia = Column(Integer)
    numero_de_parcelas = Column(Integer)
    geracao_mensal = Column(Integer)
    cet = Column(String(16))
    envia_carencia = Column(Boolean, default=False)
    valor_original_financiado = Column(Float)
    potencia_do_sistema = Column(Float)
    ipca = Column(String(255))
    ipca_vigente = Column(String(255))
    calculadora_selecionada_id = Column(String(255))
    external_simulation_id = Column(String(255))

    fornecedor_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.fornecedor.id"), nullable=True)
    calculadora_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.calculadora.id"), nullable=True)
    cidade_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.cidade.id"), nullable=True)
    comissao_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.comissao.id"))

    financiamento = relationship("Financiamento", back_populates="cotacao")
    fornecedor = relationship("Fornecedor", back_populates="cotacao")
    calculadora = relationship("Calculadora", back_populates="cotacao")
    cidade = relationship("Cidade", back_populates="cotacao")
    comissao = relationship("Comissao", back_populates="cotacao")

    parcelas = relationship(
        "Parcela",
        back_populates="cotacao",
        primaryjoin="Parcela.cotacao_id==Cotacao.id",
        lazy=True,
        order_by="Parcela.numero_de_parcelas",
    )


class Parceiro(EntityModelBase):
    __tablename__ = "parceiro"

    financiamento = relationship("Financiamento", back_populates="parceiro")
    users = relationship("Users", back_populates="parceiro")


class Users(EntityModelBase):
    __tablename__ = "users"

    confirmed = Column(Boolean, default=False, nullable=True)
    nome_completo = Column(String(255), nullable=True)
    perfil = Column(String(128), nullable=True)

    fornecedor_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.fornecedor.id"))
    parceiro_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.parceiro.id"))
    contato_id = Column(Integer, ForeignKey(f"{DATABASE_SCHEMA}.contato.id"))

    contato = relationship("Contato", back_populates="users")
    parceiro = relationship("Parceiro", back_populates="users")
    financiamento = relationship("Financiamento", back_populates="users")
    fornecedor = relationship("Fornecedor", back_populates="users")


class Fornecedor(EntityModelBase):
    __tablename__ = "fornecedor"

    users = relationship("Users", back_populates="fornecedor")
    cotacao = relationship("Cotacao", back_populates="fornecedor")


class Calculadora(EntityModelBase):
    __tablename__ = "calculadora"

    cotacao = relationship("Cotacao", back_populates="calculadora")


class Cidade(EntityModelBase):
    __tablename__ = "cidade"

    cotacao = relationship("Cotacao", back_populates="cidade")


class Contato(EntityModelBase):
    __tablename__ = "contato"

    celular = Column(String(16), nullable=True)
    email = Column(String(128), nullable=True)

    users = relationship("Users", back_populates="contato")
