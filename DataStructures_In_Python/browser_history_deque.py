from collections import deque

# ---- Initialize ----
history = deque(maxlen=5)      # Browser history with max size 5
forward_stack = deque()        # Stack for forward navigation

# ---- Functions ----
def add_page(url):
    """Add a new page to history, clear forward stack."""
    history.append(url)
    forward_stack.clear()  # Forward history is cleared on new navigation
    print(f"Visited: {url}")
    show_state()

def go_back():
    """Go back: pop from history, push to forward_stack."""
    if len(history) > 1:  # Keep at least one page in history
        page = history.pop()
        forward_stack.append(page)
        print(f"Back to: {history[-1]}")
    else:
        print("No previous page to go back to.")
    show_state()

def go_forward():
    """Go forward: pop from forward_stack, push to history."""
    if forward_stack:
        page = forward_stack.pop()
        history.append(page)
        print(f"Forward to: {page}")
    else:
        print("No forward page available.")
    show_state()

def show_state():
    """Display current state of history and forward stack."""
    print(f"History: {list(history)}")
    print(f"Forward: {list(forward_stack)}\n")

# ---- Demo Usage ----
add_page("google.com")
add_page("github.com")
add_page("stackoverflow.com")
add_page("python.org")
add_page("wikipedia.org")
add_page("reddit.com")      # This will push out the oldest (google.com)

go_back()                  # Back to wikipedia.org
go_back()                  # Back to python.org
go_forward()               # Forward to wikipedia.org
add_page("openai.com")     # Forward stack is cleared after new navigation
