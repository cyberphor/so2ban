# sister
> Normalizes and appends threat intel from CrowdStrike to your local Zeek 'intel.dat' file.

## How to download threat intel from CrowdStrike
- Login to [CrowdStrike](https://falcon.crowdstrike.com/login/)
- Click-on the *Intelligence* tab (left-hand side) > *Indicators*
- Filter for:
  - `last updated: past 30 days`
  - `confidence: high`
  - `targets:government`
- Click-on the export button (right-hand side) > JSON
- Click-on the download button when prompted
- Rename the JSON file to `intel.json`
- Deliver the JSON file to your air-gapped Bro/Zeek instance via sneaker-net
- Place the JSON file in your current working directory

## Usage
```
sudo ./sister.py
```
