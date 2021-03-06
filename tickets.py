
try:
    import pickle
    import sys, os
    from kayako import Ticket, TicketAttachment, TicketNote, TicketPost, TicketPriority, TicketStatus, TicketType, TicketCount
    from kayako import KayakoAPI

    path = str(sys.argv[0])
    path = path.replace("tickets.py", '')
    

    file = 'pickle.pk'
    file = path + file

    first = False
    try:
        with open(file, 'rb') as fi:
            previous = pickle.load(fi)
    except:
        first = True

    APIKEYS = 'APIKEYS.TXT'
    APIKEYS = path + APIKEYS
    ak = open(APIKEYS, 'r')

    lines = ak.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip("\n")

    API_URL = lines[0]
    API_KEY = lines[1]
    SECRET_KEY = lines[2]
    api = KayakoAPI(API_URL, API_KEY, SECRET_KEY)


    tickets = api.get_all(Ticket, 5, ticketstatusid=4)
    ticketcount = len(tickets)
    if first == True:
        previous = ticketcount
    print(ticketcount)
    for n in range(ticketcount):
        print(tickets[n])

    new = ''
    if ticketcount == previous + 1:
        new = '1'
    elif ticketcount == previous + 2:
        new = '2'
    elif ticketcount == previous + 3:
        new = '3'
    elif ticketcount == previous + 4:
        new = '4'
    elif ticketcount == previous + 5:
        new = '5'
    elif ticketcount >= previous + 6:
        new = "5+"

    realbody = ''
    if new == '1':
        realbody = "A new support ticket is available!"
    if new != '1':
        realbody= "%s new support tickets are available!" % new

    if ticketcount > previous:

        from twilio.rest import TwilioRestClient

        account_sid = lines[3]
        auth_token  = lines[4]

        client = TwilioRestClient(account_sid, auth_token)

        message = client.messages.create(body=realbody,
            to= lines[5],    
            from_= lines[6]) 
    

    with open(file, 'wb') as f:
        pickle.dump(ticketcount, f)

    ak.close()
except:
    pass
    # ERROR


