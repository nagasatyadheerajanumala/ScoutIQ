"""
SQLAlchemy models for ScoutIQ MVP
Defines models for all 18 PostgreSQL tables based on the Travis County ATTOM data.
"""

from sqlalchemy import Column, Integer, String, String, Date, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from datetime import datetime

Base = declarative_base()

class TaxAssessor(Base):
    """Tax Assessor data - main property information"""
    __tablename__ = 'blackland_capital_group_taxassessor_0001_sample'
    
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    situs_state_code = Column('SitusStateCode', String)
    situs_county = Column('SitusCounty', String)
    property_jurisdiction_name = Column('PropertyJurisdictionName', String)
    property_address_full = Column('PropertyAddressFull', String)
    property_address_city = Column('PropertyAddressCity', String)
    property_address_state = Column('PropertyAddressState', String)
    property_address_zip = Column('PropertyAddressZIP', String)
    property_latitude = Column('PropertyLatitude', String)
    property_longitude = Column('PropertyLongitude', String)
    party_owner1_name_full = Column('PartyOwner1NameFull', String)
    party_owner2_name_full = Column('PartyOwner2NameFull', String)
    contact_owner_mail_address_full = Column('ContactOwnerMailAddressFull', String)
    status_owner_occupied_flag = Column('StatusOwnerOccupiedFlag', String)
    tax_year_assessed = Column('TaxYearAssessed', String)
    tax_assessed_value_total = Column('TaxAssessedValueTotal', String)
    tax_market_value_total = Column('TaxMarketValueTotal', String)
    year_built = Column('YearBuilt', String)
    zoned_code_local = Column('ZonedCodeLocal', String)
    property_use_standardized = Column('PropertyUseStandardized', String)
    assessor_last_sale_date = Column('AssessorLastSaleDate', String)
    assessor_last_sale_amount = Column('AssessorLastSaleAmount', String)
    area_lot_acres = Column('AreaLotAcres', String)
    area_lot_sf = Column('AreaLotSF', String)
    bedrooms_count = Column('BedroomsCount', String)
    bath_count = Column('BathCount', String)
    stories_count = Column('StoriesCount', String)
    publication_date = Column('PublicationDate', String)

class AVM(Base):
    """Automated Valuation Model data"""
    __tablename__ = 'blackland_capital_group_avm_0002'
    
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    estimated_value = Column('EstimatedValue', String)
    estimated_min_value = Column('EstimatedMinValue', String)
    estimated_max_value = Column('EstimatedMaxValue', String)
    create_date = Column('CreateDate', String)
    valuation_date = Column('ValuationDate', String)
    confidence_score = Column('ConfidenceScore', String)
    fsd = Column('FSD', String)
    last_update_date = Column('LastUpdateDate', String)
    publication_date = Column('PublicationDate', String)

class Recorder(Base):
    """Property transaction records"""
    __tablename__ = 'blackland_capital_group_recorder_0001_sample'
    
    transaction_id = Column('TransactionID', String, primary_key=True)
    attom_id = Column('[ATTOM ID]', String)
    document_type_code = Column('DocumentTypeCode', String)
    document_number_formatted = Column('DocumentNumberFormatted', String)
    instrument_date = Column('InstrumentDate', String)
    recording_date = Column('RecordingDate', String)
    transaction_type = Column('TransactionType', String)
    transfer_amount = Column('TransferAmount', String)
    grantor1_name_full = Column('Grantor1NameFull', String)
    grantee1_name_full = Column('Grantee1NameFull', String)
    mortgage1_amount = Column('Mortgage1Amount', String)
    mortgage1_term = Column('Mortgage1Term', String)
    mortgage1_term_date = Column('Mortgage1TermDate', String)
    mortgage1_interest_rate = Column('Mortgage1InterestRate', String)
    property_address_full = Column('PropertyAddressFull', String)
    property_use_standardized = Column('PropertyUseStandardized', String)
    publication_date = Column('PublicationDate', String)

class PropertyDeletes(Base):
    """Property deletion records"""
    __tablename__ = 'blackland_capital_group_propertydeletes_0001'
    
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    property_address_full = Column('PropertyAddressFull', String)
    delete_date = Column('DeleteDate', String)
    delete_reason = Column('DeleteReason', String)
    publication_date = Column('PublicationDate', String)

class PropertyToBoundaryMatch(Base):
    """Property boundary and parcel data"""
    __tablename__ = 'blackland_capital_group_propertytoboundarymatch_parcel_0003'
    
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    property_address_full = Column('PropertyAddressFull', String)
    parcel_geometry = Column('ParcelGeometry', Text)  # GeoJSON
    parcel_number = Column('ParcelNumber', String)
    publication_date = Column('PublicationDate', String)

class AILogs(Base):
    """AI interaction logs"""
    __tablename__ = 'scoutiq_ai_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(String, nullable=False)
    input_payload = Column(JSONB)
    output_response = Column(JSONB)
    classification = Column(String)
    confidence = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    endpoint_used = Column(String)
    processing_time_ms = Column(Integer)

