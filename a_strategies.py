    
class StrategySettings():
    strategy_notes = [  
        # ///
        # ("volf_stoch", {                              # Ключ - название стратегии, можно любой например с суфиксами (volf_stoch1)
        #     "LONG": {
        #         "entry_conditions": {
        #             "rules": {
        #                 'TREND_EMA': {
        #                     'enable': False,            # True/False -- использовать/не s
        #                     'tfr': "1m",
        #                     'period1': 2,
        #                     'period2': 301,
        #                     'is_trend': 1,             # 1 -- trend, -1 -- antyTrend
        #                     'col_name': 'Close',
        #                     "ind_name": 'TREND_EMA'
        #                 },  # 
        #                 'STOCHRSI': {
        #                     'enable': True,    # True/False -- использовать/не использовать
        #                     'tfr': "15m",
        #                     'period': 14, 
        #                     'k': 3,
        #                     'd': 3,
        #                     'over_sell': 35,
        #                     'over_buy': 65,  
        #                     "ind_name": "STOCHRSI"  
        #                 },   
        #                 'VOLF': {
        #                     'enable': True,    # True/False -- использовать/не использовать
        #                     'tfr': "5m",
        #                     "mode": "a",               # r --- rolling/ a --- absoluted
        #                     'period': 14,
        #                     'a': {
        #                         'slice_factor': 1.6,
        #                     },
        #                     'r': {
        #                         'slice_factor': 2.1,
        #                     },
        #                     "ind_name": "VOLF"
        #                 },                  
        #             },     
        #             "is_close_bar": False,             # Дожидаться закрытия бара                
        #             "grid_orders": [
        #                 {'indent': 0.0, 'volume': 100, 'signal': True},
        #                 # {'indent': -10.0, 'volume': 25, 'signal': False}, # %
        #                 # {'indent': -20.0, 'volume': 25, 'signal': False},
        #                 # {'indent': -30.0, 'volume': 25, 'signal': False}, # %
        #             ],                          
        #         },

        #         "exit_conditions": {                              
        #             "close_by_signal": {
        #                 "is_active": False,    # Закрытие по сигналу
        #                 "min_profit": 0.6,   # Минимальный профит при закрытии по сигналу. None -- откл
        #             },  
        #             "trailing_sl": {
        #                 "enable": False,
        #                 "is_move_tp": True,
        #                 "val": [
        #                     {'activation_indent': 0.6, 'offset_indent': 0.01},
        #                     {'activation_indent': 1.2, 'offset_indent': 0.6}, 
        #                     {'activation_indent': 1.8, 'offset_indent': 1.2}, 
        #                     {'activation_indent': 2.4, 'offset_indent': 1.8}, 
        #                     {'activation_indent': 3.0, 'offset_indent': 2.4}, 
        #                     {'activation_indent': 3.6, 'offset_indent': 3.0},
        #                     {'activation_indent': 4.4, 'offset_indent': 3.6},
        #                     {'activation_indent': 4.8, 'offset_indent': 4.4},
        #                     {'activation_indent': 5.4, 'offset_indent': 4.8}, 
        #                     {'activation_indent': 6.0, 'offset_indent': 5.4},                       
        #                 ]
        #             } 
        #         }
        #     },

        #     "SHORT": {
        #         "entry_conditions": {
        #             "rules": {
        #                 'TREND_EMA': {
        #                     'enable': False,    # True/False -- использовать/не использовать
        #                     'tfr': "1m",
        #                     'period1': 2,
        #                     'period2': 301,
        #                     'is_trend': 1,       # 1 -- trend, -1 -- antyTrend
        #                     'col_name': 'Close',
        #                     "ind_name": 'TREND_EMA'
        #                 },  # 
        #                 'STOCHRSI': {
        #                     'enable': True,    # True/False -- использовать/не использовать
        #                     'tfr': "5m",
        #                     'period': 14, 
        #                     'k': 3,
        #                     'd': 3,
        #                     'over_sell': 35,
        #                     'over_buy': 65,  
        #                     "ind_name": "STOCHRSI"  
        #                 },   
        #                 'VOLF': {
        #                     'enable': True,    # True/False -- использовать/не использовать
        #                     'tfr': "5m",
        #                     "mode": "a", # r --- rolling/ a --- absoluted
        #                     'period': 14,
        #                     'a': {
        #                         'slice_factor': 1.6,
        #                     },
        #                     'r': {
        #                         'slice_factor': 2.9,
        #                     },
        #                     "ind_name": "VOLF"
        #                 },                  
        #             },     
        #             "is_close_bar": False,       # Дожидаться закрытия бара                
        #             "grid_orders": [
        #                 {'indent': 0.0, 'volume': 100, 'signal': True},
        #                 # {'indent': -10.0, 'volume': 25, 'signal': False}, # %
        #                 # {'indent': -20.0, 'volume': 25, 'signal': False},
        #                 # {'indent': -30.0, 'volume': 25, 'signal': False}, # %
        #             ],                        
        #         },

        #         "exit_conditions": {                              
        #             "close_by_signal": {
        #                 "is_active": False,    # Закрытие по сигналу
        #                 "min_profit": 0.6,   # Минимальный профит при закрытии по сигналу. None -- откл
        #             },  
        #             "trailing_sl": {
        #                 "enable": False,
        #                 "is_move_tp": True,
        #                 "val": [
        #                     {'activation_indent': 0.6, 'offset_indent': 0.01},
        #                     {'activation_indent': 1.2, 'offset_indent': 0.6}, 
        #                     {'activation_indent': 1.8, 'offset_indent': 1.2}, 
        #                     {'activation_indent': 2.4, 'offset_indent': 1.8}, 
        #                     {'activation_indent': 3.0, 'offset_indent': 2.4}, 
        #                     {'activation_indent': 3.6, 'offset_indent': 3.0},
        #                     {'activation_indent': 4.4, 'offset_indent': 3.6},
        #                     {'activation_indent': 4.8, 'offset_indent': 4.4},
        #                     {'activation_indent': 5.4, 'offset_indent': 4.8}, 
        #                     {'activation_indent': 6.0, 'offset_indent': 5.4},                       
        #                 ]
        #             } 
        #         }
        #     }                        
        # }),
    
        ("cron", {                              # Ключ - название стратегии, можно любой например с суфиксами (volf_stoch1)
            "LONG": {
                "entry_conditions": {
                    "rules": {
                        'CRON': {
                            'enable': True,            # True/False -- использовать/не использовать
                            'tfr': "5m",
                            'period': 0,
                            "ind_name": 'CRON_IND'
                        },  #               
                    },     
                    "is_close_bar": True,             # Дожидаться закрытия бара                
                    "grid_orders": [
                        {'indent': 0.0, 'volume': 14, 'signal': True},
                        {'indent': -7.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -14.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -21.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -28.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -35.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -42.0, 'volume': 14, 'signal': False}, # %
                    ],                      
                },

                "exit_conditions": {                              
                    "close_by_signal": {
                        "is_active": False,    # Закрытие по сигналу
                        "min_profit": 0.6,   # Минимальный профит при закрытии по сигналу. None -- откл
                    },  
                    "trailing_sl": {
                        "enable": False,
                        "is_move_tp": True,
                        "val": [
                            {'activation_indent': 0.6, 'offset_indent': 0.01},
                            {'activation_indent': 1.2, 'offset_indent': 0.6}, 
                            {'activation_indent': 1.8, 'offset_indent': 1.2}, 
                            {'activation_indent': 2.4, 'offset_indent': 1.8}, 
                            {'activation_indent': 3.0, 'offset_indent': 2.4}, 
                            {'activation_indent': 3.6, 'offset_indent': 3.0},
                            {'activation_indent': 4.4, 'offset_indent': 3.6},
                            {'activation_indent': 4.8, 'offset_indent': 4.4},
                            {'activation_indent': 5.4, 'offset_indent': 4.8}, 
                            {'activation_indent': 6.0, 'offset_indent': 5.4},                       
                        ]
                    } 
                }
            },

            "SHORT": {
                "entry_conditions": {
                    "rules": {
                        'CRON': {
                            'enable': True,            # True/False -- использовать/не использовать
                            'tfr': "5m",
                            'period': 0,
                            "ind_name": 'CRON_IND'
                        },  #               
                    },     
                    "is_close_bar": True,       # Дожидаться закрытия бара                
                    "grid_orders": [
                        {'indent': 0.0, 'volume': 14, 'signal': True},
                        {'indent': -7.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -14.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -21.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -28.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -35.0, 'volume': 14, 'signal': False}, # %
                        {'indent': -42.0, 'volume': 14, 'signal': False}, # %
                    ],                     
                },

                "exit_conditions": {                              
                    "close_by_signal": {
                        "is_active": False,    # Закрытие по сигналу
                        "min_profit": 0.6,   # Минимальный профит при закрытии по сигналу. None -- откл
                    },  
                    "trailing_sl": {
                        "enable": False,
                        "is_move_tp": True,
                        "val": [
                            {'activation_indent': 0.6, 'offset_indent': 0.01},
                            {'activation_indent': 1.2, 'offset_indent': 0.6}, 
                            {'activation_indent': 1.8, 'offset_indent': 1.2}, 
                            {'activation_indent': 2.4, 'offset_indent': 1.8}, 
                            {'activation_indent': 3.0, 'offset_indent': 2.4}, 
                            {'activation_indent': 3.6, 'offset_indent': 3.0},
                            {'activation_indent': 4.4, 'offset_indent': 3.6},
                            {'activation_indent': 4.8, 'offset_indent': 4.4},
                            {'activation_indent': 5.4, 'offset_indent': 4.8}, 
                            {'activation_indent': 6.0, 'offset_indent': 5.4},                       
                        ]
                    } 
                }
            }                        
        }),
    ]
