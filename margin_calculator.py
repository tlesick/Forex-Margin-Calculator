class Margin_Calculator(object):
    # EX: 1.15000 sell eurusd 25.00 50:1 194,779 
    def calculate(self, **kwargs):
        # Organize Key word arguments
        entry, direction, pair, lot_size, capitial, risk_of_trade, margin, stop_loss = 0,0,0,0,0,0,0,0
        for key, value in kwargs.items():
            if key == 'entry':
                entry = value
                continue
            else:
                raise ValueError('Entry Position is required: e.g. 1.15000')
            if key == 'direction':
                direction = value
                print('direction '+str(direction))
                continue
            else:
                raise ValueError('Direction is required: e.g. "buy","Sell","Long","short"')
            if key == 'pair':
                pair = value
                print('pair ' + str(pair))
                continue
            else:
                raise ValueError('pair is required: e.g. "EUR/USD" "USD/JPY"')
            if key == 'lot_size':
                lot_size = value
                continue
            else: 
                raise ValueError("lot_size is required: e.g. 1.0 or 0.05")
            if key == 'capitial':
                capitial = value
                continue
            else:
                raise ValueError("Capitial is required: e.g 5000")
            if key == 'risk':
                risk_of_trade = value
                continue
            else:
                raise ValueError("Risk is required (percent in decimal form) e.g. 0.02")
            if key == 'margin':
                margin = value
                continue


            
        # Static Margin Requirements from OANDA AUG 2018 
        margin_of_pairs = {'AUD/CAD':3.0,'AUD/CHF':3.0,'AUD/HKD':5.0,'AUD/JPY':4.0,'AUD/NZD':3.0,'AUD/SGD':5.0,'AUD/USD':3.0,'CAD/CHF':3.0,'CAD/HKD':5.0,'CAD/JPY':4.0,
        'CAD/SGD':5.0,'CHF/HKD':5.0,'CHF/JPY':4.0,'CHF/ZAR':5.0,'EUR/AUD':3.0,'EUR/CAD':2.0,'EUR/CHF':3.0,'EUR/CZK':5.0,'EUR/DKK':2.0,'EUR/GBP':5.0,'EUR/HKD':5.0,
        'EUR/HUF':5.0,'EUR/JPY':4.0,'EUR/NOK':3.0,'EUR/NZD':3.0,'EUR/PLN':5.0,'EUR/SEK':3.0,'EUR/SGD':5.0,'EUR/TRY':5.0,'EUR/USD':2.0,'EUR/ZAR':5.0,'GBP/AUD':5.0,
        'GBP/CAD':5.0,'GBP/CHF':5.0,'GBP/HKD':5.0,'GBP/JPY':5.0,'GBP/NZD':5.0,'GBP/PLN':5.0,'GBP/SGD':5.0,'GBP/USD':5.0,'GBP/ZAR':5.0,'HKD/JPY':5.0,'NZD/CAD':3.0,
        'NZD/CHF':3.0,'NZD/HKD':5.0,'NZD/JPY':4.0,'NZD/SGD':5.0,'NZD/USD':3.0,'SGD/CHF':5.0,'SGD/HKD':5.0,'SGD/JPY':5.0,'TRY/JPY':5.0,'USD/CAD':2.0,'USD/CHF':3.0,
        'USD/CNH':5.0,'USD/CZK':5.0,'USD/DKK':2.0,'USD/HKD':5.0,'USD/HUF':5.0,'USD/JPY':4.0,'USD/MXN':8.0,'USD/NOK':3.0,'USD/PLN':5.0,'USD/SAR':5.0,'USD/SEK':3.0,
        'USD/SGD':5.0,'USD/THB':5.0,'USD/TRY':5.0,'USD/ZAR':5.0,'ZAR/JPY':5.0}

        # List of Pairs that are not to the 5th decimal place (extremely weak)
        different_decimal_pairs = ['JPY','ZAR','SEK','HUF']
        
        # Convert Margin into percentage 
        if margin == 0: 
            for name, percent in margin_of_pairs.items():
                if pair == name:
                    margin = (percent /100)
        else:
            margin = (margin/100)
            

        # WEAK CURRENCY PAIRS
        for i in different_decimal_pairs:
            if i in pair:
                cost_of_margin = margin * (lot_size*100000)
                remaining_capital = capitial - cost_of_margin
                loss_risk = remaining_capital  * risk_of_trade
                number_of_pips = loss_risk/ lot_size
                if direction == 'sell' or direction == 'Sell' or direction='short' or direction='Short':
                    stop_loss = (number_of_pips/1000) + entry 
                if direction == 'Buy' or direction == 'buy' or direction='long' or direction='Long':
                    stop_loss = entry - (number_of_pips/1000)  
                return stop_loss
        # NORMAL PAIRS
            else:
                cost_of_margin = margin * (lot_size*100000)
                remaining_capital = capitial - cost_of_margin
                loss_risk = remaining_capital  * risk_of_trade
                print('Total amount possibly lost: ' + str(loss_risk))
                number_of_pips = loss_risk/ lot_size
                if direction == 'sell' or direction == 'Sell' or direction='short' or direction='Short':
                    stop_loss = (number_of_pips/100000) + entry 
                if direction == 'Buy' or direction == 'buy' or direction='long' or direction='Long':
                    stop_loss =  entry - (number_of_pips/100000)   
                return stop_loss

        

        
        # TEST

# print(Margin_Calculator().calculate(entry=111.067, direction='Sell',pair='USD/JPY',lot_size=1.00, capitial=5000, risk=0.02))
# print(Margin_Calculator().calculate( direction='Sell',pair='EUR/USD',lot_size=1.00, capitial=5000))
# print(Margin_Calculator().calculate(entry=1.15000, direction='Sell',pair='EUR/USD',lot_size=0.05, capitial=5000, risk=0.02))
