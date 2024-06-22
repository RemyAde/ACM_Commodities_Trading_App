from tortoise.contrib.pydantic import pydantic_model_creator
from db.models.admin import Admin


admin_pydantic = pydantic_model_creator(Admin, name="Admin")
admin_pydanticIn = pydantic_model_creator(Admin, name= "AdminIn", exclude_readonly=True)