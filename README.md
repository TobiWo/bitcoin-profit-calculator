# BTPC - Bitcoin Trading Profit Calculator
## Table of Content
* [Description](#description)
    * [NOTE on application speed (Bitmex)](#speed_note)
* [Version](#version)
* [Requirements](#requirements)
* [Installation](#installation)
    * [Python](#python)
    * [BTPC](#btpc)
    * [Dependencies](#dependencies)
* [Preparation](#preparation)
    * [API keys](#api_keys)
        * [Bitmex Key](#bitmex_key)
* [Usage](#usage)
    * [Output](#output)
    * [CLI flags](#cli_flags)
* [Verification](#verification)
    * [Bitmex](#bitmex_verify)
* [Planned features](#planned_features)
* [Donation](#donation)
    

## <a name="description"></a>Description
This application calculates profit, loss and taxes from leverage trading with bitcoin. Currently this is in an early phase of development and only supports Bitmex (and here only one account per run). However, multi-account support is already planned and will be integrated. Further major features will include the support for bybit and an ui. All currently planned feature are listed below in the respective section of this ReadMe. Suggestions from the community for further features are welcome.

### <a name="speed_note"></a>NOTE on application speed (Bitmex)
Because of the request limits set by Bitmex there is an artificial delay during the fetching process. Therefore after every request there is a one second pause. Due to the API nature of Bitmex the application needs to fetch data for every single day separately. In combination with the delay this leads to the fact, that a run to fetch data for a complete year, will take approx. 6 minutes, while fetching data for a month will take approx. 30 seconds.

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

## <a name="usage"></a>Usage
Currently the application has no UI and therefore is based on a command line interface (cli). All command line flags are listed below.

For usage test, navigate to the installation folder and type `python btc_trading_profit_calculator.py -h`

This will print all available command line flags.

The most important flags are `-y` and `-m` which will specify the year and the month for which you will retrieve your trading data. If you do not specify a month, the data will be retrieved for the whole year. However, specifying a year is mandatory. As mentioned above a complete list of flags and there description is listed below.

A sample call of the application would be:

`python btc_trading_profit_calculator.py -y 2019 -m 8`

This will fetch the data for August 2019. The output-files are stored in the `out`-folder within the installation folder.

### <a name="output"></a>Output
The output of the application is splitted to two files. One contains all the fundings for the specified period, the other one contains all the actual trading data (opening and closing positions for market price, limit order etc.). Currently I'm not 100% sure if this is more confusing then it helps. Therefore I will probably change this to only one output file.

The columns in the files are self-explanatory. The last three columns represent the enriched data which were added or modified by the application. While adding more platforms this may change over time. 

### <a name="cli_flags"></a>CLI flags
| Flag (short) | Flag (long) | Mandatory | Description |
| --- | -------- | --- | --- |
| -k | --keys | False | Specifies the path to your api-keys. Default path is <project_dir>/resources/api_keys.json |
| -y | --year | True | Fetch data for the defined year |
| -m | --month | False | Fetch data for the defined month |
| -t | --tax_rate | False | Tax rate specified as fraction of one: 0.x Taxe rate is applied to the total profit. |
| -l | --tax_limit | False | In some countries there is maybe kind of a free profit limit where no taxes need to be payed for. This flags defines the limit. However, if the limit/threshold is reached taxes are calculated for the whole profit. If this is not the correct way I highly recommend not to rely on tax-calculation of the application but rather do your own calcualtion based on the returned profit/loss output |

## <a name="verification"></a>Verification
Verification refers to the fact, that the APIs of the different platforms return your trades in a very unusual, kind of unreadable way. At least this is true for Bitmex (Bybit wasn't tested yet). Therefore some data wrangling is happening in the background, to export the data in the most readable way. To be 100% sure that nothing unexpected happened during modification, I provide verification scripts which you can use to verify the output of this application against the data you can download from the platforms. The verifiers can be found within the folder `verifier` of the applications installation folder.  

### <a name="bitmex_verify">Bitmex (**UNDER DEVELOPMENT**)
Within the bitmex subfolder you can find another folder named `resources`. Please put in there the following files (do not rename the files):
* the original csv-file from your Bitmex-account 
* the positions-file from the BTPC output
* the fundings-file from the BTPC output

You can run the verification process with the command:
* `python verify_bitmex.py`

In dependence whether you only put in an BTPC output from a month or a year the verification is automatically done only for this month or year.

## <a name="planned_features"></a>Planned features
* add verifier which verify the results of the BTPC against the bitmex-account.csv
* combine multiple bitmex accounts    
* add UI
* add bybit support
* combine multiple bybit accounts
* set month-range for getting data for specified (multiple) months
* logger

## <a name="donation"></a>Donation
If you think this application is helpful in regards to your trading activity, I would appreciate every Satoshi or Wei or whatever you think is reasonable. This will help to continue the work and implement new features.

You can support using Bitcoin or Ethereum.

Bitcoin:

`197GMuw8KQcD7QS7g2d6NhUKHd91TNUnuq`

Ethereum:

`0x5a7F786815C03b45DC4341baE97fD4D9D6E70320`

**Thank you very much!**