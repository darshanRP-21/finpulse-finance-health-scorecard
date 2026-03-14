# ============================================================
# FinPulse — Personal Finance Health Scorer
# Author: Darshan Pipada
# Description: Calculates a personal finance health score
#              across 5 key pillars using standard benchmarks.
#              This is the core scoring logic behind the
#              FinPulse web dashboard.
# ============================================================

# ── SCORING ENGINE ──────────────────────────────────────────

def score_savings_rate(income, savings):
    """
    Savings Rate = (Monthly Savings / Monthly Income) × 100
    Benchmark: ≥ 20% is healthy (50/30/20 rule)
    """
    if income <= 0:
        return 0
    rate = (savings / income) * 100
    if rate >= 30:  return 100
    elif rate >= 20: return 85
    elif rate >= 15: return 68
    elif rate >= 10: return 50
    elif rate >= 5:  return 28
    else:            return 10


def score_debt_load(income, debt):
    """
    Debt-to-Income Ratio = (Total Debt / Annual Income) × 100
    Benchmark: < 30% of annual income is considered healthy
    """
    if income <= 0:
        return 0
    annual_income = income * 12
    dti = (debt / annual_income) * 100
    if debt == 0:    return 100
    elif dti <= 10:  return 92
    elif dti <= 25:  return 75
    elif dti <= 40:  return 55
    elif dti <= 65:  return 32
    else:            return 12


def score_emergency_fund(expenses, emergency):
    """
    Liquidity Ratio = Emergency Fund / Monthly Expenses
    Benchmark: 3–6 months of expenses is the standard recommendation
    """
    if expenses <= 0:
        return 0
    months_covered = emergency / expenses
    if months_covered >= 6:   return 100
    elif months_covered >= 4: return 82
    elif months_covered >= 3: return 66
    elif months_covered >= 1.5: return 42
    elif months_covered >= 0.5: return 22
    else:                       return 5


def score_investment_ratio(income, investment):
    """
    Investment Ratio = (Monthly Investment / Monthly Income) × 100
    Benchmark: ≥ 10% of income invested is a healthy target
    """
    if income <= 0:
        return 0
    ratio = (investment / income) * 100
    if ratio >= 20:  return 100
    elif ratio >= 15: return 84
    elif ratio >= 10: return 66
    elif ratio >= 5:  return 46
    elif ratio >= 1:  return 24
    else:             return 0


def score_spending_discipline(income, expenses, insurance):
    """
    Spending Discipline = Expense Ratio + Insurance Bonus
    Expense Ratio = (Monthly Expenses / Monthly Income) × 100
    Benchmark: Spending ≤ 50% of income is healthy
    Bonus: +12 points if insurance is active
    """
    if income <= 0:
        return 0
    expense_ratio = (expenses / income) * 100
    if expense_ratio <= 40:  score = 95
    elif expense_ratio <= 50: score = 78
    elif expense_ratio <= 60: score = 58
    elif expense_ratio <= 72: score = 38
    elif expense_ratio <= 85: score = 18
    else:                     score = 5

    # Insurance coverage bonus
    if insurance > 0:
        score = min(100, score + 12)

    return score


# ── MAIN SCORING FUNCTION ───────────────────────────────────

