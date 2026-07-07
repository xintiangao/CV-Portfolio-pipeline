# Google Docs to Independent Portfolio Sync Pipeline 🚀

An automated CI/CD pipeline to use **Google Docs as a Headless CMS** for a standalone custom web portfolio (e.g., syncing data layers directly to a remote production web host).

## 🛠️ Configuration & Secrets Layout

To deploy this yourself, fork this repository and add the following **GitHub Actions Secrets** under `Settings -> Secrets and variables -> Actions`:

* `GOOGLE_DOC_ID`: The unique file string found in your Google Doc URL.
* `GOOGLE_SERVICE_ACCOUNT_JSON`: The complete plaintext content of your Google Service Account JSON Key file.
* `SERVER_HOST`: Public IP address or domain name of your web hosting server.
* `SERVER_USER`: SSH username for your server (e.g., `root`, `ubuntu`).
* `SERVER_REMOTE_DIR`: Absolute path to your website’s public directory on the server (e.g., `/var/www/xintiangao.com/html`).
* `SERVER_SSH_PRIVATE_KEY`: Your SSH private key used to connect to your remote instance securely.