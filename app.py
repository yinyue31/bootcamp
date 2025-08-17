from flask import Flask, render_template, request, jsonify
import numpy as np
import scipy.stats as stats
import pandas as pd
import json
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/distributions')
def distributions():
    return render_template('distributions.html')

@app.route('/hypothesis_testing')
def hypothesis_testing():
    return render_template('hypothesis_testing.html')

@app.route('/correlation')
def correlation():
    return render_template('correlation.html')

@app.route('/api/generate_distribution', methods=['POST'])
def generate_distribution():
    data = request.json
    dist_type = data['type']
    params = data['params']
    
    samples = None
    theoretical = None
    pdf = None
    
    if dist_type == 'normal':
        samples = np.random.normal(params['mean'], params['std'], 1000)
        theoretical = np.linspace(samples.min(), samples.max(), 100)
        pdf = stats.norm.pdf(theoretical, params['mean'], params['std'])
    elif dist_type == 'exponential':
        samples = np.random.exponential(params['lambda'], 1000)
        theoretical = np.linspace(0, samples.max(), 100)
        pdf = stats.expon.pdf(theoretical, scale=1/params['lambda'])
    elif dist_type == 'binomial':
        samples = np.random.binomial(params['n'], params['p'], 1000)
        theoretical = np.arange(0, params['n'] + 1)
        pmf = stats.binom.pmf(theoretical, params['n'], params['p'])
        return jsonify({
            'samples': samples.tolist(),
            'theoretical': theoretical.tolist(),
            'pmf': pmf.tolist(),
            'type': 'discrete'
        })
    
    return jsonify({
        'samples': samples.tolist(),
        'theoretical': theoretical.tolist(),
        'pdf': pdf.tolist(),
        'type': 'continuous'
    })

@app.route('/api/hypothesis_test', methods=['POST'])
def hypothesis_test():
    data = request.json
    sample_data = np.array(data['sample_data'])
    test_type = data['test_type']
    null_value = data['null_value']
    alpha = data['alpha']
    
    test_name = ""
    test_statistic = 0
    p_value = 0
    critical_value = 0
    
    if test_type == 't_test':
        t_stat, p_value = stats.ttest_1samp(sample_data, null_value)
        critical_value = stats.t.ppf(1 - alpha/2, len(sample_data) - 1)
        test_name = "One-Sample t-Test"
        test_statistic = t_stat
    elif test_type == 'z_test':
        z_stat = (np.mean(sample_data) - null_value) / (np.std(sample_data, ddof=1) / np.sqrt(len(sample_data)))
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        critical_value = stats.norm.ppf(1 - alpha/2)
        test_name = "One-Sample Z-Test"
        test_statistic = z_stat
    
    result = {
        'test_name': test_name,
        'test_statistic': float(test_statistic),
        'p_value': float(p_value),
        'critical_value': float(critical_value),
        'alpha': alpha,
        'reject_null': p_value < alpha,
        'sample_mean': float(np.mean(sample_data)),
        'sample_std': float(np.std(sample_data, ddof=1)),
        'sample_size': len(sample_data)
    }
    
    return jsonify(result)

@app.route('/api/generate_correlation_data', methods=['POST'])
def generate_correlation_data():
    data = request.json
    correlation = data['correlation']
    n_points = data['n_points']
    
    # Generate correlated data
    np.random.seed(42)
    x = np.random.normal(0, 1, n_points)
    noise = np.random.normal(0, 0.3, n_points)
    y = correlation * x + np.sqrt(1 - correlation**2) * noise
    
    # Calculate actual correlation
    actual_corr = np.corrcoef(x, y)[0, 1]
    
    return jsonify({
        'x': x.tolist(),
        'y': y.tolist(),
        'actual_correlation': float(actual_corr)
    })

if __name__ == '__main__':
    app.run(debug=True)
