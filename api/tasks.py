from orders.celery import app

from api.management.commands.load_yaml import Command

@app.task
def do_import(url):
    load_yaml = Command()
    output = load_yaml.handle(url)
    return output
