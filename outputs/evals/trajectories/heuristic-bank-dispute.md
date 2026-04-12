# Trajectory: heuristic / bank_dispute

- Score: `0.990`
- Path: `bank_home -> help_center -> card_disputes -> dispute_documentation -> card_dispute_evidence_upload_form`

```mermaid
graph TD
    node_bank_home["Pine Street Bank"]
    class node_bank_home start,visited
    node_bank_home -->|"Help Center"| node_help_center:::pathEdge
    node_bank_home -->|"Security Center"| node_security_center
    node_bank_home -->|"Cards"| node_cards
    node_help_center["Help Center"]
    class node_help_center visited
    node_help_center -->|"Card Disputes"| node_card_disputes:::pathEdge
    node_help_center -->|"Fraud and Security"| node_security_center
    node_help_center -->|"Contact Support"| node_contact_support
    node_card_disputes["Card Disputes"]
    class node_card_disputes visited
    node_card_disputes -->|"Documentation and Evidence"| node_dispute_documentation:::pathEdge
    node_card_disputes -->|"Dispute Policies"| node_dispute_policies
    node_card_disputes -->|"Dispute Hotline"| node_dispute_hotline
    node_dispute_documentation["Documentation and Evidence"]
    class node_dispute_documentation visited
    node_dispute_documentation -->|"Card Dispute Evidence Upload Form"| node_card_dispute_evidence_upload_form:::pathEdge
    node_dispute_documentation -->|"Evidence Checklist"| node_evidence_checklist
    node_dispute_documentation -->|"Card Disputes"| node_card_disputes
    node_security_center["Security Center"]
    node_security_center -->|"Fraud Hotline"| node_fraud_hotline
    node_security_center -->|"Help Center"| node_help_center
    node_cards["Cards"]
    node_cards -->|"Help Center"| node_help_center
    node_dispute_policies["Dispute Policies"]
    node_dispute_policies -->|"Card Disputes"| node_card_disputes
    node_dispute_hotline["Dispute Hotline"]
    node_dispute_hotline -->|"Card Disputes"| node_card_disputes
    node_fraud_hotline["Fraud Hotline"]
    node_fraud_hotline -->|"Security Center"| node_security_center
    node_contact_support["Contact Support"]
    node_contact_support -->|"Help Center"| node_help_center
    node_evidence_checklist["Evidence Checklist"]
    node_evidence_checklist -->|"Documentation and Evidence"| node_dispute_documentation
    node_card_dispute_evidence_upload_form["Card Dispute Evidence Upload Form"]
    class node_card_dispute_evidence_upload_form target,visited
    classDef start fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px;
    classDef target fill:#ffe5d9,stroke:#bc3908,stroke-width:3px;
    classDef visited fill:#e9f5ff,stroke:#1d4ed8,stroke-width:2px;
    classDef pathEdge stroke:#1d4ed8,stroke-width:3px;
```
