invalid_data_for_user = (
    (
        {
            'email': 'invalid_email',
            'username': ' ',
            'password': 'valid_password',
            'first_name': 'John',
            'last_name': 'Smith',
        },
        ('email', 'username'),
    ),
    (
        {
            'email': 'valid_email@test.com',
            'username': ' ',
            'password': 'valid_password',
            'first_name': 'John',
            'last_name': 'Smith',
        },
        ('username',),
    ),
    (
        {
            'email': 'valid_email@test.com',
            'username': 'me',
            'password': 'valid_password',
            'first_name': 'John',
            'last_name': 'Smith',
        },
        ('username',),
    ),
    (
        {
            'email': 'valid_email@test.com',
            'username': 'a' * 151,
            'password': 'a' * 151,
            'first_name': 'a' * 151,
            'last_name': 'a' * 151,
        },
        ('username', 'password', 'first_name', 'last_name'),
    ),
    (
        {
            'email': 'valid_email@test.com',
            'username': 'valid_username',
            'password': 'valid_password',
        },
        ('first_name', 'last_name'),
    ),
)
