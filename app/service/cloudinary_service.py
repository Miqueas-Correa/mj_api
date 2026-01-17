import cloudinary
import cloudinary.uploader

def init_cloudinary(app):
    cloudinary.config(
        cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=app.config.get('CLOUDINARY_API_KEY'),
        api_secret=app.config.get('CLOUDINARY_API_SECRET'),
        secure=True
    )

def upload_image(file, folder="productos"):
    """
    Sube una imagen a Cloudinary
    
    Args:
        file: El archivo de imagen (FileStorage de Flask)
        folder: Carpeta en Cloudinary donde guardar (opcional)
    
    Returns:
        URL segura de la imagen subida
    """
    try:
        # Subir a Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="auto",
            allowed_formats=['jpg', 'jpeg', 'png', 'gif', 'webp'],
            transformation=[
                {'width': 2000, 'height': 2000, 'crop': 'limit'},
                {'quality': 'auto:good'}
            ]
        )
        
        # Retornar la URL segura (HTTPS)
        return result['secure_url']
        
    except Exception as e:
        raise ValueError(f"Error al subir imagen a Cloudinary: {str(e)}")

def delete_image(image_url):
    """
    Elimina una imagen de Cloudinary
    
    Args:
        image_url: URL de la imagen a eliminar
    
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    try:
        if 'cloudinary.com' not in image_url:
            return False
            
        parts = image_url.split('/')
        if 'upload' in parts:
            upload_index = parts.index('upload')
            path_parts = parts[upload_index + 1:]
            
            # Si el primer elemento empieza con 'v' seguido de números, es la versión
            if path_parts[0].startswith('v') and path_parts[0][1:].isdigit():
                path_parts = path_parts[1:]
            
            # Unir el resto y quitar la extensión
            public_id = '/'.join(path_parts).rsplit('.', 1)[0]
            
            # Eliminar de Cloudinary
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
        
        return False
        
    except Exception as e:
        print(f"Error al eliminar imagen de Cloudinary: {str(e)}")
        return False