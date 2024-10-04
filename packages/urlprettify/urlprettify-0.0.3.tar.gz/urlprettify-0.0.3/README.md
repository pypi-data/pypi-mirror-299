# Пакет для преобразования URL к удобному виду

## Как пользоваться?
    import urlprettify

    ugly_url = "hxxxfd[:]//test[.]io/spam.php"
    pretty_url = urlprettify.prettify(ugly_url)

## Сборка пакета и отправка в TestPyPI

https://packaging.python.org/en/latest/tutorials/packaging-projects/

### Добавить пакет в список установленных, но с возможностью редактирования
    python3 -m pip install -e .
    python3 -m pip list -e

### Настроить pyproject.toml и собрать пакеты sdist и wheel
    python3 -m build
    python3 -m twine upload --repository testpypi dist/*