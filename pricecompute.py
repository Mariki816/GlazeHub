import modelPG


def getPrice(chemID, weight):
    price = modelPG.Chem.getChemPriceByName(chemID, weight)
    return price


# Handling fee charged by Clay Planet. If entire batch is less than 25lbs
# $5.00 surcharge per chemical, anything over 25 lbs is $7.00
# surcharge per chem
def getSurChargeLbs(batchWeight):

    if batchWeight <= 25:
        surcharge = 5.00
    else:
        surcharge = 7.00

    return surcharge


# Handling fee charged by Clay Planet. If entire batch is less than 10,000g
# $5.00 surcharge per chemical, anything over 25 lbs is $7.00
# surcharge per chem
def getSurChargeKilos(batchWeight):

    if batchWeight <= 10:
        surcharge = 5.00
    else:
        surcharge = 7.00
    return surcharge


# Tax rate for Santa Clara County
def getTax(netPrice):
    tax = netPrice * 0.0875
    return tax


# This is shipping price. Batch weight in pounds, price in dollars
def getShipping(batchweight):
    if batchweight <= 2.00:
        shipping = 6.00
    elif (batchweight > 2.00 and batchweight <= 10.00):
        shipping = 13.00
    elif (batchweight > 10 and batchweight <= 20.00):
        shipping = 17.00
    elif (batchweight > 20 and batchweight <= 25.00):
        shipping = 25.00
    else:
        shipping = 50.00
    return shipping
