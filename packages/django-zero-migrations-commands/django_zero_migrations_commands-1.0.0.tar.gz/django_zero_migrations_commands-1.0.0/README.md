# django-shell-extended

Provides a `zeromigrations` management-command that creates and applies zero migrations
## Quick start
1. Install with `pip install django-zero-migrations-commands`
2. Add `"django-zeromigrations"` to your `INSTALLED_APPS` setting like this:
    ```python
    INSTALLED_APPS = [
        # ...
        "django-zero-migrations-commands",
    ]
    ```
3. (Optional) Change the settings described in the next section in your `settings.py`
4. Create zero migrations using `python manage.py zeromigrations create`
5. Apply them on other systems using `python manage.py zeromigrations apply`

## Available settings
```python
APPS: Optional[list[str]] = getattr(settings, 'ZERO_MIGRATIONS_APPS', None)
"""The apps to reset migrations for. default: `None`. Will reset migrations for all local apps if `None`."""

ALLOW_CREATE_DEBUG_FALSE: bool = getattr(settings, 'ZERO_MIGRATIONS_ALLOW_CREATE_DEBUG_FALSE', False)
"""Whether the create action can be run in `DEBUG = False` mode. default: `False`"""

CONFIRM_CREATE_DEBUG_FALSE = getattr(settings, 'ZERO_MIGRATIONS_CONFIRM_CREATE_DEBUG_FALSE', False)
"""Whether to ask for confirmation before running the create action in `DEBUG = False` mode. default: `False`"""

ALLOW_APPLY_DEBUG_FALSE: bool = getattr(settings, 'ZERO_MIGRATIONS_ALLOW_APPLY_DEBUG_FALSE', True)
"""Whether the apply action can be run in `DEBUG = False` mode. default: `True`"""

CONFIRM_APPLY_DEBUG_FALSE = getattr(settings, 'ZERO_MIGRATIONS_CONFIRM_APPLY_DEBUG_FALSE', True)
"""Whether to ask for confirmation before running the apply action in `DEBUG = False` mode. default: `True`"""
```

## What it does
- `create` removes the migrations of your apps and replaces them by a new initial migration. Resets your migration history to this migration.
- `apply` is used to reset the migration history on other instances after receiving the new migrations by other means (i.e. version control)