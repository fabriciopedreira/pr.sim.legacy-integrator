# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Access(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    system_profile_module = models.ForeignKey('SystemProfileModule', models.DO_NOTHING)
    permissions = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'access'


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class Analise(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    etapa = models.CharField(max_length=32, blank=True, null=True)
    data_de_submissao = models.DateTimeField(blank=True, null=True)
    financiamento = models.ForeignKey('Financiamento', models.DO_NOTHING, blank=True, null=True)
    homologacao = models.ForeignKey('Homologacao', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analise'


class ApiKeys(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.UUIDField(unique=True, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_keys'


class AreaAtuacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nome = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_atuacao'


class AuditLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    entity = models.TextField()
    entity_id = models.BigIntegerField()
    action = models.TextField()
    field = models.TextField()
    before_action = models.TextField(blank=True, null=True)
    after_action = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_log'


class AuthLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    ip = models.CharField(max_length=255)
    user_agent = models.TextField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    fingerprint = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_log'


class AutoConsumoRemoto(models.Model):
    id = models.BigAutoField(primary_key=True)
    beneficiaria = models.CharField(max_length=255, blank=True, null=True)
    homologacao = models.ForeignKey('Homologacao', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auto_consumo_remoto'


class Aviso(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    endpoint = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aviso'


class AvisoUser(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    aviso = models.ForeignKey(Aviso, models.DO_NOTHING)
    data_inicio = models.DateTimeField(blank=True, null=True)
    data_fim = models.DateTimeField(blank=True, null=True)
    visualizado = models.BooleanField(blank=True, null=True)
    delay_proximo_aviso = models.DurationField(blank=True, null=True)
    proximo_aviso = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aviso_user'


class Bancarizadora(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bancarizadora'


class Biometria(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    score = models.IntegerField(blank=True, null=True)
    facematch = models.BooleanField(blank=True, null=True)
    decisao = models.TextField(blank=True, null=True)
    id_externo = models.TextField(unique=True)
    status = models.ForeignKey('BiometriaStatus', models.DO_NOTHING, blank=True, null=True)
    titular = models.ForeignKey('Cliente', models.DO_NOTHING)
    liveness = models.BooleanField(blank=True, null=True)
    template = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'biometria'


class BiometriaDocumento(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    path = models.TextField()
    tipo = models.ForeignKey('BiometriaDocumentoTipo', models.DO_NOTHING)
    biometria = models.ForeignKey(Biometria, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'biometria_documento'


class BiometriaDocumentoTipo(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    nome = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'biometria_documento_tipo'


class BiometriaStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    nome = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'biometria_status'


class Calculadora(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    porcentagem_entrada_minima = models.FloatField(blank=True, null=True)
    valor_maximo_financiado = models.FloatField(blank=True, null=True)
    valor_minimo_financiado = models.FloatField(blank=True, null=True)
    nome = models.CharField(max_length=32, blank=True, null=True)
    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=True, null=True)
    tipo_de_financiamento = models.ForeignKey('TipoDeFinanciamento', models.DO_NOTHING, blank=True, null=True)
    carencia_maxima = models.IntegerField(blank=True, null=True)
    carencia_minima = models.IntegerField(blank=True, null=True)
    ativo = models.BooleanField()
    valor_maximo_taxa_de_cadastro = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calculadora'


class Cessao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    download_link = models.TextField(blank=True, null=True)
    total_pf = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    total_pj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    valor_aquisicao_pf = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    valor_aquisicao_pj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    valor_bruto_pf = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    valor_bruto_pj = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    produto_financeiro = models.ForeignKey('ProdutoFinanceiro', models.DO_NOTHING, blank=True, null=True)
    soma_valor_bruto = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    soma_valor_financiado = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    soma_valor_aquisicao = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cessao'


class CessaoFormalizacao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cessao = models.ForeignKey(Cessao, models.DO_NOTHING)
    formalizacao = models.ForeignKey('Formalizacao', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cessao_formalizacao'


class CheckList(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    financiamento = models.OneToOneField('Financiamento', models.DO_NOTHING)
    contrato_assinado_corretamente = models.BooleanField(blank=True, null=True)
    documentos_aprovados = models.BooleanField(blank=True, null=True)
    email_aprovado = models.BooleanField(blank=True, null=True)
    parceiro_tem_conta_digital = models.BooleanField(blank=True, null=True)
    pronto_para_formalizar = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'check_list'


class Cidade(models.Model):
    nome = models.CharField(max_length=64, blank=True, null=True)
    estado = models.ForeignKey('Estado', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    distribuidor = models.ForeignKey('Distribuidor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cidade'


class Clicksign(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    financiamento = models.ForeignKey('Financiamento', models.DO_NOTHING)
    document_key = models.CharField(unique=True, max_length=64, blank=True, null=True)
    signer_key = models.CharField(max_length=64, blank=True, null=True)
    request_signature_key = models.CharField(max_length=64, blank=True, null=True)
    solicitado_por_email = models.BooleanField()
    solicitado_por_whatsapp = models.BooleanField()
    avalista_request_signature_key = models.CharField(max_length=64, blank=True, null=True)
    avalista_signer_key = models.CharField(max_length=64, blank=True, null=True)
    avalista_solicitado_por_email = models.BooleanField()
    avalista_solicitado_por_whatsapp = models.BooleanField()
    cliente_assinou = models.DateTimeField(blank=True, null=True)
    avalista_assinou = models.DateTimeField(blank=True, null=True)
    finalizado = models.DateTimeField(blank=True, null=True)
    assinado_baixado = models.DateTimeField(blank=True, null=True)
    api_signer_request_signature_key = models.CharField(max_length=64, blank=True, null=True)
    assinado_por_api = models.DateTimeField(blank=True, null=True)
    tipo_documento = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clicksign'
        unique_together = (('financiamento', 'tipo_documento'),)


class Cliente(models.Model):
    nome_completo = models.CharField(max_length=128, blank=True, null=True)
    cpf = models.CharField(max_length=32, blank=True, null=True)
    rg = models.CharField(max_length=32, blank=True, null=True)
    data_de_nascimento = models.DateField(blank=True, null=True)
    contato = models.ForeignKey('Contato', models.DO_NOTHING, blank=True, null=True)
    endereco = models.ForeignKey('Endereco', models.DO_NOTHING, blank=True, null=True)
    profissao = models.ForeignKey('Profissao', models.DO_NOTHING, blank=True, null=True)
    renda_mensal = models.FloatField(blank=True, null=True)
    comprovante_residencia = models.TextField(blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    registro_socinal = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nome_da_mae = models.CharField(max_length=64, blank=True, null=True)
    field_autorizacao_em = models.DateTimeField(db_column='_autorizacao_em', blank=True, null=True)  # Field renamed because it started with '_'.
    field_autorizacao_info = models.TextField(db_column='_autorizacao_info', blank=True, null=True)  # Field renamed because it started with '_'.
    field_autorizou = models.BooleanField(db_column='_autorizou', blank=True, null=True)  # Field renamed because it started with '_'.
    numero_email_autorizacao_enviados = models.IntegerField(blank=True, null=True)
    autorizacao = models.BooleanField(blank=True, null=True)
    autorizacao_data = models.DateTimeField(blank=True, null=True)
    autorizacao_ip = models.TextField(blank=True, null=True)
    public_id = models.UUIDField(unique=True, blank=True, null=True)
    produto_rural = models.ForeignKey('ProdutoRural', models.DO_NOTHING, blank=True, null=True)
    titular_conta_de_luz = models.ForeignKey('TitularContaDeLuz', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Cobertura(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nome = models.TextField()
    descricao = models.TextField()

    class Meta:
        managed = False
        db_table = 'cobertura'


class CodigoBancario(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nome_banco = models.CharField(unique=True, max_length=255)
    compe = models.CharField(unique=True, max_length=3)
    ispb = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = False
        db_table = 'codigo_bancario'


class Comissao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tipo = models.CharField(max_length=64)
    valor = models.FloatField(blank=True, null=True)
    pagamento_realizado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'comissao'


class ConfigAccess(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    system_role = models.ForeignKey('SystemRole', models.DO_NOTHING)
    system_profile_module = models.ForeignKey('SystemProfileModule', models.DO_NOTHING)
    system_permission = models.ForeignKey('SystemPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'config_access'
        unique_together = (('system_role', 'system_profile_module', 'system_permission'),)


class ConfiguracaoEletrica(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'configuracao_eletrica'


class Consulta(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    json_resultado = models.TextField(blank=True, null=True)
    resultado = models.CharField(max_length=64, blank=True, null=True)
    financiamento = models.ForeignKey('Financiamento', models.DO_NOTHING, blank=True, null=True)
    erro = models.TextField(blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    bureau = models.CharField(max_length=32, blank=True, null=True)
    cpf = models.CharField(max_length=32, blank=True, null=True)
    id_externo = models.CharField(max_length=64, blank=True, null=True)
    tipo = models.CharField(max_length=32, blank=True, null=True)
    comprometimento_renda = models.FloatField(blank=True, null=True)
    score_bv = models.FloatField(blank=True, null=True)
    score_serasa = models.FloatField(blank=True, null=True)
    score_solfacil = models.FloatField(blank=True, null=True)
    valor_max_financiado = models.FloatField(blank=True, null=True)
    valor_min_entrada = models.FloatField(blank=True, null=True)
    versao = models.CharField(max_length=64, blank=True, null=True)
    cnpj = models.CharField(max_length=64, blank=True, null=True)
    json_base_cnpj = models.TextField(blank=True, null=True)
    renda_esta_aprovada = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consulta'


class ConsultaCampos(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    consulta = models.ForeignKey(Consulta, models.DO_NOTHING)
    tipo = models.CharField(max_length=32, blank=True, null=True)
    nome = models.CharField(max_length=64, blank=True, null=True)
    valor = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'consulta_campos'


class Contato(models.Model):
    celular = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    telefone_fixo = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contato'


class Contrato(models.Model):
    contrato_assinado = models.TextField(blank=True, null=True)
    estimativa_de_emprestimo = models.ForeignKey('Emprestimo', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    baixado = models.BooleanField(blank=True, null=True)
    relatorios_de_credito = models.TextField(blank=True, null=True)
    pontuacao_media_formalizacao = models.FloatField(blank=True, null=True)
    a_vista = models.BooleanField(blank=True, null=True)
    documentacao_aprovada = models.BooleanField(blank=True, null=True)
    upload_drive = models.BooleanField(blank=True, null=True)
    upload_drive_data = models.DateTimeField(blank=True, null=True)
    are_docs_together = models.BooleanField(blank=True, null=True)
    documento_avalista = models.ForeignKey('Documento', models.DO_NOTHING, blank=True, null=True)
    documento_cliente = models.ForeignKey('Documento', models.DO_NOTHING, blank=True, null=True)
    produto_financeiro = models.ForeignKey('ProdutoFinanceiro', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contrato'


class ContratoDigital(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tipo = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    url_contrato_assinado = models.CharField(max_length=255, blank=True, null=True)
    integracao = models.CharField(max_length=255)
    expira_em = models.DateTimeField()
    financiamento = models.ForeignKey('Financiamento', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'contrato_digital'


class ContratoDigitalSignatario(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    assinou_em = models.DateTimeField()
    signatario = models.ForeignKey('Signatario', models.DO_NOTHING)
    contrato_digital = models.ForeignKey(ContratoDigital, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'contrato_digital_signatario'


class Cotacao(models.Model):
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, blank=True, null=True)
    geracao_mensal = models.IntegerField(blank=True, null=True)
    valor_do_projeto = models.FloatField(blank=True, null=True)
    entrada = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    calculadora = models.ForeignKey(Calculadora, models.DO_NOTHING, blank=True, null=True)
    prazo = models.ForeignKey('Prazo', models.DO_NOTHING, blank=True, null=True)
    carencia = models.IntegerField(blank=True, null=True)
    nome_do_projeto = models.CharField(max_length=128, blank=True, null=True)
    field_dealer_fee = models.FloatField(db_column='_dealer_fee', blank=True, null=True)  # Field renamed because it started with '_'.
    numero_de_parcelas = models.IntegerField(blank=True, null=True)
    field_taxa_de_cadastro = models.FloatField(db_column='_taxa_de_cadastro', blank=True, null=True)  # Field renamed because it started with '_'.
    field_taxa_de_juros = models.FloatField(db_column='_taxa_de_juros', blank=True, null=True)  # Field renamed because it started with '_'.
    field_valor_da_parcela = models.FloatField(db_column='_valor_da_parcela', blank=True, null=True)  # Field renamed because it started with '_'.
    fornecedor = models.ForeignKey('Fornecedor', models.DO_NOTHING, blank=True, null=True)
    comissao = models.ForeignKey(Comissao, models.DO_NOTHING, blank=True, null=True)
    tarifa = models.ForeignKey('Tarifa', models.DO_NOTHING, blank=True, null=True)
    cet = models.CharField(max_length=16, blank=True, null=True)
    envia_carencia = models.BooleanField(blank=True, null=True)
    valor_original_financiado = models.FloatField(blank=True, null=True)
    potencia_do_sistema = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cotacao'


class DadoBancario(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    conta = models.CharField(max_length=16, blank=True, null=True)
    agencia = models.CharField(max_length=8, blank=True, null=True)
    numero_do_banco = models.CharField(max_length=8, blank=True, null=True)
    banco = models.CharField(max_length=32, blank=True, null=True)
    conta_digito = models.CharField(max_length=1, blank=True, null=True)
    chave_pix = models.CharField(max_length=255, blank=True, null=True)
    tipo_conta = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'dado_bancario'


class DesligamentoRemoto(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo_rastreio = models.CharField(max_length=1024, blank=True, null=True)
    enviado = models.BooleanField(blank=True, null=True)
    financiamento = models.ForeignKey('Financiamento', models.DO_NOTHING)
    servico_entrega = models.ForeignKey('ServicoEntrega', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    data_envio = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'desligamento_remoto'


class Distribuidor(models.Model):
    nome = models.CharField(max_length=256, blank=True, null=True)
    iniciais = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    estado = models.ForeignKey('Estado', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'distribuidor'


class Documentacao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    assinaveis = models.TextField(blank=True, null=True)
    assinados = models.TextField(blank=True, null=True)
    disjuntor = models.TextField(blank=True, null=True)
    padrao_de_entrada = models.TextField(blank=True, null=True)
    diagrama = models.TextField(blank=True, null=True)
    conta_de_luz = models.TextField(blank=True, null=True)
    cnh = models.TextField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    aceita_sugestao = models.BooleanField(blank=True, null=True)
    comprovante_troca_titularidade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentacao'


class Documento(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    documento_de_identidade = models.TextField(blank=True, null=True)
    comprovante_de_renda = models.TextField(blank=True, null=True)
    titularidade_do_imovel = models.TextField(blank=True, null=True)
    documentos_adicionais = models.JSONField(blank=True, null=True)
    comprovante_de_residencia = models.TextField(blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    contrato_social = models.TextField(blank=True, null=True)
    comprovante_faturamento = models.TextField(blank=True, null=True)
    titular = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    dap = models.TextField(blank=True, null=True)
    comprovante_propriedade_rural = models.TextField(blank=True, null=True)
    esocial = models.TextField(blank=True, null=True)
    declaracao_do_responsavel_pela_empresa = models.TextField(blank=True, null=True)
    regularidade_do_empregador = models.TextField(blank=True, null=True)
    comprovante_titularidade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documento'


class Empresa(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nome_fantasia = models.CharField(max_length=128, blank=True, null=True)
    razao_social = models.TextField(blank=True, null=True)
    cnpj = models.CharField(max_length=32)
    contato = models.ForeignKey(Contato, models.DO_NOTHING, blank=True, null=True)
    endereco = models.ForeignKey('Endereco', models.DO_NOTHING, blank=True, null=True)
    faturamento_mensal = models.FloatField(blank=True, null=True)
    capital_social = models.FloatField(blank=True, null=True)
    autorizacao = models.BooleanField(blank=True, null=True)
    autorizacao_data = models.DateTimeField(blank=True, null=True)
    autorizacao_ip = models.TextField(blank=True, null=True)
    registro_socinal = models.CharField(max_length=32, blank=True, null=True)
    setor = models.CharField(max_length=128, blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    public_id = models.UUIDField(unique=True, blank=True, null=True)
    titular_conta_de_luz = models.ForeignKey('TitularContaDeLuz', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresa'


class Emprestimo(models.Model):
    data_de_vencimento = models.DateField(blank=True, null=True)
    cet_anual = models.FloatField(blank=True, null=True)
    cet_mensal = models.FloatField(blank=True, null=True)
    data_de_emissao = models.DateField(blank=True, null=True)
    iof = models.FloatField(blank=True, null=True)
    numero_ccb = models.CharField(max_length=32, blank=True, null=True)
    avalista = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cotacao = models.ForeignKey(Cotacao, models.DO_NOTHING, blank=True, null=True)
    parcela_contrato = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    public_id = models.UUIDField(unique=True, blank=True, null=True)
    data_geracao_ccb = models.DateTimeField(blank=True, null=True)
    porcentagem_aquisicao = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emprestimo'


class Endereco(models.Model):
    cep = models.CharField(max_length=32, blank=True, null=True)
    numero = models.CharField(max_length=16, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    complemento = models.CharField(max_length=128, blank=True, null=True)
    bairro = models.CharField(max_length=64, blank=True, null=True)
    rua = models.CharField(max_length=128, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    ponto_de_referencia = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'endereco'


class Estado(models.Model):
    nome = models.CharField(unique=True, max_length=32, blank=True, null=True)
    sigla = models.CharField(unique=True, max_length=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'


class Financiamento(models.Model):
    etapa = models.CharField(max_length=64, blank=True, null=True)
    cotacao = models.ForeignKey(Cotacao, models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    avalista = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    projeto = models.ForeignKey('Projeto', models.DO_NOTHING, blank=True, null=True)
    instalacao = models.ForeignKey('Instalacao', models.DO_NOTHING, blank=True, null=True)
    monitoramento = models.ForeignKey('Monitoramento', models.DO_NOTHING, blank=True, null=True)
    contrato = models.ForeignKey(Contrato, models.DO_NOTHING, blank=True, null=True)
    parceiro = models.ForeignKey('Parceiro', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    emprestimo = models.ForeignKey(Emprestimo, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    recebimento = models.ForeignKey('Recebimento', models.DO_NOTHING, blank=True, null=True)
    deletado = models.BooleanField(blank=True, null=True)
    inativo = models.BooleanField(blank=True, null=True)
    configuracao_eletrica = models.ForeignKey(ConfiguracaoEletrica, models.DO_NOTHING, blank=True, null=True)
    id_plataforma_antiga = models.CharField(max_length=32, blank=True, null=True)
    codigo_rastreamento_string_box = models.CharField(max_length=64, blank=True, null=True)
    tipo = models.ForeignKey('TipoDeFinanciamento', models.DO_NOTHING, blank=True, null=True)
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING, blank=True, null=True)
    bancarizadora = models.ForeignKey(Bancarizadora, models.DO_NOTHING, blank=True, null=True)
    alteracao_na_instalacao = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'financiamento'


class FinanciamentoCancelado(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    comentario = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    motivo = models.ForeignKey('FinanciamentoMotivoCancelamento', models.DO_NOTHING)
    state = models.CharField(max_length=255)
    observacoes = models.TextField(blank=True, null=True)  # This field type is a guess.
    tipo = models.CharField(max_length=255)
    cnab = models.JSONField(blank=True, null=True)
    parceiro_signatario = models.JSONField(blank=True, null=True)
    versao = models.CharField(max_length=255, blank=True, null=True)
    erros = models.TextField(blank=True, null=True)  # This field type is a guess.
    financiamento_ultimo_status = models.CharField(max_length=255, blank=True, null=True)
    cnab_baixado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'financiamento_cancelado'


class FinanciamentoMotivoCancelamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'financiamento_motivo_cancelamento'


class FinanciamentoPontuacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nota = models.IntegerField(blank=True, null=True)
    editavel = models.BooleanField(blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'financiamento_pontuacao'


class FinanciamentoSeguroTaxa(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    premio_bruto = models.FloatField(blank=True, null=True)
    valor_adicional_parcela = models.FloatField(blank=True, null=True)
    premio_liquido = models.FloatField(blank=True, null=True)
    valor_comissao_solfacil = models.FloatField(blank=True, null=True)
    valor_comissao_parceiro = models.FloatField(blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    seguro_taxa = models.ForeignKey('SeguroTaxa', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'financiamento_seguro_taxa'


class Formalizacao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    acao = models.TextField()
    ativo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formalizacao'


class Fornecedor(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nome_do_fornecedor = models.CharField(max_length=64, blank=True, null=True)
    nome_do_contato = models.CharField(max_length=64, blank=True, null=True)
    contato = models.ForeignKey(Contato, models.DO_NOTHING, blank=True, null=True)
    dado_bancario = models.ForeignKey(DadoBancario, models.DO_NOTHING, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=True, null=True)
    cnpj = models.CharField(max_length=32, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fornecedor'


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'group'


class HistoricoCcb(models.Model):
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    ccb = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'historico_ccb'


class Homologacao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    etapa = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    titular = models.ForeignKey('Titular', models.DO_NOTHING, blank=True, null=True)
    unidade_geradora = models.ForeignKey('UnidadeGeradora', models.DO_NOTHING, blank=True, null=True)
    endereco = models.ForeignKey(Endereco, models.DO_NOTHING, blank=True, null=True)
    comentarios_do_integrador = models.TextField(blank=True, null=True)
    parceiro = models.ForeignKey('Parceiro', models.DO_NOTHING, blank=True, null=True)
    documentacao = models.ForeignKey(Documentacao, models.DO_NOTHING, blank=True, null=True)
    inversores = models.TextField(blank=True, null=True)
    modulo = models.TextField(blank=True, null=True)
    quantidade_de_modulos = models.IntegerField(blank=True, null=True)
    stringbox = models.CharField(max_length=64, blank=True, null=True)
    servico = models.CharField(max_length=255, blank=True, null=True)
    modulo_1 = models.IntegerField(blank=True, null=True)
    quantidade_de_modulos_1 = models.IntegerField(blank=True, null=True)
    modulo_manual_1 = models.CharField(max_length=255, blank=True, null=True)
    modulo_2 = models.IntegerField(blank=True, null=True)
    quantidade_de_modulos_2 = models.IntegerField(blank=True, null=True)
    modulo_manual_2 = models.CharField(max_length=255, blank=True, null=True)
    inversor_1 = models.IntegerField(blank=True, null=True)
    inversor_manual_1 = models.CharField(max_length=255, blank=True, null=True)
    inversor_2 = models.IntegerField(blank=True, null=True)
    inversor_manual_2 = models.CharField(max_length=255, blank=True, null=True)
    inversor_3 = models.IntegerField(blank=True, null=True)
    inversor_manual_3 = models.CharField(max_length=255, blank=True, null=True)
    possui_stringbox = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'homologacao'


class IndiceSolarimetrico(models.Model):
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    media = models.FloatField(blank=True, null=True)
    indice_solarimetrico_mensal = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indice_solarimetrico'
        unique_together = (('latitude', 'longitude'),)


class Instalacao(models.Model):
    foto_da_nota_fiscal = models.TextField(blank=True, null=True)
    foto_ou_video_telhado = models.TextField(blank=True, null=True)
    video_desligamento_remoto = models.TextField(blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    acesso_ao_monitoramento = models.BooleanField(blank=True, null=True)
    foto_ou_video_inversores = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    login_monitoramento = models.CharField(max_length=128, blank=True, null=True)
    senha_monitoramento = models.CharField(max_length=64, blank=True, null=True)
    pagamento_realizado = models.BooleanField()
    configuracao_eletrica = models.ForeignKey(ConfiguracaoEletrica, models.DO_NOTHING, blank=True, null=True)
    ampera_ativado = models.BooleanField(blank=True, null=True)
    data_ativacao_ampera = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instalacao'


class Inversor(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    configuracao_eletrica = models.ForeignKey(ConfiguracaoEletrica, models.DO_NOTHING)
    modelo = models.ForeignKey('ModeloDeInversor', models.DO_NOTHING)
    numero_telefone_sim = models.CharField(max_length=32, blank=True, null=True)
    senha_sim = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inversor'


class Lead(models.Model):
    nome = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    celular = models.CharField(max_length=32, blank=True, null=True)
    cep = models.CharField(max_length=32, blank=True, null=True)
    origem = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    estado = models.ForeignKey(Estado, models.DO_NOTHING, blank=True, null=True)
    assunto = models.TextField(blank=True, null=True)
    mensagem = models.TextField(blank=True, null=True)
    local = models.TextField(blank=True, null=True)
    cenario = models.TextField(blank=True, null=True)
    media_luz = models.FloatField(blank=True, null=True)
    parcela = models.FloatField(blank=True, null=True)
    prazo = models.IntegerField(blank=True, null=True)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, blank=True, null=True)
    cpf = models.CharField(max_length=16, blank=True, null=True)
    aprovado_pre_analise = models.BooleanField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lead'


class LeadHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    lead = models.ForeignKey(Lead, models.DO_NOTHING, blank=True, null=True)
    parceiro = models.ForeignKey('Parceiro', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lead_history'


class MailQueue(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    to = models.CharField(max_length=64, blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    when = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(blank=True, null=True)
    subject = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_queue'


class ModeloDeInversor(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    marca = models.CharField(max_length=64, blank=True, null=True)
    potencia = models.FloatField(blank=True, null=True)
    modelo = models.CharField(max_length=64, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    tensao = models.IntegerField(blank=True, null=True)
    fase = models.IntegerField(blank=True, null=True)
    chave_contatora = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modelo_de_inversor'


class Modulo(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    potencia = models.FloatField(blank=True, null=True)
    marca = models.CharField(max_length=64, blank=True, null=True)
    modelo = models.CharField(max_length=64, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modulo'


class Monitoramento(models.Model):
    codigos_monitoramento = models.TextField(blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    pagamento_realizado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'monitoramento'


class Mppt(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    numero_de_strings_eletricas = models.IntegerField(blank=True, null=True)
    modulos_por_strings_eletricas = models.IntegerField(blank=True, null=True)
    modulo = models.ForeignKey(Modulo, models.DO_NOTHING, blank=True, null=True)
    inversor = models.ForeignKey(Inversor, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mppt'


class ObanBeats(models.Model):
    node = models.TextField()
    queue = models.TextField()
    nonce = models.TextField()
    limit = models.IntegerField()
    paused = models.BooleanField()
    running = models.TextField()  # This field type is a guess.
    inserted_at = models.DateTimeField()
    started_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oban_beats'


class ObanJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.TextField()  # This field type is a guess.
    queue = models.TextField()
    worker = models.TextField()
    args = models.JSONField()
    errors = models.TextField()  # This field type is a guess.
    attempt = models.IntegerField()
    max_attempts = models.IntegerField()
    inserted_at = models.DateTimeField()
    scheduled_at = models.DateTimeField()
    attempted_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    attempted_by = models.TextField(blank=True, null=True)  # This field type is a guess.
    discarded_at = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField()
    tags = models.TextField(blank=True, null=True)  # This field type is a guess.
    meta = models.JSONField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oban_jobs'


class ObanProducers(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.TextField()
    node = models.TextField()
    queue = models.TextField()
    meta = models.JSONField()
    running_ids = models.TextField()  # This field type is a guess.
    started_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oban_producers'


class Pagamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pagamento'


class PagamentoLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=255)
    mensagem = models.TextField()
    metadata = models.JSONField(blank=True, null=True)
    pagamento = models.ForeignKey(Pagamento, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    transferencia = models.ForeignKey('Transferencia', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagamento_log'


class Parceiro(models.Model):
    cnpj = models.CharField(max_length=32, blank=True, null=True)
    valor_total_financiado = models.FloatField(blank=True, null=True)
    endereco = models.ForeignKey(Endereco, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    contato = models.ForeignKey(Contato, models.DO_NOTHING, blank=True, null=True)
    dado_bancario = models.ForeignKey(DadoBancario, models.DO_NOTHING, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=128, blank=True, null=True)
    pai = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    responsavel = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    onboarding_flexivel = models.BooleanField()
    beneficio_a_vista = models.CharField(max_length=32)
    franqueador = models.BooleanField(blank=True, null=True)
    cnpj_no_contrato = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.TextField(blank=True, null=True)  # This field type is a guess.
    ativo = models.BooleanField(blank=True, null=True)
    recebe_leads = models.BooleanField(blank=True, null=True)
    cnpj_de_pagamento = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parceiro'


class ParceiroFornecedor(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    parceiro = models.OneToOneField(Parceiro, models.DO_NOTHING, blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parceiro_fornecedor'


class ParceiroNivel(models.Model):
    nivel = models.IntegerField()
    parceiro = models.OneToOneField(Parceiro, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'parceiro_nivel'


class ParceiroPlano(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    parceiro = models.ForeignKey(Parceiro, models.DO_NOTHING, blank=True, null=True)
    plano = models.ForeignKey('Plano', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parceiro_plano'
        unique_together = (('parceiro', 'plano'),)


class ParceiroPontuacao(models.Model):
    etapa = models.CharField(max_length=64)
    pontuacao = models.SmallIntegerField()
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parceiro_pontuacao'
        unique_together = (('financiamento', 'etapa'), ('financiamento', 'etapa'),)


class ParceiroStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    parceiro = models.ForeignKey(Parceiro, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    ativo = models.BooleanField()
    motivo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'parceiro_status'


class Parcela(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    numero_de_parcelas = models.IntegerField(blank=True, null=True)
    valor_da_parcela = models.FloatField(blank=True, null=True)
    taxa_de_juros = models.FloatField(blank=True, null=True)
    taxa_de_cadastro = models.FloatField(blank=True, null=True)
    cotacao = models.ForeignKey(Cotacao, models.DO_NOTHING, blank=True, null=True)
    iof = models.FloatField(blank=True, null=True)
    valor_da_comissao = models.FloatField(blank=True, null=True)
    cet = models.CharField(max_length=16, blank=True, null=True)
    is_valid = models.BooleanField(blank=True, null=True)
    aliquota_iof = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parcela'


class Pesquisa(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    id = models.UUIDField(primary_key=True)
    homologacao = models.FloatField(blank=True, null=True)
    instalacao = models.FloatField(blank=True, null=True)
    satisfacao = models.FloatField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    financiamento = models.OneToOneField(Financiamento, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pesquisa'


class Plano(models.Model):
    nome = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'plano'


class Prazo(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    numero_de_parcelas = models.IntegerField(blank=True, null=True)
    taxa_de_juros = models.FloatField(blank=True, null=True)
    taxa_iof_sobre_valor_com_iof = models.FloatField(blank=True, null=True)
    taxa_iof_sobre_valor_sem_iof = models.FloatField(blank=True, null=True)
    porcentagem_tc = models.FloatField(blank=True, null=True)
    calculadora = models.ForeignKey(Calculadora, models.DO_NOTHING, blank=True, null=True)
    cet = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'prazo'


class ProdutoFinanceiro(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    template = models.CharField(max_length=255)
    cnab = models.CharField(max_length=255, blank=True, null=True)
    nome = models.CharField(unique=True, max_length=255)
    porcentagem_aquisicao = models.FloatField(blank=True, null=True)
    cnpj = models.CharField(max_length=32, blank=True, null=True)
    razao_social = models.CharField(max_length=128, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto_financeiro'


class ProdutoRural(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nome = models.TextField()
    nome_registrado = models.TextField()
    classe = models.TextField()
    unidade_medida = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_atualizado_em = models.DateField()
    area_atuacao = models.ForeignKey(AreaAtuacao, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'produto_rural'


class Profissao(models.Model):
    nome_profissao = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profissao'


class Projeto(models.Model):
    potencia_do_sistema = models.FloatField(blank=True, null=True)
    potencia_dos_inversores = models.FloatField(blank=True, null=True)
    conta_de_luz = models.TextField(blank=True, null=True)
    proposta_comercial = models.TextField(blank=True, null=True)
    fotos_e_videos = models.TextField(blank=True, null=True)
    print_google_maps = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    conta_de_luz_no_nome_do_cliente = models.BooleanField(blank=True, null=True)
    endereco = models.ForeignKey(Endereco, models.DO_NOTHING, blank=True, null=True)
    wifi = models.BooleanField(blank=True, null=True)
    conta_de_luz_consumidores_adicionais = models.TextField(blank=True, null=True)
    distribuidor = models.ForeignKey(Distribuidor, models.DO_NOTHING, blank=True, null=True)
    modulo = models.ForeignKey(Modulo, models.DO_NOTHING, blank=True, null=True)
    quantidade_de_modulos = models.IntegerField(blank=True, null=True)
    fase_rede_eletrica = models.IntegerField(blank=True, null=True)
    geracao_estimada = models.FloatField(blank=True, null=True)
    nivel_exposicao = models.FloatField(blank=True, null=True)
    quebra_de_expectativa = models.FloatField(blank=True, null=True)
    aprovado_automaticamente = models.BooleanField(blank=True, null=True)
    potencia_original_do_sistema = models.FloatField(blank=True, null=True)
    potencia_original_dos_inversores = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projeto'


class RealWatts(models.Model):
    id = models.BigAutoField(primary_key=True)
    kwp_min = models.FloatField(blank=True, null=True)
    kwp_max = models.FloatField(blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'real_watts'


class Recebimento(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    modelo_de_recebimento = models.CharField(max_length=16, blank=True, null=True)
    modelo_de_emissao_de_nota = models.CharField(max_length=16, blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, models.DO_NOTHING, blank=True, null=True)
    comprovante_de_pedido = models.TextField(blank=True, null=True)
    boleto_da_compra = models.TextField(blank=True, null=True)
    comentarios_adicionais = models.TextField(blank=True, null=True)
    valor_do_equipamento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pagamento_realizado = models.BooleanField()
    comissao = models.TextField(blank=True, null=True)
    email_enviado = models.DateTimeField(blank=True, null=True)
    email_contato_fornecedor = models.CharField(max_length=64, blank=True, null=True)
    fornecedor_pago = models.BooleanField()
    opcao_marketplace = models.BooleanField()
    nome_outro_fornecedor = models.TextField(blank=True, null=True)
    marketplace_product_details = models.JSONField(blank=True, null=True)
    aceite_fixadores = models.BooleanField(blank=True, null=True)
    nota_fiscal_servico = models.TextField(blank=True, null=True)
    valor_diferenca_vkit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comprovante_diferenca_vkit = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recebimento'


class RelatorioAcesso(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tipo = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'relatorio_acesso'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    slug_role = models.CharField(max_length=255)
    system_profile = models.ForeignKey('SystemProfile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'role'


class SchemaMigrations(models.Model):
    version = models.BigIntegerField(primary_key=True)
    inserted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schema_migrations'


class Seguradora(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    razao_social = models.TextField()
    cnpj = models.CharField(unique=True, max_length=14)
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'seguradora'


class Seguro(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nome = models.TextField()
    descricao = models.TextField()
    ativo = models.BooleanField()
    inicio_vigencia = models.DateTimeField()
    fim_vigencia = models.DateTimeField(blank=True, null=True)
    seguradora = models.ForeignKey(Seguradora, models.DO_NOTHING)
    tipo = models.ForeignKey('SeguroTipo', models.DO_NOTHING)
    faq_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguro'


class SeguroCobertura(models.Model):
    id = models.BigAutoField(primary_key=True)
    seguro = models.ForeignKey(Seguro, models.DO_NOTHING)
    cobertura = models.ForeignKey(Cobertura, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'seguro_cobertura'


class SeguroEmprestimo(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    valor_adicional_parcela = models.FloatField()
    emprestimo = models.ForeignKey(Emprestimo, models.DO_NOTHING)
    financiamento_seguro_taxa = models.ForeignKey(FinanciamentoSeguroTaxa, models.DO_NOTHING)
    premio_bruto = models.FloatField(blank=True, null=True)
    premio_liquido = models.FloatField(blank=True, null=True)
    valor_comissao_solfacil = models.FloatField(blank=True, null=True)
    valor_comissao_parceiro = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguro_emprestimo'
        unique_together = (('emprestimo', 'financiamento_seguro_taxa'),)


class SeguroRegra(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tipo = models.TextField(blank=True, null=True)
    valor = models.IntegerField(blank=True, null=True)
    valor_literal = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguro_regra'
        unique_together = (('tipo', 'valor'), ('tipo', 'valor_literal'),)


class SeguroTaxa(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    imposto_premio = models.FloatField()
    comissao_solfacil = models.FloatField()
    comissao_parceiro = models.FloatField()
    taxa_premio_bruto = models.FloatField()
    inicio_vigencia = models.DateTimeField()
    fim_vigencia = models.DateTimeField(blank=True, null=True)
    seguro = models.ForeignKey(Seguro, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'seguro_taxa'


class SeguroTaxaRegra(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    seguro_taxa = models.ForeignKey(SeguroTaxa, models.DO_NOTHING, blank=True, null=True)
    seguro_regra = models.ForeignKey(SeguroRegra, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seguro_taxa_regra'
        unique_together = (('seguro_taxa', 'seguro_regra'),)


class SeguroTipo(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    nome = models.TextField()
    descricao = models.TextField()
    ativo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'seguro_tipo'


class ServicoEntrega(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=256)
    url = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    codigo = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servico_entrega'


class Signatario(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    tipo = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    request_signature_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'signatario'


class Simulacao(models.Model):
    nome_do_projeto = models.CharField(max_length=128, blank=True, null=True)
    valor_do_projeto = models.FloatField(blank=True, null=True)
    entrada = models.FloatField(blank=True, null=True)
    carencia = models.IntegerField(blank=True, null=True)
    geracao_mensal = models.IntegerField(blank=True, null=True)
    canal = models.CharField(max_length=32)
    tipo_de_financiamento = models.ForeignKey('TipoDeFinanciamento', models.DO_NOTHING)
    parceiro = models.ForeignKey(Parceiro, models.DO_NOTHING, blank=True, null=True)
    comissao = models.ForeignKey(Comissao, models.DO_NOTHING, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'simulacao'


class SmartMeter(models.Model):
    id = models.BigAutoField(primary_key=True)
    configuracao_eletrica = models.ForeignKey(ConfiguracaoEletrica, models.DO_NOTHING)
    dispositivo_solfacil_id = models.CharField(max_length=255, blank=True, null=True)
    data_envio = models.DateField(blank=True, null=True)
    codigo_rastreio = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smart_meter'


class SmartMeterInversor(models.Model):
    id = models.BigAutoField(primary_key=True)
    smart_meter = models.ForeignKey(SmartMeter, models.DO_NOTHING)
    inversor = models.ForeignKey(Inversor, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'smart_meter_inversor'


class Submissao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING, blank=True, null=True)
    analise = models.ForeignKey(Analise, models.DO_NOTHING, blank=True, null=True)
    data_de_submissao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submissao'


class SystemModule(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'system_module'


class SystemModulePermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    system_module = models.ForeignKey(SystemModule, models.DO_NOTHING)
    system_permission = models.ForeignKey('SystemPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_module_permission'


class SystemPermission(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'system_permission'


class SystemProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)
    managed_by = models.CharField(max_length=255)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'system_profile'


class SystemProfileModule(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    system_profile = models.ForeignKey(SystemProfile, models.DO_NOTHING)
    system_module = models.ForeignKey(SystemModule, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_profile_module'


class SystemRole(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'system_role'


class SystemRoleProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    system_role = models.ForeignKey(SystemRole, models.DO_NOTHING)
    system_profile = models.ForeignKey(SystemProfile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'system_role_profile'


class Tarifa(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nome = models.CharField(max_length=16)
    valor = models.FloatField()
    devolucao = models.FloatField(blank=True, null=True)
    distribuidor = models.ForeignKey(Distribuidor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tarifa'
        unique_together = (('nome', 'distribuidor'),)


class TermoAdesaoSeguro(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    # numero_da_proposta = models.BigAutoField()
    path_termo_assinado = models.TextField(blank=True, null=True)
    financiamento_seguro_taxa = models.ForeignKey(FinanciamentoSeguroTaxa, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'termo_adesao_seguro'


class TermoAutorizacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    etapa = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    usuario = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'termo_autorizacao'


class TipoDeFinanciamento(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nome = models.CharField(unique=True, max_length=32, blank=True, null=True)
    tipo = models.CharField(unique=True, max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_de_financiamento'


class TipoSimulacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(unique=True, max_length=255, blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)
    tipo_de_financiamento_id = models.IntegerField(blank=True, null=True)
    consumo_min = models.IntegerField(blank=True, null=True)
    consumo_max = models.IntegerField(blank=True, null=True)
    tarifa_classe = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tipo_simulacao'


class Titular(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nome_completo = models.CharField(max_length=64, blank=True, null=True)
    cpf = models.CharField(max_length=32, blank=True, null=True)
    contato = models.ForeignKey(Contato, models.DO_NOTHING, blank=True, null=True)
    razao_social = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'titular'


class TitularContaDeLuz(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    vinculo = models.TextField()
    vinculo_detalhe = models.TextField(blank=True, null=True)
    documento = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'titular_conta_de_luz'


class Transferencia(models.Model):
    public_id = models.UUIDField(unique=True)
    created_at = models.DateTimeField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    efetivado_em = models.DateTimeField(blank=True, null=True)
    etapa = models.CharField(max_length=64)
    id_externo = models.CharField(max_length=1, blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING)
    status = models.CharField(max_length=1)
    taxa_transferencia_fornecedor = models.DecimalField(max_digits=16, decimal_places=2)
    valor = models.DecimalField(max_digits=16, decimal_places=2)
    updated_at = models.DateTimeField(blank=True, null=True)
    pagamento = models.ForeignKey(Pagamento, models.DO_NOTHING, blank=True, null=True)
    recebedor = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    provedor = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'transferencia'
        unique_together = (('financiamento', 'etapa', 'recebedor'),)


class TransferenciaAuditoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    confirmado_por = models.ForeignKey('Users', models.DO_NOTHING)
    transferencia = models.ForeignKey(Transferencia, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'transferencia_auditoria'


class TransferenciaLog(models.Model):
    codigo = models.CharField(max_length=1, blank=True, null=True)
    created_at = models.DateTimeField()
    mensagem = models.CharField(max_length=1)
    transferencia = models.ForeignKey(Transferencia, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transferencia_log'


class UnidadeBeneficiaria(models.Model):
    id = models.BigAutoField(primary_key=True)
    homologacao = models.ForeignKey(Homologacao, models.DO_NOTHING)
    conta_de_luz = models.CharField(max_length=255, blank=True, null=True)
    comprovante_troca_titularidade = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'unidade_beneficiaria'


class UnidadeGeradora(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    potencia = models.FloatField(blank=True, null=True)
    corrente = models.FloatField(blank=True, null=True)
    numero_do_poste = models.FloatField(blank=True, null=True)
    consumo_remoto = models.BooleanField(blank=True, null=True)
    distribuidor = models.ForeignKey(Distribuidor, models.DO_NOTHING, blank=True, null=True)
    titular = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unidade_geradora'


class UserCredential(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)
    type = models.CharField(max_length=255)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_credential'


class UserStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    admin = models.ForeignKey('Users', models.DO_NOTHING)
    ativo = models.BooleanField()
    motivo = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_status'


class Users(models.Model):
    username = models.CharField(unique=True, max_length=64, blank=True, null=True)
    confirmed = models.BooleanField(blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    member_since = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    avatar_hash = models.CharField(max_length=32, blank=True, null=True)
    perfil = models.CharField(max_length=64)
    contato = models.ForeignKey(Contato, models.DO_NOTHING, blank=True, null=True)
    nome_completo = models.CharField(max_length=64, blank=True, null=True)
    parceiro = models.ForeignKey(Parceiro, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, models.DO_NOTHING, blank=True, null=True)
    viu_nova_home = models.BooleanField(blank=True, null=True)
    viu_informativo = models.BooleanField(blank=True, null=True)
    viu_informativo_desligamento_remoto = models.BooleanField()
    cpf = models.CharField(unique=True, max_length=16, blank=True, null=True)
    data_de_nascimento = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Validacao(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    comentario_para_o_parceiro = models.TextField(blank=True, null=True)
    comentario_interno = models.TextField(blank=True, null=True)
    financiamento = models.ForeignKey(Financiamento, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    etapa = models.CharField(max_length=32, blank=True, null=True)
    analise = models.ForeignKey(Analise, models.DO_NOTHING, blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    rascunho = models.BooleanField(blank=True, null=True)
    data_de_validacao = models.DateTimeField(blank=True, null=True)
    homologacao = models.ForeignKey(Homologacao, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'validacao'
