import pytest
from fastapi import HTTPException

from main import normalizar_origem, valores_origem_para_consulta


def test_normalizar_origem_aceita_camara_sem_acento():
    assert normalizar_origem("Camara") == "Camara"


def test_normalizar_origem_aceita_camara_com_acento():
    assert normalizar_origem("Câmara") == "Camara"


def test_normalizar_origem_aceita_senado():
    assert normalizar_origem("Senado") == "Senado"


def test_normalizar_origem_rejeita_valor_invalido():
    with pytest.raises(HTTPException) as exc_info:
        normalizar_origem("Assembleia")

    assert exc_info.value.status_code == 400


def test_valores_origem_para_consulta_mantem_compatibilidade_com_camara_antiga():
    assert valores_origem_para_consulta("Camara") == ["Camara", "Câmara"]


def test_valores_origem_para_consulta_senado():
    assert valores_origem_para_consulta("Senado") == ["Senado"]