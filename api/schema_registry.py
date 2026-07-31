"""Domain- and use-case-specific Schema Registry for GRAPHEN journeys."""
from __future__ import annotations

import json
import re
from typing import Any

from loguru import logger
from pydantic import BaseModel


def _node(label: str, primary_key: str, properties: str) -> dict:
    return {"label": label, "primary_key": primary_key, "key_properties": properties}


def _rel(rel_type: str, from_label: str, to_label: str, description: str) -> dict:
    return {
        "type": rel_type,
        "from": from_label,
        "to": to_label,
        "description": description,
    }


# Illustrative schemas keyed by industry → use case.
# These guide upload expectations; they are not a live Neo4j catalog.
SCHEMA_LIBRARY: dict[str, dict[str, dict[str, Any]]] = {
    "Financial Services": {
        "Financial Crime & AML": {
            "nodes": [
                _node("Individual", "individual_id", "name, dob, nationality, risk_score"),
                _node("Company", "company_id", "legal_name, jurisdiction, ubo_flag"),
                _node("Account", "account_id", "iban, currency, open_date, status"),
                _node("Transaction", "txn_id", "amount, currency, channel, timestamp"),
                _node("Device", "device_id", "imei, ip, fingerprint"),
                _node("Address", "address_id", "line1, city, country, postal_code"),
                _node("SanctionEntity", "sanction_id", "list_name, match_score, status"),
                _node("Regulation", "reg_id", "standard, version, requirement"),
            ],
            "relationships": [
                _rel("OWNS", "Individual", "Account", "Customer ownership of accounts"),
                _rel("TRANSFERRED_TO", "Account", "Account", "Fund movement between accounts"),
                _rel("EXECUTED_BY", "Transaction", "Individual", "Transaction initiator"),
                _rel("USES_DEVICE", "Individual", "Device", "Shared device usage"),
                _rel("LOCATED_AT", "Individual", "Address", "Residential or business address"),
                _rel("MATCHES_SANCTION", "Individual", "SanctionEntity", "Sanctions screening hit"),
            ],
            "upload_guidance": {
                "structured": [
                    "Individuals / customers CSV (id, name, risk attributes)",
                    "Companies / UBO CSV",
                    "Accounts and transactions CSV",
                    "Devices and addresses CSV",
                    "Sanctions / watchlist CSV",
                ],
                "unstructured": [
                    "AML / KYC policy PDFs",
                    "STR / SAR guidance documents",
                    "Investigation notes or case summaries",
                    "Regulatory circulars (PMLA, OFAC, local AML rules)",
                ],
                "why": "These sources populate people, accounts, flows, and sanctions edges used by AML ring and exposure detections.",
            },
        },
        "Customer 360": {
            "nodes": [
                _node("Customer", "customer_id", "name, segment, tenure, channel"),
                _node("Account", "account_id", "product_type, balance, status"),
                _node("Product", "product_id", "name, category, risk_band"),
                _node("Interaction", "interaction_id", "channel, sentiment, timestamp"),
                _node("Household", "household_id", "size, region"),
                _node("Branch", "branch_id", "city, region"),
                _node("Complaint", "complaint_id", "category, severity, status"),
                _node("Campaign", "campaign_id", "channel, offer_type"),
            ],
            "relationships": [
                _rel("HOLDS", "Customer", "Account", "Customer product holdings"),
                _rel("SUBSCRIBED_TO", "Customer", "Product", "Product enrollment"),
                _rel("HAS_INTERACTION", "Customer", "Interaction", "Service or sales touchpoint"),
                _rel("BELONGS_TO", "Customer", "Household", "Household grouping"),
                _rel("SERVICED_BY", "Customer", "Branch", "Primary servicing location"),
                _rel("RAISED", "Customer", "Complaint", "Complaint ownership"),
            ],
            "upload_guidance": {
                "structured": [
                    "Customer master CSV",
                    "Accounts / products CSV",
                    "Interaction / CRM events CSV",
                    "Complaints and campaign response CSV",
                ],
                "unstructured": [
                    "Call transcripts or chat logs",
                    "Product brochures and policy terms",
                    "Branch or service SOP documents",
                ],
                "why": "A unified customer graph needs both master data and interaction evidence across channels.",
            },
        },
        "Credit Risk Intelligence": {
            "nodes": [
                _node("Borrower", "borrower_id", "name, segment, rating"),
                _node("Facility", "facility_id", "limit, utilisation, currency"),
                _node("Collateral", "collateral_id", "type, value, haircut"),
                _node("Counterparty", "counterparty_id", "sector, country, rating"),
                _node("Guarantee", "guarantee_id", "guarantor, amount, expiry"),
                _node("RatingEvent", "event_id", "agency, grade, date"),
                _node("Covenant", "covenant_id", "type, threshold, status"),
                _node("Document", "doc_id", "doc_type, effective_date"),
            ],
            "relationships": [
                _rel("HAS_FACILITY", "Borrower", "Facility", "Credit facility ownership"),
                _rel("SECURED_BY", "Facility", "Collateral", "Collateral linkage"),
                _rel("EXPOSED_TO", "Borrower", "Counterparty", "Connected exposure"),
                _rel("GUARANTEED_BY", "Facility", "Guarantee", "Guarantee coverage"),
                _rel("HAS_RATING", "Borrower", "RatingEvent", "Rating history"),
                _rel("BOUNDED_BY", "Facility", "Covenant", "Covenant constraints"),
            ],
            "upload_guidance": {
                "structured": [
                    "Borrower / counterparty master CSV",
                    "Facilities and utilisation CSV",
                    "Collateral and guarantee CSV",
                    "Rating and covenant breach CSV",
                ],
                "unstructured": [
                    "Credit memoranda / PDFs",
                    "Facility agreements",
                    "Collateral valuation reports",
                ],
                "why": "Credit decisions require linked exposure, collateral, and covenant evidence.",
            },
        },
        "KYC & Regulatory Compliance": {
            "nodes": [
                _node("Customer", "customer_id", "name, kyc_status, risk_tier"),
                _node("IdentityDoc", "doc_id", "doc_type, issuer, expiry"),
                _node("UBO", "ubo_id", "name, ownership_pct, nationality"),
                _node("Company", "company_id", "legal_name, registration_no"),
                _node("Obligation", "obligation_id", "clause, due_date, status"),
                _node("Policy", "policy_id", "policy_name, version"),
                _node("ReviewCase", "case_id", "status, severity, opened_at"),
                _node("Regulator", "regulator_id", "name, jurisdiction"),
            ],
            "relationships": [
                _rel("PROVIDED", "Customer", "IdentityDoc", "KYC identity evidence"),
                _rel("OWNED_BY", "Company", "UBO", "Beneficial ownership"),
                _rel("SUBJECT_TO", "Customer", "Obligation", "Regulatory obligation"),
                _rel("GOVERNED_BY", "Customer", "Policy", "Applicable KYC policy"),
                _rel("UNDER_REVIEW", "Customer", "ReviewCase", "Open compliance case"),
                _rel("OVERSEEN_BY", "Obligation", "Regulator", "Supervisory authority"),
            ],
            "upload_guidance": {
                "structured": [
                    "Customer / UBO CSV",
                    "Identity document inventory CSV",
                    "Obligation / review case CSV",
                ],
                "unstructured": [
                    "KYC / CDD policy PDFs",
                    "Regulatory circulars",
                    "Onboarding forms and ID scans",
                ],
                "why": "Compliance graphs connect identity evidence, ownership, and obligation status.",
            },
        },
    },
    "Healthcare & Life Sciences": {
        "Patient Journey 360": {
            "nodes": [
                _node("Patient", "patient_id", "age_band, gender, risk_flag"),
                _node("Provider", "provider_id", "specialty, npi, facility"),
                _node("Encounter", "encounter_id", "date, type, disposition"),
                _node("Claim", "claim_id", "amount, status, diagnosis_code"),
                _node("Medication", "med_id", "name, dose, route"),
                _node("Diagnosis", "dx_id", "code, description"),
                _node("CarePlan", "plan_id", "goal, status"),
                _node("Facility", "facility_id", "name, region"),
            ],
            "relationships": [
                _rel("TREATED_BY", "Patient", "Provider", "Care relationship"),
                _rel("HAS_ENCOUNTER", "Patient", "Encounter", "Clinical visit"),
                _rel("HAS_CLAIM", "Encounter", "Claim", "Billing linkage"),
                _rel("PRESCRIBED", "Encounter", "Medication", "Medication order"),
                _rel("DIAGNOSED_WITH", "Patient", "Diagnosis", "Clinical diagnosis"),
                _rel("FOLLOWING", "Patient", "CarePlan", "Care-plan adherence"),
            ],
            "upload_guidance": {
                "structured": [
                    "Patient demographics CSV",
                    "Encounters / claims CSV",
                    "Medications and diagnoses CSV",
                    "Provider / facility roster CSV",
                ],
                "unstructured": [
                    "Discharge summaries",
                    "Care-plan notes",
                    "Clinical guidelines PDFs",
                ],
                "why": "Patient 360 needs clinical events joined to claims and care plans.",
            },
        },
        "Drug Discovery": {
            "nodes": [
                _node("DrugCandidate", "candidate_id", "name, modality, development_stage"),
                _node("MolecularTarget", "target_id", "gene_symbol, protein_family, organism"),
                _node("Compound", "compound_id", "smiles, molecular_weight, logp"),
                _node("Assay", "assay_id", "assay_type, readout, threshold"),
                _node("Indication", "indication_id", "disease_area, icd_code, prevalence"),
                _node("Study", "study_id", "phase, design, status"),
            ],
            "relationships": [
                _rel("BINDS_TO", "Compound", "MolecularTarget", "Binding / affinity evidence"),
                _rel("MODULATES", "DrugCandidate", "MolecularTarget", "Intended pharmacological action"),
                _rel("TESTED_IN", "Compound", "Assay", "In-vitro or in-vivo assay result"),
                _rel("INDICATED_FOR", "DrugCandidate", "Indication", "Therapeutic hypothesis"),
                _rel("SUPPORTED_BY", "DrugCandidate", "Study", "Preclinical or clinical evidence"),
            ],
            "upload_guidance": {
                "structured": [
                    "Compound / candidate registry CSV",
                    "Target annotation CSV",
                    "Assay result tables",
                    "Indication / disease mapping CSV",
                ],
                "unstructured": [
                    "Patent / literature PDFs",
                    "Assay protocols",
                    "Target validation memos",
                ],
                "why": "Drug discovery graphs connect candidates, targets, assays, and supporting studies.",
            },
        },
        "Clinical Trial Intelligence": {
            "nodes": [
                _node("Study", "study_id", "phase, indication, status"),
                _node("Site", "site_id", "country, investigator, capacity"),
                _node("Subject", "subject_id", "arm, enrollment_date, status"),
                _node("Protocol", "protocol_id", "version, amendment"),
                _node("AdverseEvent", "ae_id", "severity, outcome"),
                _node("Visit", "visit_id", "visit_name, date"),
                _node("LabResult", "lab_id", "analyte, value, unit"),
                _node("Investigator", "inv_id", "name, specialty"),
            ],
            "relationships": [
                _rel("CONDUCTED_AT", "Study", "Site", "Site participation"),
                _rel("ENROLLED_IN", "Subject", "Study", "Subject enrollment"),
                _rel("FOLLOWED", "Subject", "Protocol", "Protocol adherence"),
                _rel("REPORTED", "Subject", "AdverseEvent", "Safety event"),
                _rel("HAS_VISIT", "Subject", "Visit", "Scheduled visit"),
                _rel("MEASURED_IN", "LabResult", "Visit", "Lab observation"),
            ],
            "upload_guidance": {
                "structured": [
                    "Study / site / subject CSV",
                    "Visit and lab result CSV",
                    "Adverse event CSV",
                ],
                "unstructured": [
                    "Protocol documents",
                    "Investigator brochures",
                    "Safety narratives",
                ],
                "why": "Trial intelligence depends on protocol, site, subject, and safety linkage.",
            },
        },
        "Drug Safety & Pharmacovigilance": {
            "nodes": [
                _node("Product", "product_id", "name, form, strength"),
                _node("Batch", "batch_id", "lot_no, manufacture_date"),
                _node("AdverseEvent", "ae_id", "severity, outcome, reported_at"),
                _node("Patient", "patient_id", "age_band, sex"),
                _node("Signal", "signal_id", "method, score, status"),
                _node("Literature", "lit_id", "title, source"),
                _node("Regulator", "reg_id", "agency, region"),
                _node("Label", "label_id", "section, version"),
            ],
            "relationships": [
                _rel("PRODUCED_IN", "Product", "Batch", "Batch provenance"),
                _rel("ASSOCIATED_WITH", "AdverseEvent", "Product", "Product-AE link"),
                _rel("EXPERIENCED_BY", "AdverseEvent", "Patient", "Patient impact"),
                _rel("GENERATES", "AdverseEvent", "Signal", "Safety signal"),
                _rel("SUPPORTED_BY", "Signal", "Literature", "Evidence support"),
                _rel("REPORTED_TO", "Signal", "Regulator", "Regulatory reporting"),
            ],
            "upload_guidance": {
                "structured": [
                    "Product / batch CSV",
                    "Adverse event case CSV",
                    "Signal assessment CSV",
                ],
                "unstructured": [
                    "Case narratives",
                    "Label / SmPC documents",
                    "Literature extracts",
                ],
                "why": "Pharmacovigilance graphs connect products, cases, signals, and labels.",
            },
        },
        "Provider & Referral Integrity": {
            "nodes": [
                _node("Patient", "patient_id", "member_id, plan"),
                _node("Provider", "provider_id", "specialty, npi"),
                _node("Claim", "claim_id", "amount, cpt, status"),
                _node("Referral", "referral_id", "date, reason"),
                _node("Facility", "facility_id", "name, network_status"),
                _node("Diagnosis", "dx_id", "code, description"),
                _node("Network", "network_id", "plan_name, region"),
                _node("AuditFinding", "audit_id", "severity, category"),
            ],
            "relationships": [
                _rel("REFERRED_TO", "Provider", "Provider", "Referral path"),
                _rel("TREATED_BY", "Patient", "Provider", "Care delivery"),
                _rel("HAS_CLAIM", "Patient", "Claim", "Claim ownership"),
                _rel("BILLED_AT", "Claim", "Facility", "Facility billing"),
                _rel("FOR_DIAGNOSIS", "Claim", "Diagnosis", "Clinical justification"),
                _rel("FLAGGED_BY", "Claim", "AuditFinding", "Integrity finding"),
            ],
            "upload_guidance": {
                "structured": [
                    "Provider / network CSV",
                    "Referral and claims CSV",
                    "Facility and diagnosis CSV",
                ],
                "unstructured": [
                    "Referral letters",
                    "Network contracts",
                    "Audit reports",
                ],
                "why": "Referral integrity needs multi-hop provider and claim evidence.",
            },
        },
    },
    "Manufacturing & Supply Chain": {
        "Digital Twin": {
            "nodes": [
                _node("Product", "product_id", "sku, model, category, risk_flag"),
                _node("Assembly", "assembly_id", "name, parent_product, criticality"),
                _node("Component", "component_id", "part_number, material, spec_version"),
                _node("Supplier", "supplier_id", "country, tier, audit_score, single_source"),
                _node("Batch", "batch_id", "production_date, defect_rate, status"),
                _node("DefectRecord", "defect_id", "severity, root_cause, recall_required"),
                _node("Regulation", "reg_id", "standard, version, requirement"),
                _node("AuditFinding", "audit_id", "category, severity, corrective_action"),
            ],
            "relationships": [
                _rel("CONTAINS", "Assembly", "Component", "Bill of Materials containment"),
                _rel("SOURCED_FROM", "Component", "Supplier", "Single or multi-source supply"),
                _rel("PRODUCED_IN", "Batch", "Component", "Production batch traceability"),
                _rel("HAS_DEFECT", "Batch", "DefectRecord", "Defect record to batch"),
                _rel("PART_OF", "Component", "Assembly", "BOM hierarchy edge"),
                _rel("AFFECTS", "DefectRecord", "Component", "Defect propagation to component"),
            ],
            "upload_guidance": {
                "structured": [
                    "Product / assembly / component BOM CSV",
                    "Supplier master CSV",
                    "Batch and defect-rate CSV",
                    "Audit finding CSV",
                ],
                "unstructured": [
                    "Engineering drawings / specs (PDF)",
                    "Supplier audit reports",
                    "Quality / ISO standard documents",
                    "Recall or CAPA narratives",
                ],
                "why": "Digital-twin journeys need BOM structure plus supplier and quality evidence before graph construction.",
            },
        },
        "Supplier Risk Intelligence": {
            "nodes": [
                _node("Supplier", "supplier_id", "country, tier, score"),
                _node("Component", "component_id", "part_number, criticality"),
                _node("PurchaseOrder", "po_id", "amount, currency, due_date"),
                _node("Shipment", "shipment_id", "origin, eta, status"),
                _node("Contract", "contract_id", "term, renewal_date"),
                _node("RiskEvent", "event_id", "category, severity"),
                _node("Site", "site_id", "country, capacity"),
                _node("Regulation", "reg_id", "standard, region"),
            ],
            "relationships": [
                _rel("SUPPLIES", "Supplier", "Component", "Supply relationship"),
                _rel("FULFILLS", "Supplier", "PurchaseOrder", "PO fulfilment"),
                _rel("SHIPS", "PurchaseOrder", "Shipment", "Logistics linkage"),
                _rel("GOVERNED_BY", "Supplier", "Contract", "Commercial terms"),
                _rel("IMPACTED_BY", "Supplier", "RiskEvent", "Risk exposure"),
                _rel("OPERATES", "Supplier", "Site", "Manufacturing site"),
            ],
            "upload_guidance": {
                "structured": [
                    "Supplier master and tier CSV",
                    "PO / shipment CSV",
                    "Risk event and scorecard CSV",
                ],
                "unstructured": [
                    "Contracts and SLAs",
                    "Audit / ESG reports",
                    "News or incident summaries",
                ],
                "why": "Supplier risk graphs need commercial, logistics, and risk-event evidence.",
            },
        },
        "Quality & Recall Traceability": {
            "nodes": [
                _node("Product", "product_id", "sku, model"),
                _node("Batch", "batch_id", "lot_no, status"),
                _node("Component", "component_id", "part_number"),
                _node("DefectRecord", "defect_id", "severity, root_cause"),
                _node("CustomerShipment", "shipment_id", "destination, date"),
                _node("RecallAction", "recall_id", "scope, status"),
                _node("TestResult", "test_id", "metric, pass_fail"),
                _node("Supplier", "supplier_id", "name, country"),
            ],
            "relationships": [
                _rel("PRODUCED_IN", "Product", "Batch", "Batch of product"),
                _rel("CONTAINS", "Batch", "Component", "Component usage"),
                _rel("HAS_DEFECT", "Batch", "DefectRecord", "Quality defect"),
                _rel("SHIPPED_AS", "Batch", "CustomerShipment", "Distribution path"),
                _rel("TRIGGERS", "DefectRecord", "RecallAction", "Recall initiation"),
                _rel("TESTED_BY", "Batch", "TestResult", "QA measurement"),
            ],
            "upload_guidance": {
                "structured": [
                    "Batch / lot genealogy CSV",
                    "Defect and test-result CSV",
                    "Shipment destination CSV",
                ],
                "unstructured": [
                    "CAPA / recall notices",
                    "QA SOPs",
                    "Customer complaint letters",
                ],
                "why": "Recall readiness requires lot genealogy from supplier through customer shipment.",
            },
        },
        "Predictive Maintenance": {
            "nodes": [
                _node("Asset", "asset_id", "name, type, criticality"),
                _node("Sensor", "sensor_id", "metric, unit"),
                _node("WorkOrder", "wo_id", "status, priority"),
                _node("FailureEvent", "failure_id", "mode, downtime_hrs"),
                _node("Part", "part_id", "sku, lead_time"),
                _node("Technician", "tech_id", "skill, shift"),
                _node("Site", "site_id", "plant, line"),
                _node("Procedure", "proc_id", "version, title"),
            ],
            "relationships": [
                _rel("INSTALLED_AT", "Asset", "Site", "Asset location"),
                _rel("MONITORED_BY", "Asset", "Sensor", "Telemetry source"),
                _rel("HAS_FAILURE", "Asset", "FailureEvent", "Failure history"),
                _rel("REQUIRES", "WorkOrder", "Part", "Spare-part demand"),
                _rel("ASSIGNED_TO", "WorkOrder", "Technician", "Maintenance ownership"),
                _rel("GUIDED_BY", "WorkOrder", "Procedure", "Maintenance procedure"),
            ],
            "upload_guidance": {
                "structured": [
                    "Asset register CSV",
                    "Sensor / telemetry summary CSV",
                    "Work-order and failure CSV",
                ],
                "unstructured": [
                    "Maintenance procedures",
                    "Inspection reports",
                    "OEM manuals",
                ],
                "why": "Maintenance graphs connect assets, failures, parts, and procedures.",
            },
        },
    },
    "Telecommunications": {
        "Telecom Fraud": {
            "nodes": [
                _node("Subscriber", "subscriber_id", "msisdn, plan, status"),
                _node("Device", "device_id", "imei, model"),
                _node("SIM", "sim_id", "imsi, status"),
                _node("CallDetail", "cdr_id", "duration, destination, timestamp"),
                _node("Account", "account_id", "billing_id, risk_score"),
                _node("Location", "cell_id", "lac, region"),
                _node("FraudCase", "case_id", "typology, severity"),
                _node("Channel", "channel_id", "type, partner"),
            ],
            "relationships": [
                _rel("USES", "Subscriber", "Device", "Device association"),
                _rel("SUBSCRIBES_WITH", "Subscriber", "SIM", "SIM ownership"),
                _rel("GENERATED", "Subscriber", "CallDetail", "Usage event"),
                _rel("BILLED_TO", "Subscriber", "Account", "Billing link"),
                _rel("SEEN_AT", "Device", "Location", "Location presence"),
                _rel("FLAGGED_IN", "Subscriber", "FraudCase", "Fraud investigation"),
            ],
            "upload_guidance": {
                "structured": [
                    "Subscriber / SIM / device CSV",
                    "CDR / usage sample CSV",
                    "Fraud case and billing CSV",
                ],
                "unstructured": [
                    "Fraud typology playbooks",
                    "Call recordings / notes (if available)",
                    "Partner onboarding documents",
                ],
                "why": "Telecom fraud graphs need identity, device, usage, and case evidence.",
            },
        },
        "Fault Propagation": {
            "nodes": [
                _node("NetworkElement", "ne_id", "type, vendor, status"),
                _node("Service", "service_id", "name, sla_tier"),
                _node("Alarm", "alarm_id", "severity, raised_at"),
                _node("Region", "region_id", "name, customers_impacted"),
                _node("Ticket", "ticket_id", "priority, status"),
                _node("Dependency", "dep_id", "weight, criticality"),
                _node("CustomerImpact", "impact_id", "severity, count"),
                _node("ChangeEvent", "change_id", "window, owner"),
            ],
            "relationships": [
                _rel("DEPENDS_ON", "NetworkElement", "NetworkElement", "Infrastructure dependency"),
                _rel("SUPPORTS", "NetworkElement", "Service", "Service support"),
                _rel("RAISED", "NetworkElement", "Alarm", "Active alarm"),
                _rel("SERVES", "Service", "Region", "Service coverage"),
                _rel("CAUSES", "Alarm", "CustomerImpact", "Downstream impact"),
                _rel("TRACKED_BY", "Alarm", "Ticket", "Incident ticket"),
            ],
            "upload_guidance": {
                "structured": [
                    "Network topology / inventory CSV",
                    "Alarm and ticket CSV",
                    "Service-to-region mapping CSV",
                ],
                "unstructured": [
                    "NOC runbooks",
                    "Change records",
                    "Incident postmortems",
                ],
                "why": "Fault propagation needs topology dependencies plus active alarm evidence.",
            },
        },
        "Customer 360": {
            "nodes": [
                _node("Subscriber", "subscriber_id", "msisdn, segment"),
                _node("Account", "account_id", "plan, arpu"),
                _node("Device", "device_id", "imei, model"),
                _node("Interaction", "interaction_id", "channel, reason"),
                _node("Offer", "offer_id", "type, value"),
                _node("Complaint", "complaint_id", "category, status"),
                _node("UsageProfile", "usage_id", "voice, data, sms"),
                _node("Store", "store_id", "city, channel"),
            ],
            "relationships": [
                _rel("OWNS", "Subscriber", "Account", "Account ownership"),
                _rel("USES", "Subscriber", "Device", "Device usage"),
                _rel("HAS_INTERACTION", "Subscriber", "Interaction", "Support touchpoint"),
                _rel("OFFERED", "Subscriber", "Offer", "Marketing offer"),
                _rel("RAISED", "Subscriber", "Complaint", "Complaint"),
                _rel("SERVED_BY", "Subscriber", "Store", "Retail channel"),
            ],
            "upload_guidance": {
                "structured": [
                    "Subscriber / account CSV",
                    "Usage profile CSV",
                    "CRM interaction and complaint CSV",
                ],
                "unstructured": [
                    "Call-center transcripts",
                    "Offer catalogues",
                    "Store SOP documents",
                ],
                "why": "Telecom Customer 360 joins billing, usage, and service interactions.",
            },
        },
        "Churn Prediction": {
            "nodes": [
                _node("Subscriber", "subscriber_id", "tenure, plan"),
                _node("UsageDrop", "drop_id", "metric, pct_change"),
                _node("Complaint", "complaint_id", "category, severity"),
                _node("CompetitorOffer", "offer_id", "operator, value"),
                _node("PaymentDelay", "delay_id", "days_late, amount"),
                _node("ChurnSignal", "signal_id", "score, horizon"),
                _node("RetentionAction", "action_id", "type, status"),
                _node("Channel", "channel_id", "name"),
            ],
            "relationships": [
                _rel("SHOWS", "Subscriber", "UsageDrop", "Usage decline"),
                _rel("RAISED", "Subscriber", "Complaint", "Service friction"),
                _rel("EXPOSED_TO", "Subscriber", "CompetitorOffer", "Competitive pressure"),
                _rel("HAS_DELAY", "Subscriber", "PaymentDelay", "Payment stress"),
                _rel("PREDICTED_BY", "Subscriber", "ChurnSignal", "Modelled churn risk"),
                _rel("TARGETED_BY", "Subscriber", "RetentionAction", "Retention response"),
            ],
            "upload_guidance": {
                "structured": [
                    "Subscriber tenure / plan CSV",
                    "Usage trend and payment CSV",
                    "Complaint and retention-action CSV",
                ],
                "unstructured": [
                    "Win-back scripts",
                    "Competitor offer screenshots / PDFs",
                    "Customer feedback notes",
                ],
                "why": "Churn paths combine behavioural signals with retention actions.",
            },
        },
    },
    "Retail & E-Commerce": {
        "Product Knowledge Graph": {
            "nodes": [
                _node("Product", "product_id", "sku, title, brand"),
                _node("Category", "category_id", "name, level"),
                _node("Attribute", "attr_id", "name, value"),
                _node("ContentAsset", "asset_id", "type, url"),
                _node("Supplier", "supplier_id", "name, country"),
                _node("Bundle", "bundle_id", "name, price"),
                _node("Review", "review_id", "rating, sentiment"),
                _node("Warehouse", "wh_id", "region, capacity"),
            ],
            "relationships": [
                _rel("IN_CATEGORY", "Product", "Category", "Taxonomy placement"),
                _rel("HAS_ATTRIBUTE", "Product", "Attribute", "Product attribute"),
                _rel("HAS_CONTENT", "Product", "ContentAsset", "Rich content"),
                _rel("SUPPLIED_BY", "Product", "Supplier", "Source of supply"),
                _rel("PART_OF", "Product", "Bundle", "Bundle membership"),
                _rel("REVIEWED_IN", "Product", "Review", "Customer review"),
            ],
            "upload_guidance": {
                "structured": [
                    "Product catalog CSV",
                    "Category / attribute CSV",
                    "Supplier and inventory CSV",
                ],
                "unstructured": [
                    "Product descriptions / PDFs",
                    "Images and content assets",
                    "Review exports or feedback docs",
                ],
                "why": "Product KG needs catalog structure plus content and supplier context.",
            },
        },
        "Personalized Recommendation": {
            "nodes": [
                _node("Customer", "customer_id", "segment, loyalty_tier"),
                _node("Product", "product_id", "sku, category"),
                _node("Session", "session_id", "channel, started_at"),
                _node("Order", "order_id", "amount, status"),
                _node("Affinity", "affinity_id", "score, reason"),
                _node("Campaign", "campaign_id", "channel, offer"),
                _node("Wishlist", "wishlist_id", "name"),
                _node("Store", "store_id", "region"),
            ],
            "relationships": [
                _rel("VIEWED", "Customer", "Product", "Browse signal"),
                _rel("PURCHASED", "Customer", "Product", "Purchase signal"),
                _rel("HAS_SESSION", "Customer", "Session", "Engagement session"),
                _rel("PLACED", "Customer", "Order", "Order history"),
                _rel("AFFINE_TO", "Product", "Product", "Product affinity"),
                _rel("TARGETED_BY", "Customer", "Campaign", "Campaign reach"),
            ],
            "upload_guidance": {
                "structured": [
                    "Customer / order CSV",
                    "Browse / clickstream sample CSV",
                    "Campaign response CSV",
                ],
                "unstructured": [
                    "Campaign creatives",
                    "Product content pages",
                    "Customer feedback notes",
                ],
                "why": "Recommendations need behavioural and product-affinity evidence.",
            },
        },
        "Customer 360": {
            "nodes": [
                _node("Customer", "customer_id", "name, segment"),
                _node("Order", "order_id", "amount, status"),
                _node("Product", "product_id", "sku, category"),
                _node("Return", "return_id", "reason, status"),
                _node("Interaction", "interaction_id", "channel, topic"),
                _node("Loyalty", "loyalty_id", "tier, points"),
                _node("Address", "address_id", "city, region"),
                _node("PaymentMethod", "pay_id", "type, status"),
            ],
            "relationships": [
                _rel("PLACED", "Customer", "Order", "Order ownership"),
                _rel("CONTAINS", "Order", "Product", "Order lines"),
                _rel("RETURNED", "Order", "Return", "Return event"),
                _rel("HAS_INTERACTION", "Customer", "Interaction", "Service touchpoint"),
                _rel("ENROLLED_IN", "Customer", "Loyalty", "Loyalty membership"),
                _rel("SHIPS_TO", "Order", "Address", "Fulfilment address"),
            ],
            "upload_guidance": {
                "structured": [
                    "Customer master CSV",
                    "Orders / returns CSV",
                    "Loyalty and interaction CSV",
                ],
                "unstructured": [
                    "Support tickets / chat logs",
                    "Loyalty program terms",
                    "Return policy documents",
                ],
                "why": "Retail Customer 360 joins commerce events with service and loyalty context.",
            },
        },
        "Inventory & Demand Intelligence": {
            "nodes": [
                _node("Product", "product_id", "sku, category"),
                _node("Warehouse", "wh_id", "region, capacity"),
                _node("InventoryLevel", "inv_id", "on_hand, safety_stock"),
                _node("DemandSignal", "demand_id", "horizon, forecast"),
                _node("Supplier", "supplier_id", "lead_time, reliability"),
                _node("PurchaseOrder", "po_id", "qty, eta"),
                _node("Store", "store_id", "region"),
                _node("Promotion", "promo_id", "type, lift"),
            ],
            "relationships": [
                _rel("STOCKED_AT", "Product", "Warehouse", "Inventory location"),
                _rel("HAS_LEVEL", "Product", "InventoryLevel", "Stock position"),
                _rel("FORECAST_FOR", "DemandSignal", "Product", "Demand forecast"),
                _rel("SUPPLIED_BY", "Product", "Supplier", "Replenishment source"),
                _rel("REPLENISHED_BY", "Warehouse", "PurchaseOrder", "Inbound replenishment"),
                _rel("PROMOTED_BY", "Product", "Promotion", "Demand driver"),
            ],
            "upload_guidance": {
                "structured": [
                    "Inventory snapshot CSV",
                    "Demand forecast CSV",
                    "PO / supplier lead-time CSV",
                ],
                "unstructured": [
                    "Promotion calendars",
                    "Supplier SLAs",
                    "Store allocation notes",
                ],
                "why": "Inventory intelligence needs stock, demand, and replenishment evidence together.",
            },
        },
    },
}


