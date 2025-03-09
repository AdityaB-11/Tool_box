# File size limit (32MB)
MAX_CONTENT_LENGTH = 32 * 1024 * 1024

# Allowed file extensions (only images)
ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'webp', 'tiff', 'bmp', 'gif', 'ico', 'heic'
}

# File cleanup settings
CLEANUP_INTERVAL = 3600  # 1 hour
FILE_EXPIRY_TIME = 3600  # 1 hour 