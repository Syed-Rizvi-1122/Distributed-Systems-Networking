# Distributed Systems Networking -- API Gateway + Microservices

This project demonstrates a **microservices architecture** with
**Flask**, **PostgreSQL**, **Docker Compose**, and **Apache APISIX** as
the API Gateway.

------------------------------------------------------------------------

## 🐳 **Steps to Rebuild and Start the System**

``` bash
docker compose down --volumes
docker compose build --no-cache
docker compose up -d
```

------------------------------------------------------------------------

## 🐳 **Steps if Rebuild is Failed**

``` bash
cat ~/.docker/config.json || echo 'NO_DOCKER_CONFIG'
cp ~/.docker/config.json ~/.docker/config.json.bak && echo '{}' > ~/.docker config.json && echo 'BACKUP_CREATED_AND_CONFIG_CLEARED'
docker compose build --no-cache
```

------------------------------------------------------------------------

## 🔧 **APISIX Upstreams Configuration**

### ✔️ **Users Upstream**

``` bash
curl -X PUT "http://localhost:9180/apisix/admin/upstreams/1" \
  -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
  -d '{
    "type": "roundrobin",
    "nodes": {
      "users:5000": 1
    }
  }'
```

### ✔️ **Products Upstream**

``` bash
curl -X PUT "http://localhost:9180/apisix/admin/upstreams/2" \
  -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
  -d '{
    "type": "roundrobin",
    "nodes": {
      "products:5000": 1
    }
  }'
```

### ✔️ **Orders Upstream**

``` bash
curl -X PUT "http://localhost:9180/apisix/admin/upstreams/3" \
  -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
  -d '{
    "type": "roundrobin",
    "nodes": {
      "orders:5000": 1
    }
  }'
```

------------------------------------------------------------------------

## 🚏 **APISIX Routes Configuration**

### ✔️ Route for **Users**

``` bash
curl -X PUT "http://localhost:9180/apisix/admin/routes/1" \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -d '{
   "uri": "/users",
   "methods": ["POST"],
   "plugins": {
     "limit-count": {
       "count": 5,
       "time_window": 60,
       "rejected_code": 429,
       "rejected_msg": "Too many requests"
     }
   },
   "upstream_id": 1
 }'
```

### ✔️ Route for **Products**

``` bash
curl -X PUT "http://localhost:9180/apisix/admin/routes/2" \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -d '{
   "uri": "/products",
   "methods": ["POST"],
   "plugins": {
     "limit-count": {
       "count": 5,
       "time_window": 60,
       "rejected_code": 429
     }
   },
   "upstream_id": 2
 }'
```

### ✔️ Route for **Orders**

``` bash
curl -X PUT "http://localhost:9180/apisix/admin/routes/3" \
 -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" \
 -d '{
   "uri": "/orders",
   "methods": ["POST"],
   "plugins": {
     "limit-count": {
       "count": 5,
       "time_window": 60,
       "rejected_code": 429
     }
   },
   "upstream_id": 3
 }'
```

------------------------------------------------------------------------

## 🧪 **Testing an Example Request**

### Add a user:

``` bash
curl -X POST http://localhost:9080/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Shazan", "email":"shazan@test.com"}'
```

### Add a product:

``` bash
curl -X POST http://localhost:9080/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop", "price":1200}'
```

### Add an order:

``` bash
curl -X POST http://localhost:9080/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id":1, "product_id":1, "quantity":2}'
```

------------------------------------------------------------------------

## 🗄️ **Verify User in Database**

Enter the PostgreSQL container:

``` bash
docker exec -it distributed-systems-networking-db-1 psql -U postgres -d ecommerce
```

Check the table:

``` sql
SELECT * FROM users;
SELECT * FROM products;
SELECT * FROM orders;
```

------------------------------------------------------------------------

## 📂 **Database Schema via init.sql**

`db/init.sql` automatically creates:

``` sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);
```

------------------------------------------------------------------------

## 📊 **Prometheus & Grafana Monitoring**

### ✅ **Access Prometheus**

```
http://localhost:9090
```

Prometheus automatically scrapes metrics from APISIX on port 9091.

### ✅ **Access Grafana**

```
http://localhost:3000
```

**Default credentials:**
- Username: `admin`
- Password: `admin`

### ✅ **Pre-configured Dashboard**

The dashboard **"APISIX Gateway Monitoring"** is automatically provisioned with:

- **HTTP Requests Per Second** - Real-time traffic visualization
- **Request Latency (p95, p99)** - Performance metrics
- **HTTP Status Codes Distribution** - Success/error rates
- **Request Distribution by Route** - Traffic split across endpoints

Navigate to **Dashboards → APISIX Gateway Monitoring** after logging in.

### 📈 **Available APISIX Metrics**

The APISIX Prometheus plugin exposes:

```
apisix_http_requests_total          # Total HTTP requests by route/status
apisix_http_requests_duration_ms    # Request duration histogram
apisix_upstream_latency_ms          # Upstream service latency
apisix_limit_req_count              # Rate limit hits
apisix_limit_conn_count             # Connection limit hits
```

### 🔧 **Create Custom Dashboards**

1. **Via Grafana UI:**
   - Go to **Dashboards → New Dashboard**
   - Click **Add Panel**
   - Select Prometheus as data source
   - Write PromQL queries (e.g., `rate(apisix_http_requests_total[5m])`)

2. **Via JSON file:**
   - Add JSON dashboard to `grafana/provisioning/dashboards/`
   - Restart containers: `docker compose up -d`

### 💾 **Persistent Storage**

- **Prometheus data**: Stored in `prometheus_data` volume
- **Grafana config**: Stored in `grafana_data` volume
- Survives container restarts

### 📊 **Example PromQL Queries**

```promql
# Requests per second by route
rate(apisix_http_requests_total[1m])

# Error rate (5xx)
rate(apisix_http_requests_total{status=~"5.."}[1m])

# P99 latency
histogram_quantile(0.99, rate(apisix_latency_bucket[5m]))

# Upstream service latency
histogram_quantile(0.95, rate(apisix_upstream_latency_bucket[5m]))
```

------------------------------------------------------------------------

## 🎯 Project Summary

You now have:

-   3 Flask microservices (users, products, orders)
-   1 PostgreSQL database with auto‑created tables
-   APISIX as an API Gateway routing traffic
-   **Prometheus** for metrics collection
-   **Grafana** with auto-provisioned APISIX dashboard
-   Docker Compose orchestrating everything

Everything is aligned for a complete distributed systems + networking
university project with monitoring & observability.

------------------------------------------------------------------------

Made with ❤️ by **Shazan**
