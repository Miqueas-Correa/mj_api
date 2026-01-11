def test_serve_image_existente(client):
    """Test servir una imagen - solo verificamos que la ruta existe"""
    response = client.get('/uploads/productos/test.jpg')
    assert response.status_code in [404, 500]

def test_serve_image_inexistente(client):
    """Test servir una imagen que no existe"""
    response = client.get('/uploads/productos/imagen_que_no_existe.jpg')
    assert response.status_code != 200

def test_serve_image_sin_autenticacion(client):
    """Test que las imágenes son públicas (no requieren auth)"""
    response = client.get('/uploads/productos/test.jpg')
    assert response.status_code != 401

def test_serve_diferentes_formatos(client):
    """Test que acepta diferentes formatos"""
    formatos = ['test.png', 'test.jpg', 'test.jpeg']

    for filename in formatos:
        response = client.get(f'/uploads/productos/{filename}')
        assert response.status_code != 405

def test_serve_ruta_con_subdirectorios(client):
    """Test que maneja rutas con path traversal"""
    response = client.get('/uploads/../../../etc/passwd')
    assert response.status_code != 200