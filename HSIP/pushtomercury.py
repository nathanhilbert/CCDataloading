# coding: utf-8
import paramiko
import getpass
import os
import os.path as op

SOURCEDIR = r"C:\Users\nlh\Workspace\Urbis\pgDataLoading\HSIP\data"
DESTDIR = "/var/www/html/metadata/urbis/xml/hsip"
DEBUG=False

if __name__ == '__main__':
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print """You must request access to mercury.  You will be logging in with your {domain username}mercury
        (e.g. nlhmercury) and your domain password"""
    print "Username: "
    username = raw_input() 
    password = getpass.getpass("Password: ")
    s.connect("mercury.ornl.gov", 22, username=username, password=password)
    sftp = s.open_sftp()
    # sftp = paramiko.SFTPClient.from_transport(s)

    for d in os.listdir(SOURCEDIR):
        try:
            if DEBUG:
                print "doing to make dir"
                print "\t\t", DESTDIR + "/" + d
            else:
                sftp.mkdir(DESTDIR + "/" + d)
        except IOError:
            print('skip {0} folder already exists'.format(d))
        sectionsourcefolder = op.join(SOURCEDIR, d)
        sectiondestfolder = DESTDIR + "/" + d
        for f in os.listdir(sectionsourcefolder):
            if f.endswith('xml'):
                if DEBUG:
                    print "Going to put :"
                    print "\t\t", op.join(sectionsourcefolder, f)
                    print "\t\t", sectiondestfolder + "/" + f
                else:
                    sftp.put(op.join(sectionsourcefolder, f), sectiondestfolder + "/" + f)





    s.close()

