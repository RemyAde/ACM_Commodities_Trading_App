from tortoise import Model, fields


class Admin(Model):
    id = fields.IntField(pk=True, index=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    hashed_password = fields.CharField(max_length=200, null=False)

    class Meta:
        table = "admin"