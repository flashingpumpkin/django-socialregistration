import warnings

from socialregistration.contrib.facebook.middleware import FacebookMiddleware

warnings.warn("'socialregistration.middleware.FacebookMiddleware' will be removed. "
    "Use 'socialregistration.contrib.facebook.middleware.FacebookMiddleware' instead.")