class SchemaRegistryRequest(BaseModel):
    industry: str = ""
    use_case: str = ""
    objective: str = ""
    primary_entities: list[str] = []
    key_relationships: list[str] = []
    structured_focus: str = ""
    unstructured_focus: str = ""
    skip_llm: bool = False


# Domain-specific feature blueprints used when Domain Configurator entities
# do not exactly match a SCHEMA_LIBRARY entry.
_ENTITY_FEATURE_CATALOG: dict[str, list[tuple[str, str, str]]] = {
    "drugcandidate": [
        ("name", "String", "Attribute"),
        ("modality", "String", "Attribute"),
        ("development_stage", "String", "Status"),
        ("mechanism_of_action", "String", "Attribute"),
    ],
    "moleculartarget": [
        ("gene_symbol", "String", "Identifier"),
        ("protein_family", "String", "Attribute"),
        ("organism", "String", "Attribute"),
        ("druggability_score", "Float", "Metric"),
    ],
    "compound": [
        ("smiles", "String", "Identifier"),
        ("molecular_weight", "Float", "Metric"),
        ("logp", "Float", "Metric"),
        ("formula", "String", "Attribute"),
    ],
    "assay": [
        ("assay_type", "String", "Attribute"),
        ("readout", "String", "Attribute"),
        ("threshold", "Float", "Metric"),
        ("result_value", "Float", "Metric"),
    ],
    "indication": [
        ("disease_area", "String", "Attribute"),
        ("icd_code", "String", "Identifier"),
        ("prevalence", "Float", "Metric"),
        ("status", "String", "Status"),
    ],
    "medicinalproduct": [
        ("inn_name", "String", "Attribute"),
        ("dosage_form", "String", "Attribute"),
        ("strength", "String", "Attribute"),
        ("atc_code", "String", "Identifier"),
    ],
    "product": [
        ("name", "String", "Attribute"),
        ("form", "String", "Attribute"),
        ("strength", "String", "Attribute"),
        ("status", "String", "Status"),
    ],
    "adverseevent": [
        ("meddra_pt", "String", "Identifier"),
        ("severity", "String", "Attribute"),
        ("outcome", "String", "Attribute"),
        ("onset_date", "Date", "Temporal"),
    ],
    "patient": [
        ("age_band", "String", "Attribute"),
        ("sex", "String", "Attribute"),
        ("risk_flag", "Boolean", "Flag"),
        ("source_system", "String", "Provenance"),
    ],
    "safetyreport": [
        ("report_number", "String", "Identifier"),
        ("receipt_date", "Date", "Temporal"),
        ("reporter_type", "String", "Attribute"),
        ("seriousness", "String", "Attribute"),
    ],
    "label": [
        ("section", "String", "Attribute"),
        ("version", "String", "Attribute"),
        ("effective_date", "Date", "Temporal"),
        ("language", "String", "Attribute"),
    ],
    "study": [
        ("phase", "String", "Attribute"),
        ("design", "String", "Attribute"),
        ("status", "String", "Status"),
        ("indication", "String", "Attribute"),
    ],
    "clinicaltrial": [
        ("nct_id", "String", "Identifier"),
        ("phase", "String", "Attribute"),
        ("status", "String", "Status"),
        ("sponsor", "String", "Attribute"),
    ],
    "site": [
        ("country", "String", "Attribute"),
        ("investigator", "String", "Attribute"),
        ("capacity", "Integer", "Metric"),
        ("status", "String", "Status"),
    ],
    "subject": [
        ("arm", "String", "Attribute"),
        ("enrollment_date", "Date", "Temporal"),
        ("status", "String", "Status"),
    ],
    "participant": [
        ("arm", "String", "Attribute"),
        ("enrollment_date", "Date", "Temporal"),
        ("status", "String", "Status"),
    ],
    "protocol": [
        ("version", "String", "Attribute"),
        ("amendment", "String", "Attribute"),
        ("status", "String", "Status"),
    ],
    "provider": [
        ("specialty", "String", "Attribute"),
        ("npi", "String", "Identifier"),
        ("facility", "String", "Attribute"),
    ],
    "encounter": [
        ("encounter_date", "Date", "Temporal"),
        ("encounter_type", "String", "Attribute"),
        ("disposition", "String", "Attribute"),
    ],
    "claim": [
        ("amount", "Float", "Metric"),
        ("status", "String", "Status"),
        ("diagnosis_code", "String", "Identifier"),
    ],
    "customer": [
        ("segment", "String", "Attribute"),
        ("risk_score", "Float", "Metric"),
        ("kyc_status", "String", "Status"),
        ("source_system", "String", "Provenance"),
    ],
    "account": [
        ("account_type", "String", "Attribute"),
        ("opened_date", "Date", "Temporal"),
        ("balance", "Float", "Metric"),
        ("status", "String", "Status"),
    ],
    "transaction": [
        ("amount", "Float", "Metric"),
        ("currency", "String", "Attribute"),
        ("txn_timestamp", "DateTime", "Temporal"),
        ("channel", "String", "Attribute"),
    ],
    "supplier": [
        ("region", "String", "Attribute"),
        ("tier", "String", "Attribute"),
        ("risk_rating", "String", "Attribute"),
        ("status", "String", "Status"),
    ],
    "asset": [
        ("asset_class", "String", "Attribute"),
        ("criticality", "String", "Attribute"),
        ("status", "String", "Status"),
        ("location", "String", "Attribute"),
    ],
}

