import celery

from parsers import main

app = celery.Celery('parse')

class MyTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

@app.task(bind=True, max_retries=5, default_retry_delay=10)
def parsing_urls(*args):
    print(main())

links = parsing_urls()