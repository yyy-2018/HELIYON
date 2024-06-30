# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 07:50:44 2024

@author: 14125
"""

# random_forest_predictor.py

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

class RandomForestPredictor:
    def __init__(self, box_fluctuation_range=2, ellipse_fluctuation_std=0.5, num_samples=100):
        self.box_fluctuation_range = box_fluctuation_range
        self.ellipse_fluctuation_std = ellipse_fluctuation_std
        self.num_samples = num_samples
        self.rf_models_box = []
        self.rf_models_ellipse = []

    def generate_random_fluctuations(self, num_samples, mode='box'):
        if mode == 'box':
            fluctuations = np.random.uniform(-self.box_fluctuation_range, self.box_fluctuation_range, num_samples)
        elif mode == 'ellipse':
            fluctuations = np.random.normal(0, self.ellipse_fluctuation_std, num_samples)
        return fluctuations

    def train_models(self, fixed_values):
        # 确保模型列表为空
        self.rf_models_box = []
        self.rf_models_ellipse = []

        for fixed_value in fixed_values:
            # 生成数据
            fluctuations_box = self.generate_random_fluctuations(self.num_samples, mode='box').reshape(-1, 1)
            fluctuations_ellipse = self.generate_random_fluctuations(self.num_samples, mode='ellipse').reshape(-1, 1)
            
            # 目标值为固定值加波动值
            targets_box = fixed_value + fluctuations_box
            targets_ellipse = fixed_value + fluctuations_ellipse

            # 初始化随机森林模型
            rf_model_box = RandomForestRegressor(n_estimators=10, random_state=42)
            rf_model_ellipse = RandomForestRegressor(n_estimators=10, random_state=42)

            # 训练模型
            rf_model_box.fit(fluctuations_box, targets_box)
            rf_model_ellipse.fit(fluctuations_ellipse, targets_ellipse)

            # 保存模型
            self.rf_models_box.append(rf_model_box)
            self.rf_models_ellipse.append(rf_model_ellipse)

    def predict(self, fluctuation_values, mode='box'):
        predictions = []
        models = self.rf_models_box if mode == 'box' else self.rf_models_ellipse

        for model, fluctuation_value in zip(models, fluctuation_values):
            predicted_value = model.predict([[fluctuation_value]])
            predictions.append(predicted_value[0])

        return predictions

    def visualize(self, fixed_values):
        for fixed_value in fixed_values:
            fluctuations_box = self.generate_random_fluctuations(self.num_samples, mode='box').reshape(-1, 1)
            fluctuations_ellipse = self.generate_random_fluctuations(self.num_samples, mode='ellipse').reshape(-1, 1)
            targets_box = fixed_value + fluctuations_box
            targets_ellipse = fixed_value + fluctuations_ellipse

            plt.scatter(fluctuations_box, targets_box, label=f'Box Random Data (Fixed value: {fixed_value})')
            plt.scatter(fluctuations_ellipse, targets_ellipse, label=f'Ellipse Random Data (Fixed value: {fixed_value})')

        plt.xlabel('Fluctuation')
        plt.ylabel('Target (Fixed value + Fluctuation)')
        plt.title('Random Data')
        plt.legend()
        plt.show()
