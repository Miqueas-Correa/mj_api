from app.service.usuarios_service import listar, obtener_U, crear, editar,check_password, eliminar

def test_listar():
    # prueba para el metodo listar sin errores y L_activos
    resultado = listar()
    assert isinstance(resultado, list)
    assert len(resultado) > 0
    # 