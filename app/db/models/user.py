from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    hashed_password = fields.CharField(max_length=200, null=False)
    first_name = fields.CharField(max_length=30, null=True)
    last_name = fields.CharField(max_length=30, null=True)
    phone_number = fields.CharField(max_length=20, null=True)
    is_verified = fields.BooleanField(default=False)
    date_created = fields.DatetimeField(auto_now_add=True)
    profile_image = fields.CharField(max_length=200, null=True, default="profileDefault.jpg")

    class Meta:
        table = "users"