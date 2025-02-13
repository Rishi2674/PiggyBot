def process_expense_query_results(expense_data):
    """
    Processes expense query results, performs calculations, and formats data for the LLM.
    
    Args:
        expense_data (list of dict): Query results from MongoDB.
        
    Returns:
        dict: Precomputed summary for the LLM.
    """
    from collections import defaultdict

    total_spent = 0
    category_totals = defaultdict(float)
    grouped_expenses = defaultdict(list)

    for expense in expense_data:
        amount = expense["amount"]
        category = expense["category"]
        description = expense["description"]

        # Aggregate totals
        total_spent += amount
        category_totals[category] += amount
        grouped_expenses[category].append(f"{description} - ₹{amount}")

    # Prepare structured output
    summary = {
        "total_spent": total_spent,
        "category_breakdown": dict(category_totals),
        "formatted_expenses": grouped_expenses
    }
    
    return summary

def format_query_for_llm(user_name, expense_summary):
    """
    Formats the precomputed expense data into a natural language prompt for the LLM.

    Args:
        user_name (str): User's name.
        expense_summary (dict): Precomputed expense data.

    Returns:
        str: Formatted prompt for LLM.
    """
    
    total_spent = expense_summary["total_spent"]
    category_details = "\n".join(
        f"- {category}: ₹{amount}" for category, amount in expense_summary["category_breakdown"].items()
    )

    expense_details = "\n".join(
        f"**{category}:**\n" + "\n".join(expense_summary["formatted_expenses"][category])
        for category in expense_summary["formatted_expenses"]
    )

    prompt = f"""
        You are an AI assistant that converts structured MongoDB query results into a natural language summary for a user.

        **User:** {user_name}

        **Summary of Expenses:**
        - Total spent: ₹{total_spent}
        - Breakdown:
        {category_details}

        **Expense Details:**
        {expense_details}

        Convert this into a natural language summary.
        """
        
    response_text = f"""
        *User:* {user_name}

        *Summary of Expenses:*
        - Total spent: ₹{total_spent}
        - Breakdown:
        {category_details}

        *Expense Details:*
        {expense_details}
        """
    return prompt,response_text