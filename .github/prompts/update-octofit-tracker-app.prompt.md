---
agent: 'agent'
model: GPT-4.1
---

# Django App Updates

- All Django project files are in the `octofit-tracker/backend/octofit_tracker` directory.

1. Update `settings.py` for MongoDB connection and CORS.
2. Update `models.py`, `serializers.py`, `urls.py`, `views.py`, `tests.py`, and `admin.py` to support users, teams, activities, leaderboard, and workouts collections.
3. Ensure `/` points to the api and `api_root` is present in `urls.py`. (See <attachments> above for file contents. You may not need to search or read the file again.)

Please perform the updates following project conventions and ensure unit tests pass locally before committing. If any package is missing, update `requirements.txt` accordingly.
