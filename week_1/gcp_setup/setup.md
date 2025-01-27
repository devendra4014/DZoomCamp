# gcp setup

### create public private key
```
ssh-keygen -t rsa -b 4096 -f gcp
```

## create config
- create a config file at `touch ~/.shh/config`
- open file in vs code `code config`
- add below details to file
  ```sh
    # VM Connection Details
    Host zoomcamp
        HostName vm-add-ress  # Replace with your VM's IP address
        User devendra          # Replace with your VM username
        Port 22             # Standard SSH port
        IdentityFile C:/Users/Devendra/.ssh/gcp  # Path to your private SSH key 
        
    # Optional settings for specific commands 
    #  -  "StrictHostKeyChecking no" to bypass host key checking 
    #  -  "ConnectTimeout 5" to set a timeout for connection attempts 
  ```

## update 
```
sudo apt update
```

## install terraform
- create bin directory
```sh
cd ~
mkdir bin
cd bin
```
- download terraform binary using wget
```sh
wget https://releases.hashicorp.com/terraform/1.10.4/terraform_1.10.4_linux_386.zip
sudo apt-get install unzip
unzip terraform_1.10.4_linux_386.zip
rm terraform_1.10.4_linux_386.zip
```
- open bashrc file
```sh
cd ~
vim .bashrc
```
 
- add path to bashrc file
```sh
export PATH="${HOME}/bin:${PATH}"
```
- logout and again login or execute below command
```sh
source .bashrc
```