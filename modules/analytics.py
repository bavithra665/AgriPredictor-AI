from datetime import datetime, timedelta

class AnalyticsEngine:
    @staticmethod
    def get_crop_comparison_data(predictions=None):
        """
        Returns dynamic crop comparison data based on user's prediction history.
        If no history, returns default curated data for demo purposes.
        """
        base_data = {
            'Rice': {'profit': 80, 'water': 95, 'risk': 40},
            'Wheat': {'profit': 70, 'water': 60, 'risk': 30},
            'Maize': {'profit': 65, 'water': 50, 'risk': 45},
            'Millets': {'profit': 55, 'water': 20, 'risk': 10},
            'Cotton': {'profit': 90, 'water': 70, 'risk': 60},
            'Pulses': {'profit': 75, 'water': 30, 'risk': 25},
            'Jute': {'profit': 60, 'water': 85, 'risk': 50},
            'Coffee': {'profit': 85, 'water': 65, 'risk': 35}
        }
        
        # If no user predictions, return empty to keep chart blank as requested
        if not predictions:
            return {}
            
        # If user has predictions, filter to show only crops they have predicted
        # We now collect crop1, crop2, and crop3 to show the full range of recommendations
        user_crops = set()
        for p in predictions:
            if p.crop1: user_crops.add(p.crop1)
            if p.crop2: user_crops.add(p.crop2)
            if p.crop3: user_crops.add(p.crop3)
        
        # Build dataset dynamically: 
        # 1. Use predefined data if available
        # 2. Use reasonable defaults if the crop is new to our analytics engine
        filtered_data = {}
        for crop_name in user_crops:
            if crop_name in base_data:
                filtered_data[crop_name] = base_data[crop_name]
            else:
                # Fallback for crops not in our curated list (e.g., Apple, Mango)
                # We give them 'average' stats so they at least appear on the chart
                filtered_data[crop_name] = {'profit': 60, 'water': 50, 'risk': 20}
        
        return filtered_data

    @staticmethod
    def process_prediction_history(predictions):
        """
        Aggregates prediction history for charts.
        """
        if not predictions:
            return {'labels': [], 'counts': []}
            
        crop_counts = {}
        for pred in predictions:
            # We count all top 3 recommendations as "relevant" to the user
            if pred.crop1: crop_counts[pred.crop1] = crop_counts.get(pred.crop1, 0) + 1
            if pred.crop2: crop_counts[pred.crop2] = crop_counts.get(pred.crop2, 0) + 0.6 # Weighted less
            if pred.crop3: crop_counts[pred.crop3] = crop_counts.get(pred.crop3, 0) + 0.3 # Weighted even less
        
        return {
            'labels': list(crop_counts.keys()),
            'counts': list(crop_counts.values())
        }
        
    @staticmethod
    def get_trend_data(predictions):
        """
        Simulates trend data based on history.
        """
        # Group by date
        history = {}
        for pred in predictions:
            date_str = pred.created_at.strftime('%Y-%m-%d')
            history[date_str] = history.get(date_str, 0) + 1
            
        sorted_dates = sorted(history.keys())
        return {
            'labels': sorted_dates[-7:], # last 7 days of activity
            'values': [history[d] for d in sorted_dates[-7:]]
        }
