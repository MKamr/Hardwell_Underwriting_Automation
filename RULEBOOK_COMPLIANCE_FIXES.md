# 🚨 Rulebook Compliance Issues & Fixes

## Overview
This document outlines the critical issues found in `app_demo_fixed.py` when compared to the `rulebook.txt` requirements and provides specific solutions.

## 🚨 Critical Issues

### 1. **Expense Rules Violations**

#### ❌ Current Problems:
```python
# Line 362: Hardcoded expense ratio
expense_ratio = 0.32  # Should be calculated based on actuals + minimums

# Line 584-585: Hardcoded R&M values
'rm_per_unit': '250',  # Should be age-based: $500-$1000/unit
'residential_per_unit': '250',  # Should be $250/unit (correct)

# Missing age-based R&M calculations
# Missing management fee tiers
# Missing minimum expense ratio enforcement
```

#### ✅ Required Fixes:
```python
# 1. Age-based R&M calculation
def calculate_rm_minimum(property_age: int, unit_count: int) -> int:
    """Calculate R&M minimum based on property age."""
    for age_range, minimum in underwriting_config.R_M_MINIMUMS.items():
        if age_range[0] <= property_age < age_range[1]:
            return minimum * unit_count
    return 500 * unit_count  # Default

# 2. Management fee calculation
def calculate_management_fee(gross_income: float) -> float:
    """Calculate management fee based on gross income tiers."""
    for threshold, rate in underwriting_config.MANAGEMENT_FEE_RATES.items():
        if gross_income <= threshold:
            return gross_income * rate
    return gross_income * 0.025  # Default 2.5%

# 3. Minimum expense ratio enforcement
def enforce_minimum_expense_ratio(total_expenses: float, egi: float) -> float:
    """Ensure expenses meet minimum 28% of EGI."""
    min_expenses = egi * underwriting_config.MIN_EXPENSE_RATIO
    return max(total_expenses, min_expenses)
```

### 2. **Income Rules Violations**

#### ❌ Current Problems:
```python
# Line 355-356: Hardcoded rent assumptions
base_rent = 1200 if "apartment" in property_info.property_name.lower() else 1500
estimated_units = max(50, len(uploaded_files) * 15)

# Line 360: Hardcoded vacancy
vacancy_factor = 0.05 if t12_files else 0.08  # Should be 5% of GPI or actuals (whichever higher)
```

#### ✅ Required Fixes:
```python
# 1. Use actual rents from rent roll
def calculate_actual_rents(rent_roll_df: pd.DataFrame) -> Dict[str, float]:
    """Calculate actual rents from rent roll data."""
    # Implementation needed to extract actual rents
    pass

# 2. Calculate vacancy properly
def calculate_vacancy(gpi: float, actual_vacancy: float) -> float:
    """Calculate vacancy: 5% of GPI or actuals (whichever higher)."""
    vacancy_5_percent = gpi * underwriting_config.VACANCY_RATE
    return max(vacancy_5_percent, actual_vacancy)

# 3. Flag underpriced units
def flag_underpriced_units(rent_roll_df: pd.DataFrame) -> List[Dict]:
    """Flag units 30%+ under average rent for unit type."""
    flags = []
    # Implementation needed
    return flags
```

### 3. **Missing Required Output Tabs**

#### ❌ Current Problems:
- Missing "Clean Rent Roll" tab
- Missing "Clean T12 (cut off at NOI)" tab  
- Missing "Underwriting Summary" with proper columns
- Missing bridge loan specific tabs

