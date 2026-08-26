"""EC login credentials - Robot Framework variable file, kept separate from environment.py
(owner request, 2026-08-17): a screen can retrieve its login credentials from here instead of the
general environment config. Same env-var-with-safe-fallback pattern as environment.py - only the
throwaway local-sandbox value is ever committed, real secrets are always injected via OS
environment variables (CI/CD).

STANDING DECISION (owner, 2026-08-22): every EC screen gets its OWN dedicated <SCREEN>_EC_USER/
<SCREEN>_EC_PASS pair here - real EC deployments gate different screens behind different role
access, so a screen-specific login identity is the correct default going forward, not an
exception. This supersedes docs/rf-suite-styles.md point 6 (shared environment.py default,
override only via an explicit Login argument) - that doc is being updated to match. Kept as ONE
shared file (not one file per screen, which would sprawl to 100+ tiny files as more screens are
built) - the per-screen distinction lives in the VARIABLE NAME, not the file.

Override precedence (highest first), same shape for every screen's pair:
  1. <SCREEN>_EC_USER / <SCREEN>_EC_PASS OS environment variable (screen-specific override)
  2. EC_USER / EC_PASS OS environment variable (shared fallback, same as environment.py)
  3. default below (local sandbox)

Future direction (owner-stated, 2026-08-17): migrate this file to a real secrets store
(vault/keyring/CI secret manager) once the RF EC suite is otherwise complete. This file is the
interim step - only its internals change when that happens, no consuming .resource file does.
"""
import os

