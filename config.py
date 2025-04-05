import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-for-development')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    # MongoDB configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/forensic_face_system')
    
    # File paths - UPDATED
    SEARCH_SYSTEM_DIR = r"E:\projects\Forensic\search_system_export_front_side\search_system_export_front_side"
    IMAGE_BASE_DIR = r"E:\projects\Forensic\idoc-mugshots\front\front"
    SIDE_IMAGE_DIR = r"E:\projects\Forensic\idoc-mugshots\side\side"
    METADATA_CSV_PATH = r"E:\projects\Forensic\idoc-mugshots\labels_utf8.csv"
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # Search thresholds
    THRESHOLD_TEXT = 125.0
    THRESHOLD_IMAGE = 15.0
    THRESHOLD_COMBINED = 40.0
    
    # CLIP model settings
    CLIP_MODEL = "ViT-B/32"

