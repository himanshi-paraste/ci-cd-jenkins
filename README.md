
# 🚀 Python CI/CD Pipeline using Jenkins, GitHub, Docker & AWS EC2

This project demonstrates how to build a simple CI/CD pipeline that deploys a Python Flask application using Jenkins, Docker, GitHub, and AWS EC2.

---

## 📌 What You'll Do

- Create a basic Python Flask app
- Containerize it using Docker
- Push the code to GitHub
- Set up Jenkins on an AWS EC2 instance
- Build a CI/CD pipeline to automatically deploy the app when code changes

---

## 🧱 Prerequisites

- AWS EC2 instance (Ubuntu)
- Port 8080 and 5000 open in security group
- Jenkins installed and running
- Docker installed on EC2
- GitHub account and repo created
- `git`, `python3`, and `pip` installed

---

Let’s begin by setting up the core files: app.py, Dockerfile, and requirements.txt.
Alternatively, you can clone the repository and start directly from Step 4

ci-cd-jenkins/
├── app.py
├── Dockerfile
├── requirements.txt


---

## 🔨 Step 1: Create Your Python Flask App on Notepad or any editor

1. Create a file called `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    a = 5
    b = 7
    result = a + b
    return f"<h1>Addition Result:</h1><p>{a} + {b} = {result}</p>"

if __name__ == '__main__':
    print("Hello from Jenkins CI/CD pipeline test!")
    app.run(host='0.0.0.0', port=5000)
```

2. Create `requirements.txt`:

```
Flask==2.2.5

```

3. Test locally (optional):

```bash
pip install -r requirements.txt
python3 app.py
```

---

## 🐳 Step 2: Dockerize the App

Docker is what we use to package our app along with all its dependencies, so it can run the same way in any environment—whether it’s on the cloud or our local machine. This helps us keep everything consistent and avoid the “it works on my machine” problem.


Create a `Dockerfile` in the same directory:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```


---

## 🧑‍💻 Step 3: Push Code to GitHub

1. Initialize git:

```bash
git init
git remote add origin https://github.com/<your-username>/<your-repo>.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## ⚙️ Step 4: Set Up Jenkins on EC2

EC2 (Elastic Compute Cloud) is the virtual machine we use in the cloud. We will install Jenkins an java on it and host our app here. It gives us a stable server where we can run all our continuous integration and deployment (CI/CD) tasks smoothly.


1. Install java and Jenkins:

```bash

sudo apt update
sudo apt install fontconfig openjdk-21-jre

```
Add Jenkins GPG key:

```bash

sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key


```
Add Jenkins repo:

```bash

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null


```
Update apt and install Jenkins:

```bash

sudo apt update
sudo apt install jenkins


```


2. Start  and enable Jenkins:

```bash
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo systemctl status jenkins

```

3. Access Jenkins on:

```
http://<EC2-IP>:8080


```

If It Doesn’t Work

```bash
sudo journalctl -u jenkins -xe


```



📷 ![Jenkins page](screenshorts/pic1.png)


After starting Jenkins, get the initial admin password by running:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

```

4. Install recommended plugins and create an admin user.

---


## 📦 Step 5: Create Jenkins Freestyle Job

📷 ![Jenkins page](screenshorts/pic2.png)

1. New Item → Freestyle Project → `python-ci-cd`
General
- Add a **Description** (optional).
- Check **"This project is parameterized"** (optional).
- Check **"GitHub project"**.
- Enter your GitHub project URL:  
  Example: `https://github.com/yourusername/your-repo`

# Source Code Management
- Select **Git**.
- In **Repository URL**, paste your GitHub SSH URL:  
  Example: `git@github.com:yourusername/your-repo.git`


# Credentials (Add SSH Key)
 **Generate SSH Key on EC2**  
   Run on your EC2 instance (Jenkins server):
   ```bash
   ssh-keygen

This generates two files:

 (Private Key)

 (Public Key)


# Add Public Key to GitHub

- Go to GitHub > Settings > SSH and GPG keys > New SSH key

- Title: jenkins-project

- Key: Paste content from cat ~/.ssh/id_rsa.pub

- Click Add SSH key

- Add Credentials in Jenkins

# Back on Jenkins:

- Click “Add” (next to Credentials)

- Select Kind: SSH Username with private key

- ID: ubuntu (or any identifier you prefer)

- Username: ubuntu

- Private Key: Paste content from cat ~/.ssh/id_rsa

- Add a description

- Click Add

Select the Credential

Under Source Code Management, select your added credential (e.g., ubuntu) from the dropdown.

Branches to Build
Enter your Git branch:
Example: */main or */master

Now your Jenkins is connected to your GitHub repository using SSH credentials securely.



📷 ![Jenkins page](screenshorts/pic3.png)



---

## 📦 Step 6: Install docker on EC2


Since the Dockerfile is already in your GitHub repository, you only need to install Docker on the EC2 instance to automate the build and deployment process.


```bash
sudo apt install docker.io 
sudo usermod -aG docker ubuntu
sudo reboot
docker build -t python-app .
sudo docker run -d --name python-app -p 5000:5000 python-app
docker ps

```

---

## 📦 Step 7: Configure Build Steps

now go to configure


 Under **Build Steps → Execute shell**: ADD THESE COMMANDS

```bash
#!/bin/bash

# Define container and image names
CONTAINER_NAME=myapp
IMAGE_NAME=myapp-image

# Stop and remove existing container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Remove old image if needed
docker rmi -f $IMAGE_NAME

# Build new Docker image
docker build -t $IMAGE_NAME .

# Run new container
docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME

```


APPLY AND SAVE

---
## 📦 Step 8: Github webhook integration

# Install GitHub Plugin in Jenkins

1. Go to **Jenkins Dashboard → Manage Jenkins → Manage Plugins**
2. Open the **Available** tab, search for **GitHub Plugin**
3. Select it and click **Install without restart**

# Configure Jenkins to Receive GitHub Webhooks

1. Go to your Jenkins project → **Configure**
2. Under **Build Triggers**, check **GitHub hook trigger for GITScm polling**

# Create GitHub Webhook

1. Go to your GitHub repository → **Settings → Webhooks**
2. Click **Add webhook**
3. In **Payload URL**, enter your Jenkins server webhook URL:http://<JENKINS_URL>/github-webhook/
 Replace `<JENKINS_URL>` with your Jenkins server URL (e.g., `http://your-ec2-ip:8080`)

4. Content type: `application/json`
5. Select **Just the push event**
6. Click **Add webhook**

Under **Build Triggers**:
   - Check: `GitHub hook trigger for GITScm polling`

---

# Test the Webhook

- Push a commit to your GitHub repo
- Jenkins should automatically start the build

---

✅ Your Jenkins is now integrated with GitHub via webhook for automated builds!

## 🔁 Step 9: Test Your CI/CD Pipeline

1. Make a small change in your `app.py` or any file.
2. Commit and push to GitHub:

```bash
git add .
git commit -m "Test Jenkins pipeline"
git push
```

3. Jenkins should auto-trigger the build, rebuild Docker image, and deploy.

---

## 🌐 Step 10: Access the Flask App in Browser

Open:

```
http://<your-ec2-ip>:5000
```

You should see:

```
Addition Result:
5 + 7 = 12
```
📷 ![Result page](screenshorts/pic4.png)

---


## ✅ Troubleshooting Tips

-  Port already in use? Run: sudo docker ps -a and docker rm -f <container-id>
- Docker permission error? Run sudo usermod -aG docApp not loading? Check EC2 security group and Jenkins logs
- Webhook not triggering? Recheck webhook URL and payload settings

---


