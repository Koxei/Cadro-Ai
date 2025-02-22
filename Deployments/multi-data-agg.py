import requests
import time

class SocialScraper:
    def __init__(self, api_endpoints, rate_limit=1):
        """
        Initializes the Social Scraper with given API endpoints and rate limit.
        """
        self.api_endpoints = api_endpoints
        self.rate_limit = rate_limit  # Requests per second
    
    def fetch_data(self, platform):
        """
        Fetches data from the specified platform's API endpoint.
        """
        if platform not in self.api_endpoints:
            raise ValueError(f"Unknown platform: {platform}")
        
        url = self.api_endpoints[platform]
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data from {platform}, status code: {response.status_code}"}
    
    def aggregate_data(self):
        """
        Aggregates data from all platforms while respecting rate limits.
        """
        aggregated_results = {}
        for platform in self.api_endpoints:
            aggregated_results[platform] = self.fetch_data(platform)
            time.sleep(1 / self.rate_limit)  # Respect rate limit
        return aggregated_results

# Example Usage
if __name__ == "__main__":
    api_endpoints = {
        "twitter": "https://api.twitter.com/example-endpoint",
        "reddit": "https://www.reddit.com/example-endpoint.json"
    }
    scraper = SocialScraper(api_endpoints, rate_limit=2)
    data = scraper.aggregate_data()
    print(data)
