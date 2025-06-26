def rule_based_check(email_text):
    suspicious_keywords = ['verify your account', 'click here', 'login immediately', 'password expired']
    score = sum(1 for word in suspicious_keywords if word in email_text.lower())
    return score >= 2
