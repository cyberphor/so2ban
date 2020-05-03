# sister
> Feeds Bro the latest threat intel from CrowdStrike.

## Usage
* **NOTE:** this script was designed for the [Security Onion](https://securityonion.net) Network Security Monitoring platform. 
* Place the following within your current working directory:
  * `sister.py`
  * The latest threat intel from CrowdStrike in the form of a JSON file. 
    * ex: `59_indicators_2020-05-03T04_41_51Z.json`
* Execute `sudo ./sister.py`

## How to Download Threat Intel from Crowdstrike
- Login to [CrowdStrike](https://falcon.crowdstrike.com/login/)
- Click-on the *Intelligence* tab (left-hand side) > *Indicators*
- Filter for:
  - `last updated: past 30 days`
  - `confidence: high`
  - `targets: government`
- Click-on the export button (right-hand side) > JSON
- Click-on the download button when prompted
- Save the JSON file to disc
- Distribute the intel via sneaker-net

## What is Bro?
- [Learn More](https://zeek.org)

## What is CrowdStrike?
- [Learn More](https://www.crowdstrike.com/endpoint-security-products/falcon-x-threat-intelligence/)
