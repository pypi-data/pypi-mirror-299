import mailbox

def scan_mbox(filename):
    box = mailbox.mbox(filename, create=False)
    for msg in box:
        id = msg["message-id"]
        id = id.replace("\r", " ")
        id = id.replace("\n", " ")
        id = id.strip()
        msg_sub = "-" #msg["subject"]
        print("(%s) (%s)" % (id, msg_sub))
