# GitHub Authentication Guide for Zelyo

To enable Zelyo to create Pull Requests in Organization repositories, you need to authenticate with GitHub.

## Option 1: GitHub App (Recommended for Organizations)
This offers the best security and avoids using personal user accounts.

### 1. Create the GitHub App
1.  Go to **Organization Settings** > **Developer settings** > **GitHub Apps** > **New GitHub App**.
2.  **Name**: `Zelyo Config Guardian` (or similar).
3.  **Homepage URL**: `https://zelyo.io` (or placeholder).
4.  **Webhook**: Uncheck "Active" (we don't need webhooks yet).
5.  **Repository permissions**:
    *   **Contents**: `Read and Write`
    *   **Pull requests**: `Read and Write`
    *   **Metadata**: `Read Only`
6.  **Where can this GitHub App be installed?**: "Any account on this web service" (or "Only on this account").
7.  Click **Create GitHub App**.

### 2. Get Credentials
After creating the app, collect the following:
*   **App ID**: Displayed on the "About" page (e.g., `123456`).
*   **Private Key**: Scroll down to "Private keys" and click **Generate a private key**. This downloads a `.pem` file.

### 3. Install the App
1.  Go to **Install App** in the left sidebar.
2.  Click **Install** next to your Organization.
3.  Select **All repositories** (or specific ones).
4.  Click **Install**.
5.  **Installation ID**: Look at the URL in your browser after installation:
    `https://github.com/organizations/YOUR_ORG/settings/installations/12345678`
    The number at the end (`12345678`) is your `GITHUB_APP_INSTALLATION_ID`.

### 4. Configure Zelyo
Set the following environment variables (or Secrets):
*   `GITHUB_APP_ID`: The App ID.
*   `GITHUB_APP_PRIVATE_KEY`: The contents of the `.pem` file.
*   `GITHUB_APP_INSTALLATION_ID`: The installation ID.

---

## Option 2: Fine-grained Personal Access Token
Useful for personal testing or if you cannot create Apps.

1.  Go to **GitHub Settings** > **Developer settings** > **Personal access tokens** > **Fine-grained tokens**.
2.  Click **Generate new token**.
3.  **Resource owner**: Select your Organization (**Crucial!**).
4.  **Repository access**: Select **All repositories**.
5.  **Permissions**:
    *   **Contents**: `Read and Write`
    *   **Pull requests**: `Read and Write`
6.  Use as `GITHUB_TOKEN`.

---

## Option 3: Classic Personal Access Token
**Not recommended** for Organizations due to SSO complexity.
1.  Select `repo` scope.
2.  **Authorize SSO** for your organization.
