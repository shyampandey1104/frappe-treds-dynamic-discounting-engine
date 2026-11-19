# Frappe TReDS Invoice Factoring & Early Payment Dynamic Discounting Engine

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![TReDS RBI](https://img.shields.io/badge/RBI-TReDS%20Factoring-purple.svg)]()
[![Working Capital](https://img.shields.io/badge/Finance-Supply%20Chain%20Finance-teal.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

Cash flow delays severely impact MSME suppliers who typically endure 45 to 90 days credit periods from corporate enterprise buyers.

**The Financial Dilemma:**
1. **Idle Corporate Treasury Cash:** Large enterprises hold idle cash earning meager 6-7% bank returns, while their MSME vendors pay 14-18% for working capital loans.
2. **Dynamic Discounting Gap:** Enterprise buyers lack an automated sliding-scale discount engine to offer suppliers early payment (e.g. paying on Day 10 instead of Day 45 in exchange for an annualized 12-15% discount).
3. **TReDS Portal Disconnect:** Transferring approved Purchase Invoices to RBI-authorized TReDS platforms (RXIL, M1xchange, Invoicemart) for auction bidding requires automated API reconciliation.

This Frappe application unifies corporate Treasury Dynamic Discounting with institutional TReDS invoice factoring.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["ERPNext Approved Purchase Invoice (Due in 45 Days)"] -->|Eligible for Acceleration| B["SCF Working Capital Engine"]
    B --> C{"Financing Path Selection"}
    C -->|Option A: Corporate Self-Financed| D["Dynamic Discounting Engine"]
    D -->|Sliding Scale Discount (e.g. 1.2% for 35 days early)| E["Early Disbursal to MSME Vendor"]
    E -->|Buyer Realizes High Annualized Yield| F["Accounts Payable Ledger Settlement"]
    C -->|Option B: External Factoring| G["TReDS Portal API (RXIL / M1xchange)"]
    G -->|Financiers Bid Lowest Discount Rate| H["Best Bid Factoring Disbursal to MSME"]
    H -->|Due Date Settlement| I["Buyer Pays Full Invoice to Financier on Day 45"]
```

---

## 🚀 Key Engineering Capabilities

- **Sliding-Scale Discount Calculator:** Mathematically computes exact discount yields based on days early paid and target hurdle rates.
- **TReDS Exchange Interface:** Formats invoice factoring payloads for automated upload to institutional factoring platforms.
- **Automated MSME Payment Advice:** Generates instant settlement advice and updates ERPNext Accounts Payable registers.
- **Treasury ROI Analytics:** Measures corporate annualized yield on early payouts vs overnight liquid fund returns.

---

## 📂 Frappe DocType Schema & Data Structure

```text
treds_dynamic_discounting/
├── treds_dynamic_discounting_core/
│   ├── doctype/
│   │   ├── supplier_payable_invoice/
│   │   │   ├── supplier_payable_invoice.json
│   │   │   ├── supplier_payable_invoice.py
│   │   │   └── supplier_payable_invoice.js
│   │   └── treds_factoring_trade/
│   │       └── treds_factoring_trade.json
│   └── workspace/
│       └── treds_dynamic_discounting_workspace/
│           └── treds_dynamic_discounting_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/treds_dynamic_discounting.api.compute_dynamic_discount_offer`
- **Whitelisted Method:** `@frappe.whitelist() def settle_via_treds_factoring(invoice_number, treds_portal, financier_name, bid_interest_rate_pct)`
- **Hooks Event:** `on_submit` of `Purchase Invoice` tags early-payment eligible MSME invoices.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/frappe-treds-dynamic-discounting-engine
bench --site erp.yourdomain.com install-app treds_dynamic_discounting
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Built for Enterprise CFOs, Treasury Managers, and Supply Chain Finance Desks.
