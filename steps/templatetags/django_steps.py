from django import template

from ..steps import (
    get_current_step, get_current_steps, get_current_url, get_next_step,
    get_next_url, get_previous_step, get_previous_url, get_url,
)

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_all_steps(context):
    return get_current_steps(context['request'])


@register.assignment_tag()
def step_attribute(step, attr):
    if step is not None and attr is not None:
        return getattr(step, attr)
    return step


@register.assignment_tag(takes_context=True)
def step_url(context, step, *args, **kwargs):
    return get_url(step, context['request'], *args, **kwargs)


@register.assignment_tag(takes_context=True)
def current_step(context, attr=None):
    step = get_current_step(context['request'])
    return step_attribute(step, attr)


@register.assignment_tag(takes_context=True)
def next_step(context, attr=None):
    step = get_next_step(context['request'])
    return step_attribute(step, attr)


@register.assignment_tag(takes_context=True)
def previous_step(context, attr=None):
    step = get_previous_step(context['request'])
    return step_attribute(step, attr)


@register.simple_tag(takes_context=True)
def current_step_url(context, *args, **kwargs):
    return get_current_url(context['request'], *args, **kwargs)


@register.simple_tag(takes_context=True)
def next_step_url(context, *args, **kwargs):
    return get_next_url(context['request'], *args, **kwargs)


@register.simple_tag(takes_context=True)
def previous_step_url(context, *args, **kwargs):
    return get_previous_url(context['request'], *args, **kwargs)
