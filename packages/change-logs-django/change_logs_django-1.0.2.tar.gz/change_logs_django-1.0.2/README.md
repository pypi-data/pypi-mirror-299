# change-logs-django

`change-logs-django` is a simple Django package to create a changelogs page for your application. It provides an easy way to manage and display changelogs with versioning.

## Installation

1. Install the package:
   ```bash
   pip install change-logs-django
   ```

2. Add `change_logs` to `INSTALLED_APPS` in your `settings.py`:
   ```py
    INSTALLED_APPS = [
        # other apps
        'change_logs',
    ]
   ```

3. Include the `change_logs` URLs in your `urls.py`:
   ```py
   from change_logs.urls import urlpatterns as change_logs_urls

   ...
   ...

   urlpatterns += change_logs_urls
   ```

4. Run migrations
   ```bash
   python manage.py migrate
   ```
   This will create two tables in the Django admin panel: `Tags` and `ChangeLog`.

5. After completing the steps, you can access your changelogs at:
   - `yourdomain.com/change-logs`: Displays the list of changelogs.
   - `yourdomain.com/change-logs/v<version>`: Displays detailed logs for the specific version.

## Configuration
To configure the number of changelogs displayed per page, add the following setting in your `settings.py` file:
```py
CHANGE_LOGS_PER_PAGE = 10  # Change as needed
```

## Usage
After setup, you can manage your changelogs via the Django admin panel. Add, edit, or delete entries as needed, and they will be automatically reflected on the public changelogs page.
