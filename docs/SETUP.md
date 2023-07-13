# Installation
Following are steps that need to be taken before running any part of our codebase

### Requirement
   - Linux/WSL or MacOS
   - Anaconda*-*-Linux-x86_64.sh
   - Python 3.8.x

## Step-by-step instructions
Clone git repo using 
```bash
git clone https://github.com/jangid-deepak/hcp-profiler.git
cd hcp-profiler
```

### **Install conda for interpreter**

#### Downlaod the installer script using

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
```
#### Run the installer script using
```bash
bash Anaconda3-2022.10-Linux-x86_64.sh
```
[learn more](https://www.how2shout.com/how-to/install-anaconda-wsl-windows-10-ubuntu-linux-app.html) about conda installation

#### create conda environment
```bash
conda env create -f environment.yml
```
