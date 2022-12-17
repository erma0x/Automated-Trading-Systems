from kucoin_contract import *
from kucoin_utils import *
def opposite(type_order):
    if type_order=='buy':
        return 'sell'
    return 'buy'

def sort_orders(op_data_structure):
    if op_data_structure['side'] == 'buy':
        op_data_structure['take_profits'] = sorted(op_data_structure['take_profits'])
        op_data_structure['stop_losses'] = sorted(op_data_structure['stop_losses'],reverse=True)
    else:
        op_data_structure['take_profits'] = sorted(op_data_structure['take_profits'],reverse=True)
        op_data_structure['stop_losses'] = sorted(op_data_structure['stop_losses'])
    return op_data_structure

def string_to_float_prices(op_data_structure):
    columns = ['entry_prices','take_profits','stop_losses']
    for col in columns:
        for i in range(len(op_data_structure[col])):
            op_data_structure[col][i] = float(op_data_structure[col][i])
    return op_data_structure


async def trader_kucoinfutures(order_data, exchange, maintenance_capital =0.05):
    '''
    get aviable balance
    get minimal order
    rebalance with a multiple of the minimal order
    '''

    order_data = string_to_float_prices(op_data_structure=order_data)
    order_data = sort_orders(op_data_structure=order_data)
    
    amount_usd_position = await get_amount_position_usdt()

    if print_op: print('position in usdt $ ',amount_usd_position,'leverage ',order_data['leverage'])

    n_entry_prices = len(order_data['entry_prices'])
    n_take_profits = len(order_data['take_profits'])
    n_stop_losses = len(order_data['stop_losses'])

    if get_free_balance(exchange) < (1+maintenance_capital) * amount_usd_position:
        return None

    for i in range(len(order_data['entry_prices'])): 
        
        entry_price = deepcopy(order_data['entry_prices'][i])

        amount_token_position = round( amount_usd_position / n_entry_prices / entry_price , 8 )
        	

        if print_op: print('amount_token_position ',amount_token_position)      
        
        # ENTRY LONG 
        entry_order = exchange.create_limit_order(symbol=order_data['symbol'],
                                                    side=order_data['side'],
                                                    amount=amount_token_position,
                                                    price=entry_price,
                                                    params={'leverage':order_data['leverage'], # TRIGGER PRICE #,'stop':'down','stopPriceType':'TP','stopPrice':entry_price,
                                                                'forceHold':False})
                                                                
        # TAKE PROFIT 
        take_profit_quantities = balance_kucoinfutures_contract_quantity(order_data['take_profits'], amount_token_position)        
        if print_op: print('take_profit_quantities ',take_profit_quantities)
        for j in range(len(order_data['take_profits'])):
            order = exchange.create_limit_order(symbol=order_data['symbol'],
                                                side=opposite(order_data['side']),
                                                amount=take_profit_quantities[j],
                                                price=order_data['take_profits'][j],
                                                params={'leverage':order_data['leverage'],'reduceOnly':True,
                                                'stop':kucoin_side(side=order_data['side'],trigger='TAKEPROFIT'),'stopPriceType':'TP','stopPrice':order_data['take_profits'][j]})


        # STOP LOSS
        stop_loss_quantities = balance_kucoinfutures_contract_quantity(order_data['stop_losses'], amount_token_position)
        if print_op: print('stop_loss_quantities ',stop_loss_quantities)
        for k in range(len(order_data['stop_losses'])):
            order = exchange.create_limit_order(symbol=order_data['symbol'],
                                                side=opposite(order_data['side']),
                                                amount=stop_loss_quantities[k],
                                                price=order_data['stop_losses'][k],
                                                params={'leverage':order_data['leverage'],'reduceOnly':True
                                                ,'stop':kucoin_side(side=order_data['side'],trigger='STOPLOSS'),'stopPriceType':'TP','stopPrice':order_data['stop_losses'][k],
                                                'forceHold':False})