_REL_DESCRIPTION_HINTS: dict[str, str] = {
    "BINDS_TO": "Binding or affinity evidence between compound and molecular target",
    "MODULATES": "Intended pharmacological action on the target",
    "TESTED_IN": "Assay or experimental evaluation linkage",
    "INDICATED_FOR": "Therapeutic hypothesis for a disease indication",
    "SUPPORTED_BY": "Evidence or study support for the upstream entity",
    "EXPERIENCED": "Product associated with a reported adverse event",
    "SUSPECTS": "Adverse event observed or suspected in a patient",
    "DOCUMENTED_IN": "Patient case captured in a safety report",
    "DESCRIBED_BY": "Safety narrative described by label or SmPC content",
    "ASSOCIATED_WITH": "Observed association between the connected entities",
    "ENROLLED_IN": "Subject or participant enrollment into a study",
    "REPORTED": "Safety or clinical event reporting path",
    "TREATED_BY": "Care delivery relationship",
    "HAS_ENCOUNTER": "Clinical visit ownership",
    "OWNS": "Ownership or control relationship",
    "TRANSFERRED_TO": "Value or fund movement between parties",
    "RELATED_TO": "General domain association between entities",
}


def _clean(value: Any, limit: int = 500) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def _tokens(value: str) -> set[str]:
    stop = {"and", "the", "for", "with", "from", "into", "of", "a", "an", "to"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", (value or "").lower())
        if token not in stop and len(token) > 1
    }


