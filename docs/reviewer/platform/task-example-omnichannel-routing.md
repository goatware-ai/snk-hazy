# Task Example: Omnichannel Routing Evaluation

> **Inherited from the Geranium desk, not confirmed for Hazy.** This document describes
> Geranium's reviewer rules. Hazy offers no review assignments. It is kept for reference and was NOT updated in the 2026-09-21 port; treat
> anything it says about sector, rubric bands or platform checks as Geranium's, not
> this project's. See `../../RULE-DELTAS.md`.

Snorkel AI | Proprietary & Confidential | Not for Distribution

> **What this is.** An example **golden solution**, captured from the **Reviewers' Hub** and filed
> on the reviewer side because that is where the platform publishes it: it is the finished
> deliverable a task of this shape is expected to produce, shown to reviewers as the standard they
> judge a golden against. It carries no annotation of its own, unlike the annotated good/bad
> comparison in `../../submission/platform/task-example-wholesale-trade.md`.
>
> Authors can read it too — it is the bar a golden has to clear — but it is a reviewer document,
> not part of the authoring rule set.
>
> It is a **document deliverable** (an evaluation memo), not a workbook, and it sits in a different
> sector from this portfolio's Wholesale Trade work: retail / e-commerce omnichannel order
> management. Read it for deliverable *shape* and evidentiary standard, not for scenario reuse.
>
> Every figure in it reconciles exactly (verified 2026-08-26): 24.99 - 12.45 = 12.54 margin;
> 12.54 - 11.37 = 1.17 projected; 11.37 x 8.5% = 0.97; 11.37 + 0.97 + 3.75 = 16.09; 12.54 - 16.09
> = -3.55; 200 - 76 = 124; 60 / 124 = 48.39%.

## Executive Summary

An operations review of the Omni-Route 360 order management system was conducted to evaluate the vendor's claims regarding algorithmic profitability and carrier compliance.

The daily routing log contained 200 total e-commerce transactions across the active operational window. Of these, 76 transactions used Buy Online, Pick Up In Store (BOPIS) fulfillment. Under Article 1 of the standard operating procedures (SOP), BOPIS orders incur no outbound shipping or packaging costs and were therefore excluded from the compliance metric.

The remaining 124 transactions represent the valid Ship-From-Store (SFS) baseline. Evaluation of these routings against applicable operating constraints found that 60 distinct orders were approved in violation of financial or regulatory parameters, resulting in a 48.39% systemic algorithmic failure rate.

Key Finding: 60 of 124 valid SFS orders violated at least one financial or regulatory operating constraint.

---

## 1. Profitability Logic Failure

The primary cause of store-level financial losses is the algorithm's failure to account for secondary physical logistics costs when performing its baseline profitability calculation.

Under Article 6 of the SOP:

- Base shipping costs are subject to an 8.5% peak-volume surcharge.
- Fragile items incur an additional $3.75 packaging fee per unit.

The routing algorithm currently subtracts only the raw base shipping cost from gross margin. By omitting these required accessorial costs, the system creates an artificially low profitability threshold and approves orders that become unprofitable once actual fulfillment expenses are applied.

### Impact

44 distinct SFS orders generated net-negative margins as a result of this missing logic.

### Example: Order `WEB-Q0Y9DO`

| Metric | Amount |
| --- | --- |
| Product | Ceramic Candle (`BT-50212`) |
| Retail Price | $24.99 |
| Cost of Goods Sold | $12.45 |
| Gross Margin | $12.54 |
| Base Shipping Cost | $11.37 |
| System-Projected Net Profit | $1.17 |
| 8.5% Peak-Volume Surcharge | $0.97 |
| Fragile-Item Packaging Fee | $3.75 |
| True Fulfillment Cost | $16.09 |
| Actual Net Operational Result | -$3.55 |

The system approved the order based on a projected $1.17 profit. Once the mandatory surcharge and packaging fee are included, however, the order produces an actual $3.55 operational loss for the retail store.

---

## 2. Hazardous Materials Routing Failure

In addition to margin erosion, the routing algorithm fails to enforce mandatory transit restrictions for hazardous materials, creating significant compliance and enterprise-level liability.

Under Article 4 of the SOP, Department of Transportation restrictions prohibit Class 2.1 Flammable Gases from being shipped through the Air Express network. As a result, these products must never be routed via SFS to Zones 7 or 8.

The routing log identifies the following products as carrying the Class 2.1 hazardous material designation:

| Product | SKU |
| --- | --- |
| Dry Shampoo Aerosol | `HC-99201` |
| Hairspray Aerosol | `HC-88102` |
| Texture Spray | `HC-88105` |

### Impact

The routing algorithm approved these restricted products for cross-country Air Express destinations on 23 separate occasions.

### Example: Order `WEB-26Q3XL`

Order `WEB-26Q3XL` provides a direct example of this compliance failure. The system approved an aerosol product for shipment to Zone 7, despite its Class 2.1 designation.

By tendering Class 2.1 materials to the air transit network, the routing engine violates the restrictions established under the master carrier agreement.

---

## 3. Overall Assessment

The vendor's claim that Omni-Route 360 safeguards margin and adheres to applicable shipping policies is not supported by the routing-log analysis.

Two foundational deficiencies were identified:

1. Incomplete profitability calculations: The algorithm does not incorporate required secondary fulfillment costs, including peak-volume surcharges and fragile-item packaging fees.
2. Insufficient hazardous-material controls: The algorithm does not reliably enforce zone-based transit restrictions for Class 2.1 commodities.

Together, these deficiencies resulted in 60 noncompliant SFS routings out of 124 evaluated transactions, representing a 48.39% failure rate.

---

## 4. Required Remediation

Immediate technical remediation is required to prevent continued unprofitable fulfillment decisions and address carrier-compliance exposure.

The routing logic should be updated to:

- Incorporate all applicable shipping surcharges and packaging fees into profitability calculations before approving SFS fulfillment.
- Identify Class 2.1 hazardous commodities and prevent SFS routing to Zones 7 and 8 when Air Express transportation would be required.
- Validate routing decisions against applicable financial and regulatory constraints before order approval.

### Interim Operational Control

Until the routing parameters are corrected and validated, store managers should be granted emergency authorization to manually short-ship any algorithmically approved SFS order containing Class 2.1 aerosols destined for Zones 7 or 8.
