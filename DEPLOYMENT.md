# Deploy Luméa on free plans

The [Render Blueprint](render.yaml) runs the storefront, admin console and FastAPI on one **Free** service in Singapore. Postgres keeps orders, catalog data, accounts and settings across Render restarts. Use the included `onrender.com` address.

## Get a Postgres connection string

**Neon Free** — Create a project in Singapore. Open **Connect**, turn off **Connection pooling**, and copy the full direct connection string with its SSL options. The app has its own small connection pool. [Neon connection guide](https://neon.com/docs/connect/connect-from-any-app)

**Existing Supabase project** — Turn off the **Data API**, then copy the **Session pooler** URI from **Connect**. Replace `[YOUR-PASSWORD]` with the URL-encoded database password. Add `?sslmode=require` if the URI has no query string. [Supabase session pooler](https://supabase.com/docs/guides/database/connecting-to-postgres#shared-pooler-session-mode) · [Data API settings](https://supabase.com/docs/guides/api/securing-your-api#disable-the-data-api)

The temporary deployment uses bundled asset paths and existing HTTPS media URLs. There is no storage bucket to configure.

## Deploy from GitHub

1. Push the reviewed application changes and `render.yaml` to the branch you want Render to use. Keep local environment files, the local SQLite database, and payment captures out of the deployment changes.
2. Open [New Render Blueprint](https://dashboard.render.com/blueprint/new?repo=https%3A%2F%2Fgithub.com%2Fsounvisal%2FPython-E-Commerce), connect the repository, and select the deployed branch. Use the **Hobby** workspace and confirm the service is **Free**. Leave payment details off the workspace if you want Render to suspend usage at its included limits. [Render free limits](https://render.com/docs/free)
3. Paste the full connection string into Render's `DATABASE_URL` prompt. Render generates the signing key automatically. If the service already exists, update `DATABASE_URL` under **Environment** and redeploy. Keep the URI out of Git and chat.
4. Open `/` for the storefront, `/atelier/` for admin, and `/api/health` to verify the database connection. Render's automated check uses `/api/live` so it doesn't wake an idle Neon database. Apply future deploys manually from Render.

## Create the first administrator

After the initial health check succeeds, use PowerShell 7 from the repo to create your own account. The script prompts for the administrator password separately.

```powershell
Set-Location python-backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
$env:DATABASE_URL = Read-Host 'Postgres connection URI with SSL options' -MaskInput
try {
  .\venv\Scripts\python.exe create_admin.py admin@example.com --name 'Store Administrator'
} finally {
  Remove-Item Env:DATABASE_URL
}
```

The hosted database starts empty. Set the store contact details, delivery settings, catalog and stock, and publish the content you want customers to see. Test a cash-on-delivery order and confirm it appears in admin. For product, article and banner media, use an existing HTTPS URL or a bundled path such as `/images/prod-sk2.jpg`.

Hosted checkout accepts **cash on delivery**. KHQR requires a verified merchant integration. The temporary hosted build disables file uploads, including video reviews and return proof photos.

## Free-plan limits

- Render sleeps after 15 minutes of inactivity. The next visit can take about a minute, and the service is subject to workspace usage limits. [Render free limits](https://render.com/docs/free)
- Neon Free includes 1 GB of Postgres storage and 100 compute-unit hours per project per month. The database suspends after five minutes of inactivity and wakes on the next query. [Neon free plan](https://neon.com/docs/introduction/plans)
