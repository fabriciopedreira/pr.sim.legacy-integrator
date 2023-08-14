from enum import Enum


class ValidacaoEtapa(Enum):
    ANALISE_DA_DOCUMENTACAO = "analise_da_documentacao"
    ANALISE_DA_INSTALACAO = "analise_da_instalacao"
    ANALISE_DADOS_PARA_HOMOLOGACAO = "analise_dados_para_homologacao"
    ANALISE_DO_CLIENTE = "analise_do_cliente"
    ANALISE_DO_CONTRATO = "analise_do_contrato"
    ANALISE_DO_MONITORAMENTO = "analise_do_monitoramento"
    ANALISE_DO_RECEBIMENTO = "analise_do_recebimento"
    ANALISE_DOCUMENTOS_HOMOLOGACAO = "analise_documentos_homologacao"
    ANALISE_TECNICA = "analise_tecnica"
    DADOS_DO_CLIENTE = "dados_do_cliente"
    DADOS_DO_PROJETO = "dados_do_projeto"
    DOCUMENTACAO = "documentacao"
    RESUMO_GERAL = "resumo_geral"
    SIMULACAO_FINAL = "simulacao_final"


class ValidacaoStatus(Enum):
    ANALISE_MANUAL = "analise_manual"
    APROVADO = "aprovado"
    CANCELADO = "cancelado"
    EM_ANALISE = "em_analise"
    CANCELADO_EXP = "cancelado_exp"
    CONCLUIDO = "concluido"
    EM_ANDAMENTO = "em_andamento"
    REPROVADO = "reprovado"


class TipoPessoa(str, Enum):
    PESSOA_FISICA = "PF"
    PESSOA_JURIDICA = "PJ"
    PRODUTOR_RURAL = "PR"
