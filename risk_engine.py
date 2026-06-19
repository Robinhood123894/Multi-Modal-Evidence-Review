print("risk_engine loaded")

def get_risk_flags(vision_result, user_history):
    """
    Generate risk flags based on vision results and user history
    """
    risk_flags = []
    
    # Check image validity
    if not vision_result.get("valid_image", False):
        risk_flags.append("invalid_image")
    
    # Check for unknown/ambiguous results
    if vision_result.get("issue_type") == "unknown":
        risk_flags.append("unclear_damage")
    
    # User history based risks
    if not user_history.empty:
        history_row = user_history.iloc[0]
        
        # High claim frequency
        past_claims = history_row.get("past_claim_count", 0)
        if past_claims > 10:
            risk_flags.append("frequent_claims")
        
        # Multiple rejections
        rejected = history_row.get("rejected_claim", 0)
        if rejected > 3:
            risk_flags.append("multiple_rejections")
        
        # History flags from CSV
        history_flags = history_row.get("history_flags", "none")
        if history_flags != "none" and history_flags:
            if isinstance(history_flags, str):
                for flag in history_flags.split(";"):
                    if flag and flag != "none":
                        risk_flags.append(flag)
    
    # Remove duplicates
    risk_flags = list(dict.fromkeys(risk_flags))
    
    return risk_flags