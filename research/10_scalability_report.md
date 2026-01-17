# Scalability Analysis Report

## 1. Theoretical Bounds
- **API Throughput:** Assuming 200ms response time per connector, a single thread can process ~5 requests/second.
- **Data Volume:** 100 sources x 1000 items/day = 100,000 documents/day.

## 2. Horizontal Scaling Architecture
To support 10,000+ sources (e.g., every municipality in the US), the system is designed for **Kubernetes** deployment:
- **Scout Pods:** Stateless workers that poll assigned subsets of sources.
- **Message Queue:** RabbitMQ/Kafka distributes target assignments.
- **Database:** Sharded PostgreSQL or Document Store (MongoDB) for signal storage.

## 3. Cost Analysis
Running the prototype on AWS t3.micro is negligible (< $10/mo). Production scale (10k sources) estimated at $500/mo infrastructure cost vs $250k/yr labor savings (3 FTEs).

<!-- Refined by GovSignal Automation -->
