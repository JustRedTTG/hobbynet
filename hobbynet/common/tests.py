def format_validation_errors(errors):
    return '\n'.join([f"    - {', '.join(err)}" for err in errors])


def format_errors(errors):
    error_string = '\n'.join(
        [f"  > {name}:\n{format_validation_errors(errs)}" for name, errs in errors.as_data().items()])
    return '\n'.join(('Form Errors:', error_string))


def model_blank_to_null(kwargs):
    kwargs = kwargs.copy()
    for key, value in kwargs.items():
        if value.strip() == '':
            kwargs[key] = None
    return kwargs
