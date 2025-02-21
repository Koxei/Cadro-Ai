class RateLimiter:
    def __init__(self, rate_limit: int = 100, window: int = 60):
        self.rate_limit = rate_limit
        self.window = window
        self.requests = defaultdict(list)
        
    async def is_allowed(self, key: str) -> bool:
        """Check if request is allowed under rate limit."""
