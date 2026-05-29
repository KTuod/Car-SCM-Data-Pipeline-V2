# Car Supply Chain Data Pipeline

A scalable **Data Engineering project** that builds an end-to-end pipeline for processing Car Supply Chain data, from raw ingestion to business-ready analytics.

## I. Problem Statement

While modern supply chain systems generate vast amounts of data, this information is frequently stored in inconsistent and unstructured formats, hindering effective analysis. Consequently, the report generation process remains highly complex, inefficient, and time-consuming due to the need for repetitive content revisions.

## II. Solution

To address this challenge, data pipeline will be implemented that automatically ingests, cleans, and standardizes supply chain data into a structured format and actionable insights. By integrating automated reporting templates, this solution will eliminate manual, repetitive revisions and streamline the analytical workflow.

## III. Architecture Overview

```mermaid
graph TD
    %% Style Definitions
    classDef infra fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef storage fill:#fff9db,stroke:#f59f00,stroke-width:2px;
    classDef process fill:#edf2ff,stroke:#364fc7,stroke-width:2px;
    classDef monitor fill:#fff5f5,stroke:#fa5252,stroke-width:2px;

    %% Infrastructure & Orchestration Subgraph
    subgraph Infrastructure [Infrastructure & Orchestration]
        Docker[Docker]
        Bruin[Bruin]
        Terraform[Terraform]
    end

    %% Data Lake Subgraph (Cloudflare R2)
    subgraph CloudflareR2 [Cloudflare R2 - Bucket 1]
        Bronze_CSV[(Bronze / *.csv)]
        Silver_Parquet[(Silver / *.parquet)]
    end

    %% Data Warehouse Subgraph
    subgraph DataWarehouse [Data Warehouse]
        MotherDuck[(MotherDuck)]
    end

    %% Monitoring Subgraph
    subgraph Monitoring [Monitoring System]
        Logs[Logs]
        GrafanaLoki[Grafana Loki]
        Grafana[Grafana]
        Discord[Discord]
    end

    %% External Sources & Users
    Kaggle[Kaggle API]
    LocalStorage[Local Storage]
    Spark[Apache Spark]
    Streamlit[Streamlit]
    Users[Users]

    %% --- PIPELINE FLOWS & RELATIONSHIPS ---

    %% Infrastructure Deployments
    Terraform -- "Construct" --> CloudflareR2
    Bruin -- "Daily" --> Kaggle

    %% Core Data Pipeline (Ingestion & Processing)
    Kaggle -- "Ingest" --> LocalStorage
    LocalStorage -- "Upload" --> Bronze_CSV
    Bronze_CSV --> Spark
    Spark -- "Transformation" --> Silver_Parquet

    %% Medallion Integration (Lakehouse to Warehouse)
    Silver_Parquet -- "Connect, Query and Create" --> MotherDuck

    %% BI & Presentation Layer
    MotherDuck -- "Query" --> Streamlit
    Streamlit -- "View" --> Users

    %% Logging & Observability Flow
    Docker -- "Record" --> Logs
    Logs -- "Send" --> GrafanaLoki
    GrafanaLoki -- "Query" --> Grafana
    Grafana -- "View" --> Users

    %% Alerting Flow
    Bruin -- "Errors" --> Discord
    Discord -- "Send Notifications" --> Users

    %% Element Styling
    style Docker fill:#1d63ed,color:#fff
    style Terraform fill:#5c4ee5,color:#fff
    style Bruin fill:#ec4899,color:#fff
    style Spark fill:#e65100,color:#fff
    style MotherDuck fill:#ffb300,color:#000
    style Streamlit fill:#ff4b4b,color:#fff
    style Discord fill:#5865f2,color:#fff
```

This modern data pipeline follows a Medallion Architecture managed by a robust infrastructure and monitoring system. First, Terraform provisions the Cloudflare R2 storage, while Bruin schedules the daily ingestion of raw data from the Kaggle API into Local Storage and subsequently into the Bronze R2 bucket as CSV files. Next, Apache Spark processes and transforms this raw data into optimized Parquet format within the Silver R2 bucket. This clean data is then queried by MotherDuck, acting as the cloud data warehouse.

