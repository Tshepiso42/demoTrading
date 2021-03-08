from django.shortcuts import render
from .api_helper import stockSearch
from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    current_user = request.user
    stockList = Stock.objects.filter(user=current_user)
    #If user has any stocks
    total_holdings = 0
    if stockList is not None:
        for stock in stockList:
            stockSearch_object = stockSearch(stock.symbol)
            stock.price = stockSearch_object["price"]
            stock.save()
            total_holdings += stock.get_total
    
    total_holdings = round(total_holdings, 2)
    
    #Calculate user total worth
    userCashObject = Cash.objects.get(user=current_user)
    user_cash = userCashObject.user_cash
    UserTotalCash = round(total_holdings + user_cash, 2)
    
    context = {'stocks': stockList, 'holdings': total_holdings, 'totalCash': UserTotalCash}  
    return render(request, 'index.html', context)

@login_required
def quote(request):
    if request.method == 'POST':
        input_symbol = request.POST.get("symbol")
        stock = stockSearch(input_symbol)
        stock_name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]
        
        context = {'company': stock_name, 'symbol': symbol, 'price': price}
        return render(request, 'quoted.html', context)
    else:
        return render(request, 'quote.html')

@login_required
def buy(request):
    current_user = request.user

    if request.method == 'POST':
        input_symbol = request.POST.get("symbol")
        input_quantity = int(request.POST.get("shares")) 
        stock = stockSearch(input_symbol)
        stock_name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]
        #Account for inexistent searches?
        input_total = price * input_quantity
        userCashObject = Cash.objects.get(user=current_user)
        user_cashTotal = userCashObject.user_cash
        
        if input_total <= user_cashTotal: 
            #Update cash object
            userCashObject.user_cash = user_cashTotal - input_total
            userCashObject.save()

            #Record transaction
            transaction = History(user=current_user, symbol=symbol, price=price, shares=input_quantity)
            transaction.save()

            obj, created = Stock.objects.get_or_create(user=current_user, symbol=symbol)
            if created:
                #Add to newly created stock object
                obj.name = stock_name
                obj.shares_quantity = input_quantity
                obj.save()
            else:
                #Update stock object
                obj.shares_quantity += input_quantity
                obj.save()
            


    return render(request, 'buy.html')

@login_required
def sell(request):
    current_user = request.user
    stockList = Stock.objects.filter(user=current_user)  
    context = {'stocks': stockList}
    
    if request.method == 'POST':
        input_symbol = request.POST.get("symbol")
        input_quantity = int(request.POST.get("shares")) 
        stock = stockSearch(input_symbol)
        
        #Account for inexistent searches
        if stock is not None:
            stock_name = stock["name"]
            price = stock["price"]
            symbol = stock["symbol"]
            
            input_total = price * input_quantity

            userCashObject = Cash.objects.get(user=current_user)
            user_cashTotal = userCashObject.user_cash
            #StockObject will always be there because we select from database list
            stockObject = Stock.objects.get(user=current_user, symbol=symbol)
        
            if input_quantity <= stockObject.shares_quantity:
                #Update cash object
                userCashObject.user_cash = user_cashTotal + input_total
                userCashObject.save()

                #Record transaction
                transaction = History(user=current_user, symbol=symbol, price=price, shares=(-1*input_quantity))
                transaction.save()

                #Reduce stock quantity or remove object
                stockObject.shares_quantity -= input_quantity
                stockObject.save()
                if stockObject.shares_quantity == 0:
                    stockObject.delete()

        #JavaScript alert? and redirect to empty sell page again
         
    return render(request, 'sell.html', context)

@login_required
def history(request):
    current_user = request.user
    transactions = History.objects.filter(user=current_user)   
    context = {'transactions': transactions}  
    return render(request, 'history.html', context)