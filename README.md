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

## Web Scraping and Data Collection

### Data Collection Using BBBike OpenStreetMap Extracts

To collect real-world business listing data, I used **[BBBike Extract Service](https://extract.bbbike.org/)** to obtain a geographic extract covering Delhi and nearby areas.

Instead of relying entirely on synthetic data or live scraping requests, I downloaded a regional extract containing OpenStreetMap geographic data and processed it locally.

**Data collection workflow:**

1. **Select the geographic region:** Used BBBike to select a bounding area covering Delhi and surrounding areas.
2. **Download the extract:** Obtained the regional OpenStreetMap dataset in GeoPackage (`.gpkg`) format.
3. **Inspect geographic data:** Examined the available layers, including `points` and `multipolygons`, which contain mapped locations and area-based features.
4. **Extract relevant listings:** Used Python scripts to identify named features with business-related tags, such as shops, offices, amenities, and other points of interest.
5. **Transform the data:** Mapped the extracted information into structured fields, including business name, category, city, address, phone number, and source.
6. **Store in MySQL:** Imported the processed records into the `listing_master` table for dashboard analytics.
7. **Visualize the results:** Used FastAPI endpoints to aggregate the records and display city-wise, category-wise, and source-wise distributions in ListingIQ.

### Tools Used

- **BBBike Extract Service:** Downloading a selected geographic extract.
- **OpenStreetMap (OSM):** Source of mapped places and associated tags.
- **Python:** Parsing and processing the downloaded data.
- **GeoPackage / SQLite:** Reading geographic layers and their attributes.
- **FastAPI and SQLAlchemy:** Importing and querying structured listing records.
- **MySQL:** Persisting the processed records for dashboard reporting.

### Data Quality and Limitations

The downloaded extract contains mapped geographic features, not exclusively conventional businesses. Depending on their tags, records may include public amenities, parks, places of worship, government facilities, and other points of interest. The completeness of names, addresses, and phone numbers depends on the information contributed to OpenStreetMap.

The dashboard uses a reporting sample of 500 listings for its summary and charts when configured to do so; this is distinct from the total number of records that may be stored in the database.

### Attribution and Licensing

Geographic data is provided by OpenStreetMap contributors and is available under the Open Database License (ODbL).

- BBBike Extract Service: https://extract.bbbike.org/
- OpenStreetMap copyright and attribution: https://www.openstreetmap.org/copyright
- OpenStreetMap legal information: https://www.openstreetmap.org/copyright

This project uses the downloaded data for demonstration and analytics purposes. Attribution and applicable ODbL obligations should be maintained when redistributing the data or derived databases.

## Challenges Faced and Solutions

During the development of ListingIQ, I encountered several technical challenges and implemented solutions to make the data pipeline and dashboard more reliable.

### 1. Data Collection and Request Failures
**Challenge:** Collecting regional business-related data through live requests was difficult due to server errors and rate limits.

**Solution:** Used the BBBike Extract Service to download a geographic OpenStreetMap extract covering Delhi and nearby areas, then processed the data locally using Python.

### 2. Processing Geographic Data
**Challenge:** The downloaded GeoPackage contained multiple geographic layers, including points and multipolygons, and not every feature represented a conventional business.

**Solution:** Developed Python scripts to inspect the available layers, identify named features with relevant tags, and map the available attributes into a consistent listing structure.

### 3. Database Integration
**Challenge:** The extracted data needed to be stored in a structured format and made accessible to the dashboard.

**Solution:** Used MySQL and SQLAlchemy to manage listing records and FastAPI endpoints to retrieve data, calculate aggregate metrics, and support bulk insertion.

### 4. Dashboard Chart Readability
**Challenge:** Displaying many city names and business categories made charts crowded and difficult to interpret.

**Solution:** Limited the city chart to the top 10 cities, grouped smaller categories into an "Other" category, and adjusted chart labels, spacing, and legends.

### 5. Consistent Dashboard Reporting
**Challenge:** Ensuring that summary cards and charts represented a consistent set of records was important for reliable reporting.

**Solution:** Configured the dashboard reporting endpoints to use a sample of 500 listings, keeping the displayed summary metrics and charts aligned with the intended reporting sample.

### Key Learnings

- Processing and structuring real-world geographic datasets.
- Handling data extraction failures and choosing reliable data acquisition methods.
- Integrating Python, FastAPI, SQLAlchemy, and MySQL.
- Improving chart readability and dashboard usability.
- Maintaining data provenance and documenting OpenStreetMap attribution.


## Author

**Arnav Gupta**

GitHub: https://github.com/ArnavvGuupta

---

*ListingIQ — Turning business listing data into actionable insights.*
