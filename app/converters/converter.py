import os
from PIL import Image
from ..utils.file_utils import get_file_extension, UPLOAD_DIR

# Import pillow_heif for HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False

class FileConverter:
    # Supported image formats
    IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'webp', 'tiff', 'bmp', 'gif', 'ico', 'heic']
    
    @staticmethod
    def convert_file(input_path, output_path, input_format, output_format):
        """Convert a file from input format to output format"""
        try:
            # Check for HEIC support
            if input_format.lower() == 'heic' and not HEIC_SUPPORT:
                raise Exception("HEIC format is not supported. Please install pillow-heif package.")
            
            # Only handle image conversions
            if input_format in FileConverter.IMAGE_FORMATS and output_format in FileConverter.IMAGE_FORMATS:
                FileConverter._convert_image(input_path, output_path, output_format)
            else:
                raise Exception(f"Unsupported conversion: {input_format} to {output_format}. Only image conversions are supported.")

            # Verify the output file exists
            if not os.path.exists(output_path):
                raise Exception("Conversion failed: Output file not created")

        except Exception as e:
            # Clean up output file if it exists
            if os.path.exists(output_path):
                os.remove(output_path)
            raise Exception(f"Conversion failed: {str(e)}")

    @staticmethod
    def _convert_image(input_path, output_path, output_format):
        """Convert image files"""
        try:
            with Image.open(input_path) as img:
                # Handle transparency for formats that don't support it
                if img.mode in ('RGBA', 'LA') and output_format in ['jpg', 'jpeg', 'bmp']:
                    bg = Image.new('RGB', img.size, 'WHITE')
                    bg.paste(img, mask=img.split()[-1])
                    img = bg
                
                # Handle specific format requirements
                if output_format == 'jpg' or output_format == 'jpeg':
                    img.convert('RGB').save(output_path, quality=95)
                elif output_format == 'png':
                    img.save(output_path, 'PNG')
                elif output_format == 'webp':
                    img.save(output_path, 'WEBP', quality=95)
                elif output_format == 'gif':
                    img.save(output_path, 'GIF')
                elif output_format == 'bmp':
                    img.save(output_path, 'BMP')
                elif output_format == 'tiff':
                    img.save(output_path, 'TIFF')
                elif output_format == 'ico':
                    # ICO requires specific sizes
                    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
                    img.save(output_path, 'ICO', sizes=sizes)
                elif output_format == 'heic':
                    if HEIC_SUPPORT:
                        img.save(output_path, format="HEIF", quality=95)
                    else:
                        raise Exception("HEIC format is not supported. Please install pillow-heif package.")
                else:
                    img.save(output_path)
        except Exception as e:
            raise Exception(f"Image conversion error: {str(e)}") 