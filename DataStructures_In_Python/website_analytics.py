# Given visitor data
monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}

# ---- 1. Unique Visitors Across All Days ----
unique_visitors = monday_visitors | tuesday_visitors | wednesday_visitors
print("Unique Visitors Across All Days:", unique_visitors)
print("Total Unique Visitors:", len(unique_visitors))
print()

# ---- 2. Returning Visitors on Tuesday (also visited Monday) ----
returning_tuesday = monday_visitors & tuesday_visitors
print("Returning Visitors on Tuesday (also visited Monday):", returning_tuesday)
print()

# ---- 3. New Visitors Each Day ----
new_monday = monday_visitors   # first day, everyone is new
new_tuesday = tuesday_visitors - monday_visitors
new_wednesday = wednesday_visitors - (monday_visitors | tuesday_visitors)

print("New Visitors Monday:", new_monday)
print("New Visitors Tuesday:", new_tuesday)
print("New Visitors Wednesday:", new_wednesday)
print()

# ---- 4. Loyal Visitors (visited all three days) ----
loyal_visitors = monday_visitors & tuesday_visitors & wednesday_visitors
print("Loyal Visitors (all three days):", loyal_visitors)
print()

# ---- 5. Daily Visitor Overlap Analysis ----
overlap_mon_tue = monday_visitors & tuesday_visitors
overlap_tue_wed = tuesday_visitors & wednesday_visitors
overlap_mon_wed = monday_visitors & wednesday_visitors

print("Overlap Monday-Tuesday:", overlap_mon_tue)
print("Overlap Tuesday-Wednesday:", overlap_tue_wed)
print("Overlap Monday-Wednesday:", overlap_mon_wed)
