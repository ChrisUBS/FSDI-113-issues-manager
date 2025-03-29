# Mini Challenge 4

## Custom Migration for issues.Status model

### Acceptance Criteria
Create a custom or blank migration to populate Status (in issues/models.py) with the following:
1. to do: An issue for which work has not yet begun
2. in progress: An issue currently being worked on
3. done: An issue for which work has been completed

#### Then
Run all migrations, create a `superuser`, log into the admin panel and test.
Example: `python3 manage.py createsuperuser`
You can, optionally (but recommended), register the `Issue` model onto the admin panel to see statuses.