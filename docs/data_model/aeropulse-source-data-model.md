# AeroPulse Source Data Model

## 1. Purpose

This document defines the initial source-system data model for the AeroPulse Enterprise Lakehouse Platform.

The model represents a fictional aerospace engine manufacturing, engineering, maintenance, flight operations, supply chain, and manufacturing environment.

All data used in this project will be synthetic.

---

## 2. Business Domains

The initial platform includes the following domains:

1. Reference and Master Data
2. Aircraft and Engine Fleet
3. Flight Operations
4. Engine Telemetry
5. Maintenance and Engineering
6. Parts and Supply Chain
7. Manufacturing and Quality

---

# 3. Reference and Master Data

## 3.1 airlines

Represents airline customers and operators.

Primary key:

```text
airline_id
```

Important attributes:

* airline_name
* airline_code
* country
* region
* customer_status

Expected volume:

```text
500–1,000 records
```

---

## 3.2 airports

Represents airport master data.

Primary key:

```text
airport_id
```

Important attributes:

* airport_name
* iata_code
* icao_code
* city
* country
* latitude
* longitude

Expected volume:

```text
2,000–5,000 records
```

---

## 3.3 engine_models

Represents engine model reference information.

Primary key:

```text
engine_model_id
```

Important attributes:

* engine_model_name
* engine_family
* thrust_rating
* manufacturer
* generation

Expected volume:

```text
20–100 records
```

---

## 3.4 suppliers

Represents supplier master data.

Primary key:

```text
supplier_id
```

Important attributes:

* supplier_name
* supplier_country
* supplier_category
* risk_rating
* supplier_status

Expected volume:

```text
5,000–20,000 records
```

---

## 3.5 parts

Represents aircraft and engine component master data.

Primary key:

```text
part_id
```

Important attributes:

* part_number
* part_name
* part_category
* supplier_id
* unit_cost
* part_status

Expected volume:

```text
100,000+ records
```

---

# 4. Aircraft and Engine Fleet

## 4.1 aircraft

Represents aircraft master data.

Primary key:

```text
aircraft_id
```

Foreign key:

```text
airline_id
```

Important attributes:

* aircraft_registration
* aircraft_model
* airline_id
* manufacture_date
* aircraft_status

---

## 4.2 engines

Represents individual aircraft engines.

Primary key:

```text
engine_id
```

Foreign key:

```text
engine_model_id
```

Important attributes:

* engine_serial_number
* engine_model_id
* manufacture_date
* total_flight_hours
* engine_status

---

## 4.3 engine_installations

Represents the installation history of engines on aircraft.

Primary key:

```text
installation_id
```

Foreign keys:

```text
engine_id
aircraft_id
```

Important attributes:

* installation_date
* removal_date
* installation_position
* installation_status

---

# 5. Flight Operations

## 5.1 flights

Represents aircraft flight activity.

Primary key:

```text
flight_id
```

Foreign keys:

```text
aircraft_id
airline_id
origin_airport_id
destination_airport_id
```

Important attributes:

* flight_number
* aircraft_id
* departure_timestamp
* arrival_timestamp
* flight_hours
* flight_status

Expected volume:

```text
5,000,000+ records
```

---

## 5.2 flight_engine_usage

Represents the engines used during each flight.

Primary key:

```text
flight_engine_usage_id
```

Foreign keys:

```text
flight_id
engine_id
```

Important attributes:

* flight_id
* engine_id
* engine_position
* flight_hours
* cycles_completed

---

# 6. Engine Telemetry

## 6.1 engine_telemetry

Represents high-volume sensor data generated from aircraft engines.

Primary key:

```text
telemetry_id
```

Foreign keys:

```text
engine_id
flight_id
```

Important attributes:

* telemetry_timestamp
* engine_id
* flight_id
* temperature
* pressure
* vibration
* rpm
* fuel_flow
* oil_pressure
* altitude

Expected volume:

```text
10,000,000+ records
```