def calculate_finance_score(income, savings, expenses, debt,
                             emergency, investment, insurance):
    """
    Calculates overall Finance Health Score out of 100.

    Pillar Weights:
        Savings Rate         → 25%
        Debt Load            → 20%
        Emergency Fund       → 20%
        Investment Ratio     → 20%
        Spending Discipline  → 15%

    Parameters:
        income     (float): Monthly take-home income (₹)
        savings    (float): Monthly savings amount (₹)
        expenses   (float): Monthly expenses (₹)
        debt       (float): Total outstanding debt (₹)
        emergency  (float): Emergency fund balance (₹)
        investment (float): Monthly investment amount (₹)
        insurance  (float): Monthly insurance premium (₹)

    Returns:
        dict: Scores for each pillar and overall total
    """

    # Input validation
    if income <= 0:
        raise ValueError("Income must be greater than 0.")
    if savings > income:
        raise ValueError("Savings cannot exceed income.")
    if any(v < 0 for v in [savings, expenses, debt, emergency, investment, insurance]):
        raise ValueError("All values must be non-negative.")

    # Individual pillar scores
    s1 = score_savings_rate(income, savings)
    s2 = score_debt_load(income, debt)
    s3 = score_emergency_fund(expenses, emergency)
    s4 = score_investment_ratio(income, investment)
    s5 = score_spending_discipline(income, expenses, insurance)

    # Weighted total
    total = round(
        s1 * 0.25 +
        s2 * 0.20 +
        s3 * 0.20 +
        s4 * 0.20 +
        s5 * 0.15
    )

    # Computed metrics
    savings_rate  = round((savings / income) * 100, 1)
    dti_ratio     = round((debt / (income * 12)) * 100, 1)
    months_covered = round(emergency / expenses, 1) if expenses > 0 else 0
    invest_ratio  = round((investment / income) * 100, 1)
    expense_ratio = round((expenses / income) * 100, 1)

    return {
        "total_score": total,
        "grade": get_grade(total),
        "pillars": {
            "savings_rate":         {"score": s1, "value": f"{savings_rate}%",    "benchmark": "≥ 20%"},
            "debt_load":            {"score": s2, "value": f"{dti_ratio}%",       "benchmark": "< 30%"},
            "emergency_fund":       {"score": s3, "value": f"{months_covered} mo","benchmark": "3–6 months"},
            "investment_ratio":     {"score": s4, "value": f"{invest_ratio}%",    "benchmark": "≥ 10%"},
            "spending_discipline":  {"score": s5, "value": f"{expense_ratio}%",   "benchmark": "≤ 50%"},
        }
    }


def get_grade(score):
    """Returns letter grade and verdict based on total score."""
    if score >= 85: return {"grade": "A+", "verdict": "Financially Elite"}
    if score >= 75: return {"grade": "A",  "verdict": "Strong Foundations"}
    if score >= 62: return {"grade": "B",  "verdict": "On the Right Track"}
    if score >= 48: return {"grade": "C",  "verdict": "Room to Improve"}
    if score >= 32: return {"grade": "D",  "verdict": "Needs Work"}
    return              {"grade": "E",  "verdict": "Take Action Now"}


# ── DISPLAY FUNCTION ────────────────────────────────────────

def display_report(result):
    """Prints a formatted Finance Health Report to the console."""
    print("\n" + "="*52)
    print("   💰 FINPULSE — FINANCE HEALTH REPORT")
    print("   by Darshan Pipada")
    print("="*52)
    print(f"\n   Overall Score : {result['total_score']} / 100")
    print(f"   Grade         : {result['grade']['grade']}")
    print(f"   Verdict       : {result['grade']['verdict']}")
    print("\n" + "-"*52)
    print(f"   {'PILLAR':<24} {'SCORE':>6}  {'VALUE':>10}  {'BENCHMARK'}")
    print("-"*52)

    pillar_labels = {
        "savings_rate":        "Savings Rate",
        "debt_load":           "Debt Load",
        "emergency_fund":      "Emergency Fund",
        "investment_ratio":    "Investment Ratio",
        "spending_discipline": "Spending Discipline",
    }

    for key, data in result["pillars"].items():
        label = pillar_labels[key]
        bar = "█" * (data["score"] // 10) + "░" * (10 - data["score"] // 10)
        print(f"   {label:<24} {data['score']:>5}  {data['value']:>10}  {data['benchmark']}")

    print("="*52)
    print("\n   ⚠️  Educational project — not financial advice.")
    print("="*52 + "\n")


# ── EXAMPLE RUN ─────────────────────────────────────────────

if __name__ == "__main__":

    # Sample inputs — modify these to test different scenarios
    sample = {
        "income":     50000,   # Monthly income (₹)
        "savings":     8000,   # Monthly savings (₹)
        "expenses":   28000,   # Monthly expenses (₹)
        "debt":       80000,   # Total debt outstanding (₹)
        "emergency":  40000,   # Emergency fund (₹)
        "investment":  4000,   # Monthly investments (₹)
        "insurance":   1500,   # Monthly insurance premium (₹)
    }

    result = calculate_finance_score(**sample)
    display_report(result)
