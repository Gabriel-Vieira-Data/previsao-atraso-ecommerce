# 📦 Pipeline End-to-End: Previsão de Atrasos no E-commerce (Olist)

Este projeto consiste no desenvolvimento de um pipeline de dados ponta a ponta (*end-to-end*), integrando práticas modernas de **Engenharia de Dados**, **Ciência de Dados** e **MLOps**. O principal objetivo é prever a probabilidade de atraso nas entregas de uma plataforma de e-commerce brasileira, utilizando o conjunto de dados público da Olist.

A arquitetura foi desenhada sob a premissa de **otimização de custos (Zero-Budget Architecture)**, demonstrando como construir uma infraestrutura robusta, escalável e totalmente gratuita.

---

## 🏗️ Arquitetura do Projeto

```mermaid
flowchart TD
    A[Dataset Olist<br/>Kaggle - E-commerce BR] --> B[Ingestão<br/>Python + DuckDB]
    B --> C[Dados processados<br/>Parquet/DuckDB]
    C --> D[EDA + Feature Engineering<br/>distância, prazo, pagamento]
    D --> E[Modelo AutoML<br/>PyCaret]
    E --> F[Previsão de atraso<br/>na entrega]

    C -.-> G[Orquestração<br/>Airflow/Dagster]
    C -.-> H[Transformação em camadas<br/>dbt - silver/gold]
    E -.-> I[Feature store<br/>Feast]
    F -.-> J[Dashboard<br/>Streamlit/Power BI]

    style A fill:#d9f2ec,stroke:#0f6e56,color:#0f6e56
    style B fill:#d9f2ec,stroke:#0f6e56,color:#0f6e56
    style C fill:#d9f2ec,stroke:#0f6e56,color:#0f6e56
    style D fill:#d9f2ec,stroke:#0f6e56,color:#0f6e56
    style E fill:#d9f2ec,stroke:#0f6e56,color:#0f6e56
    style F fill:#d9f2ec,stroke:#0f6e56,color:#0f6e56
    style G fill:#f4f4f4,stroke:#888,color:#666
    style H fill:#f4f4f4,stroke:#888,color:#666
    style I fill:#f4f4f4,stroke:#888,color:#666
    style J fill:#f4f4f4,stroke:#888,color:#666
