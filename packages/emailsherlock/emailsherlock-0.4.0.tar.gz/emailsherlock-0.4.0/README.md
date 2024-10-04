# EmailSherlock 🕵️‍♂️📧

EmailSherlock is a powerful Python tool for validating email addresses using DNS and SMTP checks. It provides a confidence score for each email's validity and potential deliverability, helping you deduce the legitimacy of email addresses with detective-like precision.

[![PyPI version](https://badge.fury.io/py/emailsherlock.svg)](https://badge.fury.io/py/emailsherlock)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/emailsherlock.svg)](https://pypi.org/project/emailsherlock/)

## 🔍 Features

- Validates email format using regex
- Checks domain DNS records (MX and A records)
- Attempts SMTP connection to verify mail server responsiveness
- Provides a confidence score (0-100%) for each email
- Handles both single email validation and bulk validation from a file
- Multi-threaded for improved performance with large datasets
- Cleaner error messages without unnecessary instructions
- Default output file for bulk validation
- Multiple MX record support
- Improved SMTP connection attempts across various ports and protocols
- Random sender email generation for each SMTP check

## 🛠️ Installation

You can install EmailSherlock using pip:

```bash
pip install emailsherlock
```

Alternatively, you can clone the repository and install it manually:

```bash
git clone https://github.com/yourusername/emailsherlock.git
cd emailsherlock
pip install -e .
```

## 🚀 Usage

### Command Line Interface

#### Single Email Validation

To validate a single email address:

```bash
emailsherlock --single email@example.com
```

#### Bulk Email Validation from File

To validate multiple email addresses from a file:

```bash
emailsherlock --file input_file.txt
```

This will read from `input_file.txt` and write results to `results.csv` (default output file).

To specify both input and output files:

```bash
emailsherlock --file input_file.txt --output custom_output.csv
```

The input file should contain one email address per line. If you want to include additional information (like a school name), use a comma to separate it from the email:

```
email1@example.com
email2@example.com
School Name,email3@example.com
```

### Python API

You can also use EmailSherlock in your Python scripts:

```python
from emailsherlock import EmailSherlock

sherlock = EmailSherlock()

# Validate a single email
result = sherlock.validate_email("email@example.com")
print(result)

# Validate multiple emails
emails = ["email1@example.com", "email2@example.com"]
results = sherlock.validate_emails(emails)
for result in results:
    print(result)
```

## 📊 Output

The script will generate a CSV file with the following columns:
- Email
- School (if provided in the input)
- Valid (True/False)
- Confidence Score (0-100%)
- Notes

Additionally, a disclaimer about the limitations of email validation will be included at the top of the output file.

## 💯 Confidence Score Explanation

- 100%: Valid format, DNS records, MX records, and responsive SMTP server
- 75%: Valid format, DNS records, and MX records, but unresponsive SMTP server
- 50%: Valid format and DNS records, but no MX records
- 25%: Valid format and DNS records, but no MX records and unresponsive SMTP server
- 0%: Invalid format, no valid DNS records, or explicitly rejected by SMTP server

## ⚠️ Limitations

EmailSherlock provides an estimate of email validity based on DNS and SMTP checks. However, it cannot guarantee that an email address is actually in use or will successfully receive emails. The only way to be certain is to send an actual email and confirm receipt.

## 🔮 Future Enhancements

- Implement rate limiting to avoid overwhelming email servers or getting blocked
- Add a delay between validation attempts for the same domain to reduce the load on email servers
- Implement a caching mechanism for DNS and SMTP results to speed up validation for repeated domains
- Add more sophisticated patterns for email format validation, such as checking for common typos or invalid TLDs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Support the Project

If you find EmailSherlock useful, you can buy me a coffee:

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/yourusername)
