from solver.errors import UnsafeTaskError, InputTooLongError, \
    OutputTooLongError, ContentFilterError


error_codes = {
    UnsafeTaskError: 403,
    InputTooLongError: 400,
    OutputTooLongError: 400,
    ContentFilterError: 403
}
