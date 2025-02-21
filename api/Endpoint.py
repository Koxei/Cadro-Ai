GET /api/v1/token/{token_address}/analysis:
    description: Get comprehensive token analysis
    parameters:
        - token_address: Solana token address
        - timeframe: Analysis timeframe (1h, 24h, 7d)
    response:
        risk_score: float
        anomalies: List[AnomalyEvent]
        metrics: Dict[str, float]

POST /api/v1/monitor:
    description: Start token monitoring
    body:
        token_addresses: List[str]
        update_interval: int (seconds)
    response:
        status: str
        monitoring_ids: List[str]

GET /api/v1/anomalies:
    description: Retrieve detected anomalies
    parameters:
        - start_time: datetime
        - end_time: datetime
        - min_risk_score: float
    response:
        anomalies: List[AnomalyEvent]
