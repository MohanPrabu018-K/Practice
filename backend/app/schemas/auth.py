from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str; email: str; password: str

class LoginRequest(BaseModel):
    username: str; password: str

class TokenResponse(BaseModel):
    access_token: str; refresh_token: str; token_type: str = "bearer"
    username: str; email: str; role: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserOut(BaseModel):
    id: int; username: str; email: str; role: str
    phone: str | None = None; avatar_url: str | None = None
    model_config = {"from_attributes": True}

class ProfileUpdate(BaseModel):
    email: str | None = None; phone: str | None = None
    avatar_url: str | None = None

class PasswordChange(BaseModel):
    old_password: str; new_password: str
