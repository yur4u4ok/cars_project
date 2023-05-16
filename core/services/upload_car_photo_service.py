import os
from uuid import uuid1


def upload_to(instance, file: str) -> str:
    ext = file.split('.')[-1]
    return os.path.join(instance.user.email, f'{uuid1()}.{ext}')
