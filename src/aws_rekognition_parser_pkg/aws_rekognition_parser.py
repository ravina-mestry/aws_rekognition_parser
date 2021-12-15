# function parse_rekognition_response_receipt_text detects the vendor name and total amount from rekognition response and returns a dictionary
def parse_rekognition_response_receipt_text(rekognitionResponse, vendorNameList):
    
    receiptText = dict()

    isVendorName = False
    numTotal = 0
    isAmountTotal = False

    # run a for loop on TextDetections in response
    for text in rekognitionResponse['TextDetections']:
        #print( text['Type'] + ' ' + text['DetectedText'].lower() + ' : ' + str(text['Confidence']))

        # when receipt text is read, word total is found first and the next word is the amount.
        # if word total is found, numTotal is set to 1 in the previous iteration.
        # so set numTotal to 2 in this iteration so that amount can be detected.
        if numTotal == 1:
            numTotal = 2
        
        # if VendorName is not found then try to match it with vendorNameList input and if found then set it into dictionary and set isVendorName to True
        if not isVendorName:
            for vendorName in vendorNameList:
                if text['DetectedText'].lower() == vendorName.lower():
                    receiptText['vendorName'] = vendorName
                    isVendorName = True

        # when receipt text is read, word total is found first and the next word is the amount.
        # so when total is found, set numTotal to 1 and let it pass through this iteration of for loop to find the amount as the next word.
        if numTotal == 0:
            if text['DetectedText'].lower() == 'total':
                numTotal = 1
        
        # if numTotal is 2 then parse the amount and ensure it is numeric and set float amount in dictionary and set isAmountTotal to True
        if numTotal == 2:
            numTotal = 0
            amountTotal = text['DetectedText'].lower().replace('eur', '')
            if amountTotal.replace('.', '').isnumeric():
                receiptText['amountTotal'] = float(amountTotal)
                isAmountTotal = True
        
        # if both vendor name and total amount is found, then break the for loop
        if isVendorName and isAmountTotal:
            break

    return receiptText
