from django.conf.urls import include, url
from django.core.urlresolvers import reverse

__all__ = [
    'Process', 'Step', 'get_current_steps', 'get_url',
    'get_current_step', 'get_current_url',
    'get_next_step', 'get_next_url',
    'get_previous_step', 'get_previous_url',
]


class Process(object):
    views = []

    @classmethod
    def as_views(cls, namespace=None):
        return include(cls(), namespace=namespace)

    def urls(self):
        urls = []
        self._map = []
        for idx, view in enumerate(self.views):
            if isinstance(view, Step):
                step = view
            elif isinstance(view, tuple):
                step = Step(*view)
            elif callable(view):
                step = Step(view)
            step._index = idx
            step._steps = self
            self._map.append(step)
            urls.append(step.urlpattern)
        return urls

    @property
    def urlpatterns(self):
        return self.urls()

    def has_next(self, step):
        return step.index < len(self.views) - 1

    def has_previous(self, step):
        return step.index > 0

    def current(self, step):
        return self._map[step.index]

    def next(self, step):
        return self._map[step.index + 1] if self.has_next(step) else None

    def previous(self, step):
        return self._map[step.index - 1] if self.has_previous(step) else None

    def __iter__(self):
        return iter(self._map)


class Step(object):

    do_not_call_in_templates = True  # Django magic

    def __init__(self, view, name=None, title=None, pattern=None):
        self.view = view
        self.name = name if name else view.__name__
        self.title = title if title else self.name.title()
        self.pattern = pattern if pattern else (r'^%s/$' % self.name)

    def __repr__(self):
        return 'Step(%r, name=%r, title=%r, pattern=%r)' % (
            self.view, self.name, self.title, self.pattern
        )

    def __call__(self, request, *args, **kwargs):
        return self.view(request, *args, **kwargs)

    @property
    def urlpattern(self):
        return url(self.pattern, self, name=self.name)

    @property
    def index(self):
        return self._index

    @property
    def steps(self):
        return self._steps


def _get_step(request, method):
    current_step = request.resolver_match.func
    if hasattr(current_step, 'steps') and isinstance(current_step.steps, Process):
        # Calls current(), next() or previous() on a Process instance
        return getattr(current_step.steps, method)(current_step)


def get_url(step, request, *args, **kwargs):
    if step:
        current_ns = request.resolver_match.namespace
        if current_ns:
            return reverse(
                '%s:%s' % (current_ns, step.name),
                args=args,
                kwargs=kwargs,
            )
        else:
            return reverse(step.name, args=args, kwargs=kwargs)
    return ''


def get_current_steps(request):
    current_step = request.resolver_match.func
    if hasattr(current_step, 'steps') and isinstance(current_step.steps, Process):
        return current_step.steps


def get_current_step(request):
    return _get_step(request, 'current')


def get_current_url(request, *args, **kwargs):
    return get_url(get_current_step(request), request, *args, **kwargs)


def get_next_step(request):
    return _get_step(request, 'next')


def get_next_url(request, *args, **kwargs):
    return get_url(get_next_step(request), request, *args, **kwargs)


def get_previous_step(request):
    return _get_step(request, 'previous')


def get_previous_url(request, *args, **kwargs):
    return get_url(get_previous_step(request), request, *args, **kwargs)
