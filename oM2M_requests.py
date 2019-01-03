import requests

def createAE():
    print('Creating Application Entity.....')
    name = input('Please enter your AE name:')
    ae_name = '"' + name + '"'

    content = '<m2m:ae xmlns:m2m="http://www.onem2m.org/xml/protocols" rn=' + \
            ae_name + '>' + '<api>air-box</api><lbl>airbox</lbl><rr>false</rr>'  + '</m2m:ae>' 
    
    header = {"X-M2M-Origin": "admin:admin", \
                "Content-Type":"application/xml;ty=2"}
    
    url = 'http://140.113.216.14:10001/~/in-cse'
    
    r = requests.post(url, headers=header, data=content)
    print(r)

def createContainer():
    print('Creating container.....')
    ae = input('Please choose which AE you want to add container:')
    name = input('Please enter your container name:')
    containerName ='"' + name + '"'
    
    header = {"X-M2M-Origin": "admin:admin", \
                "Content-Type":"application/xml;ty=3"}

    content = '<m2m:cnt xmlns:m2m="http://www.onem2m.org/xml/protocols" rn=' + \
            containerName + '>' + '</m2m:cnt>' 

    url = 'http://140.113.216.14:10001/~/in-cse/in-name/' + ae
    
    r = requests.post(url, headers=header, data=content)
    print(r)

def createContainerInstance(data, ae, cnt):
    header = {"X-M2M-Origin": "admin:admin", \
                "Content-Type":"application/xml;ty=4"}

    content = '<m2m:cin xmlns:m2m="http://www.onem2m.org/xml/protocols">' \
                + '<cnf>' + 'data' + '</cnf>' \
                + '<con>' + data + '</con>' \
                + '</m2m:cin>'

    url = 'http://140.113.216.14:10001/~/in-cse/in-name/' + ae + '/' + cnt
    
    r = requests.post(url, headers=header, data=content)
    print(r)


def deleteAE(name):
    header = {"X-M2M-Origin": "admin:admin", \
            "Content-Type":"Accept:application/xml"}

    url = 'http://140.113.216.14:10001/~/in-cse/in-name/' + name
    
    r = requests.delete(url, headers=header)
    print(r)
