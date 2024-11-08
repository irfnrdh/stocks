import pandas as pd
import numpy as np

class FundamentalAnalysis:
    def __init__(self, financial_data):
        """
        Inisialisasi kelas dengan data keuangan perusahaan
        
        :param financial_data: DataFrame berisi data keuangan perusahaan
        """
        self.data = financial_data
    
    def calculate_financial_ratios(self):
        """
        Menghitung rasio-rasio keuangan kunci
        
        :return: Dictionary berisi rasio-rasio keuangan
        """
        ratios = {
            'current_ratio': self.data['total_current_assets'] / self.data['total_current_liabilities'],
            'debt_to_equity': self.data['total_liabilities'] / self.data['total_shareholders_equity'],
            'return_on_equity': self.data['net_income'] / self.data['total_shareholders_equity'] * 100,
            'return_on_assets': self.data['net_income'] / self.data['total_assets'] * 100,
            'gross_margin': (self.data['revenue'] - self.data['cost_of_goods_sold']) / self.data['revenue'] * 100,
            'net_profit_margin': self.data['net_income'] / self.data['revenue'] * 100
        }
        return ratios
    
    def evaluate_financial_health(self, ratios):
        """
        Mengevaluasi kesehatan keuangan berdasarkan rasio
        
        :param ratios: Dictionary rasio keuangan
        :return: Dictionary penilaian kesehatan keuangan
        """
        health_assessment = {
            'current_ratio': 'Baik' if ratios['current_ratio'] > 1.5 else 'Perlu Perhatian',
            'debt_to_equity': 'Baik' if ratios['debt_to_equity'] < 1 else 'Berisiko',
            'return_on_equity': 'Sangat Baik' if ratios['return_on_equity'] > 15 else 
                                'Baik' if ratios['return_on_equity'] > 10 else 'Perlu Perbaikan',
            'return_on_assets': 'Sangat Baik' if ratios['return_on_assets'] > 10 else 
                                'Baik' if ratios['return_on_assets'] > 5 else 'Perlu Perbaikan',
            'gross_margin': 'Sangat Baik' if ratios['gross_margin'] > 50 else 
                            'Baik' if ratios['gross_margin'] > 30 else 'Perlu Perhatian',
            'net_profit_margin': 'Sangat Baik' if ratios['net_profit_margin'] > 20 else 
                                 'Baik' if ratios['net_profit_margin'] > 10 else 'Perlu Perbaikan'
        }
        return health_assessment
    
    def calculate_intrinsic_value(self, growth_rate=0.05, required_rate_of_return=0.1):
        """
        Menghitung nilai intrinsik saham menggunakan model Dividend Discount Model (DDM)
        
        :param growth_rate: Proyeksi tingkat pertumbuhan dividen (default 5%)
        :param required_rate_of_return: Tingkat pengembalian yang diharapkan (default 10%)
        :return: Estimasi nilai intrinsik saham
        """
        last_dividend = self.data['dividend_per_share'].iloc[-1]
        intrinsic_value = last_dividend * (1 + growth_rate) / (required_rate_of_return - growth_rate)
        return intrinsic_value
    
    def generate_investment_recommendation(self, current_price, intrinsic_value, health_assessment):
        """
        Menghasilkan rekomendasi investasi
        
        :param current_price: Harga saham saat ini
        :param intrinsic_value: Nilai intrinsik saham
        :param health_assessment: Penilaian kesehatan keuangan
        :return: Rekomendasi investasi
        """
        # Hitung margin of safety
        margin_of_safety = (intrinsic_value - current_price) / intrinsic_value * 100
        
        # Evaluasi kesehatan keuangan
        financial_health_score = sum([
            1 if assessment == 'Sangat Baik' else 
            0.5 if assessment == 'Baik' else 
            0 for assessment in health_assessment.values()
        ]) / len(health_assessment)
        
        # Tentukan rekomendasi
        if margin_of_safety > 20 and financial_health_score > 0.7:
            return 'BELI'
        elif margin_of_safety > 10 and financial_health_score > 0.5:
            return 'TAHAN'
        else:
            return 'JUAL'

# Contoh penggunaan
def main():
    # Contoh data keuangan (dalam praktiknya, data ini diambil dari laporan keuangan)
    financial_data = pd.DataFrame({
        'total_current_assets': [1000000],
        'total_current_liabilities': [500000],
        'total_liabilities': [800000],
        'total_shareholders_equity': [1200000],
        'net_income': [200000],
        'total_assets': [2000000],
        'revenue': [5000000],
        'cost_of_goods_sold': [3000000],
        'dividend_per_share': [5]
    })
    
    # Inisialisasi analisis fundamental
    analysis = FundamentalAnalysis(financial_data)
    
    # Hitung rasio keuangan
    ratios = analysis.calculate_financial_ratios()
    
    # Evaluasi kesehatan keuangan
    health_assessment = analysis.evaluate_financial_health(ratios)
    
    # Hitung nilai intrinsik
    intrinsic_value = analysis.calculate_intrinsic_value()
    
    # Dapatkan rekomendasi investasi
    recommendation = analysis.generate_investment_recommendation(
        current_price=100,  # Misalkan harga saham saat ini
        intrinsic_value=intrinsic_value,
        health_assessment=health_assessment
    )
    
    print("Rasio Keuangan:", ratios)
    print("Penilaian Kesehatan:", health_assessment)
    print("Nilai Intrinsik:", intrinsic_value)
    print("Rekomendasi:", recommendation)

if __name__ == "__main__":
    main()
