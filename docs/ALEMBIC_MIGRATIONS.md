# Alembic Database Migration Workflow

This document outlines the process for managing database schema changes using Alembic and deploying them to production on Render.

## Database Migrations with Alembic

We use [Alembic](https://alembic.sqlalchemy.org/en/latest/) to handle all database schema migrations. This provides a reliable, version-controlled way to evolve the database schema without losing data.

### Local Development Workflow

Follow these steps to make and test schema changes on your local machine.

#### Step 1: Modify Your SQLAlchemy Models

Make any desired changes to your models in `backend/api/storage/models.py`. For example, you might add a new column to a table or create a new table entirely.

#### Step 2: Generate a New Migration Script

After changing your models, run the following command from the `backend` directory to automatically generate a migration script:

```bash
poetry run alembic revision --autogenerate -m "A short, descriptive message about the change"
```

For example:
```bash
poetry run alembic revision --autogenerate -m "Add phone_number to User model"
```

This will create a new file in the `backend/migrations/versions/` directory. This file contains the Python code necessary to apply your schema changes.

#### Step 3: Apply the Migration Locally

Apply the changes to your local database to ensure they work correctly:

```bash
poetry run alembic upgrade head
```

Your local database now reflects the changes you made to your models. You should now run the application and test thoroughly.

#### Other Useful Commands

*   **Downgrade a Migration:** To revert the last migration:
    ```bash
    poetry run alembic downgrade -1
    ```
*   **View Migration History:** To see the history of all migrations and the current revision:
    ```bash
    poetry run alembic history
    ```

---

### Deployment to Production (Render)

Our production environment on Render is configured for Continuous Deployment. The migration process is fully automated.

#### The CI/CD Workflow

1.  **Commit and Push:** After you have generated and tested your migration locally, commit both the model changes and the new migration script to your Git repository:
    ```bash
    git add backend/api/storage/models.py backend/migrations/versions/<new_migration_file>.py
    git commit -m "feat: Your descriptive commit message"
    git push origin main
    ```

2.  **Automated Deployment:** Pushing to the `main` branch triggers a new deployment on Render. Render will execute the `backend/scripts/build.sh` script, which performs two key actions:
    *   Installs all dependencies from `backend/requirements.txt`.
    *   Runs `alembic upgrade head`, which connects to the production database (Supabase) and applies any new migrations.

3.  **Application Start:** Once the build is successful, Render starts the application using the `backend/scripts/start.sh` script. The application code and database schema are now perfectly in sync.

#### Render Configuration Summary

*   **Root Directory:** `backend`
*   **Build Command:** `./scripts/build.sh`
*   **Start Command:** `./scripts/start.sh`

This automated workflow ensures that database migrations are a safe and routine part of the development and deployment process.