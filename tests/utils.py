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


def check_pagination(
    url: str, response_data: dict, expected_count: int, post_data=None
):
    expected_keys = ('count', 'next', 'previous', 'results')
    for key in expected_keys:
        assert (
            key in response_data
        ), f'На `{url}` должна быть пагинация. Отсутствует ключ {key}.'

    assert response_data['count'] == expected_count, (
        f'На `{url}` должна быть пагинация. '
        f'Ключ `count` содержит некорректное значение.'
    )
    assert isinstance(response_data['results'], list), (
        f'На `{url}` должна быть пагинация. '
        'Значением ключа `results` должен быть список.'
    )
    assert len(response_data['results']) == expected_count, (
        f'На `{url}` должна быть пагинация. '
        'Ключ `results` содержит некорректное количество элементов.'
    )
    if post_data:
        assert post_data in response_data['results'], (
            f'На `{url}` должна быть пагинация. '
            'Значение параметра `results` отсутствует или некорректно.'
        )
