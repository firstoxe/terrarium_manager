"""Shared helpers for safe internal redirects."""

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def safe_redirect(request, candidate=None, *, fallback='dashboard:dashboard'):
    """Redirect only to same-host relative URLs; otherwise use fallback name or path."""
    target = candidate
    if target is None:
        target = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
    if target and url_has_allowed_host_and_scheme(
        target,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(target)
    if fallback.startswith('/'):
        return redirect(fallback)
    return redirect(fallback)