BANK_EC_USER = os.environ.get("BANK_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BANK_EC_PASS = os.environ.get("BANK_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

OBJECT_LIST_EC_USER = os.environ.get("OBJECT_LIST_EC_USER", os.environ.get("EC_USER", "sysadmin"))
OBJECT_LIST_EC_PASS = os.environ.get("OBJECT_LIST_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

STATE_EC_USER = os.environ.get("STATE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STATE_EC_PASS = os.environ.get("STATE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

REGION_EC_USER = os.environ.get("REGION_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REGION_EC_PASS = os.environ.get("REGION_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

FUNCTIONAL_AREA_EC_USER = os.environ.get("FUNCTIONAL_AREA_EC_USER", os.environ.get("EC_USER", "sysadmin"))
FUNCTIONAL_AREA_EC_PASS = os.environ.get("FUNCTIONAL_AREA_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

BUSINESS_UNIT_EC_USER = os.environ.get("BUSINESS_UNIT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BUSINESS_UNIT_EC_PASS = os.environ.get("BUSINESS_UNIT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PRODUCTION_UNIT_EC_USER = os.environ.get("PRODUCTION_UNIT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCTION_UNIT_EC_PASS = os.environ.get("PRODUCTION_UNIT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

COMPANY_EC_USER = os.environ.get("COMPANY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
COMPANY_EC_PASS = os.environ.get("COMPANY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

COST_CENTRE_EC_USER = os.environ.get("COST_CENTRE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
COST_CENTRE_EC_PASS = os.environ.get("COST_CENTRE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

REVENUE_ORDER_EC_USER = os.environ.get("REVENUE_ORDER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REVENUE_ORDER_EC_PASS = os.environ.get("REVENUE_ORDER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

WBS_EC_USER = os.environ.get("WBS_EC_USER", os.environ.get("EC_USER", "sysadmin"))
WBS_EC_PASS = os.environ.get("WBS_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PAYMENT_SCHEME_EC_USER = os.environ.get("PAYMENT_SCHEME_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PAYMENT_SCHEME_EC_PASS = os.environ.get("PAYMENT_SCHEME_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

EXCHANGE_RATE_SOURCE_EC_USER = os.environ.get("EXCHANGE_RATE_SOURCE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
EXCHANGE_RATE_SOURCE_EC_PASS = os.environ.get("EXCHANGE_RATE_SOURCE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

ACCOUNT_EC_USER = os.environ.get("ACCOUNT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
ACCOUNT_EC_PASS = os.environ.get("ACCOUNT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

COUNTRY_EC_USER = os.environ.get("COUNTRY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
COUNTRY_EC_PASS = os.environ.get("COUNTRY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

COUNTY_EC_USER = os.environ.get("COUNTY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
COUNTY_EC_PASS = os.environ.get("COUNTY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

CURRENCY_EC_USER = os.environ.get("CURRENCY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CURRENCY_EC_PASS = os.environ.get("CURRENCY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

VAT_CODE_EC_USER = os.environ.get("VAT_CODE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
VAT_CODE_EC_PASS = os.environ.get("VAT_CODE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

REGULATORY_PERMITS_EC_USER = os.environ.get("REGULATORY_PERMITS_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REGULATORY_PERMITS_EC_PASS = os.environ.get("REGULATORY_PERMITS_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

FIELD_GROUP_EC_USER = os.environ.get("FIELD_GROUP_EC_USER", os.environ.get("EC_USER", "sysadmin"))
FIELD_GROUP_EC_PASS = os.environ.get("FIELD_GROUP_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

CUSTOMER_EC_USER = os.environ.get("CUSTOMER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CUSTOMER_EC_PASS = os.environ.get("CUSTOMER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

OPERATOR_LEASE_EC_USER = os.environ.get("OPERATOR_LEASE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
OPERATOR_LEASE_EC_PASS = os.environ.get("OPERATOR_LEASE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

MMS_LEASE_EC_USER = os.environ.get("MMS_LEASE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
MMS_LEASE_EC_PASS = os.environ.get("MMS_LEASE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

LICENCE_EC_USER = os.environ.get("LICENCE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
LICENCE_EC_PASS = os.environ.get("LICENCE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

VENDOR_EC_USER = os.environ.get("VENDOR_EC_USER", os.environ.get("EC_USER", "sysadmin"))
VENDOR_EC_PASS = os.environ.get("VENDOR_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

STATE_LEASE_EC_USER = os.environ.get("STATE_LEASE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STATE_LEASE_EC_PASS = os.environ.get("STATE_LEASE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PRODUCT_DESCRIPTION_EC_USER = os.environ.get("PRODUCT_DESCRIPTION_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCT_DESCRIPTION_EC_PASS = os.environ.get("PRODUCT_DESCRIPTION_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

COST_OBJECT_MAPPING_EC_USER = os.environ.get("COST_OBJECT_MAPPING_EC_USER", os.environ.get("EC_USER", "sysadmin"))
COST_OBJECT_MAPPING_EC_PASS = os.environ.get("COST_OBJECT_MAPPING_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

DOA_CREDIT_LIMIT_EC_USER = os.environ.get("DOA_CREDIT_LIMIT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DOA_CREDIT_LIMIT_EC_PASS = os.environ.get("DOA_CREDIT_LIMIT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

SALES_ORDER_EC_USER = os.environ.get("SALES_ORDER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
SALES_ORDER_EC_PASS = os.environ.get("SALES_ORDER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PRODUCT_GROUP_EC_USER = os.environ.get("PRODUCT_GROUP_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCT_GROUP_EC_PASS = os.environ.get("PRODUCT_GROUP_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

UNIT_AGREEMENT_EC_USER = os.environ.get("UNIT_AGREEMENT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
UNIT_AGREEMENT_EC_PASS = os.environ.get("UNIT_AGREEMENT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

ROYALTY_OWNER_EC_USER = os.environ.get("ROYALTY_OWNER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
ROYALTY_OWNER_EC_PASS = os.environ.get("ROYALTY_OWNER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

ROYALTY_DEPOSITOR_EC_USER = os.environ.get("ROYALTY_DEPOSITOR_EC_USER", os.environ.get("EC_USER", "sysadmin"))
ROYALTY_DEPOSITOR_EC_PASS = os.environ.get("ROYALTY_DEPOSITOR_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

CALENDAR_COLLECTION_EC_USER = os.environ.get("CALENDAR_COLLECTION_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CALENDAR_COLLECTION_EC_PASS = os.environ.get("CALENDAR_COLLECTION_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

ACCOUNT_MAPPING_EC_USER = os.environ.get("ACCOUNT_MAPPING_EC_USER", os.environ.get("EC_USER", "sysadmin"))
ACCOUNT_MAPPING_EC_PASS = os.environ.get("ACCOUNT_MAPPING_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

CALENDAR_EC_USER = os.environ.get("CALENDAR_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CALENDAR_EC_PASS = os.environ.get("CALENDAR_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

BERTH_EC_USER = os.environ.get("BERTH_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BERTH_EC_PASS = os.environ.get("BERTH_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CALCULATION_GROUP_CONTEXT_EC_USER = os.environ.get("CALCULATION_GROUP_CONTEXT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CALCULATION_GROUP_CONTEXT_EC_PASS = os.environ.get("CALCULATION_GROUP_CONTEXT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CALC_CONTEXT_EC_USER = os.environ.get("CALC_CONTEXT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CALC_CONTEXT_EC_PASS = os.environ.get("CALC_CONTEXT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
BLEND_EC_USER = os.environ.get("BLEND_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BLEND_EC_PASS = os.environ.get("BLEND_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CANAL_EC_USER = os.environ.get("CANAL_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CANAL_EC_PASS = os.environ.get("CANAL_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
INVENTORY_AREA_EC_USER = os.environ.get("INVENTORY_AREA_EC_USER", os.environ.get("EC_USER", "sysadmin"))
INVENTORY_AREA_EC_PASS = os.environ.get("INVENTORY_AREA_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CHEMICAL_TRANSPORT_TANK_EC_USER = os.environ.get("CHEMICAL_TRANSPORT_TANK_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CHEMICAL_TRANSPORT_TANK_EC_PASS = os.environ.get("CHEMICAL_TRANSPORT_TANK_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
METER_RUN_EC_USER = os.environ.get("METER_RUN_EC_USER", os.environ.get("EC_USER", "sysadmin"))
METER_RUN_EC_PASS = os.environ.get("METER_RUN_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
ORIFICE_PLATE_EC_USER = os.environ.get("ORIFICE_PLATE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
ORIFICE_PLATE_EC_PASS = os.environ.get("ORIFICE_PLATE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PORT_EC_USER = os.environ.get("PORT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PORT_EC_PASS = os.environ.get("PORT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
RESERVOIR_BLOCK_EC_USER = os.environ.get("RESERVOIR_BLOCK_EC_USER", os.environ.get("EC_USER", "sysadmin"))
RESERVOIR_BLOCK_EC_PASS = os.environ.get("RESERVOIR_BLOCK_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
RESERVOIR_FORMATION_EC_USER = os.environ.get("RESERVOIR_FORMATION_EC_USER", os.environ.get("EC_USER", "sysadmin"))
RESERVOIR_FORMATION_EC_PASS = os.environ.get("RESERVOIR_FORMATION_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
REPORT_AREA_EC_USER = os.environ.get("REPORT_AREA_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REPORT_AREA_EC_PASS = os.environ.get("REPORT_AREA_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PROCESS_TRAIN_EC_USER = os.environ.get("PROCESS_TRAIN_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PROCESS_TRAIN_EC_PASS = os.environ.get("PROCESS_TRAIN_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

SPLIT_ITEM_OTHER_EC_USER = os.environ.get("SPLIT_ITEM_OTHER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
SPLIT_ITEM_OTHER_EC_PASS = os.environ.get("SPLIT_ITEM_OTHER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
STORAGE_FLOW_EC_USER = os.environ.get("STORAGE_FLOW_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STORAGE_FLOW_EC_PASS = os.environ.get("STORAGE_FLOW_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
STREAM_ITEM_CATEGORY_EC_USER = os.environ.get("STREAM_ITEM_CATEGORY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STREAM_ITEM_CATEGORY_EC_PASS = os.environ.get("STREAM_ITEM_CATEGORY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
DATA_EXTRACT_SET_EC_USER = os.environ.get("DATA_EXTRACT_SET_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DATA_EXTRACT_SET_EC_PASS = os.environ.get("DATA_EXTRACT_SET_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
DATA_EXTRACT_SETUP_EC_USER = os.environ.get("DATA_EXTRACT_SETUP_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DATA_EXTRACT_SETUP_EC_PASS = os.environ.get("DATA_EXTRACT_SETUP_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
TRAILER_EC_USER = os.environ.get("TRAILER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
TRAILER_EC_PASS = os.environ.get("TRAILER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CARRIER_EC_USER = os.environ.get("CARRIER_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CARRIER_EC_PASS = os.environ.get("CARRIER_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

BANK_ACCOUNT_EC_USER = os.environ.get("BANK_ACCOUNT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
BANK_ACCOUNT_EC_PASS = os.environ.get("BANK_ACCOUNT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
DEFERMENT_GROUP_EC_USER = os.environ.get("DEFERMENT_GROUP_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DEFERMENT_GROUP_EC_PASS = os.environ.get("DEFERMENT_GROUP_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

DOCUMENT_TEMPLATE_EC_USER = os.environ.get("DOCUMENT_TEMPLATE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DOCUMENT_TEMPLATE_EC_PASS = os.environ.get("DOCUMENT_TEMPLATE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
PRODUCT_EC_USER = os.environ.get("PRODUCT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCT_EC_PASS = os.environ.get("PRODUCT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CHEMICAL_PRODUCT_EC_USER = os.environ.get("CHEMICAL_PRODUCT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CHEMICAL_PRODUCT_EC_PASS = os.environ.get("CHEMICAL_PRODUCT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
REPORT_CONTEXT_EC_USER = os.environ.get("REPORT_CONTEXT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REPORT_CONTEXT_EC_PASS = os.environ.get("REPORT_CONTEXT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
DOCUMENT_RECEIVED_TERM_EC_USER = os.environ.get("DOCUMENT_RECEIVED_TERM_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DOCUMENT_RECEIVED_TERM_EC_PASS = os.environ.get("DOCUMENT_RECEIVED_TERM_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
TARGET_MAPPING_CONFIGURATION_EC_USER = os.environ.get(
    "TARGET_MAPPING_CONFIGURATION_EC_USER", os.environ.get("EC_USER", "sysadmin")
)
TARGET_MAPPING_CONFIGURATION_EC_PASS = os.environ.get(
    "TARGET_MAPPING_CONFIGURATION_EC_PASS", os.environ.get("EC_PASS", "sysadmin")
)

DISPOSITION_TYPE_EC_USER = os.environ.get("DISPOSITION_TYPE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DISPOSITION_TYPE_EC_PASS = os.environ.get("DISPOSITION_TYPE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

PAYMENT_TERM_EC_USER = os.environ.get("PAYMENT_TERM_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PAYMENT_TERM_EC_PASS = os.environ.get("PAYMENT_TERM_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
DOCUMENT_DATE_TERM_EC_USER = os.environ.get("DOCUMENT_DATE_TERM_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DOCUMENT_DATE_TERM_EC_PASS = os.environ.get("DOCUMENT_DATE_TERM_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

EC_CODE_OBJECT_EC_USER = os.environ.get("EC_CODE_OBJECT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
EC_CODE_OBJECT_EC_PASS = os.environ.get("EC_CODE_OBJECT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

REPORT_GROUP_EC_USER = os.environ.get("REPORT_GROUP_EC_USER", os.environ.get("EC_USER", "sysadmin"))
REPORT_GROUP_EC_PASS = os.environ.get("REPORT_GROUP_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
STREAM_ALL_EC_USER = os.environ.get("STREAM_ALL_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STREAM_ALL_EC_PASS = os.environ.get("STREAM_ALL_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CHOKE_MODEL_EC_USER = os.environ.get("CHOKE_MODEL_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CHOKE_MODEL_EC_PASS = os.environ.get("CHOKE_MODEL_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
CHOKE_EC_USER = os.environ.get("CHOKE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
CHOKE_EC_PASS = os.environ.get("CHOKE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
PRODUCT_PRICE_OBJECT_EC_USER = os.environ.get("PRODUCT_PRICE_OBJECT_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCT_PRICE_OBJECT_EC_PASS = os.environ.get("PRODUCT_PRICE_OBJECT_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
DOCUMENT_SEQUENCE_EC_USER = os.environ.get("DOCUMENT_SEQUENCE_EC_USER", os.environ.get("EC_USER", "sysadmin"))
DOCUMENT_SEQUENCE_EC_PASS = os.environ.get("DOCUMENT_SEQUENCE_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
PRODUCT_SPLIT_KEY_EC_USER = os.environ.get("PRODUCT_SPLIT_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
PRODUCT_SPLIT_KEY_EC_PASS = os.environ.get("PRODUCT_SPLIT_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_USER = os.environ.get(
    "STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin")
)
STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_PASS = os.environ.get(
    "STREAM_ITEM_CATEGORY_SPLIT_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin")
)
COMPANY_SPLIT_KEY_EC_USER = os.environ.get("COMPANY_SPLIT_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
COMPANY_SPLIT_KEY_EC_PASS = os.environ.get("COMPANY_SPLIT_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
FIELD_SPLIT_KEY_EC_USER = os.environ.get("FIELD_SPLIT_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
FIELD_SPLIT_KEY_EC_PASS = os.environ.get("FIELD_SPLIT_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
OTHER_SPLIT_KEY_EC_USER = os.environ.get("OTHER_SPLIT_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
OTHER_SPLIT_KEY_EC_PASS = os.environ.get("OTHER_SPLIT_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
STREAM_ITEM_SPLIT_KEY_EC_USER = os.environ.get("STREAM_ITEM_SPLIT_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
STREAM_ITEM_SPLIT_KEY_EC_PASS = os.environ.get("STREAM_ITEM_SPLIT_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

INPUT_LIST_EC_USER = os.environ.get("INPUT_LIST_EC_USER", os.environ.get("EC_USER", "sysadmin"))
INPUT_LIST_EC_PASS = os.environ.get("INPUT_LIST_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
UOP_KEY_EC_USER = os.environ.get("UOP_KEY_EC_USER", os.environ.get("EC_USER", "sysadmin"))
UOP_KEY_EC_PASS = os.environ.get("UOP_KEY_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
HCB_SYSTEM_EC_USER = os.environ.get("HCB_SYSTEM_EC_USER", os.environ.get("EC_USER", "sysadmin"))
HCB_SYSTEM_EC_PASS = os.environ.get("HCB_SYSTEM_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

AREA_EC_USER = os.environ.get("AREA_EC_USER", os.environ.get("EC_USER", "sysadmin"))
AREA_EC_PASS = os.environ.get("AREA_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))

EXTERNAL_LOCATION_EC_USER = os.environ.get("EXTERNAL_LOCATION_EC_USER", os.environ.get("EC_USER", "sysadmin"))
EXTERNAL_LOCATION_EC_PASS = os.environ.get("EXTERNAL_LOCATION_EC_PASS", os.environ.get("EC_PASS", "sysadmin"))