#### ✅ Required Fixes:
```python
# 1. Clean Rent Roll Tab
def generate_clean_rent_roll(rent_roll_df: pd.DataFrame) -> pd.DataFrame:
    """Generate clean rent roll with unnecessary columns removed."""
    # Remove: deposits, tenant names, balances owed
    # Keep: unit, type, sq ft, current rent, lease expiry, status
    pass

# 2. Clean T12 Tab (cut off at NOI)
def generate_clean_t12(t12_df: pd.DataFrame) -> pd.DataFrame:
    """Generate clean T12 cut off at Net Operating Income."""
    # Remove: depreciation, interest expense, CapEx, below-the-line items
    pass

# 3. Underwriting Summary Tab
def generate_underwriting_summary(analysis_data: Dict) -> pd.DataFrame:
    """Generate underwriting summary with required columns."""
    columns = ["Line Item", "$ Amount", "% of EGI", "Notes"]
    # Implementation needed
    pass

# 4. Bridge Loan Tabs (if applicable)
def generate_bridge_loan_tabs(property_info: Dict) -> Dict[str, pd.DataFrame]:
    """Generate bridge loan specific tabs."""
    if property_info.get('is_bridge_loan'):
        return {
            "Pro Forma Rent Roll": generate_pro_forma_rent_roll(),
            "Pro Forma Income Statement": generate_pro_forma_income(),
            "Sources & Uses": generate_sources_uses(),
            "Construction Budget": generate_construction_budget()
        }
    return {}
```

### 4. **Missing Deep Logic**

#### ❌ Current Problems:
- No spike detection for utilities
- No age-based property calculations
- No trending analysis for T3/T6 vs T12
- No flagging of underpriced units

#### ✅ Required Fixes:
```python
# 1. Utility spike detection
def detect_utility_spikes(utility_data: pd.DataFrame) -> pd.DataFrame:
    """Remove abnormally high utility months before calculating."""
    # Implementation needed to detect and remove spikes
    pass

# 2. Age-based calculations
def calculate_age_based_expenses(property_age: int, unit_count: int) -> Dict[str, float]:
    """Calculate age-based expense minimums."""
    return {
        "repairs_maintenance": calculate_rm_minimum(property_age, unit_count),
        "payroll": calculate_rm_minimum(property_age, unit_count),  # Same as R&M
        "replacement_reserves": unit_count * underwriting_config.REPLACEMENT_RESERVES_PER_UNIT
    }

# 3. Trending analysis
def analyze_income_trending(t3_data: pd.DataFrame, t6_data: pd.DataFrame, t12_data: pd.DataFrame) -> Dict:
    """Analyze income trending to determine which period to use."""
    # Implementation needed to detect upward trends
    pass
```

## 🔧 Implementation Plan

### Phase 1: Configuration Management ✅
- [x] Created `config.py` with all rulebook requirements
- [ ] Update `app_demo_fixed.py` to use configuration

### Phase 2: Core Business Logic
- [ ] Implement age-based R&M calculations
- [ ] Implement management fee tiers
- [ ] Implement minimum expense ratio enforcement
- [ ] Implement proper vacancy calculation

### Phase 3: Income Analysis
- [ ] Implement actual rent extraction from rent roll
- [ ] Implement underpriced unit flagging
- [ ] Implement utility spike detection
- [ ] Implement income trending analysis

### Phase 4: Output Generation
- [ ] Implement clean rent roll generation
- [ ] Implement clean T12 generation (cut off at NOI)
- [ ] Implement underwriting summary with proper columns
- [ ] Implement bridge loan specific tabs

### Phase 5: Testing & Validation
- [ ] Create unit tests for all business logic
- [ ] Validate against rulebook requirements
- [ ] Test with real document samples

## 📊 Priority Matrix

| Issue | Severity | Impact | Effort | Priority |
|-------|----------|--------|--------|----------|
| Hardcoded expense ratios | High | High | Medium | 1 |
| Missing required output tabs | High | High | High | 2 |
| Age-based R&M calculations | Medium | High | Medium | 3 |
| Income trending analysis | Medium | Medium | High | 4 |
| Utility spike detection | Low | Medium | Medium | 5 |

## 🎯 Success Criteria

1. **100% Rulebook Compliance**: All business rules from `rulebook.txt` implemented
2. **Configurable System**: All hardcoded values moved to configuration
3. **Professional Output**: All required tabs generated correctly
4. **Deep Logic**: Advanced analysis features implemented
5. **Testing Coverage**: Comprehensive unit tests for all business logic

## 🚀 Next Steps

1. **Immediate**: Update `app_demo_fixed.py` to use the new `config.py`
2. **Short-term**: Implement core business logic fixes
3. **Medium-term**: Add missing output tabs
4. **Long-term**: Implement advanced analysis features 