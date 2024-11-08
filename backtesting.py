import numpy as np
import pandas as pd
import scipy.stats as stats
from typing import Dict, List, Any
import matplotlib.pyplot as plt

class ComprehensiveBacktestingFramework:
    def __init__(self, strategy, data_source, config):
        """
        Inisialisasi framework backtesting komprehensif
        
        Parameters:
        - strategy: Objek strategi trading
        - data_source: Sumber data historis
        - config: Konfigurasi backtesting
        """
        self.strategy = strategy
        self.data = data_source
        self.config = config
        
        # Komponen Analisis
        self.performance_metrics = {}
        self.risk_analysis = {}
        self.transaction_costs = {}
        self.model_limitations = {}
    
    class WalkForwardAnalysis:
        def __init__(self, data, window_size, forecast_horizon):
            self.data = data
            self.window_size = window_size
            self.forecast_horizon = forecast_horizon
        
        def generate_walk_forward_splits(self):
            """
            Membuat split data untuk Walk Forward Analysis
            """
            for start in range(0, len(self.data) - self.window_size, self.forecast_horizon):
                train_start = start
                train_end = start + self.window_size
                test_start = train_end
                test_end = test_start + self.forecast_horizon
                
                train_data = self.data.iloc[train_start:train_end]
                test_data = self.data.iloc[test_start:test_end]
                
                yield train_data, test_data
    
    class MonteCarloSimulation:
        def __init__(self, returns):
            self.returns = returns
        
        def simulate(self, num_simulations=10000, num_periods=252):
            """
            Simulasi Monte Carlo untuk estimasi distribusi return
            
            Parameters:
            - num_simulations: Jumlah simulasi
            - num_periods: Periode simulasi (default: 1 tahun trading)
            """
            # Parameter distribusi return
            mu = np.mean(self.returns)
            sigma = np.std(self.returns)
            
            # Simulasi return
            simulations = np.random.normal(
                mu, 
                sigma, 
                (num_simulations, num_periods)
            )
            
            # Akumulasi return
            portfolio_values = np.cumprod(1 + simulations, axis=1)
            
            return {
                'simulations': simulations,
                'portfolio_values': portfolio_values,
                'confidence_intervals': self.calculate_confidence_intervals(portfolio_values)
            }
        
        def calculate_confidence_intervals(self, portfolio_values):
            """
            Hitung interval kepercayaan dari simulasi
            """
            return {
                '95%': np.percentile(portfolio_values, [2.5, 97.5], axis=0),
                '99%': np.percentile(portfolio_values, [0.5, 99.5], axis=0)
            }
    
    class RiskDecomposition:
        def __init__(self, returns, benchmark_returns):
            self.returns = returns
            self.benchmark_returns = benchmark_returns
        
        def decompose_risk(self):
            """
            Analisis dekomposisi risiko multi-faktor
            """
            return {
                'market_risk': self.calculate_beta(),
                'specific_risk': self.calculate_specific_risk(),
                'total_risk': self.calculate_total_risk(),
                'risk_contribution': self.calculate_risk_contribution()
            }
        
        def calculate_beta(self):
            """Hitung sensitivitas terhadap pasar"""
            covariance = np.cov(self.returns, self.benchmark_returns)[0, 1]
            benchmark_variance = np.var(self.benchmark_returns)
            return covariance / benchmark_variance
        
        def calculate_specific_risk(self):
            """Hitung risiko spesifik"""
            market_component = self.calculate_beta() * self.benchmark_returns
            return self.returns - market_component
        
        def calculate_total_risk(self):
            """Hitung total risiko"""
            return np.std(self.returns)
        
        def calculate_risk_contribution(self):
            """Analisis kontribusi risiko"""
            weights = np.ones(len(self.returns)) / len(self.returns)
            portfolio_volatility = np.std(self.returns)
            
            risk_contributions = weights * self.returns / portfolio_volatility
            return risk_contributions
    
    class StatisticalValidator:
        def __init__(self, returns):
            self.returns = returns
        
        def normality_tests(self):
            """Uji normalitas distribusi return"""
            return {
                'shapiro_wilk': stats.shapiro(self.returns),
                'jarque_bera': stats.jarque_bera(self.returns),
                'anderson': stats.anderson(self.returns)
            }
        
        def independence_tests(self):
            """Uji independensi return"""
            return {
                'ljung_box': stats.diagnostic.acorr_ljungbox(self.returns),
                'runs_test': stats.runs_test(self.returns)
            }
        
        def correlation_analysis(self):
            """Analisis korelasi"""
            return np.corrcoef(self.returns)
    
    class TransactionCostModeler:
        def __init__(self, broker_config):
            self.broker_config = broker_config
        
        def estimate_transaction_costs(self, trades):
            """
            Estimasi biaya transaksi secara komprehensif
            
            Parameters:
            - trades: DataFrame berisi detail transaksi
            """
            costs = {
                'spread_cost': self.calculate_spread_cost(trades),
                'commission': self.calculate_commission(trades),
                'slippage': self.estimate_slippage(trades),
                'market_impact': self.calculate_market_impact(trades)
            }
            
            total_trade_volume = trades['volume'].sum()
            total_cost = sum(costs.values())
            
            return {
                'detailed_costs': costs,
                'total_cost_percentage': total_cost / total_trade_volume
            }
        
        def calculate_spread_cost(self, trades):
            """Hitung biaya spread"""
            return trades['spread'] * trades['volume']
        
        def calculate_commission(self, trades):
            """Hitung komisi"""
            return trades['volume'] * self.broker_config['commission_rate']
        
        def estimate_slippage(self, trades):
            """Estimasi biaya slippage"""
            return trades['volume'] * self.broker_config['slippage_rate']
        
        def calculate_market_impact(self, trades):
            """Hitung dampak pasar dari transaksi besar"""
            return trades['volume'] * self.broker_config['market_impact_rate']
    
    def run_comprehensive_backtest(self):
        """
        Jalankan backtesting komprehensif
        """
        # 1. Walk Forward Analysis
        walk_forward_analysis = self.WalkForwardAnalysis(
            self.data, 
            window_size=self.config['window_size'], 
            forecast_horizon=self.config['forecast_horizon']
        )
        
        walk_forward_results = []
        for train_data, test_data in walk_forward_analysis.generate_walk_forward_splits():
            # Latih ulang model
            self.strategy.train(train_data)
            
            # Simulasi trading
            period_results = self.strategy.simulate(test_data)
            walk_forward_results.append(period_results)
        
        # 2. Monte Carlo Simulation
        monte_carlo = self.MonteCarloSimulation(self.strategy.returns)
        mc_results = monte_carlo.simulate()
        
        # 3. Risk Decomposition
        risk_decomposer = self.RiskDecomposition(
            self.strategy.returns, 
            self.config['benchmark_returns']
        )
        risk_analysis = risk_decomposer.decompose_risk()
        
        # 4. Statistical Validation
        stat_validator = self.StatisticalValidator(self.strategy.returns)
        statistical_tests = {
            'normality': stat_validator.normality_tests(),
            'independence': stat_validator.independence_tests(),
            'correlation': stat_validator.correlation_analysis()
        }
        
        # 5. Transaction Cost Analysis
        cost_modeler = self.TransactionCostModeler(self.config['broker_config'])
        transaction_costs = cost_modeler.estimate_transaction_costs(self.strategy.trades)
        
        # Kompilasi hasil
        comprehensive_results = {
            'walk_forward_results': walk_forward_results,
            'monte_carlo_simulation': mc_results,
            'risk_analysis': risk_analysis,
            'statistical_validation': statistical_tests,
            'transaction_costs': transaction_costs
        }
        
        return comprehensive_results
    
    def visualize_results(self, results):
        """
        Visualisasi hasil backtesting
        """
        plt.figure(figsize=(15, 10))
        
        # Plot Monte Carlo Simulation
        plt.subplot(2, 2, 1)
        plt.title('Monte Carlo Portfolio Simulation')
        plt.plot(results['monte_carlo_simulation']['portfolio_values'][:100].T)
        plt.xlabel('Trading Periods')
        plt.ylabel('Portfolio Value')
        
        # Plot Risk Contribution
        plt.subplot(2, 2, 2)
        plt.title('Risk Contribution')
        plt.bar(
            range(len(results['risk_analysis']['risk_contribution'])), 
            results['risk_analysis']['risk_contribution']
        )
        plt.xlabel('Assets')
        plt.ylabel('Risk Contribution')
        
        # Plot Transaction Costs
        plt.subplot(2, 2, 3)
        costs = results['transaction_costs']['detailed_costs']
        plt.title('Transaction Costs Breakdown')
        plt.pie(costs.values(), labels=costs.keys(), autopct='%1.1f%%')
        
        plt.tight_layout()
        plt.show()

# Contoh penggunaan
def main():
    # Konfigurasi dummy
    config = {
        'window_size': 252,  # 1 tahun
        'forecast_horizon': 21,  # 1 bulan
        'benchmark_returns': np.random.normal(0.05, 0.2, 252),
        'broker_config': {
            'commission_rate': 0.001,
            'slippage_rate': 0.0005,
            'market_impact_rate': 0.0001
        }
    }
    
    # Inisialisasi framework
    backtest_framework = ComprehensiveBacktestingFramework(
        strategy=your_trading_strategy,
        data_source=historical_market_data,
        config=config
    )
    
    # Jalankan backtesting
    results = backtest_framework.run_comprehensive_backtest()
    
    # Visualisasi
    backtest_framework.visualize_results(results)

if __name__ == "__main__":
    main()
