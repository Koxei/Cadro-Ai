async def calculate_liquidity_impact(
    self,
    pool_data: Dict,
    volume: float,
    timeframe: int
) -> float:
    """Calculate market impact of liquidity changes.
    
    Args:
        pool_data: Current pool state
        volume: Transaction volume
        timeframe: Analysis timeframe in seconds
        
    Returns:
        Impact score between 0 and 1
    """
    try:
        # Calculate liquidity depth
        depth = await self._calculate_pool_depth(pool_data)
        
        # Normalize volume against pool depth
        volume_impact = min(1.0, volume / depth)
        
        # Calculate temporal factors
        temporal_impact = self._calculate_temporal_impact(
            pool_data['history'],
            timeframe
        )
        
        # Combined impact score with weights
        impact_score = (
            volume_impact * 0.7 +
            temporal_impact * 0.3
        )
        
        return float(impact_score)
        
    except Exception as e:
        logger.error(f"Error calculating liquidity impact: {e}")
        return 1.0  # Maximum impact on error
