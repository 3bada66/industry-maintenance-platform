# Run Me — Step by Step

Everything you need to run, test, and verify the Industry Maintenance Platform project on Windows.

---

## How Many PowerShell Windows Do You Need?

You need **2 PowerShell windows** open at the same time:

| Window | Purpose | When to open |
|--------|---------|--------------|
| **Window 1** | Run all Docker commands (start, stop, logs, migrations) | Open at the start, keep it open the whole time |
| **Window 2** | Run frontend and backend tests | Open only when you reach Part 6 or Part 7 |

> Docker Desktop must also be open and running in the background the entire time (it does not need a terminal window of its own).

How to open a PowerShell window:
1. Open the project folder in File Explorer (`C:\Users\obada\Desktop\SPM_git_vs`)
2. Click the address bar at the top
3. Type `powershell` and press Enter

Open Window 1 this way now. Open Window 2 the same way when you reach the tests.

---

## Part 1 — Prerequisites

**Step 1.** Install Docker Desktop
- Download from https://www.docker.com/products/docker-desktop
- After install, open Docker Desktop and wait until it shows "Engine running"

**Step 2.** Confirm Docker is running

```powershell
docker --version
docker compose version
```

Expected output: version numbers, no errors.

**Step 3.** Install Node.js (for frontend tests only)
- Download from https://nodejs.org — use the LTS version
- Confirm:

```powershell
node --version
npm --version
```

**Step 4.** Install Python 3.8 or later (for backend tests only)
- Download from https://python.org
- Confirm:

```powershell
python --version
```

---

## Part 2 — Get the Code

**Step 5.** Open PowerShell inside the project folder

If you already have the folder on your Desktop:
1. Open File Explorer and go to `C:\Users\obada\Desktop\SPM_git_vs`
2. Click the address bar, type `powershell`, press Enter

**Step 6.** Confirm you are on the right branch

```powershell
git branch
```

Expected: `course-adaptation-monitoring` is listed or active.

If not:

```powershell
git checkout course-adaptation-monitoring
```

---

## Part 3 — Start the Application

**Step 7.** Generate the SSL certificates (do this once, before the first start)

Nginx needs SSL certificates to serve HTTPS. Without them it will crash on startup.
Run these four commands one at a time in PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path nginx\ssl
```
```powershell
openssl genrsa -out nginx\ssl\key.pem 2048
```
```powershell
openssl req -new -key nginx\ssl\key.pem -out nginx\ssl\cert.csr -subj "/C=TR/ST=Istanbul/L=Istanbul/O=IndustryMaintenancePlatform/CN=localhost"
```
```powershell
openssl x509 -req -days 365 -in nginx\ssl\cert.csr -signkey nginx\ssl\key.pem -out nginx\ssl\cert.pem
```

> If `openssl` is not recognised, use the full path:
> `& "C:\Program Files\Git\usr\bin\openssl.exe"` instead of `openssl`

After the four commands you should see `nginx\ssl\cert.pem` and `nginx\ssl\key.pem` in the folder. You only need to do this once — the files stay there for future runs.

**Step 8.** Start the containers

```powershell
docker compose -f docker-compose.prod.yml up -d
```

This builds and starts all four containers (database, backend, frontend, nginx). Takes 2–5 minutes on first run. You will see download and build progress in the terminal.

**Step 9.** Wait 15 seconds, then run the database migrations

```powershell
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

**Step 10.** Load the demo data

```powershell
docker compose -f docker-compose.prod.yml exec backend python -m app.init_demo_data
```

This adds 8 assets, 3 sites, network topology, contacts, and suppliers.

**Step 11.** Check that all containers are healthy

```powershell
docker compose -f docker-compose.prod.yml ps
```

All four services (`db`, `backend`, `frontend`, `nginx`) must show `running` or `healthy`. If any show `starting`, wait 30 seconds and run the command again.

**Step 12.** Verify the health endpoint returns JSON (not HTML)

```powershell
curl.exe -k https://localhost/health
```

Expected response:

```json
{"status":"ok","database":"connected","uptime":"running","timestamp":"...Z"}
```

If you see an HTML page instead of JSON, nginx is not routing health checks to the backend. Reload nginx to fix it:

