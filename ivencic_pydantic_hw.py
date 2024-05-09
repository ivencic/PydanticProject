from pydantic import BaseModel, EmailStr, Field, field_validator


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator('name')
    def check_name(cls, v: str):
        if not v.isalpha():
            raise ValueError('Имя должно содержать только буквы')
        return v

    @field_validator('age')
    def check_age(cls, v: int, values: str):
        if not values and v < 18:
            raise ValueError('Пользователь должен быть старше 18 лет')
        return v


def process_json(json_str: str) -> str:
    try:
        user_data = User.parse_raw(json_str)
        return user_data.json()
    except Exception as e:
        return str(e)


norm_json = '''
{
    "name": "Вася",
    "age": 31,
    "email": "vasea@email.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Peipziger str",
        "house_number": 159
    }
}
'''

no_valid_json = '''
{
    "name": "Alice1",
    "age": 150,
    "email": "invalid_email",
    "is_employed": false,
    "address": {
        "city": "LA",
        "street": "1st",
        "house_number": -5
    }
}
'''

print(process_json(norm_json))
print(process_json(no_valid_json))
