from io import StringIO
import turbofm
import turbofm.scan
import mailbox
import sys
import logging
import email.generator

logging.basicConfig(level=logging.INFO)



if len(sys.argv) == 1:
    print("""
# usage: bodies SRC.mbox
""")
    sys.exit(1)


arg_infile = sys.argv[1]
logging.info("infile="+arg_infile)


try:

    for msg_item in turbofm.scan.scan_mbox(arg_infile):
        msg = msg_item["msg"]
        if msg.is_multipart():
            body_plain=""
            body_html=""
            for part in msg.walk():
                if part.get_content_type()=="text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                    body_plain = part.get_payload(decode=True).decode(errors='ignore')
                if part.get_content_type()=="text/html" and "attachment" not in str(part.get("Content-Disposition")):
                    body_html = part.get_payload(decode=True).decode(errors='ignore')
            print("-"*80)
            print(body_plain.replace("\r", "").replace("\n", "").strip())
            print("-"*80)
            print(body_html.replace("\r", "").replace("\n", "").strip())
            print("-"*80)
        else:
            print("-"*80)
            body = msg.get_payload(decode=True).decode(errors='ignore')
            print(body.replace("\r", "").replace("\n", "").strip())
            print("-"*80)
            print("-"*80)

except Exception as e:
    logging.error("Something went wrong (%s)" % str(e))
