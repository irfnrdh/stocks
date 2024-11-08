# Jangan Percaya 100% ya ini sekedar ngulik.

import pandas as pd
import numpy as np
import yfinance as yf
from typing import List, Dict, Any

class MultibaggerScreener:
    def __init__(self, stocks: List[str], years: int = 5):
        """
        Inisialisasi screener saham multibagger
        
        :param stocks: Daftar kode saham yang akan dianalisis
        :param years: Periode analisis historis
        """
        self.stocks = stocks
        self.years = years
        self.results = []
    
    def fetch_financial_data(self, stock: str) -> Dict[str, Any]:
        """
        Mengambil data keuangan dan historis saham
        
        :param stock: Kode saham
        :return: Dictionary berisi data keuangan dan historis
        """
        try:
            # Ambil data historis
            stock_data = yf.Ticker(f"{stock}.JK")  # Untuk pasar Indonesia
            
            # Ambil laporan keuangan
            financials = stock_data.financials
            balance_sheet = stock_data.balance_sheet
            
            # Ambil data historis harga
            hist_data = stock_data.history(period=f"{self.years}y")
            
            return {
                'ticker': stock,
                'financials': financials,
                'balance_sheet': balance_sheet,
                'historical_price': hist_data
            }
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
            return None
    
    def calculate_growth_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Menghitung metrik pertumbuhan untuk evaluasi multibagger
        
        :param data: Data keuangan saham
        :return: Dictionary metrik pertumbuhan
        """
        if not data or 'historical_price' not in data:
            return None
        
        try:
            # Analisis pertumbuhan harga
            hist_price = data['historical_price']['Close']
            
            # Hitung CAGR (Compound Annual Growth Rate)
            start_price = hist_price.iloc[0]
            end_price = hist_price.iloc[-1]
            years = len(hist_price) / 252  # Asumsi 252 trading days per tahun
            
            cagr = (end_price / start_price) ** (1/years) - 1
            
            # Analisis pertumbuhan fundamental
            financials = data['financials']
            revenue_growth = self._calculate_growth_rate(financials.loc['Total Revenue'])
            net_income_growth = self._calculate_growth_rate(financials.loc['Net Income'])
            
            # Return on Equity (ROE)
            total_equity = data['balance_sheet'].loc['Total Stockholder Equity']
            net_income = financials.loc['Net Income']
            
            avg_roe = np.mean([
                (net_income.iloc[i] / total_equity.iloc[i]) * 100 
                for i in range(min(len(net_income), len(total_equity)))
            ])
            
            return {
                'ticker': data['ticker'],
                'price_cagr': cagr * 100,
                'revenue_growth': revenue_growth,
                'net_income_growth': net_income_growth,
                'avg_roe': avg_roe
            }
        except Exception as e:
            print(f"Error calculating metrics for {data['ticker']}: {e}")
            return None
    
    def _calculate_growth_rate(self, series: pd.Series) -> float:
        """
        Menghitung tingkat pertumbuhan rata-rata
        
        :param series: Series data keuangan
        :return: Pertumbuhan rata-rata
        """
        try:
            growth_rates = [(series.iloc[i] / series.iloc[i+1]) - 1 for i in range(len(series)-1)]
            return np.mean(growth_rates) * 100
        except:
            return 0
    
    def apply_multibagger_criteria(self, metrics: Dict[str, float]) -> bool:
        """
        Menerapkan kriteria saham multibagger
        
        :param metrics: Metrik pertumbuhan saham
        :return: Boolean apakah saham memenuhi kriteria
        """
        if not metrics:
            return False
        
        # Kriteria multibagger:
        # 1. CAGR harga > 25%
        # 2. Pertumbuhan pendapatan > 15%
        # 3. Pertumbuhan laba bersih > 15%
        # 4. ROE > 15%
        # 5. Tidak memiliki utang berlebihan
        criteria_met = (
            metrics['price_cagr'] > 25 and
            metrics['revenue_growth'] > 15 and
            metrics['net_income_growth'] > 15 and
            metrics['avg_roe'] > 15
        )
        
        return criteria_met
    
    def screen_multibagger_stocks(self) -> List[Dict[str, Any]]:
        """
        Melakukan screening saham multibagger
        
        :return: Daftar saham potensial multibagger
        """
        for stock in self.stocks:
            try:
                # Ambil data keuangan
                financial_data = self.fetch_financial_data(stock)
                
                # Hitung metrik pertumbuhan
                growth_metrics = self.calculate_growth_metrics(financial_data)
                
                # Evaluasi kriteria multibagger
                if self.apply_multibagger_criteria(growth_metrics):
                    self.results.append(growth_metrics)
            
            except Exception as e:
                print(f"Error processing {stock}: {e}")
        
        # Urutkan hasil berdasarkan CAGR harga
        return sorted(self.results, key=lambda x: x['price_cagr'], reverse=True)

def main():
    # Daftar saham yang akan dianalisis (contoh saham Indonesia)
    stock_list = [
        'BMRI', 'BBCA', 'BBRI', 'TLKM', 'UNVR', 
        'ASII', 'SIDO', 'EXCL', 'INDF', 'GGRM'
    ]
    
    # Inisialisasi screener
    screener = MultibaggerScreener(stock_list, years=5)
    
    # Jalankan screening
    multibagger_candidates = screener.screen_multibagger_stocks()
    
    # Tampilkan hasil
    print("Kandidat Saham Multibagger:")
    for stock in multibagger_candidates:
        print(f"""
Ticker: {stock['ticker']}
CAGR Harga: {stock['price_cagr']:.2f}%
Pertumbuhan Pendapatan: {stock['revenue_growth']:.2f}%
Pertumbuhan Laba Bersih: {stock['net_income_growth']:.2f}%
Rata-rata ROE: {stock['avg_roe']:.2f}%
        """)

if __name__ == "__main__":
    main()
