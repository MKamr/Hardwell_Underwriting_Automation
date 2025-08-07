#!/usr/bin/env python3
"""
Configuration management for the Real Estate Underwriting AI application.
Centralizes all hardcoded values and business rules from rulebook.txt
"""

import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration settings."""
    
    # File upload settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set = None
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    
    # Processing settings
    MAX_CONCURRENT_SESSIONS: int = 10
    SESSION_TIMEOUT_HOURS: int = 24
    PROCESSING_TIMEOUT_MINUTES: int = 30
    
    # Database settings (for future implementation)
    DATABASE_URL: Optional[str] = None
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_HOSTS: List[str] = None
    
    def __post_init__(self):
        if self.ALLOWED_EXTENSIONS is None:
            self.ALLOWED_EXTENSIONS = {'.pdf', '.xlsx', '.xls', '.csv'}
        if self.ALLOWED_HOSTS is None:
            self.ALLOWED_HOSTS = ["*"]

@dataclass
class UnderwritingConfig:
    """Underwriting business rules and constants from rulebook.txt."""
    
    # Income Rules
    VACANCY_RATE: float = 0.05  # 5% of GPI or actuals (whichever higher)
    RENT_UNDERPRICED_THRESHOLD: float = 0.30  # Flag units 30%+ under average
    
    # Expense Rules
    PROPERTY_TAX_REFINANCE_INCREASE: float = 0.075  # 7.5% increase for refinance
    INSURANCE_INCREASE: float = 0.05  # 5% increase
    UTILITY_INCREASE: float = 0.02  # 2% increase
    
    # R&M Age-based minimums (per unit)
    R_M_MINIMUMS: Dict[Tuple[int, int], int] = None
    R_M_CAP: int = 1500  # Cap at $1,500/unit
    
    # Professional Fees
    ADMIN_MINIMUM: int = 1000  # $1,000 total minimum
    ADMIN_MAXIMUM_PER_UNIT: int = 400  # $400/unit maximum
    
    # Management Fee tiers (based on gross income)
    MANAGEMENT_FEE_RATES: Dict[float, float] = None
    
    # Replacement Reserves
    REPLACEMENT_RESERVES_PER_UNIT: int = 250  # $250/unit
    
    # Minimum Expense Ratio
    MIN_EXPENSE_RATIO: float = 0.28  # 28% of EGI
    
    # Loan Constraints
    AGENCY_MAX_LTV: float = 0.75  # 75%
    AGENCY_MIN_DSCR: float = 1.25  # 1.25x
    AGENCY_MIN_DEBT_YIELD: float = 0.08  # 8%
    CMBS_MAX_LTV: float = 0.75  # 75%
    CMBS_MIN_DSCR: float = 1.25  # 1.25x
    CMBS_MIN_DEBT_YIELD: float = 0.09  # 9%
    DEBT_FUND_MIN_LOAN: int = 20_000_000  # $20M
    DEBT_FUND_DSCR: float = 0.95  # 0.95x
    
    # Interest Rate Spreads
    AGENCY_RATE_SPREAD_6M_PLUS: float = 0.015  # 150 bps for ≥$6M
    AGENCY_RATE_SPREAD_UNDER_6M: float = 0.02  # 200 bps for <$6M
    CMBS_RATE_SPREAD: float = 0.03  # 300 bps
    DEBT_FUND_RATE_SPREAD: float = 0.015  # 150 bps
    
    def __post_init__(self):
        if self.R_M_MINIMUMS is None:
            self.R_M_MINIMUMS = {
                (0, 10): 500,    # <10 years old: $500/unit
                (10, 20): 600,   # 10–20 yrs: $600
                (20, 30): 700,   # 20–30 yrs: $700
                (30, 40): 800,   # 30–40 yrs: $800
                (40, 50): 900,   # 40–50 yrs: $900
                (50, 1000): 1000 # 50+ yrs: $1,000
            }
        
        if self.MANAGEMENT_FEE_RATES is None:
            self.MANAGEMENT_FEE_RATES = {
                500_000: 0.05,   # ≤ $500K: 5%
                750_000: 0.045,  # $500K–$750K: 4.5%
                1_000_000: 0.04, # $750K–$1M: 4%
                1_500_000: 0.035,# $1M–$1.5M: 3.5%
                2_000_000: 0.03, # $1.5M–$2M: 3%
                float('inf'): 0.025 # $2M+: 2.5%
            }

@dataclass
class ProcessingConfig:
    """Document processing configuration."""
    
    # PDF processing
    MAX_PDF_PAGES: int = 100
    TABLE_QUALITY_THRESHOLD: float = 0.7
    MAX_TABLES_PER_DOCUMENT: int = 10
    
    # CSV generation
    CSV_ENCODING: str = "utf-8"
    CSV_DELIMITER: str = ","
    
    # File naming
    TIMESTAMP_FORMAT: str = "%Y%m%d_%H%M%S"
    MAX_FILENAME_LENGTH: int = 100

# Global configuration instances
app_config = AppConfig()
underwriting_config = UnderwritingConfig()
processing_config = ProcessingConfig()

def get_config() -> Dict[str, Any]:
    """Get all configuration as a dictionary."""
    return {
        "app": app_config,
        "underwriting": underwriting_config,
        "processing": processing_config
    }

def load_config_from_env():
    """Load configuration from environment variables."""
    # App config
    app_config.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", app_config.MAX_FILE_SIZE))
    app_config.LOG_LEVEL = os.getenv("LOG_LEVEL", app_config.LOG_LEVEL)
    app_config.SECRET_KEY = os.getenv("SECRET_KEY", app_config.SECRET_KEY)
    
    # Underwriting config
    if os.getenv("VACANCY_RATE"):
        underwriting_config.VACANCY_RATE = float(os.getenv("VACANCY_RATE"))
    
    if os.getenv("MIN_EXPENSE_RATIO"):
        underwriting_config.MIN_EXPENSE_RATIO = float(os.getenv("MIN_EXPENSE_RATIO"))

# Load environment-based configuration
load_config_from_env() 