This will be the primary high-volume dataset used for:

* Structured Streaming
* Incremental ingestion
* Data quality
* Performance tuning
* Engine health analytics
* Machine learning

---

# 7. Maintenance and Engineering

## 7.1 maintenance_events

Primary key:

```text
maintenance_event_id
```

Foreign key:

```text
engine_id
```

Important attributes:

* maintenance_type
* maintenance_timestamp
* issue_code
* maintenance_cost
* downtime_hours
* maintenance_status

---

## 7.2 maintenance_work_orders

Primary key:

```text
work_order_id
```

Foreign key:

```text
maintenance_event_id
engine_id
```

Important attributes:

* work_order_type
* priority
* assigned_team
* start_timestamp
* completion_timestamp
* work_order_status

---

## 7.3 engine_component_removals

Primary key:

```text
component_removal_id
```

Foreign keys:

```text
engine_id
part_id
```

Important attributes:

* removal_timestamp
* removal_reason
* component_age_hours
* replacement_required

---

# 8. Parts and Supply Chain

## 8.1 inventory

Primary key:

```text
inventory_id
```

Foreign keys:

```text
part_id
```

Important attributes:

* warehouse_id
* available_quantity
* reserved_quantity
* reorder_level
* last_updated_timestamp

---

## 8.2 purchase_orders

Primary key:

```text
purchase_order_id
```

Foreign keys:

```text
supplier_id
```

Important attributes:

* order_date
* expected_delivery_date
* order_status
* order_value

---

## 8.3 supplier_deliveries

Primary key:

```text
delivery_id
```

Foreign keys:

```text
purchase_order_id
supplier_id
```

Important attributes:

* delivery_date
* expected_delivery_date
* delivered_quantity
* delivery_status

---

# 9. Manufacturing and Quality

## 9.1 manufacturing_batches

Primary key:

```text
batch_id
```

Important attributes:

* manufacturing_site
* production_start_date
* production_end_date
* batch_status
* quantity_produced

---

## 9.2 quality_inspections

Primary key:

```text
inspection_id
```

Foreign keys:

```text
batch_id
part_id
```

Important attributes:

* inspection_timestamp
* inspection_type
* inspection_result
* defect_code
* quality_score

---

# 10. Relationship Summary

```text
AIRLINES
    |
    └── AIRCRAFT
          |
          └── ENGINE INSTALLATIONS
                  |
                  └── ENGINES
                         |
                         ├── ENGINE TELEMETRY
                         ├── MAINTENANCE EVENTS
                         ├── WORK ORDERS
                         ├── COMPONENT REMOVALS
                         └── FLIGHT ENGINE USAGE

FLIGHTS
    |
    └── FLIGHT ENGINE USAGE

SUPPLIERS
    |
    ├── PARTS
    ├── PURCHASE ORDERS
    └── SUPPLIER DELIVERIES

PARTS
    |
    ├── INVENTORY
    ├── COMPONENT REMOVALS
    └── QUALITY INSPECTIONS

MANUFACTURING BATCHES
    |
    └── QUALITY INSPECTIONS
```

---

# 11. Source Data Volume Strategy

The project will use progressively increasing data volumes.

## Initial Development Volume

```text
Thousands to hundreds of thousands of records
```

## Performance Testing Volume

```text
One million to several million records
```

## Large-Scale Simulation

```text
Ten million or more telemetry records where practical
```

The platform will first be validated using smaller datasets before larger data volumes are generated.

---

# 12. Source Data Formats

| Domain            | Initial Source Format |
| ----------------- | --------------------- |
| Reference Data    | CSV                   |
| Fleet Data        | JSON                  |
| Flight Operations | Parquet               |
| Engine Telemetry  | JSON                  |
| Maintenance       | CSV                   |
| Supply Chain      | Parquet               |
| Manufacturing     | JSON                  |

The platform will later include:

* Batch ingestion
* Incremental ingestion
* Structured Streaming
* API ingestion simulation
