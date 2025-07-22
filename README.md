# 🤖 AI-Powered E-Commerce Analytics Assistant

A powerful data assistant that transforms e-commerce analytics by converting natural language questions into SQL queries and dynamic visualizations.

Built using **Flask**, **SQLite**, **Matplotlib**, and **Gemma 2B LLM via Ollama**, this project brings accessible data-driven insights to non-technical users.

## 🌟 Key Features

- 🧠 **Ask Anything in Natural Language**  
  No need to write SQL! Just type:  
  > *"Show ROAS per day for the last month"*  
  > *"Top 10 customers by purchase value"*

- 💬 **LLM-Powered SQL Translation**  
  Uses `Gemma:2b` from Ollama to convert user prompts into valid, schema-aware SQL queries.

- 🔐 **Private & Local**  
  Entire pipeline runs on your machine — no cloud APIs or third-party data sharing.

- ⚡ **Real-Time Execution**  
  Instant results from a local SQLite database with clear insights.

## Motivation

Data-driven decision-making in e-commerce often requires SQL expertise. This assistant bridges the gap between business teams and raw data, allowing anyone to:

- Understand performance metrics like ROAS, CPC, sales trends  
- Analyze customer behavior  
- Discover high-performing products  
- Get visual feedback from charts