# Additional models for other datasets
class PropertyDataSampleAVM0024(Base):
    __tablename__ = 'property_data_sample_csv_avm_0024'
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    estimated_value = Column('EstimatedValue', String)
    estimated_min_value = Column('EstimatedMinValue', String)
    estimated_max_value = Column('EstimatedMaxValue', String)
    confidence_score = Column('ConfidenceScore', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleAVM0030(Base):
    __tablename__ = 'property_data_sample_csv_avm_0030'
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    estimated_value = Column('EstimatedValue', String)
    estimated_min_value = Column('EstimatedMinValue', String)
    estimated_max_value = Column('EstimatedMaxValue', String)
    confidence_score = Column('ConfidenceScore', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleRecorder0023(Base):
    __tablename__ = 'property_data_sample_csv_recorder_0023'
    transaction_id = Column('TransactionID', String, primary_key=True)
    attom_id = Column('[ATTOM ID]', String)
    document_type_code = Column('DocumentTypeCode', String)
    transfer_amount = Column('TransferAmount', String)
    recording_date = Column('RecordingDate', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleRecorder0029(Base):
    __tablename__ = 'property_data_sample_csv_recorder_0029'
    transaction_id = Column('TransactionID', String, primary_key=True)
    attom_id = Column('[ATTOM ID]', String)
    document_type_code = Column('DocumentTypeCode', String)
    transfer_amount = Column('TransferAmount', String)
    recording_date = Column('RecordingDate', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleTaxAssessor0023(Base):
    __tablename__ = 'property_data_sample_csv_taxassessor_0023'
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    property_address_full = Column('PropertyAddressFull', String)
    property_latitude = Column('PropertyLatitude', String)
    property_longitude = Column('PropertyLongitude', String)
    tax_assessed_value_total = Column('TaxAssessedValueTotal', String)
    tax_market_value_total = Column('TaxMarketValueTotal', String)
    year_built = Column('YearBuilt', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleTaxAssessor0029(Base):
    __tablename__ = 'property_data_sample_csv_taxassessor_0029'
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    property_address_full = Column('PropertyAddressFull', String)
    property_latitude = Column('PropertyLatitude', String)
    property_longitude = Column('PropertyLongitude', String)
    tax_assessed_value_total = Column('TaxAssessedValueTotal', String)
    tax_market_value_total = Column('TaxMarketValueTotal', String)
    year_built = Column('YearBuilt', String)
    publication_date = Column('PublicationDate', String)

# Additional delete and recorder models
class PropertyDataSamplePropertyDeletes0023(Base):
    __tablename__ = 'property_data_sample_csv_propertydeletes_0023'
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    property_address_full = Column('PropertyAddressFull', String)
    delete_date = Column('DeleteDate', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSamplePropertyDeletes0029(Base):
    __tablename__ = 'property_data_sample_csv_propertydeletes_0029'
    attom_id = Column('[ATTOM ID]', String, primary_key=True)
    property_address_full = Column('PropertyAddressFull', String)
    delete_date = Column('DeleteDate', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleRecorderDeletes0023(Base):
    __tablename__ = 'property_data_sample_csv_recorderdeletes_0023'
    transaction_id = Column('TransactionID', String, primary_key=True)
    attom_id = Column('[ATTOM ID]', String)
    delete_date = Column('DeleteDate', String)
    publication_date = Column('PublicationDate', String)

class PropertyDataSampleRecorderDeletes0029(Base):
    __tablename__ = 'property_data_sample_csv_recorderdeletes_0029'
    transaction_id = Column('TransactionID', String, primary_key=True)
    attom_id = Column('[ATTOM ID]', String)
    delete_date = Column('DeleteDate', String)
    publication_date = Column('PublicationDate', String)

# Model registry for easy access
MODEL_REGISTRY = {
    'tax_assessor': TaxAssessor,
    'avm': AVM,
    'recorder': Recorder,
    'property_deletes': PropertyDeletes,
    'property_boundary': PropertyToBoundaryMatch,
    'ai_logs': AILogs,
    'avm_0024': PropertyDataSampleAVM0024,
    'avm_0030': PropertyDataSampleAVM0030,
    'recorder_0023': PropertyDataSampleRecorder0023,
    'recorder_0029': PropertyDataSampleRecorder0029,
    'tax_assessor_0023': PropertyDataSampleTaxAssessor0023,
    'tax_assessor_0029': PropertyDataSampleTaxAssessor0029,
    'property_deletes_0023': PropertyDataSamplePropertyDeletes0023,
    'property_deletes_0029': PropertyDataSamplePropertyDeletes0029,
    'recorder_deletes_0023': PropertyDataSampleRecorderDeletes0023,
    'recorder_deletes_0029': PropertyDataSampleRecorderDeletes0029,
}
