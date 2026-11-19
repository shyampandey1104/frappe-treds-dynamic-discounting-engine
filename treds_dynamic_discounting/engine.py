"""TReDS (Trade Receivables Discounting System) & Early Payment Dynamic Discounting Engine."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class SupplierPayableInvoice:
    invoice_number: str
    supplier_name: str
    supplier_pan: str
    invoice_date: str
    due_date: str
    net_payable_amount_inr: float
    standard_credit_period_days: int = 45

class TReDSDynamicDiscountingEngine:
    def __init__(self, buyer_corporate_pan: str):
        self.buyer_corporate_pan = buyer_corporate_pan
        self.invoices: Dict[str, SupplierPayableInvoice] = {}
        self.factored_settlements: List[Dict[str, Any]] = []

    def register_invoice(self, inv: SupplierPayableInvoice) -> Dict[str, Any]:
        self.invoices[inv.invoice_number] = inv
        return {"invoice_number": inv.invoice_number, "payable": inv.net_payable_amount_inr}

    def compute_dynamic_discount_offer(self, invoice_number: str, days_early_payment: int, annualized_discount_rate_pct: float = 12.0) -> Dict[str, Any]:
        if invoice_number not in self.invoices:
            raise ValueError(f"Invoice {invoice_number} not found.")
        inv = self.invoices[invoice_number]
        
        # Sliding scale discount: (Annual Rate / 365) * Days Early
        discount_pct = (annualized_discount_rate_pct / 365.0) * days_early_payment
        discount_amount = round(inv.net_payable_amount_inr * (discount_pct / 100.0), 2)
        accelerated_payout = round(inv.net_payable_amount_inr - discount_amount, 2)

        return {
            "invoice_number": invoice_number,
            "original_amount": inv.net_payable_amount_inr,
            "days_early_paid": days_early_payment,
            "effective_discount_pct": round(discount_pct, 3),
            "discount_earned_by_buyer": discount_amount,
            "immediate_payout_to_supplier": accelerated_payout
        }

    def settle_via_treds_factoring(self, invoice_number: str, treds_portal: str, financier_name: str, bid_interest_rate_pct: float) -> Dict[str, Any]:
        if invoice_number not in self.invoices:
            raise ValueError(f"Invoice {invoice_number} not found.")
        inv = self.invoices[invoice_number]
        
        haircut = round(inv.net_payable_amount_inr * (bid_interest_rate_pct / 100.0) * (inv.standard_credit_period_days / 365.0), 2)
        disbursed_to_msme = round(inv.net_payable_amount_inr - haircut, 2)

        record = {
            "invoice_number": invoice_number,
            "treds_portal": treds_portal,
            "financier": financier_name,
            "disbursed_to_msme": disbursed_to_msme,
            "factoring_charge": haircut,
            "buyer_liability_on_due_date": inv.net_payable_amount_inr,
            "status": "TREDS_FACTORING_SUCCESS"
        }
        self.factored_settlements.append(record)
        return record
