from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from app.models.user import users_collection
from app.models.user import User
from app.schemas.user_schema import UserSignup, UserEdit
from datetime import datetime, timedelta
from app.utils.jwt_handler import create_jwt_token
from app.database import users_collection
import uuid, random, string
from app.config import SMTP_USERNAME, SMTP_SERVER, SMTP_PORT, SMTP_PASSWORD



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# plan_durations = {
#     "monthly": 30,
#     "semiannual": 182,
#     "annual": 365,
# }

async def create_user(user_data: UserSignup, is_admin=False):
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise Exception("User already exists")

    hashed_pw = hash_password(user_data.password)
    # access_days = plan_durations.get(user_data.plan.lower(), 0)
    # access_expires = datetime.now() + timedelta(days=access_days)
    # access_code = str(uuid.uuid4())
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pw,
        is_admin=is_admin,
        # access_expires=access_expires,
        # access_code=access_code,
    )
    # print(user.dict())
    await users_collection.insert_one(user.dict())
    token = create_jwt_token({
        "email": user.email,
        "is_admin":user.is_admin
        })
    return {**user.dict(), "access_token": token}


async def update_user(email: str, user_update: UserEdit):
    existing_user = await users_collection.find_one({"email": email})
    if not existing_user:
        raise Exception("User doesn't exists")
    updates = {}

    if user_update.email:
        updates["email"] = user_update.email
    if user_update.password:
        updates["password"] = hash_password(user_update.password)

    if updates:
        await users_collection.update_one({"email": email}, {"$set": updates})
        existing_user.update(updates)  # update local dict with changes

    return existing_user

async def authenticate_user(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    # if not user["is_admin"] and user["access_expires"] < datetime.now():
    #     raise Exception("Access expired. Please renew.")
    return create_jwt_token({
        "email": user["email"],
        "is_admin": user["is_admin"]
        })

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

async def get_data(email):
    existing_user= await users_collection.find_one({"email": email})
    if not existing_user:
        raise Exception("User doesn't exist")
    return existing_user


async def forgot_password(email: str):
    existing_user = await users_collection.find_one({"email": email})
    if not existing_user:
        raise Exception("User doesn't exist")

    # 1. Generate a temporary password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    hashed_temp_password = hash_password(temp_password)
     # 2. Update password in the database
    await users_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed_temp_password}}
    )

    # 3. Send an email with the temporary password
    subject = "Your Temporary Password"
    sender_email = SMTP_USERNAME
    receiver_email = email

    html_content = f"""
    <html>
        <body>
            <h3>Hello {existing_user.get("username", "User")},</h3>
            <p>You requested a password reset. Here's your temporary password:</p>
            <p><b>{temp_password}</b></p>
            <p>Please login using this password and update it immediately.</p>
            <br>
            <p>Thanks,<br>Support Team</p>
        </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    part = MIMEText(html_content, "html")
    message.attach(part)
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Temporary password email sent.")
    except Exception as e:
        print("Error sending email:", str(e))
        raise Exception("Failed to send temporary password email")
    

# async def create_user(user_data):
#     existing_user = await users_collection.find_one({"email": user_data.email})
#     if existing_user:
#         return None
#     hashed_password = pwd_context.hash(user_data.password)
#     user = {
#         "username": user_data.username,
#         "email": user_data.email,
#         "password": hashed_password
#     }
#     await users_collection.insert_one(user)
#     return create_jwt_token({"email": user["email"]})
