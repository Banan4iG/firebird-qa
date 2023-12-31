#coding:utf-8

"""
ID:          issue-1928
ISSUE:       1928
TITLE:       Connection lost running script
DESCRIPTION:
JIRA:        CORE-1512
FBTEST:      bugs.core_1512
"""

import pytest
from firebird.qa import *

db = db_factory(charset='ISO8859_1')

test_script = """
    -- Confirmed crash on WI-V2.1.7.18553 for: CREATE TABLE FHO_OS(...)

    CREATE DOMAIN DM_COD AS
    NUMERIC(4,0);

    CREATE DOMAIN DM_COD2 AS
    NUMERIC(8,0);

    CREATE DOMAIN DM_DES AS
    VARCHAR(80)
    COLLATE PT_PT;

    CREATE DOMAIN DM_FONE AS
    VARCHAR(20)
    COLLATE PT_PT;

    CREATE DOMAIN DM_ID AS
    NUMERIC(4,0);

    CREATE DOMAIN DM_ID2 AS
    NUMERIC(8,0);

    CREATE DOMAIN DM_IMG AS
    BLOB SUB_TYPE 0 SEGMENT SIZE 4096;

    CREATE DOMAIN DM_IND AS
    CHAR(1)
    COLLATE PT_PT;

    CREATE DOMAIN DM_IND2 AS
    CHAR(2)
    COLLATE PT_PT;

    CREATE DOMAIN DM_NM AS
    VARCHAR(80)
    COLLATE PT_PT;

    CREATE DOMAIN DM_PWS AS
    VARCHAR(10)
    COLLATE PT_PT;

    CREATE DOMAIN DM_TP AS
    CHAR(1)
    COLLATE PT_PT;

    CREATE DOMAIN DM_TXT AS
    BLOB SUB_TYPE 1 SEGMENT SIZE 4096;

    CREATE TABLE FHO_ATIV_TEC (
        COD_USUARIO    DM_COD NOT NULL,
        DT_INICIO      TIMESTAMP NOT NULL,
        DT_TERMINO     TIMESTAMP,
        COD_ATIVIDADE  DM_COD2 NOT NULL,
        ID_OS          DM_ID2
    );

    CREATE TABLE FHO_OS (
        ID_OS                  DM_ID2 NOT NULL,
        DT_INICIO              TIMESTAMP NOT NULL,
        DT_TERMINO             TIMESTAMP,
        COD_FICHA              DM_COD2,
        COD_USUARIO            DM_COD NOT NULL,
        COD_ATIVIDADE          DM_COD2 NOT NULL,
        COD_PROJETO            DM_COD2,
        TXT_DESCRICAO          DM_TXT,
        IND_PENDENTE           DM_IND NOT NULL,
        IND_CANCELADO          DM_IND NOT NULL,
        ID_OS_ORIGEM           DM_ID2,
        COD_USUARIO_ENVIOU     DM_COD,
        NRO_PRIORIDADE         INTEGER,
        PERC_FATURAR           NUMERIC(5,2),
        TXT_DESCRICAO_TECNICA  DM_TXT,
        DT_PREVISAO_TERMINO    DATE,
        NM_CONTATO             DM_NM,
        IND_EXIBE_RELEASE      DM_IND,
        HRS_ORCAMENTO          NUMERIC(5,2),
        IND_STATUS             COMPUTED BY (CASE WHEN (FHO_OS.IND_CANCELADO <> 'N') THEN
                                                                  'CANCELADA'
                                                                WHEN (SELECT FIRST 1 (CASE WHEN T.DT_TERMINO IS NULL THEN 1 END) FROM FHO_ATIV_TEC T
                                                                      WHERE (T.COD_USUARIO = FHO_OS.COD_USUARIO) AND (T.ID_OS = FHO_OS.ID_OS) ORDER BY T.DT_INICIO DESC) IS NOT NULL THEN
                                                                  'EM USO'
                                                                WHEN (FHO_OS.DT_TERMINO IS NULL) THEN
                                                                  'ABERTA'
                                                                WHEN (FHO_OS.IND_PENDENTE = 'S') THEN
                                                                  'PENDENTE'
                                                                ELSE
                                                                  'FECHADA'
                                                                END),
        COD_TP_OS              DM_COD,
        HRS_CONTRATO           NUMERIC(5,2),
        HRS_PREVISAO_TERMINO   NUMERIC(5,2),
        PERC_HORA_MAQUINA      NUMERIC(5,2)
    );

"""

act = isql_act('db', test_script)

@pytest.mark.version('>=3')
def test_1(act: Action):
    act.execute()
