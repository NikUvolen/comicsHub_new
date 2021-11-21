class ImageUploadHelper:

    FIELD_TO_COMBINE_MAP = {
        'defaults': {
            'upload_postfix': 'uploads'
        },
        'Comics': {
            'field': 'slug',
            'upload_postfix': 'comics_images'
        },
        'Images': {
            'field': 'slug',
            'upload_postfix': 'comics_images'
        },
        'User': {
            'field': 'username',
            'upload_postfix': 'avatars'
        }
    }

    def __init__(self, field_name_to_combine, instance, filename, upload_postfix):
        self.field_name_to_combine = field_name_to_combine
        self.instance = instance
        self.extension = filename.split('.')[-1]
        self.upload_postfix = f'_{upload_postfix}'

    @classmethod
    def get_field_to_combine_and_upload_postfix(cls, klass):
        field_to_combine = cls.FIELD_TO_COMBINE_MAP[klass]['field']
        upload_postfix = cls.FIELD_TO_COMBINE_MAP.get(
            'upload_postfix', cls.FIELD_TO_COMBINE_MAP['defaults']['upload_postfix']
        )
        return field_to_combine, upload_postfix

    def get_attr(self):
        field_to_combine = getattr(self.instance, self.field_name_to_combine)
        filename = '.'.join([field_to_combine, self.extension])
        return field_to_combine, filename

    @property
    def path(self):
        field_to_combine, filename = self.get_attr()
        return f'images/{self.instance.__class__.__name__.lower()}{self.upload_postfix}/{field_to_combine}/{filename}'

    @property
    def image_path(self):
        field_to_combine = getattr(self.instance.comics_id, self.field_name_to_combine)
        filename = '.'.join([field_to_combine, self.extension])
        return f'images/{self.instance.comics_id.__class__.__name__.lower()}{self.upload_postfix}/{self.instance.comics_id.slug}/images/{filename}'

    @property
    def avatar_path(self):
        field_to_combine = getattr(self.instance, self.field_name_to_combine)
        filename = '.'.join([field_to_combine, self.extension])
        return f'images/{self.instance.__class__.__name__.lower()}{self.upload_postfix}/{filename}'


def _get_image(instance, filename):
    if hasattr(instance, 'content_object'):
        instance = instance.content_object
    field_to_combine, upload_postfix = ImageUploadHelper.get_field_to_combine_and_upload_postfix(
        instance.__class__.__name__
    )
    image = ImageUploadHelper(field_to_combine, instance, filename, upload_postfix)
    return image


def upload_function(instance, filename):
    image = _get_image(instance, filename)
    return image.path


def upload_user_avatars_func(instance, filename):
    image = _get_image(instance, filename)
    return image.avatar_path


def upload_comics_images(instance, filename):
    field_to_combine, upload_postfix = ImageUploadHelper.get_field_to_combine_and_upload_postfix(
        instance.comics_id.__class__.__name__
    )
    image = ImageUploadHelper(field_to_combine, instance, filename, upload_postfix)
    return image.image_path