def _snake_label(label: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", label).lower()


def _normalize_label(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", _clean(value, 50))


def _default_for_industry(industry: str) -> tuple[str, dict]:
    industry_map = SCHEMA_LIBRARY.get(industry) or SCHEMA_LIBRARY["Financial Services"]
    first_use_case = next(iter(industry_map))
    return first_use_case, industry_map[first_use_case]


def _features_for_label(label: str) -> list[dict]:
    key = label.lower()
    primary_key = f"{_snake_label(label)}_id"
    catalog = list(_ENTITY_FEATURE_CATALOG.get(key) or [])
    if not catalog:
        # Keyword fallback so custom Domain Configurator labels stay specific.
        lowered = key
        if any(token in lowered for token in ("patient", "subject", "participant", "customer")):
            catalog = [
                ("age_band", "String", "Attribute"),
                ("status", "String", "Status"),
                ("source_system", "String", "Provenance"),
            ]
        elif any(token in lowered for token in ("product", "drug", "compound", "medication", "candidate")):
            catalog = [
                ("name", "String", "Attribute"),
                ("form", "String", "Attribute"),
                ("strength", "String", "Attribute"),
                ("status", "String", "Status"),
            ]
        elif any(token in lowered for token in ("event", "alarm", "incident", "defect")):
            catalog = [
                ("severity", "String", "Attribute"),
                ("outcome", "String", "Attribute"),
                ("reported_at", "DateTime", "Temporal"),
                ("status", "String", "Status"),
            ]
        elif any(token in lowered for token in ("report", "document", "label", "protocol", "claim")):
            catalog = [
                ("title", "String", "Attribute"),
                ("version", "String", "Attribute"),
                ("effective_date", "Date", "Temporal"),
                ("status", "String", "Status"),
            ]
        elif any(token in lowered for token in ("study", "trial", "assay", "experiment")):
            catalog = [
                ("phase", "String", "Attribute"),
                ("design", "String", "Attribute"),
                ("status", "String", "Status"),
                ("start_date", "Date", "Temporal"),
            ]
        elif any(token in lowered for token in ("target", "protein", "gene")):
            catalog = [
                ("gene_symbol", "String", "Identifier"),
                ("organism", "String", "Attribute"),
                ("family", "String", "Attribute"),
                ("status", "String", "Status"),
            ]
        else:
            catalog = [
                ("name", "String", "Attribute"),
                ("category", "String", "Attribute"),
                ("status", "String", "Status"),
                ("source_system", "String", "Provenance"),
            ]

    features = [{
        "name": primary_key,
        "data_type": "String",
        "feature_type": "Primary Key",
        "is_primary_key": True,
    }]
    for name, data_type, feature_type in catalog:
        if name == primary_key:
            continue
        features.append({
            "name": name,
            "data_type": data_type,
            "feature_type": feature_type,
            "is_primary_key": False,
        })
    return features


def _node_from_label(label: str, library_nodes: list[dict] | None = None) -> dict:
    for item in library_nodes or []:
        if str(item.get("label") or "").lower() == label.lower():
            props = _clean(item.get("key_properties"), 200)
            features = _features_for_label(label)
            # Prefer library property names when present.
            lib_names = [part.strip() for part in props.split(",") if part.strip()]
            if lib_names:
                features = [{
                    "name": str(item.get("primary_key") or features[0]["name"]),
                    "data_type": "String",
                    "feature_type": "Primary Key",
                    "is_primary_key": True,
                }]
                for name in lib_names:
                    features.append({
                        "name": name,
                        "data_type": "String",
                        "feature_type": "Attribute",
                        "is_primary_key": False,
                    })
            return {
                "label": label,
                "primary_key": item.get("primary_key") or features[0]["name"],
                "key_properties": ", ".join(
                    feature["name"] for feature in features if not feature["is_primary_key"]
                ),
                "features": features,
            }
    features = _features_for_label(label)
    return {
        "label": label,
        "primary_key": features[0]["name"],
        "key_properties": ", ".join(
            feature["name"] for feature in features if not feature["is_primary_key"]
        ),
        "features": features,
    }


def _describe_relationship(rel_type: str, from_label: str, to_label: str) -> str:
    hint = _REL_DESCRIPTION_HINTS.get(rel_type)
    if hint:
        return hint
    readable = rel_type.replace("_", " ").lower()
    return f"{from_label} {readable} {to_label}"


def _parse_relationship_phrase(
    value: str, labels: list[str]
) -> tuple[str, str | None, str | None]:
    """Extract REL_TYPE and optional from/to labels from Domain Configurator phrases."""
    cleaned = _clean(value, 120)
    arrow = re.search(
        r"([A-Za-z][A-Za-z0-9]*)\s*[-–>]+\s*([A-Z0-9_]+)\s*[-–>]+\s*([A-Za-z][A-Za-z0-9]*)",
        cleaned,
    )
    if arrow:
        return (
            re.sub(r"[^A-Za-z0-9_]", "_", arrow.group(2)).upper().strip("_"),
            _normalize_label(arrow.group(1)) or None,
            _normalize_label(arrow.group(3)) or None,
        )

    upper = cleaned.upper()
    token_match = re.search(r"\b([A-Z][A-Z0-9_]{2,})\b", upper)
    rel_type = (
        re.sub(r"[^A-Za-z0-9_]", "_", token_match.group(1)).strip("_")
        if token_match
        else re.sub(r"[^A-Za-z0-9_]", "_", cleaned).upper().strip("_")
    )
    from_label = to_label = None
    label_map = {item.lower(): item for item in labels}
    for item in labels:
        if item.lower() in cleaned.lower().replace(" ", ""):
            if not from_label:
                from_label = item
            elif item != from_label and not to_label:
                to_label = item
    # Prefer exact CamelCase mentions.
    for raw in re.findall(r"\b[A-Z][A-Za-z0-9]+\b", cleaned):
        normalized = _normalize_label(raw)
        if normalized.lower() in label_map:
            resolved = label_map[normalized.lower()]
            if not from_label:
                from_label = resolved
            elif resolved != from_label and not to_label:
                to_label = resolved
    return rel_type or "RELATED_TO", from_label, to_label


def _schema_from_preview(
    primary_entities: list[str],
    key_relationships: list[str],
    library_schema: dict | None = None,
) -> dict | None:
    labels = []
    for value in primary_entities[:8]:
        label = _normalize_label(value)
        if label and label not in labels:
            labels.append(label)
    if len(labels) < 2:
        return None

    library_nodes = list((library_schema or {}).get("nodes") or [])
    library_rels = {
        str(item.get("type") or "").upper(): item
        for item in (library_schema or {}).get("relationships") or []
        if item.get("type")
    }
    nodes = [_node_from_label(label, library_nodes) for label in labels]

    relationships = []
    seen = set()
    for index, value in enumerate(key_relationships[:8]):
        rel_type, from_hint, to_hint = _parse_relationship_phrase(value, labels)
        if not rel_type or rel_type in seen:
            continue
        seen.add(rel_type)
        library_rel = library_rels.get(rel_type)
        from_label = from_hint or (library_rel or {}).get("from") or labels[index % len(labels)]
        to_label = (
            to_hint
            or (library_rel or {}).get("to")
            or labels[(index + 1) % len(labels)]
        )
        if from_label not in labels:
            from_label = labels[index % len(labels)]
        if to_label not in labels or to_label == from_label:
            to_label = labels[(labels.index(from_label) + 1) % len(labels)]
        description = _clean(
            (library_rel or {}).get("description")
            or _describe_relationship(rel_type, from_label, to_label),
            180,
        )
        relationships.append(_rel(rel_type, from_label, to_label, description))

    if not relationships:
        relationships = [
            _rel(
                "RELATED_TO",
                labels[0],
                labels[1],
                _describe_relationship("RELATED_TO", labels[0], labels[1]),
            )
        ]

    result = {"nodes": nodes, "relationships": relationships}
    guidance = (library_schema or {}).get("upload_guidance")
    if guidance:
        result["upload_guidance"] = guidance
    return result


def _best_library_match(use_case: str, industry_map: dict[str, dict]) -> str | None:
    use_lower = (use_case or "").strip().lower()
    if not use_lower:
        return None
    exact = next((key for key in industry_map if key.lower() == use_lower), None)
    if exact:
        return exact
    substring = next(
        (key for key in industry_map if use_lower in key.lower() or key.lower() in use_lower),
        None,
    )
    if substring:
        return substring

    use_tokens = _tokens(use_case)
    best_key = None
    best_score = 0.0
    for key in industry_map:
        key_tokens = _tokens(key)
        if not key_tokens or not use_tokens:
            continue
        overlap = len(use_tokens & key_tokens)
        if overlap <= 0:
            continue
        score = overlap + (0.25 if overlap == len(use_tokens) else 0)
        if score > best_score:
            best_score = score
            best_key = key
    return best_key if best_score >= 1 else None


def _resolve_schema(
    industry: str,
    use_case: str,
    primary_entities: list[str] | None = None,
    key_relationships: list[str] | None = None,
) -> tuple[str, str, dict, str]:
    """Return industry, use_case, schema, and resolution source."""
    requested_use_case = (use_case or "").strip() or "Custom Use Case"
    if industry not in SCHEMA_LIBRARY:
        industry = "Financial Services"
    industry_map = SCHEMA_LIBRARY[industry]
    match = requested_use_case if requested_use_case in industry_map else _best_library_match(
        requested_use_case, industry_map
    )
    library_schema = industry_map.get(match) if match else None

    synthesized = _schema_from_preview(
        primary_entities or [],
        key_relationships or [],
        library_schema,
    )
    if synthesized:
        if library_schema and not synthesized.get("upload_guidance"):
            guidance = library_schema.get("upload_guidance")
            if guidance:
                synthesized["upload_guidance"] = guidance
        source = "domain_preview" if not match else "domain_preview+library"
        return industry, requested_use_case, synthesized, source

    if library_schema:
        enriched_nodes = [
            _node_from_label(str(node.get("label") or ""), [node])
            for node in library_schema.get("nodes") or []
            if node.get("label")
        ]
        schema = {
            "nodes": enriched_nodes or list(library_schema.get("nodes") or []),
            "relationships": list(library_schema.get("relationships") or []),
        }
        if library_schema.get("upload_guidance"):
            schema["upload_guidance"] = library_schema["upload_guidance"]
        return industry, match or requested_use_case, schema, "schema_library"

    fallback, schema = _default_for_industry(industry)
    return industry, requested_use_case or fallback, schema, "industry_default"


def _build_cypher(nodes: list[dict], relationships: list[dict]) -> str:
    lines = ["// Illustrative Neo4j pattern — reference only"]
    for node in nodes[:5]:
        label = node["label"]
        key = node["primary_key"]
        lines.append(f"CREATE CONSTRAINT ON (n:{label}) ASSERT n.{key} IS UNIQUE;")
    lines.append("")
    lines.append("// Performance indexes for high-traversal relationships")
    for rel in relationships[:4]:
        lines.append(f"CREATE INDEX FOR ()-[r:{rel['type']}]-() ON (r.weight);")
    return "\n".join(lines)


def _reference_dimensions(
    nodes: list[dict], relationships: list[dict], objective: str
) -> list[dict]:
    primary_keys = [node["primary_key"] for node in nodes[:5]]
    properties = [
        part.strip()
        for node in nodes[:4]
        for part in str(node.get("key_properties") or "").split(",")
        if part.strip()
    ]
    relationship_types = [rel["type"] for rel in relationships[:5]]
    return [
        {
            "name": "Entity identity",
            "purpose": "Distinguish and resolve the principal business entities.",
            "example_attributes": ", ".join(primary_keys),
        },
        {
            "name": "Business context",
            "purpose": "Describe the attributes used to interpret each entity.",
            "example_attributes": ", ".join(properties[:6]),
        },
        {
            "name": "Relationship context",
            "purpose": "Express how entities connect for graph traversal.",
            "example_attributes": ", ".join(relationship_types),
        },
        {
            "name": "Time and lifecycle",
            "purpose": "Place records and relationships in an event or status sequence.",
            "example_attributes": "timestamp, effective_date, status, version",
        },
        {
            "name": "Decision outcome",
            "purpose": _clean(objective, 220),
            "example_attributes": "score, severity, confidence, review_status",
        },
    ]


def _reference_tables(nodes: list[dict]) -> list[dict]:
    tables = []
    for node in nodes[:8]:
        label = str(node["label"])
        table_name = _snake_label(label) + "_reference"
        tables.append({
            "table": table_name,
            "grain": f"One illustrative row per {label}",
            "primary_key": node["primary_key"],
            "example_columns": node.get("key_properties") or "",
        })
    return tables


def _default_upload_guidance(
    industry: str,
    use_case: str,
    structured_focus: str,
    unstructured_focus: str,
) -> dict:
    structured = [
        item.strip()
        for item in re.split(r"[;\n|]", structured_focus or "")
        if item.strip()
    ][:4]
    unstructured = [
        item.strip()
        for item in re.split(r"[;\n|]", unstructured_focus or "")
        if item.strip()
    ][:4]
    if not structured:
        structured = [
            f"{use_case} entity master CSV",
            f"{use_case} event / transaction CSV",
            "Reference dimension tables",
        ]
    if not unstructured:
        unstructured = [
            "Policy / protocol documents",
            "Narrative reports and notes",
            "Supporting PDF or image evidence",
        ]
    return {
        "structured": structured,
        "unstructured": unstructured,
        "why": (
            f"Upload structured masters and unstructured evidence that can connect "
            f"{industry} · {use_case} entities into a traversable graph."
        ),
    }


def _input_catalog(
    nodes: list[dict],
    upload_guidance: dict,
    structured_focus: str,
    unstructured_focus: str,
) -> list[dict]:
    rows: list[dict] = []
    for node in nodes[:8]:
        label = str(node["label"])
        table = _snake_label(label) + "_reference"
        features = list(node.get("features") or [])
        if not features:
            features = _features_for_label(label)
            # Keep PK + properties only when features were absent on the node.
            pk = node.get("primary_key") or features[0]["name"]
            props = [
                part.strip()
                for part in str(node.get("key_properties") or "").split(",")
                if part.strip()
            ]
            features = [{
                "name": pk,
                "data_type": "String",
                "feature_type": "Primary Key",
                "is_primary_key": True,
            }] + [
                {
                    "name": prop,
                    "data_type": "String",
                    "feature_type": "Attribute",
                    "is_primary_key": False,
                }
                for prop in props
            ]
        for feature in features[:6]:
            rows.append({
                "table": table,
                "entity": label,
                "feature": feature["name"],
                "data_type": feature.get("data_type") or "String",
                "feature_type": feature.get("feature_type") or "Attribute",
                "modality": "Structured",
                "is_primary_key": bool(feature.get("is_primary_key")),
            })

    unstructured_sources = list(upload_guidance.get("unstructured") or [])
    if unstructured_focus and unstructured_focus not in unstructured_sources:
        unstructured_sources = [unstructured_focus] + unstructured_sources
    for index, source in enumerate(unstructured_sources[:4]):
        rows.append({
            "table": "unstructured_evidence",
            "entity": "EvidenceDocument",
            "feature": _clean(source, 80) or f"evidence_source_{index + 1}",
            "data_type": "Text/Document",
            "feature_type": "Unstructured Source",
            "modality": "Unstructured",
            "is_primary_key": False,
        })

    if structured_focus:
        rows.insert(0, {
            "table": "intake_summary",
            "entity": "DomainIntake",
            "feature": _clean(structured_focus, 120),
            "data_type": "Text",
            "feature_type": "Structured Focus",
            "modality": "Structured",
            "is_primary_key": False,
        })
    return rows


def build_schema_registry(req: SchemaRegistryRequest) -> dict:
    industry, use_case, schema, source = _resolve_schema(
        req.industry,
        req.use_case,
        req.primary_entities,
        req.key_relationships,
    )
    nodes = list(schema["nodes"])
    # Ensure every node carries feature metadata for the input catalog.
    enriched_nodes = []
    for node in nodes:
        label = str(node.get("label") or "")
        if not label:
            continue
        if node.get("features"):
            enriched_nodes.append(node)
        else:
            enriched_nodes.append(_node_from_label(label, [node]))
    nodes = enriched_nodes or nodes
    relationships = list(schema["relationships"])
    objective = _clean(req.objective) or f"Explore a knowledge graph for {use_case}."
    dimensions = _reference_dimensions(nodes, relationships, objective)
    reference_tables = _reference_tables(nodes)
    upload_guidance = dict(schema.get("upload_guidance") or {})
    if not upload_guidance:
        upload_guidance = _default_upload_guidance(
            industry,
            use_case,
            req.structured_focus,
            req.unstructured_focus,
        )
    input_catalog = _input_catalog(
        nodes,
        upload_guidance,
        req.structured_focus,
        req.unstructured_focus,
    )
    return {
        "source": source,
        "phase_label": "Step 2 of 11 · Schema Registry",
        "industry": industry,
        "use_case": use_case,
        "title": "Schema Registry — Entity & Relationship Types",
        "subtitle": (
            f"Illustrative knowledge-graph blueprint for {industry} · {use_case}, synthesized "
            "from the preceding Domain Configurator selection."
        ),
        "intro": (
            "This reference page shows the entities, features, data types, and relationships "
            "implied by your Domain Configurator selection. Use it as an input-data checklist "
            "before upload — examples are conceptual and non-binding."
        ),
        "reference_note": (
            "Reference example only — feature names, data types, and modalities are synthesized "
            "from Domain Configurator entities and closest industry patterns, not ingestion contracts."
        ),
        "objective": objective,
        "structured_focus": _clean(req.structured_focus, 240),
        "unstructured_focus": _clean(req.unstructured_focus, 240),
        "upload_guidance": upload_guidance,
        "input_catalog": input_catalog,
        "node_types": nodes,
        "relationship_types": relationships,
        "dimensions": dimensions,
        "reference_tables": reference_tables,
        "node_count": len(nodes),
        "relationship_count": len(relationships),
        "dimension_count": len(dimensions),
        "table_count": len(reference_tables),
        "feature_count": len(input_catalog),
        "cypher_preview": _build_cypher(nodes, relationships),
    }


def enrich_schema_registry_with_llm(payload: dict, req: SchemaRegistryRequest) -> dict:
    system = (
        "You are a knowledge-graph schema editor. Return STRICT JSON only. Keep the selected "
        "industry and use case authoritative. Refine node_types and relationship_types so each "
        "entity has DISTINCT, domain-specific key_properties — never reuse the same property "
        "list across all nodes. Relationship descriptions must be specific to the from/to pair. "
        "Also return input_catalog rows describing table, entity, feature, data_type, "
        "feature_type, modality (Structured or Unstructured), and is_primary_key. "
        "Return keys: subtitle, intro, reference_note, node_types, relationship_types, "
        "dimensions, reference_tables, input_catalog, upload_guidance. "
        "node_types items: label, primary_key, key_properties. "
        "relationship_types items: type, from, to, description. "
        "dimensions items: name, purpose, example_attributes. "
        "reference_tables items: table, grain, primary_key, example_columns. "
        "upload_guidance: structured (array), unstructured (array), why (string). "
        "Provide 5..8 nodes, 4..7 relationships, 4..6 dimensions, 4..8 tables, and "
        "12..40 input_catalog features. Keep node labels CamelCase without spaces."
    )
    user = json.dumps({
        "industry": payload["industry"],
        "use_case": payload["use_case"],
        "objective": req.objective,
        "structured_focus": req.structured_focus,
        "unstructured_focus": req.unstructured_focus,
        "primary_entities": req.primary_entities,
        "key_relationships": req.key_relationships,
        "baseline": {
            "node_types": payload["node_types"],
            "relationship_types": payload["relationship_types"],
            "dimensions": payload["dimensions"],
            "reference_tables": payload["reference_tables"],
            "input_catalog": payload.get("input_catalog") or [],
            "upload_guidance": payload.get("upload_guidance") or {},
        },
    }, ensure_ascii=False)
    try:
        from leaseguard.llm.llm_client import LLMClient

        parsed = LLMClient().extract_json(system, user)
        if not isinstance(parsed, dict):
            return payload

        nodes = []
        for item in parsed.get("node_types") or []:
            if not isinstance(item, dict) or not item.get("label"):
                continue
            label = re.sub(r"[^A-Za-z0-9_]", "", str(item["label"]))[:40]
            if not label:
                continue
            node = {
                "label": label,
                "primary_key": _clean(item.get("primary_key") or f"{_snake_label(label)}_id", 60),
                "key_properties": _clean(item.get("key_properties"), 160),
            }
            nodes.append(_node_from_label(label, [node]))
        if 4 <= len(nodes) <= 10:
            payload["node_types"] = nodes
            payload["node_count"] = len(nodes)

        rels = []
        for item in parsed.get("relationship_types") or []:
            if not isinstance(item, dict) or not item.get("type"):
                continue
            rel_type = re.sub(r"[^A-Za-z0-9_]", "", str(item["type"]).upper())[:40]
            if not rel_type:
                continue
            from_label = _clean(item.get("from"), 40)
            to_label = _clean(item.get("to"), 40)
            description = _clean(item.get("description"), 180) or _describe_relationship(
                rel_type, from_label, to_label
            )
            # Reject the old generic placeholder if the model still emits it.
            if description.lower().startswith("synthesized relationship"):
                description = _describe_relationship(rel_type, from_label, to_label)
            rels.append({
                "type": rel_type,
                "from": from_label,
                "to": to_label,
                "description": description,
            })
        if 3 <= len(rels) <= 10:
            payload["relationship_types"] = rels
            payload["relationship_count"] = len(rels)

        dimensions = []
        for item in parsed.get("dimensions") or []:
            if not isinstance(item, dict) or not item.get("name"):
                continue
            dimensions.append({
                "name": _clean(item.get("name"), 80),
                "purpose": _clean(item.get("purpose"), 240),
                "example_attributes": _clean(item.get("example_attributes"), 220),
            })
        if 3 <= len(dimensions) <= 8:
            payload["dimensions"] = dimensions
            payload["dimension_count"] = len(dimensions)

        reference_tables = []
        for item in parsed.get("reference_tables") or []:
            if not isinstance(item, dict) or not item.get("table"):
                continue
            reference_tables.append({
                "table": _clean(item.get("table"), 80),
                "grain": _clean(item.get("grain"), 180),
                "primary_key": _clean(item.get("primary_key"), 80),
                "example_columns": _clean(item.get("example_columns"), 220),
            })
        if 3 <= len(reference_tables) <= 10:
            payload["reference_tables"] = reference_tables
            payload["table_count"] = len(reference_tables)

        catalog = []
        for item in parsed.get("input_catalog") or []:
            if not isinstance(item, dict) or not item.get("feature"):
                continue
            catalog.append({
                "table": _clean(item.get("table"), 80) or "reference_table",
                "entity": _clean(item.get("entity"), 60) or "Entity",
                "feature": _clean(item.get("feature"), 80),
                "data_type": _clean(item.get("data_type"), 40) or "String",
                "feature_type": _clean(item.get("feature_type"), 40) or "Attribute",
                "modality": (
                    "Unstructured"
                    if "unstruct" in str(item.get("modality") or "").lower()
                    else "Structured"
                ),
                "is_primary_key": bool(item.get("is_primary_key")),
            })
        if 8 <= len(catalog) <= 60:
            payload["input_catalog"] = catalog
            payload["feature_count"] = len(catalog)
        else:
            payload["input_catalog"] = _input_catalog(
                payload["node_types"],
                payload.get("upload_guidance") or {},
                req.structured_focus,
                req.unstructured_focus,
            )
            payload["feature_count"] = len(payload["input_catalog"])

        guidance = parsed.get("upload_guidance")
        if isinstance(guidance, dict):
            structured = [
                _clean(item, 120)
                for item in (guidance.get("structured") or [])
                if _clean(item, 120)
            ][:6]
            unstructured = [
                _clean(item, 120)
                for item in (guidance.get("unstructured") or [])
                if _clean(item, 120)
            ][:6]
            if structured and unstructured:
                payload["upload_guidance"] = {
                    "structured": structured,
                    "unstructured": unstructured,
                    "why": _clean(guidance.get("why"), 240)
                    or (payload.get("upload_guidance") or {}).get("why", ""),
                }

        payload["subtitle"] = _clean(parsed.get("subtitle"), 500) or payload["subtitle"]
        payload["intro"] = _clean(parsed.get("intro"), 700) or payload["intro"]
        payload["reference_note"] = (
            _clean(parsed.get("reference_note"), 500) or payload["reference_note"]
        )
        payload["cypher_preview"] = _build_cypher(
            payload["node_types"], payload["relationship_types"]
        )
        payload["source"] = "llm"
    except Exception as exc:
        logger.warning(f"Schema registry LLM enrichment failed: {exc}")
    return payload
