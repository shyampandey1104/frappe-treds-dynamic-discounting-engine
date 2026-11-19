import unittest
from treds_dynamic_discounting.engine import SupplierPayableInvoice, TReDSDynamicDiscountingEngine

class TestTReDSDynamicDiscountingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = TReDSDynamicDiscountingEngine(buyer_corporate_pan="AAACT9901Z")
        self.inv = SupplierPayableInvoice(
            invoice_number="INV-MSME-2026-081", supplier_name="Shree Precision Works",
            supplier_pan="AAAFP5512K", invoice_date="2026-03-01", due_date="2026-04-15",
            net_payable_amount_inr=1000000.0, standard_credit_period_days=45
        )
        self.engine.register_invoice(self.inv)

    def test_dynamic_discount_computation(self):
        offer = self.engine.compute_dynamic_discount_offer("INV-MSME-2026-081", days_early_payment=35, annualized_discount_rate_pct=14.0)
        self.assertGreater(offer["discount_earned_by_buyer"], 0)
        self.assertEqual(offer["immediate_payout_to_supplier"] + offer["discount_earned_by_buyer"], 1000000.0)

    def test_treds_factoring(self):
        res = self.engine.settle_via_treds_factoring("INV-MSME-2026-081", "RXIL", "Axis Bank", bid_interest_rate_pct=8.5)
        self.assertEqual(res["status"], "TREDS_FACTORING_SUCCESS")
        self.assertGreater(res["disbursed_to_msme"], 980000.0)

if __name__ == "__main__":
    unittest.main()
