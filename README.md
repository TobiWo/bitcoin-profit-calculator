# BTPC - Bitcoin Trading Profit Calculator
## Table of Content
* [Description](#description)
* [Version](#version)
* [Requirements](#requirements)
* [Installation](#installation)
    * [Python](#python)
    * [BTPC](#btpc)
    * [Dependencies](#dependencies)
    

## <a name="description"></a>Description
This application calculates profit, loss and taxes from leverage trading with bitcoin. Currently this is in an early phase of development and only supports Bitmex (and here only one account per run). However, multi-account support is already planned and will be integrated. Further major features will include the support for bybit and an ui. All currently planned feature are listed below in the respective section of this ReadMe. Suggestions from the community for further features are welcome.

## <a name="version"></a>Version
Current version: **0.1**

## <a name="requirements"></a>Requirements
Python 3.6 or higher

## <a name="installation"></a>Installation
### <a name="python"></a>Python
Use `python --version` (in a cmd (Windows) or terminal (Linux, Mac)) to check if you have the required version installed.

If the above command returns an error, you have no Python installed or at least it is not in your system PATH-variable. In this case I simply suggest to download the official installer from [here](https://www.python.org/downloads/) and follow the installation instructions. **IMPORTANT**: If the installer asks you to add Python to your PATH-variable, you should agree.

If the above command returns a version lower than the requirement, I suggest to install miniconda in order not to mess up with the current installation. This has the advantage that you can create a separate Python-environment only for this application which will not effect the Python version already installed on your system.
To get the latest miniconda version: [click here](https://docs.conda.io/en/latest/miniconda.html).
After installation you should open an "Anaconda Prompt" on Windows or a terminal on unix-based systems and type `conda create --name py37 python=3.7`. This will create a new Python-environment with Python 3.7.x. After creation of the environment you simply need to activate it for the current terminal/cmd-sesssion. Use `conda activate py37`. Now you can proceed with the rest of the installation.

### <a name="btpc"></a>BTPC
In order to install this application you simply need to clone the repo or to download the zip and unpack it to a folder of your choice. That's it.

### <a name="dependencies"></a>Dependencies
The application has some dependencies which need to be installed before you can run it. Fortunately, this is only a one-liner.

Open a terminal or a "Anaconda Prompt" (activate the respective environment `conda activate py37`), navigate to the folder where you downloaded and unpacked the BTPC-application and type `pip install -r requirements.txt`. After dependency-installation you are good to go.

## <a name="preparation"></a>Preparation
### <a name="api_keys"></a>API Keys
The application uses the APIs from the respective trading portals. For version 0.1 it's only Bitmex. In order to retrieve data for your account you need to create an API key-pair. This key-pair needs to be saved in a specific json-format. A sample how this file looks like is already included within the application folders. Simply navigate to the BTPC installation folder and open the following file `resources/api_keys.json` with a text editor of your choice (for Windows: Notepad++ is great). As mentioned often times, the application currently only supports one account,therefore you just need to change the demo key-pair with the one you created at Bitmex.

#### <a name="bitmex_key"></a>Bitmex key-pair
* login to your account
* navigate to "API"

    ![API](https://raw.githubusercontent.com/TobiWo/bitcoin-trading-profit-calculator/development/resources/api_generation/bitmex/api_2.PNG "Bitmex API")

* navigate to "API Key Management

    ![Key Management](https://raw.githubusercontent.com/TobiWo/bitcoin-trading-profit-calculator/development/resources/api_generation/bitmex/management_2.png "Bitmex API")

* find your IP-address using [this website](https://www.whatismyip.com/de/)
* fill out the API-creation form and hit the "Create API Key"-button
    * in CIDR put in your IP as follows `<your IP>/32`
    * **NOTE**: Your IP can change over time. Therefore it will be necessary to re-create the API-key from time to time.
* Copy&Paste the key-ID and the key-Secret to the above mentioned **api_keys.json**


