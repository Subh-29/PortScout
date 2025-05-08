# 🔍 Port Scanner + Banner Grabber

A simple yet powerful multi-threaded **Python port scanner** with **banner grabbing** and **SSL certificate inspection**. This tool helps you identify open ports, fetch HTTP response headers, and extract SSL/TLS certificate info from HTTPS-enabled services.

## 🚀 Features

- Scans ports 1–1023 with multi-threading (up to 300 threads)
- Grabs HTTP response banners on port 80
- Extracts SSL certificate subject & TLS version on port 443
- Saves results to `.json` or `.txt`
- Colorful terminal output using `colorama`

## 🔧 Requirements

- Python 3.x
- `colorama` library

Install with:
```bash
pip install colorama

```

---

## 🧠 How It Works

1. Enter a target IP or domain
2. Tool scans ports 1 to 1023
3. For each open port:

   * **Port 80**: sends HTTP HEAD request and grabs banner
   * **Port 443**: initiates SSL handshake, extracts certificate info
4. Results are displayed and optionally saved in `.json` or `.txt` format

---

## 💻 Sample Terminal Output (Masked)

```
Enter target IP or Domain Name: example.com

 ====> Banner on Port 80 : HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Set-Cookie: JSESSIONID=****************************; Path=/; HttpOnly
Content-Type: text/html;charset=ISO-8859-1
Date: Thu, 08 May 2025 13:31:02 GMT
Connection: close

 [+] Port 443 is OPEN

   └─>SSL/TLS Version: TLSv1.2

   └─>Certificate Subject: ((('commonName', 'example.com'),),)

   └─>IP: xxx.xxx.xxx.xxx

Save results as (json/txt)? json
[✔] Results saved to scan_results_YYYYMMDD_HHMMSS.json
```

> ⚠️ **Note**: Output above is masked for privacy. Actual banners will include raw headers and certificate details.

---

## 📦 Sample JSON Output

```json
[
    {
        "port": 80,
        "status": "open",
        "banner": "HTTP/1.1 200 OK\r\nServer: Apache-Coyote/1.1\r\nSet-Cookie: JSESSIONID=****************************; Path=/; HttpOnly\r\nContent-Type: text/html;charset=ISO-8859-1\r\nDate: Thu, 08 May 2025 13:36:16 GMT\r\nConnection: close"
    },
    {
        "port": 443,
        "status": "open",
        "banner": [
            [
                [
                    [
                        "commonName",
                        "example.com"
                    ]
                ]
            ],
            [
                "xxx.xxx.xxx.xxx",
                443
            ]
        ]
    }
]
```

---

## 📁 Output Files

* `scan_results_YYYYMMDD_HHMMSS.json` – structured JSON with banners and SSL info
* `scan_results_YYYYMMDD_HHMMSS.txt` – plain readable list of open ports and banners

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes only**.
Scanning systems without permission is **unauthorized**, may be **illegal**, and is **strictly discouraged**.

Use only on systems:

* You **own**
* Have **written consent** to test

---

## 🧠 Future Ideas

* `argparse` for CLI flags
* Live progress bar
* Export results in CSV
* OS detection & service guessing

---

## 🤝 Contributing

Pull requests, issues, and ideas are welcome!

---