**Relationship Diagram (Gold Layer Star Schema)**
```mermaid
erDiagram
    dim_customer {
        VARCHAR CustomerID PK
        VARCHAR CustomerName
        VARCHAR Gender
        VARCHAR JobTitle
        VARCHAR job_group
        VARCHAR PhoneNumber
        VARCHAR EmailAddress
        VARCHAR CustomerAddress
        VARCHAR City
        VARCHAR State
        VARCHAR Country
        VARCHAR CountryCode
        VARCHAR PostalCode
        VARCHAR ProductID
        VARCHAR SupplierID
    }

    dim_product {
        VARCHAR ProductID PK
        VARCHAR CarMaker
        VARCHAR CarModel
        VARCHAR CarType
        VARCHAR CarColor
        VARCHAR CarColorGroup
        INTEGER CarModelYear
        DOUBLE CarPrice
    }

    dim_supplier {
        VARCHAR SupplierID PK
        VARCHAR SupplierName
        VARCHAR SupplierAddress
        VARCHAR SupplierContactDetails
    }

    dim_date {
        DATE DateKey PK
        INTEGER Year
        INTEGER Month
        INTEGER Day
        INTEGER Quarter
        VARCHAR DayOfWeekName
    }

    fact_sales {
        VARCHAR OrderID PK
        VARCHAR CustomerID FK
        VARCHAR ProductID FK
        VARCHAR SupplierID FK
        DATE OrderDateKey FK
        DATE ShipDateKey FK
        VARCHAR ShipMode
        VARCHAR CreditCardType
        VARCHAR CreditCard
        VARCHAR CustomerFeedback
        DOUBLE Sales
        INTEGER Quantity
        DOUBLE Discount
        DOUBLE Shipping
    }

    dim_customer ||--o{ fact_sales : "a customer can place many orders (1:N)"
    dim_product ||--o{ fact_sales : "a product can be sold in many orders (1:N)"
    dim_supplier ||--o{ fact_sales : "a supplier can fulfill many orders (1:N)"
    dim_date ||--o{ fact_sales : "a calendar date can be an order date for many orders (1:N)"
    dim_date ||--o{ fact_sales : "a calendar date can be a ship date for many orders (1:N)"
```

Finally, Streamlit query to MotherDuck for creating application for end-user data visualization. Throughout this workflow, Docker container logs are collected by Grafana Loki and visualized via Grafana for continuous observability, while any pipeline errors encountered by Bruin trigger real-time alerts to users via Discord.

## IV. Tech Stack

| Layer | Technology | Key Role in Architecture |
|---|---|---|
| **Infrastructure & Orchestration** | **Terraform** | Infrastructure as Code (IaC) to provision Cloudflare R2 buckets. |
|  | **Bruin** | Data orchestrator to schedule and trigger the daily ingestion tasks. |
|  | **Docker** | Containerization to isolate services and standardise logging environments. |
| **Data Lake & Cloud Storage** | **Cloudflare R2** | Object storage hosting the Medallion architecture (**Bronze** and **Silver** layers). |
| **Data Ingestion & Processing** | **Kaggle API** | The primary external data source for the pipeline. |
|  | **Apache Spark** | Distributed compute engine used to normalize and transform CSVs into optimized Parquet files. |
| **Data Warehouse** | **MotherDuck** | Cloud-native, DuckDB-powered data warehouse for analytical queries. |
| **BI & Presentation Layer** | **Streamlit** | Python-based web framework for interactive dashboards and data viewing. |
| **Observability & Alerting** | **Grafana Loki & Grafana** | Log aggregation and visualization stack to monitor Docker container metrics. |
|  | **Discord** | Webhook integration for real-time pipeline error notifications. |

## V. Project Structure

```text
scm-data-pipeline-v2/
├── .bruin.yml                 # Bruin global configuration
├── .env                       # Environment variables configuration
├── requirements.txt           # Python application dependencies
├── README.md                  # Project documentation
│
├── data/                      # Local data cache
│   └── Car_SupplyChainManagementDataSet.csv
│
├── pipelines/                 # Data orchestration pipeline
│   ├── pipeline.yml           # Pipeline-level configuration
│   └── assets/                # Medallion layers ETL code
│       ├── bronze/            # Bronze Tier: Ingestion & storage
│       │   ├── ingest/
│       │   │   └── ingest_scm_kaggle.py
│       │   └── storage/
│       │       └── upload_to_r2.py
│       ├── silver/            # Silver Tier: Cleaning & transformation
│       │   └── data_normalization.py
│       └── gold/              # Gold Tier: Analytical modeling
│           ├── load_to_motherduck.py
│           └── queries/       # Star Schema transformation scripts
│               ├── dim_customer.sql
│               ├── dim_date.sql
│               ├── dim_product.sql
│               ├── dim_supplier.sql
│               └── fact_sale.sql
│
├── dashboard/                 # Analytics and reporting application
│   ├── app.py                 # Streamlit dashboard application
│   ├── db_queries.py          # Data retrieval layers from MotherDuck
│   └── queries/               # Dashboard analytical queries
│       ├── page_1/
│       │   ├── charts/
│       │   └── metrics/
│       └── page_2/
│           ├── charts/
│           └── metrics/
│
├── terraform/                 # Infrastructure as Code config
│   ├── main.tf                # Cloud resources definition
│   ├── variables.tf           # Terraform input parameters
│   ├── terraform.tfvars       # Terraform variable values
│   └── terraform.tfstate      # Infrastructure state file
│
└── logs/                      # Executions log directory
```

