import click

@click.command()
@click.argument('name')
def hello(name):
   click.echo('Hello %s!' % name)
