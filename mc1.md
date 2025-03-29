# Mini Challenge 1

## Initial project set up

### Acceptance Criteria

## Note: Do not run migrations!

#### Phase One
1. Create a new django project in `this` directory (~/Code/SDGKU/issue_mgr)
1.1. Your manage.py should be at the root of this directory.
1.2. Your configuration directory should be named `config` and should exist at the root of this directory.
2. Add bootstrap support.
3. Create a home page.
4. Create an about page (you can use a fictional company)
5. Add anchor tags to your site to make sure these are accessible.


#### Phase Two

2. Create an app called `issues`, then, create a model called `Issue` with the following fields:
2.1. a name with a maximum length of 64 chars
2.2. a summary field with a maximum length of 128 characters
2.3. a description field without limit (of type TEXT)
2.4. A field called reporter, which should link to the user model as a foreign key constrant.
2.5. A field called assignee, which should link to the user model as a foreign key constraint.
2.6. A "created_on" date that automatically sets a timestamp every time a new issue is created.
2.7. A status field, which is a foreign key constrain to the model in #3 on this list.
3. Create a model called `Status` which has the following fields:
3.1. name (max length 128)
3.2. description (max length 256)
4. When objects from the `Status` model are rendered as strings, their name is shown (or rendered) instead.

## Bonus
If you have extra time, work on static files (CSS, images, etc).