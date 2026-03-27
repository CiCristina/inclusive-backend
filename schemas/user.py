from datetime import datetime

from pydantic import BaseModel, EmailStr


class AccessibilitySettings(BaseModel):
    libras: bool = False
    captions: bool = False
    high_contrast: bool = False
    screen_reader: bool = False
    font_size: str = "medium"  # 'small' | 'medium' | 'large'
    preferred_language: str = "pt"


class UserUpdate(BaseModel):
    name: str | None = None
    department: str | None = None
    role: str | None = None
    company_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    phone: str | None = None
    accessibility: AccessibilitySettings | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    user_type: str
    department: str | None
    role: str | None
    company_name: str | None
    avatar_url: str | None
    bio: str | None
    phone: str | None
    accessibility: AccessibilitySettings
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        # Flatten accessibility fields from the ORM object into the nested schema
        if hasattr(obj, "accessibility_libras"):
            data = {
                "id": obj.id,
                "email": obj.email,
                "name": obj.name,
                "user_type": obj.user_type,
                "department": obj.department,
                "role": obj.role,
                "company_name": obj.company_name,
                "avatar_url": obj.avatar_url,
                "bio": obj.bio,
                "phone": obj.phone,
                "created_at": obj.created_at,
                "accessibility": AccessibilitySettings(
                    libras=obj.accessibility_libras,
                    captions=obj.accessibility_captions,
                    high_contrast=obj.accessibility_high_contrast,
                    screen_reader=obj.accessibility_screen_reader,
                    font_size=obj.accessibility_font_size,
                    preferred_language=obj.preferred_language,
                ),
            }
            return cls(**data)
        return super().model_validate(obj, **kwargs)
