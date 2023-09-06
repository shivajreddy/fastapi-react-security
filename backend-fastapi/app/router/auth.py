import secrets
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from app.database import db
from app.oauth2 import create_access_token, create_refresh_token, verify_refresh_token, get_current_user_data
from app.schema import User, NewUserSchema
from app.utils import hash_password, verify_password

router = APIRouter()


# Register a new user
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(payload: NewUserSchema):
    # Check if user already exist
    user_coll = db["users"]
    existing_user = user_coll.find_one({"username": payload.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exist"
        )

    # create new User object
    new_user = User(
        username=payload.username,
        hashed_password=hash_password(payload.plain_password),  # Hash the password
    )
    # set roles, other properties
    new_user.roles = [101]
    new_user.created_at = datetime.utcnow().isoformat()

    # add verified status to false.
    new_user.verified = False

    # add to DB
    inserted_id = user_coll.insert_one(new_user.model_dump()).inserted_id

    # create JWTs -> access-token & refresh-token
    access_token = create_access_token(data=new_user)

    refresh_token = create_refresh_token(data=new_user)

    # create a secret key, to email them for verifying email
    email_verification_key = secrets.token_urlsafe(16)

    # add refresh_token to document
    user_coll.update_one(
        {"_id": inserted_id},
        {"$set": {**new_user.model_dump(), "refresh_token": refresh_token}},
    )

    # create a ppty in the document to save the secret key

    response = JSONResponse(
        content={"access_token": access_token, "token_type": "Bearer"}
    )
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=86400
    )
    return response


@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # async def login_user(payload: LoginUserSchema, response: Response):
    user_coll = db["users"]
    # user_doc = user_coll.find_one({"username": payload.email})
    user_doc = user_coll.find_one({"username": form_data.username})

    # print(f"✅ user_in_db: {user_doc}, type: {type(user_doc)}")

    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User email doesn't exist"
        )

    # evaluate password
    # if not verify_password(payload.password, user_doc.get("hashed_password")):
    if not verify_password(form_data.password, user_doc.get("hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password"
        )

    # create JWTs -> access-token & refresh-token
    user = User(
        # **user_doc
        username=user_doc["username"],
        hashed_password=user_doc["hashed_password"],
        roles=user_doc["roles"],
        verified=True,
        created_at=user_doc["created_at"],
    )

    access_token = create_access_token(data=user)
    refresh_token = create_refresh_token(data=user)

    # update refresh_token in the document
    user_coll.update_one(user_doc, {"$set": {"refresh_token": refresh_token}})

    # store refresh and access token in cookie
    response = JSONResponse(
        content={"status": "success", "access_token": access_token, "roles": user.roles}
    )
    response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=86400)
    return response


@router.get("/refresh")
def refresh(request: Request):
    # print("🔥cookies:", request.cookies)

    if "refresh_token" not in request.cookies:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No Refresh Token in cookies",
        )
    refresh_token = request.cookies["refresh_token"]

    refresh_token_data = verify_refresh_token(refresh_token)
    # print("👾 refresh_token is validated:", refresh_token_data)

    user_coll = db["users"]
    user_doc = user_coll.find_one({"username": refresh_token_data.username})
    # print("🍔 user_doc:", user_doc)

    user_data = {k: v for (k, v) in user_doc.items() if k != "_id"}
    user = User(**user_data)
    # print("☺️ user=", user)

    new_access_token = create_access_token(data=user)
    # print("✅ new_access_token", new_access_token)

    return {
        "username": user.username,
        "roles": user.roles,
        "new_access_token": new_access_token,
    }


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"status": "successfully logged out"}


@router.get("/reset-password")
async def reset_password(
        current_user_data: Annotated[User, Depends(get_current_user_data)]
):
    # only logged-in users can view this page
    # print("current-user:", current_user_data)
    pass


@router.get("/forgot-password")
async def forgot_password():
    # open for public
    # get the user-name, make sure he/she
    # set verified status to False

    # create secret
    forgot_password_secret = secrets.token_urlsafe(16)

    # email secret
    pass


@router.get("/forgot-password/confirmation/{secret_key}")
async def forgot_password_confirmation(secret_key: str):
    # get the
    print("given secret_key", secret_key)

    # get the secret_key from DB
    secret_key_from_db = None

    # verify both equal

    # get the new password

    # hash the new password
    new_hashed_password = None

    # save the new_hashed_password in db

    # send tokens


@router.get("/confirm-registration/{email_verification_key}")
async def confirm_registration(email_verification_key: str):
    # set the verified status to True
    print("given key", email_verification_key)

    # get the user, and his email_verification_key

    # validate key

    # set the verification status to true.
    # delete the email_verification_key
    pass


@router.post("/update-password")
async def update_password(
        new_plain_password: str,
        current_user_data: Annotated[User, Depends(get_current_user_data)],
):
    print(current_user_data)

    # hash the new password
    print("new_password given:", new_plain_password)

    # save the hashed password to db
    new_hashed_password = hash_password(new_plain_password)


@router.get("/users")
async def get_all_users(
        current_user_data: Annotated[User, Depends(get_current_user_data)]
):
    print(f"you are, {current_user_data}")
    user_coll = db["users"]
    result = []
    for doc in list(user_coll.find()):
        data = {k: v for (k, v) in doc.items() if k != "_id"}
        result.append(data)
    return result


@router.get("/test")
async def testing_protected_route(
        current_user_data: Annotated[User, Depends(get_current_user_data)]
):
    return f"you are, {current_user_data}"
