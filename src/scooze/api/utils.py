from functools import cache


def _check_for_safe_context(function):
    """
    Wrapper to ensure an instance method of ScoozeApi is called in a safe
    context.
    """

    def wrapper_safe_context(self, *args, **kwargs):
        if not self.safe_context:
            raise RuntimeError("ScoozeApi used outside of 'with' context")
        return function(self, *args, **kwargs)

    return wrapper_safe_context


@cache
def _safe_cache(function):
    """
    Wrapper for cache to ensure incoming arguments are hashable.
    """

    def _convert_list_args_to_tuple(*args, **kwargs):
        # TODO(#207): additional behavior to convert non-hashable arguments to hashable to allow cache
        args = [tuple(x) if type(x) == list else x for x in args]
        kwargs = {k: tuple(x) if type(x) == list else x for k, x in kwargs.items()}
        result = function(*args, **kwargs)
        result = tuple(result) if type(result) == list else result
        return result

    return function
