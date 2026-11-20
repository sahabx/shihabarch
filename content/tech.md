---
title: Tech Toolkit
status: reviewed
---

# Tech Toolkit

For the curious and the technical reviewer: the actual tools behind the work, explained in plain English. The rest of the site keeps this terminology out of your way.

## Infrastructure — where things run

| Term | Plain English |
|---|---|
| Self-hosted | Your software runs on servers you control, not on a vendor's. |
| Open-source | The code is free for anyone to inspect, modify, and run. |
| VPS | A rented server on the internet — your own machine in a data center. |
| Docker | Packs software so it runs identically on any machine. |
| Traefik | Routes visitors to the right app and handles secure connections automatically. |
| Tailscale | A private network so servers talk to each other without being on the public internet. |
| Kubernetes | Runs and scales containerized apps across many servers. |
| Proxmox | Turns a physical server into multiple isolated virtual machines. |
| Air-gapped | A system kept fully off the public internet. |
| SSL / HTTPS | Encrypts the connection between a visitor and the server. |

## Data — where information lives

| Term | Plain English |
|---|---|
| PostgreSQL | A powerful, widely used database. |
| NocoDB | A spreadsheet-style interface on top of a real database. |
| Twenty (CRM) | An open-source customer-relationship system — a smart address book plus a sales pipeline. |
| Row-level security | A rule so each person sees only the rows that belong to them. |
| OpenRefine | A tool for cleaning messy data (duplicates, bad formats). |
| Teable / Grist / Mathesar | Open-source database tools with spreadsheet-style interfaces. |
| Grafana | Turns live data into dashboards and charts. |

## Automation & AI

| Term | Plain English |
|---|---|
| n8n | Connects your apps so work flows automatically between them. |
| Chatwoot | One shared inbox for WhatsApp, Messenger, TikTok and more. |
| Botpress / Dify | Tools for building AI chatbots and automatic replies. |
| LLM | "Large language model" — the engine that writes answers (e.g. DeepSeek, Qwen). |
| RAG | "Retrieval-augmented generation" — the AI looks up your own documents before answering, so it doesn't invent facts. |
| WhisperX | Turns long audio into text. |
| MCP | A standard way to let AI assistants use your own tools and data. |
| CLI agents | AI agents that work in the terminal — running commands and code. |
| LangChain | A toolkit for building AI applications that chain models and data. |
| Cron job | A task that runs automatically on a schedule. |
| TTS / ASR | Text-to-speech / speech-to-text. |

## Connections & APIs

| Term | Plain English |
|---|---|
| API | A doorway that lets two programs talk to each other. |
| WhatsApp / Messenger / TikTok Business API | Official doorways to send and receive platform messages from your own system. |
| Eazypay | A local payment gateway. |
| Webhook | A signal that fires when something happens ("a new message arrived"). |
| Markdown | Plain-text formatting that both people and machines can read. |
| Git | Version history for code — every change is kept, nothing is lost. |

## How the on-site AI works

- This site publishes the same content twice: as pages for people, and as plain files (`llms.txt`, `.md` twins, JSON) that machines can read.
- When you type a question, the assistant finds the most relevant pieces of that content.
- If a language model is connected, it writes a short answer using only those pieces — with links to the sources. If not, it shows the most relevant page directly.
- Either way, it never invents numbers that aren't already on the site.