## VI. Getting Started

### Step 1: Prerequisites

Ensure you have the following installed and configured on your machine:
1. **Docker Desktop** (running on your host machine).
2. **VS Code** with the **Dev Containers** extension installed.
3. **Accounts and Credentials**:
   * **Kaggle Account** (to download the source dataset). Generate an API Token from your Kaggle Profile Settings to receive `kaggle.json` credentials (`username` and `key`).
   * **Cloudflare Account** (for R2 object storage).
   * **MotherDuck Account** (for cloud DuckDB data warehousing). Get your MotherDuck service token from the dashboard.

### Step 2: Set Up the Development Environment

1. Open the project folder in VS Code.
2. Click the green button in the bottom-left corner of VS Code (or press `Ctrl + Shift + P`) and select:
   ```bash
   Dev Containers: Reopen in Container
   ```
3. VS Code will build the Docker container and configure all development tools automatically.

### Step 3: Configure Variables

#### 1. Terraform Credentials (`terraform/terraform.tfvars`)
Create a variables file to provision the Cloudflare R2 bucket:
```bash
cd terraform
touch terraform.tfvars
```
Add the following content to `terraform/terraform.tfvars`:
```hcl
cloudflare_account_id = "your_cloudflare_account_id"
cloudflare_api_token  = "your_cloudflare_api_token"

bucket_name           = "scm-car-dataset"
alert_email           = "your_email@example.com"
```

#### 2. Pipeline Environment Variables (`.env`)
Create a `.env` file in the root directory:
```bash
touch .env
```
Populate the file with the following variables:
```env
# Cloudflare R2 Storage Credentials
R2_ACCOUNT_ID=your_cloudflare_account_id
R2_ACCESS_KEY=your_r2_access_key
R2_SECRET_KEY=your_r2_secret_key
R2_BUCKET_NAME=scm-car-dataset

# Kaggle API Credentials
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_token_key

# MotherDuck Warehouse Token
MOTHERDUCK_TOKEN=your_motherduck_access_token

# Local Path to raw cache (optional)
RAW_DATA_PATH=d:/Projects/scm-data-pipeline-v2/data

# Optional Discord Alerting Hook
DISCORD_WEBHOOK=your_discord_webhook_url

# Loki
GRAFANA_LOKI_URL=your_loki_url
GRAFANA_LOKI_USER=your_loki_user
GRAFANA_LOKI_TOKEN=your_loki_token
```

### Step 4: Provision Cloud Infrastructure

Deploy the Cloudflare R2 object storage bucket defined in your configuration:
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
cd ..
```

### Step 5: 

Before running the pipeline, start Promtail in the background to capture and ship Docker container logs to Grafana Loki:
```bash
nohup promtail -config.file=/workspaces/scm-data-pipeline-v2/.devcontainer/promtail-config.yml -config.expand-env=true > /tmp/promtail.out 2>&1 &
```

### Step 6: Run the Data Pipeline

Run the pipeline:
```bash
# Run the complete data pipeline sequence (Bronze -> Silver -> Gold)
bruin run pipelines/pipeline.yml
```

### Step 7: Launch the Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```
After executing the command, Streamlit will expose a local URL (typically `http://localhost:8501`) where you can interact with SCM KPIs and transactional graphs.

![Car SCM Dashboard Page 1.1](/dashboard/images/dashboard_page1.1.png)
![Car SCM Dashboard Page 1.2](/dashboard/images/dashboard_page1.2.png)
![Car SCM Dashboard Page 1.3](/dashboard/images/dashboard_page1.3.png)

![Car SCM Dashboard Page 2.1](/dashboard/images/dashboard_page2.1.png)
![Car SCM Dashboard Page 2.2](/dashboard/images/dashboard_page2.2.png)
![Car SCM Dashboard Page 2.3](/dashboard/images/dashboard_page2.3.png)

![Loki Grafana for Tracking Logs](/dashboard/images/dashboard_lokiGrafana.png)