import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
JWT_SECRET = os.getenv("JWT_SECRET", "chupchodu")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY",None)
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY",None)
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET",None)

STABLE_DIFFUSION=os.getenv("STABLE_DIFFUSION",None)