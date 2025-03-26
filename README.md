# Oracle Exposure Check (python)

## Description

Oracle Exposure Check (python) is a tool that queries the CloudSEK API to determine whether a given domain is affected by Oracle-related vulnerabilities. The tool allows users to check a single domain or scan multiple domains from a list, and it automatically generates a CSV report of the results.

The tool is intended for educational and informational purposes only. It helps to identify domains potentially impacted by Oracle vulnerabilities, but it should be used responsibly, and you must ensure you have proper authorization before scanning any domains.

Thanks and credits to CloudSEK for https://exposure.cloudsek.com/.

---

## Disclaimer

**This tool is provided 'as-is' for educational and informational purposes only.**

- I'm not associated with CloudSEK
- Use at your own risk.
- The author is not responsible for any misuse, damage, or unintended consequences.
- Ensure that you have proper authorization to perform any scans or actions using this tool.
- It is your responsibility to comply with all applicable laws and regulations.

---

## Features

- **Single Domain Scan**: Check if a single domain is impacted by Oracle-related vulnerabilities.
- **Multiple Domain Scan**: Provide a list of domains (one per line) and scan them all at once.
- **Automatic CSV Export**: After scanning, results are automatically saved to a CSV file for easy reference.
- **Dynamic Proxy-Authorization**: A random Base64-encoded Proxy-Authorization key is generated for each run, ensuring seamless authentication.

---

## Requirements

- Python 3.x
- `requests` library
- `colorama` library (for colorful console output)

You can install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/zer0lightning/oracle-exposure-check.git
cd oracle-exposure-check
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the tool:

```bash
python oracle_exposure_check.py
```

---

## Usage

1. **Single Domain Check**:  
   When prompted, enter the domain you want to check. The tool will display whether it is impacted by Oracle vulnerabilities and save the results to a CSV file.

2. **Multiple Domain Check**:  
   If you have a list of domains (one per line), provide the path to the file, and the tool will scan all the domains and save the results to a CSV file.

3. **CSV Output**:  
   After scanning, you can save the results to a CSV file. The file will contain two columns: `Domain` and `Impacted Oracle Attack`.

---

## Example Output

```
------------------------------------
Oracle Exposure Check
Author: Lewis Saludo
Version: 1.0
Credits: CloudSEK API
------------------------------------

Generated Proxy-Authorization key: Basic eXNhbWVzdHJpbmc6ZGVtbyBzdHJpbmc=

Scan single Domain or provide a list file? (single/list): single
Please provide the domain to check: example.com
Domain: example.com | Impacted Oracle Attack: Yes

Results have been automatically saved to 'oracle_attack_results.csv'.
Do you want to continue? (y/n): n
Exiting the program...
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributing

If you find any issues or want to contribute improvements to the tool, feel free to open an issue or submit a pull request. All contributions are welcome!

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

---

## Author

- **Lewis Saludo** - [Your GitHub Profile](https://github.com/zer0lightning)

---

## Acknowledgments

- Thanks to the CloudSEK team for providing the API used to identify Oracle breaches.
- Inspired by various security tools for vulnerability scanning.

---

## Contact

For any questions or issues, please open an issue on GitHub.
