def calculate_spam_probability():
    # Get user inputs
    try:
        total_emails = int(input("Enter total number of emails: "))
        emails_with_free = int(input("Enter number of emails containing 'free': "))
        spam_emails = int(input("Enter number of spam emails: "))
        spam_and_free = int(input("Enter number of emails that are spam and contain 'free': "))
    except ValueError:
        print("❌ Please enter valid integers.")
        return

    # Validate inputs
    if total_emails <= 0:
        print("❌ Total emails must be greater than 0.")
        return
    if not (0 <= emails_with_free <= total_emails):
        print("❌ Emails with 'free' must be between 0 and total emails.")
        return
    if not (0 <= spam_emails <= total_emails):
        print("❌ Spam emails must be between 0 and total emails.")
        return
    if not (0 <= spam_and_free <= min(spam_emails, emails_with_free)):
        print("❌ Spam & Free count must be between 0 and min(spam_emails, emails_with_free).")
        return

    # Apply Bayes' Theorem
    P_spam = spam_emails / total_emails
    P_free = emails_with_free / total_emails
    P_free_given_spam = spam_and_free / spam_emails if spam_emails > 0 else 0

    if P_free == 0:
        print("❌ Cannot compute probability because P(Free) = 0.")
        return

    P_spam_given_free = (P_free_given_spam * P_spam) / P_free

    # Print result
    print(f"P(Spam | Free): {P_spam_given_free:.4f}")


# Run program
calculate_spam_probability()
