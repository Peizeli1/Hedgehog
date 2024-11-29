from libgravatar import Gravatar


def get_gravatar_url(email, size=120):
    """Return a URL to the user's gravatar."""
    gravatar_object = Gravatar(email)
    gravatar_url = gravatar_object.get_image(size=size, default='identicon')
    return gravatar_url


def get_mini_gravatar_url(email):
    """Return a URL to a miniature version of the user's gravatar."""
    return get_gravatar_url(email, size=60)