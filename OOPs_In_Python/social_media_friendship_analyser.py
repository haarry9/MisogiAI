def analyze_friendships():
    """
    Analyze friendship patterns across different social media platforms
    """
    # User friends on different platforms
    facebook_friends = {"alice", "bob", "charlie", "diana", "eve", "frank"}
    instagram_friends = {"bob", "charlie", "grace", "henry", "alice", "ivan"}
    twitter_friends = {"alice", "diana", "grace", "jack", "bob", "karen"}
    linkedin_friends = {"charlie", "diana", "frank", "grace", "luke", "mary"}

    # 1. Friends who are on ALL four platforms (intersection)
    all_platforms = facebook_friends & instagram_friends & twitter_friends & linkedin_friends

    # 2. Friends who are ONLY on Facebook (difference)
    facebook_only = facebook_friends - (instagram_friends | twitter_friends | linkedin_friends)

    # 3. Friends who are on Instagram OR Twitter but NOT on both (symmetric difference)
    instagram_xor_twitter = instagram_friends ^ twitter_friends

    # 4. Total unique friends across all platforms (union)
    total_unique = facebook_friends | instagram_friends | twitter_friends | linkedin_friends

    # 5. Friends who are on exactly 2 platforms
    # Count appearances across platforms
    all_sets = [facebook_friends, instagram_friends, twitter_friends, linkedin_friends]
    friend_count = {}
    for s in all_sets:
        for name in s:
            friend_count[name] = friend_count.get(name, 0) + 1
    exactly_two_platforms = {name for name, count in friend_count.items() if count == 2}

    # Return results
    return {
        "all_platforms": all_platforms,
        "facebook_only": facebook_only,
        "instagram_xor_twitter": instagram_xor_twitter,
        "total_unique": total_unique,
        "exactly_two_platforms": exactly_two_platforms
    }

# Test the function
result = analyze_friendships()
print("All platforms:", result.get('all_platforms'))
print("Facebook only:", result.get('facebook_only'))
print("Instagram XOR Twitter:", result.get('instagram_xor_twitter'))
print("Total unique friends:", result.get('total_unique'))
print("Exactly 2 platforms:", result.get('exactly_two_platforms'))
