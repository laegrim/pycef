# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:16:38 2013

@author: laegrim
"""

import smtplib
import logging
import logging.config
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from configobj import ConfigObj
from pycef.lib.conf.constants import LOG_CONF_LOC, SCRAPE_CONF_LOC, CONF_DIR
import pycef.execution.export_data as Export

logging.config.dictConfig(LOG_CONF_LOC)

class SendMail(object):
    '''class SendMail handles actually sending the cef information
    '''
    
    def __init__(self, send_to):
        self.send_to = send_to
        self.logger = logging.getLogger('send_mail')
        self.email_attachment = None
        
        try:
            assert type(self.send_to) == list
        except AssertionError:
            self.logger.exception('send_to is not a list')
        
        self.msg = MIMEMultipart()
        self.msg['From'] = 'cef_server'
        self.msg['To'] = COMMASPACE.join(self.send_to)
        self.msg['Date'] = formatdate(localtime = True)
        self.msg['Subject'] = 'Daily CEF File'
        
    def configure_mail(self, text, attachment_loc):
        ''' SendMail.configure_mail(email_text, email_attachment_loc)
            function to configure the email containing cef information
        '''
        
        try: 
            assert type(text) == str
        except AssertionError:
            self.logger.exception('text is not a string')
            
        try:
            assert type(attachment_loc) == str
        except AssertionError:
            self.logger.exception('email attachment location is not str')
            
        self.msg.attach(MIMEText(text))
        self.email_attachment = MIMEBase('application', "octet-stream")
        
        try:
            self.email_attachment.set_payload(
                                    open(attachment_loc, 'rb').read()
                                    )
        except IOError:
            self.logger.exception('could not open file')
            
        Encoders.encode_base64(self.email_attachment)
        self.email_attachment.add_header('Content-Disposition', 
                                    'attachment; filename="%s"' %'Info.csv')
        self.msg.attach(self.email_attachment)
        
    def send(self):
        ''' SendMail.send(email_text, email_attachment_loc)
            function to actually send the email containing cef information
        '''        

        smtp = smtplib.SMTP('localhost')
        
        try:
            smtp.sendmail('cef server', self.send_to, self.msg.as_string())
        except smtplib.SMTPRecipientsRefused:
            self.logger.exception('recipients of mail were refused')
        except smtplib.SMTPHeloError:
            self.logger.exception('server didn''t reply properly')
        except smtplib.SMTPSenderRefused:
            self.logger.exception('server didn''t accept the from address')
        except smtplib.SMTPDataError:
            self.logger.exception('unexpected server error')
            
        smtp.close()

if __name__ == '__main__':
    ATTACHMENT = Export.ExportCSV(SCRAPE_CONF_LOC)
    ATTACHMENT.parse_config()
    ATTACHMENT.grab_info('CEFS', 'CEF_Info')
    ATTACHMENT.format_info()
    ATTACHMENT.write_info(CONF_DIR + '/attachment.csv')
    config = ConfigObj(CONF_DIR + '/scrape.conf')
    recipt = config['send_freq']['recp_email']
    MAIL = SendMail(recipt)
    MAIL.configure_mail(
        open(SCRAPE_CONF_LOC).read(), CONF_DIR + '/attachment.csv')
    MAIL.send()
    
    
    
    
    
    
