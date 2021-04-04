from invoke import task


@task
def start(ctx):
    ctx.run("python src/index.py")
