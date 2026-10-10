# ListingIQ — Business Listings Dashboard

A full-stack business intelligence dashboard that helps users explore business listings across cities, categories, and data sources. Built with **React, FastAPI, and MySQL**, ListingIQ transforms business listing data into clear, interactive visual insights.

<img width="1870" height="1023" alt="Screenshot 2026-10-10 224128" src="https://github.com/user-attachments/assets/d3aaaea4-1d4b-4fda-b1bf-8e10f9e79eb0" />


## Features

- **Business Overview:** Displays total listings, cities covered, categories, and data sources.
- **Interactive Analytics:** Visualizes the top 10 cities, category breakdown, and source distribution.
- **Business Listings:** Displays business names, categories, cities, phone numbers, and data sources.
- **REST API:** Provides endpoints for retrieving listings, dashboard metrics, and bulk insertion.
- **MySQL Database:** Stores structured listing data in the `listing_master` table.
- **Responsive UI:** Clean dashboard interface with interactive charts and navigation.
- **Data Integration:** Supports OpenStreetMap business-related data and synthetic sample records where applicable.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, Recharts |
| Styling | CSS |
| Icons | Lucide React |
| Backend | Python, FastAPI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Data Processing | Python |

<img width="1881" height="1053" alt="Screenshot 2026-10-10 224140" src="https://github.com/user-attachments/assets/5e5968bd-d22e-4b01-b77c-22552e8f294d" />


## Dashboard Preview

The dashboard includes four summary cards and three interactive reports:

1. **Top 10 Cities:** Compares business listing counts across cities.
2. **Category Breakdown:** Displays the distribution of businesses by category.
3. **Source Distribution:** Shows the sources represented in the dataset.

A business listings table displays recent records stored in the database.

## Project Structure

```text
ListingIQ/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── seed_data.py
│   └── requirements.txt
├── database/
│   └── business_data.sql
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   ├── index.css
    │   ├── main.jsx
    │   └── services/
    │       └── api.js
    ├── package.json
    └── vite.config.js
```

## Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.10+
- Node.js and npm
- MySQL Server
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ArnavvGuupta/ListingIQ.git
cd ListingIQ
```

### 2. Set Up the Database

Create the MySQL database:

```sql
CREATE DATABASE business_dashboard;
```

Import the SQL dump using MySQL Workbench, or run:

```bash
mysql -u root -p business_dashboard < database/business_data.sql
```

Enter your MySQL password when prompted.

### 3. Configure the Backend

Open a terminal in the project directory and run:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory with your local MySQL credentials:

```dotenv
DB_HOST=localhost
DB_PORT=3306
DB_NAME=business_dashboard
DB_USER=root
DB_PASSWORD=your_mysql_password
```

Make sure these variable names match the configuration in `backend/database.py`. Replace the example password with your actual local MySQL password.

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

Interactive API documentation: `http://127.0.0.1:8000/docs`

### 4. Set Up the Frontend

Open a second terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL shown by Vite, usually:

`http://localhost:5173`

Ensure the backend is running while using the dashboard.

The API base URL is configured in `frontend/src/services/api.js`. For local development, it should point to `http://127.0.0.1:8000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/dashboard/summary` | Retrieves dashboard summary metrics |
| GET | `/api/dashboard/cities` | Returns listing counts by city |
| GET | `/api/dashboard/categories` | Returns listing counts by category |
| GET | `/api/dashboard/sources` | Returns listing counts by source |
| GET | `/api/listings` | Retrieves business listing records |
| POST | `/api/listings/bulk` | Inserts multiple listings in one request |

## Data Sources and Attribution

This project uses business-related data sourced from **OpenStreetMap (OSM)** and may include synthetic sample records for development or demonstration.

- OpenStreetMap copyright and attribution: https://www.openstreetmap.org/copyright
- OpenStreetMap data is available under the Open Database License (ODbL).
- Listing completeness depends on available mapped data. Some records may represent public amenities or other places rather than conventional commercial businesses.
- Synthetic records, where present, should not be treated as verified real businesses.

## Security

- Never commit `.env` files, database passwords, API keys, or other credentials.
- Keep virtual environments, `node_modules`, and large raw datasets out of the repository.
- Review the SQL dump for credentials and confirm that the data is appropriate to redistribute before publishing.

## Future Improvements

- Server-side search, filtering, and pagination
- CSV export functionality
- Automated duplicate detection and data validation
- User authentication and role-based access control
- Automated testing and deployment

## Author

**Arnav Gupta**

GitHub: https://github.com/ArnavvGuupta

---

*ListingIQ — Turning business listing data into actionable insights.*
