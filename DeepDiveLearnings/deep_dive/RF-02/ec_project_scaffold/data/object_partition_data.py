"""
Object Partition test data
Used in data-driven tests via Variables import
"""

# Test operators and roles — use AUTOTEST_ prefix for all test data
TEST_OPERATORS = [
    'OPS_ENGINEER',
    'ALLOC_ENGINEER',
]

TEST_ROLES = [
    'AUTOTEST_ROLE_READ',
    'AUTOTEST_ROLE_WRITE',
]

# Combined data for data-driven insert tests
OPERATOR_ROLE_PAIRS = [
    ('OPS_ENGINEER', 'AUTOTEST_ROLE_READ'),
    ('ALLOC_ENGINEER', 'AUTOTEST_ROLE_WRITE'),
]