```powershell
docker compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

Then run the curl command again — it must return JSON before continuing.

**Step 13.** Open the application in your browser

```
https://localhost
```

You will see a certificate warning because the certificate is self-signed. Click **Advanced** then **Proceed to localhost**.

**Step 14.** Log in

```
Email:    admin@example.com
Password: admin123
```

The main dashboard should load with assets, risk scores, and charts.

---

## Part 4 — Verify the Three Dashboards

**Step 15.** Open the Technical Monitoring Dashboard

```
https://localhost/monitoring
```

You should see a green **HEALTHY** banner, system resource bars, and a metrics table.

**Step 16.** Open the Management Monitoring Dashboard

```
https://localhost/management
```

You should see KPI tiles (SPI, sprint velocity, task completion), sprint velocity bars, and a team workload table.

**Step 17.** Open the Risk Dashboard

```
https://localhost/risk
```

You should see risk KPI tiles, a risk distribution panel, risky assets list, and the project risk register.

---

## Part 5 — Verify the Health Endpoints

**Step 18.** Check the basic health endpoint

```powershell
curl.exe -k https://localhost/health
```

Expected response:

```json
{"status":"ok","database":"connected","uptime":"running","timestamp":"2026-...Z"}
```

**Step 19.** Check the detailed health endpoint

```powershell
curl.exe -k https://localhost/health/detailed
```

Expected response: a JSON object with `database`, `system` (CPU, memory, disk), and `uptime_seconds`.

> Note: use `curl.exe` (not `curl`) in PowerShell to get the real curl behavior.

---

## Part 6 — Run the Frontend Tests

**Step 20.** Go to the frontend folder

```powershell
cd frontend
```

**Step 21.** Install dependencies

```powershell
npm ci
```

**Step 22.** Run the unit tests

```powershell
npm run test:unit
```

Expected output:

```
1 test file — 29 tests — all passed
```

**Step 23.** Return to the project root

```powershell
cd ..
```

---

## Part 7 — Run the Backend Tests

> The backend tests require the containers from Part 3 to be running first.

**Step 24.** Go to the backend folder

```powershell
cd backend
```

**Step 25.** Install Python dependencies

```powershell
pip install -r requirements.txt
```

**Step 26.** Run the tests

```powershell
pytest tests/ -v --tb=short
```

Expected: all tests pass. If you see `OperationalError` or `connection refused`, the database container is not running — go back and complete Part 3.

**Step 27.** Return to the project root

```powershell
cd ..
```

---

## Part 8 — Run the Smoke Tests

Run these four commands after every deployment to confirm the system is alive end-to-end.

**Step 28.** Health check

```powershell
curl.exe -k https://localhost/health
```

**Step 29.** Detailed health check

```powershell
curl.exe -k https://localhost/health/detailed
```

**Step 30.** Login and get a token

```powershell
curl.exe -k -X POST https://localhost/api/login -d "username=admin@example.com&password=admin123"
```

Copy the `access_token` value from the response.

**Step 31.** Authenticated API call (replace `YOUR_TOKEN` with the value from Step 30)

```powershell
curl.exe -k -H "Authorization: Bearer YOUR_TOKEN" https://localhost/api/assets/
```

Expected: a JSON list of assets (not a 401 error).

---

## Part 9 — Load Demo Data (if needed)

If the dashboards show no data after starting:

**Step 32.** Load demo data

```powershell
docker compose -f docker-compose.prod.yml exec backend python -m app.init_demo_data
```

---

## Part 10 — Stop the Application

**Step 33.** Stop all containers

```powershell
docker compose -f docker-compose.prod.yml down
```

**Step 34.** To remove all containers and data completely (destructive — only if you want to start from scratch)

```powershell
docker compose -f docker-compose.prod.yml down -v
```

---

## Part 11 — CI/CD (Automatic on GitHub)

No steps required locally. Every push to GitHub triggers:

- **Backend pipeline** (`.github/workflows/backend.yml`): syntax check → pytest with a real PostgreSQL container → coverage report
- **Frontend pipeline** (`.github/workflows/frontend.yml`): `npm ci` → Vitest tests → Vite production build

View results at: `https://github.com/<your-repo>/actions`

---

## Quick Reference

| Goal | PowerShell Command |
|------|--------------------|
| Start containers | `docker compose -f docker-compose.prod.yml up -d` |
| Run migrations | `docker compose -f docker-compose.prod.yml exec backend alembic upgrade head` |
| Load demo data | `docker compose -f docker-compose.prod.yml exec backend python -m app.init_demo_data` |
| Check service health | `docker compose -f docker-compose.prod.yml ps` |
| View logs | `docker compose -f docker-compose.prod.yml logs -f` |
| Restart services | `docker compose -f docker-compose.prod.yml restart` |
| Stop containers | `docker compose -f docker-compose.prod.yml down` |
| Full reset | `docker compose -f docker-compose.prod.yml down -v` |
| Run frontend tests | `cd frontend; npm ci; npm run test:unit` |
| Run backend tests | `cd backend; pytest tests/ -v` |

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| `docker compose` not found | Docker Desktop is not running — open it and wait for "Engine running" |
| Container shows `unhealthy` after 2 minutes | Run `docker compose -f docker-compose.prod.yml logs` to see the error |
| Browser shows "connection refused" | Containers are still starting — wait 30 seconds and refresh |
| Certificate warning in browser | Click Advanced → Proceed to localhost (self-signed cert is normal) |
| Frontend tests fail with "cannot find module" | Run `npm ci` first to install dependencies |
| Backend tests fail with `OperationalError` | Containers are not running — complete Part 3 first |
| Dashboards show no data | Run the demo data command from Step 32 |
| Technical Monitoring shows all "unknown" | Health endpoint returning HTML — run `docker compose -f docker-compose.prod.yml exec nginx nginx -s reload` then retry Step 12 |
| Port 443 already in use | Another app is using port 443 — stop it or restart your computer |
| nginx shows `Restarting` | SSL certificates are missing — run the four `openssl` commands in Step 7, then run `docker compose -f docker-compose.prod.yml restart nginx` |
