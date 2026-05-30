class EffectivenessKPIs:
    """
    KPI-driven framework to measure the effectiveness of corporate actions.
    """
    
    @staticmethod
    def get_kpi_metrics():
        return {
            "Tracking Error": "Difference between forecasted prices and actual market prices to measure model accuracy.",
            "Cost Savings": "Total dollar amount saved by executing hedges or forward contracts compared to spot market rates.",
            "Variance Analysis": "Periodic review of actual vs. budgeted procurement costs to identify leakage.",
            "A/B Supply Chain Testing": "Comparing procurement costs between a traditional single-source chain and a diversified chain."
        }

    @staticmethod
    def get_measurement_protocol():
        protocol = """
        MEASUREMENT FRAMEWORK
        ---------------------
        1. Monthly Audit: Review procurement invoices against the 12-month forecast.
        2. Quarterly Review: Evaluate the ROI of hedging premiums paid vs. price protection gained.
        3. Annual Assessment: Recalibrate supply chain weights based on regional price performance.
        """
        return protocol

if __name__ == "__main__":
    kpis = EffectivenessKPIs()
    print(kpis.get_measurement_protocol())
    for kpi, desc in kpis.get_kpi_metrics().items():
        print(f"- {kpi}: {desc}")
